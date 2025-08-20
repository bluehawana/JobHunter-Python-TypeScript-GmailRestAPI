#!/bin/bash
# Daily Job Automation Script for Heroku Scheduler
# Triggers the job automation system

echo "🚀 Starting daily job automation..."
echo "⏰ Time: $(date)"

# Trigger the automation endpoint
curl -X POST https://jobhunter-automation-a305320a98c3.herokuapp.com/trigger/manual-run

echo "✅ Daily job automation triggered"