#!/bin/bash
# Final deployment script - run this on the server

set -e

echo "🚀 Completing LEGO Job Generator deployment..."

# Verify Node.js version
NODE_VERSION=$(node --version)
echo "✅ Node.js version: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v1[8-9]\. ]] && [[ ! "$NODE_VERSION" =~ ^v2[0-9]\. ]]; then
    echo "❌ Node.js version must be 18 or higher"
    exit 1
fi

# Navigate to application directory
cd /var/www/lego-job-generator

echo "📁 Current directory: $(pwd)"
echo "📦 Files present:"
ls -la

# Setup backend
echo ""
echo "🐍 Setting up Python backend..."
cd backend

# Verify backend files
if [ ! -f "lego_app.py" ]; then
    echo "❌ lego_app.py not found!"
    exit 1
fi

# Create/activate virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install flask flask-cors gunicorn

# Create requirements.txt
cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
EOF

deactivate

echo "✅ Backend setup complete"

# Setup frontend
echo ""
echo "⚛️ Building React frontend..."
cd ../frontend

# Verify frontend files
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found!"
    exit 1
fi

# Clean and rebuild
rm -rf node_modules package-lock.json build
npm install
npm run build

if [ ! -d "build" ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

echo "✅ Frontend build complete"

# Create systemd service
echo ""
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

echo "✅ Systemd service created"

# Configure Nginx
echo ""
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/jobs.bluehawana.com > /dev/null << 'EOF'
server {
    listen 80;
    server_name jobs.bluehawana.com 94.72.141.71;

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
sudo ln -sf /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "✅ Testing Nginx configuration..."
sudo nginx -t

# Create directory for generated PDFs
echo ""
echo "📁 Creating output directory..."
mkdir -p /var/www/lego-job-generator/backend/generated_applications
chmod 755 /var/www/lego-job-generator/backend/generated_applications

# Start services
echo ""
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable lego-backend
sudo systemctl start lego-backend
sudo systemctl restart nginx

# Wait a moment for services to start
sleep 3

# Check status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
sudo systemctl status lego-backend --no-pager || true
echo ""
echo "🌐 Nginx Status:"
sudo systemctl status nginx --no-pager || true
echo ""
echo "🔍 Testing services..."
echo ""
echo "Backend health check:"
curl -s http://localhost:5000/health || echo "⚠️  Backend not responding yet (may need a moment to start)"
echo ""
echo "Frontend check:"
curl -s -I http://localhost | head -n 1 || echo "⚠️  Frontend not responding"
echo ""
echo "🔗 Your application should now be running at:"
echo "   http://94.72.141.71"
echo "   http://jobs.bluehawana.com (after DNS is configured)"
echo ""
echo "📝 Useful commands:"
echo "   sudo systemctl status lego-backend    # Check backend status"
echo "   sudo systemctl restart lego-backend   # Restart backend"
echo "   sudo journalctl -u lego-backend -f    # View backend logs"
echo "   sudo tail -f /var/log/nginx/error.log # View nginx errors"
echo ""
echo "🎉 Happy job hunting with LEGO bricks!"
