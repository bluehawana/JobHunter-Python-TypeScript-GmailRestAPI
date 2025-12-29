#!/bin/bash
# Deployment commands for AlphaVPS (94.72.141.71:1025)

# Copy Python files
echo "Copying ai_analyzer.py..."
scp -P 1025 backend/ai_analyzer.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/

echo "Copying cv_templates.py..."
scp -P 1025 backend/cv_templates.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/

echo "Copying lego_api.py..."
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

echo "Copying minimax_search module..."
scp -P 1025 -r backend/minimax_search harvad@94.72.141.71:/var/www/lego-job-generator/backend/

echo "Copying test script..."
scp -P 1025 backend/test_vps_ai.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/

echo "Copying .env file..."
scp -P 1025 .env harvad@94.72.141.71:/var/www/lego-job-generator/

echo "✅ All files copied!"
echo ""
echo "Next steps:"
echo "1. SSH to VPS: ssh -p 1025 harvad@94.72.141.71"
echo "2. Install package: pip3 install anthropic"
echo "3. Test: python3 backend/test_vps_ai.py"
echo "4. Restart: sudo systemctl restart lego-api"
