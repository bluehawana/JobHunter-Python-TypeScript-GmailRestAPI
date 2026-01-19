#!/usr/bin/env python3

import sys
sys.path.append('backend')

from app.lego_api import build_lego_cover_letter

# Test with Emerson job (should use fallback since no it_business_analyst template)
company = "Emerson"
title = "It Business Analyst"
role_category = "it_business_analyst"

print("Generating cover letter for Emerson...")
cl_content = build_lego_cover_letter(
    role_type="IT Business Analyst",
    company=company,
    title=title,
    role_category=role_category,
    job_description="IT Business Analyst role at Emerson"
)

print("Generated cover letter header:")
print("=" * 50)
lines = cl_content.split('\n')
for i, line in enumerate(lines):
    if 'begin{center}' in line:
        for j in range(i, min(i+8, len(lines))):
            print(lines[j])
        break

# Save to file
with open('test_emerson_cl_final.tex', 'w', encoding='utf-8') as f:
    f.write(cl_content)

print("=" * 50)
print("Saved to test_emerson_cl_final.tex")