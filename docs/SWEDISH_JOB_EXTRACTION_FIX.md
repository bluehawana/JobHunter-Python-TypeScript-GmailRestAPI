# Swedish Job Site Extraction Fix

## Problem
When processing Swedish job postings (like Göteborgs Stad), the system was extracting "att" (Swedish word for "to/that") instead of the actual company name "Göteborgs Stad".

## Root Cause
The fallback company extraction logic wasn't handling Swedish job site patterns, particularly:
- Swedish-specific field labels like "Förvaltning/bolag" (Department/Company)
- Swedish section headers like "Om oss" (About us)
- Swedish phrases that were being mistaken for company names

## Solution Implemented

### 1. Created `extract_company_and_title_from_text()` Function
Added a new extraction function in `backend/app/lego_api.py` that:

**Handles Swedish Patterns:**
- Recognizes "Förvaltning/bolag" pattern (Göteborgs Stad specific)
- Looks for "Om oss" (About us) sections
- Searches for explicit mentions of "Göteborgs Stad" or "Intraservice"

**Improved Title Extraction:**
- Filters out Swedish phrases like "som ", "kommer du", "vi söker"
- Looks for job keywords in first 10 lines
- Validates title length and format

**Better Company Detection:**
- Checks for Swedish company indicators: "företag:", "arbetsgivare:", "organisation:"
- Scans text for explicit company mentions
- Filters out Swedish stop words: "att", "och", "för", "med", etc.

### 2. Updated `analyze_job_description()` Function
Modified to use the new extraction function as fallback when URL-based extraction fails.

## Test Results

### Before Fix
```
Company: att
Title: Som Azure Specialist kommer du bland annat att
```

### After Fix
```
Company: Göteborgs Stad
Title: Azure Specialist
```

## Files Modified
- `backend/app/lego_api.py` - Added `extract_company_and_title_from_text()` function
- `test_goteborg_azure_specialist.py` - Test script for Göteborgs Stad job

## Deployment

### Local Testing
```bash
python3 test_goteborg_azure_specialist.py
```

### Deploy to VPS
```bash
./deploy/deploy_goteborg_fix.sh
```

## Verification Steps

### 1. Test with URL
```bash
# Paste job URL: https://goteborg.se/wps/portal/start/jobba-i-goteborgs-stad/lediga-jobb?id=893909
# Should extract: Company="Göteborgs Stad", Title="Azure Specialist"
```

### 2. Test with Job Description Text Only
```bash
# Paste the Swedish job description text
# Should extract: Company="Göteborgs Stad", Title="Azure Specialist"
```

### 3. Check Cover Letter
```bash
# Verify cover letter header shows:
# Göteborgs Stad
# Azure Specialist
# Gothenburg, Sweden
```

## Supported Patterns

### Swedish Job Sites
- ✅ Göteborgs Stad (goteborg.se)
- ✅ Swedish government job portals
- ✅ Jobs with "Förvaltning/bolag" field
- ✅ Jobs with "Om oss" sections

### International Job Sites
- ✅ LinkedIn
- ✅ Indeed
- ✅ Company career pages
- ✅ Jobs with "Company - Title" format
- ✅ Jobs with "Title | Company" format

## Future Improvements
1. Add support for more Swedish job portals (Arbetsförmedlingen, etc.)
2. Handle Norwegian and Danish job sites
3. Improve extraction for government agencies with long names
4. Add caching for frequently seen company names

## Related Files
- `backend/linkedin_job_extractor.py` - URL-based extraction
- `backend/app/lego_api.py` - Main analysis and extraction logic
- `test_goteborg_azure_specialist.py` - Test case for Swedish jobs
