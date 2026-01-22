#!/usr/bin/env python3

import sys
import os
sys.path.append('backend')

from app.lego_api import build_lego_cover_letter

# Test cover letter generation
company = "Omegapoint"
title = "Java Software Developer"
role_category = "backend_developer"

print("Generating cover letter...")
cl_content = build_lego_cover_letter(
    role_type="Backend Developer",
    company=company,
    title=title,
    role_category=role_category,
    job_description="Java developer position at Omegapoint"
)

print("Generated cover letter:")
print("=" * 50)
print(cl_content[:1000])  # First 1000 characters
print("=" * 50)

# Save to file
with open('test_omegapoint_cl.tex', 'w', encoding='utf-8') as f:
    f.write(cl_content)

print("Saved to test_omegapoint_cl.tex")