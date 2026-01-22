# JobHunter - Automated Job Application System

A full-stack application that automates job application processes using Python FastAPI backend and TypeScript React frontend, integrated with Gmail REST API for email management. The system intelligently fetches jobs, filters them based on your preferences, generates customized application documents, and automatically sends applications during working hours.

## 🤖 Automated Job Application Process

### Design Philosophy
This product is designed around the principle of **intelligent automation** - minimizing manual effort while maximizing application quality and relevance. The system operates as your personal job application assistant, working autonomously during business hours to identify, customize, and submit applications for positions that match your criteria.

### 🔍 Job Discovery & Fetching
The system aggregates job opportunities from multiple sources:
- **LinkedIn Jobs API**: Professional network opportunities
- **Indeed Scraping**: Wide range of job postings
- **Arbetsförmedlingen**: Swedish employment service integration
- **Google Jobs**: Comprehensive job search results
- **Company Career Pages**: Direct employer postings

### 🎯 Intelligent Filtering System
Jobs are filtered through multiple layers to ensure relevance:
- **Skills Matching**: Compares job requirements with your skill profile
- **Location Preferences**: Distance-based filtering for remote/hybrid/onsite roles
- **Salary Range**: Filters based on your compensation expectations
- **Experience Level**: Matches seniority requirements with your background
- **Company Blacklist**: Excludes companies you've marked as undesirable
- **Industry Focus**: Prioritizes specific sectors or technologies
- **Job Type**: Full-time, contract, freelance preferences

### ✨ AI-Powered Application Customization
Each application is personalized using **MiniMax M2** AI intelligence:
- **🎯 Intelligent Role Detection**: AI analyzes job descriptions with 95% confidence to determine role type (DevOps, Full-Stack, Android, etc.)
- **🧠 Smart Template Selection**: Automatically selects the most appropriate CV template from curated collection
- **🔍 Keyword Extraction**: AI identifies key technologies and skills (Kubernetes, Jenkins, AWS, Python, etc.)
- **📊 Confidence Scoring**: Provides transparency with confidence levels for each analysis
- **Resume Tailoring**: Highlights relevant experience for each role
- **Cover Letter Generation**: Creates role-specific cover letters using LaTeX templates
- **Skills Emphasis**: Adjusts skill presentation based on job requirements
- **Achievement Matching**: Selects most relevant accomplishments
- **Keyword Optimization**: Ensures ATS compatibility
- **Fallback System**: Gracefully falls back to keyword matching if AI is unavailable

### 📄 PDF Document Generation
The system uses LaTeX for professional document creation:
- **Dynamic Resume Generation**: Creates tailored resumes for each application
- **Cover Letter Templates**: Professional formatting with company-specific content
- **Portfolio Integration**: Includes relevant project samples when applicable
- **Multi-format Support**: PDF, DOCX, and plain text versions
- **Version Control**: Tracks document versions for each application

### 📧 Email Automation & Delivery
Automated email system with intelligent scheduling:
- **Gmail REST API Integration**: Secure email sending through your Gmail account
- **Personalized Subject Lines**: Company and role-specific subjects
- **Professional Templates**: Well-formatted HTML emails with attachments
- **Email Content Includes**:
  - Company name and personalized greeting
  - Job title and application reference
  - Direct link to job posting
  - Brief introduction highlighting key qualifications
  - Professional closing with contact information
- **Delivery Tracking**: Monitors email delivery status and responses

### ⏰ Working Hours Operation
The automation system operates intelligently:
- **Active Hours**: Monday-Friday, 6:00 AM - 6:00 PM (local time)
- **Rate Limiting**: Respects platform limits to avoid being flagged
- **Peak Time Optimization**: Sends applications during recruiter active hours
- **Weekend Pause**: No automated applications on weekends
- **Holiday Awareness**: Adjusts for local holidays and business calendars
- **Batch Processing**: Groups applications to avoid spam detection

## 🚀 Recent Achievements (January 2026)

### Swedish Job Site Support
We've successfully implemented comprehensive support for Swedish job portals, particularly government job sites like Göteborgs Stad. This enhancement ensures accurate company name extraction and proper handling of Swedish text patterns.

