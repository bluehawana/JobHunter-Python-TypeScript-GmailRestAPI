#!/bin/bash
# Update LEGO API on AlphaVPS server (no sudo required)

echo "🚀 Updating LEGO API on jobs.bluehawana.com..."

# Upload updated lego_api.py
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

echo ""
echo "✅ File uploaded successfully!"
echo ""
echo "📋 Next steps (run on server):"
echo "   ssh -p 1025 harvad@94.72.141.71"
echo "   cd /var/www/lego-job-generator/backend"
echo "   source venv/bin/activate"
echo "   pip install requests beautifulsoup4"
echo "   sudo systemctl restart lego-job-generator"
echo ""
echo "🌐 Then test at: http://jobs.bluehawana.com"
