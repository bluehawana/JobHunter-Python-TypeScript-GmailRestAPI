#!/bin/bash
# Check DNS configuration for bluehawana.com domains

echo "🌐 DNS Configuration Check"
echo "=" * 30

echo "Checking weather.bluehawana.com DNS:"
echo "Expected: weatheranywhere-917b4ca5eb69.herokuapp.com"
echo "Actual:"
nslookup weather.bluehawana.com 2>/dev/null | grep -A 2 "Non-authoritative answer:" || echo "DNS not resolved yet"

echo ""
echo "Checking jobs.bluehawana.com DNS:"
echo "Expected: jobhunter-dashboard.herokuapp.com"  
echo "Actual:"
nslookup jobs.bluehawana.com 2>/dev/null | grep -A 2 "Non-authoritative answer:" || echo "DNS not resolved yet"

echo ""
echo "📋 If DNS is not working, add these CNAME records:"
echo "Name: weather → Value: weatheranywhere-917b4ca5eb69.herokuapp.com"
echo "Name: jobs → Value: jobhunter-dashboard.herokuapp.com"