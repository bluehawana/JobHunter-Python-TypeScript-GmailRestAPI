# 🚀 Deploy to AlphaVPS - Manual File Copy Method

**VPS Details:**
- Host: `harvad@94.72.141.71`
- Port: `1025` (custom SSH port)
- Project: `/var/www/lego-job-generator`
- Service: `lego-backend.service`

---

## 📦 Method 1: Using SCP (Recommended)

### On Your Local Machine:

```bash
# 1. Copy Python files
scp -P 1025 backend/ai_analyzer.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/
scp -P 1025 backend/cv_templates.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

# 2. Copy minimax_search module (entire folder)
scp -P 1025 -r backend/minimax_search harvad@94.72.141.71:/var/www/lego-job-generator/backend/

# 3. Copy test script
scp -P 1025 backend/test_vps_ai.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/

# 4. Copy .env file
scp -P 1025 .env harvad@94.72.141.71:/var/www/lego-job-generator/
```

---

## 📦 Method 2: Using SFTP (Alternative)

```bash
# Connect via SFTP (note the -P for port)
sftp -P 1025 harvad@94.72.141.71

# Navigate to project
cd /var/www/lego-job-generator/backend

# Upload files
put backend/ai_analyzer.py
put backend/cv_templates.py
put backend/app/lego_api.py
put backend/test_vps_ai.py

# Upload folder
put -r backend/minimax_search

# Upload .env
cd /var/www/lego-job-generator
put .env

# Exit
bye
```

---

## 📦 Method 3: Copy-Paste (Simplest)

### Step 1: SSH to VPS
```bash
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
```

### Step 2: Backup Existing Files
```bash
# Create backup
mkdir -p backups
cp backend/ai_analyzer.py backups/ai_analyzer.py.backup 2>/dev/null || true
cp backend/cv_templates.py backups/cv_templates.py.backup 2>/dev/null || true
cp backend/app/lego_api.py backups/lego_api.py.backup 2>/dev/null || true
```

### Step 3: Create/Update Files

**Create ai_analyzer.py:**
```bash
nano backend/ai_analyzer.py
# Copy the entire content from your local backend/ai_analyzer.py
# Paste it, then save: Ctrl+O, Enter, Ctrl+X
```

**Update cv_templates.py:**
```bash
nano backend/cv_templates.py
# Copy the entire content from your local backend/cv_templates.py
# Paste it, then save: Ctrl+O, Enter, Ctrl+X
```

**Update lego_api.py:**
```bash
nano backend/app/lego_api.py
# Copy the entire content from your local backend/app/lego_api.py
# Paste it, then save: Ctrl+O, Enter, Ctrl+X
```

**Create minimax_search module:**
```bash
mkdir -p backend/minimax_search
cd backend/minimax_search

# Create each file
nano __init__.py       # Copy from local
nano models.py         # Copy from local
nano exceptions.py     # Copy from local
nano client.py         # Copy from local
nano indexer.py        # Copy from local
nano service.py        # Copy from local
nano cache.py          # Copy from local
nano rate_limiter.py   # Copy from local
nano ranker.py         # Copy from local

cd /var/www/lego-job-generator
```

**Update .env:**
```bash
nano .env
```

Add these lines:
```bash
# MiniMax M2 AI Configuration
ANTHROPIC_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJsZWUgbGVvbiIsIlVzZXJOYW1lIjoibGVlIGxlb24iLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4MjkwNzkyMzU2MjUwNDI2NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODI5MDc5MjM1NTQxMTE3MjEiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJibHVlaGF3YW5hQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEyLTE4IDE3OjQ4OjQzIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.dGMrSVZCu8lWcqC5OAQ3ScJV0SVbfI7XgZatgtg_g7R8vf7grZklzvMeBfYAL3teo71Dqx0COdlxZf8f6Qj5VAbxzGJc1xL5unqcR1PzHe-XoRaUy6dkDmCVL6jlUDVrVsQVybXS2jDe59MCPANU0kzSBC2YnFQEN4fuyyfFBFThClwnkz2aWy74xBnnHIy-y92OfrGtO1xjYVIAFYgaS7xG-TmLZNQGBz5740truxkKwP31ulThVDq7sUpOqxw1Q-87zg-WeeQ1CXM4Z5TK-0aydoZv1NCkfLbdCQ3QsVhqWRsCcHYafA_Mz_-aOZQopV_Us2RXLt2FooeMGRyqXQ
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
AI_ENABLED=true
AI_MODEL=MiniMax-M2
```

---

## 🔧 After Files Are Copied

### Step 4: Install Dependencies

```bash
cd /var/www/lego-job-generator

# Check if virtual environment exists
ls -la venv/ env/ 2>/dev/null

# If venv exists, activate it
source venv/bin/activate
# OR
source env/bin/activate

# Install anthropic
pip3 install anthropic

# Optional: install testing packages
pip3 install hypothesis pytest
```

### Step 5: Test

```bash
# Test the AI
python3 backend/test_vps_ai.py
```

Should show:
```
✅ AI Integration: WORKING
   Your VPS has full AI intelligence!
```

### Step 6: Restart Application

```bash
# Check what's running
ps aux | grep python | grep lego

# Restart the service (your service is lego-backend.service)
sudo systemctl restart lego-backend.service

# Check status
sudo systemctl status lego-backend.service
```

### Step 7: Verify

```bash
# Check if running
ps aux | grep python | grep lego

# Check logs
tail -f /var/log/lego-job-generator/app.log
# OR
journalctl -u lego-api -f
# OR
pm2 logs
```

---

## 🎯 Quick Verification

Visit your web app and test with this job description:

```
DevOps Engineer with Kubernetes, Docker, AWS, and CI/CD experience.
```

You should see AI confidence score and correct template selection!

---

## 📋 Files That Need to Be Copied

Checklist:
- [ ] `backend/ai_analyzer.py` (NEW)
- [ ] `backend/cv_templates.py` (UPDATED)
- [ ] `backend/app/lego_api.py` (UPDATED)
- [ ] `backend/minimax_search/` (NEW - entire folder)
- [ ] `backend/test_vps_ai.py` (NEW)
- [ ] `.env` (UPDATED - add API keys)

---

## 🐛 Troubleshooting

### "Permission denied"
```bash
sudo chown -R harvad:harvad /var/www/lego-job-generator
```

### "Module not found"
```bash
# Make sure files are in the right place
ls -la /var/www/lego-job-generator/backend/ai_analyzer.py
ls -la /var/www/lego-job-generator/backend/minimax_search/
```

### "anthropic not installed"
```bash
pip3 install anthropic --user
# OR
sudo pip3 install anthropic
```

---

## 💡 Recommended: Use SCP

The **easiest and fastest** method is SCP (Method 1). Just run those commands from your local machine and files will be copied directly to your VPS.

Replace `your-vps-ip` with your actual VPS IP address!
