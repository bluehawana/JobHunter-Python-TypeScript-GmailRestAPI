#!/bin/bash

# Deploy Template-Based LEGO System to VPS Server
# Server: 94.72.141.71:1025
# User: harvad

echo "=========================================="
echo "Deploying Template System to VPS"
echo "=========================================="

SERVER="harvad@94.72.141.71"
PORT="1025"
REMOTE_PATH="/var/www/lego-job-generator/backend"

echo ""
echo "Step 1: Upload cv_templates.py..."
scp -P $PORT backend/cv_templates.py $SERVER:$REMOTE_PATH/

echo ""
echo "Step 2: Upload updated lego_api.py..."
scp -P $PORT backend/app/lego_api.py $SERVER:$REMOTE_PATH/app/

echo ""
echo "Step 3: Create job_applications directory on server if it doesn't exist..."
ssh $SERVER -p $PORT "mkdir -p $REMOTE_PATH/job_applications"

echo ""
echo "Step 4: Upload ecarx_android_developer template folder..."
scp -P $PORT -r job_applications/ecarx_android_developer $SERVER:$REMOTE_PATH/job_applications/

echo ""
echo "Step 5: Upload other template folders..."
echo "  - Uploading tata_incident_management..."
scp -P $PORT -r job_applications/tata_incident_management $SERVER:$REMOTE_PATH/job_applications/

echo "  - Uploading nasdaq_devops_cloud..."
scp -P $PORT -r job_applications/nasdaq_devops_cloud $SERVER:$REMOTE_PATH/job_applications/

echo "  - Uploading doit_international..."
scp -P $PORT -r job_applications/doit_international $SERVER:$REMOTE_PATH/job_applications/

echo ""
echo "Step 6: Verify files on server..."
ssh $SERVER -p $PORT "ls -la $REMOTE_PATH/cv_templates.py"
ssh $SERVER -p $PORT "ls -la $REMOTE_PATH/app/lego_api.py"
ssh $SERVER -p $PORT "ls -la $REMOTE_PATH/job_applications/ecarx_android_developer/"

echo ""
echo "Step 7: Restart Gunicorn..."
ssh $SERVER -p $PORT "pkill -9 gunicorn && cd $REMOTE_PATH && source venv/bin/activate && gunicorn --bind 127.0.0.1:5000 --workers 3 --daemon lego_app:app"

echo ""
echo "Step 8: Wait 2 seconds for Gunicorn to start..."
sleep 2

echo ""
echo "Step 9: Check Gunicorn status..."
ssh $SERVER -p $PORT "ps aux | grep gunicorn | grep -v grep"

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "Test the system at: https://jobs.bluehawana.com"
echo ""
echo "Test with Android job URL:"
echo "https://careers.cpacsystems.se/jobs/6832158-android-platform-developer"
echo ""
