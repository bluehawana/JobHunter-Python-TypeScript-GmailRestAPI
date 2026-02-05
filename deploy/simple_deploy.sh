#!/bin/bash
# Simple deployment - just tells you what to do on VPS

echo "🚀 Simple Deployment Guide"
echo "=========================="
echo ""
echo "Step 1: Push your code (if you have changes)"
echo "---------------------------------------------"
git add -A
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null || echo "No changes to commit"
git push origin main
echo ""

echo "Step 2: SSH to VPS and run these commands"
echo "------------------------------------------"
echo ""
echo "ssh harvad@jobs.bluehawana.com"
echo ""
echo "Then run:"
echo ""
echo "cd /var/www/lego-job-generator"
echo "git pull origin main"
echo "sudo systemctl stop lego-backend"
echo "sleep 2"
echo "sudo pkill -9 -f 'gunicorn.*lego_app'"
echo "sudo systemctl start lego-backend"
echo "sleep 3"
echo "curl http://127.0.0.1:5000/health"
echo ""
echo "✅ Done! Service restarted with all workers synchronized"
