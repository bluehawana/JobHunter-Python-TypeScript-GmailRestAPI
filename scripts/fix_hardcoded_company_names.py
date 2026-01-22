#!/usr/bin/env python3
"""
Replace hardcoded company names and job titles with placeholders in CL templates
"""

import re
from pathlib import Path

def fix_cl_template(file_path):
    """Fix hardcoded company names in a CL template"""
    print(f"\n📝 Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Extract company name from filename or path
    # e.g., "ALTEN_Cloud_Engineer_Harvad_CL.tex" -> "ALTEN"
    filename = file_path.stem
    parts = filename.split('_')
    
    # Common patterns to detect company name in header
    # Pattern 1: Company name at start of document after \begin{document}
    # Look for: CompanyName\\ or {\color{linkedinblue}CompanyName\\
    
    # Find the header section (between \begin{document} and first \vspace)
    header_match = re.search(
        r'(\\begin\{document\}.*?% Header[^\n]*\n)(.*?)(\\vspace\{1cm\})',
        content,
        re.DOTALL
    )
    
    if header_match:
        header_section = header_match.group(2)
        
        # Check if already using placeholders
        if 'COMPANY_NAME' in header_section or 'JOB_TITLE' in header_section:
            print(f"✓ Already using placeholders")
            return False
        
        # Extract lines from header
        header_lines = [line.strip() for line in header_section.strip().split('\n') if line.strip()]
        
        # Filter out color commands and empty lines
        clean_lines = []
        for line in header_lines:
            # Remove color wrappers
            line = re.sub(r'{\s*\\color\{[^}]+\}\s*', '', line)
            line = re.sub(r'\s*}$', '', line)
            if line and not line.startswith('%'):
                clean_lines.append(line)
        
        if len(clean_lines) >= 2:
            # First line is usually company, second is job title
            company_line = clean_lines[0].replace('\\\\', '').strip()
            title_line = clean_lines[1].replace('\\\\', '').strip()
            
            print(f"   Found company: '{company_line}'")
            print(f"   Found title: '{title_line}'")
            
            # Replace in header section
            new_header = header_section
            
            # Replace company name (preserve color if present)
            if '\\color{linkedinblue}' in new_header:
                new_header = re.sub(
                    r'({\s*\\color\{linkedinblue\})\s*' + re.escape(company_line) + r'\\',
                    r'\1COMPANY_NAME\\',
                    new_header
                )
            else:
                new_header = new_header.replace(company_line + '\\\\', 'COMPANY_NAME\\\\')
            
            # Replace job title
            new_header = new_header.replace(title_line + '\\\\', 'JOB_TITLE\\\\')
            
            # Replace in full content
            content = content.replace(header_section, new_header)
            
            # Also replace in body text
            # Pattern: "for the [Title] position at [Company]"
            content = re.sub(
                r'for the ' + re.escape(title_line) + r' position at ' + re.escape(company_line),
                r'for the JOB_TITLE position at COMPANY_NAME',
                content,
                flags=re.IGNORECASE
            )
            
            # Pattern: "contribute to [Company]'s"
            content = re.sub(
                r'contribute to ' + re.escape(company_line) + r"'s",
                r"contribute to COMPANY_NAME's",
                content,
                flags=re.IGNORECASE
            )
            
            # Pattern: "at [Company]."
            content = re.sub(
                r'at ' + re.escape(company_line) + r'\.',
                r'at COMPANY_NAME.',
                content
            )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated with placeholders")
        return True
    else:
        print(f"⏭️  No changes needed")
        return False

def main():
    """Fix all CL templates"""
    print("🔄 Replacing hardcoded company names with placeholders")
    print("=" * 70)
    
    # Find all CL templates
    job_apps_dir = Path('job_applications')
    cl_files = list(job_apps_dir.glob('**/*_CL.tex'))
    
    print(f"\n📋 Found {len(cl_files)} CL templates")
    
    updated_count = 0
    for cl_file in cl_files:
        if fix_cl_template(cl_file):
            updated_count += 1
    
    print(f"\n" + "=" * 70)
    print(f"✅ Updated {updated_count} out of {len(cl_files)} CL templates")

if __name__ == '__main__':
    main()
