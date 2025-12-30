#!/usr/bin/env python3
"""
Update all CV templates to use Overleaf format with blue clickable links
"""

import re
from pathlib import Path

def update_cv_header(file_path: Path) -> bool:
    """Update CV header to new format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already updated
        if 'Harvad (Hongzhi) Li' in content and '\\textcolor{darkblue}' in content:
            print(f"✓ Already updated: {file_path.name}")
            return False
        
        # Add darkblue color definition if not present
        if 'definecolor{darkblue}' not in content:
            content = content.replace(
                '\\definecolor{titlecolor}{RGB}{0,102,204}',
                '\\definecolor{titlecolor}{RGB}{0,102,204}\n\\definecolor{darkblue}{RGB}{0,102,204}'
            )
        
        # Old header pattern
        old_pattern = r'\\begin{center}\s*\{\\Huge\\bfseries Harvad Lee\}\\\\\\[6pt\\]\s*\{\\Large ([^\}]+)\}\\\\\\[10pt\\]\s*hongzhili01@gmail\.com \| \+46 72 838 4299 \| Gothenburg, Sweden\\\\\s*linkedin\.com/in/hzl \| github\.com/bluehawana\s*\\end{center}'
        
        # New header format
        new_header = r'''\\begin{center}
{\\LARGE \\textbf{Harvad (Hongzhi) Li}}\\\\[10pt]
{\\Large \\textit{\1}}\\\\[10pt]
\\textcolor{darkblue}{\\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \\href{tel:+46728384299}{+46 72 838 4299} | \\href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \\href{https://github.com/bluehawana}{GitHub}}
\\end{center}'''
        
        # Replace
        updated_content = re.sub(old_pattern, new_header, content, flags=re.DOTALL)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ Updated: {file_path.name}")
            return True
        else:
            print(f"⚠ No match found in: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    # Find all CV template files
    cv_files = list(Path('job_applications').rglob('*_CV.tex'))
    
    print(f"Found {len(cv_files)} CV template files\n")
    
    updated_count = 0
    for cv_file in cv_files:
        if update_cv_header(cv_file):
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count} files")
    print(f"✓ Skipped {len(cv_files) - updated_count} files (already updated or no match)")

if __name__ == '__main__':
    main()
