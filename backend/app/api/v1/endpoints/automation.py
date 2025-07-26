from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import logging

from app.api.v1.endpoints.auth import get_current_user
from app.services.job_automation_service import JobAutomationService
from app.services.email_automation_service import EmailAutomationService
from app.tasks.job_automation_tasks import (
    test_job_automation_task, 
    test_email_task,
    run_daily_job_automation_task
)
from app.core.database import get_async_session

router = APIRouter()
logger = logging.getLogger(__name__)

class AutomationConfig(BaseModel):
    """Automation configuration settings"""
    enabled: bool = Field(True, description="Enable/disable automation")
    email_notifications: bool = Field(True, description="Send email notifications")
    max_applications_per_day: int = Field(10, ge=1, le=50, description="Max applications per day")
    target_email: str = Field("leeharvard@gmail.com", description="Email to send applications to")

class AutomationStats(BaseModel):
    """Automation statistics"""
    total_runs: int
    total_applications: int
    success_rate: float
    last_run: Optional[datetime]
    applications_this_week: int
    companies_applied: List[str]

class JobFilter(BaseModel):
    """Job filtering criteria"""
    max_experience_years: int = 5
    swedish_level: str = "B2"
    required_skills: List[str] = []
    excluded_companies: List[str] = []
    min_salary: Optional[int] = None

@router.get("/status")
async def get_automation_status(
    current_user: dict = Depends(get_current_user)
):
    """Get current automation system status"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # Get automation service
        automation_service = JobAutomationService()
        
        # Get recent stats
        stats = await automation_service.get_automation_stats(user_id, days=7)
        
        # Check if automation is enabled
        db = await get_database()
        user = await db.users.find_one({"_id": user_id})
        automation_config = user.get("automation_config", {}) if user else {}
        
        return {
            "automation_enabled": automation_config.get("enabled", True),
            "email_notifications": automation_config.get("email_notifications", True),
            "target_email": automation_config.get("target_email", "leeharvad@gmail.com"),
            "schedule": "Weekdays at 06:00 CET",
            "stats": stats,
            "next_run": "Next weekday at 06:00 CET",
            "system_status": "active"
        }
        
    except Exception as e:
        logger.error("Error getting automation status: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get automation status: {str(e)}")

@router.post("/configure")
async def configure_automation(
    config: AutomationConfig,
    current_user: dict = Depends(get_current_user)
):
    """Configure automation settings"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # Save configuration to database
        db = await get_database()
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "automation_config": config.dict(),
                    "automation_updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        logger.info("Automation configuration updated for user: %s", user_id)
        
        return {
            "message": "Automation configuration updated successfully",
            "config": config.dict(),
            "next_run": "Next weekday at 06:00 CET" if config.enabled else "Disabled"
        }
        
    except Exception as e:
        logger.error("Error configuring automation: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to configure automation: {str(e)}")

