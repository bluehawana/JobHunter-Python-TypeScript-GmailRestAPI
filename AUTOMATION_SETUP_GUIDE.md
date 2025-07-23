# 🤖 JobHunter Automation System - Complete Setup Guide

## 🎯 Overview

Your JobHunter application now has a **fully automated job application system** that:
- **Triggers every weekday at 6:00 AM** (Monday-Friday)
- **Fetches jobs** from LinkedIn, Arbetsförmedlingen, and Gmail within 2 weeks
- **Filters jobs** for ≤5 years experience, B2 Swedish level, and your tech skills
- **Generates customized CV & Cover Letters** using your LaTeX templates
- **Emails applications** to leeharvad@gmail.com with attachments and job links

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Install Redis (for Celery task queue)
brew install redis                # macOS
sudo apt-get install redis-server # Ubuntu

# Install MongoDB (for job storage)
brew install mongodb-community    # macOS
sudo apt-get install mongodb      # Ubuntu

# Install LaTeX (for PDF generation)
brew install --cask mactex        # macOS
sudo apt-get install texlive-full # Ubuntu
```

### 2. Setup Email Authentication
1. **Enable 2-Factor Authentication** on hongzhili01@gmail.com
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "JobHunter"
3. **Update environment file**:
   ```bash
   # Edit backend/.env
   SMTP_PASSWORD=your-generated-app-password-here
   ```

### 3. Start the System
```bash
cd backend
./start_automation.sh
```

## 📋 System Architecture

```
JobHunter Automation System
├── 🕕 Scheduler (Celery Beat)
│   └── Triggers at 6:00 AM weekdays
│
├── 🔄 Worker (Celery Worker)
│   ├── Job Fetching Service
│   ├── LaTeX Resume Service
│   └── Email Automation Service
│
├── 🎯 Job Sources
│   ├── LinkedIn API (with your credentials)
│   ├── Arbetsförmedlingen API
│   └── Gmail Job Extraction
│
├── 🧠 Smart Filtering
│   ├── Experience Level (≤5 years)
│   ├── Swedish Language (≤B2)
│   ├── Skills Matching
│   └── Job Quality Checks
│
└── 📧 Email Delivery
    ├── Customized CV (PDF)
    ├── Customized Cover Letter (PDF)
    └── Application Email to leeharvad@gmail.com
```

## 🛠️ API Endpoints

### Automation Management
- `GET /api/v1/automation/status` - System status and stats
- `POST /api/v1/automation/configure` - Configure settings
- `POST /api/v1/automation/test-run` - Manual test run
- `POST /api/v1/automation/test-email` - Test email functionality
- `POST /api/v1/automation/pause` - Pause automation
- `POST /api/v1/automation/resume` - Resume automation

### Statistics & Monitoring
- `GET /api/v1/automation/stats` - Detailed statistics
- `GET /api/v1/automation/processed-jobs` - View processed jobs
- `GET /api/v1/automation/logs` - System logs

## 🎯 Intelligent Filtering System

### 1. **Experience Level Filter**
- ✅ Accepts jobs requiring ≤5 years experience
- ❌ Filters out "Senior", "Lead", "Principal" roles (except Architect)
- 🔍 Analyzes job titles and descriptions for experience keywords

### 2. **Swedish Language Filter**
- ✅ Accepts jobs requiring ≤B2 Swedish level
- ❌ Filters out jobs requiring "flytande svenska", "modersmål", C1/C2
- 🔍 Uses regex patterns to detect language requirements

### 3. **Skills Matching Filter**
```python
Your Skills = [
    # Programming: Java, JavaScript, C#, Python, TypeScript
    # Frontend: React, Angular, Vue, HTML, CSS
    # Backend: Spring Boot, Node.js, .NET Core
    # Cloud: AWS, Azure, GCP, Docker, Kubernetes
    # Databases: SQL, PostgreSQL, MySQL, MongoDB
    # DevOps: CI/CD, Jenkins, Terraform, Grafana
    # Roles: Fullstack, Backend, Cloud Developer, DevOps
]
```
- ✅ Requires at least 2 matching skills
- 🎯 Prioritizes jobs with more skill matches

### 4. **Job Quality Filter**
- ✅ Must have title, company, description (≥50 chars), and URL
- ❌ Filters out spam keywords
- 📅 Only jobs posted within 2 weeks

## 📄 LaTeX Document Generation

### CV Customization
- **Dynamic Job Role**: Adapts header based on job (Fullstack Developer, DevOps Engineer, etc.)
- **Tailored Profile**: Customizes summary to highlight relevant technologies
- **Relevant Skills**: Reorders skills based on job requirements
- **Company-Specific**: Filename includes company and position

### Cover Letter Personalization
- **Job-Specific Content**: References specific role and company
- **Technology Alignment**: Mentions technologies from job description
- **Experience Matching**: Tailors experience narrative to job type
- **Professional Formatting**: Uses your provided LaTeX template

## 📧 Email Automation

### Email Features
- **HTML Formatted**: Professional appearance with job details
- **Attachments**: Customized CV and Cover Letter PDFs
- **Job Information**: Includes application link, location, source
- **Automation Details**: Shows how job was discovered and processed

### Email Content
```
Subject: Application: [Job Title] at [Company Name]

