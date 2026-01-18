#!/bin/bash
# 🚀 Deploy Updated Templates and LinkedIn Extraction to AlphaVPS
# Run this from your local machine

set -e  # Exit on error

VPS_HOST="harvad@94.72.141.71"
VPS_PORT="1025"
VPS_PATH="/var/www/lego-job-generator"

echo "=========================================="
echo "🚀 Deploying Updated Templates to AlphaVPS"
echo "=========================================="
echo ""
echo "VPS: $VPS_HOST:$VPS_PORT"
echo "Path: $VPS_PATH"
echo ""

# Check if key files exist locally
echo "📋 Checking local files..."
if [ ! -f "backend/linkedin_job_extractor.py" ]; then
    echo "❌ backend/linkedin_job_extractor.py not found!"
    exit 1
fi
if [ ! -f "backend/app/lego_api.py" ]; then
    echo "❌ backend/app/lego_api.py not found!"
    exit 1
fi
if [ ! -f "backend/template_customizer.py" ]; then
    echo "❌ backend/template_customizer.py not found!"
    exit 1
fi
echo "✅ All key files found locally"
echo ""

# Copy backend files
echo "📦 Copying backend files to VPS..."

echo "  → backend/linkedin_job_extractor.py"
scp -P $VPS_PORT backend/linkedin_job_extractor.py $VPS_HOST:$VPS_PATH/backend/

echo "  → backend/app/lego_api.py"
scp -P $VPS_PORT backend/app/lego_api.py $VPS_HOST:$VPS_PATH/backend/app/

echo "  → backend/template_customizer.py"
scp -P $VPS_PORT backend/template_customizer.py $VPS_HOST:$VPS_PATH/backend/

echo "  → backend/cv_templates.py"
scp -P $VPS_PORT backend/cv_templates.py $VPS_HOST:$VPS_PATH/backend/

echo "✅ Backend files copied successfully"
echo ""

# Copy all job application templates
echo "📁 Copying job application templates..."
echo "  → Syncing entire job_applications directory..."
rsync -avz -e "ssh -p $VPS_PORT" --delete job_applications/ $VPS_HOST:$VPS_PATH/job_applications/

echo "✅ Templates copied successfully"
echo ""

# Copy environment file
echo "🔧 Copying environment file..."
scp -P $VPS_PORT .env $VPS_HOST:$VPS_PATH/

echo "✅ Environment file copied"
echo ""

# Install dependencies and restart service
echo "🔧 Installing dependencies on VPS..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
cd /var/www/lego-job-generator
source backend/venv/bin/activate
pip install anthropic beautifulsoup4 requests
deactivate
echo "✅ Dependencies installed"
ENDSSH

echo ""
echo "🔄 Restarting service..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
sudo systemctl restart lego-backend.service
sleep 3
sudo systemctl status lego-backend.service --no-pager
ENDSSH

echo ""
echo "🧪 Testing the deployment..."
ssh -p $VPS_PORT $VPS_HOST << 'ENDSSH'
cd /var/www/lego-job-generator
echo "Testing LinkedIn extraction..."
python3 -c "
from backend.linkedin_job_extractor import extract_company_and_title
result = extract_company_and_title('Test content with Meltwater and Software Engineer')
print(f'Test result: {result}')
"
ENDSSH

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "🎉 Your VPS now has:"
echo "  • Updated cover letter templates with new format"
echo "  • LinkedIn job extraction functionality"
echo "  • Enhanced template customization"
echo "  • Vue.js added to all CV templates"
echo ""
echo "🌐 Test at: https://jobs.bluehawana.com"
echo ""
echo "New cover letter format:"
echo "  • Header: Company, Job Title, Location (no name)"
echo "  • Signature: Best Regards, Harvad (Hongzhi) Li"
echo "  • Footer: Address and date with line separator"
echo "  • Updated address: Ebbe Lieberathsgatan 27, 41265 Gothenburg"
echo ""