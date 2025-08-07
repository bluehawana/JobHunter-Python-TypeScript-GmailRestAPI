#!/bin/bash
echo "🧪 Testing bluehawana.com domain setup..."

echo "Testing JobHunter Dashboard:"
curl -I https://jobs.bluehawana.com 2>/dev/null | head -1

echo "Testing Weather App:"
curl -I https://weather.bluehawana.com 2>/dev/null | head -1

echo "Testing JobHunter API:"
curl -s https://jobs.bluehawana.com/health | jq '.status' 2>/dev/null || echo "API test failed"

echo "✅ Domain tests completed!"
