#!/usr/bin/env python3
"""
Test cover letter generation for Aros Kapital
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.lego_api import customize_cover_letter

# Load the cover letter template
with open('backend/latex_sources/cover_letter_hongzhi_li_template.tex', 'r') as f:
    template = f.read()

# Test with Aros Kapital
company = "Aros Kapital"
title = "IT Support Specialist"

print(f"Testing cover letter for: {company} - {title}")
print("=" * 80)

# Customize
customized = customize_cover_letter(template, company, title)

# Check for placeholders
if 'COMPANY_NAME_PLACEHOLDER' in customized:
    print("❌ COMPANY_NAME_PLACEHOLDER not replaced!")
else:
    print("✅ COMPANY_NAME_PLACEHOLDER replaced")

if 'JOB_TITLE_PLACEHOLDER' in customized:
    print("❌ JOB_TITLE_PLACEHOLDER not replaced!")
else:
    print("✅ JOB_TITLE_PLACEHOLDER replaced")

# Check for company name
if company in customized:
    print(f"✅ Company name '{company}' found in document")
    count = customized.count(company)
    print(f"   Found {count} occurrences")
else:
    print(f"❌ Company name '{company}' NOT found!")

# Check for title
if title in customized:
    print(f"✅ Job title '{title}' found in document")
    count = customized.count(title)
    print(f"   Found {count} occurrences")
else:
    print(f"❌ Job title '{title}' NOT found!")

# Check for color issues - should NOT have all text in color blocks
header_section = customized[customized.find('\\begin{document}'):customized.find('Dear Hiring Manager')]
if '{\\color{lightblue}' in header_section and 'COMPANY_NAME_PLACEHOLDER' not in header_section:
    print("⚠️  Warning: Color block found in header (check if text is colored)")
else:
    print("✅ No problematic color blocks in header")

# Save test output
output_file = 'test_aros_kapital_cl.tex'
with open(output_file, 'w') as f:
    f.write(customized)

print(f"\n✅ Test output saved to: {output_file}")
print("\nHeader preview:")
print("=" * 80)
lines = customized.split('\n')
for i, line in enumerate(lines):
    if '\\begin{document}' in line:
        for j in range(i, min(i+10, len(lines))):
            print(lines[j])
        break
