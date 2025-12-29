# ✅ Quick Deploy Checklist for AlphaVPS

## 5-Minute Deployment

### □ Step 1: SSH to AlphaVPS
```bash
ssh alphavps
cd ~/your-project-folder
```

### □ Step 2: Pull Latest Code
```bash
git pull origin main
```

### □ Step 3: Update .env
```bash
nano .env
```
Add:
```
ANTHROPIC_API_KEY=REMOVED_SECRET
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
AI_MODEL=MiniMax-M2
```

### □ Step 4: Install Package
```bash
pip3 install anthropic
```

### □ Step 5: Test
```bash
python3 backend/test_vps_ai.py
```
Should show: `✅ AI Integration: WORKING`

### □ Step 6: Restart
```bash
sudo systemctl restart jobhunter-api
# OR
pm2 restart all
```

### □ Step 7: Verify
Visit your web app and test with a job description!

---

## 🎉 Done!

Your VPS now has AI intelligence. No frontend changes needed!
