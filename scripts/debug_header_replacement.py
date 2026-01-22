#!/usr/bin/env python3
"""
Debug header replacement to see what's happening
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.template_customizer import TemplateCustomizer

def debug_replacement():
    """Debug the replacement process"""
    
    template = r"{\Large \textbf{COMPANY_NAME // JOB_TITLE // Gothenburg, Sweden}}"
    
    print("🔍 Debugging Header Replacement")
    print("=" * 50)
    print(f"Original template: {template}")
    
    customizer = TemplateCustomizer()
    
    # Test the replacement manually
    replacements = {
        'COMPANY_NAME': 'Meltwater',
        'JOB_TITLE': 'Software Engineer'
    }
    
    print(f"\nReplacements: {replacements}")
    
    # Test replace_placeholders method directly
    result = customizer.replace_placeholders(template, replacements)
    print(f"After replacement: {result}")
    
    # Test full customization
    full_result = customizer.customize_template(
        template,
        company="Meltwater",
        title="Software Engineer",
        role_type="backend_developer"
    )
    print(f"Full customization: {full_result}")
    
    # Check if placeholders exist
    if 'COMPANY_NAME' in result:
        print("❌ COMPANY_NAME placeholder not replaced")
    if 'JOB_TITLE' in result:
        print("❌ JOB_TITLE placeholder not replaced")
    
    if 'Meltwater' in result and 'Software Engineer' in result:
        print("✅ Replacement successful!")
    else:
        print("❌ Replacement failed")

if __name__ == '__main__':
    debug_replacement()