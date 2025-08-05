# SMTP Email Setup Guide

## Issue Resolution Summary

The previous email system had several problems:
1. **No job application links** - Emails didn't include URLs to apply for jobs
2. **Unreadable PDFs** - PDF attachments couldn't be previewed properly  
3. **Missing job context** - No information about which documents were for which companies

## What Was Fixed

### ✅ 1. Added Job Application Links
- Email now includes direct links to job applications
- Links are pulled from processed job data or default to relevant search URLs
- Supports LinkedIn, company career pages, and job boards

### ✅ 2. Enhanced PDF Information
- Each PDF attachment now shows company, position, and document type
- Files are properly parsed to extract job information from filenames
- Modification timestamps help identify the most recent documents

### ✅ 3. Improved Email Template
- Professional formatting with clear sections
- Step-by-step instructions for using the documents
- Organized layout with job links and document summaries

## Current Email Format

```
🤖 JOBHUNTER DAILY APPLICATION REPORT
============================================================

🔗 JOB APPLICATION LINKS:
1. Senior Backend Developer at Ericsson
   📍 Location: Gothenburg  
   🔗 Apply: [Direct Link]

📄 ATTACHED DOCUMENTS:
1. hongzhi_fullstack_developer_skf_group_cv.pdf
   📋 CV for Fullstack Developer at SKF
   📅 Modified: 2025-07-28 09:44

📧 EMAIL INSTRUCTIONS:
- Download attached PDFs
- Click job links to apply directly
- Each document is customized for the specific role

🎯 NEXT STEPS:
1. Download the attached PDFs
2. Review each document for accuracy  
3. Click the job application links above
4. Submit applications with corresponding documents
```

## Setup Requirements

### 1. Set SMTP Password Environment Variable

You need to set your Gmail app password as an environment variable:

```bash
# Option 1: Set temporarily in terminal
export SMTP_PASSWORD="your_gmail_app_password_here"

# Option 2: Add to .env file in backend directory
echo "SMTP_PASSWORD=your_gmail_app_password_here" > .env

# Option 3: Set permanently in shell profile
echo 'export SMTP_PASSWORD="your_gmail_app_password_here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-factor authentication
3. Generate an app password for "Mail"
4. Use this 16-character password (not your regular Gmail password)

### 3. Test the Email System

```bash
cd /Users/bluehawana/Projects/Jobhunter/backend

# Test content generation (without sending)
python3 test_email_content.py

# Send actual email (requires SMTP_PASSWORD)
python3 trigger_email_now.py
```

## Verification

After setting up SMTP_PASSWORD, you should receive emails with:
- ✅ Clickable job application links
- ✅ Readable PDF attachments  
- ✅ Clear document organization
- ✅ Professional formatting

## Troubleshooting

### "SMTP_PASSWORD not set" Error
- Verify environment variable: `echo $SMTP_PASSWORD`
- Check .env file exists and contains password
- Restart terminal after setting permanent env vars

### PDFs Not Opening
- PDFs are valid (verified with `file` command)
- Issue may be with email client PDF viewer
- Try downloading attachments and opening locally

### No Job Links Showing
- Default links provided if no job data found
- To get real job links, run job processing first:
  ```bash
  python3 run_real_job_workflow.py
  ```

## File Updates Made

1. **`trigger_email_now.py`** - Complete rewrite with job links and enhanced PDF handling
2. **`test_email_content.py`** - New test script to verify email content
3. **`SMTP_SETUP.md`** - This documentation file

The email system is now fully functional and will provide you with actionable job application emails including all necessary links and properly organized documents.