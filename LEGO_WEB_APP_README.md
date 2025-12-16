# 🧱 LEGO Bricks Job Application Generator - Web Application

## Overview

A full-stack web application that automatically generates tailored CV and Cover Letters using the LEGO bricks methodology. Hosted at **jobs.bluehawana.com**.

## Features

✅ **Job Analysis** - Paste job URL or description, AI analyzes requirements
✅ **LEGO Bricks Assembly** - Dynamically builds role-specific CV & CL
✅ **Live Preview** - View generated PDFs in browser
✅ **Iterative Refinement** - Provide feedback and regenerate
✅ **Professional Styling** - Blue accents, clean design
✅ **ATS Optimized** - Keywords matched to job requirements

## Architecture

### Frontend (React + TypeScript)
- **Location:** `frontend/src/pages/LegoJobGenerator.tsx`
- **Styling:** `frontend/src/styles/LegoJobGenerator.css`
- **Features:**
  - Job input (URL or paste)
  - Analysis display
  - PDF preview
  - Feedback loop

### Backend (Flask + Python)
- **Location:** `backend/app/lego_api.py`
- **Main App:** `backend/lego_app.py`
- **Features:**
  - Job description analysis
  - LEGO bricks selection
  - LaTeX generation
  - PDF compilation

## Installation

### Prerequisites
```bash
# Install pdflatex (for PDF generation)
brew install --cask mactex-no-gui  # macOS
# or
sudo apt-get install texlive-latex-base texlive-latex-extra  # Linux

# Install Python dependencies
pip install flask flask-cors
```

### Backend Setup
```bash
cd backend
python lego_app.py
# Server runs on http://localhost:5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
# App runs on http://localhost:3000
```

## API Endpoints

### 1. Analyze Job
```
POST /api/analyze-job
Body: {
  "jobDescription": "string",
  "jobUrl": "string" (optional)
}
Response: {
  "analysis": {
    "roleType": "Incident Management Specialist",
    "keywords": ["Kubernetes", "Terraform", ...],
    "requiredSkills": [...],
    "company": "Company Name",
    "title": "Job Title"
  }
}
```

### 2. Generate Application
```
POST /api/generate-lego-application
Body: {
  "jobDescription": "string",
  "analysis": {...}
}
Response: {
  "documents": {
    "cvUrl": "/api/download/.../cv.pdf",
    "clUrl": "/api/download/.../cl.pdf"
  }
}
```

### 3. Download/Preview
```
GET /api/download/<folder>/<filename>
GET /api/preview/<folder>/<filename>
```

## LEGO Bricks System

### Profile Bricks
- `incident_management_specialist` - DevOps/SRE focus
- `devops_engineer` - CI/CD and automation focus
- `fullstack_developer` - React/TypeScript focus
- `android_developer` - Mobile development focus

### Skills Bricks
- `incident_management_primary` - Monitoring, RCA, on-call first
- `devops_primary` - CI/CD, IaC, containers first
- `fullstack_primary` - React, APIs, cloud first

### Dynamic Assembly
1. Analyze job description
2. Detect role type (incident management, devops, fullstack, etc.)
3. Select appropriate LEGO bricks
4. Assemble CV with role-specific content
5. Generate professional PDF with blue styling

## Deployment to jobs.bluehawana.com

### Option 1: Vercel (Frontend) + Heroku (Backend)

**Frontend (Vercel):**
```bash
cd frontend
vercel --prod
# Set environment variable: REACT_APP_API_URL=https://your-backend.herokuapp.com
```

**Backend (Heroku):**
```bash
cd backend
heroku create lego-job-generator
heroku buildpacks:add --index 1 https://github.com/Scalingo/apt-buildpack.git
# Add Aptfile with: texlive-latex-base texlive-latex-extra
git push heroku main
```

### Option 2: Single Server (DigitalOcean/AWS)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-latex-extra nginx python3-pip nodejs npm

# Setup backend
cd backend
pip3 install -r requirements.txt
gunicorn lego_app:app --bind 0.0.0.0:5000

# Setup frontend
cd frontend
npm install
npm run build

# Configure nginx to serve frontend and proxy API to backend
```

### Option 3: Docker

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:3000
```

## Usage Flow

1. **User visits jobs.bluehawana.com**
2. **Pastes job URL or description**
3. **Clicks "Analyze Job"**
   - Backend analyzes requirements
   - Detects role type
   - Extracts keywords
4. **Reviews analysis**
   - See role type, keywords, LEGO bricks selected
5. **Clicks "Generate CV & Cover Letter"**
   - Backend assembles LEGO bricks
   - Generates LaTeX
   - Compiles to PDF
6. **Previews documents in browser**
   - CV and CL side-by-side
7. **Provides feedback (optional)**
   - "Make it more technical"
   - "Emphasize leadership"
   - Regenerates with adjustments
8. **Downloads final documents**
   - Ready to apply!

## File Structure

```
.
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── LegoJobGenerator.tsx    # Main React component
│       └── styles/
│           └── LegoJobGenerator.css    # Styling
├── backend/
│   ├── app/
│   │   └── lego_api.py                 # API endpoints
│   ├── lego_app.py                     # Flask app
│   └── generated_applications/         # Output PDFs
├── create_tata_incident_management.py  # Python generator (reference)
└── compile_cleaning_robot_online.py    # Chinese CV generator (reference)
```

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

### Backend (.env)
```
FLASK_ENV=development
GEMINI_API_KEY=your_key_here  # For AI polishing (optional)
```

## Testing

### Test Backend API
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "DevOps Engineer with Kubernetes experience..."}'
```

### Test Frontend
```bash
cd frontend
npm test
```

## Troubleshooting

### PDF Generation Fails
- Ensure pdflatex is installed: `which pdflatex`
- Check LaTeX logs in `generated_applications/*/`
- Verify file permissions

### CORS Errors
- Ensure Flask-CORS is installed
- Check API_URL in frontend .env
- Verify backend is running

### Slow Generation
- PDF compilation takes 2-3 seconds
- Consider caching common templates
- Use loading indicators

## Future Enhancements

- [ ] AI-powered feedback interpretation
- [ ] Multiple language support (Chinese, Swedish)
- [ ] Email delivery integration
- [ ] Application tracking dashboard
- [ ] LinkedIn profile import
- [ ] Resume parsing from existing CV
- [ ] A/B testing different LEGO brick combinations
- [ ] Analytics on application success rates

## Support

For issues or questions:
- GitHub: https://github.com/bluehawana/JobHunter-Python-TypeScript-GmailRestAPI
- Email: hongzhili01@gmail.com

## License

MIT License - See LICENSE file for details

---

**Built with 🧱 LEGO Bricks methodology for maximum ATS optimization and role-specific customization**
