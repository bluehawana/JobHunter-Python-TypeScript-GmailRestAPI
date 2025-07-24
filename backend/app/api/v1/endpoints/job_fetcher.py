from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from pydantic import BaseModel, HttpUrl
import logging

from app.services.job_link_fetcher import job_link_fetcher
from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)

router = APIRouter()

class JobUrlsRequest(BaseModel):
    urls: List[str]

class JobFetchResponse(BaseModel):
    success: bool
    message: str
    fetched_jobs: List[Dict[str, Any]]
    failed_urls: List[str]

@router.post("/fetch-jobs", response_model=JobFetchResponse)
async def fetch_jobs_from_urls(request: JobUrlsRequest):
    """
    Fetch job information from provided URLs and save to database
    """
    try:
        logger.info(f"Fetching jobs from {len(request.urls)} URLs")
        
        # Validate URLs
        valid_urls = []
        invalid_urls = []
        
        for url in request.urls:
            try:
                # Basic URL validation
                if url.startswith(('http://', 'https://')):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            except Exception:
                invalid_urls.append(url)
        
        if not valid_urls:
            raise HTTPException(status_code=400, detail="No valid URLs provided")
        
        # Fetch jobs from valid URLs
        fetched_jobs = await job_link_fetcher.fetch_and_save_jobs(valid_urls)
        
        # Determine which URLs failed
        successful_urls = [job.get('application_link') for job in fetched_jobs if job.get('application_link')]
        failed_urls = [url for url in valid_urls if url not in successful_urls] + invalid_urls
        
        return JobFetchResponse(
            success=True,
            message=f"Successfully fetched {len(fetched_jobs)} jobs. {len(failed_urls)} URLs failed.",
            fetched_jobs=fetched_jobs,
            failed_urls=failed_urls
        )
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/applications", response_model=List[Dict[str, Any]])
async def get_all_applications(limit: int = 50, offset: int = 0):
    """
    Get all job applications from database
    """
    try:
        applications = await supabase_service.get_job_applications(limit=limit, offset=offset)
        return applications
    except Exception as e:
        logger.error(f"Error fetching applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/applications/{application_id}")
async def get_application(application_id: str):
    """
    Get a specific job application by ID
    """
    try:
        application = await supabase_service.get_job_application(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return application
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/applications/{application_id}/status")
async def update_application_status(application_id: str, status: str, notes: str = None):
    """
    Update application status
    """
    try:
        success = await supabase_service.update_application_status(application_id, status, notes)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found or update failed")
        return {"message": "Status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating application status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/applications/status/{status}")
async def get_applications_by_status(status: str):
    """
    Get applications by status
    """
    try:
        applications = await supabase_service.get_applications_by_status(status)
        return applications
    except Exception as e:
        logger.error(f"Error fetching applications by status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_application_statistics():
    """
    Get application statistics
    """
    try:
        stats = await supabase_service.get_application_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/applications/{application_id}/interview")
async def add_interview_round(application_id: str, interview_data: Dict[str, Any]):
    """
    Add an interview round to an application
    """
    try:
        success = await supabase_service.add_interview_round(application_id, interview_data)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found or update failed")
        return {"message": "Interview round added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding interview round: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/applications/{application_id}/communication")
async def add_communication_log(application_id: str, communication_data: Dict[str, Any]):
    """
    Add a communication log entry to an application
    """
    try:
        success = await supabase_service.add_communication_log(application_id, communication_data)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found or update failed")
        return {"message": "Communication log added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding communication log: {e}")
        raise HTTPException(status_code=500, detail=str(e))