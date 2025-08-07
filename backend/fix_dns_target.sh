#!/bin/bash
# Fix DNS to point to the correct Heroku endpoint

echo "🔧 Fixing DNS target for weather.bluehawana.com"
echo "=" * 50

WEATHER_APP="weatheranywhere"
CORRECT_ENDPOINT="weatheranywhere-917b4ca5eb69.herokuapp.com"

echo "🌤️  App Name: $WEATHER_APP"
echo "🌐 Correct Endpoint: $CORRECT_ENDPOINT"

# Remove the existing domain first
echo "🗑️  Removing existing domain configuration..."
heroku domains:remove weather.bluehawana.com --app $WEATHER_APP --confirm $WEATHER_APP

# Wait a moment
sleep 2

# Add the domain again (this should get the correct DNS target)
echo "📱 Re-adding domain with correct configuration..."
heroku domains:add weather.bluehawana.com --app $WEATHER_APP

# Show the current domain configuration
echo "🌐 Current Domain Configuration:"
heroku domains --app $WEATHER_APP

# Test the correct endpoint
echo "🧪 Testing correct endpoint:"
curl -I "https://$CORRECT_ENDPOINT" 2>/dev/null | head -3

echo ""
echo "📋 IMPORTANT: Update your DNS CNAME record to:"
echo "   Name: weather"
echo "   Value: $(heroku domains --app $WEATHER_APP | grep 'weather.bluehawana.com' | awk '{print $4}')"
echo ""
echo "✅ The domain should work once DNS is updated correctly!"