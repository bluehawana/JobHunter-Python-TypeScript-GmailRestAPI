from typing import Optional, List, Dict
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class JobPosting(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    source: str  # gmail, linkedin, indeed
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    requirements: List[str] = []
    salary: Optional[Dict] = None
    posting_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    url: Optional[str] = None
    keywords: List[str] = []
    match_score: float = 0.0
    confidence_score: float = 0.0
    is_saved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Gmail specific fields
    email_id: Optional[str] = None
    thread_id: Optional[str] = None
    from_email: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class JobCreate(BaseModel):
    source: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    url: Optional[str] = None
    keywords: List[str] = []

class AggregatedJob(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    
    # Source information
    source: str  # linkedin_saved, gmail_linkedin, gmail_indeed, arbetsformedlingen, linkedin_search
    source_job_id: Optional[str] = None  # Original job ID from source
    source_url: str  # Original job URL
    
    # Basic job information
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: List[str] = []
    salary: Optional[str] = None
    job_type: Optional[str] = None  # Full-time, Part-time, Contract, etc.
    seniority_level: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    remote_option: bool = False
    
    # Content analysis
    keywords: List[str] = []
    match_score: float = 0.0  # How well it matches user preferences
    confidence_score: float = 0.0  # Quality of job extraction
    
    # Application workflow
    application_status: str = "discovered"  # discovered, saved, generated, applied, rejected, archived
    priority: str = "medium"  # low, medium, high, urgent
    user_notes: Optional[str] = None
    
    # Document generation
    cv_generated: bool = False
    cover_letter_generated: bool = False
    cv_file_path: Optional[str] = None
    cover_letter_file_path: Optional[str] = None
    documents_generated_at: Optional[datetime] = None
    
    # Application tracking
    applied_at: Optional[datetime] = None
    application_method: Optional[str] = None  # email, linkedin, company_site
    response_received: bool = False
    response_date: Optional[datetime] = None
    interview_scheduled: bool = False
    interview_date: Optional[datetime] = None
    
    # Source-specific metadata
    email_id: Optional[str] = None  # For Gmail sources
    email_thread_id: Optional[str] = None
    email_subject: Optional[str] = None
    posting_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    
    # System metadata
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    is_duplicate: bool = False
    duplicate_of: Optional[PyObjectId] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class SavedJobCreate(BaseModel):
    linkedin_job_id: str
    title: str
    company: str
    location: Optional[str] = None
    description: str
    url: str
    salary: Optional[str] = None
    job_type: Optional[str] = None
    priority: str = "medium"
    notes: Optional[str] = None

class SavedJobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    application_status: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_saved: Optional[bool] = None