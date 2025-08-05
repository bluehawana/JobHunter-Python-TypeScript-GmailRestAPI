#!/bin/bash
# Simple script to run the complete job hunting automation

echo "🚀 JobHunter Complete Automation"
echo "=================================="
echo "Starting complete workflow..."
echo ""

# Change to backend directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    echo "📋 Checking dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Run the automation
echo "🎯 Running master automation orchestrator..."
python run_complete_automation.py

echo ""
echo "✅ Automation completed!"
echo "📧 Check your email for job applications"