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

### ✨ Application Customization
Each application is personalized using AI-powered customization:
- **Resume Tailoring**: Highlights relevant experience for each role
- **Cover Letter Generation**: Creates role-specific cover letters using LaTeX templates
- **Skills Emphasis**: Adjusts skill presentation based on job requirements
- **Achievement Matching**: Selects most relevant accomplishments
- **Keyword Optimization**: Ensures ATS compatibility

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

## 🚀 Features

- **Automated Job Application Management**: End-to-end automation from job discovery to application submission
- **Gmail Integration**: Seamless email management using Gmail REST API
- **Document Management**: Dynamic PDF generation with LaTeX templates
- **Dashboard Analytics**: Real-time insights into application success rates
- **User Authentication**: Secure OAuth-based login system
- **Multi-platform Job Aggregation**: Comprehensive job discovery across platforms
- **AI-Powered Customization**: Intelligent resume and cover letter tailoring
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
```

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add your credentials to the `.env` file

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

### Backend Deployment
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