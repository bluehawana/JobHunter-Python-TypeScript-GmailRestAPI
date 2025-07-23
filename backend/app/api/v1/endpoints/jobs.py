 from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.api.v1.endpoints.auth import get_current_user
from app.services.job_aggregation_service import JobAggregationService, JobSearchRequest as ServiceJobSearchRequest
from bson import ObjectId

router = APIRouter()

class JobSearchRequest(BaseModel):
    query: str = Field(..., description="Job search query (e.g., 'python developer')")
    location: str = Field("", description="Location filter (e.g., 'San Francisco, CA')")
    max_results: int = Field(50, ge=1, le=100, description="Maximum number of results")
    include_remote: bool = Field(True, description="Include remote job opportunities")
    job_types: Optional[List[str]] = Field(None, description="Job types filter")
    salary_min: Optional[int] = Field(None, description="Minimum salary requirement")
    salary_max: Optional[int] = Field(None, description="Maximum salary preference")
    date_posted: str = Field("all", description="Date filter: today, week, month, all")
    experience_levels: Optional[List[str]] = Field(None, description="Experience levels")
    companies_exclude: Optional[List[str]] = Field(None, description="Companies to exclude")
    keywords_required: Optional[List[str]] = Field(None, description="Required keywords")
    keywords_exclude: Optional[List[str]] = Field(None, description="Keywords to exclude")

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posting_date: Optional[datetime]
    salary: Optional[dict]
    job_type: Optional[str]
    requirements: List[str] = []
    benefits: List[str] = []
    experience_level: Optional[str]
    remote_option: bool = False
    keywords: List[str] = []
    match_score: float
    confidence_score: float
    ats_score: float
    category: str
    application_difficulty: str

class JobSearchResponse(BaseModel):
    jobs: List[JobPosting]
    total_count: int
    search_params: dict
    search_timestamp: datetime
    sources_used: List[str]

