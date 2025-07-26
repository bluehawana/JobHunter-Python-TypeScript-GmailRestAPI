from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class SalaryRange(BaseModel):
    min: Optional[int] = Field(None, ge=0, description="Minimum salary")
    max: Optional[int] = Field(None, ge=0, description="Maximum salary")
    currency: str = Field("USD", description="Currency code")
    
    @field_validator('max')
    @classmethod
    def validate_salary_range(cls, v, info):
        if v is not None and 'min' in info.data and info.data['min'] is not None:
            if v < info.data['min']:
                raise ValueError('Maximum salary must be greater than minimum salary')
        return v

class UserPreferences(BaseModel):
    # Job search preferences
    keywords: List[str] = Field(default_factory=list, description="Job search keywords")
    job_types: List[str] = Field(default_factory=list, description="Preferred job types")
    locations: List[str] = Field(default_factory=list, description="Preferred locations")
    salary_range: Optional[SalaryRange] = None
    remote_work: bool = Field(False, description="Open to remote work")
    
    # Application preferences
    auto_apply: bool = Field(False, description="Automatically apply to matching jobs")
    daily_job_limit: int = Field(5, ge=1, le=50, description="Maximum jobs to apply per day")
    
    # Document preferences
    resume_template: str = Field("default", description="Resume template to use")
    cover_letter_template: str = Field("default", description="Cover letter template to use")
    
    @field_validator('keywords')
    @classmethod
    def validate_keywords(cls, v):
        if len(v) > 50:
            raise ValueError('Maximum 50 keywords allowed')
        return [keyword.strip().lower() for keyword in v if keyword.strip()]
    
    @field_validator('job_types')
    @classmethod
    def validate_job_types(cls, v):
        valid_types = ['full-time', 'part-time', 'contract', 'freelance', 'internship', 'temporary']
        for job_type in v:
            if job_type.lower() not in valid_types:
                raise ValueError(f'Invalid job type: {job_type}')
        return v

class GmailIntegration(BaseModel):
    connected: bool = False
    email: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scopes: List[str] = Field(default_factory=list)
    last_sync: Optional[datetime] = None

class LinkedInIntegration(BaseModel):
    connected: bool = False
    profile_id: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    last_sync: Optional[datetime] = None

class IndeedIntegration(BaseModel):
    connected: bool = False
    api_key: Optional[str] = None
    last_sync: Optional[datetime] = None

class UserIntegrations(BaseModel):
    gmail: GmailIntegration = Field(default_factory=GmailIntegration)
    linkedin: LinkedInIntegration = Field(default_factory=LinkedInIntegration)
    indeed: IndeedIntegration = Field(default_factory=IndeedIntegration)

class UserProfile(BaseModel):
    # Personal information
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]+$')
    location: Optional[str] = Field(None, max_length=100)
    
    # Professional information
    current_title: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = Field(None, max_length=200)
    
    # Resume information
    summary: Optional[str] = Field(None, max_length=1000)
    linkedin_url: Optional[str] = Field(None, pattern=r'^https://www\.linkedin\.com/in/[\w\-]+/?$')
    portfolio_url: Optional[str] = None
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if len(v) > 100:
            raise ValueError('Maximum 100 skills allowed')
        return [skill.strip() for skill in v if skill.strip()]

class UserBase(BaseModel):
    email: EmailStr
    profile: UserProfile
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    integrations: UserIntegrations = Field(default_factory=UserIntegrations)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    profile: Optional[UserProfile] = None
    preferences: Optional[UserPreferences] = None

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Statistics
    total_jobs_found: int = 0
    total_applications: int = 0
    total_documents_generated: int = 0
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class User(BaseModel):
    id: str
    email: EmailStr
    profile: UserProfile
    preferences: UserPreferences
    integrations: UserIntegrations
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    # Statistics
    total_jobs_found: int
    total_applications: int
    total_documents_generated: int

class UserPublic(BaseModel):
    """Public user information (for API responses)"""
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserPublic

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class EmailVerification(BaseModel):
    token: str

# OAuth related models
class OAuthToken(BaseModel):
    user_id: str
    service: str  # gmail, linkedin, indeed
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scopes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GmailAuthRequest(BaseModel):
    authorization_code: str
    state: Optional[str] = None

class UserStats(BaseModel):
    """User statistics for dashboard"""
    total_jobs_found: int
    total_applications: int
    applications_pending: int
    applications_rejected: int
    applications_interview: int
    applications_offer: int
    documents_generated: int
    ats_average_score: float
    last_activity: Optional[datetime]