#!/bin/bash
# Upgrade Node.js to v18 LTS on Ubuntu 22.04

set -e

echo "🔄 Upgrading Node.js to v18 LTS..."

# Remove old Node.js
echo "📦 Removing old Node.js..."
sudo apt-get remove -y nodejs npm libnode72 libnode-dev nodejs-doc 2>/dev/null || true
sudo apt-get autoremove -y

# Install Node.js v18 from NodeSource
echo "📥 Installing Node.js v18 from NodeSource..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
echo ""
echo "✅ Node.js upgraded successfully!"
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
echo ""
echo "🎯 Next steps:"
echo "1. cd /var/www/lego-job-generator/frontend"
echo "2. rm -rf node_modules package-lock.json build"
echo "3. npm install"
echo "4. npm run build"
