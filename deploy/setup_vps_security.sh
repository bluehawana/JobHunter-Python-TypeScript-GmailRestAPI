#!/bin/bash
# VPS Security Setup with Tailscale
# Run this as ROOT on your VPS first
# Usage: ssh root@jobs.bluehawana.com 'bash -s' < deploy/setup_vps_security.sh

set -e

echo "🔒 Setting up VPS Security with Tailscale"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "⚠️  Please run as root"
   exit 1
fi

# Step 1: Install Tailscale
echo "Step 1: Installing Tailscale..."
echo "--------------------------------"
if command -v tailscale &> /dev/null; then
    echo "✅ Tailscale already installed"
else
    curl -fsSL https://tailscale.com/install.sh | sh
    echo "✅ Tailscale installed"
fi
echo ""

# Step 2: Start Tailscale
echo "Step 2: Starting Tailscale with SSH..."
echo "---------------------------------------"
echo "⚠️  You'll need to visit the authentication URL"
tailscale up --ssh || true
echo ""

# Step 3: Create admin user
echo "Step 3: Creating admin user..."
echo "------------------------------"
if id "admin" &>/dev/null; then
    echo "✅ User 'admin' already exists"
else
    adduser --gecos "" admin
    usermod -aG sudo admin
    echo "✅ User 'admin' created"
fi
echo ""

# Step 4: Setup firewall
echo "Step 4: Configuring firewall..."
echo "--------------------------------"
apt install ufw -y

# Default policies
ufw default deny incoming
ufw default allow outgoing

# IMPORTANT: Keep SSH open for now!
ufw allow 22/tcp comment 'SSH - will disable after Tailscale is verified'

# Allow Tailscale
ufw allow in on tailscale0
ufw allow in from 100.64.0.0/10

# Enable firewall
ufw --force enable

echo "✅ Firewall configured (SSH still open)"
echo "⚠️  SSH port 22 is still open for safety"
echo ""

# Step 5: Display Tailscale IP
echo "Step 5: Getting Tailscale IP..."
echo "--------------------------------"
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "Not available yet")
echo "📍 Your Tailscale IP: $TAILSCALE_IP"
echo ""

# Step 6: Optional - Disable traditional SSH
echo "Step 6: Disable traditional SSH? (optional)"
echo "--------------------------------------------"
echo "⚠️  This will close port 22 to the public"
echo "   You'll only be able to connect via Tailscale SSH"
echo ""
read -p "Disable traditional SSH? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl disable --now ssh
    echo "✅ Traditional SSH disabled"
else
    echo "⏭️  Keeping traditional SSH enabled"
fi
echo ""

echo "🎉 VPS SECURITY SETUP COMPLETE!"
echo ""
echo "📝 Next Steps:"
echo "   1. Install Tailscale on your local machine"
echo "   2. Connect: tailscale ssh admin@$TAILSCALE_IP"
echo "   3. Run: deploy/install_openclaw_ai.sh"
echo ""
echo "🔒 Security Status:"
ufw status numbered
echo ""
echo "🌐 Tailscale Status:"
tailscale status
echo ""
