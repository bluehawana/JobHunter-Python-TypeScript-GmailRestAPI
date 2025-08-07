#!/bin/bash
# Quick fix for weather.bluehawana.com domain

echo "🔧 Quick Fix for weather.bluehawana.com"
echo "=" * 40

WEATHER_APP="weatheranywhere-917b4ca5eb69"

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login check
heroku auth:whoami || heroku login

echo "🌤️  Configuring Weather App Domain..."

# Ensure the domain is added
echo "📱 Adding custom domain..."
heroku domains:add weather.bluehawana.com --app $WEATHER_APP 2>/dev/null || echo "Domain already exists"

# Enable SSL
echo "🔒 Enabling SSL..."
heroku certs:auto:enable --app $WEATHER_APP

# Wake up the app
echo "⏰ Waking up the app..."
curl -s "https://$WEATHER_APP.herokuapp.com" > /dev/null

# Scale the app to ensure it's running
echo "⚡ Ensuring app is running..."
heroku ps:scale web=1 --app $WEATHER_APP

# Show current status
echo ""
echo "📊 Current Status:"
heroku ps --app $WEATHER_APP

echo ""
echo "🌐 Domain Configuration:"
heroku domains --app $WEATHER_APP

echo ""
echo "✅ Fix applied! Please:"
echo "1. Wait 5-10 minutes for DNS propagation"
echo "2. Ensure your DNS has this CNAME record:"
echo "   Name: weather"
echo "   Value: $WEATHER_APP.herokuapp.com"
echo "3. Test the direct URL first: https://$WEATHER_APP.herokuapp.com"
echo "4. Then test: https://weather.bluehawana.com"