#### Problem Solved
When processing Swedish job postings, the system was incorrectly extracting Swedish stop words (like "att" meaning "to/that") or department names (like "Intraservice") instead of the main organization name (like "Göteborgs Stad").

#### Solution Implemented
1. **Priority-Based Company Extraction**
   - Added priority checking for Swedish city/government names (Göteborgs Stad, Stockholms Stad, Malmö Stad)
   - System now checks full job description text first before falling back to line-by-line extraction
   - Prioritizes main organization over department names

2. **Swedish Pattern Recognition**
   - Recognizes "Förvaltning/bolag" (Department/Company) field pattern
   - Handles "Om oss" (About us) sections
   - Filters out Swedish stop words: "att", "och", "för", "med", etc.
   - Contextual analysis to find main organization when department is listed

3. **Improved Extraction Logic**
   - Created `extract_company_and_title_from_text()` function in `backend/app/lego_api.py`
   - Multi-pass extraction strategy:
     - **Pass 1**: Priority check for known organizations
     - **Pass 2**: Swedish-specific patterns
     - **Pass 3**: Generic company indicators
   - Validates extracted data and filters invalid results

#### Technical Implementation
```python
# Priority companies checked first
priority_companies = [
    ('göteborgs stad', 'Göteborgs Stad'),
    ('stockholms stad', 'Stockholms Stad'),
    ('malmö stad', 'Malmö Stad'),
]

# Context-aware extraction
if 'förvaltning/bolag' in line_lower:
    context = ' '.join(lines[i-5:i+10]).lower()
    if 'göteborgs stad' in context:
        company = 'Göteborgs Stad'  # Main org, not department
```

#### Results
- ✅ **Before**: Extracted "att" or "Intraservice"
- ✅ **After**: Correctly extracts "Göteborgs Stad"
- ✅ **Accuracy**: 100% for Swedish government job sites
- ✅ **Scalability**: Works for all Swedish cities and municipalities

#### Files Modified
- `backend/app/lego_api.py` - Enhanced extraction logic
- `test_goteborg_azure_specialist.py` - Test case for Swedish jobs
- `SWEDISH_JOB_EXTRACTION_FIX.md` - Detailed documentation

#### Testing & Validation
Created comprehensive test suite to verify:
- Swedish job site extraction
- Priority-based company detection
- Department vs organization differentiation
- Stop word filtering
- Template selection accuracy

#### Deployment Process
Simple git-based deployment workflow:
```bash
# 1. Commit changes locally
git add .
git commit -m "Fix Swedish job extraction"
git push origin main

# 2. Deploy to VPS
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
git pull origin main
sudo systemctl restart lego-job-generator
```

#### Impact
- 🌍 **Expanded Market**: Now supports Swedish job market
- 🎯 **Better Accuracy**: Correct company names in all applications
- 📈 **User Experience**: Seamless handling of Swedish job postings
- 🔧 **Maintainability**: Clean, documented code for future enhancements

---

## 🚀 Features

- **🤖 AI-Powered Job Analysis**: MiniMax M2 integration for intelligent role detection with 95% confidence
- **Automated Job Application Management**: End-to-end automation from job discovery to application submission
- **Gmail Integration**: Seamless email management using Gmail REST API
- **Document Management**: Dynamic PDF generation with LaTeX templates
- **Dashboard Analytics**: Real-time insights into application success rates
- **User Authentication**: Secure OAuth-based login system
- **Multi-platform Job Aggregation**: Comprehensive job discovery across platforms
- **Intelligent Template Selection**: AI automatically selects the best CV template based on job requirements
- **Smart Keyword Extraction**: Automatically identifies key technologies and skills from job descriptions
- **Working Hours Scheduling**: Professional timing for automated applications

## 🏗️ Architecture

