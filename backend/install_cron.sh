#!/bin/bash
# Install cron job for daily job automation

# Add to current user's crontab
(crontab -l 2>/dev/null; echo "00 09 * * * cd /Users/bluehawana/Projects/Jobhunter/backend && /opt/homebrew/opt/python@3.13/bin/python3.13 /Users/bluehawana/Projects/Jobhunter/backend/daily_job_automation.py >> /tmp/jobhunter_automation.log 2>&1") | crontab -
echo "✅ Cron job installed successfully!"
echo "📋 Current crontab:"
crontab -l
