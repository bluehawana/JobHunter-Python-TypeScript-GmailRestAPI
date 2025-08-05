#!/bin/bash
"""
Deploy JobHunter LEGO System to Heroku
Automated 6 AM weekday job hunting
"""

echo "🚀 Deploying JobHunter LEGO System to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   brew tap heroku/brew && brew install heroku"
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Create Heroku app (if it doesn't exist)
APP_NAME="jobhunter-lego-system"
echo "📱 Creating Heroku app: $APP_NAME"
heroku create $APP_NAME --region eu || echo "App already exists"

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set ANTHROPIC_AUTH_TOKEN=sk-wldqMp1L48Uh85iQWgv05sRuUgtZxqyJAH92mW476z0SyiG4 --app $APP_NAME
heroku config:set ANTHROPIC_BASE_URL=https://anyrouter.top --app $APP_NAME
heroku config:set CLAUDE_MODEL=claude-3-7-sonnet-20250219 --app $APP_NAME
heroku config:set SENDER_EMAIL=leeharvad@gmail.com --app $APP_NAME
heroku config:set SENDER_GMAIL_PASSWORD=vsdclxhjnklrccsf --app $APP_NAME
heroku config:set SMTP_PASSWORD=vsdclxhjnklrccsf --app $APP_NAME
heroku config:set GMAIL_APP_PASSWORD=vsodrpyblpgtujof --app $APP_NAME
heroku config:set TARGET_EMAIL=hongzhili01@gmail.com --app $APP_NAME
heroku config:set TZ=Europe/Stockholm --app $APP_NAME
heroku config:set ENVIRONMENT=production --app $APP_NAME

# Add LaTeX buildpack (for PDF generation)
echo "📦 Adding LaTeX buildpack..."
heroku buildpacks:add --index 1 https://github.com/Thermondo/heroku-buildpack-texlive.git --app $APP_NAME
heroku buildpacks:add --index 2 heroku/python --app $APP_NAME

# Ensure all automation files are included
echo "📁 Preparing automation files..."
cp master_automation_orchestrator.py ./
cp improved_working_automation.py ./
cp -r templates/ ./
cp -r app/ ./

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy JobHunter Master Automation System to Heroku"
git push heroku main

# Scale the web dyno
echo "⚡ Scaling web dyno..."
heroku ps:scale web=1 --app $APP_NAME

# Show app info
echo "✅ Deployment completed!"
echo "🌐 App URL: https://$APP_NAME.herokuapp.com"
echo "📊 Dashboard: https://dashboard.heroku.com/apps/$APP_NAME"
echo "📅 Scheduled: Monday-Friday at 6:00 AM Stockholm time"

# Show logs
echo "📋 Recent logs:"
heroku logs --tail --app $APP_NAME