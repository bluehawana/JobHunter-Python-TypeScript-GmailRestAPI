#!/usr/bin/env python3
"""
Simple test to verify the fixes without importing the full lego_api
"""

def test_color_in_template():
    """Test that the template uses LinkedIn blue"""
    print("🎨 Testing Cover Letter Template Color")
    print("=" * 50)
    
    # Read the cover letter template
    try:
        with open('templates/cl_template_overleaf.tex', 'r') as f:
            template_content = f.read()
        
        has_linkedin_blue = 'linkedinblue' in template_content
        has_dark_blue = 'darkblue' in template_content
        
        print(f"✓ Template uses LinkedIn Blue: {has_linkedin_blue}")
        print(f"✗ Template uses Dark Blue: {has_dark_blue}")
        
        if has_linkedin_blue and not has_dark_blue:
            print("🎉 Template color fix SUCCESS!")
            return True
        else:
            print("❌ Template color fix FAILED")
            return False
            
    except FileNotFoundError:
        print("❌ Template file not found")
        return False

def test_lego_api_color_fix():
    """Test that lego_api.py uses LinkedIn blue in fallback"""
    print("\n🔧 Testing Lego API Color Fix")
    print("=" * 50)
    
    try:
        with open('backend/app/lego_api.py', 'r') as f:
            api_content = f.read()
        
        # Check if the fallback template uses linkedinblue
        # Look for the specific fallback section in build_lego_cover_letter
        fallback_start = api_content.find('latex = r"""\\documentclass[10pt,a4paper]{article}')
        if fallback_start == -1:
            print("❌ Fallback template not found")
            return False
            
        fallback_end = api_content.find('return latex', fallback_start)
        fallback_section = api_content[fallback_start:fallback_end]
        
        has_linkedin_blue = 'linkedinblue' in fallback_section
        has_dark_blue = 'darkblue' in fallback_section
        
        print(f"✓ Fallback uses LinkedIn Blue: {has_linkedin_blue}")
        print(f"✗ Fallback uses Dark Blue: {has_dark_blue}")
        
        if has_linkedin_blue and not has_dark_blue:
            print("🎉 Lego API color fix SUCCESS!")
            return True
        else:
            print("❌ Lego API color fix FAILED")
            if has_dark_blue:
                print("  Still contains darkblue references")
            if not has_linkedin_blue:
                print("  Missing linkedinblue references")
            return False
            
    except FileNotFoundError:
        print("❌ Lego API file not found")
        return False

def test_ai_analyzer_rules():
    """Test that AI analyzer has customer support rules"""
    print("\n🤖 Testing AI Analyzer Rules")
    print("=" * 50)
    
    try:
        with open('backend/ai_analyzer.py', 'r') as f:
            analyzer_content = f.read()
        
        # Check if customer support is mentioned in classification rules
        has_customer_support_rule = 'customer support' in analyzer_content
        has_it_support_rule = 'it_support' in analyzer_content
        
        print(f"✓ Has customer support rule: {has_customer_support_rule}")
        print(f"✓ Has IT support classification: {has_it_support_rule}")
        
        if has_customer_support_rule and has_it_support_rule:
            print("🎉 AI analyzer rules fix SUCCESS!")
            return True
        else:
            print("❌ AI analyzer rules fix FAILED")
            return False
            
    except FileNotFoundError:
        print("❌ AI analyzer file not found")
        return False

def test_cv_templates_keywords():
    """Test that cv_templates.py has customer support keywords"""
    print("\n📋 Testing CV Templates Keywords")
    print("=" * 50)
    
    try:
        with open('backend/cv_templates.py', 'r') as f:
            templates_content = f.read()
        
        # Check if customer support is in IT support keywords
        it_support_start = templates_content.find("'it_support': {")
        it_support_end = templates_content.find("'priority': 5", it_support_start) + 20
        it_support_section = templates_content[it_support_start:it_support_end]
        
        has_customer_support = 'customer support' in it_support_section
        has_support_engineer = 'support engineer' in it_support_section
        
        print(f"✓ Has customer support keyword: {has_customer_support}")
        print(f"✓ Has support engineer keyword: {has_support_engineer}")
        
        if has_customer_support and has_support_engineer:
            print("🎉 CV templates keywords fix SUCCESS!")
            return True
        else:
            print("❌ CV templates keywords fix FAILED")
            print(f"IT Support section: {it_support_section[:200]}...")
            return False
            
    except FileNotFoundError:
        print("❌ CV templates file not found")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Kamstrup Customer Support Engineer Fixes")
    print("=" * 60)
    
    # Run tests
    template_color_ok = test_color_in_template()
    api_color_ok = test_lego_api_color_fix()
    ai_rules_ok = test_ai_analyzer_rules()
    keywords_ok = test_cv_templates_keywords()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Template Color Fix: {'✅ PASS' if template_color_ok else '❌ FAIL'}")
    print(f"API Color Fix: {'✅ PASS' if api_color_ok else '❌ FAIL'}")
    print(f"AI Rules Fix: {'✅ PASS' if ai_rules_ok else '❌ FAIL'}")
    print(f"Keywords Fix: {'✅ PASS' if keywords_ok else '❌ FAIL'}")
    
    all_passed = template_color_ok and api_color_ok and ai_rules_ok and keywords_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)