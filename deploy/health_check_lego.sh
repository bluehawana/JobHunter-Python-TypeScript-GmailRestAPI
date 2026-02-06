#!/bin/bash
# Health check script for Lego API
# Checks if the API is responding and restarts if needed

LOG_FILE="/var/www/lego-job-generator/backend/app/health_check.log"
API_URL="http://127.0.0.1:8000/api/health"

echo "[$(date)] Starting health check..." >> "$LOG_FILE"

# Check if port 8000 is listening
if ! sudo lsof -i :8000 > /dev/null 2>&1; then
    echo "[$(date)] ❌ Port 8000 not listening - restarting service" >> "$LOG_FILE"
    sudo systemctl restart lego-api
    sleep 5
    exit 1
fi

# Check if API responds to health check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL" --max-time 5)

if [ "$HTTP_CODE" != "200" ]; then
    echo "[$(date)] ❌ API not responding (HTTP $HTTP_CODE) - restarting service" >> "$LOG_FILE"
    sudo systemctl restart lego-api
    sleep 5
    exit 1
fi

echo "[$(date)] ✅ API is healthy" >> "$LOG_FILE"
exit 0
