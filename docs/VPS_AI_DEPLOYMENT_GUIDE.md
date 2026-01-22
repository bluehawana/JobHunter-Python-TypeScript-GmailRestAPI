# 🚀 VPS AI Deployment Guide

## Will Your VPS Have AI Intelligence?

**YES!** ✅ Your VPS will have the same AI capabilities once you deploy the updated code.

---

## 📋 What Needs to Be Deployed

### 1. Updated Files
```bash
backend/ai_analyzer.py          # AI analyzer with MiniMax M2
backend/cv_templates.py         # Template manager
backend/app/lego_api.py         # Integrated API
backend/minimax_search/         # Search module (foundation)
.env                            # Environment configuration
```

### 2. New Dependencies
```bash
anthropic==0.75.0              # MiniMax M2 API client
hypothesis==6.141.1            # Property-based testing
pytest==8.4.2                  # Test framework
```

---

## 🔧 Deployment Steps

### Step 1: Update VPS Environment Variables

SSH into your VPS and update the `.env` file:

```bash
ssh your-vps-user@your-vps-ip

# Navigate to your project
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI

# Edit .env file
nano .env
```

Add these lines to `.env`:
```bash
# MiniMax M2 AI Configuration
ANTHROPIC_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJsZWUgbGVvbiIsIlVzZXJOYW1lIjoibGVlIGxlb24iLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4MjkwNzkyMzU2MjUwNDI2NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODI5MDc5MjM1NTQxMTE3MjEiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJibHVlaGF3YW5hQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEyLTE4IDE3OjQ4OjQzIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.dGMrSVZCu8lWcqC5OAQ3ScJV0SVbfI7XgZatgtg_g7R8vf7grZklzvMeBfYAL3teo71Dqx0COdlxZf8f6Qj5VAbxzGJc1xL5unqcR1PzHe-XoRaUy6dkDmCVL6jlUDVrVsQVybXS2jDe59MCPANU0kzSBC2YnFQEN4fuyyfFBFThClwnkz2aWy74xBnnHIy-y92OfrGtO1xjYVIAFYgaS7xG-TmLZNQGBz5740truxkKwP31ulThVDq7sUpOqxw1Q-87zg-WeeQ1CXM4Z5TK-0aydoZv1NCkfLbdCQ3QsVhqWRsCcHYafA_Mz_-aOZQopV_Us2RXLt2FooeMGRyqXQ
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
AI_ENABLED=true
AI_MODEL=MiniMax-M2
```

### Step 2: Push Code to VPS

**Option A: Using Git (Recommended)**
```bash
# On your local machine
git add .
git commit -m "Add AI-powered template selection with MiniMax M2"
git push origin main

# On VPS
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI
git pull origin main
```

**Option B: Using rsync**
```bash
# From your local machine
rsync -avz --exclude 'node_modules' --exclude '__pycache__' \
  backend/ your-vps-user@your-vps-ip:/path/to/project/backend/
```

**Option C: Using SCP**
```bash
# Copy updated files
scp -r backend/ai_analyzer.py your-vps-user@your-vps-ip:/path/to/project/backend/
scp -r backend/cv_templates.py your-vps-user@your-vps-ip:/path/to/project/backend/
scp -r backend/app/lego_api.py your-vps-user@your-vps-ip:/path/to/project/backend/app/
scp -r backend/minimax_search/ your-vps-user@your-vps-ip:/path/to/project/backend/
scp .env your-vps-user@your-vps-ip:/path/to/project/
```

### Step 3: Install Dependencies on VPS

```bash
# SSH into VPS
ssh your-vps-user@your-vps-ip

# Navigate to project
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI

# Activate virtual environment (if using one)
source venv/bin/activate

# Install new dependencies
pip3 install anthropic hypothesis pytest

# Or install from requirements.txt
pip3 install -r backend/requirements.txt
```

### Step 4: Restart Your Application

```bash
# If using systemd service
sudo systemctl restart jobhunter-api

# If using PM2
pm2 restart jobhunter-api

# If using screen/tmux
# Kill old process and restart
pkill -f "python.*lego_api"
nohup python3 backend/app/lego_api.py &

# If using gunicorn
sudo systemctl restart gunicorn
```

### Step 5: Verify AI is Working

```bash
# Test the AI analyzer
python3 backend/ai_analyzer.py

# Check logs
tail -f /var/log/jobhunter/app.log

# Or check systemd logs
journalctl -u jobhunter-api -f
```

---

## ✅ Verification Checklist

After deployment, verify these work:

### 1. Check Environment Variables
```bash
python3 -c "import os; print('API Key:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```
Should output: `API Key: True`

### 2. Test AI Analyzer
```bash
cd backend
python3 -c "
from ai_analyzer import AIAnalyzer
analyzer = AIAnalyzer()
print('AI Available:', analyzer.is_available())
"
```
Should output: `AI Available: True`

