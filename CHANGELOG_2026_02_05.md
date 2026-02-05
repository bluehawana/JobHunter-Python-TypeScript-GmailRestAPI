# Changelog - February 5, 2026

## 🎯 Today's Achievements: Template System Polish & Privacy Updates

### 1. Phone Number Privacy Update
**Issue:** Personal phone number exposed in all templates  
**Solution:** Changed all CV templates from `+46 72 838 4299` to `+46 76 006 7977`  
**Files Updated:** 11 CV templates  
**Commit:** `f0dc696`

---

### 2. Cover Letter Styling - LinkedIn Blue Consistency
**Issue:** Cover letter headers and footers had inconsistent colors (black text, dark blue separators)  
**Solution:** Made ALL text in headers and footers LinkedIn blue (RGB: 0,119,181)  
**Impact:** Professional, consistent branding across all documents  
**Files Updated:**
- `backend/latex_sources/cover_letter_hongzhi_li_template.tex`
- `templates/cl_templates/project_manager_cl_template.tex`

---

### 3. Cover Letter Length Optimization
**Issue:** Cover letters exceeded 1 page, unprofessional formatting  
**Solution:**
- Reduced margins from 1in to 0.75in
- Condensed verbose content to key achievements
- Tightened spacing between sections
- Used compact lists with `enumitem` package
- Removed redundant paragraphs

**Result:** All cover letters now fit perfectly on 1 page  
**Commit:** `cfeabe0`

---

### 4. Footer Formatting Fix
**Issue:** Footer was 2 lines with date right-aligned, inconsistent with header  
**Solution:** Changed footer to 3 lines, left-aligned like header:
```
Ebbe Lieberathsgatan 27
412 65, Gothenburg, Sweden
February 5, 2026
```

**Commit:** `78ea7c7`

---

### 5. Company Name Extraction Improvements
**Issue:** Company names included prepositions like "by InfiMotion" instead of "InfiMotion"  
**Solution:** Enhanced regex patterns to strip ALL prepositions:
- by, till, to, på, hos, at, for, from
- Smart company suffix detection (AB, Ltd, Inc, GmbH, AG, SA, etc.)
- Priority company list for known companies

**Files Updated:** `backend/app/lego_api.py`  
**Commits:** `715a6fa`, `ce36e57`, `2adce75`, `2d46dcb`

---

### 6. Smart PDF Filenames
**Issue:** Generic filenames like `cv.pdf` and `cl.pdf`  
**Solution:** Implemented smart naming: `cv_harvad_ArosKapital.pdf`, `cl_harvad_InfiMotion.pdf`
- Sanitizes company names (removes spaces, Swedish chars)
- Professional, organized file naming

**Files Updated:** `backend/app/lego_api.py`

---

### 7. Project Manager CV Template Enhancement
**Issue:** CV header had verbose tagline, phone number not in LinkedIn blue  
**Solution:**
- Simplified header to just job title: "Senior Project Manager"
- Made ALL contact info LinkedIn blue (email, phone, LinkedIn, GitHub)
- Clean, professional appearance

**Files Updated:** `templates/cv_templates/project_manager_template.tex`  
**Commit:** `2696286`

---

## 📊 Technical Details

### Templates Updated
- **CV Templates:** 11 files (all major role templates)
- **CL Templates:** 2 files (main + project manager)

### Key Technologies
- LaTeX formatting with `geometry`, `xcolor`, `hyperref`, `enumitem` packages
- Python regex for company name extraction
- AI-powered job parsing with GLM-4.6 (Z.AI API)

### Deployment
- All changes committed to GitHub
- Deployed to VPS: `alphavps` at `/var/www/lego-job-generator`
- Service restarted with graceful reload: `kill -HUP`

---

## ✅ Quality Checklist

- [x] All CV templates use new phone number
- [x] All CL templates have LinkedIn blue headers/footers
- [x] All CL templates fit on 1 page
- [x] Footer formatting consistent (3 lines, left-aligned)
- [x] Company name extraction removes prepositions
- [x] Smart PDF filenames implemented
- [x] All changes deployed to production
- [x] Service restarted successfully

---

## 🎨 Design Standards Established

### Cover Letter Format
```
Header (LinkedIn Blue, Left-aligned):
  COMPANY NAME
  JOB TITLE
  Gothenburg, Sweden

Body:
  - Concise opening (1 paragraph)
  - Key achievements (bullet points)
  - Core competencies (compact list)
  - Closing (1 paragraph)

Footer (LinkedIn Blue, Left-aligned):
  Ebbe Lieberathsgatan 27
  412 65, Gothenburg, Sweden
  [Today's Date]
```

### CV Format
```
Header (LinkedIn Blue, Centered):
  Name
  Job Title
  Email — Phone — LinkedIn — GitHub (all LinkedIn blue)
```

---

## 🚀 Next Steps

1. Monitor production for any formatting issues
2. Collect user feedback on new templates
3. Consider adding more role-specific CL templates
4. Optimize AI company extraction accuracy

---

## 📝 Lessons Learned

1. **Consistency is Key:** Always update ALL related templates when making formatting changes
2. **Test Before Deploy:** Verify LaTeX compilation locally before pushing to production
3. **Professional Standards:** Keep formatting clean, concise, and consistent
4. **Privacy Matters:** Separate personal and professional contact information

---

**Total Commits Today:** 7  
**Files Changed:** 15+  
**Lines Changed:** ~200  
**Production Deployments:** 7  

**Status:** ✅ All systems operational, templates production-ready
