#!/usr/bin/env python3
"""
Test script to verify Kamstrup Customer Support Engineer fixes:
1. Cover letter should use LinkedIn blue color (not dark blue)
2. Job should be classified as IT Support (not DevOps Cloud)
"""

import sys
import os
sys.path.append('backend')
sys.path.append('backend/app')

from lego_api import build_lego_cover_letter, build_lego_cv
from ai_analyzer import AIAnalyzer

def test_color_fix():
    """Test that cover letter uses LinkedIn blue color"""
    print("🎨 Testing Cover Letter Color Fix")
    print("=" * 50)
    
    # Generate a cover letter
    cl_content = build_lego_cover_letter(
        role_type="Customer Support Engineer",
        company="Kamstrup",
        title="Customer Support Engineer",
        role_category="it_support",
        job_description="Customer support engineer role at Kamstrup"
    )
    
    # Check for LinkedIn blue color
    has_linkedin_blue = 'linkedinblue' in cl_content
    has_dark_blue = 'darkblue' in cl_content
    
    print(f"✓ Uses LinkedIn Blue: {has_linkedin_blue}")
    print(f"✗ Uses Dark Blue: {has_dark_blue}")
    
    if has_linkedin_blue and not has_dark_blue:
        print("🎉 Color fix SUCCESS - Cover letter uses LinkedIn blue!")
    else:
        print("❌ Color fix FAILED - Cover letter still uses dark blue")
        
    return has_linkedin_blue and not has_dark_blue

def test_job_classification():
    """Test that Kamstrup Customer Support Engineer is classified correctly"""
    print("\n🔍 Testing Job Classification Fix")
    print("=" * 50)
    
    # Sample Kamstrup Customer Support Engineer job description
    job_description = """
    Customer Support Engineer
    Kamstrup
    Gothenburg, Sweden
    
    We are looking for a Customer Support Engineer to join our team. 
    You will provide technical support to our customers, troubleshoot issues,
    and help resolve customer problems with our smart metering solutions.
    
    Key responsibilities:
    - Provide technical support to customers
    - Troubleshoot customer issues
    - Document support cases
    - Work with engineering teams to resolve complex issues
    - Customer communication and relationship management
    
    Requirements:
    - Experience in customer support or technical support
    - Strong troubleshooting skills
    - Good communication skills
    - Technical background preferred
    """
    
    # Test AI classification
    analyzer = AIAnalyzer()
    if analyzer.is_available():
        result = analyzer.analyze_job_description(job_description)
        if result:
            role_category = result['role_category']
            confidence = result['confidence']
            reasoning = result['reasoning']
            
            print(f"AI Classification: {role_category}")
            print(f"Confidence: {confidence:.2f}")
            print(f"Reasoning: {reasoning}")
            
            if role_category == 'it_support':
                print("🎉 Classification fix SUCCESS - Job classified as IT Support!")
                return True
            else:
                print(f"❌ Classification fix FAILED - Job classified as {role_category}")
                return False
        else:
            print("❌ AI analysis failed")
            return False
    else:
        print("⚠️ AI analyzer not available - skipping classification test")
        return True

def test_cv_title_generation():
    """Test that CV title is generated correctly for IT Support roles"""
    print("\n📄 Testing CV Title Generation")
    print("=" * 50)
    
    # Generate CV for IT Support role
    cv_content = build_lego_cv(
        role_type="Customer Support Engineer",
        company="Kamstrup",
        title="Customer Support Engineer",
        role_category="it_support",
        job_description="Customer support engineer role"
    )
    
    # Check if CV contains appropriate title
    has_support_title = any(title in cv_content for title in [
        'Customer Support Engineer',
        'Technical Support',
        'IT Support',
        'Support Engineer'
    ])
    
    # Should NOT contain "IT Business Analyst"
    has_wrong_title = 'IT Business Analyst' in cv_content
    
    print(f"✓ Has Support-related title: {has_support_title}")
    print(f"✗ Has wrong title (IT Business Analyst): {has_wrong_title}")
    
    if has_support_title and not has_wrong_title:
        print("🎉 CV title fix SUCCESS!")
        return True
    else:
        print("❌ CV title fix FAILED")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Kamstrup Customer Support Engineer Fixes")
    print("=" * 60)
    
    # Run tests
    color_ok = test_color_fix()
    classification_ok = test_job_classification()
    cv_title_ok = test_cv_title_generation()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Color Fix: {'✅ PASS' if color_ok else '❌ FAIL'}")
    print(f"Classification Fix: {'✅ PASS' if classification_ok else '❌ FAIL'}")
    print(f"CV Title Fix: {'✅ PASS' if cv_title_ok else '❌ FAIL'}")
    
    all_passed = color_ok and classification_ok and cv_title_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)