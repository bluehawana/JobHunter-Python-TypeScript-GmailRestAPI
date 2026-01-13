# JobHunter 24/7 Deployment Guide

This guide will help you deploy and maintain your JobHunter application for 24/7 availability during your job search.

## Quick Start

### Deploy Everything
```bash
./deploy.sh
```

### Deploy with Health Check
```bash
./deploy.sh --health-check-url https://jobs.bluehawana.com/api/health
```

### Skip Tests (Faster Deployment)
```bash
./deploy.sh --skip-tests
```

## Deployment Options

### Option 1: Local Development
```bash
# Terminal 1 - Backend (Flask LEGO API)
cd backend
python3 lego_app.py

# Terminal 2 - Frontend (React)
cd frontend
npm start
```

### Option 2: Docker Deployment (Recommended for 24/7)
```bash
# Build and start both services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Production Server (Cloudflare Pages + Backend)

#### Frontend (Cloudflare Pages)
1. Build: `cd frontend && npm run build`
2. Deploy: Upload `build/` folder to Cloudflare Pages
3. Configure custom domain: jobs.bluehawana.com

#### Backend (Cloud Server)
1. Choose a cloud provider (DigitalOcean, AWS, Azure, etc.)
2. Deploy Flask app using Gunicorn:
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 lego_app:app
```

3. Use a process manager (PM2, systemd) for auto-restart:
```bash
# Using PM2
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 lego_app:app" --name jobhunter-api
pm2 save
pm2 startup
```

4. Setup reverse proxy (Nginx):
```nginx
server {
    listen 80;
    server_name api.bluehawana.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings to prevent hanging
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /api/health {
        proxy_pass http://localhost:5000;
        access_log off;
    }
}
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Frontend
REACT_APP_API_URL=https://api.bluehawana.com

# Backend
FLASK_ENV=production
FLASK_APP=lego_app.py
SECRET_KEY=your-secret-key-here

# AI Services (if needed)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key

# Database (if using)
MONGODB_URI=mongodb://localhost:27017/jobhunter
```

## Monitoring & Health Checks

### Health Check Endpoint
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

### Setup Uptime Monitoring

Use a free service to monitor your app 24/7:

1. **UptimeRobot** (https://uptimerobot.com)
   - Monitor: https://jobs.bluehawana.com/api/health
   - Alert: Email/SMS when down
   - Free: 50 monitors

2. **Pingdom** (https://pingdom.com)
   - Free tier available
   - More detailed analytics

3. **Better Uptime** (https://betteruptime.com)
   - Modern interface
   - Incident management

### Logging

Monitor application logs:
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# PM2 logs
pm2 logs jobhunter-api

# System logs
journalctl -u jobhunter -f
```

## Automated Updates

### Setup Git Hooks for Auto-Deploy
Create `.git/hooks/post-receive`:
```bash
#!/bin/bash
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI
git pull
./deploy.sh --skip-tests
```

### Setup Cron for Regular Health Checks
```bash
# Check every 5 minutes
*/5 * * * * curl -f https://jobs.bluehawana.com/api/health || echo "Health check failed" | mail -s "JobHunter Down" your@email.com
```

## Backup Strategy

### Automated Backups
```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/JobHunter && tar -czf backups/jobhunter-$(date +\%Y\%m\%d).tar.gz frontend/build backend generated_applications
```

### Manual Backup
```bash
./deploy.sh  # Automatically creates backup in backups/ folder
```

## Rollback Procedure

If something goes wrong:

1. **Quick Rollback (Docker)**
   ```bash
   docker-compose down
   docker-compose up -d jobhunter-frontend:previous-tag jobhunter-backend:previous-tag
   ```

2. **Manual Rollback**
   ```bash
   # Restore from backup
   cp -r backups/TIMESTAMP/build_backup frontend/build

   # Restart services
   docker-compose restart
   # OR
   pm2 restart jobhunter-api
   ```

## Performance Optimization

### Frontend Optimizations
- [x] Gzip compression (enabled in nginx.conf)
- [x] Static asset caching (1 year)
- [x] Request timeouts (45s for analysis, 60s for generation)
- [x] Error recovery with user-friendly messages

### Backend Optimizations
- [ ] Add Redis caching for job analysis results
- [ ] Implement request queuing for heavy PDF generation
- [ ] Setup load balancing if traffic increases
- [ ] Database connection pooling

## Troubleshooting

### Application Gets Stuck
**Fixed**: Added 45s timeout for job analysis, 60s for document generation

### 404 on favicon.ico
**Fixed**: Created favicon.ico and favicon.svg in public/

### manifest.json Syntax Error
**Fixed**: Ensured manifest.json is included in build and served correctly

### Backend Not Responding
Check health endpoint:
```bash
curl -v https://jobs.bluehawana.com/api/health
```

If backend is down:
```bash
# Check if process is running
ps aux | grep python
ps aux | grep gunicorn

# Restart backend
pm2 restart jobhunter-api
# OR
docker-compose restart backend
```

### High Memory Usage
```bash
# Check memory usage
docker stats
# OR
pm2 monit

# Restart if needed
pm2 restart jobhunter-api
```

## Daily Maintenance Checklist

- [ ] Check health endpoint: `curl https://jobs.bluehawana.com/api/health`
- [ ] Review error logs: `pm2 logs jobhunter-api --err`
- [ ] Check disk space: `df -h`
- [ ] Monitor response times in browser DevTools
- [ ] Verify job analysis is working with a test job
- [ ] Check generated applications folder size

## Support & Updates

### Get Latest Updates
```bash
git pull origin main
./deploy.sh
```

### Check for Dependency Updates
```bash
# Frontend
cd frontend
npm outdated

# Backend
cd backend
pip list --outdated
```

## Success Metrics

Track these to ensure your application is helping your job search:

- Jobs analyzed per day
- Applications generated per day
- API response time (should be < 5s for analysis)
- PDF generation time (should be < 30s)
- Uptime percentage (target: 99.9%)

---

**Remember**: Your job search tool should work FOR you, not against you. Keep it running smoothly, and it will help you land that perfect role!

Good luck with your job hunting! 🚀
