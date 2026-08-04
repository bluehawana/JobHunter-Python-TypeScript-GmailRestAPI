#!/bin/bash
# 🚀 Complete Redeployment Script for jobs.bluehawana.com
# Use this after OS reinstall on AlphaVPS

set -e  # Exit on any error

echo "🚀 Starting complete redeployment of jobs.bluehawana.com..."
echo "📅 Date: $(date)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# STEP 1: System Update & Dependencies
# ============================================
echo -e "${GREEN}[1/10] Updating system packages...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${GREEN}[2/10] Installing dependencies...${NC}"
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    nodejs \
    npm \
    nginx \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-xetex \
    git \
    curl \
    wget \
    certbot \
    python3-certbot-nginx

# ============================================
# STEP 2: Create Application Directory
# ============================================
echo -e "${GREEN}[3/10] Creating application directory...${NC}"
sudo mkdir -p /root/JobHunter-Python-TypeScript-GmailRestAPI
cd /root/JobHunter-Python-TypeScript-GmailRestAPI

# ============================================
# STEP 3: Clone Repository
# ============================================
echo -e "${GREEN}[4/10] Cloning repository...${NC}"
# Option 1: Clone from GitHub (if you have the repo there)
# git clone https://github.com/yourusername/JobHunter-Python-TypeScript-GmailRestAPI.git .

# Option 2: Upload files manually (recommended for now)
echo -e "${YELLOW}⚠️  Repository clone skipped - files need to be uploaded manually${NC}"
echo -e "${YELLOW}📦 Upload files using: scp -P 1025 -r ./JobHunter-Python-TypeScript-GmailRestAPI/ harvad@94.72.141.71:/root/${NC}"
echo ""
read -p "Press Enter after you've uploaded the files..."

# ============================================
# STEP 4: Setup Python Backend
# ============================================
echo -e "${GREEN}[5/10] Setting up Python backend...${NC}"
cd /root/JobHunter-Python-TypeScript-GmailRestAPI

python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Additional packages for LEGO API
pip install flask flask-cors gunicorn beautifulsoup4 requests anthropic

deactivate

# ============================================
# STEP 5: Setup Frontend
# ============================================
echo -e "${GREEN}[6/10] Setting up frontend...${NC}"
cd /root/JobHunter-Python-TypeScript-GmailRestAPI/frontend

# Update npm
sudo npm install -g n
sudo n stable

npm install
npm run build

# ============================================
# STEP 6: Create systemd Service
# ============================================
echo -e "${GREEN}[7/10] Creating systemd service...${NC}"

sudo tee /etc/systemd/system/lego-api.service > /dev/null << 'EOF'
[Unit]
Description=LEGO API Service for jobs.bluehawana.com
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/JobHunter-Python-TypeScript-GmailRestAPI/backend/app
Environment="PATH=/root/JobHunter-Python-TypeScript-GmailRestAPI/venv/bin"
EnvironmentFile=/root/JobHunter-Python-TypeScript-GmailRestAPI/.env
ExecStart=/root/JobHunter-Python-TypeScript-GmailRestAPI/venv/bin/python3 lego_api.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# ============================================
# STEP 7: Configure Nginx
# ============================================
echo -e "${GREEN}[8/10] Configuring Nginx...${NC}"

sudo tee /etc/nginx/sites-available/jobs.bluehawana.com > /dev/null << 'EOF'
server {
    listen 80;
    server_name jobs.bluehawana.com;

    # Frontend (React build)
    location / {
        root /root/JobHunter-Python-TypeScript-GmailRestAPI/frontend/build;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeouts for PDF generation
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Increase max body size
    client_max_body_size 10M;
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# ============================================
# STEP 8: Setup Environment Variables
# ============================================
echo -e "${GREEN}[9/10] Setting up environment variables...${NC}"

cat > /root/JobHunter-Python-TypeScript-GmailRestAPI/.env << 'EOF'
# API Keys (replace with your actual keys)
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
SCRAPERAPI_KEY=your_scraperapi_key_here

# Application Settings
FLASK_ENV=production
DEBUG=False
EOF

echo -e "${YELLOW}⚠️  Remember to update .env with your actual API keys!${NC}"

# ============================================
# STEP 9: Start Services
# ============================================
echo -e "${GREEN}[10/10] Starting services...${NC}"

# Reload systemd
sudo systemctl daemon-reload

# Enable and start lego-api
sudo systemctl enable lego-api
sudo systemctl start lego-api

# Restart nginx
sudo systemctl restart nginx

# ============================================
# STEP 10: Setup SSL (Optional but Recommended)
# ============================================
echo ""
echo -e "${YELLOW}Would you like to setup SSL with Let's Encrypt? (y/n)${NC}"
read -p "Answer: " setup_ssl

if [[ $setup_ssl == "y" || $setup_ssl == "Y" ]]; then
    echo -e "${GREEN}Setting up SSL certificate...${NC}"
    sudo certbot --nginx -d jobs.bluehawana.com --non-interactive --agree-tos --email hongzhili01@gmail.com --redirect
else
    echo -e "${YELLOW}SSL setup skipped. Run this later:${NC}"
    echo "sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect"
fi

# ============================================
# Verification
# ============================================
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Service Status:"
sudo systemctl status lego-api --no-pager
echo ""
sudo systemctl status nginx --no-pager
echo ""

echo -e "${GREEN}🧪 Testing local API...${NC}"
sleep 5
curl http://localhost:8000/health || echo -e "${RED}❌ API health check failed${NC}"

echo ""
echo -e "${GREEN}🌐 Your application should now be accessible at:${NC}"
echo "   http://jobs.bluehawana.com"
echo "   https://jobs.bluehawana.com (if SSL was configured)"
echo ""

echo -e "${YELLOW}📝 Useful Commands:${NC}"
echo "   Check API status:    sudo systemctl status lego-api"
echo "   Check API logs:      sudo journalctl -u lego-api -f"
echo "   Restart API:         sudo systemctl restart lego-api"
echo "   Check Nginx status:  sudo systemctl status nginx"
echo "   Check Nginx logs:    sudo tail -f /var/log/nginx/error.log"
echo ""

echo -e "${YELLOW}🔐 Security Recommendations:${NC}"
echo "1. Update .env with your actual API keys"
echo "2. Setup firewall: sudo ufw allow 80/tcp && sudo ufw allow 443/tcp && sudo ufw allow 1025/tcp && sudo ufw enable"
echo "3. Setup automatic SSL renewal: sudo certbot renew --dry-run"
echo ""

echo -e "${GREEN}🎉 Deployment finished successfully!${NC}"
