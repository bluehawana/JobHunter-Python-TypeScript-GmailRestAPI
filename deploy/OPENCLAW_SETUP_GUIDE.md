# OpenClaw AI Assistant Setup with Tailscale

Complete guide to install OpenClaw on your VPS with zero public ports using Tailscale VPN.

## Overview

- **VPS**: jobs.bluehawana.com (or your VPS IP)
- **Security**: Zero public ports, Tailscale VPN only
- **Cost**: ~$25/month (VPS + Kimi Code subscription)
- **Time**: ~30 minutes

---

## Part 1: VPS Setup (Run on VPS)

### Step 1: Initial SSH Connection

```bash
# Connect to your VPS (last time using public IP!)
ssh root@jobs.bluehawana.com
```

### Step 2: Install and Configure Tailscale

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale with SSH enabled
sudo tailscale up --ssh

# Visit the authentication URL shown and approve the device
```

### Step 3: Create Admin User

```bash
# Create non-root user
adduser admin

# Add to sudo group
usermod -aG sudo admin

# Set password when prompted
```

### Step 4: Lock Down Firewall

```bash
# Install UFW
apt install ufw -y

# Default deny all incoming
ufw default deny incoming
ufw default allow outgoing

# Allow only Tailscale subnet
ufw allow in on tailscale0
ufw allow in from 100.64.0.0/10

# Enable firewall
ufw --force enable

# Verify
ufw status
```

### Step 5: Disable Traditional SSH (Optional but Recommended)

```bash
# Since Tailscale SSH is now active, disable regular SSH
systemctl disable --now ssh

# This closes port 22 to the public internet
```

### Step 6: Get Your Tailscale IP

```bash
# Note this IP - you'll need it to connect
tailscale ip -4
```

Example output: `100.x.x.x`

---

## Part 2: Local Machine Setup

### Step 1: Install Tailscale on Your Local Machine

**Linux/WSL:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl start tailscaled
sudo tailscale up
```

**macOS:**
```bash
# Download from https://tailscale.com/download/mac
# Or use Homebrew:
brew install tailscale
sudo tailscale up
```

### Step 2: Fix WSL MTU Issue (WSL Users Only)

If SSH connections hang:

```bash
# Temporary fix
sudo ip link set dev tailscale0 mtu 1200

# Permanent fix - add to ~/.bashrc
echo 'sudo ip link set dev tailscale0 mtu 1200 2>/dev/null' >> ~/.bashrc
```

### Step 3: Test Tailscale Connection

```bash
# Ping your VPS
tailscale ping 100.x.x.x

# Should show successful pings
```

---

## Part 3: Install OpenClaw on VPS

### Step 1: Connect via Tailscale SSH

```bash
# From your local machine
tailscale ssh admin@100.x.x.x

# Or if you know the hostname
tailscale ssh admin@jobs-bluehawana
```

### Step 2: Run Installation Script

```bash
# Download the installation script
curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/deploy/install_openclaw_ai.sh -o install_openclaw.sh

# Or if you have it locally, copy it:
# From local machine:
scp deploy/install_openclaw_ai.sh admin@100.x.x.x:~/

# Make executable
chmod +x install_openclaw.sh

# Run it
./install_openclaw.sh
```

Or run it manually:

```bash
# Install Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -
source ~/.bashrc

# Clone OpenClaw
mkdir -p ~/GIT && cd ~/GIT
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Install and build
pnpm install
pnpm ui:build
pnpm build

# Run onboarding
pnpm openclaw onboard \
  --non-interactive \
  --accept-risk \
  --flow quickstart \
  --mode local \
  --skip-channels \
  --skip-skills \
  --install-daemon

# Enable systemd user service
sudo loginctl enable-linger $USER

# Check status
pnpm openclaw gateway status
```

---

## Part 4: Configure Kimi Code API

### Step 1: Get Kimi Code API Key

1. Go to https://kimi.com/code
2. Sign up or log in
3. Subscribe to a plan (~$19/month for Andante tier)
4. Go to API Keys section
5. Create new key and copy it

### Step 2: Configure OpenClaw

```bash
# On VPS, in ~/GIT/openclaw directory
cd ~/GIT/openclaw

# Interactive config
pnpm openclaw config
# Select: Model → Moonshot AI → Paste API key

# Or one-line config
pnpm openclaw onboard --kimi-code-api-key "YOUR_API_KEY_HERE"

# Restart gateway
pnpm openclaw gateway restart
```

### Step 3: Test It

```bash
# Send a test message
pnpm openclaw agent --message "Hello! What model are you?"

# Should get response from Kimi K2.5
```