- Job details and application link
- Your contact information
- Attached customized CV and cover letter
- Automation system information
```

## ⏰ Scheduling Details

### Timing
- **Weekdays Only**: Monday through Friday
- **6:00 AM CET**: Swedish timezone
- **No Weekends**: System respects work-life balance

### Process Flow
1. **06:00** - Job fetching begins
2. **06:05** - Filtering and processing
3. **06:15** - CV/Cover letter generation
4. **06:30** - Email sending
5. **08:00** - Daily summary email

## 🔧 Configuration Options

### Automation Settings
```json
{
  "enabled": true,
  "email_notifications": true,
  "max_applications_per_day": 10,
  "target_email": "leeharvad@gmail.com"
}
```

### Job Search Queries
- "fullstack developer"
- "backend developer"
- "java developer"
- "c# developer"
- "cloud developer"
- "cloud architect"
- "devops engineer"
- "platform architect"
- "integration specialist"
- "software engineer"

### Search Locations
- Stockholm, Göteborg, Malmö, Uppsala, Linköping, Örebro, Sweden

## 📊 Monitoring & Analytics

### Daily Statistics
- Jobs fetched from all sources
- Jobs after filtering
- Applications sent
- Success/failure rates

### Weekly Reports
- Companies applied to
- Application trends
- Source effectiveness
- Filter performance

## 🚨 Error Handling

### Automatic Recovery
- **API Failures**: Continues with available sources
- **Email Failures**: Retries with exponential backoff
- **PDF Generation**: Falls back to default templates
- **Database Issues**: Logs errors and continues

### Notifications
- Daily summary emails
- Error notifications
- System status updates

## 🧪 Testing

### Manual Testing
```bash
# Test job fetching
curl -X POST "http://localhost:8000/api/v1/automation/test-run"

# Test email functionality
curl -X POST "http://localhost:8000/api/v1/automation/test-email"

# Check system status
curl -X GET "http://localhost:8000/api/v1/automation/status"
```

### Integration Testing
```bash
# Test job integration
curl -X GET "http://localhost:8000/api/v1/jobs/test/integration"
```

## 📁 File Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── job_automation_service.py    # Main automation logic
│   │   ├── latex_resume_service.py      # CV/Cover letter generation
│   │   └── email_automation_service.py  # Email sending
│   ├── tasks/
│   │   └── job_automation_tasks.py      # Celery tasks
│   └── api/v1/endpoints/
│       └── automation.py                # API endpoints
├── start_automation.sh                  # Startup script
├── stop_automation.sh                   # Stop script
└── requirements.txt                     # Dependencies
```

## 🛠️ Troubleshooting

### Common Issues

**1. LaTeX compilation fails**
```bash
# Check if pdflatex is installed
which pdflatex

# Install LaTeX distribution
brew install --cask mactex  # macOS
```

**2. Email authentication fails**
```bash
# Check app password in .env file
grep SMTP_PASSWORD backend/.env

# Verify Gmail app password is generated correctly
```

**3. Redis connection fails**
```bash
# Start Redis server
redis-server --daemonize yes

# Check if running
ps aux | grep redis
```

**4. MongoDB connection fails**
```bash
# Start MongoDB
brew services start mongodb-community  # macOS

# Check if running
ps aux | grep mongod
```

### Debug Mode
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
./start_automation.sh
```

## 🔐 Security Features

- **Environment Variables**: All sensitive data in .env
- **OAuth 2.0**: Secure Gmail integration
- **Input Validation**: All job data sanitized
- **Rate Limiting**: API call throttling
- **Secure Email**: TLS encryption for SMTP

## 📈 Performance Optimization

- **Parallel Processing**: All job sources queried simultaneously
- **Database Indexing**: Optimized queries for processed jobs
- **Caching**: Redis-based caching for API responses
- **Background Processing**: Celery for non-blocking operations

## 🎯 Success Metrics

Based on typical job search automation:
- **Expected Applications**: 5-15 per day
- **Filter Efficiency**: ~80% jobs filtered out
- **Email Success Rate**: >95%
- **PDF Generation**: >99% success rate

## 📞 Support & Maintenance

### Daily Monitoring
- Check automation logs: `GET /api/v1/automation/logs`
- Review daily statistics: `GET /api/v1/automation/stats`
- Monitor email delivery success

### Weekly Maintenance
- Review processed jobs: `GET /api/v1/automation/processed-jobs`
- Update job search queries if needed
- Clean up old automation runs (automatic)

---

## 🎉 System Ready!

Your JobHunter automation system is now **fully configured** and ready to:

✅ **Automatically fetch jobs** every weekday morning  
✅ **Filter for your requirements** (experience, Swedish, skills)  
✅ **Generate customized applications** using your LaTeX templates  
✅ **Email applications** to leeharvad@gmail.com with attachments  
✅ **Provide detailed statistics** and monitoring  

**Start the system**: `./start_automation.sh`  
**Monitor status**: http://localhost:8000/api/v1/automation/status  
**Test run**: http://localhost:8000/api/v1/automation/test-run  

The system will handle everything automatically - just check your leeharvad@gmail.com inbox for job applications!