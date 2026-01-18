#!/usr/bin/env python3
"""
Update all cover letter templates to the final format matching ECARX example
- Simple header: COMPANY_NAME, JOB_TITLE, Gothenburg, Sweden
- Sincerely signature
- Footer with address and date only (no contact info)
"""

import os
import re
from pathlib import Path

def update_cl_template_final(file_path):
    """Update a single CL template to the final format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if it's already in the correct format
        if 'COMPANY\_NAME\\\\' in content and 'Sincerely,' in content and 'Ebbe Lieberathsgatan 27\\\\' in content:
            print(f"⚪ Already updated: {file_path}")
            return False
        
        # Replace centered header with simple left-aligned header
        header_pattern = r'% Header with job information \(no name\).*?\\vspace\{1cm\}'
        new_header = r'''% Header with job information (no name)
COMPANY\_NAME\\
JOB\_TITLE\\
Gothenburg, Sweden

\vspace{1cm}'''
        
        content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)
        
        # Replace signature and footer
        footer_pattern = r'\\vspace\{1cm\}.*?\\end\{document\}'
        new_footer = r'''\vspace{1cm}

Sincerely,\\
Harvad (Hongzhi) Li

\vspace{\fill}

% Line separator
\hrule

\vspace{0.3cm}

% Footer with address and date
\noindent Ebbe Lieberathsgatan 27\\
41265 Gothenburg, Sweden \hfill \today

\end{document}'''
        
        content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all CL templates"""
    print("🔍 Finding CL templates to update...")
    
    # Find all CL template files
    job_applications_dir = Path("job_applications")
    cl_files = list(job_applications_dir.glob("**/*CL*.tex"))
    
    print(f"📁 Found {len(cl_files)} CL template files")
    
    updated_count = 0
    
    for cl_file in cl_files:
        print(f"\n📄 Processing: {cl_file}")
        
        if update_cl_template_final(cl_file):
            updated_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   Total CL files found: {len(cl_files)}")
    print(f"   Files updated: {updated_count}")
    print(f"   Files already up-to-date: {len(cl_files) - updated_count}")
    
    print(f"\n✅ All cover letter templates now use the final format:")
    print(f"   • Header: COMPANY_NAME, JOB_TITLE, Gothenburg, Sweden (left-aligned)")
    print(f"   • Signature: Sincerely, Harvad (Hongzhi) Li")
    print(f"   • Footer: Address and date only (no contact info)")

if __name__ == '__main__':
    main()