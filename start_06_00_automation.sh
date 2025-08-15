#!/bin/bash
"""
Start 06:00 Job Automation Scheduler
This script starts the scheduler that will run job automation every weekday at 6:00 AM
"""

echo "🎯 Starting 06:00 Job Automation Scheduler"
echo "=========================================="
echo "📅 Schedule: Monday-Friday at 06:00 AM"
echo "📧 Delivery: Applications by 08:00 AM"
echo "=========================================="

# Activate virtual environment
source venv/bin/activate

# Install required packages if missing
pip install schedule > /dev/null 2>&1

# Start the scheduler
echo "⏰ Starting scheduler daemon..."
echo "💡 Press Ctrl+C to stop"
echo ""

python3 daily_06_00_scheduler.py