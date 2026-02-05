#!/bin/bash
# Deploy the latest fixes to VPS - lego-job-generator

echo "🚀 Deploying Kamstrup fixes to VPS..."

# 1. Navigate to the correct project directory
cd /var/www/lego-job-generator

# 2. Pull latest changes from git
echo "📥 Pulling latest changes..."
git pull origin main

# 3. Check if there are any new Python dependencies
echo "📦 Checking Python dependencies..."
pip3 install -r backend/requirements.txt

# 4. Restart the backend service (adjust service name as needed)
echo "🔄 Restarting backend service..."

# Option A: If using systemd service
if systemctl is-active --quiet lego-app; then
    echo "Restarting lego-app systemd service..."
    sudo systemctl restart lego-app
    sudo systemctl status lego-app
elif systemctl is-active --quiet lego-job-generator; then
    echo "Restarting lego-job-generator systemd service..."
    sudo systemctl restart lego-job-generator
    sudo systemctl status lego-job-generator
# Option B: If using PM2
elif command -v pm2 &> /dev/null; then
    echo "Restarting PM2 processes..."
    pm2 restart all
    pm2 status
# Option C: If using screen/tmux sessions
else
    echo "⚠️ Please manually restart your backend process"
    echo "Common commands:"
    echo "  - Kill existing: pkill -f 'python.*lego_api'"
    echo "  - Start new: cd backend && python3 app/lego_api.py &"
fi

# 5. Check if frontend needs restart (if applicable)
if [ -d "frontend" ]; then
    echo "🌐 Checking frontend..."
    if command -v pm2 &> /dev/null && pm2 list | grep -q frontend; then
        echo "Restarting frontend..."
        pm2 restart frontend
    fi
fi

echo "✅ Deployment complete!"
echo ""
echo "🧪 Test the fixes:"
echo "1. Go to https://jobs.bluehawana.com"
echo "2. Copy-paste the Kamstrup job description (don't use LinkedIn URL)"
echo "3. Check that it shows:"
echo "   - Role: Customer Support Engineer"
echo "   - Company: Kamstrup"
echo "   - Generates CV/CL successfully"