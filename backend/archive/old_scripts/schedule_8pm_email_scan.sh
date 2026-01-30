#!/bin/bash
"""
Heroku Scheduler Script - 20:00 (8 PM) Daily Job Hunting
Runs the Master Automation Orchestrator with complete sequential workflow
Optimal time for Claude API (Chinese users sleeping, less API load)
"""

echo "🎯 Starting JobHunter Master Automation at 20:00 (8 PM Swedish time)..."
echo "📅 Date: $(date)"
echo "🌍 Timezone: $TZ"
echo "🔄 Sequential workflow: Gmail scan → Claude LEGO analysis → PDF generation → Email delivery"
echo "🧠 Claude API optimization: Running at night when Chinese users are sleeping"

# Set environment variables for the script
export PYTHONPATH="${PYTHONPATH}:."

# Run the master automation orchestrator
echo "🚀 Executing Heroku Job Automation with Beautiful PDFs..."
python3 heroku_job_automation.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Heroku Job Automation completed successfully!"
    echo "📧 Check hongzhili01@gmail.com for beautiful multi-page PDF applications"
    echo "🎯 LEGO intelligence with Claude API integration working"
    echo "📊 Beautiful PDFs generated - NO MORE ONE-PAGE SHIT!"
else
    echo "❌ Heroku Job Automation failed with exit code $?"
    echo "📋 Check logs for detailed error information"
fi

echo "🎯 JobHunter Heroku Automation execution finished at $(date)"