# 🚀 Quick Start - Complete Deployment in 3 Steps

## Current Situation
You're on the AlphaVPS server with:
- ✅ Files extracted in home directory
- ✅ All system dependencies installed
- ⚠️ Node.js v12 (needs upgrade to v18)
- ⏳ Ready to complete deployment

## 3 Simple Steps to Go Live

### Step 1: Upgrade Node.js (2 minutes)

```bash
chmod +x ~/upgrade_nodejs.sh
./upgrade_nodejs.sh
```

This will:
- Remove old Node.js v12
- Install Node.js v18 LTS
- Verify installation

### Step 2: Complete Deployment (5-10 minutes)

```bash
chmod +x ~/continue_deployment.sh
./continue_deployment.sh
```

This will:
- Copy files to `/var/www/lego-job-generator/`
- Setup Python backend with Flask
- Build React frontend
- Configure systemd service
- Configure Nginx
- Start all services

### Step 3: Verify It Works

```bash
# Check backend
sudo systemctl status lego-backend

# Check Nginx
sudo systemctl status nginx

# Test API
curl http://localhost:5000/health

# Test frontend
curl -I http://localhost
```

## That's It! 🎉

Your application should now be running at:
- **Local:** http://localhost
- **Public:** http://94.72.141.71
- **Domain:** http://jobs.bluehawana.com (after DNS setup)

## Optional: Setup SSL (2 minutes)

```bash
sudo certbot --nginx -d jobs.bluehawana.com --email hongzhili01@gmail.com --agree-tos --redirect
```

## Troubleshooting

### If something fails, check logs:

```bash
# Backend logs
sudo journalctl -u lego-backend -n 50

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### If frontend build fails:

```bash
# Check Node.js version (should be v18.x.x)
node --version

# Rebuild manually
cd /var/www/lego-job-generator/frontend
rm -rf node_modules build
npm install
npm run build
```

### If backend won't start:

```bash
# Check if port 5000 is in use
sudo lsof -i :5000

# Test manually
cd /var/www/lego-job-generator/backend
source venv/bin/activate
python lego_app.py
```

## Useful Commands

```bash
# Restart backend
sudo systemctl restart lego-backend

# Restart Nginx
sudo systemctl restart nginx

# View logs in real-time
sudo journalctl -u lego-backend -f

# Check disk space
df -h
```

## File Locations

- **Application:** `/var/www/lego-job-generator/`
- **Backend:** `/var/www/lego-job-generator/backend/`
- **Frontend:** `/var/www/lego-job-generator/frontend/build/`
- **Generated PDFs:** `/var/www/lego-job-generator/backend/generated_applications/`

---

**Need help?** Check `DEPLOYMENT_STEPS.md` for detailed instructions.
