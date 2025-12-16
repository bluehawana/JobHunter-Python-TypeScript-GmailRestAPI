#!/bin/bash
# 📤 Upload LEGO Job Generator to AlphaVPS
# Run this from your project root directory

set -e

echo "📤 Uploading LEGO Job Generator to AlphaVPS..."

# Get current directory
CURRENT_DIR=$(pwd)
PROJECT_NAME=$(basename "$CURRENT_DIR")

echo "📁 Current directory: $CURRENT_DIR"
echo "📦 Project: $PROJECT_NAME"

# Create a clean deployment package (exclude unnecessary files)
echo "📦 Creating deployment package..."
tar --no-xattrs -czf lego-deploy.tar.gz \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='venv' \
    --exclude='job_applications' \
    --exclude='generated_applications' \
    --exclude='.env' \
    frontend/src/pages/LegoJobGenerator.tsx \
    frontend/src/styles/LegoJobGenerator.css \
    frontend/src/index.tsx \
    frontend/src/index.css \
    frontend/src/App.tsx \
    frontend/src/App.css \
    frontend/src/reportWebVitals.ts \
    frontend/src/react-app-env.d.ts \
    frontend/package.json \
    frontend/public \
    frontend/tsconfig.json \
    backend/app/lego_api.py \
    backend/lego_app.py \
    backend/gemini_content_polisher.py \
    backend/smart_latex_editor.py \
    deploy/

echo "✅ Package created: lego-deploy.tar.gz"

# Upload to server
echo "📤 Uploading to AlphaVPS..."
scp -P 1025 lego-deploy.tar.gz harvad@94.72.141.71:~/

echo "📤 Uploading deployment scripts..."
scp -P 1025 deploy/alphavps_setup.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/update_app.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/health_check.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/upgrade_nodejs.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/continue_deployment.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/check_frontend_files.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/complete_deployment.sh harvad@94.72.141.71:~/ 2>/dev/null || true

# Clean up local package
rm lego-deploy.tar.gz

echo ""
echo "✅ Upload complete!"
echo ""
echo "🚀 Next steps on server (ssh -p 1025 harvad@94.72.141.71):"
echo ""
echo "1. Upgrade Node.js to v18:"
echo "   chmod +x upgrade_nodejs.sh"
echo "   ./upgrade_nodejs.sh"
echo ""
echo "2. Continue deployment:"
echo "   chmod +x continue_deployment.sh"
echo "   ./continue_deployment.sh"
echo ""
echo "3. Verify deployment:"
echo "   sudo systemctl status lego-backend"
echo "   curl http://localhost:5000/health"
echo ""
echo "4. After DNS is configured, setup SSL:"
echo "   sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect"
