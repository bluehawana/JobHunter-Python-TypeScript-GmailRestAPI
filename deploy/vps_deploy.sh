#!/bin/bash
# Run this script ON the VPS server
# Usage: ssh root@jobs.bluehawana.com 'bash -s' < deploy/vps_deploy.sh

set -e

echo "🚀 VPS Deployment with Atomic Restart"
echo "======================================"
echo ""

# Step 1: Pull latest code
echo "Step 1: Pulling latest code from git..."
echo "---------------------------------------"
cd /var/www/lego-job-generator
git pull origin main
echo "✅ Code pulled"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
echo "----------------------------------"
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 3: Atomic restart
echo "Step 3: Atomic restart (all workers reload together)..."
echo "-------------------------------------------------------"

# Stop service completely
echo "🛑 Stopping service..."
sudo systemctl stop lego-job-generator

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
sudo systemctl start lego-job-generator

# Wait for service to be ready
sleep 3

# Check health
if curl -sf http://127.0.0.1:5000/health > /dev/null 2>&1; then
    echo "✅ Service is healthy!"
else
    echo "⚠️  Service may not be fully ready yet"
fi

echo ""
echo "Step 4: Verify deployment..."
echo "----------------------------"
sudo systemctl status lego-job-generator --no-pager | head -15

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "🎯 All workers are now running the same code version"
echo "🌐 Test: http://jobs.bluehawana.com"
