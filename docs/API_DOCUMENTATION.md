# LEGO Bricks API Documentation

## Overview

The LEGO Bricks API provides intelligent job analysis and CV/Cover Letter generation using AI-powered role detection and percentage-based template matching.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently, no authentication is required for API endpoints.

## Endpoints

### 1. Analyze Job Description

Analyzes a job description to determine the best matching role category and provides detailed percentage breakdown.

**Endpoint:** `POST /analyze-job`

**Request Body:**
```json
{
  "jobDescription": "string (required if jobUrl not provided)",
  "jobUrl": "string (optional - URL to fetch job description from)"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "roleType": "Full Stack Developer",
    "roleCategory": "fullstack_developer",
    "keywords": ["react", "typescript", "node.js", "aws", "docker"],
    "requiredSkills": ["react", "typescript", "node.js", "python", "aws"],
    "achievements": [
      "26-server incident resolution in 5 hours",
      "45% cloud cost reduction",
      "35% MTTR reduction",
      "24/7 multi-region support"
    ],
    "company": "TechCorp",
    "title": "Senior Full Stack Developer",
    "templateInfo": {
      "keywords": ["fullstack", "react", "typescript", "javascript"],
      "cv_template": "job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CV.tex",
      "cl_template": "job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CL.tex",
      "priority": 2,
      "category": "fullstack_developer",
      "display_name": "Fullstack Developer"
    },
    "aiAnalysis": {
      "used": true,
      "confidence": 0.85,
      "reasoning": "Strong indicators for full-stack development with React and backend technologies",
      "model": "MiniMax-M2"
    },
    "rolePercentages": {
      "fullstack_developer": 45.2,
      "backend_developer": 28.1,
      "devops_cloud": 15.3,
      "android_developer": 8.7,
      "ai_product_engineer": 2.7
    },
    "roleBreakdown": [
      {"role": "fullstack_developer", "percentage": 45.2},
      {"role": "backend_developer", "percentage": 28.1},
      {"role": "devops_cloud", "percentage": 15.3},
      {"role": "android_developer", "percentage": 8.7}
    ],
    "roleScores": {
      "fullstack_developer": 12.5,
      "backend_developer": 7.8,
      "devops_cloud": 4.2,
      "android_developer": 2.4,
      "ai_product_engineer": 0.7
    },
    "confidenceScore": 0.85
  },
  "jobDescription": "Full job description text..."
}
```

**Response Fields:**

- `roleType`: Human-readable role name (e.g., "Full Stack Developer")
- `roleCategory`: Internal category key used for template matching (e.g., "fullstack_developer")
- `keywords`: Top 15 extracted keywords from the job description
- `requiredSkills`: Top 10 most relevant skills for the role
- `achievements`: Relevant achievements to highlight for this role type
- `company`: Extracted company name from job description
- `title`: Extracted job title from job description
- `templateInfo`: Information about the selected template including file paths and priority
- `aiAnalysis`: Details about AI analysis including confidence and reasoning
- `rolePercentages`: **NEW** - Percentage scores for all role categories (0-100%, normalized to sum to 100%)
- `roleBreakdown`: **NEW** - Filtered list of significant roles (>5% threshold) with percentages
- `roleScores`: **NEW** - Raw weighted scores before percentage normalization
- `confidenceScore`: **NEW** - Overall confidence in the role detection (0.0-1.0)

**Error Responses:**
```json
{
  "error": "Job description or URL required"
}
```

### 2. Generate LEGO Application

Generates customized CV and Cover Letter based on job analysis.

**Endpoint:** `POST /generate-lego-application`

**Request Body:**
```json
{
  "jobDescription": "string (required)",
  "analysis": {
    "roleType": "Full Stack Developer",
    "roleCategory": "fullstack_developer",
    "company": "TechCorp",
    "title": "Senior Full Stack Developer",
    "rolePercentages": {...},
    "roleBreakdown": [...],
    "confidenceScore": 0.85
  },
  "customizationNotes": "string (optional - user's specific requirements)"
}
```

**Response:**
```json
{
  "success": true,
  "files": {
    "cv": {
      "filename": "TechCorp_Senior_Full_Stack_Developer_CV.tex",
      "content": "LaTeX CV content...",
      "path": "/path/to/generated/cv.tex"
    },
    "coverLetter": {
      "filename": "TechCorp_Senior_Full_Stack_Developer_CL.tex", 
      "content": "LaTeX Cover Letter content...",
      "path": "/path/to/generated/cl.tex"
    }
  },
  "analysis": {
    "roleType": "Full Stack Developer",
    "roleCategory": "fullstack_developer",
    "rolePercentages": {...},
    "roleBreakdown": [...],
    "confidenceScore": 0.85,
    "templateUsed": "job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CV.tex"
  },
  "customization": {
    "aiEnhanced": true,
    "userNotesApplied": true,
    "keyTechnologiesHighlighted": ["react", "typescript", "node.js"]
  }
}
```

