from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Application Automation"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Alternative frontend port
        "https://localhost:3000",
        "https://localhost:8080",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database settings - Supabase PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/jobhunter")
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = os.getenv("SENDER_EMAIL", "")
    SOURCE_GMAIL_CREDENTIALS: Optional[str] = os.getenv("SOURCE_GMAIL_CREDENTIALS")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_GMAIL_PASSWORD: Optional[str] = os.getenv("SENDER_GMAIL_PASSWORD")
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_FROM_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    GMAIL_APP_PASSWORD: Optional[str] = os.getenv("GMAIL_APP_PASSWORD")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # External API settings
    GMAIL_CLIENT_ID: Optional[str] = os.getenv("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET: Optional[str] = os.getenv("GMAIL_CLIENT_SECRET")
    GMAIL_CREDENTIALS: Optional[str] = os.getenv("GMAIL_CREDENTIALS")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    LINKEDIN_CLIENT_ID: Optional[str] = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: Optional[str] = os.getenv("LINKEDIN_CLIENT_SECRET")
    LINKEDIN_ACCESS_TOKEN: Optional[str] = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    # Claude API settings
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_AUTH_TOKEN: Optional[str] = os.getenv("ANTHROPIC_AUTH_TOKEN")
    ANTHROPIC_BASE_URL: Optional[str] = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    CLAUDE_MODEL: Optional[str] = os.getenv("CLAUDE_MODEL")
    
    # R2 Storage settings
    R2_ENDPOINT: Optional[str] = os.getenv("R2_ENDPOINT")
    R2_ENDPOINT_URL: Optional[str] = os.getenv("R2_ENDPOINT_URL")
    R2_ACCESS_KEY: Optional[str] = os.getenv("R2_ACCESS_KEY")
    R2_ACCESS_KEY_ID: Optional[str] = os.getenv("R2_ACCESS_KEY_ID")
    R2_SECRET_KEY: Optional[str] = os.getenv("R2_SECRET_KEY")
    R2_SECRET_ACCESS_KEY: Optional[str] = os.getenv("R2_SECRET_ACCESS_KEY")
    R2_BUCKET: str = os.getenv("R2_BUCKET", "jobhunter-documents")
    R2_BUCKET_NAME: Optional[str] = os.getenv("R2_BUCKET_NAME")
    R2_PUBLIC_DOMAIN: Optional[str] = os.getenv("R2_PUBLIC_DOMAIN")
    BASE_URL: Optional[str] = os.getenv("BASE_URL")
    
    # Job Search APIs
    GOOGLE_CUSTOM_SEARCH_API_KEY: Optional[str] = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    GOOGLE_CUSTOM_SEARCH_ENGINE_ID: Optional[str] = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
    INDEED_PUBLISHER_ID: Optional[str] = os.getenv("INDEED_PUBLISHER_ID")
    RAPIDAPI_KEY: Optional[str] = os.getenv("RAPIDAPI_KEY")  # For job search APIs
    
    # Redis/Celery
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER")
    USER_PHONE_NUMBER: Optional[str] = os.getenv("USER_PHONE_NUMBER")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Allow extra environment variables

settings = Settings()