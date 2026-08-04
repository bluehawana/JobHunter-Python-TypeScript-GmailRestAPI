# 🚀 REDEPLOY jobs.bluehawana.com NOW

## Your VPS was reinstalled. Here's how to get it back online:

### ONE-COMMAND DEPLOYMENT 🎯

**On your Mac (open a NEW terminal, not the SSH one):**

```bash
cd ~/Projects/JobHunter-Python-TypeScript-GmailRestAPI
./deploy/UPLOAD_TO_VPS.sh
```

Then SSH in and run:

```bash
sudo mv /tmp/JobHunter-Python-TypeScript-GmailRestAPI /root/ && \
cd /root/JobHunter-Python-TypeScript-GmailRestAPI/deploy && \
chmod +x COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh && \
sudo ./COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh
```

---

## That's it! ✅

The script will:
1. ✅ Update system packages
2. ✅ Install all dependencies (Python, Node.js, Nginx, LaTeX)
3. ✅ Setup Python virtual environment
4. ✅ Install Python packages
5. ✅ Build React frontend
6. ✅ Create systemd service for API
7. ✅ Configure Nginx
8. ✅ Setup SSL certificate (optional)
9. ✅ Start all services

**Time:** ~15-20 minutes (depending on your internet speed)

---

## After Deployment

### 1. Update API Keys
```bash
nano /root/JobHunter-Python-TypeScript-GmailRestAPI/.env
```

Add your actual keys:
```
ANTHROPIC_API_KEY=your_actual_key_here
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
SCRAPERAPI_KEY=your_scraper_key_here
```

### 2. Restart API
```bash
sudo systemctl restart lego-api
```

### 3. Verify It Works
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 4. Test from Browser
Open: https://jobs.bluehawana.com

---

## Quick Status Check

```bash
# Check if services are running
sudo systemctl status lego-api
sudo systemctl status nginx

# View API logs
sudo journalctl -u lego-api -n 50

# Test API
curl https://jobs.bluehawana.com/api/health
```

---

## If Something Fails

### Option 1: Check Logs
```bash
sudo journalctl -u lego-api -f
sudo tail -f /var/log/nginx/error.log
```

### Option 2: Manual Restart
```bash
sudo systemctl restart lego-api
sudo systemctl restart nginx
```

### Option 3: Re-run Deployment
```bash
cd /root/JobHunter-Python-TypeScript-GmailRestAPI/deploy
sudo ./COMPLETE_REDEPLOY_AFTER_OS_REINSTALL.sh
```

---

## Current VPS Status

**You are here:** `harvad@harvad:~$`  
**VPS:** 94.72.141.71:1025  
**OS:** Fresh Debian 6.1.0-32  
**Domain:** jobs.bluehawana.com  
**Status:** 🔴 Needs deployment  

---

## Need Help?

Check the detailed guide:
```bash
cat ~/Projects/JobHunter-Python-TypeScript-GmailRestAPI/deploy/QUICK_REDEPLOY_GUIDE.md
```

Or just ask me! 😊
