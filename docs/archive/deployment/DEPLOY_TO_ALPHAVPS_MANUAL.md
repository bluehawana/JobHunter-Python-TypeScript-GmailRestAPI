# 🚀 Manual Deployment to AlphaVPS - Simple Steps

Since you can SSH directly to your AlphaVPS, here's the easiest way to deploy the AI updates.

---

## 📋 Prerequisites

- ✅ SSH access to AlphaVPS: `ssh alphavps`
- ✅ Your project is already running on AlphaVPS
- ✅ You know where your project is located on the VPS

---

## 🎯 Deployment Steps (5 Minutes)

### Step 1: Push Code to Git (Optional but Recommended)

On your **local machine**:

```bash
# Commit your changes
git add .
git commit -m "Add AI-powered template selection with MiniMax M2"
git push origin main
```

### Step 2: SSH into AlphaVPS

```bash
ssh alphavps
```

### Step 3: Navigate to Your Project

```bash
# Find your project (common locations)
cd ~/JobHunter-Python-TypeScript-GmailRestAPI
# OR
cd /var/www/jobhunter
# OR
cd /root/jobhunter

# Verify you're in the right place
ls -la backend/app/lego_api.py
```

### Step 4: Pull Latest Code (If Using Git)

```bash
git pull origin main
```

**OR** if not using Git, manually copy files (see Alternative Method below)

### Step 5: Update Environment Variables

```bash
# Edit .env file
nano .env

# Add these lines (or update if they exist):
ANTHROPIC_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJsZWUgbGVvbiIsIlVzZXJOYW1lIjoibGVlIGxlb24iLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4MjkwNzkyMzU2MjUwNDI2NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODI5MDc5MjM1NTQxMTE3MjEiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJibHVlaGF3YW5hQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEyLTE4IDE3OjQ4OjQzIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.dGMrSVZCu8lWcqC5OAQ3ScJV0SVbfI7XgZatgtg_g7R8vf7grZklzvMeBfYAL3teo71Dqx0COdlxZf8f6Qj5VAbxzGJc1xL5unqcR1PzHe-XoRaUy6dkDmCVL6jlUDVrVsQVybXS2jDe59MCPANU0kzSBC2YnFQEN4fuyyfFBFThClwnkz2aWy74xBnnHIy-y92OfrGtO1xjYVIAFYgaS7xG-TmLZNQGBz5740truxkKwP31ulThVDq7sUpOqxw1Q-87zg-WeeQ1CXM4Z5TK-0aydoZv1NCkfLbdCQ3QsVhqWRsCcHYafA_Mz_-aOZQopV_Us2RXLt2FooeMGRyqXQ
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
AI_ENABLED=true
AI_MODEL=MiniMax-M2

# Save: Ctrl+O, Enter, Ctrl+X
```

### Step 6: Install Python Dependencies

```bash
# If using virtual environment
source venv/bin/activate  # or source env/bin/activate

# Install anthropic package
pip3 install anthropic

# Install testing packages (optional)
pip3 install hypothesis pytest
```

### Step 7: Test the AI

```bash
# Quick test
python3 backend/test_vps_ai.py
```

You should see:
```
✅ AI Integration: WORKING
   Your VPS has full AI intelligence!
```

### Step 8: Restart Your Application

Choose the method that matches your setup:

**If using systemd:**
```bash
sudo systemctl restart jobhunter-api
# OR
sudo systemctl restart lego-api
```

**If using PM2:**
```bash
pm2 restart all
# OR
pm2 restart jobhunter
```

**If using screen/tmux:**
```bash
# Find the process
ps aux | grep python | grep lego_api

# Kill it (replace XXXX with actual PID)
kill XXXX

# Restart
cd backend/app
nohup python3 lego_api.py &
```

### Step 9: Verify It's Working

```bash
# Check if process is running
ps aux | grep python | grep lego_api

# Test the API
curl http://localhost:5000/api/health

# Check logs
tail -f /var/log/jobhunter/app.log
# OR
journalctl -u jobhunter-api -f
```

---

## 🔄 Alternative Method (Without Git)

If you're not using Git, copy files manually:

### On Your Local Machine:

```bash
# Copy files to AlphaVPS
scp backend/ai_analyzer.py alphavps:~/project/backend/
scp backend/cv_templates.py alphavps:~/project/backend/
scp backend/app/lego_api.py alphavps:~/project/backend/app/
scp -r backend/minimax_search/ alphavps:~/project/backend/
scp .env alphavps:~/project/
```

Then continue from Step 6 above.

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Files are updated on VPS
- [ ] .env has ANTHROPIC_API_KEY
- [ ] anthropic package is installed
- [ ] test_vps_ai.py shows "AI Integration: WORKING"
- [ ] Application is running
- [ ] Web app can analyze jobs

---

## 🧪 Quick Test

Visit your web app and paste this job description:

```
DevOps Engineer position requiring Kubernetes, Docker, AWS, and CI/CD experience.
Must have Python and Terraform skills.
```

You should see:
- ✅ AI confidence score (e.g., 95%)
- ✅ Correct template selected (devops_cloud)
- ✅ Technologies extracted (Kubernetes, Docker, AWS, etc.)

---

## 🐛 Troubleshooting

### "anthropic not found"
```bash
pip3 install anthropic --upgrade
```

### "AI Analyzer not available"
```bash
# Check .env
cat .env | grep ANTHROPIC

# Check if key is loaded
python3 -c "import os; print(bool(os.getenv('ANTHROPIC_API_KEY')))"
```

### "Module not found"
```bash
# Make sure you're in the right directory
pwd
ls backend/ai_analyzer.py
```

### Application won't restart
```bash
# Check what's running
ps aux | grep python

# Check logs for errors
tail -100 /var/log/jobhunter/app.log
```

---

## 📞 Need Help?

If you get stuck:

1. Check the logs: `tail -f /var/log/jobhunter/app.log`
2. Run the test: `python3 backend/test_vps_ai.py`
3. Verify files exist: `ls -la backend/ai_analyzer.py`

---

## 🎉 Done!

Your AlphaVPS now has AI intelligence! The web app will automatically use it.

**No frontend changes needed** - the AI works behind the scenes in the backend API.
