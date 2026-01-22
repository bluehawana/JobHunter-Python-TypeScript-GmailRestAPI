#!/usr/bin/env python3
"""
Update all CL templates with LinkedIn blue header and footer styling
"""

import os
import re
from pathlib import Path

def update_cl_template(file_path):
    """Update a single CL template with correct header/footer styling"""
    print(f"\n📝 Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Extract company name and job title from existing header
    # Look for patterns like: COMPANY\\nJOB_TITLE\\n or Company\\Job Title\\
    header_match = re.search(r'\\begin\{document\}.*?(?:{\s*(?:\\color\{[^}]+\})?\s*([^\\\n]+)\\+\s*([^\\\n]+)\\+\s*(?:Gothenburg|Stockholm)', content, re.DOTALL)
    
    if not header_match:
        print(f"⚠️  Could not find header pattern in {file_path}")
        return False
    
    # Fix header: ensure it has LinkedIn blue color
    # Pattern: {\color{linkedinblue}COMPANY\\TITLE\\Gothenburg, Sweden}
    content = re.sub(
        r'(\\begin\{document\}\s*\n\s*% Header[^\n]*\n)(?:{\s*(?:\\color\{[^}]+\})?\s*)?([^\\\n]+)\\+\s*([^\\\n]+)\\+\s*([^\\\n}]+)\s*}?',
        r'\1{\\color{linkedinblue}\2\\\\\n\3\\\\\n\4}',
        content,
        count=1
    )
    
    # Fix footer: ensure it has LinkedIn blue color and correct format
    # Pattern: {\color{linkedinblue}Ebbe Lieberathsgatan 27\\41265, Gothenburg, Sweden\\\hfill \today}
    footer_pattern = r'(% Line separator\s*\n{\s*\\color\{linkedinblue\}\\hrule height 0\.5pt\}\s*\n\s*\\vspace\{0\.3cm\}\s*\n\s*% Footer[^\n]*\n).*?(\\end\{document\})'
    
    new_footer = r'\1{\\color{linkedinblue}Ebbe Lieberathsgatan 27\\\\\n41265, Gothenburg, Sweden\\\\\n\\hfill \\today}\n\n\2'
    
    content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
    
    # Ensure LinkedIn blue is defined
    if 'definecolor{linkedinblue}' not in content:
        content = content.replace(
            r'\setlength{\parindent}{0pt}',
            r'\setlength{\parindent}{0pt}\n\\definecolor{linkedinblue}{RGB}{0,119,181}'
        )
    
    # Ensure hyperref uses LinkedIn blue
    if 'hypersetup' in content and 'linkedinblue' not in content.split('hypersetup')[1].split('}')[0]:
        content = re.sub(
            r'\\hypersetup\{[^}]*\}',
            r'\\hypersetup{colorlinks=true, linkcolor=linkedinblue, urlcolor=linkedinblue}',
            content
        )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated: {file_path}")
        return True
    else:
        print(f"⏭️  No changes needed: {file_path}")
        return False

def main():
    """Update all CL templates"""
    print("🔄 Updating all CL templates with LinkedIn blue header/footer styling")
    print("=" * 70)
    
    # Find all CL templates
    job_apps_dir = Path('job_applications')
    cl_files = list(job_apps_dir.glob('**/*_CL.tex'))
    
    print(f"\n📋 Found {len(cl_files)} CL templates")
    
    updated_count = 0
    for cl_file in cl_files:
        if update_cl_template(cl_file):
            updated_count += 1
    
    print(f"\n" + "=" * 70)
    print(f"✅ Updated {updated_count} out of {len(cl_files)} CL templates")
    print(f"⏭️  Skipped {len(cl_files) - updated_count} templates (no changes needed)")

if __name__ == '__main__':
    main()
