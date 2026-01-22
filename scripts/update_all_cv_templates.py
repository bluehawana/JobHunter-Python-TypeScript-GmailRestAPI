#!/usr/bin/env python3
"""
Script to add Vue.js to all CV templates that mention React
"""

import os
import re
from pathlib import Path

def update_cv_template(file_path):
    """Update a single CV template to add Vue.js"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Frontend: React, JavaScript, TypeScript -> Frontend: React, Vue.js, JavaScript, TypeScript
        pattern1 = r'(\\textbf\{Frontend[^}]*\}:?\s*)React,\s*JavaScript,\s*TypeScript'
        replacement1 = r'\1React, Vue.js, JavaScript, TypeScript'
        content = re.sub(pattern1, replacement1, content)
        
        # Pattern 2: Frontend: TypeScript, React, JavaScript -> Frontend: TypeScript, React, Vue.js, JavaScript
        pattern2 = r'(\\textbf\{Frontend[^}]*\}:?\s*)TypeScript,\s*React,\s*JavaScript'
        replacement2 = r'\1TypeScript, React, Vue.js, JavaScript'
        content = re.sub(pattern2, replacement2, content)
        
        # Pattern 3: Frontend (Full-Stack): React, TypeScript, JavaScript -> Frontend (Full-Stack): React, Vue.js, TypeScript, JavaScript
        pattern3 = r'(\\textbf\{Frontend[^}]*\}:?\s*)React,\s*TypeScript,\s*JavaScript'
        replacement3 = r'\1React, Vue.js, TypeScript, JavaScript'
        content = re.sub(pattern3, replacement3, content)
        
        # Pattern 4: Frontend Engineering: React, TypeScript -> Frontend Engineering: React, Vue.js, TypeScript
        pattern4 = r'(\\textbf\{Frontend[^}]*\}:?\s*)React,\s*TypeScript'
        replacement4 = r'\1React, Vue.js, TypeScript'
        content = re.sub(pattern4, replacement4, content)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⚪ No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all CV templates"""
    print("🔍 Finding CV templates to update...")
    
    # Find all CV template files
    job_applications_dir = Path("job_applications")
    cv_files = list(job_applications_dir.glob("**/*CV.tex"))
    
    print(f"📁 Found {len(cv_files)} CV template files")
    
    updated_count = 0
    
    for cv_file in cv_files:
        print(f"\n📄 Processing: {cv_file}")
        
        # Check if file contains React
        try:
            with open(cv_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'React' in content and 'Frontend' in content:
                if update_cv_template(cv_file):
                    updated_count += 1
            else:
                print(f"⚪ Skipping (no React frontend): {cv_file}")
                
        except Exception as e:
            print(f"❌ Error reading {cv_file}: {e}")
    
    print(f"\n🎉 Summary:")
    print(f"   Total CV files found: {len(cv_files)}")
    print(f"   Files updated: {updated_count}")
    print(f"   Files skipped: {len(cv_files) - updated_count}")

if __name__ == '__main__':
    main()