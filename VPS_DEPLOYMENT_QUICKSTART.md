# 🚀 VPS Deployment Quickstart - Deploy Your Fixes Now!

## Current VPS Status

✅ **VPS is Running**
- Server: harvad@94.72.141.71:1025
- Domain: https://jobs.bluehawana.com
- Service: lego-backend.service (active)
- Backend API: ✅ Working
- Health endpoint: ❌ Not deployed yet (needs update)

## What Will Be Deployed

1. ✅ **Health check endpoint** - `/api/health` for monitoring
2. ✅ **Request timeouts** - 45-60s to prevent hanging
3. ✅ **Better error handling** - Clear, actionable error messages
4. ✅ **Updated frontend** - With all timeout fixes
5. ✅ **favicon.ico & favicon.svg** - Fixed 404 errors
6. ✅ **Fixed manifest.json** - No more syntax errors
7. ✅ **Updated dependencies** - Fixed cryptography version

## Deploy in 1 Command

```bash
./deploy-to-vps.sh
```

That's it! The script will:
1. ✅ Build your frontend locally
2. ✅ Create a deployment package
3. ✅ Upload to your VPS
4. ✅ Backup current version
5. ✅ Deploy new files
6. ✅ Restart services
7. ✅ Verify everything works

## First Time Setup

If you haven't set up SSH keys yet:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to VPS
ssh-copy-id -p 1025 harvad@94.72.141.71

# Test connection
ssh -p 1025 harvad@94.72.141.71 "echo 'SSH is working!'"
```

## What Happens During Deployment

```
🚀 Deploying JobHunter Fixes to VPS
├─ Step 1: Building Frontend (2-3 minutes)
│  └─ npm install & build
│
├─ Step 2: Creating Deployment Package
│  └─ Packaging frontend/build + backend files
│
├─ Step 3: Uploading to VPS (30 seconds)
│  └─ Secure upload via SCP
│
├─ Step 4: Deploying on VPS
│  ├─ Creating backup
│  ├─ Extracting files
│  ├─ Installing Python dependencies
│  ├─ Deploying frontend & backend
│  ├─ Restarting services
│  └─ Reloading Nginx
│
└─ Step 5: Verifying Deployment
   ├─ Testing /api/health
   ├─ Testing /api/analyze-job
   └─ Testing frontend
```

## Manual Deployment (If Needed)

### Step 1: Build Locally
```bash
cd frontend
npm install
npm run build
```

### Step 2: Upload Files
```bash
# Create package
tar -czf fixes.tar.gz frontend/build backend/app/lego_api.py backend/requirements.txt

# Upload
scp -P 1025 fixes.tar.gz harvad@94.72.141.71:~/
```

### Step 3: Deploy on VPS
```bash
# Connect to VPS
ssh -p 1025 harvad@94.72.141.71

# Backup current version
mkdir -p ~/backups/$(date +%Y%m%d_%H%M%S)
cp -r /var/www/lego-job-generator/backend/app/lego_api.py ~/backups/$(date +%Y%m%d_%H%M%S)/
cp -r /var/www/lego-job-generator/frontend/build ~/backups/$(date +%Y%m%d_%H%M%S)/

# Extract and deploy
cd ~
tar -xzf fixes.tar.gz

# Deploy backend
cp backend/app/lego_api.py /var/www/lego-job-generator/backend/app/
cp backend/requirements.txt /var/www/lego-job-generator/backend/

# Install dependencies
cd /var/www/lego-job-generator/backend
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Deploy frontend
rm -rf /var/www/lego-job-generator/frontend/build
mv ~/frontend/build /var/www/lego-job-generator/frontend/

# Restart services
sudo systemctl restart lego-backend.service
sudo nginx -t && sudo systemctl reload nginx

# Verify
curl https://jobs.bluehawana.com/api/health
```

## Verification

After deployment, verify everything works:

### 1. Health Check
```bash
curl https://jobs.bluehawana.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "JobHunter LEGO API",
  "timestamp": "2026-01-12T19:00:00",
  "version": "1.0.0"
}
```

### 2. Job Analysis
```bash
curl -X POST https://jobs.bluehawana.com/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{"jobDescription":"DevOps Engineer with Kubernetes"}'
```

Should return job analysis with roleType, keywords, etc.

### 3. Frontend
Open https://jobs.bluehawana.com in your browser:
- ✅ No favicon 404 errors
- ✅ No manifest.json syntax errors
- ✅ Application doesn't hang when analyzing jobs
- ✅ Clear error messages if something goes wrong

## Rollback (If Needed)

If something goes wrong:

```bash
ssh -p 1025 harvad@94.72.141.71

# List backups
ls -lt ~/backups/

# Restore from backup
BACKUP_DATE="20260112_190000"  # Use your actual backup date
cp ~/backups/$BACKUP_DATE/lego_api.py /var/www/lego-job-generator/backend/app/
cp -r ~/backups/$BACKUP_DATE/build /var/www/lego-job-generator/frontend/

# Restart
sudo systemctl restart lego-backend.service
sudo systemctl reload nginx
```

## Monitoring After Deployment

### Check Service Status
```bash
ssh -p 1025 harvad@94.72.141.71 "sudo systemctl status lego-backend.service"
```

### View Live Logs
```bash
ssh -p 1025 harvad@94.72.141.71 "sudo journalctl -u lego-backend.service -f"
```

### Check Nginx Logs
```bash
ssh -p 1025 harvad@94.72.141.71 "sudo tail -f /var/log/nginx/access.log"
```

## Setup Uptime Monitoring (Recommended)

1. Go to [UptimeRobot.com](https://uptimerobot.com) (free)
2. Add new monitor:
   - Type: HTTP(S)
   - URL: `https://jobs.bluehawana.com/api/health`
   - Monitoring Interval: 5 minutes
   - Alert Contacts: Your email
3. You'll get notified if your app goes down

## Troubleshooting

### Service Won't Start
```bash
# Check logs
ssh -p 1025 harvad@94.72.141.71 "sudo journalctl -u lego-backend.service -n 50"

# Check if port is in use
ssh -p 1025 harvad@94.72.141.71 "sudo lsof -i :5000"

# Kill old processes
ssh -p 1025 harvad@94.72.141.71 "sudo pkill -f gunicorn"
ssh -p 1025 harvad@94.72.141.71 "sudo systemctl restart lego-backend.service"
```

### 502 Bad Gateway
- Backend service is down
- Check: `sudo systemctl status lego-backend.service`
- Restart: `sudo systemctl restart lego-backend.service`

### Changes Not Visible
- Clear Cloudflare cache
- Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check if correct files deployed: `ls -la /var/www/lego-job-generator/frontend/build/`

## Quick Commands Reference

```bash
# Deploy everything
./deploy-to-vps.sh

# Connect to VPS
ssh -p 1025 harvad@94.72.141.71

# Check service status
ssh -p 1025 harvad@94.72.141.71 "sudo systemctl status lego-backend.service"

# View logs
ssh -p 1025 harvad@94.72.141.71 "sudo journalctl -u lego-backend.service -f"

# Restart service
ssh -p 1025 harvad@94.72.141.71 "sudo systemctl restart lego-backend.service"

# Test health endpoint
curl https://jobs.bluehawana.com/api/health

# Test job analysis
curl -X POST https://jobs.bluehawana.com/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{"jobDescription":"test"}'
```

---

## Ready to Deploy?

Run this command now:
```bash
./deploy-to-vps.sh
```

It will take about 5 minutes and deploy all your fixes to production!

Good luck with your job hunting! 🚀
