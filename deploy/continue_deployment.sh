#!/bin/bash
# Continue deployment after Node.js upgrade

set -e

echo "🚀 Continuing deployment after Node.js upgrade..."

# Navigate to application directory
cd /var/www/lego-job-generator

# Copy backend files if not already there
echo "📁 Ensuring backend files are in place..."
if [ -d ~/backend ]; then
    echo "Copying backend files from home directory..."
    cp -r ~/backend/* backend/ 2>/dev/null || true
fi

# Setup backend virtual environment
echo "🐍 Setting up Python backend..."
cd backend

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install flask flask-cors gunicorn

# Create requirements.txt
cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
EOF

deactivate

# Setup frontend
echo "⚛️ Building React frontend..."
cd ../frontend

# Copy frontend files if not already there
if [ -d ~/frontend ]; then
    echo "Copying frontend files from home directory..."
    cp -r ~/frontend/* . 2>/dev/null || true
fi

# Clean and rebuild
rm -rf node_modules package-lock.json build
npm install
npm run build

# Create systemd service
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
sudo ln -sf /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "✅ Testing Nginx configuration..."
sudo nginx -t

# Create directory for generated PDFs
echo "📁 Creating output directory..."
mkdir -p /var/www/lego-job-generator/backend/generated_applications
chmod 755 /var/www/lego-job-generator/backend/generated_applications

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable lego-backend
sudo systemctl start lego-backend
sudo systemctl restart nginx

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
echo "Backend health check:"
curl -s http://localhost:5000/health || echo "Backend not responding yet (may need to wait a moment)"
echo ""
echo "Frontend check:"
curl -s -I http://localhost | head -n 1 || echo "Frontend not responding"
echo ""
echo "🔗 Your application should now be running at:"
echo "   http://jobs.bluehawana.com"
echo ""
echo "📝 Useful commands:"
echo "   sudo systemctl status lego-backend    # Check backend status"
echo "   sudo systemctl restart lego-backend   # Restart backend"
echo "   sudo journalctl -u lego-backend -f    # View backend logs"
echo "   sudo tail -f /var/log/nginx/error.log # View nginx errors"
echo ""
echo "🎉 Happy job hunting with LEGO bricks!"
