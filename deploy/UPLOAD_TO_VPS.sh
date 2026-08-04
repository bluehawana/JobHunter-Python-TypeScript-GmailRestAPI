#!/bin/bash
# 📦 Upload Project to AlphaVPS Script
# Run this from your Mac to upload the complete project

set -e

echo "📦 Uploading JobHunter project to AlphaVPS..."

# Check if SSH config alias exists
if grep -q "Host alphavps" ~/.ssh/config 2>/dev/null; then
    echo "✓ Using SSH config alias 'alphavps'"
    VPS_ALIAS="alphavps"
    SSH_CMD="ssh $VPS_ALIAS"
    VPS_TARGET="alphavps"
else
    echo "⚠ SSH config alias not found, using direct connection"
    VPS_HOST="94.72.141.71"
    VPS_PORT="1025"
    VPS_USER="harvad"
    VPS_TARGET="$VPS_USER@$VPS_HOST"
    SSH_CMD="ssh -p $VPS_PORT $VPS_TARGET"
fi

VPS_PATH="/tmp/JobHunter-Python-TypeScript-GmailRestAPI"

# Current project directory
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "📁 Project directory: $PROJECT_DIR"
echo "🌐 Target VPS: $VPS_TARGET"
echo ""

echo "📦 Creating compressed archive..."
echo "⏳ This may take a minute..."

# Create temporary tarball (faster upload than individual files)
TEMP_TAR="/tmp/jobhunter-deploy-$(date +%s).tar.gz"

tar czf "$TEMP_TAR" \
  --exclude='.git' \
  --exclude='.hypothesis' \
  --exclude='.pytest_cache' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='.Python' \
  --exclude='env' \
  --exclude='venv' \
  --exclude='ENV' \
  --exclude='build' \
  --exclude='dist' \
  --exclude='*.egg-info' \
  --exclude='.DS_Store' \
  --exclude='.env' \
  --exclude='node_modules' \
  --exclude='frontend/build' \
  --exclude='backend/generated_applications' \
  --exclude='*.log' \
  --exclude='*.aux' \
  --exclude='*.out' \
  --exclude='*.pdf' \
  --exclude='.idea' \
  --exclude='.vscode' \
  --exclude='.kiro' \
  -C "$PROJECT_DIR" .

echo "✓ Archive created: $(du -h "$TEMP_TAR" | cut -f1)"
echo ""

echo "📤 Uploading to VPS..."
scp "$TEMP_TAR" "$VPS_TARGET:/tmp/jobhunter-deploy.tar.gz"

echo ""
echo "📂 Extracting files on VPS..."
$SSH_CMD "mkdir -p $VPS_PATH && tar xzf /tmp/jobhunter-deploy.tar.gz -C $VPS_PATH && rm /tmp/jobhunter-deploy.tar.gz"

# Clean up local tarball
rm "$TEMP_TAR"

echo ""
echo "✅ Upload complete!"
echo ""
echo "📝 Next steps:"
echo "1. SSH into VPS: $SSH_CMD"
echo "2. Run this one-liner:"
echo ""
echo "sudo mv $VPS_PATH /root/ && cd /root/JobHunter-Python-TypeScript-GmailRestAPI/deploy && chmod +x COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh && sudo ./COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh"
echo ""
