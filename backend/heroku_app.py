#!/usr/bin/env python3
"""
Heroku JobHunter LEGO System
Automated job hunting with 6 AM weekday scheduling
"""
import os
import sys
import asyncio
import logging
from datetime import datetime, time
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging for Heroku
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import scheduler components after path setup
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz
    SCHEDULER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Scheduler not available: {e}")
    SCHEDULER_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="JobHunter LEGO System",
    description="Automated job hunting with intelligent template customization",
    version="1.0.0"
)

# Initialize scheduler if available
scheduler = None
if SCHEDULER_AVAILABLE:
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Stockholm'))

@app.on_event("startup")
async def startup_event():
    """Start the scheduler when app starts"""
    try:
        if SCHEDULER_AVAILABLE and scheduler:
            # Schedule daily job hunting at 6:00 AM Stockholm time, Monday-Friday
            scheduler.add_job(
                run_daily_lego_automation,
                CronTrigger(
                    hour=6,
                    minute=0,
                    day_of_week='mon-fri',
                    timezone=pytz.timezone('Europe/Stockholm')
                ),
                id='daily_job_hunt',
                name='Daily LEGO Job Hunting',
                replace_existing=True
            )
            
            scheduler.start()
            logger.info("🚀 JobHunter LEGO System started with 6 AM weekday scheduling")
            logger.info("📅 Next run: Monday-Friday at 6:00 AM Stockholm time")
        else:
            logger.info("🚀 JobHunter LEGO System started (scheduler disabled)")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler when app stops"""
    if scheduler:
        scheduler.shutdown()
    logger.info("🛑 JobHunter LEGO System stopped")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "JobHunter LEGO System",
        "next_scheduled_run": get_next_run_time(),
        "timezone": "Europe/Stockholm",
        "schedule": "Monday-Friday at 6:00 AM",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    scheduler_info = {
        "scheduler_available": SCHEDULER_AVAILABLE,
        "scheduler_running": scheduler.running if scheduler else False,
        "jobs_scheduled": len(scheduler.get_jobs()) if scheduler else 0,
    }
    
    return {
        "status": "healthy",
        **scheduler_info,
        "next_run": get_next_run_time(),
        "system_time": datetime.now().isoformat(),
        "stockholm_time": datetime.now(pytz.timezone('Europe/Stockholm')).isoformat() if SCHEDULER_AVAILABLE else "N/A"
    }

@app.post("/trigger/manual-run")
async def manual_trigger(background_tasks: BackgroundTasks):
    """Manual trigger for testing"""
    logger.info("🔧 Manual automation triggered via master orchestrator")
    background_tasks.add_task(run_daily_lego_automation)
    return {
        "status": "triggered",
        "message": "Manual automation started using master orchestrator",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/run-automation")
async def run_automation_sync():
    """Synchronous automation run for immediate results"""
    try:
        logger.info("🚀 Running automation synchronously...")
        
        # Import and run master orchestrator
        try:
            from master_automation_orchestrator import MasterAutomationOrchestrator
            orchestrator = MasterAutomationOrchestrator()
            
            # Run the complete automation workflow
            await orchestrator.run_complete_automation()
            
            return {
                "status": "success",
                "message": f"Automation completed: {orchestrator.successful_applications} applications sent",
                "successful_applications": orchestrator.successful_applications,
                "failed_applications": orchestrator.failed_applications,
                "execution_time": orchestrator._get_execution_time(),
                "timestamp": datetime.now().isoformat()
            }
        except ImportError as e:
            logger.error(f"❌ Import error: {e}")
            return {
                "status": "error",
                "message": f"Import error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"❌ Automation failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/status/next-jobs")
async def get_scheduled_jobs():
    """Get information about scheduled jobs"""
    if not scheduler:
        return {
            "scheduled_jobs": [],
            "scheduler_running": False,
            "scheduler_available": SCHEDULER_AVAILABLE,
            "timezone": "Europe/Stockholm"
        }
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    
    return {
        "scheduled_jobs": jobs,
        "scheduler_running": scheduler.running,
        "scheduler_available": SCHEDULER_AVAILABLE,
        "timezone": "Europe/Stockholm"
    }

def get_next_run_time():
    """Get next scheduled run time"""
    if not scheduler:
        return None
    jobs = scheduler.get_jobs()
    if jobs:
        next_run = jobs[0].next_run_time
        return next_run.isoformat() if next_run else None
    return None

async def run_daily_lego_automation():
    """Daily automation task using master orchestrator"""
    try:
        logger.info("🎯 Starting daily automation at 6 AM via master orchestrator...")
        
        # Import and run master orchestrator
        try:
            from master_automation_orchestrator import MasterAutomationOrchestrator
            
            orchestrator = MasterAutomationOrchestrator()
            await orchestrator.run_complete_automation()
            
            logger.info(f"🎉 Daily automation completed: {orchestrator.successful_applications} applications sent")
        except ImportError as e:
            logger.error(f"❌ Import error in daily automation: {e}")
        
    except Exception as e:
        logger.error(f"❌ Daily automation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Get port from environment (Heroku sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the app
    uvicorn.run(
        "heroku_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )