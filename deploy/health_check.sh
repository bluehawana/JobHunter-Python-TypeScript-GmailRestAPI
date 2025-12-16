#!/bin/bash
# 🏥 Health Check Script for LEGO Bricks Job Generator
# Run this to verify everything is working

echo "🏥 Running health checks..."
echo ""

# Check backend service
echo "1️⃣ Checking backend service..."
if sudo systemctl is-active --quiet lego-backend; then
    echo "   ✅ Backend service is running"
else
    echo "   ❌ Backend service is NOT running"
    echo "   Run: sudo systemctl start lego-backend"
fi

# Check nginx
echo "2️⃣ Checking Nginx..."
if sudo systemctl is-active --quiet nginx; then
    echo "   ✅ Nginx is running"
else
    echo "   ❌ Nginx is NOT running"
    echo "   Run: sudo systemctl start nginx"
fi

# Check backend API
echo "3️⃣ Checking backend API..."
if curl -s http://localhost:5000/health | grep -q "healthy"; then
    echo "   ✅ Backend API is responding"
else
    echo "   ❌ Backend API is NOT responding"
    echo "   Check logs: sudo journalctl -u lego-backend -n 50"
fi

# Check frontend
echo "4️⃣ Checking frontend..."
if curl -s http://localhost | grep -q "LEGO"; then
    echo "   ✅ Frontend is accessible"
else
    echo "   ❌ Frontend is NOT accessible"
    echo "   Check nginx logs: sudo tail -f /var/log/nginx/error.log"
fi

# Check disk space
echo "5️⃣ Checking disk space..."
DISK_USAGE=$(df -h /var/www/lego-job-generator | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo "   ✅ Disk space OK ($DISK_USAGE% used)"
else
    echo "   ⚠️  Disk space warning ($DISK_USAGE% used)"
    echo "   Consider cleaning old PDFs: find /var/www/lego-job-generator/backend/generated_applications -type d -mtime +7 -exec rm -rf {} +"
fi

# Check PDF generation capability
echo "6️⃣ Checking PDF generation..."
if which pdflatex > /dev/null; then
    echo "   ✅ pdflatex is installed"
else
    echo "   ❌ pdflatex is NOT installed"
    echo "   Run: sudo apt-get install texlive-latex-base texlive-latex-extra"
fi

# Check SSL certificate
echo "7️⃣ Checking SSL certificate..."
if sudo certbot certificates 2>/dev/null | grep -q "jobs.bluehawana.com"; then
    EXPIRY=$(sudo certbot certificates 2>/dev/null | grep "Expiry Date" | head -1)
    echo "   ✅ SSL certificate is configured"
    echo "   $EXPIRY"
else
    echo "   ⚠️  SSL certificate not found"
    echo "   Run: sudo certbot --nginx -d jobs.bluehawana.com"
fi

# Check recent errors
echo "8️⃣ Checking recent errors..."
ERROR_COUNT=$(sudo journalctl -u lego-backend --since "1 hour ago" | grep -i error | wc -l)
if [ $ERROR_COUNT -eq 0 ]; then
    echo "   ✅ No errors in the last hour"
else
    echo "   ⚠️  Found $ERROR_COUNT errors in the last hour"
    echo "   View logs: sudo journalctl -u lego-backend -n 50"
fi

echo ""
echo "🎯 Overall Status:"
if sudo systemctl is-active --quiet lego-backend && sudo systemctl is-active --quiet nginx; then
    echo "   ✅ System is healthy and running"
    echo "   🌐 Access at: https://jobs.bluehawana.com"
else
    echo "   ❌ System has issues - check details above"
fi