@router.post("/test-run")
async def test_automation_run(
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Manually trigger a test run of the automation system"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        logger.info("Manual test automation triggered by user: %s", user_id)
        
        # Run automation in background
        task = test_job_automation_task.delay(user_id)
        
        return {
            "message": "Test automation run started",
            "task_id": task.id,
            "status": "running",
            "note": "This will process a limited number of jobs for testing. Check your email for results."
        }
        
    except Exception as e:
        logger.error("Error starting test automation: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to start test automation: {str(e)}")

@router.post("/test-email")
async def test_email_connection(
    current_user: dict = Depends(get_current_user)
):
    """Test email connection and send a test email"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # Test email connection
        task = test_email_task.delay(user_id)
        result = task.get(timeout=30)  # Wait up to 30 seconds
        
        if result.get("status") == "success":
            # Send test email
            email_service = EmailAutomationService()
            test_job = {
                "title": "Test Position - Software Developer",
                "company": "Test Company AB",
                "location": "Stockholm, Sweden",
                "url": "https://example.com/test-job",
                "source": "automation_test",
                "posting_date": datetime.utcnow()
            }
            
            email_sent = await email_service.send_application_email(
                to_email="leeharvad@gmail.com",
                subject="TEST: JobHunter Automation System",
                body="This is a test email from the JobHunter automation system to verify email functionality.",
                cv_content=b"",  # Empty for test
                cover_letter_content=b"",  # Empty for test
                job_data=test_job
            )
            
            return {
                "email_connection": result,
                "test_email_sent": email_sent,
                "message": "Email test completed. Check leeharvad@gmail.com for test email."
            }
        else:
            return {
                "email_connection": result,
                "test_email_sent": False,
                "message": "Email connection failed. Please check SMTP configuration."
            }
        
    except Exception as e:
        logger.error("Error testing email: %s", e)
        raise HTTPException(status_code=500, detail=f"Email test failed: {str(e)}")

@router.get("/stats")
async def get_automation_statistics(
    days: int = Query(30, ge=1, le=365, description="Number of days to include in statistics"),
    current_user: dict = Depends(get_current_user)
):
    """Get detailed automation statistics"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        automation_service = JobAutomationService()
        stats = await automation_service.get_automation_stats(user_id, days)
        
        # Get additional database stats
        db = await get_database()
        
        # Applications by day
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "processed_at": {
                        "$gte": datetime.utcnow() - datetime.timedelta(days=days)
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$processed_at"
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        daily_stats = await db.processed_jobs.aggregate(pipeline).to_list(length=None)
        
        # Top companies applied to
        company_pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "processed_at": {
                        "$gte": datetime.utcnow() - datetime.timedelta(days=days)
                    }
                }
            },
            {
                "$group": {
                    "_id": "$company",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        company_stats = await db.processed_jobs.aggregate(company_pipeline).to_list(length=None)
        
        return {
            **stats,
            "daily_applications": daily_stats,
            "top_companies": company_stats,
            "period_days": days
        }
        
    except Exception as e:
        logger.error("Error getting automation statistics: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.get("/processed-jobs")
async def get_processed_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    company: Optional[str] = Query(None, description="Filter by company name"),
    date_from: Optional[date] = Query(None, description="Filter jobs from date"),
    date_to: Optional[date] = Query(None, description="Filter jobs to date"),
    current_user: dict = Depends(get_current_user)
):
    """Get list of processed jobs with filtering"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # Build query
        query = {"user_id": user_id}
        
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        
        if date_from or date_to:
            date_query = {}
            if date_from:
                date_query["$gte"] = datetime.combine(date_from, datetime.min.time())
            if date_to:
                date_query["$lte"] = datetime.combine(date_to, datetime.max.time())
            query["processed_at"] = date_query
        
        # Get jobs from database
        db = await get_database()
        
        # Get total count
        total_count = await db.processed_jobs.count_documents(query)
        
        # Get jobs with pagination
        jobs = await db.processed_jobs.find(query)\
            .sort("processed_at", -1)\
            .skip(skip)\
            .limit(limit)\
            .to_list(length=limit)
        
        # Convert ObjectIds to strings
        for job in jobs:
            job["_id"] = str(job["_id"])
        
        return {
            "jobs": jobs,
            "total_count": total_count,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total_count
        }
        
    except Exception as e:
        logger.error("Error getting processed jobs: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get processed jobs: {str(e)}")

@router.delete("/processed-jobs/{job_id}")
async def delete_processed_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a processed job record"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        db = await get_database()
        
        # Delete the job
        result = await db.processed_jobs.delete_one({
            "_id": job_id,
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Processed job not found")
        
        return {"message": "Processed job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting processed job: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to delete processed job: {str(e)}")

@router.post("/pause")
async def pause_automation(
    current_user: dict = Depends(get_current_user)
):
    """Pause automation system"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        db = await get_database()
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "automation_config.enabled": False,
                    "automation_paused_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "message": "Automation paused successfully",
            "status": "paused",
            "note": "Automation will not run until resumed"
        }
        
    except Exception as e:
        logger.error("Error pausing automation: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to pause automation: {str(e)}")

@router.post("/resume")
async def resume_automation(
    current_user: dict = Depends(get_current_user)
):
    """Resume automation system"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        db = await get_database()
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "automation_config.enabled": True,
                    "automation_resumed_at": datetime.utcnow()
                },
                "$unset": {
                    "automation_paused_at": ""
                }
            }
        )
        
        return {
            "message": "Automation resumed successfully",
            "status": "active",
            "next_run": "Next weekday at 06:00 CET"
        }
        
    except Exception as e:
        logger.error("Error resuming automation: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to resume automation: {str(e)}")

@router.get("/logs")
async def get_automation_logs(
    limit: int = Query(100, ge=1, le=500),
    level: Optional[str] = Query(None, description="Filter by log level"),
    current_user: dict = Depends(get_current_user)
):
    """Get automation system logs"""
    try:
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        # This would typically connect to your logging system
        # For now, return recent automation runs as "logs"
        db = await get_database()
        
        query = {"user_id": user_id}
        logs = await db.automation_runs.find(query)\
            .sort("run_date", -1)\
            .limit(limit)\
            .to_list(length=limit)
        
        # Convert to log format
        log_entries = []
        for log in logs:
            log_entries.append({
                "timestamp": log.get("run_date"),
                "level": "INFO" if log.get("status") == "completed" else "ERROR",
                "message": f"Automation run completed: {log.get('applications_sent', 0)} applications sent",
                "details": log
            })
        
        return {
            "logs": log_entries,
            "total_entries": len(log_entries),
            "note": "Showing automation run results. For detailed logs, check server log files."
        }
        
    except Exception as e:
        logger.error("Error getting automation logs: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")