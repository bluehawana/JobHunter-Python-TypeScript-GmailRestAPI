from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.models.user import PyObjectId

class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    APPLIED = "applied"
    ACKNOWLEDGED = "acknowledged"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    REJECTED = "rejected"
    OFFER_RECEIVED = "offer_received"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    WITHDRAWN = "withdrawn"

class ApplicationMethod(str, Enum):
    EMAIL = "email"
    WEBSITE = "website"
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    REFERRAL = "referral"
    OTHER = "other"

class InterviewType(str, Enum):
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    PANEL = "panel"

class Interview(BaseModel):
    type: InterviewType
    scheduled_at: datetime
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    interviewer_name: Optional[str] = None
    interviewer_email: Optional[str] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    completed: bool = False
    feedback: Optional[str] = None

class StatusHistory(BaseModel):
    status: ApplicationStatus
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    source: Optional[str] = None  # email, manual, automated

class ApplicationBase(BaseModel):
    job_id: str
    company_name: str = Field(..., min_length=1, max_length=100)
    position_title: str = Field(..., min_length=1, max_length=100)
    job_url: Optional[str] = None
    application_method: ApplicationMethod
    
    # Contact information
    contact_person: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    
    # Application details
    cover_letter_sent: bool = False
    resume_sent: bool = True
    portfolio_sent: bool = False
    
    # Salary and benefits
    salary_offered: Optional[int] = Field(None, ge=0)
    salary_currency: str = "USD"
    benefits_offered: Optional[str] = None
    
    # Notes and tracking
    notes: Optional[str] = Field(None, max_length=2000)
    follow_up_date: Optional[datetime] = None
    
    @validator('job_url')
    def validate_job_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Job URL must be a valid HTTP/HTTPS URL')
        return v

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    company_name: Optional[str] = Field(None, min_length=1, max_length=100)
    position_title: Optional[str] = Field(None, min_length=1, max_length=100)
    job_url: Optional[str] = None
    application_method: Optional[ApplicationMethod] = None
    contact_person: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    salary_offered: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    benefits_offered: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=2000)
    follow_up_date: Optional[datetime] = None

class ApplicationInDB(ApplicationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    status: ApplicationStatus = ApplicationStatus.DRAFT
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    applied_at: Optional[datetime] = None
    
    # Document references
    resume_id: Optional[str] = None
    cover_letter_id: Optional[str] = None
    
    # Status tracking
    status_history: List[StatusHistory] = Field(default_factory=list)
    
    # Interview tracking
    interviews: List[Interview] = Field(default_factory=list)
    
    # Email tracking
    email_thread_ids: List[str] = Field(default_factory=list)
    last_email_received: Optional[datetime] = None
    
    # Analytics
    response_time_days: Optional[int] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Application(ApplicationBase):
    id: str
    user_id: str
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    applied_at: Optional[datetime]
    resume_id: Optional[str]
    cover_letter_id: Optional[str]
    status_history: List[StatusHistory]
    interviews: List[Interview]
    email_thread_ids: List[str]
    last_email_received: Optional[datetime]
    response_time_days: Optional[int]

class ApplicationSummary(BaseModel):
    """Summary view of application for lists"""
    id: str
    company_name: str
    position_title: str
    status: ApplicationStatus
    applied_at: Optional[datetime]
    last_updated: datetime
    response_time_days: Optional[int]

class ApplicationStats(BaseModel):
    """Application statistics"""
    total: int
    by_status: Dict[ApplicationStatus, int]
    by_method: Dict[ApplicationMethod, int]
    average_response_time: Optional[float]
    success_rate: float
    this_month: int
    this_week: int

class BulkApplicationUpdate(BaseModel):
    application_ids: List[str] = Field(..., min_items=1, max_items=100)
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)
    
class ApplicationFilter(BaseModel):
    """Filter parameters for application queries"""
    status: Optional[List[ApplicationStatus]] = None
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    application_method: Optional[List[ApplicationMethod]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    has_interviews: Optional[bool] = None
    follow_up_due: Optional[bool] = None