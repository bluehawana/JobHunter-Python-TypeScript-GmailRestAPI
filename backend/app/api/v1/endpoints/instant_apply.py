"""
Instant Job Application API Endpoint
Provides one-click job application with LEGO brick strategy
"""
import logging
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
import asyncio

from app.services.smart_cv_service import SmartCVService
from app.services.email_automation_service import EmailAutomationService
from app.core.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

class InstantApplyRequest(BaseModel):
    job_url: HttpUrl
    custom_message: Optional[str] = None
    role_preference: Optional[str] = None  # fullstack, frontend, backend, devops

class InstantApplyResponse(BaseModel):
    success: bool
    job_id: str
    company: str
    title: str
    ats_score: float
    documents_generated: bool
    email_sent: bool
    message: str

@router.post("/instant-apply", response_model=InstantApplyResponse)
async def instant_apply_to_job(
    request: InstantApplyRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Instantly apply to a job using URL with LEGO brick strategy
    """
    try:
        # Extract job information from URL
        job_data = await extract_job_from_url(str(request.job_url))
        
        if not job_data:
            raise HTTPException(status_code=400, detail="Could not extract job information from URL")
        
        # Initialize services
        cv_service = SmartCVService()
        email_service = EmailAutomationService()
        
        await cv_service.initialize()
        
        # Add user preferences
        job_data['role_preference'] = request.role_preference
        job_data['custom_message'] = request.custom_message
        
        # Process application with LEGO strategy
        logger.info(f"Processing instant application for {job_data.get('title')} at {job_data.get('company')}")
        
        # Generate customized documents
        application_result = await cv_service.process_job_application(job_data)
        
        # Send application in background
        background_tasks.add_task(
            send_application_email,
            job_data,
            application_result,
            email_service
        )
        
        return InstantApplyResponse(
            success=True,
            job_id=f"{job_data.get('company', 'unknown')}_{job_data.get('title', 'unknown')}".replace(' ', '_'),
            company=job_data.get('company', ''),
            title=job_data.get('title', ''),
            ats_score=application_result.get('ats_analysis', {}).get('total_score', 0.0),
            documents_generated=bool(application_result.get('optimized_cv')),
            email_sent=False,  # Will be updated by background task
            message=f"Application submitted for {job_data.get('title')} at {job_data.get('company')}"
        )
        
    except Exception as e:
        logger.error(f"Error in instant apply: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def extract_job_from_url(job_url: str) -> Optional[Dict]:
    """Extract job information from various job board URLs"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(job_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # LinkedIn job extraction
        if 'linkedin.com' in job_url:
            return extract_linkedin_job(soup, job_url)
        
        # Indeed job extraction
        elif 'indeed.com' in job_url:
            return extract_indeed_job(soup, job_url)
        
        # Generic job extraction
        else:
            return extract_generic_job(soup, job_url)
            
    except Exception as e:
        logger.error(f"Error extracting job from URL {job_url}: {e}")
        return None

def extract_linkedin_job(soup: BeautifulSoup, job_url: str) -> Dict:
    """Extract LinkedIn job details"""
    try:
        title = soup.find('h1', {'class': 'topcard__title'})
        company = soup.find('a', {'class': 'topcard__org-name-link'})
        description = soup.find('div', {'class': 'show-more-less-html__markup'})
        
        return {
            'title': title.get_text().strip() if title else 'Unknown Position',
            'company': company.get_text().strip() if company else 'Unknown Company',
            'description': description.get_text().strip() if description else '',
            'source': 'linkedin',
            'url': job_url
        }
    except Exception as e:
        logger.error(f"Error parsing LinkedIn job: {e}")
        return {}

def extract_indeed_job(soup: BeautifulSoup, job_url: str) -> Dict:
    """Extract Indeed job details"""
    try:
        title = soup.find('h1', {'class': 'jobsearch-JobInfoHeader-title'})
        company = soup.find('div', {'class': 'jobsearch-InlineCompanyRating'})
        description = soup.find('div', {'id': 'jobDescriptionText'})
        
        return {
            'title': title.get_text().strip() if title else 'Unknown Position',
            'company': company.get_text().strip().split('\n')[0] if company else 'Unknown Company',
            'description': description.get_text().strip() if description else '',
            'source': 'indeed',
            'url': job_url
        }
    except Exception as e:
        logger.error(f"Error parsing Indeed job: {e}")
        return {}

def extract_generic_job(soup: BeautifulSoup, job_url: str) -> Dict:
    """Extract job details from generic job boards"""
    try:
        # Common patterns for job titles
        title_selectors = ['h1', '[class*="title"]', '[class*="job-title"]', '[id*="title"]']
        title = None
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem and title_elem.get_text().strip():
                title = title_elem.get_text().strip()
                break
        
        # Common patterns for company names
        company_selectors = ['[class*="company"]', '[class*="employer"]', '[id*="company"]']
        company = None
        for selector in company_selectors:
            company_elem = soup.select_one(selector)
            if company_elem and company_elem.get_text().strip():
                company = company_elem.get_text().strip()
                break
        
        # Get page text as description fallback
        description = soup.get_text()[:2000]  # First 2000 chars
        
        return {
            'title': title or 'Unknown Position',
            'company': company or 'Unknown Company',
            'description': description,
            'source': 'generic',
            'url': job_url
        }
    except Exception as e:
        logger.error(f"Error parsing generic job: {e}")
        return {}

async def send_application_email(job_data: Dict, application_result: Dict, email_service: EmailAutomationService):
    """Send application email in background"""
    try:
        await email_service.send_application_email(job_data, application_result)
        logger.info(f"Application email sent successfully for {job_data.get('title')}")
    except Exception as e:
        logger.error(f"Error sending application email: {e}")

@router.get("/instant-apply/status/{job_id}")
async def get_application_status(
    job_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get status of an instant application"""
    # This would typically query a database for application status
    return {
        "job_id": job_id,
        "status": "submitted",
        "timestamp": "2025-08-25T10:00:00Z"
    }