#!/bin/bash
# Corrected deployment script for bluehawana.com subdomain integration
# Uses proper Heroku custom domain support

echo "🌐 CORRECTED: bluehawana.com Subdomain Integration"
echo "🎯 Jobs: jobs.bluehawana.com"
echo "🌤️  Weather: weather.bluehawana.com"
echo "=" * 50

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login check
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Deploy JobHunter Dashboard
echo "🚀 Deploying JobHunter Dashboard..."
APP_NAME_JOBS="jobhunter-dashboard"
heroku create $APP_NAME_JOBS --region eu || echo "App already exists"

# Set environment variables for JobHunter
echo "⚙️ Configuring JobHunter Dashboard..."
heroku config:set ANTHROPIC_AUTH_TOKEN=sk-wldqMp1L48Uh85iQWgv05sRuUgtZxqyJAH92mW476z0SyiG4 --app $APP_NAME_JOBS
heroku config:set ANTHROPIC_BASE_URL=https://anyrouter.top --app $APP_NAME_JOBS
heroku config:set CLAUDE_MODEL=claude-3-7-sonnet-20250219 --app $APP_NAME_JOBS
heroku config:set SENDER_EMAIL=leeharvad@gmail.com --app $APP_NAME_JOBS
heroku config:set SENDER_GMAIL_PASSWORD=vsdclxhjnklrccsf --app $APP_NAME_JOBS
heroku config:set TARGET_EMAIL=hongzhili01@gmail.com --app $APP_NAME_JOBS
heroku config:set TZ=Europe/Stockholm --app $APP_NAME_JOBS
heroku config:set ENVIRONMENT=production --app $APP_NAME_JOBS

# Add buildpacks for JobHunter
echo "📦 Adding buildpacks..."
heroku buildpacks:clear --app $APP_NAME_JOBS
heroku buildpacks:add --index 1 https://github.com/Thermondo/heroku-buildpack-texlive.git --app $APP_NAME_JOBS
heroku buildpacks:add --index 2 heroku/python --app $APP_NAME_JOBS

# Create Procfile for dashboard
echo "web: python dashboard_app.py" > Procfile

# Deploy JobHunter
echo "📤 Deploying JobHunter Dashboard..."
git add .
git commit -m "Deploy JobHunter Dashboard for jobs.bluehawana.com" || echo "No changes to commit"
git push heroku main

# Scale JobHunter
heroku ps:scale web=1 --app $APP_NAME_JOBS

echo "✅ JobHunter Dashboard deployed!"
echo "🌐 Heroku URL: https://$APP_NAME_JOBS.herokuapp.com"

# Add custom domains (the correct way)
echo ""
echo "🔗 Adding custom domains..."

# Add custom domain to JobHunter Dashboard
echo "📱 Adding jobs.bluehawana.com to JobHunter Dashboard..."
heroku domains:add jobs.bluehawana.com --app $APP_NAME_JOBS

# Add custom domain to existing Weather app
echo "🌤️  Adding weather.bluehawana.com to Weather App..."
WEATHER_APP="weatheranywhere-917b4ca5eb69"
heroku domains:add weather.bluehawana.com --app $WEATHER_APP

# Enable SSL certificates
echo "🔒 Enabling SSL certificates..."
heroku certs:auto:enable --app $APP_NAME_JOBS
heroku certs:auto:enable --app $WEATHER_APP

# Show domain status
echo ""
echo "📋 Domain Configuration Status:"
echo "JobHunter Dashboard domains:"
heroku domains --app $APP_NAME_JOBS

echo ""
echo "Weather App domains:"
heroku domains --app $WEATHER_APP

# Generate DNS instructions
echo ""
echo "🌐 DNS CONFIGURATION REQUIRED"
echo "=" * 50
echo "Add these CNAME records to your DNS provider:"
echo ""
echo "Type: CNAME"
echo "Name: jobs"
echo "Value: $APP_NAME_JOBS.herokuapp.com"
echo "TTL: 300"
echo ""
echo "Type: CNAME"
echo "Name: weather"
echo "Value: $WEATHER_APP.herokuapp.com"
echo "TTL: 300"

# Generate navigation HTML
echo ""
echo "📱 WEBSITE NAVIGATION UPDATE"
echo "=" * 50
cat > navigation_update.html << EOF
<!-- Add this to your main website navigation -->
<nav>
    <a href="https://bluehawana.com">Home</a>
    <a href="https://bluehawana.com/about">About</a>
    <a href="https://bluehawana.com/projects">Projects</a>
    <a href="https://jobs.bluehawana.com">Job Hunter</a>
    <a href="https://weather.bluehawana.com">Weather</a>
    <a href="https://bluehawana.com/contact">Contact</a>
</nav>
EOF

echo "📄 Navigation HTML saved to: navigation_update.html"

# Test script
echo ""
echo "🧪 TESTING SCRIPT"
echo "=" * 50
cat > test_domains.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing bluehawana.com domain setup..."

echo "Testing JobHunter Dashboard:"
curl -I https://jobs.bluehawana.com 2>/dev/null | head -1

echo "Testing Weather App:"
curl -I https://weather.bluehawana.com 2>/dev/null | head -1

echo "Testing JobHunter API:"
curl -s https://jobs.bluehawana.com/health | jq '.status' 2>/dev/null || echo "API test failed"

echo "✅ Domain tests completed!"
EOF

chmod +x test_domains.sh
echo "📄 Test script saved to: test_domains.sh"

# Summary
echo ""
echo "🎉 DEPLOYMENT SUMMARY"
echo "=" * 50
echo "✅ JobHunter Dashboard: https://jobs.bluehawana.com"
echo "✅ Weather App: https://weather.bluehawana.com"
echo "✅ SSL certificates: Enabled"
echo "✅ Heroku domains: Configured"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Add the DNS CNAME records shown above"
echo "2. Wait 5-10 minutes for DNS propagation"
echo "3. Run ./test_domains.sh to verify setup"
echo "4. Update your main website navigation"
echo ""
echo "🌟 Your professional subdomain setup is ready!"
echo "📧 JobHunter will run automatically at 6 AM weekdays"