#!/usr/bin/env python3
"""
JobHunter Dashboard - Professional web interface for job hunting automation
Designed for integration with bluehawana.com/jobs
"""
import os
import asyncio
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get configuration for custom domain support
BASE_PATH = os.getenv('BASE_PATH', '')
CUSTOM_DOMAIN = os.getenv('CUSTOM_DOMAIN', '')

# Initialize FastAPI app
app = FastAPI(
    title="JobHunter Dashboard",
    description="Professional job hunting automation dashboard",
    version="2.0.0",
    root_path=BASE_PATH  # Support for bluehawana.com/jobs
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize scheduler
scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Stockholm'))

class JobHunterDashboard:
    """Dashboard controller for job hunting automation"""
    
    def __init__(self):
        self.automation_running = False
        self.last_execution = None
        self.execution_history = []
        self.stats = {
            "total_jobs_found": 0,
            "total_applications_sent": 0,
            "success_rate": 0.0,
            "last_run": None
        }
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        return {
            "status": {
                "automation_running": self.automation_running,
                "scheduler_active": scheduler.running,
                "next_scheduled_run": self._get_next_run_time(),
                "last_execution": self.last_execution
            },
            "stats": self.stats,
            "recent_executions": self.execution_history[-10:],  # Last 10 runs
            "schedule_info": {
                "timezone": "Europe/Stockholm",
                "frequency": "Monday-Friday at 6:00 AM",
                "enabled": True
            }
        }
    
    def _get_next_run_time(self) -> Optional[str]:
        """Get next scheduled run time"""
        jobs = scheduler.get_jobs()
        if jobs:
            next_run = jobs[0].next_run_time
            return next_run.isoformat() if next_run else None
        return None
    
    async def run_automation(self) -> Dict[str, Any]:
        """Run the automation and return results"""
        if self.automation_running:
            raise HTTPException(status_code=409, detail="Automation already running")
        
        try:
            self.automation_running = True
            start_time = datetime.now()
            
            # Import and run master orchestrator
            from master_automation_orchestrator import MasterAutomationOrchestrator
            orchestrator = MasterAutomationOrchestrator()
            
            await orchestrator.run_complete_automation()
            
            # Update stats
            execution_result = {
                "timestamp": start_time.isoformat(),
                "duration": orchestrator._get_execution_time(),
                "jobs_found": len(orchestrator.processed_jobs),
                "successful_applications": orchestrator.successful_applications,
                "failed_applications": orchestrator.failed_applications,
                "success_rate": f"{(orchestrator.successful_applications / max(len(orchestrator.processed_jobs), 1) * 100):.1f}%"
            }
            
            self.execution_history.append(execution_result)
            self.last_execution = execution_result
            
            # Update overall stats
            self.stats["total_jobs_found"] += len(orchestrator.processed_jobs)
            self.stats["total_applications_sent"] += orchestrator.successful_applications
            self.stats["last_run"] = start_time.isoformat()
            
            if self.stats["total_jobs_found"] > 0:
                self.stats["success_rate"] = (self.stats["total_applications_sent"] / self.stats["total_jobs_found"]) * 100
            
            return execution_result
            
        finally:
            self.automation_running = False

# Initialize dashboard controller
dashboard = JobHunterDashboard()

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on startup"""
    try:
        # Schedule daily automation
        scheduler.add_job(
            run_scheduled_automation,
            CronTrigger(
                hour=6,
                minute=0,
                day_of_week='mon-fri',
                timezone=pytz.timezone('Europe/Stockholm')
            ),
            id='daily_job_hunt',
            name='Daily Job Hunting Automation',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("🚀 JobHunter Dashboard started with scheduling")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    scheduler.shutdown()
    logger.info("🛑 JobHunter Dashboard stopped")

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard page"""
    dashboard_data = await dashboard.get_dashboard_data()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": dashboard_data,
        "page_title": "JobHunter Dashboard",
        "base_path": BASE_PATH,
        "custom_domain": CUSTOM_DOMAIN
    })

@app.get("/api/status")
async def get_status():
    """API endpoint for dashboard status"""
    return await dashboard.get_dashboard_data()

@app.post("/api/run-automation")
async def trigger_automation(background_tasks: BackgroundTasks):
    """Trigger automation manually"""
    try:
        result = await dashboard.run_automation()
        return {
            "status": "success",
            "message": "Automation completed successfully",
            "result": result
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"❌ Manual automation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

@app.get("/api/history")
async def get_execution_history():
    """Get execution history"""
    return {
        "executions": dashboard.execution_history,
        "total_count": len(dashboard.execution_history)
    }

@app.get("/api/stats")
async def get_statistics():
    """Get automation statistics"""
    return dashboard.stats

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "JobHunter Dashboard",
        "version": "2.0.0",
        "scheduler_running": scheduler.running,
        "automation_running": dashboard.automation_running,
        "timestamp": datetime.now().isoformat()
    }

async def run_scheduled_automation():
    """Scheduled automation task"""
    try:
        logger.info("🕕 Running scheduled automation at 6 AM...")
        await dashboard.run_automation()
        logger.info("✅ Scheduled automation completed")
    except Exception as e:
        logger.error(f"❌ Scheduled automation error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "dashboard_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )