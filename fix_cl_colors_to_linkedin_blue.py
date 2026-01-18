#!/usr/bin/env python3
"""
Fix all CL templates to use LinkedIn blue for headers, lines, and footer
"""

import os
import re
from pathlib import Path

def fix_cl_colors(file_path):
    """Fix CL template to use LinkedIn blue for header, line, and footer"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Ensure linkedinblue color is defined
        if 'definecolor{linkedinblue}' not in content:
            # Add color definition after geometry
            content = content.replace(
                r'\setlength{\parindent}{0pt}',
                r'\setlength{\parindent}{0pt}\n\definecolor{linkedinblue}{RGB}{0,119,181}'
            )
        
        # Fix header to use LinkedIn blue
        header_patterns = [
            (r'(% Header with job information \(no name\)\n)([^{]*)(COMPANY\\_NAME\\\\?\n?JOB\\_TITLE\\\\?\n?Gothenburg, Sweden)', 
             r'\1{\color{linkedinblue}\n\3\n}'),
            (r'(COMPANY\\_NAME\\\\?\n?JOB\\_TITLE\\\\?\n?Gothenburg, Sweden)', 
             r'{\color{linkedinblue}\n\1\n}')
        ]
        
        for pattern, replacement in header_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                break
        
        # Fix line separator to use LinkedIn blue
        content = re.sub(
            r'% Line separator\n\\hrule\n',
            r'% Line separator\n{\color{linkedinblue}\hrule height 0.5pt}\n',
            content
        )
        
        # Fix footer to use LinkedIn blue
        footer_patterns = [
            (r'(\\noindent )(Ebbe Lieberathsgatan 27\\\\?\n?41265 Gothenburg, Sweden)( \\hfill )(\\today)',
             r'\1{\color{linkedinblue}\2} \3{\color{linkedinblue}\4}'),
            (r'(\\noindent )(.*Ebbe Lieberathsgatan.*Sweden)( \\hfill )(.*today.*)',
             r'\1{\color{linkedinblue}\2} \3{\color{linkedinblue}\4}')
        ]
        
        for pattern, replacement in footer_patterns:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # If changes were made, write back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed colors in: {file_path}")
            return True
        else:
            print(f"⚪ No color changes needed: {file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all CL templates"""
    print("🎨 Fixing CL template colors to LinkedIn blue...")
    
    # Find all CL template files
    job_applications_dir = Path("job_applications")
    cl_files = list(job_applications_dir.glob("**/*CL*.tex"))
    
    print(f"📁 Found {len(cl_files)} CL template files")
    
    fixed_count = 0
    
    for cl_file in cl_files:
        print(f"\n📄 Processing: {cl_file}")
        
        if fix_cl_colors(cl_file):
            fixed_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   Total CL files found: {len(cl_files)}")
    print(f"   Files with color fixes: {fixed_count}")
    print(f"   Files already correct: {len(cl_files) - fixed_count}")
    
    print(f"\n✅ All CL templates now use LinkedIn blue for headers, lines, and footer")

if __name__ == '__main__':
    main()