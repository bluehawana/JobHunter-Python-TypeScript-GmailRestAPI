#!/bin/bash
# Troubleshoot weather.bluehawana.com domain issues

echo "🔍 Troubleshooting weather.bluehawana.com"
echo "=" * 50

WEATHER_APP="weatheranywhere-917b4ca5eb69"

# Check if Heroku CLI is available
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Check Heroku authentication
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Check app status
echo ""
echo "📱 Checking Weather App Status..."
heroku ps --app $WEATHER_APP

# Check app logs
echo ""
echo "📋 Recent App Logs:"
heroku logs --tail --num=20 --app $WEATHER_APP

# Check domains
echo ""
echo "🌐 Checking Domain Configuration:"
heroku domains --app $WEATHER_APP

# Check SSL certificates
echo ""
echo "🔒 Checking SSL Certificates:"
heroku certs --app $WEATHER_APP

# Test DNS resolution
echo ""
echo "🔍 Testing DNS Resolution:"
echo "weather.bluehawana.com resolves to:"
nslookup weather.bluehawana.com || dig weather.bluehawana.com

# Test direct Heroku URL
echo ""
echo "🧪 Testing Direct Heroku URL:"
echo "Testing https://$WEATHER_APP.herokuapp.com"
curl -I "https://$WEATHER_APP.herokuapp.com" 2>/dev/null | head -5

# Test custom domain
echo ""
echo "🧪 Testing Custom Domain:"
echo "Testing https://weather.bluehawana.com"
curl -I "https://weather.bluehawana.com" 2>/dev/null | head -5

# Wake up the app if it's sleeping
echo ""
echo "⏰ Waking up the app (in case it's sleeping)..."
curl -s "https://$WEATHER_APP.herokuapp.com" > /dev/null
echo "App wake-up request sent"

# Check if we need to add the domain
echo ""
echo "🔧 Checking if domain needs to be added..."
DOMAIN_EXISTS=$(heroku domains --app $WEATHER_APP | grep "weather.bluehawana.com" || echo "NOT_FOUND")

if [[ "$DOMAIN_EXISTS" == "NOT_FOUND" ]]; then
    echo "❌ Domain not found. Adding weather.bluehawana.com..."
    heroku domains:add weather.bluehawana.com --app $WEATHER_APP
    echo "✅ Domain added. Please wait 5-10 minutes for DNS propagation."
else
    echo "✅ Domain is configured"
fi

# Enable SSL if not already enabled
echo ""
echo "🔒 Ensuring SSL is enabled..."
heroku certs:auto:enable --app $WEATHER_APP

echo ""
echo "📋 TROUBLESHOOTING SUMMARY"
echo "=" * 50
echo "If the domain still doesn't work:"
echo "1. Wait 5-10 minutes for DNS propagation"
echo "2. Check if your DNS provider has the CNAME record:"
echo "   Name: weather"
echo "   Value: $WEATHER_APP.herokuapp.com"
echo "3. Try accessing the direct Heroku URL first:"
echo "   https://$WEATHER_APP.herokuapp.com"
echo "4. Check if the app is running with: heroku ps --app $WEATHER_APP"
echo ""
echo "🔄 Run this script again in 10 minutes if issues persist"