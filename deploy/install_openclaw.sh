#!/bin/bash
# Install OpenClaw on VPS
# Usage: ssh root@jobs.bluehawana.com 'bash -s' < deploy/install_openclaw.sh

set -e

echo "🎮 Installing OpenClaw on VPS"
echo "=============================="
echo ""

# Step 1: Install dependencies
echo "Step 1: Installing build dependencies..."
echo "----------------------------------------"
sudo apt-get update
sudo apt-get install -y \
    git \
    cmake \
    build-essential \
    libsdl2-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsdl2-image-dev \
    zlib1g-dev \
    libtinyxml-dev \
    libpng-dev

echo "✅ Dependencies installed"
echo ""

# Step 2: Clone OpenClaw repository
echo "Step 2: Cloning OpenClaw repository..."
echo "---------------------------------------"
cd /opt
if [ -d "OpenClaw" ]; then
    echo "⚠️  OpenClaw directory exists, removing..."
    sudo rm -rf OpenClaw
fi

sudo git clone https://github.com/pjasicek/OpenClaw.git
cd OpenClaw

echo "✅ Repository cloned"
echo ""

# Step 3: Build OpenClaw
echo "Step 3: Building OpenClaw..."
echo "----------------------------"
mkdir -p Build_Release
cd Build_Release

cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)

echo "✅ OpenClaw built successfully"
echo ""

# Step 4: Setup game data directory
echo "Step 4: Setting up game directory..."
echo "------------------------------------"
sudo mkdir -p /opt/openclaw
sudo cp -r ../Build_Release/* /opt/openclaw/

echo "✅ Game files copied"
echo ""

# Step 5: Create launch script
echo "Step 5: Creating launch script..."
echo "---------------------------------"
cat > /opt/openclaw/launch.sh << 'EOF'
#!/bin/bash
cd /opt/openclaw
./openclaw
EOF

chmod +x /opt/openclaw/launch.sh

echo "✅ Launch script created"
echo ""

echo "🎉 INSTALLATION COMPLETE!"
echo ""
echo "📝 Important Notes:"
echo "   - OpenClaw is installed in: /opt/openclaw"
echo "   - You need the original Captain Claw game assets (CLAW.REZ)"
echo "   - Place CLAW.REZ in /opt/openclaw/"
echo ""
echo "🎮 To run OpenClaw:"
echo "   cd /opt/openclaw && ./openclaw"
echo ""
echo "⚠️  Note: This is a VPS without GUI. You'll need:"
echo "   1. X11 forwarding: ssh -X root@jobs.bluehawana.com"
echo "   2. Or install a VNC server for remote desktop"
echo ""
