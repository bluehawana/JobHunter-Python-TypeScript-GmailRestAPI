#!/bin/bash
# Deploy smart filename fix to VPS

echo "🚀 Deploying smart filename fix to VPS..."

# Copy frontend build
echo "📦 Copying frontend build..."
scp -r frontend/build/* alphavps:/var/www/lego-job-generator/frontend/build/

# Copy backend lego_api.py
echo "📦 Copying backend API..."
scp backend/app/lego_api.py alphavps:/var/www/lego-job-generator/backend/app/

# Restart backend service
echo "🔄 Restarting backend service..."
ssh alphavps "sudo systemctl restart lego-backend.service"

echo "✅ Deployment complete!"
echo "🧪 Test by generating a new application - filenames should now be cv_harvad_CompanyName.pdf"
