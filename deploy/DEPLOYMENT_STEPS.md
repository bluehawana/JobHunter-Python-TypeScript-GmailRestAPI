# 🚀 AlphaVPS Deployment - Step by Step Instructions

## Current Status
✅ Files uploaded to server  
✅ Files extracted to home directory  
✅ System packages updated  
✅ Dependencies installed (Python, Nginx, LaTeX, etc.)  
⚠️ Node.js v12.22.9 (too old - needs upgrade to v18)  
⏳ Frontend build pending  
⏳ Services configuration pending  

## Next Steps to Complete Deployment

### Step 1: Upload New Scripts to Server

From your **local machine**, run:

```bash
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI

# Upload the new deployment scripts
scp -P 1025 deploy/upgrade_nodejs.sh harvad@94.72.141.71:~/
scp -P 1025 deploy/continue_deployment.sh harvad@94.72.141.71:~/
```

### Step 2: Connect to Server

```bash
ssh -p 1025 harvad@94.72.141.71
```

### Step 3: Upgrade Node.js to v18

On the **server**, run:

```bash
# Make script executable
chmod +x ~/upgrade_nodejs.sh

# Run upgrade script
./upgrade_nodejs.sh
```

Expected output:
```
🔄 Upgrading Node.js to v18 LTS...
📦 Removing old Node.js...
📥 Installing Node.js v18 from NodeSource...
✅ Node.js upgraded successfully!
Node.js version: v18.x.x
npm version: 10.x.x
```

### Step 4: Copy Files to Application Directory

```bash
# Create application directory
sudo mkdir -p /var/www/lego-job-generator
sudo chown -R harvad:harvad /var/www/lego-job-generator

# Copy backend files
cp -r ~/backend /var/www/lego-job-generator/

# Copy frontend files
cp -r ~/frontend /var/www/lego-job-generator/
```

### Step 5: Continue Deployment

```bash
# Make script executable
chmod +x ~/continue_deployment.sh

# Run deployment script
./continue_deployment.sh
```

This script will:
- Setup Python virtual environment
- Install Flask, Flask-CORS, Gunicorn
- Build React frontend with new Node.js
- Create systemd service for backend
- Configure Nginx
- Start all services

### Step 6: Verify Deployment

Check if services are running:

```bash
# Check backend service
sudo systemctl status lego-backend

# Check Nginx
sudo systemctl status nginx

# Test backend API
curl http://localhost:5000/health

# Test frontend
curl -I http://localhost
```

Expected responses:
- Backend: `{"status": "healthy"}` or similar
- Frontend: `HTTP/1.1 200 OK`

### Step 7: Setup SSL Certificate (Optional but Recommended)

```bash
sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect
```

### Step 8: Setup DNS

Point your domain to the server:
- Go to your DNS provider (Cloudflare, etc.)
- Add A record: `jobs.bluehawana.com → 94.72.141.71`

### Step 9: Test Application

Open in browser:
- http://jobs.bluehawana.com (or http://94.72.141.71 if DNS not setup yet)

You should see the LEGO Job Generator interface!

## Troubleshooting

### If Backend Fails to Start

```bash
# Check logs
sudo journalctl -u lego-backend -n 50

# Check if files exist
ls -la /var/www/lego-job-generator/backend/

# Test manually
cd /var/www/lego-job-generator/backend
source venv/bin/activate
python lego_app.py
```

### If Frontend Build Fails

```bash
# Check Node.js version
node --version  # Should be v18.x.x

# Try building manually
cd /var/www/lego-job-generator/frontend
rm -rf node_modules package-lock.json build
npm install
npm run build

# Check if build directory was created
ls -la build/
```

### If Nginx Shows 502 Bad Gateway

```bash
# Check if backend is running
sudo systemctl status lego-backend

# Check if backend is listening on port 5000
sudo lsof -i :5000

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### If Port 5000 is Already in Use

```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process (replace PID with actual process ID)
sudo kill -9 <PID>

# Restart backend
sudo systemctl restart lego-backend
```

## Useful Commands

```bash
# View backend logs in real-time
sudo journalctl -u lego-backend -f

# Restart backend
sudo systemctl restart lego-backend

# Restart Nginx
sudo systemctl restart nginx

# Check disk space
df -h

# Check memory usage
free -h

# View all running services
sudo systemctl list-units --type=service --state=running
```

## File Locations

- **Application Root:** `/var/www/lego-job-generator/`
- **Backend:** `/var/www/lego-job-generator/backend/`
- **Frontend Build:** `/var/www/lego-job-generator/frontend/build/`
- **Generated PDFs:** `/var/www/lego-job-generator/backend/generated_applications/`
- **Backend Service:** `/etc/systemd/system/lego-backend.service`
- **Nginx Config:** `/etc/nginx/sites-available/jobs.bluehawana.com`
- **Backend Logs:** `sudo journalctl -u lego-backend`
- **Nginx Logs:** `/var/log/nginx/error.log`, `/var/log/nginx/access.log`

## Success Checklist

- [ ] Node.js upgraded to v18
- [ ] Files copied to `/var/www/lego-job-generator/`
- [ ] Backend virtual environment created
- [ ] Python dependencies installed
- [ ] Frontend built successfully
- [ ] Systemd service created and running
- [ ] Nginx configured and running
- [ ] Backend responds to health check
- [ ] Frontend accessible via browser
- [ ] SSL certificate installed (optional)
- [ ] DNS pointing to server

## Next Steps After Deployment

1. **Test the application** by submitting a job URL
2. **Monitor logs** for any errors
3. **Setup automatic cleanup** of old PDFs (already configured in script)
4. **Setup monitoring** (optional - use health_check.sh)
5. **Configure firewall** if needed

---

**🎉 Once complete, your LEGO Job Generator will be live at jobs.bluehawana.com!**
