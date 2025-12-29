#!/bin/bash
# Restart LEGO Job Generator service on AlphaVPS server

echo "🔄 Restarting LEGO Job Generator service..."
echo ""

# Restart the service
sudo systemctl restart lego-job-generator

# Wait a moment
sleep 3

# Check status
echo "📊 Service Status:"
sudo systemctl status lego-job-generator --no-pager

echo ""
echo "✅ Service restarted!"
echo ""
echo "🌐 Test the application:"
echo "   http://jobs.bluehawana.com"
echo ""
echo "🔍 Check logs:"
echo "   sudo journalctl -u lego-job-generator -f"
