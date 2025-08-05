#!/usr/bin/env python3
"""
Heroku-optimized automation for JobHunter
Designed for cloud deployment with webhook triggers
"""
import os
import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse

# Configure logging for Heroku
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your services
from app.services.professional_latex_service import ProfessionalLaTeXService
from app.services.job_application_processor import JobApplicationProcessor

app = FastAPI(title="JobHunter Automation API")

# Initialize services
latex_service = ProfessionalLaTeXService()
job_processor = JobApplicationProcessor()

@app.get("/")
async def root():
    return {"message": "JobHunter Automation API", "status": "running", "timestamp": datetime.now()}

@app.post("/heroku/trigger/daily-scan")
async def heroku_daily_scan(background_tasks: BackgroundTasks):
    """Heroku-triggered daily job scan"""
    logger.info("🚀 Heroku daily scan triggered")
    background_tasks.add_task(run_heroku_job_scan)
    return {"status": "triggered", "message": "Daily scan started"}

@app.post("/heroku/trigger/process-jobs")
async def heroku_process_jobs(background_tasks: BackgroundTasks):
    """Heroku-triggered job processing"""
    logger.info("🎯 Heroku job processing triggered")
    background_tasks.add_task(run_heroku_job_processing)
    return {"status": "triggered", "message": "Job processing started"}

async def run_heroku_job_scan():
    """Background task for Heroku job scanning"""
    try:
        logger.info("📧 Starting Heroku job scan...")
        
        # Import email scanner
        from app.services.real_email_scanner import RealEmailScanner
        email_scanner = RealEmailScanner()
        
        # Scan Gmail
        jobs = await email_scanner.scan_real_gmail_jobs(days_back=1)
        logger.info(f"🔍 Found {len(jobs)} jobs on Heroku")
        
        # Process each job
        for job in jobs:
            try:
                # Generate documents
                cv_pdf = await latex_service.generate_customized_cv(job)
                cl_pdf = await latex_service.generate_customized_cover_letter(job)
                
                if cv_pdf and cl_pdf:
                    # Send application
                    processed_job = {
                        'job': job,
                        'cv_pdf': cv_pdf,
                        'cover_letter_pdf': cl_pdf,
                        'status': 'success'
                    }
                    
                    await job_processor.send_job_application_email(processed_job)
                    logger.info(f"✅ Heroku processed: {job['company']}")
                
                await asyncio.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"❌ Heroku job error: {e}")
        
        logger.info("🎉 Heroku job scan completed")
        
    except Exception as e:
        logger.error(f"❌ Heroku scan error: {e}")

async def run_heroku_job_processing():
    """Background task for general job processing"""
    try:
        logger.info("⚙️ Running Heroku job processing...")
        await run_heroku_job_scan()  # Same as scan for now
    except Exception as e:
        logger.error(f"❌ Heroku processing error: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)