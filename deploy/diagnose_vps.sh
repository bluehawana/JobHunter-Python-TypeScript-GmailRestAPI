#!/bin/bash
# Diagnose VPS issues after deployment

echo "🔍 Diagnosing VPS at jobs.bluehawana.com..."
echo ""

ssh -p 1025 harvad@94.72.141.71 << 'EOF'
echo "📊 System Status"
echo "==============="
echo ""

echo "1️⃣ Service Status:"
sudo systemctl status lego-job-generator --no-pager | head -20
echo ""

echo "2️⃣ Recent Logs (last 50 lines):"
sudo journalctl -u lego-job-generator -n 50 --no-pager
echo ""

echo "3️⃣ Git Status:"
cd /var/www/lego-job-generator
git status
git log --oneline -5
echo ""

echo "4️⃣ Check LaTeX Installation:"
which pdflatex
pdflatex --version | head -3
echo ""

echo "5️⃣ Check Template Files:"
echo "CV Templates:"
find job_applications -name "*_CV.tex" -type f | wc -l
echo "CL Templates:"
find job_applications -name "*_CL.tex" -type f | wc -l
echo ""

echo "6️⃣ Check Python Dependencies:"
source venv/bin/activate
python3 -c "import sys; print(f'Python: {sys.version}')"
python3 -c "from cv_templates import CVTemplateManager; print('✓ cv_templates imports OK')"
python3 -c "from app.lego_api import analyze_job_description; print('✓ lego_api imports OK')"
echo ""

echo "7️⃣ Disk Space:"
df -h /var/www/lego-job-generator
echo ""

echo "8️⃣ Recent Error Logs:"
if [ -f /var/log/lego-job-generator/error.log ]; then
    tail -30 /var/log/lego-job-generator/error.log
else
    echo "No error log file found"
fi

EOF

echo ""
echo "✅ Diagnosis complete!"
