# Simple Deployment Guide

## Deploy to jobs.bluehawana.com

### Step 1: Commit and Push (Mac)

```bash
git add .
git commit -m "Fix Swedish job extraction for Göteborgs Stad"
git push origin main
```

### Step 2: Pull and Restart (VPS)

```bash
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
git pull origin main
sudo systemctl restart lego-job-generator
exit
```

### Done! ✅

Test at: http://jobs.bluehawana.com

---

## Quick Verification

1. Paste Göteborgs Stad job URL or description
2. Check company shows "Göteborgs Stad" (not "att")
3. Generate cover letter
4. Verify header is correct

---

## Current Changes Ready to Deploy

✅ Swedish job site extraction (Göteborgs Stad support)
✅ Improved company name extraction from job descriptions
✅ Better handling of Swedish text patterns
✅ Filters out Swedish stop words ("att", "och", "för", etc.)

---

## VPS Details

- **Server:** 94.72.141.71:1025
- **User:** harvad
- **Path:** /var/www/lego-job-generator
- **Service:** lego-job-generator
- **URL:** http://jobs.bluehawana.com
