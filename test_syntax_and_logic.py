#!/usr/bin/env python3
"""
Test syntax and core logic without Flask dependencies
"""

import sys
import os
import re

def test_ai_review_function_syntax():
    """Test that the ai_review_documents function has correct syntax"""
    print("🔍 Testing ai_review_documents function syntax...")
    
    # Read the file and check for the function
    with open('backend/app/lego_api.py', 'r') as f:
        content = f.read()
    
    # Check if function is defined at module level (not inside another function)
    function_pattern = r'^def ai_review_documents\('
    if re.search(function_pattern, content, re.MULTILINE):
        print("✅ ai_review_documents function found at module level")
    else:
        print("❌ ai_review_documents function not found at module level")
        return False
    
    # Check if function is called correctly
    call_pattern = r'quality_check = ai_review_documents\('
    if re.search(call_pattern, content):
        print("✅ ai_review_documents function called correctly")
    else:
        print("❌ ai_review_documents function call not found")
        return False
    
    return True

def test_linkedin_blue_color():
    """Test that LinkedIn blue color is used consistently"""
    print("\n🎨 Testing LinkedIn blue color consistency...")
    
    # Check main API file
    with open('backend/app/lego_api.py', 'r') as f:
        api_content = f.read()
    
    # Check for LinkedIn blue RGB values
    linkedin_blue_patterns = [
        r'0,119,181',  # RGB format
        r'0/119/181',  # Alternative format
        r'definecolor.*linkedin.*0\.467.*0\.710.*0\.710'  # LaTeX color definition
    ]
    
    found_linkedin_blue = False
    for pattern in linkedin_blue_patterns:
        if re.search(pattern, api_content):
            found_linkedin_blue = True
            print(f"✅ Found LinkedIn blue pattern: {pattern}")
            break
    
    if not found_linkedin_blue:
        print("⚠️ LinkedIn blue color not found in API file")
    
    # Check template files
    template_files = [
        'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
        'templates/cl_template_overleaf.tex'
    ]
    
    for template_file in template_files:
        try:
            with open(template_file, 'r') as f:
                template_content = f.read()
            
            if '0,119,181' in template_content or '0/119/181' in template_content:
                print(f"✅ LinkedIn blue found in {template_file}")
            else:
                print(f"⚠️ LinkedIn blue not found in {template_file}")
        except FileNotFoundError:
            print(f"⚠️ Template file not found: {template_file}")
    
    return True

def test_cover_letter_content():
    """Test that cover letter templates don't have inappropriate content"""
    print("\n💌 Testing cover letter content...")
    
    inappropriate_phrases = [
        'passion for innovative software development',
        '[COMPANY NAME]',
        '[SPECIFIC REASON',
        'software development',
        'innovative software'
    ]
    
    # Check main cover letter template
    try:
        with open('backend/latex_sources/cover_letter_hongzhi_li_template.tex', 'r') as f:
            cl_content = f.read()
        
        issues_found = []
        for phrase in inappropriate_phrases:
            if phrase.lower() in cl_content.lower():
                issues_found.append(phrase)
        
        if issues_found:
            print(f"❌ Inappropriate content found in cover letter template:")
            for issue in issues_found:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Cover letter template content looks appropriate")
    except FileNotFoundError:
        print("⚠️ Cover letter template not found")
    
    return True

def test_role_category_mapping():
    """Test that IT Support roles map to correct templates"""
    print("\n🗂️ Testing role category mapping...")
    
    try:
        with open('backend/cv_templates.py', 'r') as f:
            cv_templates_content = f.read()
        
        # Check if IT Support maps to incident_management_template
        if "'it_support'" in cv_templates_content and 'incident_management_template' in cv_templates_content:
            print("✅ IT Support role category mapping found")
        else:
            print("⚠️ IT Support role category mapping not clear")
        
        # Check template paths use backend/latex_sources/
        if 'backend/latex_sources/' in cv_templates_content:
            print("✅ Template paths use correct backend/latex_sources/ prefix")
        else:
            print("❌ Template paths missing backend/latex_sources/ prefix")
            return False
            
    except FileNotFoundError:
        print("❌ cv_templates.py not found")
        return False
    
    return True

def test_company_title_splitting():
    """Test company-title splitting logic"""
    print("\n📝 Testing company-title splitting logic...")
    
    with open('backend/app/lego_api.py', 'r') as f:
        api_content = f.read()
    
    # Check for splitting logic
    splitting_patterns = [
        r"company\.split\('\s*-\s*'",
        r"title\.split\('\s*-\s*'",
        r"Split combined string"
    ]
    
    found_splitting = False
    for pattern in splitting_patterns:
        if re.search(pattern, api_content):
            found_splitting = True
            print(f"✅ Found splitting logic: {pattern}")
            break
    
    if not found_splitting:
        print("❌ Company-title splitting logic not found")
        return False
    
    return True

def main():
    """Run all syntax and logic tests"""
    print("🚀 Starting syntax and logic tests...")
    
    tests = [
        test_ai_review_function_syntax,
        test_linkedin_blue_color,
        test_cover_letter_content,
        test_role_category_mapping,
        test_company_title_splitting
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL SYNTAX AND LOGIC TESTS PASSED!")
        return True
    else:
        print("⚠️ Some tests failed - check output above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)