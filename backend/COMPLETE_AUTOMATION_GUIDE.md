# Complete Job Hunting Automation Guide

## 🎯 Overview

This system provides a complete, sequential job hunting automation that executes all steps from a single entry point:

1. **Environment Validation** - Checks dependencies and configuration
2. **Gmail Job Scanning** - Scans your Gmail for job opportunities
3. **Job Data Processing** - Enhances and processes job information
4. **Document Generation** - Creates tailored CV and cover letter PDFs
5. **Application Delivery** - Sends professional applications via email
6. **Results Summary** - Provides detailed execution report

## 🚀 Quick Start

### Local Execution

```bash
# Option 1: Simple shell script
./run_automation.sh

# Option 2: Direct Python execution
python run_complete_automation.py

# Option 3: Master orchestrator directly
python master_automation_orchestrator.py
```

### Heroku Deployment

```bash
# Deploy to Heroku with scheduled automation
./deploy_to_heroku.sh

# Manual trigger via API
curl -X POST https://your-app.herokuapp.com/run-automation

# Check status
curl https://your-app.herokuapp.com/health
```

## 📋 System Architecture

### Master Orchestrator
- **File**: `master_automation_orchestrator.py`
- **Purpose**: Coordinates all automation steps sequentially
- **Features**: 
  - Step-by-step execution logging
  - Error handling and recovery
  - Detailed execution summary
  - Progress tracking

### Entry Points

1. **`run_complete_automation.py`** - Simple launcher
2. **`run_automation.sh`** - Shell script with environment setup
3. **`heroku_app.py`** - Web service with scheduled automation
4. **`master_automation_orchestrator.py`** - Direct orchestrator execution

## 🔧 Configuration

### Environment Variables

```bash
# Required
SENDER_EMAIL=your-email@gmail.com
SENDER_GMAIL_PASSWORD=your-app-password
CLAUDE_API_KEY=your-claude-api-key

# Optional
TARGET_EMAIL=hongzhili01@gmail.com  # Default recipient
DAYS_BACK=3                         # Gmail scan range
```

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `reportlab` - PDF generation
- `supabase` - Database operations
- `anthropic` - Claude API integration
- `fastapi` - Web service (for Heroku)
- `apscheduler` - Task scheduling

## 📊 Execution Flow

### Step 1: Environment Validation
- ✅ Checks required environment variables
- ✅ Validates Python packages
- ✅ Verifies file structure
- ✅ Installs missing dependencies

### Step 2: Gmail Job Scanning
- 📧 Connects to Gmail using app password
- 🔍 Scans last 3 days for job opportunities
- 📝 Extracts job details from emails
- 🏷️ Categorizes and filters relevant jobs

### Step 3: Job Data Processing
- 🏢 Improves company name extraction
- 📋 Enhances job titles and descriptions
- 🔗 Extracts application URLs
- 🎯 Adds processing metadata

### Step 4: Document Generation
- 📄 Generates tailored CV PDFs
- 💌 Creates personalized cover letters
- 🎨 Uses professional formatting
- 📏 Optimizes for ATS systems

### Step 5: Application Delivery
- 📧 Sends professional emails with PDFs
- 🔗 Includes direct application links
- ⏱️ Implements rate limiting
- 📊 Tracks success/failure rates

### Step 6: Results Summary
- 📈 Generates execution report
- 💾 Saves detailed logs
- 📊 Provides success metrics
- 🧹 Performs cleanup tasks

## 📈 Monitoring & Logging

### Execution Logs
- Real-time step-by-step logging
- Error tracking and recovery
- Performance metrics
- Success/failure rates

### Summary Reports
- JSON format execution summaries
- Detailed job processing information
- Email delivery status
- Execution time tracking

### Example Log Output
```
✅ STEP_1: Environment validation completed successfully
✅ STEP_2: Found 5 job opportunities from Gmail scan
✅ STEP_3: Successfully processed 5 jobs
✅ STEP_4: Successfully generated documents for 5 applications
✅ STEP_5: Email sending completed: 4 successful, 1 failed
✅ STEP_6: Summary generation and cleanup completed
```

## 🔄 Scheduling Options

### Heroku Scheduler (Recommended)
- Automatic 6 AM weekday execution
- Stockholm timezone
- Web interface monitoring
- Scalable cloud deployment

### Local Cron Job
```bash
# Add to crontab for 6 AM weekday execution
0 6 * * 1-5 cd /path/to/jobhunter/backend && ./run_automation.sh
```

### Manual Execution
- Run anytime via command line
- Immediate results and feedback
- Perfect for testing and debugging

## 🛠️ Troubleshooting

### Common Issues

1. **Gmail Authentication Failed**
   ```bash
   # Test Gmail connection
   python test_email_auth.py
   ```

2. **Missing Dependencies**
   ```bash
   # Install all requirements
   pip install -r requirements.txt
   ```

3. **PDF Generation Failed**
   ```bash
   # Install reportlab
   pip install reportlab
   ```

4. **Claude API Issues**
   ```bash
   # Test Claude API
   python test_claude_api_direct.py
   ```

### Debug Mode
```bash
# Run with detailed logging
PYTHONPATH=. python -m logging.basicConfig level=DEBUG master_automation_orchestrator.py
```

## 📧 Email Output

Each successful application generates:
- **Professional CV PDF** - Tailored to job requirements
- **Personalized Cover Letter PDF** - Company-specific content
- **Direct Application Link** - Ready-to-click job application URL
- **Job Details Summary** - Complete opportunity information

## 🎉 Success Metrics

The system tracks:
- Jobs found and processed
- Documents generated successfully
- Emails sent successfully
- Overall success rate
- Execution time
- Error recovery rate

## 🔐 Security

- Environment variables for sensitive data
- Gmail app passwords (not main password)
- Secure API key handling
- No credentials in code or logs

## 📞 Support

For issues or questions:
1. Check the execution logs
2. Review the summary JSON files
3. Test individual components
4. Verify environment configuration

## 🚀 Next Steps

After successful automation:
1. Check your email for applications
2. Review the execution summary
3. Monitor success rates
4. Adjust configuration as needed
5. Scale with Heroku for daily automation

---

**Ready to automate your job hunt? Run `./run_automation.sh` and let the system work for you!** 🎯