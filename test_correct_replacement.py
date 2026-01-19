#!/usr/bin/env python3

# Read the correct template
with open('correct_cl_template.tex', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace placeholders
company = "Emerson"
job_title = "It Business Analyst"

result = template.replace('COMPANY_NAME', company).replace('JOB_TITLE', job_title)

# Save result
with open('test_emerson_cl_fixed.tex', 'w', encoding='utf-8') as f:
    f.write(result)

print("Generated test_emerson_cl_fixed.tex")
print("Header preview:")
print("=" * 50)
lines = result.split('\n')
for i, line in enumerate(lines):
    if 'begin{center}' in line:
        for j in range(i, min(i+6, len(lines))):
            print(lines[j])
        break