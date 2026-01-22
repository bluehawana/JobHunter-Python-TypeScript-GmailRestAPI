#!/usr/bin/env python3
"""
Test template replacement locally
"""

import sys
sys.path.append('backend')

from app.lego_api import customize_cover_letter

# Load ALTEN template
with open('job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CL.tex', 'r') as f:
    template = f.read()

print("Original template header:")
print(template[:500])
print("\n" + "="*70 + "\n")

# Test replacement
result = customize_cover_letter(template, "Stena Metall", "Infrastructure Architect")

print("After replacement header:")
print(result[:500])
print("\n" + "="*70 + "\n")

# Check if replacements worked
if "COMPANY_NAME" in result:
    print("❌ COMPANY_NAME not replaced!")
if "JOB_TITLE" in result:
    print("❌ JOB_TITLE not replaced!")
if "Stena Metall" in result:
    print("✅ Stena Metall found")
if "Infrastructure Architect" in result:
    print("✅ Infrastructure Architect found")
