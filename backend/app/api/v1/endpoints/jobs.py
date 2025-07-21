from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from app.api.v1.endpoints.auth import get_current_user
from app.services.gmail_service import GmailService

router = APIRouter()

class JobSearchRequest(BaseModel):
    keywords: List[str]
    sources: List[str] = ["gmail", "linkedin", "indeed"]
    location: Optional[str] = None
    job_type: Optional[str] = None
    days_back: int = 7

class JobPosting(BaseModel):
    id: str
    source: str
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    description: str
    url: Optional[str]
    posting_date: Optional[str]
    salary_range: Optional[str]
    job_type: Optional[str]
    keywords: List[str]
    match_score: float
    confidence_score: float = 0.0

class JobSearchResponse(BaseModel):
    jobs: List[JobPosting]
    total_count: int
    sources_searched: List[str]
    search_timestamp: str

@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(
    search_request: JobSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for job postings from multiple sources
    """
    try:
        jobs = []
        sources_searched = []
        
        # Search Gmail if requested
        if "gmail" in search_request.sources:
            try:
                # In a real implementation, you would:
                # 1. Get user's Gmail credentials from database
                # 2. Initialize GmailService with those credentials
                # 3. Search for job emails
                
                # Mock Gmail job search results
                gmail_jobs = [
                    {
                        "id": "gmail_job_1",
                        "source": "gmail",
                        "title": "Senior Software Engineer",
                        "company": "TechCorp",
                        "location": "San Francisco, CA",
                        "description": "We are looking for a senior software engineer...",
                        "url": "https://techcorp.com/jobs/senior-engineer",
                        "posting_date": "2024-01-15",
                        "salary_range": "$120k - $160k",
                        "job_type": "Full-time",
                        "keywords": search_request.keywords,
                        "match_score": 0.85,
                        "confidence_score": 0.9
                    }
                ]
                jobs.extend(gmail_jobs)
                sources_searched.append("gmail")
                
            except Exception as e:
                print(f"Gmail search error: {e}")
        
        # Search LinkedIn if requested
        if "linkedin" in search_request.sources:
            try:
                # Mock LinkedIn job search results
                linkedin_jobs = [
                    {
                        "id": "linkedin_job_1",
                        "source": "linkedin",
                        "title": "Full Stack Developer",
                        "company": "StartupXYZ",
                        "location": "Remote",
                        "description": "Join our growing team as a full stack developer...",
                        "url": "https://linkedin.com/jobs/view/123456",
                        "posting_date": "2024-01-14",
                        "salary_range": "$90k - $130k",
                        "job_type": "Full-time",
                        "keywords": search_request.keywords,
                        "match_score": 0.78,
                        "confidence_score": 1.0
                    }
                ]
                jobs.extend(linkedin_jobs)
                sources_searched.append("linkedin")
                
            except Exception as e:
                print(f"LinkedIn search error: {e}")
        
        # Search Indeed if requested
        if "indeed" in search_request.sources:
            try:
                # Mock Indeed job search results
                indeed_jobs = [
                    {
                        "id": "indeed_job_1",
                        "source": "indeed",
                        "title": "Python Developer",
                        "company": "DataCorp",
                        "location": "New York, NY",
                        "description": "We need a Python developer for our data team...",
                        "url": "https://indeed.com/viewjob?jk=abc123",
                        "posting_date": "2024-01-13",
                        "salary_range": "$100k - $140k",
                        "job_type": "Full-time",
                        "keywords": search_request.keywords,
                        "match_score": 0.82,
                        "confidence_score": 0.95
                    }
                ]
                jobs.extend(indeed_jobs)
                sources_searched.append("indeed")
                
            except Exception as e:
                print(f"Indeed search error: {e}")
        
        from datetime import datetime
        
        return JobSearchResponse(
            jobs=[JobPosting(**job) for job in jobs],
            total_count=len(jobs),
            sources_searched=sources_searched,
            search_timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@router.get("/", response_model=List[JobPosting])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    source: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Get saved job postings with pagination
    """
    # In a real implementation, you would query the database
    # For now, return mock data
    
    mock_jobs = [
        {
            "id": "job_1",
            "source": "gmail",
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "description": "We are looking for a senior software engineer...",
            "url": "https://techcorp.com/jobs/senior-engineer",
            "posting_date": "2024-01-15",
            "salary_range": "$120k - $160k",
            "job_type": "Full-time",
            "keywords": ["python", "react", "aws"],
            "match_score": 0.85,
            "confidence_score": 0.9
        },
        {
            "id": "job_2",
            "source": "linkedin",
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "description": "Join our growing team as a full stack developer...",
            "url": "https://linkedin.com/jobs/view/123456",
            "posting_date": "2024-01-14",
            "salary_range": "$90k - $130k",
            "job_type": "Full-time",
            "keywords": ["javascript", "node", "react"],
            "match_score": 0.78,
            "confidence_score": 1.0
        }
    ]
    
    # Apply filtering and pagination
    filtered_jobs = mock_jobs
    if source:
        filtered_jobs = [job for job in filtered_jobs if job["source"] == source]
    
    paginated_jobs = filtered_jobs[skip:skip + limit]
    
    return [JobPosting(**job) for job in paginated_jobs]

@router.get("/{job_id}", response_model=JobPosting)
async def get_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific job posting by ID
    """
    # In a real implementation, you would query the database
    # For now, return mock data
    
    mock_job = {
        "id": job_id,
        "source": "gmail",
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "location": "San Francisco, CA",
        "description": "We are looking for a senior software engineer with 5+ years of experience...",
        "url": "https://techcorp.com/jobs/senior-engineer",
        "posting_date": "2024-01-15",
        "salary_range": "$120k - $160k",
        "job_type": "Full-time",
        "keywords": ["python", "react", "aws"],
        "match_score": 0.85,
        "confidence_score": 0.9
    }
    
    return JobPosting(**mock_job)

@router.post("/{job_id}/save")
async def save_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Save a job posting for later reference
    """
    # In a real implementation, you would save to database
    return {"message": f"Job {job_id} saved successfully"}

@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a saved job posting
    """
    # In a real implementation, you would delete from database
    return {"message": f"Job {job_id} deleted successfully"}