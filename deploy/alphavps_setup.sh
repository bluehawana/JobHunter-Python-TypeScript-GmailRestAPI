#!/bin/bash
# 🧱 LEGO Bricks Job Generator - AlphaVPS Deployment Script
# This script sets up the application on AlphaVPS for 24/7 operation

set -e

echo "🚀 Starting AlphaVPS deployment for jobs.bluehawana.com..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "📦 Installing dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    nginx \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    supervisor \
    git \
    certbot \
    python3-certbot-nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/lego-job-generator
sudo chown -R $USER:$USER /var/www/lego-job-generator

# Clone or copy application
echo "📥 Setting up application files..."
cd /var/www/lego-job-generator

# Create backend virtual environment
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors gunicorn

# Create requirements.txt if not exists
cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
EOF

pip install -r requirements.txt
deactivate

# Setup frontend
echo "⚛️ Setting up React frontend..."
cd ../frontend
npm install
npm run build

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
sudo ln -sf /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "✅ Testing Nginx configuration..."
sudo nginx -t

# Create directory for generated PDFs
echo "📁 Creating output directory..."
mkdir -p /var/www/lego-job-generator/backend/generated_applications
chmod 755 /var/www/lego-job-generator/backend/generated_applications

# Setup log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/lego-job-generator > /dev/null << EOF
/var/www/lego-job-generator/backend/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 $USER $USER
    sharedscripts
}
EOF

# Setup automatic cleanup of old PDFs (keep last 7 days)
echo "🧹 Setting up automatic cleanup..."
(crontab -l 2>/dev/null; echo "0 2 * * * find /var/www/lego-job-generator/backend/generated_applications -type d -mtime +7 -exec rm -rf {} +") | crontab -

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable lego-backend
sudo systemctl start lego-backend
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
echo "🔒 Setting up SSL certificate..."
read -p "Do you want to setup SSL with Let's Encrypt? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo certbot --nginx -d jobs.bluehawana.com --non-interactive --agree-tos --email hongzhili01@gmail.com --redirect
fi

# Setup monitoring with supervisor (optional)
echo "📊 Setting up process monitoring..."
sudo tee /etc/supervisor/conf.d/lego-backend.conf > /dev/null << EOF
[program:lego-backend]
command=/var/www/lego-job-generator/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 lego_app:app
directory=/var/www/lego-job-generator/backend
user=$USER
autostart=true
autorestart=true
stderr_logfile=/var/log/lego-backend.err.log
stdout_logfile=/var/log/lego-backend.out.log
EOF

sudo supervisorctl reread
sudo supervisorctl update

# Check status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
sudo systemctl status lego-backend --no-pager
echo ""
echo "🌐 Nginx Status:"
sudo systemctl status nginx --no-pager
echo ""
echo "🔗 Your application should now be running at:"
echo "   http://jobs.bluehawana.com"
echo "   https://jobs.bluehawana.com (if SSL was configured)"
echo ""
echo "📝 Useful commands:"
echo "   sudo systemctl status lego-backend    # Check backend status"
echo "   sudo systemctl restart lego-backend   # Restart backend"
echo "   sudo systemctl restart nginx          # Restart nginx"
echo "   sudo journalctl -u lego-backend -f    # View backend logs"
echo "   sudo tail -f /var/log/nginx/error.log # View nginx errors"
echo ""
echo "🎉 Happy job hunting with LEGO bricks!"
