#!/bin/bash
# 🔧 Fix Node.js Upgrade Conflict on AlphaVPS
# This script removes old Node.js packages and installs Node.js 18

set -e

echo "🔧 Fixing Node.js upgrade conflict..."

# Step 1: Remove ALL old Node.js packages completely
echo "📦 Removing old Node.js packages..."
sudo apt-get remove -y nodejs libnode72 libnode-dev nodejs-doc 2>/dev/null || true
sudo apt-get autoremove -y
sudo apt-get clean

# Step 2: Remove any leftover Node.js files
echo "🧹 Cleaning up leftover files..."
sudo rm -rf /usr/lib/node_modules
sudo rm -rf /usr/share/nodejs
sudo rm -rf /usr/share/systemtap/tapset/node.stp

# Step 3: Verify NodeSource repository is configured
echo "📦 Verifying NodeSource repository..."
if [ ! -f /etc/apt/sources.list.d/nodesource.list ]; then
    echo "⚠️  NodeSource repository not found. Adding it..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
fi

# Step 4: Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Step 5: Install Node.js 18 fresh
echo "📦 Installing Node.js 18..."
sudo apt-get install -y nodejs

# Step 6: Verify installation
echo ""
echo "✅ Node.js upgrade complete!"
echo ""
echo "📊 Installed versions:"
node --version
npm --version
echo ""

# Step 7: Install global npm packages if needed
echo "📦 Installing global npm packages..."
sudo npm install -g npm@latest

echo ""
echo "🎉 Node.js is now ready!"
echo ""
echo "Next steps:"
echo "  1. cd /var/www/lego-job-generator/frontend"
echo "  2. rm -rf node_modules package-lock.json"
echo "  3. npm install"
echo "  4. npm run build"
