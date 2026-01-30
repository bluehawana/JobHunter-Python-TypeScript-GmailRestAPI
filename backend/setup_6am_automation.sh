#!/bin/bash
# Setup 6 AM daily automation for JobHunter

# Remove old cron job
crontab -l | grep -v "daily_job_automation" | crontab -

# Add new 6 AM cron job with fixed script
(crontab -l 2>/dev/null; echo "00 06 * * 1-5 cd /Users/bluehawana/Projects/Jobhunter/backend && python3 daily_job_automation_with_env.py >> /Users/bluehawana/Projects/Jobhunter/backend/automation_6am.log 2>&1") | crontab -

echo "✅ 6 AM automation scheduled!"
echo "📅 Will run Monday-Friday at 6:00 AM Stockholm time"
echo "📧 Will send job opportunities to hongzhili01@gmail.com"
echo "📄 Will use proper LaTeX PDF generation"
echo "📋 Logs will be saved to automation_6am.log"

# Show current cron jobs
echo ""
echo "Current cron jobs:"
crontab -l