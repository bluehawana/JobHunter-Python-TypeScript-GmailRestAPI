#!/bin/bash
# Install systemd service and timer

sudo cp /Users/bluehawana/Projects/Jobhunter/backend/jobhunter-automation.service /etc/systemd/system/
sudo cp /Users/bluehawana/Projects/Jobhunter/backend/jobhunter-automation.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jobhunter-automation.timer
sudo systemctl start jobhunter-automation.timer
echo "✅ Systemd timer installed and started!"
echo "📋 Timer status:"
sudo systemctl status jobhunter-automation.timer
