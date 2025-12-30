# Deployment Instructions - Template Library Update

## Files Deployed ✅
- ✅ `backend/cv_templates.py` - Updated with real job_applications templates
- ✅ `backend/app/lego_api.py` - Fixed skills reordering regex

## Service Status
Service is currently running (started at 12:45:30 CET):
- Main PID: 12450
- Workers: 3 (PIDs: 12455, 12456, 12457)
- Memory: 135.4M

## Manual Restart Required

Since sudo requires password, please restart the service manually:

```bash
# SSH to VPS
ssh -p 1025 harvad@alphavps

# Enter password: 11

# Restart service
sudo systemctl restart lego-backend.service

# Verify service is running
sudo systemctl status lego-backend.service

# Check logs for any errors
sudo journalctl -u lego-backend.service -n 50 --no-pager
```

## What Changed

### 1. Template Selection
- **DevOps jobs** now use `alten_cloud` template (NO banking content)
- **FinTech jobs** use `nasdaq_devops_cloud` template (WITH banking content)
- **AI jobs** use `omnimodular` template (NO banking content)
- **Android jobs** use `ecarx_android_developer` template

### 2. Skills Reordering
- Fixed regex pattern to correctly match LaTeX `\item` lines
- Now successfully reorders 9 skill categories based on JD keywords
- Adds comment: `% Skills reordered based on job requirements`

## Testing After Restart

### Test 1: DevOps Job (Should use ALTEN template)
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Senior DevOps Engineer needed. Kubernetes, Docker, Terraform, AWS experience required."
  }'
```

Expected: `roleCategory: "devops_cloud"`, template should be `alten_cloud`

### Test 2: FinTech Job (Should use Nasdaq template)
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "DevOps Engineer for financial services. Experience with payment systems and banking operations preferred."
  }'
```

Expected: `roleCategory: "devops_fintech"`, template should be `nasdaq_devops_cloud`

### Test 3: Generate CV and Check Skills Reordering
```bash
# Generate a CV and check if skills reordering comment appears
curl -X POST http://localhost:5000/api/generate-lego-application \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Senior DevOps Engineer. Kubernetes, Terraform, AWS.",
    "analysis": {
      "roleType": "Devops Cloud",
      "roleCategory": "devops_cloud",
      "company": "Test Company",
      "title": "Senior DevOps Engineer"
    }
  }'

# Download the generated CV and check for:
# 1. "% Skills reordered based on job requirements" comment
# 2. No banking content in the CV
# 3. Skills ordered with Kubernetes, Terraform, AWS at the top
```

## Success Criteria
- ✅ Service restarts without errors
- ✅ DevOps jobs use ALTEN template (no banking)
- ✅ FinTech jobs use Nasdaq template (with banking)
- ✅ Skills reordering comment appears in generated CVs
- ✅ Skills are reordered based on JD keywords

## Rollback Plan (If Needed)
If issues occur, rollback to previous version:

```bash
cd /var/www/lego-job-generator
git log --oneline -5  # Find previous commit
git checkout <previous-commit-hash> backend/cv_templates.py backend/app/lego_api.py
sudo systemctl restart lego-backend.service
```

## Next Steps After Successful Deployment
1. Test with real job descriptions via web UI
2. Verify CV generation works for all role types
3. Check that banking content only appears for FinTech jobs
4. Monitor logs for any errors: `sudo journalctl -u lego-backend.service -f`
