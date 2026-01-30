#!/bin/bash
# Test jobs.bluehawana.com dashboard

echo "🎯 Testing JobHunter Dashboard at jobs.bluehawana.com"
echo "=" * 50

JOBS_APP="jobhunter-dashboard"

# Check if the app exists and is running
echo "📱 Checking JobHunter Dashboard App Status..."
heroku ps --app $JOBS_APP

echo ""
echo "🌐 Checking Domain Configuration:"
heroku domains --app $JOBS_APP

echo ""
echo "🔒 Checking SSL Certificates:"
heroku certs --app $JOBS_APP

echo ""
echo "🧪 Testing Direct Heroku URL:"
echo "Testing https://$JOBS_APP.herokuapp.com"
curl -I "https://$JOBS_APP.herokuapp.com" 2>/dev/null | head -5

echo ""
echo "🧪 Testing Custom Domain:"
echo "Testing https://jobs.bluehawana.com"
curl -I "https://jobs.bluehawana.com" 2>/dev/null | head -5

echo ""
echo "🔍 Testing DNS Resolution:"
echo "jobs.bluehawana.com resolves to:"
nslookup jobs.bluehawana.com 2>/dev/null | grep -A 2 "Non-authoritative answer:" || echo "DNS not resolved yet"

echo ""
echo "🧪 Testing Dashboard API:"
echo "Testing https://jobs.bluehawana.com/health"
curl -s "https://jobs.bluehawana.com/health" 2>/dev/null | head -3 || echo "API not responding"

echo ""
echo "📋 DASHBOARD STATUS SUMMARY:"
echo "Direct Heroku URL: https://$JOBS_APP.herokuapp.com"
echo "Custom Domain: https://jobs.bluehawana.com"
echo "Expected Features:"
echo "  - Professional dashboard interface"
echo "  - Real-time automation status"
echo "  - Manual trigger controls"
echo "  - Execution history"
echo "  - Success rate analytics"