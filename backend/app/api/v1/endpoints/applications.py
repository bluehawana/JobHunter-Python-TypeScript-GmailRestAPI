from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class ApplicationCreate(BaseModel):
    job_id: str
    company_name: str
    position_title: str
    application_method: str  # email, website, etc.
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class Application(BaseModel):
    id: str
    job_id: str
    user_id: str
    company_name: str
    position_title: str
    status: str
    application_date: datetime
    last_updated: datetime
    application_method: str
    notes: Optional[str] = None
    resume_id: Optional[str] = None
    cover_letter_id: Optional[str] = None

@router.post("/", response_model=Application)
async def create_application(
    application_data: ApplicationCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new job application"""
    # Mock application creation
    mock_application = {
        "id": "app_123",
        "job_id": application_data.job_id,
        "user_id": current_user["id"],
        "company_name": application_data.company_name,
        "position_title": application_data.position_title,
        "status": "applied",
        "application_date": datetime.now(),
        "last_updated": datetime.now(),
        "application_method": application_data.application_method,
        "notes": application_data.notes
    }
    
    return Application(**mock_application)

@router.get("/", response_model=List[Application])
async def get_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get user's job applications"""
    # Mock applications data
    mock_applications = [
        {
            "id": "app_1",
            "job_id": "job_1",
            "user_id": current_user["id"],
            "company_name": "TechCorp",
            "position_title": "Senior Software Engineer",
            "status": "applied",
            "application_date": datetime.now(),
            "last_updated": datetime.now(),
            "application_method": "email",
            "notes": "Applied via email with customized resume"
        },
        {
            "id": "app_2",
            "job_id": "job_2",
            "user_id": current_user["id"],
            "company_name": "StartupXYZ",
            "position_title": "Full Stack Developer",
            "status": "interview",
            "application_date": datetime.now(),
            "last_updated": datetime.now(),
            "application_method": "website",
            "notes": "Phone interview scheduled for next week"
        }
    ]
    
    # Apply filtering
    if status:
        mock_applications = [app for app in mock_applications if app["status"] == status]
    
    # Apply pagination
    paginated_apps = mock_applications[skip:skip + limit]
    
    return [Application(**app) for app in paginated_apps]

@router.get("/{application_id}", response_model=Application)
async def get_application(
    application_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific application"""
    mock_application = {
        "id": application_id,
        "job_id": "job_1",
        "user_id": current_user["id"],
        "company_name": "TechCorp",
        "position_title": "Senior Software Engineer",
        "status": "applied",
        "application_date": datetime.now(),
        "last_updated": datetime.now(),
        "application_method": "email",
        "notes": "Applied via email with customized resume"
    }
    
    return Application(**mock_application)

@router.put("/{application_id}", response_model=Application)
async def update_application(
    application_id: str,
    update_data: ApplicationUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update an application"""
    # Mock update
    mock_application = {
        "id": application_id,
        "job_id": "job_1",
        "user_id": current_user["id"],
        "company_name": "TechCorp",
        "position_title": "Senior Software Engineer",
        "status": update_data.status or "applied",
        "application_date": datetime.now(),
        "last_updated": datetime.now(),
        "application_method": "email",
        "notes": update_data.notes or "Updated application"
    }
    
    return Application(**mock_application)

@router.delete("/{application_id}")
async def delete_application(
    application_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete an application"""
    return {"message": f"Application {application_id} deleted successfully"}