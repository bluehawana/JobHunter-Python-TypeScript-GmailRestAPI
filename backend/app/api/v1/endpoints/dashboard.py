from fastapi import APIRouter, Depends
from typing import List, Dict
from pydantic import BaseModel
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class DashboardStats(BaseModel):
    total_jobs_found: int
    total_applications: int
    applications_pending: int
    applications_rejected: int
    applications_interview: int
    applications_offer: int
    documents_generated: int
    ats_average_score: float

class RecentActivity(BaseModel):
    id: str
    type: str  # job_found, application_sent, document_generated, status_update
    title: str
    description: str
    timestamp: str

class DashboardData(BaseModel):
    stats: DashboardStats
    recent_activities: List[RecentActivity]
    upcoming_tasks: List[str]

@router.get("/", response_model=DashboardData)
async def get_dashboard_data(current_user: dict = Depends(get_current_user)):
    """Get dashboard data for the user"""
    
    # Mock dashboard data
    mock_stats = {
        "total_jobs_found": 45,
        "total_applications": 12,
        "applications_pending": 8,
        "applications_rejected": 2,
        "applications_interview": 2,
        "applications_offer": 0,
        "documents_generated": 24,
        "ats_average_score": 0.82
    }
    
    mock_activities = [
        {
            "id": "activity_1",
            "type": "job_found",
            "title": "New Job Found",
            "description": "Senior Software Engineer at TechCorp",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "id": "activity_2",
            "type": "document_generated",
            "title": "Resume Generated",
            "description": "Customized resume for TechCorp position",
            "timestamp": "2024-01-15T09:15:00Z"
        },
        {
            "id": "activity_3",
            "type": "application_sent",
            "title": "Application Sent",
            "description": "Applied to Full Stack Developer at StartupXYZ",
            "timestamp": "2024-01-14T16:45:00Z"
        }
    ]
    
    mock_tasks = [
        "Follow up on TechCorp application",
        "Prepare for StartupXYZ interview",
        "Update LinkedIn profile",
        "Search for new opportunities"
    ]
    
    return DashboardData(
        stats=DashboardStats(**mock_stats),
        recent_activities=[RecentActivity(**activity) for activity in mock_activities],
        upcoming_tasks=mock_tasks
    )

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Get detailed analytics data"""
    
    # Mock analytics data
    return {
        "application_success_rate": 0.25,
        "average_response_time": "5.2 days",
        "top_keywords": ["python", "react", "aws", "docker"],
        "application_trends": {
            "last_7_days": 3,
            "last_30_days": 12,
            "last_90_days": 28
        },
        "source_effectiveness": {
            "gmail": {"jobs_found": 15, "applications": 5, "success_rate": 0.2},
            "linkedin": {"jobs_found": 20, "applications": 6, "success_rate": 0.3},
            "indeed": {"jobs_found": 10, "applications": 1, "success_rate": 0.1}
        }
    }