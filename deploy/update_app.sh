#!/bin/bash
# 🔄 Update LEGO Bricks Job Generator on AlphaVPS
# Use this script to deploy updates without full reinstall

set -e

echo "🔄 Updating LEGO Bricks Job Generator..."

APP_DIR="/var/www/lego-job-generator"

# Pull latest changes (if using git)
echo "📥 Pulling latest changes..."
cd $APP_DIR
# git pull origin main  # Uncomment if using git

# Update backend
echo "🐍 Updating backend..."
cd $APP_DIR/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
deactivate

# Rebuild frontend
echo "⚛️ Rebuilding frontend..."
cd $APP_DIR/frontend
npm install
npm run build

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart lego-backend
sudo systemctl reload nginx

# Check status
echo "✅ Update complete!"
sudo systemctl status lego-backend --no-pager

echo ""
echo "🌐 Application updated at https://jobs.bluehawana.com"