---

## Part 5: Access the Dashboard

### Step 1: Create SSH Tunnel

From your local machine:

```bash
# Create tunnel to forward port 18789
tailscale ssh -L 18789:localhost:18789 admin@100.x.x.x

# Keep this terminal open
```

### Step 2: Get Gateway Token

In another terminal, connect to VPS:

```bash
tailscale ssh admin@100.x.x.x

# View the token
cat ~/.openclaw/openclaw.json | grep -A 2 '"auth"'
```

Copy the `token` value.

### Step 3: Open Dashboard

Open your browser:

```
http://localhost:18789/?token=YOUR_GATEWAY_TOKEN
```

You should see the OpenClaw dashboard!

---

## Useful Commands

### Gateway Management

```bash
# Check status
pnpm openclaw gateway status

# Restart
pnpm openclaw gateway restart

# Stop
pnpm openclaw gateway stop

# View logs
pnpm openclaw logs

# Health check
pnpm openclaw doctor
```

### Testing

```bash
# Send message via CLI
pnpm openclaw agent --message "Your message here"

# List models
pnpm openclaw models list

# Reconfigure
pnpm openclaw config
```

### Systemd Service

```bash
# Check service status
systemctl --user status openclaw-gateway

# View service logs
journalctl --user -u openclaw-gateway -f

# Restart service
systemctl --user restart openclaw-gateway
```

### Updating OpenClaw

```bash
cd ~/GIT/openclaw
git pull --rebase origin main
pnpm install
pnpm ui:build
pnpm build
pnpm openclaw gateway restart
```

---

## Troubleshooting

### Can't Connect via Tailscale SSH

```bash
# Check Tailscale status
tailscale status

# Check if VPS is online
tailscale ping 100.x.x.x

# WSL: Fix MTU
sudo ip link set dev tailscale0 mtu 1200
```

### Gateway Not Starting

```bash
# Check logs
pnpm openclaw logs

# Check systemd service
systemctl --user status openclaw-gateway

# Restart
pnpm openclaw gateway restart
```

### Dashboard Not Loading

```bash
# Verify tunnel is active
# On local machine, check if port is forwarded:
lsof -i :18789

# Verify gateway is running on VPS
pnpm openclaw gateway status

# Check token is correct
cat ~/.openclaw/openclaw.json | grep token
```

### Kimi API Not Working

```bash
# Verify API key is set
cat ~/.openclaw/openclaw.json | grep -i kimi

# Test with simple message
pnpm openclaw agent --message "test"

# Check quota at https://kimi.com/code
```

---

## Security Checklist

- [x] UFW firewall enabled (deny all except Tailscale)
- [x] Traditional SSH disabled
- [x] Root login disabled
- [x] OpenClaw gateway bound to localhost only
- [x] Dashboard access via SSH tunnel only
- [x] API key stored securely on server
- [x] Tailscale SSH enabled
- [x] No public ports exposed

---

## Architecture

```
┌─────────────────────────┐        ┌──────────────────────────┐
│   Your Machine          │        │   VPS (Ubuntu)           │
│                         │        │                          │
│  Browser ──SSH tunnel──────────────→ OpenClaw :18789        │
│                         │        │   └── Kimi K2.5 API      │
│  Terminal               │        │   └── Workspace          │
│   └── tailscale ssh ──────────────→ Shell access            │
│                         │        │                          │
│  Tailscale ◄──WireGuard──────────►  Tailscale              │
└─────────────────────────┘        └──────────────────────────┘
                                   🔒 ALL public ports CLOSED
```

---

## Configuration Files

- **Main config**: `~/.openclaw/openclaw.json`
- **Workspace**: `~/.openclaw/workspace/`
- **Systemd service**: `~/.config/systemd/user/openclaw-gateway.service`
- **Logs**: Check with `pnpm openclaw logs`

---

## Resources

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://openclaw.com/docs)
- [Tailscale](https://tailscale.com)
- [Kimi Code](https://kimi.com/code)
- [Original Guide](https://dev.to/nunc/self-hosting-openclaw-ai-assistant-on-a-vps-with-tailscale-vpn-zero-public-ports-35fn)

---

## Quick Start Summary

1. **VPS**: Install Tailscale, create admin user, lock firewall
2. **Local**: Install Tailscale, connect to VPS
3. **Install**: Run OpenClaw installation script
4. **Configure**: Add Kimi Code API key
5. **Access**: SSH tunnel + browser to localhost:18789

Total time: ~30 minutes
Total cost: ~$25/month (VPS + Kimi Code)
