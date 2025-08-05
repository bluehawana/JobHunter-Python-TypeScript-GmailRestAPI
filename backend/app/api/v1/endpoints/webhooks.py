#!/usr/bin/env python3
"""
Webhook endpoints for automation services (n8n, Zapier, Twilio)
Fully automated job processing without manual intervention
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from typing import Dict, Any
import logging
from datetime import datetime
import asyncio

from app.services.professional_latex_service import ProfessionalLaTeXService
from app.services.job_application_processor import JobApplicationProcessor
from app.services.real_email_scanner import RealEmailScanner

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
latex_service = ProfessionalLaTeXService()
job_processor = JobApplicationProcessor()
email_scanner = RealEmailScanner()

@router.post("/trigger/daily-job-scan")
async def trigger_daily_job_scan(background_tasks: BackgroundTasks):
    """
    Webhook endpoint for daily automated job scanning
    Can be triggered by n8n, Zapier, or cron jobs
    """
    try:
        logger.info("🚀 Daily job scan triggered via webhook")
        
        # Run job scanning in background
        background_tasks.add_task(process_daily_jobs)
        
        return {
            "status": "success",
            "message": "Daily job scan initiated",
            "timestamp": datetime.now().isoformat(),
            "webhook": "daily-job-scan"
        }
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger/process-job")
async def trigger_job_processing(job_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Webhook endpoint for processing individual jobs
    Perfect for n8n/Zapier integration when new jobs are detected
    """
    try:
        logger.info(f"🎯 Job processing triggered: {job_data.get('title')} at {job_data.get('company')}")
        
        # Validate required fields
        required_fields = ['title', 'company', 'description']
        for field in required_fields:
            if not job_data.get(field):
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Process job in background
        background_tasks.add_task(process_single_job, job_data)
        
        return {
            "status": "success",
            "message": f"Processing job: {job_data['title']} at {job_data['company']}",
            "job_id": job_data.get('id', 'unknown'),
            "timestamp": datetime.now().isoformat(),
            "webhook": "process-job"
        }
        
    except Exception as e:
        logger.error(f"❌ Job processing webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger/gmail-scan")
async def trigger_gmail_scan(background_tasks: BackgroundTasks):
    """
    Webhook endpoint for Gmail scanning
    Can be triggered by Twilio SMS, n8n schedules, or external services
    """
    try:
        logger.info("📧 Gmail scan triggered via webhook")
        
        # Run Gmail scanning in background
        background_tasks.add_task(scan_gmail_for_jobs)
        
        return {
            "status": "success",
            "message": "Gmail scan initiated",
            "timestamp": datetime.now().isoformat(),
            "webhook": "gmail-scan"
        }
        
    except Exception as e:
        logger.error(f"❌ Gmail scan webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger/emergency-job-alert")
async def trigger_emergency_job_alert(alert_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Webhook for urgent job alerts (e.g., Volvo Energy positions)
    Can be triggered by keyword monitoring services
    """
    try:
        logger.info(f"🚨 Emergency job alert: {alert_data.get('keywords', [])}")
        
        # Process urgent job immediately
        background_tasks.add_task(process_urgent_job, alert_data)
        
        return {
            "status": "success",
            "message": "Emergency job alert processed",
            "keywords": alert_data.get('keywords', []),
            "timestamp": datetime.now().isoformat(),
            "webhook": "emergency-job-alert"
        }
        
    except Exception as e:
        logger.error(f"❌ Emergency alert webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/automation")
async def get_automation_status():
    """
    Status endpoint for monitoring automation health
    Perfect for n8n/Zapier health checks
    """
    try:
        return {
            "status": "healthy",
            "services": {
                "latex_service": "active",
                "job_processor": "active", 
                "email_scanner": "active"
            },
            "last_check": datetime.now().isoformat(),
            "automation": "fully_automated"
        }
        
    except Exception as e:
        logger.error(f"❌ Status check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Background task functions
async def process_daily_jobs():
    """Background task for daily job processing"""
    try:
        logger.info("🔄 Starting daily job processing...")
        
        # Scan Gmail for new jobs
        jobs = await email_scanner.scan_real_gmail_jobs(days_back=1)
        logger.info(f"📧 Found {len(jobs)} new jobs")
        
        # Process each job
        for job in jobs:
            try:
                # Generate customized documents
                cv_pdf = await latex_service.generate_customized_cv(job)
                cl_pdf = await latex_service.generate_customized_cover_letter(job)
                
                if cv_pdf and cl_pdf:
                    # Send application email
                    processed_job = {
                        'job': job,
                        'cv_pdf': cv_pdf,
                        'cover_letter_pdf': cl_pdf,
                        'status': 'success'
                    }
                    
                    await job_processor.send_job_application_email(processed_job)
                    logger.info(f"✅ Processed: {job['title']} at {job['company']}")
                else:
                    logger.warning(f"⚠️ Document generation failed for {job['company']}")
                    
                # Small delay between jobs
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Error processing job {job.get('title', 'Unknown')}: {e}")
        
        logger.info("🎉 Daily job processing completed")
        
    except Exception as e:
        logger.error(f"❌ Daily job processing error: {e}")

async def process_single_job(job_data: Dict[str, Any]):
    """Background task for processing a single job"""
    try:
        logger.info(f"🎯 Processing single job: {job_data['title']} at {job_data['company']}")
        
        # Generate customized documents
        cv_pdf = await latex_service.generate_customized_cv(job_data)
        cl_pdf = await latex_service.generate_customized_cover_letter(job_data)
        
        if cv_pdf and cl_pdf:
            # Send application email
            processed_job = {
                'job': job_data,
                'cv_pdf': cv_pdf,
                'cover_letter_pdf': cl_pdf,
                'status': 'success'
            }
            
            await job_processor.send_job_application_email(processed_job)
            logger.info(f"✅ Single job processed successfully: {job_data['company']}")
        else:
            logger.error(f"❌ Document generation failed for {job_data['company']}")
            
    except Exception as e:
        logger.error(f"❌ Single job processing error: {e}")

async def scan_gmail_for_jobs():
    """Background task for Gmail scanning"""
    try:
        logger.info("📧 Starting Gmail scan...")
        
        # Scan Gmail for jobs
        jobs = await email_scanner.scan_real_gmail_jobs(days_back=3)
        logger.info(f"📧 Gmail scan found {len(jobs)} jobs")
        
        # Process each job found
        for job in jobs:
            await process_single_job(job)
            await asyncio.sleep(1)  # Rate limiting
            
        logger.info("📧 Gmail scan completed")
        
    except Exception as e:
        logger.error(f"❌ Gmail scan error: {e}")

async def process_urgent_job(alert_data: Dict[str, Any]):
    """Background task for urgent job processing"""
    try:
        keywords = alert_data.get('keywords', [])
        logger.info(f"🚨 Processing urgent job alert for keywords: {keywords}")
        
        # Scan for jobs matching urgent keywords
        jobs = await email_scanner.scan_real_gmail_jobs(days_back=1)
        
        # Filter for urgent jobs
        urgent_jobs = []
        for job in jobs:
            job_content = f"{job.get('title', '')} {job.get('description', '')}".lower()
            if any(keyword.lower() in job_content for keyword in keywords):
                urgent_jobs.append(job)
        
        logger.info(f"🚨 Found {len(urgent_jobs)} urgent jobs")
        
        # Process urgent jobs immediately
        for job in urgent_jobs:
            await process_single_job(job)
            
        logger.info("🚨 Urgent job processing completed")
        
    except Exception as e:
        logger.error(f"❌ Urgent job processing error: {e}")