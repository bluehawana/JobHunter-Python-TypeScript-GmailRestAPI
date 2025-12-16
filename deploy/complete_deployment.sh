#!/bin/bash
# 🚀 Complete AlphaVPS Deployment - After Node.js Fix
# Run this after fix_nodejs_upgrade.sh completes successfully

set -e

echo "🚀 Completing AlphaVPS deployment for jobs.bluehawana.com..."

# Verify Node.js version
echo "📊 Checking Node.js version..."
NODE_VERSION=$(node --version)
echo "Node.js version: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v(1[4-9]|[2-9][0-9]) ]]; then
    echo "❌ Error: Node.js version must be 14 or higher"
    echo "Current version: $NODE_VERSION"
    exit 1
fi

# Navigate to application directory
cd /var/www/lego-job-generator

# Build frontend
echo "⚛️ Building React frontend..."
cd frontend

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf node_modules package-lock.json build

# Install dependencies
echo "📦 Installing npm packages..."
npm install

# Build production version
echo "🏗️  Building production bundle..."
npm run build

if [ ! -d "build" ]; then
    echo "❌ Error: Frontend build failed - build directory not created"
    exit 1
fi

echo "✅ Frontend build complete!"

# Create systemd service for backend
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/lego-backend.service > /dev/null << EOF
[Unit]
Description=LEGO Bricks Job Generator Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/lego-job-generator/backend
Environment="PATH=/var/www/lego-job-generator/backend/venv/bin"
ExecStart=/var/www/lego-job-generator/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 lego_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/jobs.bluehawana.com > /dev/null << 'EOF'
server {
    listen 80;
    server_name jobs.bluehawana.com;

    # Frontend - React build
    location / {
        root /var/www/lego-job-generator/frontend/build;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeout for PDF generation
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Increase max body size for job descriptions
    client_max_body_size 10M;
}
EOF

# Enable site
echo "🔗 Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "✅ Testing Nginx configuration..."
sudo nginx -t

# Create directory for generated PDFs
echo "📁 Creating output directory..."
mkdir -p /var/www/lego-job-generator/backend/generated_applications
chmod 755 /var/www/lego-job-generator/backend/generated_applications

# Setup automatic cleanup of old PDFs (keep last 7 days)
echo "🧹 Setting up automatic cleanup..."
(crontab -l 2>/dev/null | grep -v "generated_applications"; echo "0 2 * * * find /var/www/lego-job-generator/backend/generated_applications -type d -mtime +7 -exec rm -rf {} + 2>/dev/null") | crontab -

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable lego-backend
sudo systemctl start lego-backend
sudo systemctl restart nginx

# Wait for services to start
sleep 3

# Check service status
echo ""
echo "📊 Service Status:"
echo ""
echo "Backend Service:"
sudo systemctl status lego-backend --no-pager | head -10
echo ""
echo "Nginx Service:"
sudo systemctl status nginx --no-pager | head -10
echo ""

# Test backend health
echo "🏥 Testing backend health..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ Backend is responding!"
else
    echo "⚠️  Backend health check failed"
fi

# Test frontend
echo "🌐 Testing frontend..."
if curl -s http://localhost > /dev/null; then
    echo "✅ Frontend is responding!"
else
    echo "⚠️  Frontend check failed"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔗 Your application is running at:"
echo "   http://jobs.bluehawana.com (HTTP)"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo ""
echo "1. Configure DNS A record:"
echo "   jobs.bluehawana.com → 94.72.141.71"
echo ""
echo "2. Setup SSL certificate (after DNS is configured):"
echo "   sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect"
echo ""
echo "3. Test the application:"
echo "   curl http://94.72.141.71"
echo "   curl http://94.72.141.71/api/health"
echo ""
echo "📝 Useful commands:"
echo "   sudo systemctl status lego-backend    # Check backend status"
echo "   sudo systemctl restart lego-backend   # Restart backend"
echo "   sudo journalctl -u lego-backend -f    # View backend logs"
echo "   sudo systemctl restart nginx          # Restart nginx"
echo "   sudo tail -f /var/log/nginx/error.log # View nginx errors"
echo ""
echo "🎉 Happy job hunting with LEGO bricks!"
