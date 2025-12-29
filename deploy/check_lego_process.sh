#!/bin/bash
# Check how LEGO Job Generator is running

echo "🔍 Checking LEGO Job Generator process..."
echo ""

echo "1️⃣ Checking Python processes:"
ps aux | grep -E 'lego_app|gunicorn|flask' | grep -v grep

echo ""
echo "2️⃣ Checking what's listening on port 5000:"
sudo netstat -tlnp | grep 5000 || sudo ss -tlnp | grep 5000

echo ""
echo "3️⃣ Checking nginx configuration:"
sudo nginx -t

echo ""
echo "4️⃣ Checking if backend directory exists:"
ls -la /var/www/lego-job-generator/backend/ | head -20

echo ""
echo "5️⃣ Checking for any systemd services:"
sudo systemctl list-units --type=service | grep -i lego

echo ""
echo "6️⃣ Checking supervisor (if installed):"
which supervisorctl && sudo supervisorctl status || echo "Supervisor not installed"
