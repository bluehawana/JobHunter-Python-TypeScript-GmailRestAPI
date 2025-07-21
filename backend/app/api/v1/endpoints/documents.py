from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class DocumentGenerate(BaseModel):
    job_id: str
    document_type: str  # resume, cover_letter
    customizations: Optional[List[str]] = None

class Document(BaseModel):
    id: str
    user_id: str
    job_id: str
    document_type: str
    filename: str
    pdf_url: str
    latex_source: str
    ats_score: float
    created_at: str
    customizations: List[str]

@router.post("/generate", response_model=Document)
async def generate_document(
    doc_request: DocumentGenerate,
    current_user: dict = Depends(get_current_user)
):
    """Generate a customized resume or cover letter"""
    # Mock document generation
    mock_document = {
        "id": "doc_123",
        "user_id": current_user["id"],
        "job_id": doc_request.job_id,
        "document_type": doc_request.document_type,
        "filename": f"{doc_request.document_type}_techcorp.pdf",
        "pdf_url": f"/documents/doc_123.pdf",
        "latex_source": "\\documentclass{article}...",
        "ats_score": 0.85,
        "created_at": "2024-01-15T10:30:00Z",
        "customizations": doc_request.customizations or []
    }
    
    return Document(**mock_document)

@router.get("/", response_model=List[Document])
async def get_documents(
    document_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get user's documents"""
    # Mock documents
    mock_documents = [
        {
            "id": "doc_1",
            "user_id": current_user["id"],
            "job_id": "job_1",
            "document_type": "resume",
            "filename": "resume_techcorp.pdf",
            "pdf_url": "/documents/doc_1.pdf",
            "latex_source": "\\documentclass{article}...",
            "ats_score": 0.85,
            "created_at": "2024-01-15T10:30:00Z",
            "customizations": ["highlighted python skills", "emphasized aws experience"]
        }
    ]
    
    if document_type:
        mock_documents = [doc for doc in mock_documents if doc["document_type"] == document_type]
    
    return [Document(**doc) for doc in mock_documents]

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific document"""
    mock_document = {
        "id": document_id,
        "user_id": current_user["id"],
        "job_id": "job_1",
        "document_type": "resume",
        "filename": "resume_techcorp.pdf",
        "pdf_url": f"/documents/{document_id}.pdf",
        "latex_source": "\\documentclass{article}...",
        "ats_score": 0.85,
        "created_at": "2024-01-15T10:30:00Z",
        "customizations": ["highlighted python skills"]
    }
    
    return Document(**mock_document)