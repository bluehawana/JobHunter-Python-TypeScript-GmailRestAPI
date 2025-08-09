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