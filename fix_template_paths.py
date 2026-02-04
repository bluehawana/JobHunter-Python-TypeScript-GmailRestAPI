#!/usr/bin/env python3
"""
Script to fix all template paths in cv_templates.py
"""

def fix_template_paths():
    """Fix all template paths from latex_sources/ to backend/latex_sources/"""
    
    # Read the current file
    with open('backend/cv_templates.py', 'r') as f:
        content = f.read()
    
    # Replace all occurrences
    old_cv_path = "'latex_sources/cv_hongzhi_li_modern.tex'"
    new_cv_path = "'backend/latex_sources/cv_hongzhi_li_modern.tex'"
    
    old_cl_path = "'latex_sources/cover_letter_hongzhi_li_template.tex'"
    new_cl_path = "'backend/latex_sources/cover_letter_hongzhi_li_template.tex'"
    
    # Count occurrences before replacement
    cv_count = content.count(old_cv_path)
    cl_count = content.count(old_cl_path)
    
    print(f"Found {cv_count} CV template paths to fix")
    print(f"Found {cl_count} CL template paths to fix")
    
    # Replace all occurrences
    content = content.replace(old_cv_path, new_cv_path)
    content = content.replace(old_cl_path, new_cl_path)
    
    # Write back to file
    with open('backend/cv_templates.py', 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {cv_count} CV template paths")
    print(f"✅ Fixed {cl_count} CL template paths")
    print("✅ All template paths updated successfully")

if __name__ == '__main__':
    fix_template_paths()