### 3. Test API Endpoint
```bash
curl -X POST http://your-vps-ip:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "DevOps engineer with Kubernetes and AWS experience",
    "jobUrl": "https://example.com/job"
  }'
```

Should return JSON with `aiAnalysis` field:
```json
{
  "roleType": "Devops Cloud",
  "roleCategory": "devops_cloud",
  "aiAnalysis": {
    "used": true,
    "confidence": 0.95,
    "model": "MiniMax-M2",
    "reasoning": "..."
  }
}
```

### 4. Check Web UI
Visit your web application and paste a job description. You should see:
- AI confidence score displayed
- Correct template selected
- Key technologies extracted

---

## 🔍 Troubleshooting

### Issue: "anthropic package not installed"
```bash
pip3 install anthropic --upgrade
```

### Issue: "AI Analyzer not available"
Check environment variables:
```bash
cat .env | grep ANTHROPIC
```

### Issue: "invalid api key"
Verify the API key is correctly set:
```bash
python3 -c "import os; print(os.getenv('ANTHROPIC_API_KEY')[:50])"
```

### Issue: API returns keyword matching instead of AI
Check logs for errors:
```bash
tail -100 /var/log/jobhunter/app.log | grep -i "ai\|anthropic\|error"
```

### Issue: Import errors
Ensure all files are uploaded:
```bash
ls -la backend/ai_analyzer.py
ls -la backend/minimax_search/
```

---

## 📊 Performance on VPS

### Expected Performance:
- **AI Analysis:** 2-3 seconds per job
- **Keyword Fallback:** <100ms
- **Memory Usage:** +50-100MB (for Anthropic SDK)
- **CPU Usage:** Minimal (API calls are async)

### Optimization Tips:
1. **Enable caching** - Cache AI results for 5 minutes
2. **Use async** - Make API calls non-blocking
3. **Monitor quota** - Track MiniMax M2 API usage
4. **Fallback gracefully** - Always have keyword matching as backup

---

## 🔐 Security Considerations

### 1. Protect API Keys
```bash
# Set proper permissions on .env
chmod 600 .env

# Never commit .env to git
echo ".env" >> .gitignore
```

### 2. Use Environment Variables
Don't hardcode API keys in code. Always use:
```python
api_key = os.getenv('ANTHROPIC_API_KEY')
```

### 3. Rate Limiting
The system already has rate limiting built-in via `RateLimiter` class.

---

## 📈 Monitoring

### Add Logging
```python
import logging
logging.basicConfig(
    filename='/var/log/jobhunter/ai.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor API Usage
Track in your logs:
- AI analysis success rate
- Confidence scores
- Fallback frequency
- Response times

---

## 🎯 Quick Deployment Script

Create `deploy_ai_to_vps.sh`:

```bash
#!/bin/bash

VPS_USER="your-vps-user"
VPS_IP="your-vps-ip"
PROJECT_PATH="/path/to/JobHunter-Python-TypeScript-GmailRestAPI"

echo "🚀 Deploying AI updates to VPS..."

# 1. Copy files
echo "📦 Copying files..."
rsync -avz --exclude '__pycache__' \
  backend/ai_analyzer.py \
  backend/cv_templates.py \
  backend/app/lego_api.py \
  backend/minimax_search/ \
  $VPS_USER@$VPS_IP:$PROJECT_PATH/backend/

# 2. Copy .env
echo "🔐 Updating environment..."
scp .env $VPS_USER@$VPS_IP:$PROJECT_PATH/

# 3. Install dependencies and restart
echo "🔧 Installing dependencies and restarting..."
ssh $VPS_USER@$VPS_IP << 'EOF'
cd /path/to/JobHunter-Python-TypeScript-GmailRestAPI
pip3 install anthropic hypothesis pytest
sudo systemctl restart jobhunter-api
echo "✅ Deployment complete!"
EOF

echo "🎉 AI deployment finished!"
echo "🔍 Verify at: http://$VPS_IP:5000/api/health"
```

Make it executable:
```bash
chmod +x deploy_ai_to_vps.sh
./deploy_ai_to_vps.sh
```

---

## ✨ What Your Users Will See

### Before (Stupid LEGO):
```
Job Description: DevOps with Kubernetes
→ Always uses Nasdaq template
→ No intelligence
→ Generic content
```

### After (AI-Powered):
```
Job Description: DevOps with Kubernetes
→ AI analyzes: "devops_cloud" (95% confidence)
→ Selects: Nasdaq DevOps template
→ Extracts: Kubernetes, Docker, AWS, CI/CD
→ Customizes content for role
```

---

## 🎊 Summary

**YES, your VPS will have the same AI intelligence!**

Just:
1. ✅ Push the updated code
2. ✅ Set environment variables
3. ✅ Install `anthropic` package
4. ✅ Restart your application

**That's it!** Your VPS will now use MiniMax M2 AI for intelligent template selection. 🚀
