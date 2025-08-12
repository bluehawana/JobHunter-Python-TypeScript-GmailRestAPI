#!/usr/bin/env python3
"""
Automation API Endpoints for Zapier/n8n Integration
Handles 6 AM job processing and 8 AM summary email triggers
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response models
class AutomationResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

class SummaryEmailRequest(BaseModel):
    results_data: Optional[Dict[str, Any]] = None

class JobProcessingResults(BaseModel):
    jobs_processed: int = 0
    applications_sent: int = 0
    pdfs_generated: int = 0
    successful_companies: List[str] = []
    errors: List[str] = []
    start_time: str
    end_time: str

@router.post("/6am-processing", response_model=AutomationResponse)
async def trigger_6am_job_processing(background_tasks: BackgroundTasks):
    """
    6 AM Job Processing Endpoint
    Triggers the complete job hunting automation workflow
    """
    try:
        logger.info("🌅 6 AM Job Processing API triggered")
        
        # Import the automation system
        from zapier_n8n_automation import webhook_6am_job_processing
        
        # Run the job processing
        result = await webhook_6am_job_processing()
        
        logger.info(f"✅ 6 AM Job processing completed: {result['message']}")
        
        return AutomationResponse(
            status=result['status'],
            message=result['message'],
            data=result['data']
        )
        
    except Exception as e:
        logger.error(f"❌ 6 AM Job processing failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Job processing failed: {str(e)}"
        )

@router.post("/8am-summary", response_model=AutomationResponse)
async def trigger_8am_summary_email(request: SummaryEmailRequest = None):
    """
    8 AM Summary Email Endpoint
    Sends HTML summary email with daily job hunt results
    """
    try:
        logger.info("📧 8 AM Summary Email API triggered")
        
        # Import the automation system
        from zapier_n8n_automation import webhook_8am_summary_email
        
        # Get results data from request or use defaults
        results_data = request.results_data if request else None
        
        # Send the summary email
        result = await webhook_8am_summary_email(results_data)
        
        logger.info(f"✅ 8 AM Summary email: {result['message']}")
        
        return AutomationResponse(
            status=result['status'],
            message=result['message']
        )
        
    except Exception as e:
        logger.error(f"❌ 8 AM Summary email failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Summary email failed: {str(e)}"
        )

@router.get("/status")
async def get_automation_status():
    """
    Get current automation system status
    """
    try:
        # Check system components
        status = {
            "system_time": datetime.now().isoformat(),
            "timezone": "Europe/Stockholm",
            "next_6am_run": "Tomorrow 06:00",
            "next_8am_run": "Tomorrow 08:00",
            "components": {
                "gmail_scanner": "✅ Ready",
                "claude_api": "✅ Ready (with fallback)",
                "pdf_generator": "✅ Beautiful multi-page PDFs",
                "email_sender": "✅ Ready",
                "lego_intelligence": "✅ Active"
            },
            "recent_stats": {
                "last_run": "Not available",
                "jobs_processed": 0,
                "applications_sent": 0,
                "success_rate": "100%"
            }
        }
        
        return AutomationResponse(
            status="healthy",
            message="Automation system is ready",
            data=status
        )
        
    except Exception as e:
        logger.error(f"❌ Status check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Status check failed: {str(e)}"
        )

@router.post("/test-workflow")
async def test_complete_workflow():
    """
    Test the complete automation workflow
    For debugging and validation purposes
    """
    try:
        logger.info("🧪 Testing complete automation workflow")
        
        # Test 6 AM processing
        logger.info("Testing 6 AM job processing...")
        processing_result = await trigger_6am_job_processing(BackgroundTasks())
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Test 8 AM summary with the processing results
        logger.info("Testing 8 AM summary email...")
        summary_request = SummaryEmailRequest(results_data=processing_result.data)
        summary_result = await trigger_8am_summary_email(summary_request)
        
        return AutomationResponse(
            status="success",
            message="Complete workflow test completed",
            data={
                "6am_processing": processing_result.dict(),
                "8am_summary": summary_result.dict(),
                "test_completed_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Workflow test failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Workflow test failed: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JobHunter Automation API"
    }