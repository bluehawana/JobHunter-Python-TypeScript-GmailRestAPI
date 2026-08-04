#!/bin/bash
# Install OpenClaw AI Assistant on VPS with Tailscale
# Based on: https://dev.to/nunc/self-hosting-openclaw-ai-assistant-on-a-vps-with-tailscale-vpn-zero-public-ports-35fn
# Usage: Run this script on your VPS after Tailscale is set up

set -e

echo "🦞 Installing OpenClaw AI Assistant"
echo "===================================="
echo ""

# Check if running as non-root
if [ "$EUID" -eq 0 ]; then 
   echo "⚠️  Please run as non-root user (e.g., admin)"
   echo "   Example: su - admin"
   exit 1
fi

# Step 1: Install Node.js 22+
echo "Step 1: Installing Node.js 22..."
echo "--------------------------------"
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
NODE_VERSION=$(node --version)
echo "✅ Node.js installed: $NODE_VERSION"
echo ""

# Step 2: Install pnpm
echo "Step 2: Installing pnpm..."
echo "--------------------------"
curl -fsSL https://get.pnpm.io/install.sh | sh -
export PNPM_HOME="$HOME/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
source ~/.bashrc 2>/dev/null || true
PNPM_VERSION=$(pnpm --version 2>/dev/null || echo "installing...")
echo "✅ pnpm installed: $PNPM_VERSION"
echo ""

# Step 3: Clone OpenClaw
echo "Step 3: Cloning OpenClaw repository..."
echo "---------------------------------------"
mkdir -p ~/GIT
cd ~/GIT

if [ -d "openclaw" ]; then
    echo "⚠️  OpenClaw directory exists, updating..."
    cd openclaw
    git pull origin main
else
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
fi

echo "✅ Repository ready"
echo ""

# Step 4: Install dependencies and build
echo "Step 4: Installing dependencies and building..."
echo "-----------------------------------------------"
pnpm install
pnpm ui:build
pnpm build

echo "✅ Build complete"
echo ""

# Step 5: Run onboard wizard
echo "Step 5: Running onboard wizard..."
echo "---------------------------------"
pnpm openclaw onboard \
  --non-interactive \
  --accept-risk \
  --flow quickstart \
  --mode local \
  --skip-channels \
  --skip-skills \
  --install-daemon

echo "✅ Onboarding complete"
echo ""

# Step 6: Enable lingering for systemd user service
echo "Step 6: Enabling systemd user service..."
echo "-----------------------------------------"
sudo loginctl enable-linger $USER

echo "✅ User service enabled"
echo ""

# Step 7: Check gateway status
echo "Step 7: Checking gateway status..."
echo "-----------------------------------"
sleep 2
pnpm openclaw gateway status

echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo ""
echo "📝 Next Steps:"
echo "   1. Get a Kimi Code API key from: https://kimi.com/code"
echo "   2. Configure OpenClaw: pnpm openclaw config"
echo "   3. Or use: pnpm openclaw onboard --kimi-code-api-key 'YOUR_KEY'"
echo ""
echo "🌐 Access Dashboard:"
echo "   From your local machine, create SSH tunnel:"
echo "   tailscale ssh -L 18789:localhost:18789 $USER@\$(tailscale ip -4)"
echo "   Then open: http://localhost:18789"
echo ""
echo "🔧 Useful Commands:"
echo "   pnpm openclaw gateway status    # Check status"
echo "   pnpm openclaw gateway restart   # Restart gateway"
echo "   pnpm openclaw logs              # View logs"
echo "   pnpm openclaw agent --message 'Hello!' # Test"
echo ""
echo "📍 Configuration: ~/.openclaw/openclaw.json"
echo "📍 Workspace: ~/.openclaw/workspace/"
echo ""
