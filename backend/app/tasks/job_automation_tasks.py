from celery import Celery
from celery.schedules import crontab
from datetime import datetime
import logging
import asyncio
from app.core.config import settings

# Initialize Celery
celery_app = Celery(
    "jobhunter",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.job_automation_tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Stockholm",  # Swedish timezone
    enable_utc=True,
    
    # Task routing
    task_routes={
        "app.tasks.job_automation_tasks.run_daily_job_automation": {"queue": "job_automation"},
        "app.tasks.job_automation_tasks.send_daily_summary": {"queue": "notifications"},
    },
    
    # Beat schedule for automated tasks
    beat_schedule={
        # Daily job automation - 6:00 AM on weekdays only
        "daily-job-automation": {
            "task": "app.tasks.job_automation_tasks.run_daily_job_automation",
            "schedule": crontab(
                hour=6, 
                minute=0, 
                day_of_week="1,2,3,4,5"  # Monday=1 through Friday=5
            ),
            "args": ("default_user_id",),  # You'll need to set the actual user ID
        },
        
        # Send daily summary at 8:00 AM on weekdays (after job processing)
        "daily-summary-email": {
            "task": "app.tasks.job_automation_tasks.send_daily_summary",
            "schedule": crontab(
                hour=8, 
                minute=0, 
                day_of_week="1,2,3,4,5"
            ),
            "args": ("default_user_id",),
        },
        
        # Weekly cleanup of old processed jobs (Sundays at 2:00 AM)
        "weekly-cleanup": {
            "task": "app.tasks.job_automation_tasks.cleanup_old_jobs",
            "schedule": crontab(
                hour=2, 
                minute=0, 
                day_of_week=0  # Sunday
            ),
        },
    },
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def run_daily_job_automation_task(self, user_id: str):
    """
    Celery task for daily job automation
    Runs at 6:00 AM on weekdays (Monday-Friday)
    """
    try:
        logger.info("Starting daily job automation task for user: %s", user_id)
        
        # Import here to avoid circular imports
        from app.services.job_automation_service import JobAutomationService
        
        # Create event loop for async code
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            automation_service = JobAutomationService()
            result = loop.run_until_complete(
                automation_service.run_daily_job_automation(user_id)
            )
            
            logger.info("Daily automation completed: %s", result)
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Error in daily job automation task: %s", e)
        
        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            logger.info("Retrying task in %d seconds...", 2 ** self.request.retries * 60)
            raise self.retry(countdown=2 ** self.request.retries * 60)
        else:
            logger.error("Max retries reached for daily automation task")
            return {"status": "error", "error": str(e)}

@celery_app.task(bind=True)
def send_daily_summary_task(self, user_id: str):
    """Send daily summary email"""
    try:
        logger.info("Sending daily summary for user: %s", user_id)
        
        from app.services.email_automation_service import EmailAutomationService
        from app.core.database import get_database
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            async def send_summary():
                # Get today's automation results
                db = await get_database()
                today = datetime.utcnow().date()
                
                # Get automation run results
                automation_result = await db.automation_runs.find_one({
                    "user_id": user_id,
                    "run_date": {
                        "$gte": datetime.combine(today, datetime.min.time()),
                        "$lt": datetime.combine(today, datetime.max.time())
                    }
                })
                
                # Get processed jobs
                processed_jobs = await db.processed_jobs.find({
                    "user_id": user_id,
                    "processed_at": {
                        "$gte": datetime.combine(today, datetime.min.time()),
                        "$lt": datetime.combine(today, datetime.max.time())
                    }
                }).to_list(length=None)
                
                if automation_result:
                    email_service = EmailAutomationService()
                    success = await email_service.send_daily_summary_email(
                        to_email="leeharvad@gmail.com",
                        automation_results=automation_result,
                        processed_jobs=processed_jobs
                    )
                    
                    return {"status": "success", "email_sent": success}
                else:
                    return {"status": "no_data", "message": "No automation results found for today"}
            
            result = loop.run_until_complete(send_summary())
            logger.info("Daily summary completed: %s", result)
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Error sending daily summary: %s", e)
        return {"status": "error", "error": str(e)}

@celery_app.task
def cleanup_old_jobs_task():
    """Weekly cleanup of old processed jobs (older than 30 days)"""
    try:
        logger.info("Starting weekly cleanup of old jobs")
        
        from app.core.database import get_database
        from datetime import timedelta
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            async def cleanup():
                db = await get_database()
                cutoff_date = datetime.utcnow() - timedelta(days=30)
                
                # Remove old processed jobs
                result = await db.processed_jobs.delete_many({
                    "processed_at": {"$lt": cutoff_date}
                })
                
                # Remove old automation runs
                result2 = await db.automation_runs.delete_many({
                    "run_date": {"$lt": cutoff_date}
                })
                
                return {
                    "processed_jobs_deleted": result.deleted_count,
                    "automation_runs_deleted": result2.deleted_count
                }
            
            result = loop.run_until_complete(cleanup())
            logger.info("Cleanup completed: %s", result)
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Error in cleanup task: %s", e)
        return {"status": "error", "error": str(e)}

# Manual trigger tasks (for testing)
@celery_app.task
def test_job_automation_task(user_id: str):
    """Manual test of job automation (for development/testing)"""
    logger.info("Running test job automation for user: %s", user_id)
    return run_daily_job_automation_task.delay(user_id)

@celery_app.task
def test_email_task(user_id: str):
    """Test email functionality"""
    try:
        from app.services.email_automation_service import EmailAutomationService
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            async def test_email():
                email_service = EmailAutomationService()
                return await email_service.test_email_connection()
            
            result = loop.run_until_complete(test_email())
            return result
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error("Error testing email: %s", e)
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # For development - run celery worker
    celery_app.start()