#!/bin/bash
# Schedule email scanning at 6am daily
# For Heroku Scheduler: Add this command to run at 06:00 UTC daily
# Command: bash schedule_6am_email_scan.sh

echo "Starting 6am email job scan at $(date)"

# Run the email scanner
python app/scheduler/job_runner.py scan_emails

echo "6am email job scan completed at $(date)"