## Role Categories

The system supports the following role categories with their priorities:

| Priority | Role Category | Display Name | Keywords |
|----------|---------------|--------------|----------|
| 1 | `it_business_analyst` | IT Business Analyst | business analyst, requirements gathering, stakeholder |
| 1 | `android_developer` | Android Developer | android, kotlin, mobile app, aosp |
| 1 | `devops_fintech` | DevOps FinTech | fintech, financial, banking, payment |
| 1 | `ai_product_engineer` | AI Product Engineer | ai engineer, model training, rag, mlops |
| 2 | `fullstack_developer` | Fullstack Developer | fullstack, react, typescript, web developer |
| 3 | `backend_developer` | Backend Developer | backend, java, spring boot, microservices |
| 4 | `devops_cloud` | DevOps Cloud | devops, aws, kubernetes, docker |
| 4 | `incident_management_sre` | SRE | incident, sre, monitoring, on-call |
| 5 | `platform_engineer` | Platform Engineer | platform engineer, internal tools, devex |

## AI Configuration

The system uses multiple AI models for enhanced analysis:

### Primary AI Model: MiniMax M2
- **Purpose**: Job description analysis and role detection
- **Confidence Threshold**: 0.5 (50%)
- **Fallback**: Keyword-based matching if AI unavailable

### AI Integration Keywords
The system distinguishes between:
- **AI Product Engineer**: Building AI systems (model training, RAG, MLOps)
- **Software Engineer with AI**: Using AI APIs (OpenAI API, Claude API, AI integration)

## Percentage-Based Scoring

### How It Works
1. **Keyword Extraction**: Extract keywords for each role category from job description
2. **Weighted Scoring**: Calculate scores based on keyword matches and role priority
3. **Percentage Normalization**: Convert scores to percentages (0-100%, sum = 100%)
4. **Role Selection**: Select role with highest percentage
5. **Content Alignment**: Validate template content aligns with job requirements

### Thresholds
- **Role Breakdown Threshold**: 5% (only roles with ≥5% are included in breakdown)
- **Mixed Role Warning**: Triggered when primary role <50%
- **Content Alignment**: Minimum 10% of role keywords must match job description
- **AI Misclassification Prevention**: AI Product Engineer requires ≥50% to prevent misclassification

### Example Percentage Distribution
```json
{
  "fullstack_developer": 45.2,    // Primary role - selected
  "backend_developer": 28.1,      // Secondary role
  "devops_cloud": 15.3,          // Tertiary role  
  "android_developer": 8.7,       // Minor role
  "ai_product_engineer": 2.7      // Minimal role (filtered out of breakdown)
}
```

## Error Handling

### Common Error Scenarios
1. **Template Not Found**: System automatically falls back to next best template
2. **AI Analysis Failed**: Falls back to keyword-based matching
3. **Invalid Job Description**: Returns error with suggestion to provide valid input
4. **URL Fetch Failed**: Returns error suggesting manual copy-paste

### Error Response Format
```json
{
  "error": "Error description",
  "suggestion": "Helpful suggestion for user",
  "fallback": "Alternative action taken (if any)"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## Examples

### Example 1: Full-Stack Developer Job
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "We are looking for a Full-stack Developer with React and TypeScript experience. Backend development with Node.js required. Experience with AWS and Docker is a plus."
  }'
```

### Example 2: DevOps Engineer Job
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "DevOps Engineer position. Must have AWS, Kubernetes, and Terraform experience. CI/CD pipeline knowledge required."
  }'
```

### Example 3: AI Product Engineer Job
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "AI Engineer needed to build and train machine learning models. Experience with PyTorch, model training, and MLOps required. RAG and vector databases experience essential."
  }'
```

## Monitoring and Logging

The system provides comprehensive logging for:
- Role detection process with keyword matches
- Template selection and fallback usage
- AI analysis results and confidence scores
- Error scenarios and recovery actions
- Mixed role warnings when primary role <50%

Log levels:
- `INFO`: Normal operation, role selection results
- `WARNING`: Mixed roles, template misalignment, fallbacks
- `ERROR`: Template loading failures, AI analysis errors
- `DEBUG`: Detailed keyword matches, percentage calculations

## Troubleshooting

### Common Issues

1. **Wrong Template Selected**
   - Check `rolePercentages` in response to understand scoring
   - Verify job description contains relevant keywords
   - Check logs for content alignment warnings

2. **Low Confidence Score**
   - Job description may be too generic or mixed-role
   - Check `roleBreakdown` for percentage distribution
   - Consider adding more specific keywords to job description

3. **AI Analysis Not Working**
   - Verify MiniMax API configuration
   - Check network connectivity
   - System will automatically fall back to keyword matching

4. **Template Loading Errors**
   - Verify template files exist in specified paths
   - Check file permissions
   - System will use fallback templates automatically