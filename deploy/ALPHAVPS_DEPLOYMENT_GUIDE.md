# 🚀 AlphaVPS Deployment Guide - jobs.bluehawana.com

## Server Details
- **Host:** 94.72.141.71
- **Port:** 1025
- **User:** harvad
- **Domain:** jobs.bluehawana.com

## Quick Deployment

### Step 1: Connect to Server
```bash
ssh -p 1025 harvad@94.72.141.71
```

### Step 2: Upload Application Files
From your local machine:
```bash
# Create deployment package
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI
tar -czf lego-app.tar.gz \
    frontend/src/pages/LegoJobGenerator.tsx \
    frontend/src/styles/LegoJobGenerator.css \
    frontend/package.json \
    frontend/public \
    backend/app/lego_api.py \
    backend/lego_app.py \
    backend/gemini_content_polisher.py \
    backend/smart_latex_editor.py \
    deploy/

# Upload to server
scp -P 1025 lego-app.tar.gz harvad@94.72.141.71:~/
scp -P 1025 deploy/alphavps_setup.sh harvad@94.72.141.71:~/
```

### Step 3: Run Deployment Script
On the server:
```bash
ssh -p 1025 harvad@94.72.141.71

# Extract files
tar -xzf lego-app.tar.gz
chmod +x deploy/alphavps_setup.sh

# Run deployment
cd deploy
./alphavps_setup.sh
```

## Manual Deployment (Step by Step)

### 1. System Setup
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3 python3-pip python3-venv \
    nodejs npm \
    nginx \
    texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
    supervisor git certbot python3-certbot-nginx
```

### 2. Create Application Directory
```bash
sudo mkdir -p /var/www/lego-job-generator
sudo chown -R harvad:harvad /var/www/lego-job-generator
cd /var/www/lego-job-generator
```

### 3. Setup Backend
```bash
# Create backend structure
mkdir -p backend/app
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install flask flask-cors gunicorn

# Create requirements.txt
cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
EOF

# Copy backend files
# (Upload lego_app.py, app/lego_api.py, etc.)

deactivate
```

### 4. Setup Frontend
```bash
cd /var/www/lego-job-generator/frontend

# Install dependencies
npm install

# Build production version
npm run build
```

### 5. Configure Systemd Service
```bash
sudo nano /etc/systemd/system/lego-backend.service
```

Add:
```ini
[Unit]
Description=LEGO Bricks Job Generator Backend
After=network.target

[Service]
Type=simple
User=harvad
WorkingDirectory=/var/www/lego-job-generator/backend
Environment="PATH=/var/www/lego-job-generator/backend/venv/bin"
ExecStart=/var/www/lego-job-generator/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 lego_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lego-backend
sudo systemctl start lego-backend
sudo systemctl status lego-backend
```

### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/jobs.bluehawana.com
```

Add:
```nginx
server {
    listen 80;
    server_name jobs.bluehawana.com;

    # Frontend
    location / {
        root /var/www/lego-job-generator/frontend/build;
        try_files $uri $uri/ /index.html;
        
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
        
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    client_max_body_size 10M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Setup SSL Certificate
```bash
sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect
```

### 8. Setup Automatic Cleanup
```bash
# Clean old PDFs every day at 2 AM
crontab -e
```

Add:
```
0 2 * * * find /var/www/lego-job-generator/backend/generated_applications -type d -mtime +7 -exec rm -rf {} +
```

### 9. Setup Monitoring
```bash
# Create health check script
nano /var/www/lego-job-generator/health_check.sh
```

Add health check script content, then:
```bash
chmod +x /var/www/lego-job-generator/health_check.sh

