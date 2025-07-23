from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.models.user import PyObjectId

class DocumentType(str, Enum):
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    PORTFOLIO = "portfolio"
    REFERENCE_LETTER = "reference_letter"

class DocumentFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    LATEX = "latex"
    MARKDOWN = "markdown"

class ATSOptimization(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="ATS compatibility score")
    keywords_matched: List[str] = Field(default_factory=list)
    keywords_missing: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    formatting_score: float = Field(..., ge=0.0, le=1.0)
    readability_score: float = Field(..., ge=0.0, le=1.0)

class DocumentCustomization(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_requirements: List[str] = Field(default_factory=list)
    skills_emphasized: List[str] = Field(default_factory=list)
    experience_highlighted: List[str] = Field(default_factory=list)
    custom_sections: Dict[str, str] = Field(default_factory=dict)

class DocumentVersion(BaseModel):
    version: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    changes_summary: Optional[str] = None
    file_url: Optional[str] = None
    ats_score: Optional[float] = None

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    document_type: DocumentType
    template_name: str = Field("default", max_length=100)
    
    # Content
    latex_source: Optional[str] = None
    html_content: Optional[str] = None
    markdown_content: Optional[str] = None
    
    # Customization
    customization: DocumentCustomization = Field(default_factory=DocumentCustomization)
    
    # Metadata
    tags: List[str] = Field(default_factory=list, max_items=20)
    is_template: bool = False
    is_default: bool = False
    
    @validator('tags')
    def validate_tags(cls, v):
        return [tag.strip().lower() for tag in v if tag.strip()]

class DocumentCreate(DocumentBase):
    job_id: Optional[str] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    latex_source: Optional[str] = None
    html_content: Optional[str] = None
    markdown_content: Optional[str] = None
    customization: Optional[DocumentCustomization] = None
    tags: Optional[List[str]] = Field(None, max_items=20)
    
    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            return [tag.strip().lower() for tag in v if tag.strip()]
        return v

class DocumentInDB(DocumentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    job_id: Optional[str] = None
    
    # File information
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    file_format: DocumentFormat = DocumentFormat.PDF
    
    # Versions
    current_version: int = 1
    versions: List[DocumentVersion] = Field(default_factory=list)
    
    # ATS optimization
    ats_optimization: Optional[ATSOptimization] = None
    
    # Usage tracking
    download_count: int = 0
    last_downloaded: Optional[datetime] = None
    applications_used: List[str] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Document(DocumentBase):
    id: str
    user_id: str
    job_id: Optional[str]
    file_url: Optional[str]
    file_size: Optional[int]
    file_format: DocumentFormat
    current_version: int
    versions: List[DocumentVersion]
    ats_optimization: Optional[ATSOptimization]
    download_count: int
    last_downloaded: Optional[datetime]
    applications_used: List[str]
    created_at: datetime
    updated_at: datetime

class DocumentSummary(BaseModel):
    """Summary view for document lists"""
    id: str
    title: str
    document_type: DocumentType
    file_format: DocumentFormat
    ats_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    download_count: int

class DocumentGenerate(BaseModel):
    """Request to generate a new document"""
    job_id: str
    document_type: DocumentType
    template_name: str = "default"
    customizations: Optional[List[str]] = Field(None, max_items=10)
    optimize_for_ats: bool = True
    
    @validator('customizations')
    def validate_customizations(cls, v):
        if v is not None:
            return [c.strip() for c in v if c.strip()]
        return v

class DocumentTemplate(BaseModel):
    """Document template definition"""
    name: str = Field(..., min_length=1, max_length=100)
    document_type: DocumentType
    description: Optional[str] = Field(None, max_length=500)
    latex_template: str
    variables: List[str] = Field(default_factory=list)
    preview_url: Optional[str] = None
    is_premium: bool = False
    category: Optional[str] = None

class BulkDocumentOperation(BaseModel):
    document_ids: List[str] = Field(..., min_items=1, max_items=50)
    operation: str = Field(..., regex="^(delete|download|optimize)$")
    
class DocumentStats(BaseModel):
    """Document statistics"""
    total_documents: int
    by_type: Dict[DocumentType, int]
    by_format: Dict[DocumentFormat, int]
    average_ats_score: Optional[float]
    total_downloads: int
    most_used_template: Optional[str]
    recent_documents: int  # Last 30 days

class DocumentFilter(BaseModel):
    """Filter parameters for document queries"""
    document_type: Optional[List[DocumentType]] = None
    file_format: Optional[List[DocumentFormat]] = None
    template_name: Optional[str] = None
    min_ats_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    is_template: Optional[bool] = None