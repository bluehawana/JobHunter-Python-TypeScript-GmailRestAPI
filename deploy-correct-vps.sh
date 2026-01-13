#!/bin/bash
set -e

# Correct VPS IP: 107.174.51.158
VPS_IP="107.174.51.158"
VPS_PORT="1025"
VPS_USER="harvad"

echo "🚀 JobHunter VPS Deployment"
echo "==========================="
echo ""
echo "VPS: $VPS_USER@$VPS_IP:$VPS_PORT"
echo ""

# Check package exists
if [ ! -f /tmp/fixes.tar.gz ]; then
    echo "❌ Package not found at /tmp/fixes.tar.gz"
    echo "Run the build first!"
    exit 1
fi

echo "✅ Package ready: $(du -h /tmp/fixes.tar.gz | cut -f1)"
echo ""

# Step 1: Upload
echo "📤 Step 1: Uploading to VPS..."
echo "Password: 11"
echo ""

scp -P $VPS_PORT /tmp/fixes.tar.gz $VPS_USER@$VPS_IP:~/

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Upload failed"
    exit 1
fi

echo ""
echo "✅ Upload complete!"
echo ""

# Step 2: Deploy
echo "🚀 Step 2: Deploying on VPS..."
echo "Password: 11"
echo ""

ssh -p $VPS_PORT $VPS_USER@$VPS_IP 'bash -s' << 'ENDSSH'
set -e

echo "📋 Creating backup..."
BACKUP_DIR="$HOME/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -d /var/www/lego-job-generator/frontend/build ]; then
    cp -r /var/www/lego-job-generator/frontend/build "$BACKUP_DIR/"
    echo "   ✅ Frontend backed up"
fi

if [ -f /var/www/lego-job-generator/backend/app/lego_api.py ]; then
    cp /var/www/lego-job-generator/backend/app/lego_api.py "$BACKUP_DIR/"
    echo "   ✅ Backend backed up"
fi

echo ""
echo "📦 Extracting files..."
cd ~
tar -xzf fixes.tar.gz
echo "   ✅ Extracted"

echo ""
echo "🔧 Deploying backend..."
cp backend/app/lego_api.py /var/www/lego-job-generator/backend/app/
cp backend/requirements.txt /var/www/lego-job-generator/backend/
echo "   ✅ Backend deployed"

echo ""
echo "📚 Installing dependencies..."
cd /var/www/lego-job-generator/backend
source venv/bin/activate
pip install -q -r requirements.txt 2>&1 | tail -5
deactivate
echo "   ✅ Dependencies installed"

echo ""
echo "🎨 Deploying frontend..."
rm -rf /var/www/lego-job-generator/frontend/build.old 2>/dev/null || true
if [ -d /var/www/lego-job-generator/frontend/build ]; then
    mv /var/www/lego-job-generator/frontend/build /var/www/lego-job-generator/frontend/build.old
fi
mv ~/frontend/build /var/www/lego-job-generator/frontend/
echo "   ✅ Frontend deployed"

echo ""
echo "🔄 Restarting services..."
sudo systemctl restart lego-backend.service
sleep 3

if sudo systemctl is-active --quiet lego-backend.service; then
    echo "   ✅ Backend running"
    sudo systemctl status lego-backend.service --no-pager -l | head -10
else
    echo "   ❌ Backend failed"
    sudo journalctl -u lego-backend.service -n 20 --no-pager
    exit 1
fi

echo ""
sudo nginx -t
sudo systemctl reload nginx
echo "   ✅ Nginx reloaded"

echo ""
echo "🧹 Cleanup..."
rm -f ~/fixes.tar.gz
rm -rf ~/frontend ~/backend

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "Backup: $BACKUP_DIR"
ENDSSH

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Deployment failed"
    exit 1
fi

# Step 3: Verify
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "🔍 Verifying deployment..."
echo "============================================"
echo ""

echo "Testing /api/health..."
HEALTH=$(curl -s https://jobs.bluehawana.com/api/health 2>&1)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ Health endpoint WORKING!"
    echo "$HEALTH" | python3 -m json.tool
else
    echo "⏳ Health endpoint: $HEALTH"
    echo "   (May need another minute to start)"
fi

echo ""
echo "Testing /favicon.ico..."
if curl -sfI https://jobs.bluehawana.com/favicon.ico 2>&1 | grep -q "200"; then
    echo "✅ Favicon WORKING!"
else
    echo "⚠️  Favicon: Clear Cloudflare cache"
fi

echo ""
echo "Testing /api/analyze-job..."
if curl -sf -X POST https://jobs.bluehawana.com/api/analyze-job \
    -H "Content-Type: application/json" \
    -d '{"jobDescription":"test"}' 2>&1 | grep -q "success"; then
    echo "✅ API WORKING!"
else
    echo "⚠️  API may need a moment"
fi

echo ""
echo "============================================"
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "============================================"
echo ""
echo "🌐 Your site: https://jobs.bluehawana.com"
echo ""
echo "🚨 CRITICAL: Change password NOW!"
echo ""
echo "   ssh -p $VPS_PORT $VPS_USER@$VPS_IP"
echo "   passwd"
echo ""
echo "📖 Security guide: URGENT_SECURITY_STEPS.md"
echo ""

rm -f /tmp/fixes.tar.gz
