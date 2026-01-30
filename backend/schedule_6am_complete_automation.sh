#!/bin/bash
"""
Alternative Heroku Scheduler Script - 6 AM Daily Job Hunting
Uses the simple launcher for maximum reliability
"""

echo "🚀 Starting JobHunter Complete Automation at 6 AM..."
echo "📅 Date: $(date)"
echo "🌍 Timezone: $TZ"
echo "🔄 Complete workflow execution with error handling"

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:."

# Change to the correct directory
cd "$(dirname "$0")"

# Run the complete automation launcher
echo "🎯 Executing Complete Automation Launcher..."
python3 run_complete_automation.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Complete Automation finished successfully!"
    echo "📧 Professional applications sent to hongzhili01@gmail.com"
    echo "📊 Execution summary saved with detailed metrics"
else
    echo "❌ Complete Automation failed with exit code $?"
    echo "📋 Check logs for troubleshooting information"
fi

# Show recent log entries if available
if [ -f "automation.log" ]; then
    echo "📋 Recent log entries:"
    tail -10 automation.log
fi

echo "🎯 JobHunter Complete Automation finished at $(date)"