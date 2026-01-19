#!/usr/bin/env python3

import sys
sys.path.append('backend')

from templates.cover_letter_template import generate_tailored_cover_letter

# Test with Emerson job
job_data = {
    'title': 'It Business Analyst',
    'company': 'Emerson',
    'description': 'Business analyst role focusing on IT and business alignment',
    'location': 'Gothenburg, Sweden'
}

print("Generating cover letter with updated template...")
cl_content = generate_tailored_cover_letter(job_data)

print("Generated cover letter header:")
print("=" * 50)
lines = cl_content.split('\n')
for i, line in enumerate(lines):
    if 'begin{center}' in line:
        for j in range(i, min(i+8, len(lines))):
            print(lines[j])
        break

# Save to file
with open('test_emerson_cl_updated.tex', 'w', encoding='utf-8') as f:
    f.write(cl_content)

print("=" * 50)
print("Saved to test_emerson_cl_updated.tex")