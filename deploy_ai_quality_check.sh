#!/bin/bash
# Deploy AI quality check fixes to VPS

set -e

echo "🚀 Deploying AI quality check and cover letter fixes to VPS..."

# VPS details (using SSH alias 'alphavps')
VPS_ALIAS="alphavps"
VPS_PATH="/var/www/lego-job-generator"

echo "📦 Step 1: Pull latest code on VPS..."
ssh ${VPS_ALIAS} << 'ENDSSH'
cd /var/www/lego-job-generator
git pull origin main
echo "✅ Code updated"
ENDSSH

echo "🔄 Step 2: Restart backend service..."
ssh -t ${VPS_ALIAS} "sudo systemctl restart lego-backend.service && echo '✅ Service restarted'"

echo "⏳ Step 3: Wait for service to start..."
sleep 5

echo "🏥 Step 4: Check service status..."
ssh -t ${VPS_ALIAS} "sudo systemctl status lego-backend.service --no-pager -l | head -20"

echo ""
echo "🧪 Step 5: Test API health..."
ssh ${VPS_ALIAS} << 'ENDSSH'
curl -s http://localhost:5000/api/health | python3 -m json.tool || echo "Health check failed"
ENDSSH

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Summary of changes deployed:"
echo "  ✅ Added ai_review_documents() function for quality checks"
echo "  ✅ Fixed cover letter placeholder replacement"
echo "  ✅ Enhanced customize_cover_letter() function"
echo "  ✅ Removed inappropriate generic language"
echo ""
echo "🌐 Test the application at: https://jobs.bluehawana.com"
echo ""
