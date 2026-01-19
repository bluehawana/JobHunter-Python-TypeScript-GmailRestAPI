#!/usr/bin/env python3
"""
Fix all CL template footers to use LinkedIn blue with correct formatting
"""

import os
import re
from pathlib import Path

def fix_footer(file_path):
    """Fix footer in a CL template"""
    print(f"\n📝 Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find and replace the footer section
    # Look for the line separator and everything after it until \end{document}
    footer_pattern = r'(% Line separator\s*\n\{\\color\{linkedinblue\}\\hrule height 0\.5pt\}\s*\n\s*\\vspace\{0\.3cm\}\s*\n\s*)% Footer.*?\\end\{document\}'
    
    new_footer = r'\1% Footer with address and date\n{\\color{linkedinblue}Ebbe Lieberathsgatan 27\\\\\n41265, Gothenburg, Sweden\\\\\n\\hfill \\today}\n\n\\end{document}'
    
    content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated footer in: {file_path}")
        return True
    else:
        print(f"⏭️  No changes needed: {file_path}")
        return False

def main():
    """Fix all CL template footers"""
    print("🔄 Fixing all CL template footers with LinkedIn blue styling")
    print("=" * 70)
    
    # Find all CL templates
    job_apps_dir = Path('job_applications')
    cl_files = list(job_apps_dir.glob('**/*_CL.tex'))
    
    print(f"\n📋 Found {len(cl_files)} CL templates")
    
    updated_count = 0
    for cl_file in cl_files:
        if fix_footer(cl_file):
            updated_count += 1
    
    print(f"\n" + "=" * 70)
    print(f"✅ Updated {updated_count} out of {len(cl_files)} CL templates")

if __name__ == '__main__':
    main()