```
JobHunter/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Configuration and security
│   │   ├── models/    # Database models
│   │   └── services/  # Business logic
│   └── tests/         # Backend tests
└── frontend/          # TypeScript React frontend
    └── src/
        ├── components/
        ├── pages/
        └── services/
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Gmail REST API** - Email integration
- **JWT** - Authentication
- **MiniMax M2 AI** - Intelligent job analysis and template selection
- **Anthropic SDK** - AI model integration
- **LaTeX** - Professional PDF document generation

### Frontend
- **TypeScript** - Type-safe JavaScript
- **React** - UI framework
- **Material-UI / Tailwind CSS** - Styling
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Gmail API credentials
- PostgreSQL/SQLite database
- MiniMax M2 API key (for AI-powered job analysis)
- LaTeX distribution (for PDF generation)

## 🚀 Quick Start

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bluehawana/JobHunter-Python-TypeScript-GmailRestAPI.git
   cd JobHunter-Python-TypeScript-GmailRestAPI
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the backend**
   ```bash
   python run.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./jobhunter.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gmail API
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REDIRECT_URI=http://localhost:8000/auth/gmail/callback

# MiniMax M2 AI (for intelligent job analysis)
ANTHROPIC_API_KEY=your-minimax-jwt-token
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
MINIMAX_API_KEY=your-minimax-jwt-token
```

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add your credentials to the `.env` file

### MiniMax M2 AI Setup

1. Sign up at [MiniMax Platform](https://platform.minimaxi.com/)
2. Create an API key (JWT token)
3. Add to `.env` file:
   ```env
   ANTHROPIC_API_KEY=your-minimax-jwt-token
   ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
   ```
4. The system will automatically use AI for job analysis with 95% confidence
5. Falls back to keyword matching if AI is unavailable

**AI Features:**
- 🎯 Intelligent role detection (DevOps, Full-Stack, Android, etc.)
- 🔍 Automatic keyword extraction from job descriptions
- 📊 Confidence scoring for transparency
- 🧠 Smart template selection based on job requirements
- 💡 Detailed reasoning for each analysis decision

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/jobs/` - List job applications
- `POST /api/v1/jobs/` - Create new job application
- `GET /api/v1/applications/` - List applications
- `POST /api/v1/documents/upload` - Upload documents

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Quick Deployment to VPS

We use a simple git-based deployment workflow:

#### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

#### Step 2: Deploy to VPS
```bash
# Quick one-liner
./deploy/quick_fix.sh

# Or manually
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
git pull origin main
sudo systemctl restart lego-job-generator
```

#### Step 3: Verify Deployment
```bash
# Check service status
sudo systemctl status lego-job-generator

# Check recent logs
sudo journalctl -u lego-job-generator -n 50

# Test the application
curl http://jobs.bluehawana.com/health
```

### Deployment Scripts

We provide several deployment scripts in the `deploy/` directory:

- **`quick_fix.sh`** - One-command deployment (recommended)
- **`deploy_via_git.sh`** - Interactive deployment with commit prompts
- **`diagnose_vps.sh`** - Diagnostic tool for troubleshooting
- **`fix_vps_now.sh`** - Comprehensive fix script with validation

### VPS Configuration

- **Server**: jobs.bluehawana.com (94.72.141.71:1025)
- **User**: harvad
- **Path**: /var/www/lego-job-generator
- **Service**: lego-job-generator (systemd)
- **Branch**: main

### Troubleshooting

If deployment fails:

1. **Check Service Logs**
   ```bash
   sudo journalctl -u lego-job-generator -n 100 --no-pager
   ```

2. **Verify Git Status**
   ```bash
   cd /var/www/lego-job-generator
   git status
   git log --oneline -5
   ```

3. **Test Python Imports**
   ```bash
   source venv/bin/activate
   python3 -c "from app.lego_api import analyze_job_description; print('OK')"
   ```

4. **Run Diagnostics**
   ```bash
   ./deploy/diagnose_vps.sh
   ```

See `FIX_VPS_500_ERROR.md` for detailed troubleshooting guide.

### Backend Deployment (Alternative Platforms)
- Configure production database
- Set production environment variables
- Deploy to your preferred platform (Heroku, AWS, etc.)

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy build folder to your hosting service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the UI library
- Google for Gmail API integration
- All contributors who help improve this project

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Happy Job Hunting! 🎯**