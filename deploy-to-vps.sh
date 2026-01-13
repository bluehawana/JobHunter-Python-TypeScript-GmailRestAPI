#!/bin/bash

###############################################################################
# Deploy JobHunter Fixes to AlphaVPS
# Server: harvad@94.72.141.71:1025
# Location: /var/www/lego-job-generator
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# VPS Configuration
VPS_HOST="94.72.141.71"
VPS_PORT="1025"
VPS_USER="harvad"
VPS_PATH="/var/www/lego-job-generator"
VPS_SERVICE="lego-backend.service"

print_header "🚀 Deploying JobHunter Fixes to VPS"

# Check if we can connect
print_info "Checking VPS connection..."
if ssh -p $VPS_PORT -o ConnectTimeout=5 $VPS_USER@$VPS_HOST "echo 'Connection OK'" 2>/dev/null; then
    print_success "VPS connection successful"
else
    print_error "Cannot connect to VPS. Please check:"
    echo "  1. VPS is running"
    echo "  2. SSH key is configured: ssh-copy-id -p $VPS_PORT $VPS_USER@$VPS_HOST"
    echo "  3. Port $VPS_PORT is accessible"
    exit 1
fi

# Step 1: Build frontend locally
print_header "Step 1: Building Frontend"
cd frontend
print_info "Installing dependencies..."
npm install --silent

print_info "Building production bundle..."
npm run build

if [ ! -d "build" ]; then
    print_error "Build failed - no build directory created"
    exit 1
fi

print_success "Frontend built successfully"
cd ..

# Step 2: Create deployment package
print_header "Step 2: Creating Deployment Package"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="jobhunter-fixes-${TIMESTAMP}.tar.gz"

print_info "Packaging files..."
tar -czf "$PACKAGE_NAME" \
    frontend/build/ \
    backend/app/lego_api.py \
    backend/requirements.txt \
    2>/dev/null

print_success "Package created: $PACKAGE_NAME"

# Step 3: Upload to VPS
print_header "Step 3: Uploading to VPS"

print_info "Uploading package..."
scp -P $VPS_PORT "$PACKAGE_NAME" "$VPS_USER@$VPS_HOST:~/"

print_success "Upload complete"

# Step 4: Deploy on VPS
print_header "Step 4: Deploying on VPS"

ssh -p $VPS_PORT $VPS_USER@$VPS_HOST << 'ENDSSH'
set -e

echo "[INFO] Creating backup..."
BACKUP_DIR="$HOME/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup current backend
if [ -f "/var/www/lego-job-generator/backend/app/lego_api.py" ]; then
    cp /var/www/lego-job-generator/backend/app/lego_api.py "$BACKUP_DIR/"
    echo "[SUCCESS] Backend backed up"
fi

# Backup current frontend
if [ -d "/var/www/lego-job-generator/frontend/build" ]; then
    cp -r /var/www/lego-job-generator/frontend/build "$BACKUP_DIR/"
    echo "[SUCCESS] Frontend backed up"
fi

echo "[INFO] Extracting new files..."
cd ~
tar -xzf jobhunter-fixes-*.tar.gz

echo "[INFO] Deploying backend..."
cp backend/app/lego_api.py /var/www/lego-job-generator/backend/app/
cp backend/requirements.txt /var/www/lego-job-generator/backend/

echo "[INFO] Installing Python dependencies..."
cd /var/www/lego-job-generator/backend
source venv/bin/activate
pip install -r requirements.txt --quiet
deactivate

echo "[INFO] Deploying frontend..."
rm -rf /var/www/lego-job-generator/frontend/build.old
if [ -d "/var/www/lego-job-generator/frontend/build" ]; then
    mv /var/www/lego-job-generator/frontend/build /var/www/lego-job-generator/frontend/build.old
fi
mv ~/frontend/build /var/www/lego-job-generator/frontend/

echo "[INFO] Restarting backend service..."
sudo systemctl restart lego-backend.service
sleep 3

echo "[INFO] Checking service status..."
if sudo systemctl is-active --quiet lego-backend.service; then
    echo "[SUCCESS] Backend service is running"
else
    echo "[ERROR] Backend service failed to start"
    echo "[INFO] Checking logs..."
    sudo journalctl -u lego-backend.service -n 20 --no-pager
    exit 1
fi

echo "[INFO] Reloading Nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo "[SUCCESS] Deployment complete!"
ENDSSH

print_success "Deployment completed on VPS"

# Step 5: Verify deployment
print_header "Step 5: Verifying Deployment"

sleep 5

print_info "Testing health endpoint..."
if curl -f -s https://jobs.bluehawana.com/api/health > /dev/null 2>&1; then
    print_success "Health endpoint is working!"
    curl -s https://jobs.bluehawana.com/api/health | python3 -m json.tool
else
    print_warning "Health endpoint not accessible yet (might need a few more seconds)"
fi

print_info "Testing job analysis..."
RESPONSE=$(curl -s -X POST https://jobs.bluehawana.com/api/analyze-job \
    -H "Content-Type: application/json" \
    -d '{"jobDescription":"DevOps Engineer test"}' 2>&1)

if echo "$RESPONSE" | grep -q "success"; then
    print_success "Job analysis is working!"
else
    print_warning "Job analysis response: $RESPONSE"
fi

print_info "Testing frontend..."
if curl -f -s https://jobs.bluehawana.com > /dev/null 2>&1; then
    print_success "Frontend is accessible!"
else
    print_warning "Frontend not accessible"
fi

# Cleanup
print_header "Cleanup"
print_info "Removing local package..."
rm -f "$PACKAGE_NAME"
print_success "Cleanup complete"

# Summary
print_header "✅ Deployment Summary"
echo ""
echo "Deployed to: $VPS_USER@$VPS_HOST:$VPS_PORT"
echo "Package: $PACKAGE_NAME"
echo "Timestamp: $TIMESTAMP"
echo ""
echo "Verify deployment:"
echo "  Frontend: https://jobs.bluehawana.com"
echo "  Health:   https://jobs.bluehawana.com/api/health"
echo "  API:      https://jobs.bluehawana.com/api/analyze-job"
echo ""
echo "View logs:"
echo "  ssh -p $VPS_PORT $VPS_USER@$VPS_HOST"
echo "  sudo journalctl -u $VPS_SERVICE -f"
echo ""
print_success "All fixes have been deployed to production!"
echo ""
