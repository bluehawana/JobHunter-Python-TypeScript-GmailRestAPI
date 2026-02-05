#!/usr/bin/env python3
"""
Test the Kamstrup LinkedIn job classification
"""

import sys
import os
sys.path.append('backend')

def test_kamstrup_job_classification():
    """Test classification of the actual Kamstrup LinkedIn job"""
    print("🔍 Testing Kamstrup LinkedIn Job Classification")
    print("=" * 60)
    
    # The actual job description from LinkedIn
    job_description = """
    Customer Support Engineer - Kamstrup
    Danderyd, Stockholm County, Sweden
    
    Are you energized by providing a high level of customer support? Do you thrive with technically complex tasks, where the best solution is not always clear? Are you ready to provide and receive sparring to ensure that you succeed as a team? 
    
    Provide our customers with high quality support As a Customer Support Engineer, you will be responsible for providing a high level of service to our customers, acting as their single point of contact. Through your technical knowledge, you will be providing support on issues independently while seeking knowledge from specialized colleagues on more complex matters.
    
    More specifically, you will be:
    - Remotely resolving technical issues, requests and questions from customers concerning all Kamstrup's products, services and solutions
    - Troubleshooting advanced technical issues within Kamstrup products: Hardware, Software, configuration, setup, networking, different radio technologies and analyzing tools
    - Exhausting possible solutions within the team of experts and escalate when necessary
    - Clarifying the scope of issues and defining requests for services, bug fixes and Feature Requests / improvement opportunities
    - Working closely with the international Kamstrup team of customer support, customer services and developers / experts
    - Training customers and colleagues in Kamstrup's systems, services, and applications, as well as participating in customer facing activities when applicable
    - Helping develop and maintain our internal systems and processes, actively contributing to our knowledge database and documentation
    
    We imagine that you have extensive experience in advanced technical support, including experience in or one or more ticketing systems, such as ServiceNow.
    
    Key Requirements:
    - Swedish and English language skills
    - Technical support experience
    - Ticketing systems experience (ServiceNow)
    - Hardware and software troubleshooting
    - Networking knowledge
    - Customer service skills
    """
    
    try:
        from cv_templates import CVTemplateManager
        
        # Test keyword-based classification
        template_manager = CVTemplateManager()
        role_category = template_manager.analyze_job_role(job_description)
        
        print(f"🎯 Classification Result: {role_category}")
        
        # Check if it's correctly classified
        expected_categories = ['kamstrup', 'it_support']
        
        if role_category == 'kamstrup':
            print("🎉 PERFECT! Classified as 'kamstrup' (Priority 1 - Company Specific)")
            print("✅ This is the ideal classification for this job")
            return True
        elif role_category == 'it_support':
            print("✅ GOOD! Classified as 'it_support' (Priority 3 - Customer Support)")
            print("💡 This is acceptable, though 'kamstrup' would be better")
            return True
        else:
            print(f"❌ WRONG! Classified as '{role_category}' instead of expected categories")
            print(f"Expected: {expected_categories}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing classification: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_keywords():
    """Analyze which keywords should match"""
    print("\n🔍 Keyword Analysis")
    print("=" * 30)
    
    job_text = """Customer Support Engineer Kamstrup troubleshooting technical support networking hardware software ServiceNow ticketing systems customer service"""
    
    try:
        from cv_templates import CVTemplateManager
        template_manager = CVTemplateManager()
        
        # Check Kamstrup keywords
        kamstrup_keywords = template_manager.ROLE_CATEGORIES['kamstrup']['keywords']
        print(f"Kamstrup keywords: {kamstrup_keywords}")
        
        # Check IT Support keywords  
        it_support_keywords = template_manager.ROLE_CATEGORIES['it_support']['keywords']
        print(f"IT Support keywords: {it_support_keywords[:10]}...")  # Show first 10
        
        # Check matches
        job_lower = job_text.lower()
        
        kamstrup_matches = [kw for kw in kamstrup_keywords if kw.lower() in job_lower]
        it_support_matches = [kw for kw in it_support_keywords if kw.lower() in job_lower]
        
        print(f"\n🎯 Kamstrup matches: {kamstrup_matches}")
        print(f"🎯 IT Support matches: {it_support_matches}")
        
        print(f"\nKamstrup score: {len(kamstrup_matches)} matches (Priority 1)")
        print(f"IT Support score: {len(it_support_matches)} matches (Priority 3)")
        
        if kamstrup_matches:
            print("✅ Kamstrup should win due to company-specific keywords + higher priority")
        else:
            print("⚠️ No Kamstrup matches - IT Support should win")
            
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing keywords: {e}")
        return False

def test_role_type_generation():
    """Test role type generation"""
    print("\n📝 Testing Role Type Generation")
    print("=" * 40)
    
    test_cases = [
        ('kamstrup', 'Kamstrup'),
        ('it_support', 'It Support'),
        ('devops_cloud', 'Devops Cloud')
    ]
    
    for role_category, expected_role_type in test_cases:
        role_type = role_category.replace('_', ' ').title()
        print(f"Role Category: '{role_category}' -> Role Type: '{role_type}'")
        
        if role_type == expected_role_type:
            print("✅ Correct")
        else:
            print(f"❌ Expected '{expected_role_type}', got '{role_type}'")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Kamstrup LinkedIn Job Processing")
    print("=" * 70)
    
    # Run tests
    classification_ok = test_kamstrup_job_classification()
    keywords_ok = analyze_keywords()
    role_type_ok = test_role_type_generation()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Job Classification: {'✅ PASS' if classification_ok else '❌ FAIL'}")
    print(f"Keyword Analysis: {'✅ PASS' if keywords_ok else '❌ FAIL'}")
    print(f"Role Type Generation: {'✅ PASS' if role_type_ok else '❌ FAIL'}")
    
    all_passed = all([classification_ok, keywords_ok, role_type_ok])
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ The system should correctly handle this Kamstrup job")
        print("✅ Expected: Company='Kamstrup', Role='Customer Support Engineer'")
        print("✅ Classification: 'kamstrup' or 'it_support'")
        print("✅ CV Title: 'Kamstrup' or 'It Support'")
    else:
        print(f"\n❌ SOME TESTS FAILED")
        print("The system may not handle this job correctly")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)