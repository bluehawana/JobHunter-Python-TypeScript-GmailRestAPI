#!/bin/bash

# 🚀 Deploy AI Intelligence to VPS
# This script deploys the MiniMax M2 AI integration to your VPS

set -e  # Exit on error

# Configuration - UPDATE THESE VALUES
VPS_USER="${VPS_USER:-your-vps-user}"
VPS_IP="${VPS_IP:-your-vps-ip}"
PROJECT_PATH="${PROJECT_PATH:-/path/to/JobHunter-Python-TypeScript-GmailRestAPI}"

echo "════════════════════════════════════════════════════════════════"
echo "🚀 Deploying AI Intelligence to VPS"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "VPS: $VPS_USER@$VPS_IP"
echo "Path: $PROJECT_PATH"
echo ""

# Check if we can connect to VPS
echo "🔍 Checking VPS connection..."
if ! ssh -o ConnectTimeout=5 $VPS_USER@$VPS_IP "echo 'Connected'" > /dev/null 2>&1; then
    echo "❌ Cannot connect to VPS. Please check:"
    echo "   - VPS_USER and VPS_IP are correct"
    echo "   - SSH keys are set up"
    echo "   - VPS is running"
    exit 1
fi
echo "✅ VPS connection successful"
echo ""

# 1. Backup existing files
echo "📦 Creating backup..."
ssh $VPS_USER@$VPS_IP << EOF
    cd $PROJECT_PATH
    mkdir -p backups
    tar -czf backups/backup_\$(date +%Y%m%d_%H%M%S).tar.gz \
        backend/ai_analyzer.py \
        backend/cv_templates.py \
        backend/app/lego_api.py \
        .env 2>/dev/null || true
    echo "✅ Backup created"
EOF

# 2. Copy updated files
echo ""
echo "📤 Uploading updated files..."

# Copy Python files
echo "  → ai_analyzer.py"
scp backend/ai_analyzer.py $VPS_USER@$VPS_IP:$PROJECT_PATH/backend/

echo "  → cv_templates.py"
scp backend/cv_templates.py $VPS_USER@$VPS_IP:$PROJECT_PATH/backend/

echo "  → lego_api.py"
scp backend/app/lego_api.py $VPS_USER@$VPS_IP:$PROJECT_PATH/backend/app/

# Copy minimax_search module
echo "  → minimax_search/ module"
rsync -avz --exclude '__pycache__' --exclude '*.pyc' \
    backend/minimax_search/ \
    $VPS_USER@$VPS_IP:$PROJECT_PATH/backend/minimax_search/

echo "✅ Files uploaded"

# 3. Update environment variables
echo ""
echo "🔐 Updating environment variables..."
scp .env $VPS_USER@$VPS_IP:$PROJECT_PATH/.env
ssh $VPS_USER@$VPS_IP "chmod 600 $PROJECT_PATH/.env"
echo "✅ Environment updated"

# 4. Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
ssh $VPS_USER@$VPS_IP << EOF
    cd $PROJECT_PATH
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "  → Activating virtual environment"
        source venv/bin/activate
    fi
    
    # Install dependencies
    echo "  → Installing anthropic"
    pip3 install anthropic --upgrade --quiet
    
    echo "  → Installing hypothesis"
    pip3 install hypothesis --upgrade --quiet
    
    echo "  → Installing pytest"
    pip3 install pytest --upgrade --quiet
    
    echo "✅ Dependencies installed"
EOF

# 5. Run tests
echo ""
echo "🧪 Running tests..."
ssh $VPS_USER@$VPS_IP << EOF
    cd $PROJECT_PATH
    
    # Test AI analyzer
    echo "  → Testing AI analyzer..."
    python3 -c "
from backend.ai_analyzer import AIAnalyzer
analyzer = AIAnalyzer()
if analyzer.is_available():
    print('    ✅ AI Analyzer available')
else:
    print('    ⚠️  AI Analyzer not available (will use keyword fallback)')
" || echo "    ⚠️  Could not test AI analyzer"
    
    # Test imports
    echo "  → Testing imports..."
    python3 -c "
from backend.cv_templates import CVTemplateManager
from backend.minimax_search.models import Document
print('    ✅ All imports successful')
" || echo "    ❌ Import test failed"
EOF

# 6. Restart application
echo ""
echo "🔄 Restarting application..."

ssh $VPS_USER@$VPS_IP << 'EOF'
    # Try different restart methods
    if systemctl list-units --type=service | grep -q jobhunter; then
        echo "  → Restarting systemd service..."
        sudo systemctl restart jobhunter-api || sudo systemctl restart jobhunter
    elif command -v pm2 &> /dev/null; then
        echo "  → Restarting PM2 process..."
        pm2 restart jobhunter-api || pm2 restart all
    else
        echo "  → Manual restart required"
        echo "    Please restart your application manually"
    fi
    
    echo "✅ Restart command sent"
EOF

# 7. Verify deployment
echo ""
echo "🔍 Verifying deployment..."
sleep 3  # Wait for service to start

ssh $VPS_USER@$VPS_IP << EOF
    cd $PROJECT_PATH
    
    # Check if process is running
    if pgrep -f "python.*lego_api" > /dev/null; then
        echo "  ✅ Application is running"
    else
        echo "  ⚠️  Application may not be running"
    fi
    
    # Check environment variables
    if grep -q "ANTHROPIC_API_KEY" .env; then
        echo "  ✅ API key configured"
    else
        echo "  ❌ API key not found in .env"
    fi
EOF

# Summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ Deployment Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo "  1. Test the API: curl http://$VPS_IP:5000/api/health"
echo "  2. Check logs: ssh $VPS_USER@$VPS_IP 'tail -f /var/log/jobhunter/app.log'"
echo "  3. Test AI: Paste a job description in your web app"
echo ""
echo "📚 Documentation:"
echo "  - VPS_AI_DEPLOYMENT_GUIDE.md"
echo "  - INTELLIGENT_SYSTEM_SUMMARY.md"
echo ""
echo "🎉 Your VPS now has AI intelligence!"
echo "════════════════════════════════════════════════════════════════"
