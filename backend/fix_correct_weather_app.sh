#!/bin/bash
# Fix weather domain with correct app name

echo "🔧 Fixing weather.bluehawana.com with correct app name"
echo "=" * 50

# Correct app name
WEATHER_APP="weatheranywhere"

echo "🌤️  Configuring Weather App: $WEATHER_APP"

# Add custom domain
echo "📱 Adding custom domain..."
heroku domains:add weather.bluehawana.com --app $WEATHER_APP

# Enable SSL
echo "🔒 Enabling SSL..."
heroku certs:auto:enable --app $WEATHER_APP

# Check app status
echo "📊 App Status:"
heroku ps --app $WEATHER_APP

# Show domains
echo "🌐 Domain Configuration:"
heroku domains --app $WEATHER_APP

# Test the app
echo "🧪 Testing direct URL:"
curl -I "https://$WEATHER_APP.herokuapp.com" 2>/dev/null | head -3

echo ""
echo "✅ Configuration complete!"
echo "🌐 Your weather app should now be available at:"
echo "   https://weather.bluehawana.com"
echo ""
echo "📋 DNS should already be working since it resolves correctly."
echo "⏰ Wait 2-3 minutes for SSL certificate provisioning."