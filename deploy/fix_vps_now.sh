#!/bin/bash
# Quick fix for VPS PDF compilation error

echo "🚑 Fixing VPS at jobs.bluehawana.com..."
echo ""

ssh -p 1025 harvad@94.72.141.71 << 'EOF'
cd /var/www/lego-job-generator

echo "1️⃣ Pulling latest changes..."
git pull origin main

echo ""
echo "2️⃣ Checking template files..."
echo "CV templates: $(find job_applications -name "*_CV.tex" -type f | wc -l)"
echo "CL templates: $(find job_applications -name "*_CL.tex" -type f | wc -l)"

echo ""
echo "3️⃣ Verifying Python imports..."
source venv/bin/activate
python3 << 'PYTHON'
try:
    from cv_templates import CVTemplateManager
    print("✓ CVTemplateManager imports OK")
    
    manager = CVTemplateManager()
    print(f"✓ Template manager initialized")
    
    # Test loading a template
    template = manager.load_template('devops_cloud', 'cv')
    if template:
        print(f"✓ Template loading works ({len(template)} chars)")
    else:
        print("✗ Template loading failed")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
PYTHON

echo ""
echo "4️⃣ Restarting service..."
sudo systemctl restart lego-job-generator

echo ""
echo "5️⃣ Checking service status..."
sleep 2
sudo systemctl status lego-job-generator --no-pager | head -15

echo ""
echo "6️⃣ Checking recent logs for errors..."
sudo journalctl -u lego-job-generator -n 20 --no-pager | grep -i error || echo "No errors found"

EOF

echo ""
echo "✅ Fix attempt complete!"
echo "🌐 Test at: http://jobs.bluehawana.com"
echo ""
echo "If still failing, run: ./deploy/diagnose_vps.sh"
