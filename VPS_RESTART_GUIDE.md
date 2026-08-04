# VPS Restart Guide - Quick Fix for 502 Bad Gateway

## Error Symptoms
- 502 Bad Gateway on https://jobs.bluehawana.com/api/*
- Frontend returns HTML error page instead of JSON
- Lego API service crashed or stopped

## SSH Connection
```bash
ssh alphavps
# Enter your auth code when prompted
```

## Quick Diagnostic Commands

### 1. Check if lego-api service is running
```bash
systemctl status lego-api
```

### 2. Check recent logs
```bash
journalctl -u lego-api -n 50 --no-pager
```

### 3. Check if process is actually running
```bash
ps aux | grep lego_api
```

### 4. Check port 8000
```bash
netstat -tlnp | grep 8000
# or
lsof -i :8000
```

## Quick Restart Options

### Option 1: Restart the service (recommended)
```bash
systemctl restart lego-api
systemctl status lego-api
```

### Option 2: If service won't start, check for port conflicts
```bash
# Kill any process on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
systemctl restart lego-api
```

### Option 3: Manual restart if systemd fails
```bash
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
source venv/bin/activate
cd backend/app
nohup python3 lego_api.py > /var/log/lego-api.log 2>&1 &
```

## Verify It's Working

### 1. Check service status
```bash
systemctl status lego-api
# Should show "active (running)"
```

### 2. Test the API locally
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 3. Test from outside
```bash
curl https://jobs.bluehawana.com/api/health
```

## Common Issues & Fixes

### Issue: "Address already in use"
```bash
lsof -ti:8000 | xargs kill -9
systemctl restart lego-api
```

### Issue: Python dependencies missing
```bash
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
source venv/bin/activate
pip install -r backend/requirements.txt
systemctl restart lego-api
```

### Issue: Out of memory
```bash
free -h
# If low memory, restart service to clear
systemctl restart lego-api
```

### Issue: Nginx not forwarding
```bash
systemctl status nginx
nginx -t  # Test config
systemctl restart nginx
```

## Check Logs for Root Cause

```bash
# Last 100 lines of lego-api logs
journalctl -u lego-api -n 100 --no-pager

# Follow logs in real-time
journalctl -u lego-api -f

# Check nginx error logs
tail -f /var/log/nginx/error.log
```

## After Restart - Verify

1. Service is running: `systemctl status lego-api`
2. Port is listening: `netstat -tlnp | grep 8000`
3. API responds: `curl http://localhost:8000/health`
4. External access works: `curl https://jobs.bluehawana.com/api/health`

## If Still Not Working

Check the full deployment guide:
```bash
cat /root/JobHunter-Python-TypeScript-GmailRestAPI/deploy/CONSISTENCY_DEPLOYMENT_GUIDE.md
```

Or run the atomic restart script:
```bash
cd /root/JobHunter-Python-TypeScript-GmailRestAPI
bash deploy/atomic_restart.sh
```