@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(
    search_request: JobSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for job postings from multiple sources using advanced aggregation
    """
    try:
        # Initialize job aggregation service
        job_service = JobAggregationService()
        
        # Convert API request to service request
        service_request = ServiceJobSearchRequest(
            query=search_request.query,
            location=search_request.location,
            max_results=search_request.max_results,
            include_remote=search_request.include_remote,
            job_types=search_request.job_types,
            salary_min=search_request.salary_min,
            salary_max=search_request.salary_max,
            date_posted=search_request.date_posted,
            experience_levels=search_request.experience_levels,
            companies_exclude=search_request.companies_exclude,
            keywords_required=search_request.keywords_required,
            keywords_exclude=search_request.keywords_exclude
        )
        
        # Execute search
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        jobs = await job_service.search_jobs(service_request, user_id)
        
        # Convert to response format
        job_postings = []
        for job in jobs:
            job_posting = JobPosting(
                title=job.get("title", ""),
                company=job.get("company", ""),
                location=job.get("location", ""),
                description=job.get("description", ""),
                url=job.get("url", ""),
                source=job.get("source", ""),
                posting_date=job.get("posting_date"),
                salary=job.get("salary"),
                job_type=job.get("job_type"),
                requirements=job.get("requirements", []),
                benefits=job.get("benefits", []),
                experience_level=job.get("experience_level"),
                remote_option=job.get("remote_option", False),
                keywords=job.get("keywords", []),
                match_score=job.get("match_score", 0.0),
                confidence_score=job.get("confidence_score", 0.0),
                ats_score=job.get("ats_score", 0.0),
                category=job.get("category", "general"),
                application_difficulty=job.get("application_difficulty", "medium")
            )
            job_postings.append(job_posting)
        
        return JobSearchResponse(
            jobs=job_postings,
            total_count=len(job_postings),
            search_params=search_request.dict(),
            search_timestamp=datetime.utcnow(),
            sources_used=["google_jobs", "indeed", "arbetsformedlingen", "gmail"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@router.get("/saved", response_model=List[JobPosting])
async def get_saved_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's saved job postings
    """
    try:
        job_service = JobAggregationService()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        saved_jobs = await job_service.get_saved_jobs(user_id, limit)
        
        job_postings = []
        for job in saved_jobs[skip:skip + limit]:
            job_posting = JobPosting(
                title=job.get("title", ""),
                company=job.get("company", ""),
                location=job.get("location", ""),
                description=job.get("description", ""),
                url=job.get("url", ""),
                source=job.get("source", ""),
                posting_date=job.get("posting_date"),
                salary=job.get("salary"),
                job_type=job.get("job_type"),
                requirements=job.get("requirements", []),
                benefits=job.get("benefits", []),
                experience_level=job.get("experience_level"),
                remote_option=job.get("remote_option", False),
                keywords=job.get("keywords", []),
                match_score=job.get("match_score", 0.0),
                confidence_score=job.get("confidence_score", 0.0),
                ats_score=job.get("ats_score", 0.0),
                category=job.get("category", "general"),
                application_difficulty=job.get("application_difficulty", "medium")
            )
            job_postings.append(job_posting)
        
        return job_postings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get saved jobs: {str(e)}")

@router.get("/history")
async def get_search_history(
    limit: int = Query(20, ge=1, le=50),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's job search history
    """
    try:
        job_service = JobAggregationService()
        user_id = current_user.get("user_id") or str(current_user.get("_id"))
        
        history = await job_service.get_search_history(user_id, limit)
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get search history: {str(e)}")

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

@router.get("/test/integration")
async def test_job_integration(
    current_user: dict = Depends(get_current_user)
):
    """
    Test all job source integrations including LinkedIn, Arbetsförmedlingen, and Gmail
    """
    try:
        from app.services.linkedin_service import LinkedInService
        from app.services.arbetsformedlingen_service import ArbetsformedlingenService
        from app.services.gmail_service import GmailService
        from app.core.database import get_database
        from google.oauth2.credentials import Credentials
        
        test_results = {
            "linkedin": {"status": "unknown", "message": "", "sample_jobs": 0},
            "arbetsformedlingen": {"status": "unknown", "message": "", "sample_jobs": 0},
            "gmail": {"status": "unknown", "message": "", "sample_jobs": 0},
            "aggregation": {"status": "unknown", "message": "", "total_jobs": 0}
        }
        
        # Test LinkedIn integration
        try:
            linkedin_service = LinkedInService()
            linkedin_jobs = await linkedin_service.search_jobs(
                query="python developer",
                location="Stockholm",
                num_results=5
            )
            test_results["linkedin"] = {
                "status": "success",
                "message": f"Found {len(linkedin_jobs)} jobs",
                "sample_jobs": len(linkedin_jobs)
            }
        except Exception as e:
            test_results["linkedin"] = {
                "status": "error",
                "message": f"LinkedIn API error: {str(e)}",
                "sample_jobs": 0
            }
        
        # Test Arbetsförmedlingen integration
        try:
            arbetsformedlingen_service = ArbetsformedlingenService()
            af_jobs = await arbetsformedlingen_service.search_jobs(
                query="utvecklare",
                location="Stockholm",
                num_results=5
            )
            test_results["arbetsformedlingen"] = {
                "status": "success",
                "message": f"Found {len(af_jobs)} jobs",
                "sample_jobs": len(af_jobs)
            }
        except Exception as e:
            test_results["arbetsformedlingen"] = {
                "status": "error",
                "message": f"Arbetsförmedlingen API error: {str(e)}",
                "sample_jobs": 0
            }
        
        # Test Gmail integration
        try:
            db = await get_database()
            user_id = current_user.get("user_id") or str(current_user.get("_id"))
            user = await db.users.find_one({"_id": user_id})
            
            if user and user.get("gmail_credentials"):
                gmail_creds = user["gmail_credentials"]
                credentials = Credentials(
                    token=gmail_creds.get("token"),
                    refresh_token=gmail_creds.get("refresh_token"),
                    token_uri=gmail_creds.get("token_uri"),
                    client_id=gmail_creds.get("client_id"),
                    client_secret=gmail_creds.get("client_secret"),
                    scopes=gmail_creds.get("scopes", ["https://www.googleapis.com/auth/gmail.readonly"])
                )
                
                gmail_service = GmailService(credentials)
                gmail_jobs = await gmail_service.search_job_emails(
                    keywords=["developer", "engineer"],
                    days_back=7
                )
                test_results["gmail"] = {
                    "status": "success",
                    "message": f"Found {len(gmail_jobs)} job emails",
                    "sample_jobs": len(gmail_jobs)
                }
            else:
                test_results["gmail"] = {
                    "status": "not_connected",
                    "message": "Gmail not connected for this user",
                    "sample_jobs": 0
                }
        except Exception as e:
            test_results["gmail"] = {
                "status": "error",
                "message": f"Gmail integration error: {str(e)}",
                "sample_jobs": 0
            }
        
        # Test job aggregation service
        try:
            job_service = JobAggregationService()
            service_request = ServiceJobSearchRequest(
                query="python developer",
                location="Stockholm",
                max_results=10
            )
            
            aggregated_jobs = await job_service.search_jobs(service_request, user_id)
            test_results["aggregation"] = {
                "status": "success",
                "message": f"Aggregated {len(aggregated_jobs)} jobs from all sources",
                "total_jobs": len(aggregated_jobs)
            }
        except Exception as e:
            test_results["aggregation"] = {
                "status": "error",
                "message": f"Job aggregation error: {str(e)}",
                "total_jobs": 0
            }
        
        # Calculate overall status
        successful_integrations = sum(1 for result in test_results.values() if result["status"] == "success")
        total_integrations = len(test_results)
        
        return {
            "overall_status": "success" if successful_integrations >= 2 else "partial",
            "successful_integrations": successful_integrations,
            "total_integrations": total_integrations,
            "test_results": test_results,
            "recommendations": [
                "LinkedIn integration: Ensure valid access token" if test_results["linkedin"]["status"] != "success" else None,
                "Arbetsförmedlingen integration: Check API endpoint availability" if test_results["arbetsformedlingen"]["status"] != "success" else None,
                "Gmail integration: Connect Gmail account via /api/v1/gmail/connect" if test_results["gmail"]["status"] == "not_connected" else None
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Integration test failed: {str(e)}")