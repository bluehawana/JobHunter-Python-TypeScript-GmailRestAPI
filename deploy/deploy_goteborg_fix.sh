#!/bin/bash
# Deploy fix for Swedish job site company extraction

echo "🚀 Deploying Göteborgs Stad extraction fix..."

# Upload updated files
echo "📤 Uploading updated lego_api.py..."
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

echo "📤 Uploading updated linkedin_job_extractor.py..."
scp -P 1025 backend/linkedin_job_extractor.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/

# SSH and restart
ssh -p 1025 harvad@94.72.141.71 << 'EOF'
cd /var/www/lego-job-generator/backend

# Restart the service
sudo systemctl restart lego-job-generator

# Check status
sudo systemctl status lego-job-generator --no-pager | head -20

echo ""
echo "✅ Deployment complete!"
echo "🌐 Test at: http://jobs.bluehawana.com"
EOF

echo ""
echo "✅ Fix deployed successfully!"
echo ""
echo "📝 Testing instructions:"
echo "1. Go to http://jobs.bluehawana.com"
echo "2. Paste the Göteborgs Stad job URL"
echo "3. Manually enter company: 'Göteborgs Stad'"
echo "4. Manually enter title: 'Azure Specialist'"
echo "5. Generate cover letter"
echo "6. Verify company name shows 'Göteborgs Stad' (not 'att')"
