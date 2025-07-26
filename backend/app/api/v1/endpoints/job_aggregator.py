from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.api.v1.endpoints.auth import get_current_user
from app.services.multi_source_job_aggregator import MultiSourceJobAggregator
from app.models.job import AggregatedJob
from app.models.user import User

router = APIRouter()

class JobAggregationRequest(BaseModel):
    sources: Optional[List[str]] = None  # Specific sources to sync
    sync_preferences: Optional[Dict[str, Any]] = None

class JobProcessingRequest(BaseModel):
    job_ids: List[str]
    action: str  # 'generate_documents', 'apply', 'save', 'reject'
    priority: Optional[str] = 'medium'
    notes: Optional[str] = None

class JobFilterRequest(BaseModel):
    source: Optional[str] = None
    application_status: Optional[str] = None
    priority: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    keywords: Optional[List[str]] = None

@router.post("/aggregate")
async def aggregate_jobs(
    request: JobAggregationRequest = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger job aggregation from all or specified sources
    """
    try:
        aggregator = MultiSourceJobAggregator()
        
        # If specific sources requested, enable only those
        if request.sources:
            for source_name in aggregator.sources:
                aggregator.sources[source_name].enabled = source_name in request.sources
        
        results = await aggregator.aggregate_all_jobs(
            user_id=str(current_user.id),
            sync_preferences=request.sync_preferences
        )
        
        return {
            "status": "success",
            "message": f"Job aggregation completed. Found {results['total_jobs_found']} jobs, {results['new_jobs']} new.",
            "data": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job aggregation failed: {str(e)}")

@router.get("/jobs")
async def get_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    source: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    Get paginated list of aggregated jobs with filtering
    """
    try:
        # Implement database query with filters
        # This is a placeholder - you'd implement proper database queries
        
        jobs = [
            {
                "id": "example_id",
                "title": "Senior Python Developer",
                "company": "Tech Company",
                "location": "Stockholm, Sweden",
                "source": "linkedin_saved",
                "application_status": "saved",
                "priority": "high",
                "discovered_at": datetime.utcnow(),
                "source_url": "https://linkedin.com/jobs/view/123456"
            }
        ]
        
        return {
            "status": "success",
            "data": {
                "jobs": jobs,
                "page": page,
                "limit": limit,
                "total": len(jobs),
                "has_next": False
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve jobs: {str(e)}")

@router.post("/jobs/filter")
async def filter_jobs(
    filters: JobFilterRequest = Body(...),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Advanced job filtering with multiple criteria
    """
    try:
        # Implement advanced filtering logic
        # Apply filters: source, status, priority, company, location, dates, keywords
        
        filtered_jobs = []  # Placeholder
        
        return {
            "status": "success",
            "data": {
                "jobs": filtered_jobs,
                "filters_applied": filters.dict(exclude_none=True),
                "page": page,
                "limit": limit,
                "total": len(filtered_jobs)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job filtering failed: {str(e)}")

@router.post("/jobs/process")
async def process_jobs(
    request: JobProcessingRequest = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Process selected jobs (generate documents, apply, save, etc.)
    """
    try:
        aggregator = MultiSourceJobAggregator()
        
        if request.action == "generate_documents":
            results = await aggregator.process_selected_jobs(
                user_id=str(current_user.id),
                job_ids=request.job_ids
            )
            
            return {
                "status": "success",
                "message": f"Processed {results['processed_jobs']} jobs, {results['successful_applications']} successful",
                "data": results
            }
            
        elif request.action == "save":
            # Update job status to saved with priority
            await _update_jobs_status(request.job_ids, "saved", request.priority, request.notes)
            
            return {
                "status": "success",
                "message": f"Saved {len(request.job_ids)} jobs"
            }
            
        elif request.action == "reject":
            # Update job status to rejected
            await _update_jobs_status(request.job_ids, "rejected", notes=request.notes)
            
            return {
                "status": "success", 
                "message": f"Rejected {len(request.job_ids)} jobs"
            }
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job processing failed: {str(e)}")

@router.get("/jobs/{job_id}")
async def get_job_details(
    job_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about a specific job
    """
    try:
        # Fetch job from database
        # This is a placeholder
        job = {
            "id": job_id,
            "title": "Senior Python Developer",
            "company": "Tech Company",
            "location": "Stockholm, Sweden",
            "description": "Full job description here...",
            "requirements": ["Python", "FastAPI", "PostgreSQL"],
            "source": "linkedin_saved",
            "source_url": "https://linkedin.com/jobs/view/123456",
            "application_status": "saved",
            "priority": "high",
            "keywords": ["python", "backend", "api"],
            "match_score": 0.85,
            "discovered_at": datetime.utcnow()
        }
        
        return {
            "status": "success",
            "data": job
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")

@router.put("/jobs/{job_id}")
async def update_job(
    job_id: str,
    updates: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Update job information (status, priority, notes, etc.)
    """
    try:
        # Update job in database
        # This is a placeholder
        
        allowed_updates = [
            'application_status', 'priority', 'user_notes', 
            'applied_at', 'response_received', 'interview_scheduled'
        ]
        
        valid_updates = {k: v for k, v in updates.items() if k in allowed_updates}
        
        return {
            "status": "success",
            "message": f"Updated job {job_id}",
            "data": {"updated_fields": list(valid_updates.keys())}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job update failed: {str(e)}")

@router.get("/sources/status")
async def get_sources_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get status of all job sources (last sync, error counts, etc.)
    """
    try:
        aggregator = MultiSourceJobAggregator()
        
        sources_status = {}
        for name, source in aggregator.sources.items():
            sources_status[name] = {
                "name": source.name,
                "enabled": source.enabled,
                "last_sync": source.last_sync,
                "error_count": source.error_count,
                "total_jobs_found": source.total_jobs_found
            }
        
        return {
            "status": "success",
            "data": sources_status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sources status: {str(e)}")

@router.post("/sources/configure")
async def configure_sources(
    config: Dict[str, bool] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Enable/disable specific job sources
    """
    try:
        aggregator = MultiSourceJobAggregator()
        
        updated_sources = []
        for source_name, enabled in config.items():
            if source_name in aggregator.sources:
                aggregator.sources[source_name].enabled = enabled
                updated_sources.append(source_name)
        
        return {
            "status": "success",
            "message": f"Updated configuration for {len(updated_sources)} sources",
            "data": {"updated_sources": updated_sources}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Source configuration failed: {str(e)}")

@router.get("/analytics")
async def get_job_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Get job aggregation analytics and statistics
    """
    try:
        # Calculate analytics from database
        analytics = {
            "period_days": days,
            "total_jobs_discovered": 150,
            "jobs_by_source": {
                "gmail_linkedin": 45,
                "gmail_indeed": 30,
                "linkedin_saved": 25,
                "arbetsformedlingen": 35,
                "linkedin_search": 10
            },
            "jobs_by_status": {
                "discovered": 80,
                "saved": 40,
                "generated": 20,
                "applied": 8,
                "rejected": 2
            },
            "top_companies": [
                {"name": "Company A", "count": 12},
                {"name": "Company B", "count": 8},
                {"name": "Company C", "count": 6}
            ],
            "top_locations": [
                {"name": "Stockholm", "count": 60},
                {"name": "Gothenburg", "count": 45},
                {"name": "Malmö", "count": 25}
            ],
            "application_success_rate": 0.75,
            "average_match_score": 0.68
        }
        
        return {
            "status": "success",
            "data": analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

async def _update_jobs_status(job_ids: List[str], status: str, priority: str = None, notes: str = None):
    """Helper function to update job status in database"""
    # Implement database update logic
    pass