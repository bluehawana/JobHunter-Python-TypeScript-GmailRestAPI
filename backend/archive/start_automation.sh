#!/bin/bash

# JobHunter Automation Startup Script
echo "🚀 Starting JobHunter Automation System..."

# Check if required dependencies are installed
echo "📋 Checking dependencies..."

# Check Redis
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis not found. Please install Redis:"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Check MongoDB
if ! command -v mongod &> /dev/null; then
    echo "❌ MongoDB not found. Please install MongoDB:"
    echo "   macOS: brew install mongodb-community"
    echo "   Ubuntu: sudo apt-get install mongodb"
    exit 1
fi

# Check pdflatex
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found. Please install LaTeX:"
    echo "   macOS: brew install --cask mactex"
    echo "   Ubuntu: sudo apt-get install texlive-full"
    exit 1
fi

echo "✅ All dependencies found"

# Start Redis if not running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "🔴 Starting Redis..."
    redis-server --daemonize yes
    sleep 2
fi

# Start MongoDB if not running
if ! pgrep -x "mongod" > /dev/null; then
    echo "🔴 Starting MongoDB..."
    mongod --fork --logpath /var/log/mongodb.log --dbpath /usr/local/var/mongodb
    sleep 3
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start Celery worker in background
echo "🔄 Starting Celery worker..."
celery -A app.tasks.job_automation_tasks worker --loglevel=info --detach

# Start Celery Beat scheduler in background
echo "⏰ Starting Celery Beat scheduler..."
celery -A app.tasks.job_automation_tasks beat --loglevel=info --detach

# Start FastAPI server
echo "🌐 Starting FastAPI server..."
echo ""
echo "🎯 JobHunter Automation System is now running!"
echo ""
echo "📱 API Documentation: http://localhost:8000/docs"
echo "📊 Automation Status: http://localhost:8000/api/v1/automation/status"
echo "🧪 Test Automation: http://localhost:8000/api/v1/automation/test-run"
echo ""
echo "⏰ Automation Schedule: Weekdays at 06:00 CET"
echo "📧 Applications sent to: leeharvad@gmail.com"
echo ""
echo "🛑 To stop all services, run: ./stop_automation.sh"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload