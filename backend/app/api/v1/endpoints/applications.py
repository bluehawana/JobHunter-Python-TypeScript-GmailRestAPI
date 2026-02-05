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

class TailoredApplicationRequest(BaseModel):
    job_details: dict
    application_type: str = "android_focused"  # android_focused, fullstack, generic

class TailoredApplicationResponse(BaseModel):
    success: bool
    message: str
    cv_generated: bool = False
    cover_letter_generated: bool = False
    email_sent: bool = False
    error: Optional[str] = None

@router.post("/generate-tailored", response_model=TailoredApplicationResponse)
async def generate_tailored_application(
    request: TailoredApplicationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate tailored CV and cover letter based on job details
    Uses the same system that created the successful ECARX application
    """
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        
        from true_template_automation import TrueTemplateAutomation
        
        # Initialize automation system
        automation = TrueTemplateAutomation()
        
        # Prepare job details for automation
        job_data = {
            'company': request.job_details.get('company', 'Unknown Company'),
            'title': request.job_details.get('title', 'Software Developer'),
            'location': request.job_details.get('location', 'Sweden'),
            'description': request.job_details.get('description', ''),
            'requirements': request.job_details.get('requirements', []),
            'url': request.job_details.get('url', ''),
            'email_subject': f"{request.job_details.get('title', 'Position')} at {request.job_details.get('company', 'Company')}",
            'sender': 'careers@company.com',
            'body': request.job_details.get('description', ''),
            'raw_content': f"{request.job_details.get('title', '')} {request.job_details.get('company', '')} {' '.join(request.job_details.get('requirements', []))}"
        }
        
        # Add application type specific context for LEGO bricks
        if request.application_type == "android_focused":
            job_data['android_focus'] = {
                'experience_years': '5+',
                'primary_language': 'Kotlin',
                'secondary_language': 'Java',
                'ide': 'Android Studio',
                'automotive_projects': 4,
                'learning_areas': ['Native AOSP', 'C/C++', 'RRO'],
                'cultural_advantage': 'Mandarin + Cross-cultural communication'
            }
            # Force LEGO bricks to use Android focus
            job_data['force_android_focus'] = True
        
        cv_generated = False
        cover_letter_generated = False
        email_sent = False
        
        # Generate CV
        try:
            cv_latex = await automation._generate_true_cv(job_data)
            if cv_latex:
                cv_pdf = await automation._compile_latex_to_pdf(cv_latex, f"tailored_cv_{job_data['company']}")
                if cv_pdf:
                    cv_generated = True
        except Exception as e:
            logger.error(f"CV generation error: {str(e)}")
        
        # Generate Cover Letter
        try:
            cl_latex = await automation._generate_true_cover_letter(job_data)
            if cl_latex:
                cl_pdf = await automation._compile_latex_to_pdf(cl_latex, f"tailored_cl_{job_data['company']}")
                if cl_pdf:
                    cover_letter_generated = True
        except Exception as e:
            logger.error(f"Cover letter generation error: {str(e)}")
        
        # Send email if both documents generated
        if cv_generated and cover_letter_generated:
            try:
                email_result = await automation._send_true_email(job_data, cv_pdf, cl_pdf)
                email_sent = email_result
            except Exception as e:
                logger.error(f"Email sending error: {str(e)}")
        
        # Determine success
        success = cv_generated and cover_letter_generated
        
        if success:
            message = f"Tailored application generated for {job_data['title']} at {job_data['company']}"
            if email_sent:
                message += " and sent to your email!"
            else:
                message += " but email sending failed."
        else:
            message = "Failed to generate complete application package"
        
        return TailoredApplicationResponse(
            success=success,
            message=message,
            cv_generated=cv_generated,
            cover_letter_generated=cover_letter_generated,
            email_sent=email_sent,
            error=None if success else "Document generation failed"
        )
        
    except Exception as e:
        logger.error(f"Tailored application generation error: {str(e)}")
        return TailoredApplicationResponse(
            success=False,
            message="Application generation failed",
            cv_generated=False,
            cover_letter_generated=False,
            email_sent=False,
            error=str(e)
        )