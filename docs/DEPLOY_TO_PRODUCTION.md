# Deploy to jobs.bluehawana.com

## Recent Changes

✅ Swedish job site extraction (Göteborgs Stad support)
✅ LinkedIn blue CL footer format (all templates)
✅ Expanded CV certifications section with Power BI, Tableau, Visio
✅ Updated backend template generation code

## Quick Deployment (Recommended)

### Using the Deployment Script

```bash
# One-command deployment via Git
./deploy/deploy_via_git.sh
```

This script will:
1. Show current git status
2. Optionally commit and push your changes
3. SSH to VPS and pull latest changes
4. Restart the service
5. Show service status

### Manual Git Deployment

```bash
# 1. Commit and push changes locally
git add .
git commit -m "Your commit message"
git push origin main

# 2. SSH to VPS and pull changes
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
git pull origin main
sudo systemctl restart lego-job-generator
sudo systemctl status lego-job-generator
exit
```

## Alternative Deployment Methods

### Option 1: Direct File Upload (Not Recommended)

Only use if git is not available:

```bash
# Upload specific files via SCP
scp -P 1025 backend/app/lego_api.py harvad@94.72.141.71:/var/www/lego-job-generator/backend/app/

# SSH and restart
ssh -p 1025 harvad@94.72.141.71
sudo systemctl restart lego-job-generator
```

### Option 2: CI/CD Pipeline (Future)

Set up GitHub Actions for automatic deployment on push to main branch.

## Verification After Deployment

### Test 1: Swedish Job Site (Göteborgs Stad)

1. Go to https://jobs.bluehawana.com
2. Paste job URL: `https://goteborg.se/wps/portal/start/jobba-i-goteborgs-stad/lediga-jobb?id=893909`
3. Or paste the Swedish job description text
4. Generate cover letter
5. Verify header shows:
   - Company: "Göteborgs Stad" (NOT "att" or "Company")
   - Title: "Azure Specialist" (NOT "Som Azure Specialist kommer du...")
   - Location: "Gothenburg, Sweden"

### Test 2: Check CL Footer Format

1. Generate any cover letter
2. Check footer has:
   - LinkedIn blue color
   - Address on 2 lines
   - Date on same line with address

### Test 3: Check Role Detection

1. Paste Stena Infrastructure Architect job
2. Should detect as "DevOps Cloud" or "Infrastructure"
3. Header should show correct company and title (not placeholders)

### Test 4: Check CV Certifications

1. Generate CV for IT Business Analyst role
2. Check certifications section has 3 lines:
   - Cloud Certifications
   - Business Intelligence & Analytics (Power BI, Tableau)
   - Business Analysis & Modeling Tools (Visio, Miro)

## Troubleshooting

### Issue: Old templates still showing

**Solution:**
```bash
# Clear application cache
rm -rf /tmp/jobhunter_cache/*  # or wherever cache is stored

# Restart application
sudo systemctl restart jobhunter
```

### Issue: Company name not updating (still shows "ALTEN")

**Cause:** Template customization not working

**Solution:**
```bash
# Check if lego_api.py was updated
grep "COMPANY_NAME" backend/app/lego_api.py

# Should see the customize_cover_letter function
# If not, re-upload the file
```

### Issue: Role detection wrong

**Cause:** AI analysis or template matching issue

**Solution:**
```bash
# Check logs for role detection
tail -f /var/log/jobhunter/app.log | grep "Role detected"

# Should show correct role category
```

## Current Server Configuration

**Server:** jobs.bluehawana.com
**Repository:** https://github.com/bluehawana/JobHunter-Python-TypeScript-GmailRestAPI
**Branch:** main
**Last Commit:** 87dc9f8 - "Update CL footer format with LinkedIn blue and expand CV certifications section"

## Post-Deployment Checklist

- [ ] Application restarted successfully
- [ ] Health check endpoint responding
- [ ] CL footer shows LinkedIn blue format
- [ ] Company name and title correctly replaced (not showing "ALTEN")
- [ ] CV certifications section expanded to 3 lines
- [ ] Role detection working correctly
- [ ] No errors in application logs

## Need Help?

If deployment fails, check:
1. Application logs: `/var/log/jobhunter/` or `pm2 logs`
2. System logs: `journalctl -u jobhunter -f`
3. Git status: `git status` and `git log`
4. File permissions: `ls -la backend/app/lego_api.py`