# Run health check every 5 minutes
crontab -e
```

Add:
```
*/5 * * * * /var/www/lego-job-generator/health_check.sh >> /var/log/lego-health.log 2>&1
```

## DNS Configuration

Point your domain to the server:
```
A Record: jobs.bluehawana.com → 94.72.141.71
```

## Firewall Configuration

```bash
# Allow HTTP, HTTPS, and SSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 1025/tcp
sudo ufw enable
```

## Useful Commands

### Service Management
```bash
# Check backend status
sudo systemctl status lego-backend

# Restart backend
sudo systemctl restart lego-backend

# View backend logs
sudo journalctl -u lego-backend -f

# Restart nginx
sudo systemctl restart nginx

# Check nginx status
sudo systemctl status nginx
```

### Debugging
```bash
# Test backend API directly
curl http://localhost:5000/health

# Test frontend
curl http://localhost

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check backend logs
sudo journalctl -u lego-backend -n 100

# Check disk space
df -h

# Check running processes
ps aux | grep gunicorn
```

### Updates
```bash
# Pull latest changes
cd /var/www/lego-job-generator
git pull origin main  # if using git

# Update backend
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
deactivate
sudo systemctl restart lego-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

### Backup
```bash
# Backup application
tar -czf lego-backup-$(date +%Y%m%d).tar.gz /var/www/lego-job-generator

# Backup database (if any)
# pg_dump or mysqldump commands here
```

## Monitoring & Maintenance

### Daily Checks
- [ ] Check service status: `sudo systemctl status lego-backend nginx`
- [ ] Check disk space: `df -h`
- [ ] Check error logs: `sudo journalctl -u lego-backend --since today`

### Weekly Checks
- [ ] Review generated PDFs count
- [ ] Check SSL certificate expiry: `sudo certbot certificates`
- [ ] Update system packages: `sudo apt-get update && sudo apt-get upgrade`

### Monthly Checks
- [ ] Review and clean old logs
- [ ] Check for security updates
- [ ] Test backup restoration

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u lego-backend -n 50

# Check if port is in use
sudo lsof -i :5000

# Test manually
cd /var/www/lego-job-generator/backend
source venv/bin/activate
python lego_app.py
```

### PDF Generation Fails
```bash
# Check if pdflatex is installed
which pdflatex

# Test pdflatex
echo '\documentclass{article}\begin{document}Test\end{document}' > test.tex
pdflatex test.tex

# Check permissions
ls -la /var/www/lego-job-generator/backend/generated_applications
```

### Nginx 502 Bad Gateway
```bash
# Check if backend is running
sudo systemctl status lego-backend

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test backend directly
curl http://localhost:5000/health
```

### SSL Certificate Issues
```bash
# Renew certificate manually
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

## Performance Optimization

### Enable Gzip Compression
Add to nginx config:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### Enable Caching
Add to nginx config:
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Increase Worker Processes
In `/etc/systemd/system/lego-backend.service`:
```ini
ExecStart=/var/www/lego-job-generator/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 lego_app:app
```

## Security Best Practices

1. **Keep system updated**
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

2. **Use strong SSH keys** (disable password auth)
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   ```

3. **Enable fail2ban**
   ```bash
   sudo apt-get install fail2ban
   sudo systemctl enable fail2ban
   ```

4. **Regular backups**
   - Automated daily backups
   - Store offsite

5. **Monitor logs**
   - Set up log monitoring
   - Alert on errors

## Support

For issues:
- Check logs: `sudo journalctl -u lego-backend -f`
- Run health check: `./health_check.sh`
- Email: hongzhili01@gmail.com

## Success Checklist

- [ ] Server accessible via SSH
- [ ] All dependencies installed
- [ ] Backend service running
- [ ] Nginx configured and running
- [ ] SSL certificate installed
- [ ] Domain pointing to server
- [ ] Application accessible at https://jobs.bluehawana.com
- [ ] PDF generation working
- [ ] Automatic cleanup configured
- [ ] Monitoring setup
- [ ] Backups configured

---

**🎉 Once complete, your LEGO Bricks Job Generator will be running 24/7 at jobs.bluehawana.com!**
