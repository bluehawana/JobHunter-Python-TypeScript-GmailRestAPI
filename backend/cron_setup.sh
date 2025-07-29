#!/bin/bash

# Set up environment variables for cron
ENV_FILE="/Users/bluehawana/Projects/Jobhunter/backend/.env"
VENV_PATH="/Users/bluehawana/Projects/Jobhunter/backend/venv"
LOG_FILE="/Users/bluehawana/Projects/Jobhunter/backend/automation.log"

# Create cron command with proper environment setup
CRON_CMD="source $ENV_FILE && source $VENV_PATH/bin/activate && cd /Users/bluehawana/Projects/Jobhunter/backend && python3 daily_job_automation.py >> $LOG_FILE 2>&1"

# Install new cron job for 10 AM
(crontab -l 2>/dev/null | grep -v "daily_job_automation.py"; echo "00 10 * * 1-5 $CRON_CMD") | crontab -

echo "✅ Cron job installed for 10 AM on weekdays!"
echo "📋 Current crontab:"
crontab -l