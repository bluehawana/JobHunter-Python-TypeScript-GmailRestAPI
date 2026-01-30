#!/bin/bash
# Fix jobs.bluehawana.com dashboard deployment

echo "🔧 Fixing JobHunter Dashboard Deployment"
echo "=" * 50

JOBS_APP="jobhunter-dashboard"

echo "🎯 Target App: $JOBS_APP"

# Check current app status
echo "📱 Current App Status:"
heroku ps --app $JOBS_APP

# Check if we need to set the correct git remote
echo "🔗 Setting up git remote for correct app..."
heroku git:remote -a $JOBS_APP

# Create the correct Procfile for dashboard
echo "📄 Creating Procfile for dashboard..."
echo "web: python dashboard_app.py" > Procfile

# Deploy the dashboard to the correct app
echo "🚀 Deploying dashboard to correct app..."
git add Procfile
git commit -m "Fix: Deploy dashboard to correct jobhunter-dashboard app" || echo "No changes to commit"

# Push to the correct app
git push heroku main

# Scale the web dyno
echo "⚡ Scaling web dyno..."
heroku ps:scale web=1 --app $JOBS_APP

# Check final status
echo "📊 Final App Status:"
heroku ps --app $JOBS_APP

# Test the deployment
echo "🧪 Testing deployment..."
sleep 5
curl -I "https://$JOBS_APP.herokuapp.com" 2>/dev/null | head -3

echo ""
echo "✅ Dashboard should now be available at:"
echo "   Direct: https://$JOBS_APP.herokuapp.com"
echo "   Custom: https://jobs.bluehawana.com"