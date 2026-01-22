# Fix VPS 500 Error - PDF Compilation Failed

## Problem
The VPS is returning a 500 error: "CV PDF compilation failed"

## Quick Fix

### Step 1: SSH to VPS and Pull Latest Code

```bash
ssh -p 1025 harvad@94.72.141.71
cd /var/www/lego-job-generator
git pull origin main
```

### Step 2: Check Template Files Exist

```bash
# Should show template files
ls -la job_applications/alten_cloud/*.tex
ls -la job_applications/incluso_it_business_analyst/*.tex
ls -la job_applications/ecarx_android_developer/*.tex

# Count all templates
find job_applications -name "*_CV.tex" | wc -l  # Should be ~15+
find job_applications -name "*_CL.tex" | wc -l  # Should be ~15+
```

### Step 3: Test Python Imports

```bash
source venv/bin/activate
python3 << 'EOF'
from cv_templates import CVTemplateManager
manager = CVTemplateManager()

# Test loading a template
template = manager.load_template('devops_cloud', 'cv')
print(f"Template loaded: {len(template) if template else 0} chars")

if not template:
    print("ERROR: Template loading failed!")
else:
    print("SUCCESS: Template loading works!")
EOF
```

### Step 4: Check LaTeX Installation

```bash
which pdflatex
pdflatex --version
```

If pdflatex is not installed:
```bash
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-latex-extra
```

### Step 5: Restart Service

```bash
sudo systemctl restart lego-job-generator
sudo systemctl status lego-job-generator
```

### Step 6: Check Logs for Errors

```bash
# Check service logs
sudo journalctl -u lego-job-generator -n 50 --no-pager

# Check for specific errors
sudo journalctl -u lego-job-generator -n 100 --no-pager | grep -i "error\|failed\|exception"
```

## Common Issues and Solutions

### Issue 1: Template Files Missing

**Symptom:** `Template file does not exist` in logs

**Solution:**
```bash
cd /var/www/lego-job-generator
git pull origin main
# Make sure .gitignore allows .tex files
cat .gitignore | grep "\.tex"
```

### Issue 2: LaTeX Not Installed

**Symptom:** `pdflatex: command not found`

**Solution:**
```bash
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### Issue 3: Python Import Errors

**Symptom:** `ModuleNotFoundError` or `ImportError`

**Solution:**
```bash
cd /var/www/lego-job-generator/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 4: File Permissions

**Symptom:** `Permission denied` errors

**Solution:**
```bash
cd /var/www/lego-job-generator
sudo chown -R harvad:harvad .
chmod -R 755 job_applications/
```

### Issue 5: Outdated Code

**Symptom:** Old extraction logic (extracting "att" instead of "Göteborgs Stad")

**Solution:**
```bash
cd /var/www/lego-job-generator
git fetch origin
git reset --hard origin/main
sudo systemctl restart lego-job-generator
```

## Automated Fix Script

Run this from your Mac:

```bash
./deploy/fix_vps_now.sh
```

Or manually:

```bash
ssh -p 1025 harvad@94.72.141.71 << 'EOF'
cd /var/www/lego-job-generator
git pull origin main
source venv/bin/activate
sudo systemctl restart lego-job-generator
sudo systemctl status lego-job-generator --no-pager
EOF
```

## Verify Fix

1. Go to http://jobs.bluehawana.com
2. Paste a job description
3. Click "Generate Application"
4. Should see PDF download (not 500 error)

## Still Not Working?

Run diagnostic script:
```bash
./deploy/diagnose_vps.sh
```

Then check the output for specific errors and address them.
