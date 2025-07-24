#!/usr/bin/env python3
"""
Simple job scheduler for Heroku - replaces Celery
Run this with Heroku Scheduler: python app/scheduler/job_runner.py
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.services.job_automation_service import JobAutomationService
from app.services.email_automation_service import EmailAutomationService
from app.services.email_scanner_service import EmailScannerService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_daily_job_automation():
    """Run the daily job automation process"""
    try:
        logger.info("Starting daily job automation...")
        
        # Initialize services
        job_service = JobAutomationService()
        
        # Run the automation
        results = await job_service.run_daily_automation()
        
        logger.info(f"Job automation completed. Results: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Error in daily job automation: {e}")
        raise

async def scan_email_jobs():
    """Scan emails for job opportunities - runs daily at 6am"""
    try:
        logger.info("Starting email job scanning...")
        
        # Initialize email scanner
        email_scanner = EmailScannerService()
        
        # Scan for job emails from yesterday (since this runs daily)
        job_opportunities = await email_scanner.scan_job_emails(days_back=1)
        
        logger.info(f"Found {len(job_opportunities)} job opportunities in emails")
        
        # TODO: Save jobs to database or process them further
        # For now, just log the results
        for job in job_opportunities:
            logger.info(f"Job found: {job['title']} at {job['company']} ({job['source']})")
        
        return {"jobs_found": len(job_opportunities), "jobs": job_opportunities}
        
    except Exception as e:
        logger.error(f"Error scanning email jobs: {e}")
        raise

async def send_daily_summary():
    """Send daily summary email"""
    try:
        logger.info("Sending daily summary...")
        
        email_service = EmailAutomationService()
        
        # First scan for jobs
        scan_results = await scan_email_jobs()
        
        # Get summary data
        summary_data = {
            "jobs_found": scan_results.get("jobs_found", 0),
            "applications_sent": 0,
            "date": "today",
            "job_details": scan_results.get("jobs", [])[:5]  # Include top 5 jobs
        }
        
        # Send to leeharvad@gmail.com
        await email_service.send_daily_summary_email(
            to_email="leeharvad@gmail.com",
            summary_data=summary_data
        )
        
        logger.info("Daily summary sent successfully")
        
    except Exception as e:
        logger.error(f"Error sending daily summary: {e}")
        raise

async def main():
    """Main function to run based on command line argument"""
    if len(sys.argv) < 2:
        print("Usage: python job_runner.py <job_automation|daily_summary|scan_emails>")
        sys.exit(1)
    
    task = sys.argv[1]
    
    if task == "job_automation":
        await run_daily_job_automation()
    elif task == "daily_summary":
        await send_daily_summary()
    elif task == "scan_emails":
        await scan_email_jobs()
    else:
        print(f"Unknown task: {task}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())