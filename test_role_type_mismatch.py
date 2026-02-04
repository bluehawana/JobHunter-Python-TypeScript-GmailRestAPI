#!/usr/bin/env python3
"""
Test script to reproduce the role_type vs role_category mismatch issue
"""

import sys
import os
sys.path.append('backend')
sys.path.append('backend/app')

def test_analyze_job_description():
    """Test the analyze_job_description function directly"""
    print("🔍 Testing analyze_job_description function")
    print("=" * 60)
    
    # Sample job description that might be classified as devops_cloud
    job_description = """
    DevOps Engineer
    TechCorp
    Gothenburg, Sweden
    
    We are looking for a DevOps Engineer to join our team.
    You will work with Kubernetes, Docker, Terraform, and AWS.
    Experience with CI/CD pipelines and monitoring is required.
    
    Key requirements:
    - Kubernetes experience
    - Docker containerization
    - Terraform infrastructure as code
    - AWS cloud platform
    - CI/CD pipeline management
    """
    
    try:
        from lego_api import analyze_job_description
        
        analysis = analyze_job_description(job_description)
        
        print(f"Role Type: {analysis.get('roleType')}")
        print(f"Role Category: {analysis.get('roleCategory')}")
        print(f"Company: {analysis.get('company')}")
        print(f"Title: {analysis.get('title')}")
        
        # Check for mismatch
        role_type = analysis.get('roleType')
        role_category = analysis.get('roleCategory')
        
        expected_role_type = role_category.replace('_', ' ').title() if role_category else 'Unknown'
        
        print(f"\nExpected Role Type (from category): {expected_role_type}")
        print(f"Actual Role Type: {role_type}")
        
        if role_type == expected_role_type:
            print("✅ Role type matches role category - NO MISMATCH")
            return True
        else:
            print("❌ MISMATCH DETECTED - Role type doesn't match role category")
            return False
            
    except Exception as e:
        print(f"❌ Error testing analyze_job_description: {e}")
        return False

def test_customer_support_case():
    """Test the specific customer support case"""
    print("\n🎯 Testing Customer Support Case")
    print("=" * 60)
    
    # The problematic job description
    job_description = """
    Customer Support Engineer
    Kamstrup
    Gothenburg, Sweden
    
    We are looking for a Customer Support Engineer to join our team.
    You will provide technical support to customers, troubleshoot networking issues,
    and help resolve customer problems with our smart metering solutions.
    
    Key requirements:
    - Experience in customer support or technical support
    - Strong troubleshooting skills
    - Networking knowledge
    - Good communication skills
    """
    
    try:
        from lego_api import analyze_job_description
        
        analysis = analyze_job_description(job_description)
        
        print(f"Role Type: {analysis.get('roleType')}")
        print(f"Role Category: {analysis.get('roleCategory')}")
        print(f"Company: {analysis.get('company')}")
        print(f"Title: {analysis.get('title')}")
        
        # Check for mismatch
        role_type = analysis.get('roleType')
        role_category = analysis.get('roleCategory')
        
        # For customer support, we expect either 'kamstrup' or 'it_support'
        expected_categories = ['kamstrup', 'it_support']
        
        if role_category in expected_categories:
            print(f"✅ Correct classification: {role_category}")
            
            expected_role_type = role_category.replace('_', ' ').title()
            if role_type == expected_role_type:
                print("✅ Role type matches role category - NO MISMATCH")
                return True
            else:
                print(f"❌ MISMATCH: Expected '{expected_role_type}', got '{role_type}'")
                return False
        else:
            print(f"❌ Wrong classification: Expected {expected_categories}, got {role_category}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing customer support case: {e}")
        return False

def test_build_lego_cv():
    """Test the build_lego_cv function to see what title it generates"""
    print("\n📄 Testing build_lego_cv Function")
    print("=" * 60)
    
    try:
        from lego_api import build_lego_cv
        
        # Test case: role_type="IT Business Analyst", role_category="devops_cloud"
        cv_content = build_lego_cv(
            role_type="IT Business Analyst",
            company="TestCorp",
            title="DevOps Engineer",
            role_category="devops_cloud",
            job_description="Test job description"
        )
        
        # Extract the title from the CV content
        import re
        title_match = re.search(r'\\Large \\textit\{([^}]+)\}', cv_content)
        
        if title_match:
            cv_title = title_match.group(1)
            print(f"CV Title in LaTeX: {cv_title}")
            
            if cv_title == "IT Business Analyst":
                print("❌ CONFIRMED: CV shows 'IT Business Analyst' title")
                print("This confirms the mismatch issue exists")
                return False
            else:
                print(f"✅ CV shows correct title: {cv_title}")
                return True
        else:
            print("❌ Could not extract title from CV content")
            return False
            
    except Exception as e:
        print(f"❌ Error testing build_lego_cv: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Role Type vs Role Category Mismatch Issue")
    print("=" * 70)
    
    # Run tests
    analyze_ok = test_analyze_job_description()
    customer_support_ok = test_customer_support_case()
    cv_build_ok = test_build_lego_cv()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Analyze Job Description: {'✅ PASS' if analyze_ok else '❌ FAIL'}")
    print(f"Customer Support Case: {'✅ PASS' if customer_support_ok else '❌ FAIL'}")
    print(f"CV Build Test: {'✅ PASS' if cv_build_ok else '❌ FAIL'}")
    
    all_passed = all([analyze_ok, customer_support_ok, cv_build_ok])
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)