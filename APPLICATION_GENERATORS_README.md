# 🧱 Job Application Generators - LEGO Bricks System

## 📁 Main Application Generators (Root Directory)

These are the **NEWEST** and **MOST IMPORTANT** scripts using the LEGO Bricks methodology:

### 🎯 Active Generators (Use These!)

1. **`create_tata_incident_management.py`** ⭐ NEWEST (Dec 16, 2025)
   - **Role:** Incident Management Specialist / DevOps / SRE
   - **Company:** Tata Technologies
   - **Features:** 
     - LEGO bricks modular architecture
     - Role-specific profile, skills, and experience assembly
     - ATS-optimized keywords
     - Quantified achievements (26-server incident, 45% cost reduction, 35% MTTR reduction)
     - Professional blue styling for CV and cover letter
   - **Usage:** `python3 create_tata_incident_management.py`

2. **`create_doit_fullstack.py`** (Dec 12, 2025)
   - **Role:** Full Stack Engineer (Frontend-Oriented)
   - **Company:** DoiT International
   - **Features:**
     - LEGO bricks for fullstack/frontend roles
     - React, TypeScript, cloud intelligence focus
     - Gemini AI content polishing
   - **Usage:** `python3 create_doit_fullstack.py`

3. **`send_lego_bricks_ecarx.py`** (Dec 12, 2025)
   - **Role:** Android Developer
   - **Company:** ECARX
   - **Features:**
     - Email automation
     - Android-focused LEGO bricks assembly
     - Automotive technology emphasis

### 🤖 Cleaning Robot Application (Chinese Market)

4. **`compile_cleaning_robot_online.py`** (Dec 14, 2025)
   - Compiles Chinese CV and cover letter for Keenon Robotics
   - Includes 2寸 photo, Chinese language, blue styling

5. **`compile_cleaning_robot_cv.py`** & **`compile_cleaning_robot_cl.py`**
   - Individual CV and CL compilers for cleaning robot position

6. **`create_cleaning_robot_cv.py`**
   - Generator for cleaning robot CV

---

## 📂 Organized Scripts Folders

### `scripts/utilities/`
Utility scripts for common tasks:
- `crop_photo_2inch.py` - Crop photos to 2寸 (3.5cm x 5.3cm) for Chinese CVs
- `open_pdf.py` - Open PDF files automatically
- `open_tata_cv.py` - Quick open Tata CV
- `open_cleaning_robot_cv_in_overleaf.py` - Open in Overleaf

### `scripts/automation/`
Automation and scheduling scripts:
- `run_06_00_automation.py` - Daily 6:00 AM job automation
- `daily_06_00_scheduler.py` - Scheduler configuration
- `heroku_scheduler_endpoint.py` - Heroku integration
- `simple_gmail_scanner.py` - Gmail job scanning
- `manual_job_input.py` - Manual job entry

### `scripts/archive_old_applications/`
Old application generators (archived):
- Kollmorgen applications (multiple versions)
- Eworks applications
- ECARX specialized versions
- Essity applications
- Opera DevOps applications

### `scripts/archive_tests/`
Test and debugging scripts (archived):
- All `test_*.py` files
- R2/Overleaf integration tests
- API tests (Gemini, Claude)
- Company extraction tests

---

## 🧱 LEGO Bricks Methodology

The newest generators use a **modular "LEGO bricks" approach**:

### Key Concepts:

1. **Profile Bricks** - Different profile summaries for different roles
   - `incident_management_specialist`
   - `devops_engineer`
   - `fullstack_developer`
   - `android_developer`

2. **Skills Bricks** - Skills ordered by role priority
   - `incident_management_primary` - Incident response, monitoring, RCA first
   - `devops_primary` - CI/CD, IaC, cloud platforms first
   - `fullstack_primary` - React, TypeScript, APIs first

3. **Experience Bricks** - Role-specific experience descriptions
   - `ecarx_incident_focused` - 24/7 on-call, 26-server incident, monitoring
   - `ecarx_devops_focused` - CI/CD pipelines, infrastructure automation
   - `ecarx_fullstack_focused` - React dashboards, API design

4. **Dynamic Assembly** - CV is rebuilt based on job requirements
   - Analyze job description
   - Select appropriate bricks
   - Assemble tailored CV
   - Generate professional PDF

### Benefits:

✅ **Higher ATS scores** - Keywords match job requirements exactly
✅ **Role-specific identity** - Not generic, matches job title
✅ **Quantified achievements** - Numbers prominently featured
✅ **Professional styling** - Blue accents, clean layout
✅ **Time savings** - No manual CV editing needed

---

## 🎯 How to Create a New Application

### Step 1: Identify the Role Type
- Incident Management / DevOps / SRE → Use `create_tata_incident_management.py` as template
- Full Stack / Frontend → Use `create_doit_fullstack.py` as template
- Android / Mobile → Use `send_lego_bricks_ecarx.py` as template

### Step 2: Copy and Modify
```bash
cp create_tata_incident_management.py create_new_company_role.py
```

### Step 3: Update LEGO Bricks
- Modify `PROFILE_BRICKS` for role-specific summary
- Reorder `SKILLS_BRICKS` by priority
- Adjust `EXPERIENCE_BRICKS` to emphasize relevant achievements

### Step 4: Generate Application
```bash
python3 create_new_company_role.py
```

---

## 📊 Success Metrics

### ECARX Application (LEGO Bricks):
- ✅ 6/6 Android indicators found
- ✅ CV rebuilt from fullstack to Android developer identity
- ✅ Projects reordered (AndroidAuto first)
- ✅ Skills reordered (Kotlin, Android Studio first)

### Tata Application (LEGO Bricks):
- ✅ Incident Management Specialist identity (not generic DevOps)
- ✅ 26-server incident prominently featured
- ✅ Quantified achievements: 45% cost reduction, 35% MTTR reduction
- ✅ ATS-optimized keywords: Terraform, Kubernetes, Prometheus, Grafana

---

## 🚀 Quick Reference

**Need to create a new application?**
1. Paste job description to Kiro
2. Identify role type (DevOps/SRE, Fullstack, Android, etc.)
3. Use the appropriate template from root directory
4. LEGO bricks will assemble the perfect CV automatically

**Main generators are in root directory - easy to find!** 🎯
