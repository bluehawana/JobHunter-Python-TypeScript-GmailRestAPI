#!/bin/bash
# Install Lego API as a systemd service with auto-restart

set -e

echo "🔧 Installing Lego API systemd service..."

# Copy service file
sudo cp /var/www/lego-job-generator/deploy/lego-api.service /etc/systemd/system/

# Make health check script executable
chmod +x /var/www/lego-job-generator/deploy/health_check_lego.sh

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable lego-api

# Stop any existing process on port 8000
echo "🛑 Stopping any existing process on port 8000..."
sudo lsof -ti:8000 | xargs sudo kill -9 2>/dev/null || true
sleep 2

# Start the service
echo "🚀 Starting Lego API service..."
sudo systemctl start lego-api

# Wait a moment
sleep 3

# Check status
echo ""
echo "📊 Service Status:"
sudo systemctl status lego-api --no-pager

echo ""
echo "🔍 Checking if API is running..."
if sudo lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ API is running on port 8000"
else
    echo "❌ API is NOT running on port 8000"
    echo "Check logs with: sudo journalctl -u lego-api -n 50"
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status lego-api    # Check status"
echo "  sudo systemctl restart lego-api   # Restart service"
echo "  sudo systemctl stop lego-api      # Stop service"
echo "  sudo systemctl start lego-api     # Start service"
echo "  sudo journalctl -u lego-api -f    # View logs (live)"
echo "  sudo journalctl -u lego-api -n 50 # View last 50 log lines"
echo ""
echo "📝 Setting up health check cron job (every 30 minutes)..."

# Add cron job for health check
CRON_JOB="*/30 * * * * /var/www/lego-job-generator/deploy/health_check_lego.sh"
(crontab -l 2>/dev/null | grep -v "health_check_lego.sh"; echo "$CRON_JOB") | crontab -

echo "✅ Health check cron job installed (runs every 30 minutes)"
echo "   View health check logs: tail -f /var/www/lego-job-generator/backend/app/health_check.log"
