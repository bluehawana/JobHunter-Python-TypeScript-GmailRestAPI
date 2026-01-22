#!/usr/bin/env python3
"""
Fix all CV templates to use LinkedIn blue instead of dark blue
"""

import os
import re
from pathlib import Path

def fix_cv_colors(file_path):
    """Fix CV template colors to use LinkedIn blue"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace darkblue color definition with linkedinblue
        content = content.replace(
            r'\definecolor{darkblue}{RGB}{0,51,102}',
            r'\definecolor{linkedinblue}{RGB}{0,119,181}'
        )
        
        # Replace darkblue usage with linkedinblue
        content = content.replace('darkblue', 'linkedinblue')
        
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
    """Main function to fix all CV templates"""
    print("🎨 Fixing CV template colors to LinkedIn blue...")
    
    # Find all CV template files
    job_applications_dir = Path("job_applications")
    cv_files = list(job_applications_dir.glob("**/*CV*.tex"))
    
    print(f"📁 Found {len(cv_files)} CV template files")
    
    fixed_count = 0
    
    for cv_file in cv_files:
        print(f"\n📄 Processing: {cv_file}")
        
        if fix_cv_colors(cv_file):
            fixed_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   Total CV files found: {len(cv_files)}")
    print(f"   Files with color fixes: {fixed_count}")
    print(f"   Files already correct: {len(cv_files) - fixed_count}")
    
    print(f"\n✅ All CV templates now use LinkedIn blue (RGB 0,119,181)")

if __name__ == '__main__':
    main()