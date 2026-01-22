#!/usr/bin/env python3
"""
Debug replacement in detail
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.template_customizer import TemplateCustomizer

def debug_step_by_step():
    """Debug each step of the customization process"""
    
    template = r"""{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[8pt]
{\Large \textbf{COMPANY_NAME}}\\[4pt]
{\Large \textbf{JOB_TITLE}}\\[4pt]
{\Large \textbf{Gothenburg, Sweden}}\\[8pt]"""
    
    print("🔍 Step-by-step Debugging")
    print("=" * 50)
    print(f"Original template:\n{template}")
    
    customizer = TemplateCustomizer()
    
    # Step 1: Test escape_latex_chars
    company = "Meltwater"
    title = "Software Engineer"
    
    escaped_company = customizer.escape_latex_chars(company)
    escaped_title = customizer.escape_latex_chars(title)
    
    print(f"\nStep 1 - Escaped values:")
    print(f"  Company: '{company}' -> '{escaped_company}'")
    print(f"  Title: '{title}' -> '{escaped_title}'")
    
    # Step 2: Test replacements dictionary
    replacements = {
        'COMPANY_NAME': escaped_company,
        'JOB_TITLE': escaped_title,
    }
    
    print(f"\nStep 2 - Replacements dict:")
    for key, value in replacements.items():
        print(f"  {key}: '{value}'")
    
    # Step 3: Test replace_placeholders
    after_replacement = customizer.replace_placeholders(template, replacements)
    print(f"\nStep 3 - After replace_placeholders:")
    print(f"{after_replacement}")
    
    # Step 4: Test _update_cv_header_title
    after_header_update = customizer._update_cv_header_title(after_replacement, escaped_title)
    print(f"\nStep 4 - After _update_cv_header_title:")
    print(f"{after_header_update}")
    
    # Check what changed
    if after_replacement != after_header_update:
        print("\n⚠️ _update_cv_header_title modified the content!")
    else:
        print("\n✅ _update_cv_header_title skipped (as expected)")
    
    # Final check
    if 'Meltwater' in after_header_update and 'Software Engineer' in after_header_update:
        print("\n✅ Final result contains expected values")
    else:
        print("\n❌ Final result missing expected values")
        if 'COMPANY_NAME' in after_header_update:
            print("   - COMPANY_NAME placeholder still present")
        if 'JOB_TITLE' in after_header_update:
            print("   - JOB_TITLE placeholder still present")

if __name__ == '__main__':
    debug_step_by_step()