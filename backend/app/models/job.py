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

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_saved: Optional[bool] = None