#!/bin/bash
# Update LEGO API on AlphaVPS server

echo "🚀 Updating LEGO API on jobs.bluehawana.com..."

# Upload updated lego_api.py
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

# SSH and restart service
ssh -p 1025 harvad@94.72.141.71 << 'EOF'
cd /var/www/lego-job-generator/backend

# Install required packages if not already installed
source venv/bin/activate
pip install requests beautifulsoup4 --quiet

# Restart the service
sudo systemctl restart lego-job-generator

# Check status
sudo systemctl status lego-job-generator --no-pager

echo "✅ LEGO API updated successfully!"
echo "🌐 Test at: http://jobs.bluehawana.com"
EOF

echo ""
echo "✅ Deployment complete!"
echo "🌐 Visit: http://jobs.bluehawana.com"
