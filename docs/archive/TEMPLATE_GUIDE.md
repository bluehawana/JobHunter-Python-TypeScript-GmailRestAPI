# LaTeX Template Guide - Overleaf Styling

## ✅ Templates Saved

### CV Template

**Location**: `templates/cv_template_overleaf.tex`

**Features**:

- Professional Overleaf styling with dark blue accents
- FontAwesome icons support
- Clean section formatting with horizontal rules
- ATS-friendly layout
- Hyperlinked contact information

**Placeholders**:

- `JOB_TITLE_PLACEHOLDER` - Job title
- `PROFILE_SUMMARY_PLACEHOLDER` - Profile summary
- `SKILLS_PLACEHOLDER` - Technical skills list
- `EXPERIENCE_PLACEHOLDER` - Work experience
- `PROJECTS_PLACEHOLDER` - Projects section

### Cover Letter Template

**Location**: `templates/cl_template_overleaf.tex`

**Features**:

- Clean professional layout
- Dark blue color scheme matching CV
- Proper spacing and formatting
- Contact information footer with horizontal rule

**Placeholders**:

- `COMPANY_NAME_PLACEHOLDER` - Company name
- `DEPARTMENT_PLACEHOLDER` - Department/team
- `ADDRESS_PLACEHOLDER` - Company address
- `LETTER_CONTENT_PLACEHOLDER` - Main letter content

## 🎯 Essity Application - COMPLETED

### Files Generated:

1. **Essity_Cloud_DevOps_CV_Overleaf.pdf** (110.3 KB) ✅
2. **Essity_Cloud_DevOps_CL_Overleaf.pdf** (42.4 KB) ✅

### Location:

`job_applications/essity/`

### Key Highlights:

- ✅ 4+ years Azure/AWS/GCP experience
- ✅ DevOps toolchains: Docker, Terraform, Azure DevOps, Helm
- ✅ CI/CD multi-staging expertise
- ✅ Programming: Python, C#, Go
- ✅ 40% cost reduction achievement
- ✅ 25% CI/CD performance improvement
- ✅ Sustainability focus aligned with Essity's goals

## 🚀 How to Use Templates for Future Applications

### Method 1: Using Python Script

```python
from pathlib import Path

# Read template
cv_template = Path('templates/cv_template_overleaf.tex').read_text()

# Replace placeholders
cv_template = cv_template.replace('JOB_TITLE_PLACEHOLDER', 'Cloud DevOps Engineer')
cv_template = cv_template.replace('PROFILE_SUMMARY_PLACEHOLDER', 'Your summary...')
# ... more replacements

# Save
Path('output/cv.tex').write_text(cv_template)
```

### Method 2: Compile with pdflatex

```bash
pdflatex -interaction=nonstopmode -output-directory=output cv.tex
```

## 📋 Template Checklist

When creating new applications:

- [ ] Copy templates from `templates/` folder
- [ ] Replace all placeholders with job-specific content
- [ ] Tailor skills section to match job requirements
- [ ] Highlight relevant projects and achievements
- [ ] Update company name and address in cover letter
- [ ] Compile with pdflatex
- [ ] Review PDFs for formatting
- [ ] Save to `job_applications/[company_name]/` folder

## 🔧 System Requirements

### Installed:

- ✅ MiKTeX 24.1 (LaTeX for Windows)
- ✅ pdflatex compiler
- ✅ Python 3.x

### LaTeX Packages Used:

- geometry (page layout)
- enumitem (list formatting)
- titlesec (section formatting)
- xcolor (colors)
- hyperref (hyperlinks)
- fontawesome (icons)

## 💡 Tips

1. **Always use Overleaf templates** - They have the professional styling you prefer
2. **Test compile** - Always compile after making changes to catch errors early
3. **Keep backups** - Save both .tex and .pdf files
4. **Consistent naming** - Use format: `CompanyName_Position_Type_Date.tex`
5. **Version control** - Keep templates in `templates/` folder, applications in `job_applications/`

## 🎨 Color Scheme

- **Dark Blue**: RGB(0,51,102) - Used for headers, links, accents
- **Light Gray**: RGB(128,128,128) - Used for subtle elements

## 📝 Next Steps for New Applications

1. Copy templates from `templates/` folder
2. Create new folder: `job_applications/[company_name]/`
3. Customize content for the specific job
4. Compile with pdflatex
5. Review and submit!

---

**Last Updated**: October 2, 2025
**Templates Version**: 1.0 (Overleaf Style)
