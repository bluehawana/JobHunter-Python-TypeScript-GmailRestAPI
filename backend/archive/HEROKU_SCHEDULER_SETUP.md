# 🚀 Heroku Scheduler Setup - Job Automation

## 📋 Entry Point File
**Main file**: `heroku_job_automation.py`
- Runs the complete job hunting automation
- Uses beautiful multi-page PDF generator
- Claude API integration with intelligent fallback
- Scheduled for 20:00 Swedish time (optimal API performance)

## ⚙️ Heroku Scheduler Configuration

### 1. Add Heroku Scheduler Add-on
```bash
heroku addons:create scheduler:standard --app your-app-name
```

### 2. Configure Scheduled Job
```bash
heroku addons:open scheduler --app your-app-name
```

### 3. Add New Job with These Settings:
- **Command**: `python3 heroku_job_automation.py`
- **Schedule**: `0 20 * * *` (8 PM UTC = 20:00 Swedish time)
- **Timezone**: `Europe/Stockholm`

### Alternative: Use Shell Script
- **Command**: `bash schedule_8pm_email_scan.sh`
- **Schedule**: `0 20 * * *`

## 🔧 Environment Variables Required

Make sure these are set in Heroku:
```bash
# Claude API Configuration
ANTHROPIC_AUTH_TOKEN=your_third_party_token
ANTHROPIC_BASE_URL=https://anyrouter.top
CLAUDE_MODEL=claude-3-7-sonnet-20250219
ANTHROPIC_OFFICIAL_API_KEY=your_official_claude_key

# Email Configuration
GMAIL_CREDENTIALS=path/to/credentials.json
GMAIL_APP_PASSWORD=your_gmail_app_password
SENDER_EMAIL=leeharvad@gmail.com
SENDER_GMAIL_PASSWORD=your_password

# Other Configuration
TZ=Europe/Stockholm
```

## 📊 What Happens When It Runs

1. **20:00 Swedish Time**: Heroku Scheduler triggers
2. **Gmail Scan**: Scans for job opportunities (last 3 days)
3. **Claude Analysis**: Analyzes each job for LEGO strategy
4. **PDF Generation**: Creates beautiful multi-page PDFs
5. **Email Delivery**: Sends professional applications
6. **Logging**: Detailed logs for monitoring

## 🎯 Expected Output

```
🚀 HEROKU JOB AUTOMATION STARTED
⏰ Start Time: 2025-01-09 20:00:00 UTC
📧 Scanning Gmail for job opportunities...
🧠 Claude analyzing job requirements for Company X
🎉 BEAUTIFUL MULTI-PAGE PDF: Generated professional resume (7941 bytes)
✅ Email sent for Company X
🎉 HEROKU AUTOMATION COMPLETED!
```

## 📧 Results

You'll receive emails at `hongzhili01@gmail.com` with:
- **Beautiful multi-page CV PDFs** (7000+ bytes)
- **Personalized cover letters** with soft skills focus
- **LEGO-tailored content** based on job requirements
- **Professional formatting** matching your LaTeX template quality

## 🔍 Monitoring

### Check Heroku Logs:
```bash
heroku logs --tail --app your-app-name
```

### Check Scheduler Runs:
```bash
heroku addons:open scheduler --app your-app-name
```

## 🎉 Status: READY FOR PRODUCTION

The system is configured to run automatically every day at 20:00 Swedish time when:
- Chinese users are sleeping (less API load)
- Claude API performance is optimal
- Beautiful multi-page PDFs are generated
- Professional job applications are sent automatically

**NO MORE ONE-PAGE SHIT! 🎯**