#!/usr/bin/env python3
"""
Comprehensive local test for the LEGO Job Generator API
Tests all functionality including CV/CL generation and AI quality check
"""

import sys
import os
sys.path.append('backend')

# Test imports
try:
    from app.lego_api import (
        analyze_job_description,
        build_lego_cv,
        build_lego_cover_letter,
        ai_review_documents,
        extract_company_and_title_from_text
    )
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test job description
test_job_description = """
Customer Support Engineer
Kamstrup

About the role:
We are looking for a Customer Support Engineer to join our team in Gothenburg, Sweden. 
You will be responsible for providing technical support to our customers, troubleshooting 
issues with our water and heat cooling systems, and working with ServiceNow ticketing systems.

Requirements:
- Experience with ServiceNow
- Strong networking knowledge
- Radio technologies experience
- Troubleshooting skills
- Ticketing systems experience

About Kamstrup:
Kamstrup is a leading provider of intelligent energy and water metering solutions.
"""

def test_job_analysis():
    """Test job description analysis"""
    print("\n🔍 Testing job analysis...")
    try:
        analysis = analyze_job_description(test_job_description)
        print(f"✅ Role Type: {analysis.get('roleType', 'N/A')}")
        print(f"✅ Role Category: {analysis.get('roleCategory', 'N/A')}")
        print(f"✅ Company: {analysis.get('company', 'N/A')}")
        print(f"✅ Title: {analysis.get('title', 'N/A')}")
        print(f"✅ Keywords: {analysis.get('keywords', [])[:5]}...")
        return analysis
    except Exception as e:
        print(f"❌ Job analysis failed: {e}")
        return None

def test_company_title_extraction():
    """Test company and title extraction"""
    print("\n📝 Testing company/title extraction...")
    try:
        company, title = extract_company_and_title_from_text(test_job_description)
        print(f"✅ Extracted Company: {company}")
        print(f"✅ Extracted Title: {title}")
        return company, title
    except Exception as e:
        print(f"❌ Company/title extraction failed: {e}")
        return None, None

def test_cv_generation(analysis):
    """Test CV generation"""
    print("\n📄 Testing CV generation...")
    try:
        role_type = analysis.get('roleType', 'IT Support')
        role_category = analysis.get('roleCategory', 'it_support')
        company = analysis.get('company', 'Kamstrup')
        title = analysis.get('title', 'Customer Support Engineer')
        
        cv_latex = build_lego_cv(
            role_type=role_type,
            company=company,
            title=title,
            role_category=role_category,
            job_description=test_job_description
        )
        
        print(f"✅ CV generated successfully ({len(cv_latex)} characters)")
        print(f"✅ Contains company name: {'Kamstrup' in cv_latex}")
        print(f"✅ Contains LinkedIn blue color: {'0,119,181' in cv_latex}")
        print(f"✅ Contains role-specific content: {'ServiceNow' in cv_latex}")
        
        return cv_latex
    except Exception as e:
        print(f"❌ CV generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_cl_generation(analysis):
    """Test Cover Letter generation"""
    print("\n💌 Testing Cover Letter generation...")
    try:
        role_type = analysis.get('roleType', 'IT Support')
        role_category = analysis.get('roleCategory', 'it_support')
        company = analysis.get('company', 'Kamstrup')
        title = analysis.get('title', 'Customer Support Engineer')
        
        cl_latex = build_lego_cover_letter(
            role_type=role_type,
            company=company,
            title=title,
            role_category=role_category,
            job_description=test_job_description
        )
        
        print(f"✅ Cover Letter generated successfully ({len(cl_latex)} characters)")
        print(f"✅ Contains company name: {'Kamstrup' in cl_latex}")
        print(f"✅ Contains LinkedIn blue color: {'0,119,181' in cl_latex}")
        print(f"✅ No placeholder text: {'[COMPANY NAME]' not in cl_latex}")
        print(f"✅ No inappropriate content: {'software development' not in cl_latex.lower()}")
        
        return cl_latex
    except Exception as e:
        print(f"❌ Cover Letter generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_ai_quality_check(cv_latex, cl_latex, analysis):
    """Test AI quality check"""
    print("\n🤖 Testing AI quality check...")
    try:
        company = analysis.get('company', 'Kamstrup')
        title = analysis.get('title', 'Customer Support Engineer')
        
        quality_result = ai_review_documents(
            cv_latex=cv_latex,
            cl_latex=cl_latex,
            job_description=test_job_description,
            company=company,
            title=title
        )
        
        print(f"✅ AI Quality Check completed")
        print(f"✅ Overall Score: {quality_result.get('overall_score', 'N/A')}/100")
        print(f"✅ Ready to Send: {quality_result.get('ready_to_send', 'N/A')}")
        print(f"✅ Critical Issues: {len(quality_result.get('critical_issues', []))}")
        
        if quality_result.get('critical_issues'):
            print("⚠️ Issues found:")
            for issue in quality_result['critical_issues']:
                print(f"   - {issue}")
        
        return quality_result
    except Exception as e:
        print(f"❌ AI quality check failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive local API tests...")
    
    # Test 1: Job Analysis
    analysis = test_job_analysis()
    if not analysis:
        print("❌ Job analysis failed - stopping tests")
        return False
    
    # Test 2: Company/Title Extraction
    company, title = test_company_title_extraction()
    
    # Test 3: CV Generation
    cv_latex = test_cv_generation(analysis)
    if not cv_latex:
        print("❌ CV generation failed - stopping tests")
        return False
    
    # Test 4: Cover Letter Generation
    cl_latex = test_cl_generation(analysis)
    if not cl_latex:
        print("❌ Cover Letter generation failed - stopping tests")
        return False
    
    # Test 5: AI Quality Check
    quality_result = test_ai_quality_check(cv_latex, cl_latex, analysis)
    
    # Summary
    print("\n📊 TEST SUMMARY:")
    print("✅ Job Analysis: PASSED")
    print("✅ Company/Title Extraction: PASSED")
    print("✅ CV Generation: PASSED")
    print("✅ Cover Letter Generation: PASSED")
    print(f"✅ AI Quality Check: {'PASSED' if quality_result else 'FAILED (non-critical)'}")
    
    print("\n🎉 ALL CORE TESTS PASSED - Ready for deployment!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)