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
ANTHROPIC_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJsZWUgbGVvbiIsIlVzZXJOYW1lIjoibGVlIGxlb24iLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4MjkwNzkyMzU2MjUwNDI2NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODI5MDc5MjM1NTQxMTE3MjEiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJibHVlaGF3YW5hQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEyLTE4IDE3OjQ4OjQzIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.dGMrSVZCu8lWcqC5OAQ3ScJV0SVbfI7XgZatgtg_g7R8vf7grZklzvMeBfYAL3teo71Dqx0COdlxZf8f6Qj5VAbxzGJc1xL5unqcR1PzHe-XoRaUy6dkDmCVL6jlUDVrVsQVybXS2jDe59MCPANU0kzSBC2YnFQEN4fuyyfFBFThClwnkz2aWy74xBnnHIy-y92OfrGtO1xjYVIAFYgaS7xG-TmLZNQGBz5740truxkKwP31ulThVDq7sUpOqxw1Q-87zg-WeeQ1CXM4Z5TK-0aydoZv1NCkfLbdCQ3QsVhqWRsCcHYafA_Mz_-aOZQopV_Us2RXLt2FooeMGRyqXQ
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
