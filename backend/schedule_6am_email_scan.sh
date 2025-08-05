#!/bin/bash
"""
Heroku Scheduler Script - 6 AM Daily Job Hunting
Runs the Master Automation Orchestrator with complete sequential workflow
"""

echo "🎯 Starting JobHunter Master Automation at 6 AM..."
echo "📅 Date: $(date)"
echo "🌍 Timezone: $TZ"
echo "🔄 Sequential workflow: Gmail scan → Job processing → PDF generation → Email delivery"

# Set environment variables for the script
export PYTHONPATH="${PYTHONPATH}:."

# Run the master automation orchestrator
echo "🚀 Executing Master Automation Orchestrator..."
python3 master_automation_orchestrator.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Master Automation completed successfully!"
    echo "📧 Check hongzhili01@gmail.com for professional PDF applications"
    echo "📊 Check automation summary files for detailed results"
else
    echo "❌ Master Automation failed with exit code $?"
    echo "📋 Check automation.log for detailed error information"
fi

echo "🎯 JobHunter Master Automation execution finished at $(date)"