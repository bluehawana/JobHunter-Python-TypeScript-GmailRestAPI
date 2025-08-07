#!/bin/bash
# Deploy Fixed JobHunter Dashboard to Heroku

echo "🔧 Deploying FIXED JobHunter Dashboard to Heroku..."

# Check if we're in the right directory
if [ ! -f "heroku_app.py" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Check Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login check
heroku auth:whoami || heroku login

# App name
APP_NAME="jobhunter-dashboard"

# Test imports first
echo "🧪 Testing imports..."
python3 test_heroku_imports.py
if [ $? -ne 0 ]; then
    echo "❌ Import test failed. Please fix imports first."
    exit 1
fi

echo "✅ Import test passed!"

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

# Deploy
echo "🚀 Deploying fixed dashboard..."
cd ..
git add .
git commit -m "Fix Heroku deployment: Update Procfile and improve error handling"
git push heroku main

# Scale
heroku ps:scale web=1 --app $APP_NAME

# Check status
echo "📊 Checking deployment status..."
heroku ps --app $APP_NAME
heroku logs --tail --app $APP_NAME &
LOGS_PID=$!

# Wait a bit then kill logs
sleep 10
kill $LOGS_PID 2>/dev/null

echo "✅ Deployment completed!"
echo "🌐 App URL: https://$APP_NAME.herokuapp.com"
echo "🔍 Check health: https://$APP_NAME.herokuapp.com/health"
echo "📋 View logs: heroku logs --tail --app $APP_NAME"