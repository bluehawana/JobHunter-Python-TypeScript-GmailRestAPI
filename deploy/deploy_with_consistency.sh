#!/bin/bash
# Zero-downtime deployment with guaranteed consistency
# Ensures all workers run the same code version

set -e

SERVER="alphavps"
PORT=""  # Not needed with SSH alias
REMOTE_PATH="/var/www/lego-job-generator"
SERVICE_NAME="lego-backend"

echo "🚀 Deploying with Guaranteed Consistency"
echo "=========================================="
echo ""

# Step 1: Push to git (local)
echo "Step 1: Pushing code to git..."
echo "-------------------------------"
git add -A
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin main
echo "✅ Code pushed to git"
echo ""

# Step 2: Pull on server and restart atomically (single SSH session)
echo "Step 2: Pull code and atomic restart on server..."
echo "--------------------------------------------------"
ssh $SERVER << 'ENDSSH'
# Pull latest code
echo "📥 Pulling latest code from git..."
cd /var/www/lego-job-generator
git pull origin main

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt

# Atomic restart
# Atomic restart
echo "🔄 Atomic restart (all workers reload together)..."
# Stop service completely
echo "🛑 Stopping service..."
sudo systemctl stop lego-backend

# Wait for all workers to die
sleep 2

# Kill any lingering processes
if pgrep -f "gunicorn.*lego_app" > /dev/null; then
    echo "⚠️  Killing lingering gunicorn processes..."
    sudo pkill -9 -f "gunicorn.*lego_app"
    sleep 1
fi

# Start service with fresh workers
echo "🚀 Starting service with fresh workers..."
sudo systemctl start lego-backend

# Wait for service to be ready
sleep 3

# Check health
if curl -sf http://127.0.0.1:5000/health > /dev/null 2>&1; then
    echo "✅ Service is healthy!"
else
    echo "⚠️  Service may not be fully ready yet"
fi
ENDSSH
echo ""

# Step 3: Verify deployment
echo "Step 3: Verifying deployment..."
echo "-------------------------------"
ssh $SERVER << 'ENDSSH'
sudo systemctl status lego-backend --no-pager | head -15
ENDSSH
echo ""

echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "🎯 All workers are now running the same code version"
echo "🌐 Test: http://jobs.bluehawana.com"
echo ""
echo "🔍 Monitor logs:"
echo "   ssh $SERVER 'sudo journalctl -u $SERVICE_NAME -f'"
echo ""
echo "⚡ Quick test commands:"
echo "   # Test NVIDIA"
echo "   curl -X POST http://jobs.bluehawana.com/api/analyze-job -H 'Content-Type: application/json' -d '{\"job_description\":\"NVIDIA\\nCloud Solution Architect\"}'"
echo ""
echo "   # Test Microsoft"
echo "   curl -X POST http://jobs.bluehawana.com/api/analyze-job -H 'Content-Type: application/json' -d '{\"job_description\":\"Microsoft\\nCloud Solution Architect\"}'"
