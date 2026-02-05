#!/usr/bin/env python3
"""
Simple test for cover letter placeholder replacement
"""

import re

def customize_cover_letter(template_content: str, company: str, title: str) -> str:
    """Customize cover letter template with company and title"""
    # Clean up title - remove leading articles (an, a, the)
    if title:
        title = re.sub(r'^(an?|the)\s+', '', title, flags=re.IGNORECASE).strip()
        # Capitalize first letter of each word, but preserve acronyms
        title = title.title() if title else title
        # Restore common acronyms that .title() would break
        acronyms = ['IT', 'AI', 'API', 'CI/CD', 'DevOps', 'SRE', 'UI', 'UX', 'QA', 'BI', 'ERP', 'CRM', 'HR', 'AWS', 'GCP', 'iOS', 'ML']
        for acronym in acronyms:
            title = re.sub(r'\b' + acronym.title() + r'\b', acronym, title, flags=re.IGNORECASE)

    # Replace placeholders - handle multiple formats
    if company and company != 'Company':
        template_content = template_content.replace('COMPANY_NAME_PLACEHOLDER', company)  # New format
        template_content = template_content.replace('[COMPANY NAME]', company)
        template_content = template_content.replace('[Company Name]', company)
        template_content = template_content.replace('{company_name}', company)
        template_content = template_content.replace('COMPANY\\_NAME', company)  # LaTeX escaped
        template_content = template_content.replace('COMPANY_NAME', company)    # Regular

    # Replace position/job title placeholders
    if title and title != 'Position':
        template_content = template_content.replace('JOB_TITLE_PLACEHOLDER', title)  # New format
        template_content = template_content.replace('[JOB TITLE]', title)
        template_content = template_content.replace('[Position]', title)
        template_content = template_content.replace('{job_title}', title)
        template_content = template_content.replace('JOB\\_TITLE', title)  # LaTeX escaped
        template_content = template_content.replace('JOB_TITLE', title)    # Regular

    return template_content


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

# Check for color issues
if '{\\color{lightblue}COMPANY_NAME_PLACEHOLDER' in template:
    print("⚠️  Original template has color wrapping company placeholder")
if '{\\color{lightblue}' + company in customized:
    print("❌ Company name is wrapped in color block!")
else:
    print("✅ Company name is NOT wrapped in color block")

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
        for j in range(i, min(i+15, len(lines))):
            print(lines[j])
        break

# Try to compile
print("\n" + "=" * 80)
print("Attempting PDF compilation...")
import subprocess
result = subprocess.run(
    ['pdflatex', '-interaction=nonstopmode', output_file],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ PDF compiled successfully!")
    print(f"   Output: test_aros_kapital_cl.pdf")
else:
    print("❌ PDF compilation failed")
    if 'error' in result.stdout.lower():
        print("Errors found in output")
