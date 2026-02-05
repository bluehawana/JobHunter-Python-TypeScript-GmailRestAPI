#!/bin/bash
# Atomic restart script - ensures ALL workers reload simultaneously
# This guarantees 100% consistency across all requests

set -e

echo "🔄 Atomic Restart - Ensuring All Workers Reload Together"
echo "=========================================================="
echo ""

SERVICE_NAME="lego-job-generator"
HEALTH_CHECK_URL="http://127.0.0.1:5000/health"
MAX_WAIT=30

# Function to check if service is healthy
check_health() {
    curl -sf "$HEALTH_CHECK_URL" > /dev/null 2>&1
    return $?
}

# Function to wait for service to be healthy
wait_for_health() {
    local wait_time=0
    echo "⏳ Waiting for service to be healthy..."
    
    while [ $wait_time -lt $MAX_WAIT ]; do
        if check_health; then
            echo "✅ Service is healthy!"
            return 0
        fi
        sleep 1
        wait_time=$((wait_time + 1))
        echo -n "."
    done
    
    echo ""
    echo "❌ Service did not become healthy within ${MAX_WAIT}s"
    return 1
}

echo "Step 1: Stop the service completely"
echo "-----------------------------------"
sudo systemctl stop $SERVICE_NAME
echo "✅ Service stopped"
echo ""

# Wait a moment to ensure all workers are dead
sleep 2

# Verify no gunicorn processes are running
if pgrep -f "gunicorn.*lego_app" > /dev/null; then
    echo "⚠️  Found lingering gunicorn processes, killing them..."
    sudo pkill -9 -f "gunicorn.*lego_app"
    sleep 1
fi

echo "Step 2: Start the service with fresh workers"
echo "--------------------------------------------"
sudo systemctl start $SERVICE_NAME
echo "✅ Service started"
echo ""

echo "Step 3: Health check"
echo "-------------------"
if wait_for_health; then
    echo ""
    echo "Step 4: Verify service status"
    echo "-----------------------------"
    sudo systemctl status $SERVICE_NAME --no-pager | head -20
    echo ""
    echo "✅ ATOMIC RESTART COMPLETE!"
    echo ""
    echo "🎯 All workers are now running the same code version"
    echo "🌐 Test: http://jobs.bluehawana.com"
    echo ""
else
    echo ""
    echo "❌ RESTART FAILED - Service is not healthy"
    echo ""
    echo "🔍 Check logs:"
    echo "   sudo journalctl -u $SERVICE_NAME -n 50 --no-pager"
    exit 1
fi
