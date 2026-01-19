#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append('backend')

from app.lego_api import build_lego_cover_letter

print("🔄 Regenerating Emerson cover letter with LinkedIn blue header...")

# Generate new cover letter
cl_content = build_lego_cover_letter(
    role_type="IT Business Analyst",
    company="Emerson",
    title="IT Business Analyst",
    role_category="it_business_analyst",
    job_description="IT Business Analyst role at Emerson"
)

# Save to file
with open('job_applications/emerson_it_business_analyst/Emerson_IT_Business_Analyst_CL_NEW.tex', 'w', encoding='utf-8') as f:
    f.write(cl_content)

print("✓ New cover letter saved: Emerson_IT_Business_Analyst_CL_NEW.tex")
print("Header preview:")
print("=" * 50)
lines = cl_content.split('\n')
for i, line in enumerate(lines):
    if 'Emerson' in line:
        for j in range(i, min(i+5, len(lines))):
            print(lines[j])
        break