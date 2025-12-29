#!/bin/bash
# 🚀 Quick Deploy AI Updates to AlphaVPS
# Run this from your local machine

set -e  # Exit on error

VPS_HOST="harvad@94.72.141.71"
VPS_PORT="1025"
VPS_PATH="/var/www/lego-job-generator"

echo "=========================================="
echo "🚀 Deploying AI Updates to AlphaVPS"
echo "=========================================="
echo ""
echo "VPS: $VPS_HOST:$VPS_PORT"
echo "Path: $VPS_PATH"
echo ""

# Check if files exist locally
echo "📋 Checking local files..."
if [ ! -f "backend/ai_analyzer.py" ]; then
    echo "❌ backend/ai_analyzer.py not found!"
    exit 1
fi
if [ ! -f "backend/cv_templates.py" ]; then
    echo "❌ backend/cv_templates.py not found!"
    exit 1
fi
if [ ! -f "backend/app/lego_api.py" ]; then
    echo "❌ backend/app/lego_api.py not found!"
    exit 1
fi
if [ ! -d "backend/minimax_search" ]; then
    echo "❌ backend/minimax_search/ directory not found!"
    exit 1
fi
echo "✅ All files found locally"
echo ""

# Copy files
echo "📦 Copying files to VPS..."

echo "  → backend/ai_analyzer.py"
scp -P $VPS_PORT backend/ai_analyzer.py $VPS_HOST:$VPS_PATH/backend/

echo "  → backend/cv_templates.py"
scp -P $VPS_PORT backend/cv_templates.py $VPS_HOST:$VPS_PATH/backend/

echo "  → backend/app/lego_api.py"
scp -P $VPS_PORT backend/app/lego_api.py $VPS_HOST:$VPS_PATH/backend/app/

echo "  → backend/minimax_search/ (folder)"
scp -P $VPS_PORT -r backend/minimax_search $VPS_HOST:$VPS_PATH/backend/

echo "  → backend/test_vps_ai.py"
scp -P $VPS_PORT backend/test_vps_ai.py $VPS_HOST:$VPS_PATH/backend/

echo "  → .env"
scp -P $VPS_PORT .env $VPS_HOST:$VPS_PATH/

echo "✅ Files copied successfully"
echo ""

# Run commands on VPS
echo "🔧 Installing dependencies on VPS..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
cd /var/www/lego-job-generator
source backend/venv/bin/activate
pip install anthropic
deactivate
echo "✅ Dependencies installed"
ENDSSH

echo ""
echo "🧪 Testing AI on VPS..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
cd /var/www/lego-job-generator
python3 backend/test_vps_ai.py
ENDSSH

echo ""
echo "🔄 Restarting service..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
sudo systemctl restart lego-backend.service
sudo systemctl status lego-backend.service --no-pager
ENDSSH

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your VPS now has AI intelligence! 🎉"
echo ""
echo "Next steps:"
echo "1. Visit your web app"
echo "2. Paste a job description"
echo "3. See AI analysis in action!"
echo ""
