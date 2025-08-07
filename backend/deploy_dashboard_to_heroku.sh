#!/bin/bash
# Deploy JobHunter Dashboard to Heroku with custom domain integration

echo "🚀 Deploying JobHunter Dashboard to Heroku..."
echo "🌐 For integration with bluehawana.com/jobs"

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login check
heroku auth:whoami || heroku login

# Create app
APP_NAME="jobhunter-dashboard"
echo "📱 Creating Heroku app: $APP_NAME"
heroku create $APP_NAME --region eu || echo "App already exists"

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set ANTHROPIC_AUTH_TOKEN=REMOVED_SECRET --app $APP_NAME
heroku config:set ANTHROPIC_BASE_URL=https://anyrouter.top --app $APP_NAME
heroku config:set CLAUDE_MODEL=claude-3-7-sonnet-20250219 --app $APP_NAME
heroku config:set SENDER_EMAIL=leeharvad@gmail.com --app $APP_NAME
heroku config:set SENDER_GMAIL_PASSWORD=vsdclxhjnklrccsf --app $APP_NAME
heroku config:set TARGET_EMAIL=hongzhili01@gmail.com --app $APP_NAME
heroku config:set TZ=Europe/Stockholm --app $APP_NAME
heroku config:set ENVIRONMENT=production --app $APP_NAME

# Add buildpacks
echo "📦 Adding buildpacks..."
heroku buildpacks:add --index 1 https://github.com/Thermondo/heroku-buildpack-texlive.git --app $APP_NAME
heroku buildpacks:add --index 2 heroku/python --app $APP_NAME

# Create Procfile for dashboard
echo "web: python dashboard_app.py" > Procfile

# Deploy
echo "🚀 Deploying dashboard..."
git add .
git commit -m "Deploy JobHunter Dashboard for bluehawana.com/jobs"
git push heroku main

# Scale
heroku ps:scale web=1 --app $APP_NAME

echo "✅ Dashboard deployed!"
echo "🌐 App URL: https://$APP_NAME.herokuapp.com"
echo "📋 Next steps for custom domain:"
echo "   1. Add custom domain: heroku domains:add jobs.bluehawana.com --app $APP_NAME"
echo "   2. Configure DNS CNAME: jobs.bluehawana.com -> $APP_NAME.herokuapp.com"
echo "   3. Add SSL: heroku certs:auto:enable --app $APP_NAME"