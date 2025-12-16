# Job Application Automation - Mock Test Guide

## 🎯 Overview

This mock test demonstrates the complete job application automation workflow:

1. **Email Scanning**: Scan `bluehawana@gmail.com` for LinkedIn job emails
2. **Job Extraction**: Find newest job spots with title "LinkedIn Jobs"
3. **Document Generation**: Create customized resume and cover letter in LaTeX format
4. **PDF Conversion**: Generate PDF files for both documents
5. **Email Delivery**: Send to `leeharvad@gmail.com` with job details and attachments

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**: Python 3.8+ installed
2. **Dependencies**: Install required packages
3. **Email Configuration**: Set up Gmail app password
4. **LaTeX**: Install LaTeX distribution for PDF generation

### Setup Instructions

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables** in `.env`:
   ```env
   # Email configuration
   SMTP_USER=bluehawana@gmail.com
   SMTP_PASSWORD=your-gmail-app-password
   EMAILS_FROM_EMAIL=bluehawana@gmail.com
   EMAILS_FROM_NAME=JobHunter Bot
   ```

4. **Run the mock test**:
   ```bash
   python run_mock_test.py
   ```

## 📧 What the Mock Test Does

### Step 1: Email Scanning Simulation
- Simulates scanning `bluehawana@gmail.com` for job emails
- Looks for emails with "LinkedIn Jobs" in the title
- Extracts job details from email content

### Step 2: Job Processing
For each job found, the system:
- Extracts job title, company, location, and description
- Identifies relevant keywords and requirements
- Analyzes job requirements for customization

### Step 3: Document Customization
- **Resume (CV)**: Customizes based on job requirements
  - Highlights relevant skills and experience
  - Emphasizes matching keywords
  - Tailors professional summary
  
- **Cover Letter**: Generates personalized content
  - Addresses specific company and role
  - Mentions relevant experience
  - Includes job-specific motivation

### Step 4: PDF Generation
- Converts LaTeX documents to professional PDFs
- Ensures ATS-friendly formatting
- Optimizes for readability and parsing

### Step 5: Email Delivery
Sends email to `leeharvad@gmail.com` containing:
- **Subject**: "Job Application Ready: [Job Title] at [Company]"
- **Attachments**: 
  - `CV_[Company]_[JobTitle].pdf`
  - `CoverLetter_[Company]_[JobTitle].pdf`
- **Content**:
  - Job details (title, company, location)
  - Application link
  - Job description excerpt
  - Extracted keywords
  - Document generation status

## 📋 Sample Jobs in Mock Test

The mock test processes these sample jobs:

### Job 1: Senior Fullstack Developer at TechCorp Sweden
- **Location**: Stockholm, Sweden
- **Keywords**: Java, Spring Boot, React, TypeScript, AWS, Microservices
- **Type**: Full-time with remote options
- **URL**: LinkedIn job posting link

### Job 2: Backend Developer at Growing Startup
- **Location**: Gothenburg, Sweden  
- **Keywords**: Java, Spring Boot, AWS, PostgreSQL, Docker, Kubernetes
- **Type**: Full-time, on-site
- **URL**: LinkedIn job posting link

## 📤 Expected Email Output

After running the mock test, `leeharvad@gmail.com` will receive emails like:

```
Subject: Job Application Ready: Senior Fullstack Developer at TechCorp Sweden

Dear Lee,

I've processed a new job opportunity and generated customized application documents:

📋 JOB DETAILS:
• Position: Senior Fullstack Developer
• Company: TechCorp Sweden
• Location: Stockholm, Sweden
• Source: linkedin_email
• Job Type: fulltime
• Remote Option: Yes

🔗 APPLICATION LINK:
https://www.linkedin.com/jobs/view/3756789123

📝 JOB DESCRIPTION:
We are seeking a Senior Fullstack Developer to join our innovative team...

🎯 EXTRACTED KEYWORDS:
java, spring boot, react, typescript, aws, azure, microservices, docker

📎 ATTACHMENTS:
- Customized CV (PDF)
- Customized Cover Letter (PDF)

The documents have been tailored specifically for this position based on the job requirements and keywords.

Best regards,
JobHunter Automation System
```

## 🔧 Customization Features

### Resume Customization
- **Skills Highlighting**: Emphasizes relevant technical skills
- **Experience Tailoring**: Highlights matching work experience
- **Keyword Optimization**: Includes job-specific keywords for ATS
- **Professional Summary**: Customized based on job requirements

### Cover Letter Personalization
- **Company Research**: References specific company information
- **Role Alignment**: Explains fit for the specific position
- **Motivation**: Expresses genuine interest in the opportunity
- **Call to Action**: Professional closing with next steps

## 📊 Mock Test Output

The test provides detailed output showing:

```
🚀 Starting Job Application Automation Mock Test
============================================================
📧 Step 1: Initializing Email Scanner and Job Processor...
🔍 Step 2: Scanning bluehawana@gmail.com for LinkedIn job emails...
   ✅ Found 2 job opportunities from LinkedIn emails
📄 Step 3: Processing jobs and generating customized documents...

   Processing Job 1/2: Senior Fullstack Developer at TechCorp Sweden
   📝 Generating customized CV...
   📝 Generating customized cover letter...
   ✅ Documents generated successfully
   📧 Sending application email to leeharvad@gmail.com...
   ✅ Email sent successfully!

============================================================
📊 WORKFLOW SUMMARY
============================================================
📧 Emails scanned: bluehawana@gmail.com
🔍 Jobs found: 2
✅ Successfully processed: 2
❌ Failed to process: 0
📤 Emails sent to leeharvad@gmail.com: 2
```

## 🎯 Next Steps After Mock Test

1. **Check Email**: Look for emails in `leeharvad@gmail.com`
2. **Review Documents**: Open and review the PDF attachments
3. **Evaluate Quality**: Assess document customization quality
4. **Apply to Jobs**: Use the provided links to apply
5. **Track Applications**: Monitor application status

## 🛠️ Troubleshooting

### Common Issues

1. **Email Authentication Error**:
   - Ensure Gmail app password is correctly set
   - Check SMTP configuration in `.env`

2. **LaTeX Compilation Error**:
   - Install LaTeX distribution (TeX Live, MiKTeX)
   - Check LaTeX template syntax

3. **PDF Generation Failed**:
   - Verify LaTeX installation
   - Check file permissions in temp directory

4. **No Jobs Found**:
   - Check email scanning configuration
   - Verify IMAP connection settings

### Debug Mode

Run with debug logging:
```bash
PYTHONPATH=. python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from mock_test_complete_workflow import mock_test_complete_workflow
import asyncio
asyncio.run(mock_test_complete_workflow())
"
```

## 📈 Production Deployment

To deploy this system for daily automation:

1. **Schedule Daily Runs**: Use cron or task scheduler
2. **Database Integration**: Store job applications and status
3. **Error Handling**: Implement robust error recovery
4. **Monitoring**: Add logging and alerting
5. **Rate Limiting**: Respect email provider limits

## 🔒 Security Considerations

- **Email Credentials**: Use app passwords, not main password
- **API Keys**: Store securely in environment variables
- **Data Privacy**: Handle personal information responsibly
- **Rate Limits**: Respect service provider limits

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review log output for specific errors
3. Verify all prerequisites are installed
4. Test individual components separately

---

**Happy Job Hunting! 🎉**