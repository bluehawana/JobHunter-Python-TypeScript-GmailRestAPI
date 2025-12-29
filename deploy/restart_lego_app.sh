#!/bin/bash
# Restart LEGO Job Generator application

echo "🔄 Restarting LEGO Job Generator..."
echo ""

# Kill the existing process
echo "1️⃣ Stopping existing process (PID: $(pgrep -f lego_app.py))..."
pkill -f lego_app.py
sleep 2

# Navigate to backend directory
cd /var/www/lego-job-generator/backend

# Activate virtual environment and start the app
echo "2️⃣ Starting application..."
source venv/bin/activate
nohup python3 lego_app.py > /tmp/lego_app.log 2>&1 &

sleep 3

# Check if it's running
NEW_PID=$(pgrep -f lego_app.py)
if [ -n "$NEW_PID" ]; then
    echo "✅ Application started successfully!"
    echo "   PID: $NEW_PID"
    echo "   Port: 5000"
    echo ""
    echo "🌐 Test the application:"
    echo "   http://jobs.bluehawana.com"
    echo ""
    echo "📋 Check logs:"
    echo "   tail -f /tmp/lego_app.log"
else
    echo "❌ Failed to start application"
    echo "Check logs: tail -f /tmp/lego_app.log"
fi
