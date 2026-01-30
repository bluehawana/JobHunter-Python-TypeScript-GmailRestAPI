# 🚀 Zapier/n8n Daily Job Automation Setup

## 📋 Overview
- **6 AM**: Process jobs, generate beautiful PDFs, send applications
- **8 AM**: Send HTML summary email with results
- **Working days only**: Monday-Friday
- **Timezone**: Europe/Stockholm (Swedish time)

## 🔧 API Endpoints

### 1. 6 AM Job Processing
```
POST https://your-heroku-app.herokuapp.com/api/v1/automation/6am-processing
```
**Response:**
```json
{
  "status": "success",
  "message": "Processed 5 jobs, sent 4 applications",
  "data": {
    "jobs_processed": 5,
    "applications_sent": 4,
    "pdfs_generated": 8,
    "successful_companies": ["Volvo Group", "Spotify", "Ericsson"],
    "errors": [],
    "start_time": "2025-01-09T06:00:00",
    "end_time": "2025-01-09T06:15:00"
  }
}
```

### 2. 8 AM Summary Email
```
POST https://your-heroku-app.herokuapp.com/api/v1/automation/8am-summary
```
**Response:**
```json
{
  "status": "success",
  "message": "Summary email sent"
}
```

## 🔄 Zapier Setup

### Step 1: Create Zap for 6 AM Processing
1. **Trigger**: Schedule by Zapier
   - Event: Every Day
   - Time: 06:00
   - Timezone: Europe/Stockholm
   - Filter: Only weekdays (Mon-Fri)

2. **Action**: Webhooks by Zapier
   - Event: POST
   - URL: `https://your-heroku-app.herokuapp.com/api/v1/automation/6am-processing`
   - Method: POST
   - Headers: `Content-Type: application/json`

3. **Action**: Email by Zapier (Success notification)
   - To: hongzhili01@gmail.com
   - Subject: `✅ Job Hunt: {{applications_sent}} Applications Sent`
   - Body: Use webhook response data

### Step 2: Create Zap for 8 AM Summary
1. **Trigger**: Schedule by Zapier
   - Event: Every Day
   - Time: 08:00
   - Timezone: Europe/Stockholm
   - Filter: Only weekdays (Mon-Fri)

2. **Action**: Webhooks by Zapier
   - Event: POST
   - URL: `https://your-heroku-app.herokuapp.com/api/v1/automation/8am-summary`
   - Method: POST

## 🎯 n8n Setup

### Import Workflow
1. Copy the JSON from `automation/n8n_daily_job_automation.json`
2. Import into your n8n instance
3. Update the webhook URLs to your Heroku app
4. Configure email settings for notifications

### Workflow Components
- **6 AM Cron Trigger**: `0 6 * * 1-5` (Mon-Fri at 6 AM)
- **8 AM Cron Trigger**: `0 8 * * 1-5` (Mon-Fri at 8 AM)
- **HTTP Requests**: Call your automation endpoints
- **Conditional Logic**: Handle success/error responses
- **Email Notifications**: Send status updates

## 📧 Email Templates

### 6 AM Success Email
```
Subject: ✅ Job Hunt: {{applications_sent}} Applications Sent

Morning job processing completed successfully!

📊 Results:
• Jobs found: {{jobs_processed}}
• Applications sent: {{applications_sent}}
• PDFs generated: {{pdfs_generated}}

🏢 Companies applied to:
{{successful_companies}}

🎯 Beautiful multi-page PDFs generated
🤖 Claude LEGO intelligence active
📧 Professional applications delivered

Next run: Tomorrow at 6:00 AM
```

### 8 AM Summary Email (HTML)
The system automatically generates a beautiful HTML email with:
- Professional styling and layout
- Statistics dashboard
- Company tags
- System status indicators
- Error reporting (if any)

## 🧪 Testing

### Test Individual Endpoints
```bash
# Test 6 AM processing
curl -X POST https://your-heroku-app.herokuapp.com/api/v1/automation/6am-processing

# Test 8 AM summary
curl -X POST https://your-heroku-app.herokuapp.com/api/v1/automation/8am-summary

# Test complete workflow
curl -X POST https://your-heroku-app.herokuapp.com/api/v1/automation/test-workflow

# Check system status
curl https://your-heroku-app.herokuapp.com/api/v1/automation/status
```

### Test with Python
```bash
cd backend
python zapier_n8n_automation.py 6am    # Test 6 AM processing
python zapier_n8n_automation.py 8am    # Test 8 AM summary
python zapier_n8n_automation.py        # Test full workflow
```

## 🔒 Security

### Webhook Authentication (Optional)
Add authentication headers to your webhooks:
```json
{
  "Authorization": "Bearer your-webhook-token",
  "X-API-Key": "your-api-key"
}
```

## 📊 Monitoring

### Check Automation Status
- **Zapier**: View Zap history and logs
- **n8n**: Check workflow executions
- **Heroku**: Monitor app logs with `heroku logs --tail`

### Expected Daily Flow
```
06:00 → Gmail scan starts
06:05 → Jobs found and analyzed
06:10 → Beautiful PDFs generated
06:15 → Applications sent
06:16 → Success notification sent

08:00 → Summary email generation
08:01 → HTML email sent to hongzhili01@gmail.com
08:02 → Summary confirmation
```

## 🎉 Benefits

✅ **Fully Automated**: No manual intervention needed
✅ **Working Days Only**: Respects your schedule
✅ **Beautiful PDFs**: Multi-page professional resumes
✅ **LEGO Intelligence**: Job-specific tailoring
✅ **Claude Integration**: AI-powered customization
✅ **Professional Emails**: HTML summary reports
✅ **Error Handling**: Automatic notifications if issues occur
✅ **Monitoring**: Full visibility into automation performance

**Your job hunting is now completely automated! 🚀**