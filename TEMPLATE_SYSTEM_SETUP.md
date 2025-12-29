# Template-Based LEGO System Setup

## Overview
Successfully implemented a template-based LEGO bricks system for intelligent CV generation based on job role detection.

## What Was Done

### 1. Created CV Template Manager (`backend/cv_templates.py`)
- **Role Categories Defined**: 8 role categories with keyword matching
  - `android_developer` - Android, Kotlin, Java, mobile, AOSP, automotive, infotainment
  - `devops_cloud` - DevOps, cloud, AWS, Azure, Kubernetes, Docker, Terraform, CI/CD
  - `incident_management_sre` - Incident, SRE, site reliability, on-call, monitoring
  - `fullstack_developer` - Fullstack, React, Vue, Angular, Node.js, frontend, backend
  - `ict_software_engineer` - ICT, software engineer, .NET, C#, Java, Spring Boot
  - `platform_engineer` - Platform engineer, infrastructure, internal tools
  - `integration_architect` - Integration, architect, API, microservices
  - `backend_developer` - Backend, API, database, microservices, REST

- **Smart Role Detection**: 
  - Analyzes job description text
  - Counts keyword occurrences
  - Applies priority weighting
  - Returns best matching role category

- **Template Loading**:
  - Searches for `*_CV.tex` files in template directories
  - Loads template content for customization
  - Fallback to LEGO bricks if no template found

### 2. Integrated Template Manager into LEGO API (`backend/app/lego_api.py`)
- **Updated `analyze_job_description()`**:
  - Now uses `CVTemplateManager.analyze_job_role()` for better role detection
  - Returns `roleCategory` and `templateInfo` in analysis results

- **Updated `build_lego_cv()`**:
  - Accepts `role_category` parameter
  - Loads template using `CVTemplateManager.load_template()`
  - Returns template content as base (customization to be added later)
  - Falls back to LEGO bricks generation if no template

- **Updated `generate_lego_application()`**:
  - Passes `role_category` to `build_lego_cv()`

### 3. Created Android Developer Template
- **Location**: `job_applications/ecarx_android_developer/`
- **Files Created**:
  - `Ecarx_Android_Developer_CV.tex` - Android developer CV template
  - `Ecarx_Android_Developer_CL.tex` - Android developer cover letter template

- **Template Features**:
  - Consistent Tata/ALTEN blue styling (RGB 0,51,102)
  - Centered header with name, title, contact info
  - Blue section headers with horizontal rules
  - Focus on Android Auto, AOSP, Kotlin/Java, automotive technology
  - Real work experience at ECARX with Android AOSP achievements
  - Android Auto projects (AI Bot, CarTVPlayer)
  - Learning C++ for native Android development

### 4. Template Mapping
```python
'android_developer': {
    'keywords': ['android', 'kotlin', 'java', 'mobile', 'aosp', 'automotive', 'infotainment'],
    'template_path': 'job_applications/ecarx_android_developer',
    'priority': 1  # Highest priority
}
```

## How It Works

### Job Analysis Flow
1. User submits job description (text or URL)
2. `CVTemplateManager.analyze_job_role()` analyzes keywords
3. Returns best matching role category (e.g., `android_developer`)
4. System loads corresponding template from `job_applications/ecarx_android_developer/`
5. Template is used as base for CV generation

### Example: Android Platform Developer Job
```
Job Description: "Android Platform Developer for automotive infotainment systems. 
Experience with Kotlin, Java, AOSP, Android Auto required."

Detection Result:
- Role Category: android_developer
- Template: job_applications/ecarx_android_developer/Ecarx_Android_Developer_CV.tex
- Keywords Matched: android, kotlin, java, aosp, automotive, infotainment
```

## Next Steps

### 1. Deploy to VPS Server
- Upload updated files to server:
  - `backend/cv_templates.py`
  - `backend/app/lego_api.py`
  - `job_applications/ecarx_android_developer/` (entire folder)

### 2. Test Template System
- Test with Android job URL: https://careers.cpacsystems.se/jobs/6832158-android-platform-developer
- Verify role detection works correctly
- Verify template loads successfully
- Verify PDF generation works

### 3. Add Template Customization (Future Enhancement)
- Parse template LaTeX structure
- Replace placeholders with job-specific content
- Customize profile summary based on job requirements
- Adjust skills section based on job keywords
- Modify experience bullets to highlight relevant achievements

### 4. Add More Templates
- Create templates for other role categories
- Map existing job applications to role categories
- Ensure all 8 role categories have templates

## Files Modified
- ✅ `backend/cv_templates.py` - Created template manager
- ✅ `backend/app/lego_api.py` - Integrated template system
- ✅ `job_applications/ecarx_android_developer/Ecarx_Android_Developer_CV.tex` - Created
- ✅ `job_applications/ecarx_android_developer/Ecarx_Android_Developer_CL.tex` - Created

## Files to Deploy
```bash
# Upload to server
scp -P 1025 backend/cv_templates.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/
scp -P 1025 -r job_applications/ecarx_android_developer harvad@94.72.141.71:/var/www/lego-job-generator/backend/job_applications/

# Restart Gunicorn
ssh harvad@94.72.141.71 -p 1025 "pkill -9 gunicorn && cd /var/www/lego-job-generator/backend && source venv/bin/activate && gunicorn --bind 127.0.0.1:5000 --workers 3 --daemon lego_app:app"
```

## Benefits
1. **Better ATS Optimization**: Uses proven templates optimized for specific roles
2. **Faster Ma