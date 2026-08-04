# 🚀 Quick Redeployment Guide for jobs.bluehawana.com

## Context
Your AlphaVPS was reinstalled with a fresh Debian OS. This guide will help you get jobs.bluehawana.com back online.

## Prerequisites
- Fresh Debian installation on VPS (94.72.141.71)
- SSH access: `ssh -p 1025 harvad@94.72.141.71`
- Your project files on local machine

---

## Option 1: Automated Deployment (Recommended)

### Step 1: Upload Project Files
From your local Mac terminal:

```bash
cd ~/Projects
scp -P 1025 -r JobHunter-Python-TypeScript-GmailRestAPI/ harvad@94.72.141.71:/tmp/
```

### Step 2: SSH into VPS
```bash
ssh -p 1025 harvad@94.72.141.71
```

### Step 3: Move Files and Run Script
```bash
sudo mv /tmp/JobHunter-Python-TypeScript-GmailRestAPI /root/
cd /root/JobHunter-Python-TypeScript-GmailRestAPI/deploy
chmod +x COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh
sudo ./COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh
```

### Step 4: Update API Keys
```bash
nano /root/JobHunter-Python-TypeScript-GmailRestAPI/.env
```

Update with your actual keys:
- `ANTHROPIC_API_KEY=your_actual_key`
- `SCRAPERAPI_KEY=your_actual_key`

Save and restart:
```bash
sudo systemctl restart lego-api
```

---

## Option 2: Manual Deployment (Step by Step)

If the automated script fails, follow these manual steps:

### 1. System Setup
```bash
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm nginx \
    texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
    git certbot python3-certbot-nginx
```

### 2. Setup Application Directory
```bash
sudo mkdir -p /root/JobHunter-Python-TypeScript-GmailRestAPI
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
```

Upload your files using scp from your Mac.

### 3. Backend Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install flask flask-cors gunicorn
deactivate
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. Create Systemd Service
```bash
sudo nano /etc/systemd/system/lego-api.service
```

Paste this content:
```ini
[Unit]
Description=LEGO API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/JobHunter-Python-TypeScript-GmailRestAPI/backend/app
Environment="PATH=/root/JobHunter-Python-TypeScript-GmailRestAPI/venv/bin"
ExecStart=/root/JobHunter-Python-TypeScript-GmailRestAPI/venv/bin/python3 lego_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/jobs.bluehawana.com
```

Paste this content:
```nginx
server {
    listen 80;
    server_name jobs.bluehawana.com;

    location / {
        root /root/JobHunter-Python-TypeScript-GmailRestAPI/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    client_max_body_size 10M;
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/jobs.bluehawana.com /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
```

### 7. Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable lego-api
sudo systemctl start lego-api
sudo systemctl restart nginx
```

### 8. Setup SSL
```bash
sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect
```

---

## Verification

### Check Service Status
```bash
# Check API
sudo systemctl status lego-api
sudo journalctl -u lego-api -n 50

# Check Nginx
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

### Test API
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Test External Access
From your Mac:
```bash
curl https://jobs.bluehawana.com/api/health
```

---

## Troubleshooting

### API Won't Start
```bash
# Check logs
sudo journalctl -u lego-api -n 100

# Check if port 8000 is in use
sudo lsof -i :8000

# Try manual start to see errors
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
source venv/bin/activate
cd backend/app
python3 lego_api.py
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

### Frontend Not Loading
```bash
# Check if build exists
ls -la /root/JobHunter-Python-TypeScript-GmailRestAPI/frontend/build/

# Rebuild if needed
cd /root/JobHunter-Python-TypeScript-GmailRestAPI/frontend
npm run build
sudo systemctl reload nginx
```

### PDF Generation Fails
```bash
# Check LaTeX installation
which pdflatex

# Test LaTeX
echo '\documentclass{article}\begin{document}Test\end{document}' > test.tex
pdflatex test.tex
```

---

## Maintenance Commands

### Update Application
```bash
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
git pull origin main  # If using git
sudo systemctl restart lego-api
```

### View Logs
```bash
# API logs (real-time)
sudo journalctl -u lego-api -f

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Restart Services
```bash
sudo systemctl restart lego-api
sudo systemctl restart nginx
```

### Check Disk Space
```bash
df -h
du -sh /root/JobHunter-Python-TypeScript-GmailRestAPI/backend/generated_applications/*
```

---

## Security Checklist

- [ ] Firewall configured (ports 80, 443, 1025)
- [ ] SSL certificate installed
- [ ] .env file has correct API keys
- [ ] Regular backups configured
- [ ] Automatic SSL renewal tested

```bash
# Setup firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 1025/tcp
sudo ufw enable

# Test SSL renewal
sudo certbot renew --dry-run
```

---

## Success Indicators

✅ `sudo systemctl status lego-api` shows "active (running)"  
✅ `curl http://localhost:8000/health` returns `{"status":"healthy"}`  
✅ `curl https://jobs.bluehawana.com/api/health` returns `{"status":"healthy"}`  
✅ Website loads at https://jobs.bluehawana.com  
✅ Can generate CV/CL successfully  

---

## Support

If you encounter issues:
1. Check the logs: `sudo journalctl -u lego-api -n 100`
2. Verify Nginx config: `sudo nginx -t`
3. Test API locally: `curl http://localhost:8000/health`
4. Review this guide's troubleshooting section

---

## Next Steps After Deployment

1. Test job application generation
2. Verify PDF compilation works
3. Check Cloudflare DNS settings point to 94.72.141.71
4. Setup monitoring/alerts (optional)
5. Configure automatic backups (optional)

---

**Last Updated:** August 4, 2026  
**Server:** AlphaVPS (94.72.141.71:1025)  
**Domain:** jobs.bluehawana.com
