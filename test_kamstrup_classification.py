#!/usr/bin/env python3
"""
Test script to verify Kamstrup Customer Support Engineer classification fixes
"""

import sys
import os
sys.path.append('backend')

def test_priority_fix():
    """Test that IT support now has higher priority than DevOps"""
    print("🏆 Testing Priority Fix")
    print("=" * 50)
    
    try:
        from cv_templates import CVTemplateManager
        manager = CVTemplateManager()
        
        it_support_priority = manager.ROLE_CATEGORIES['it_support']['priority']
        devops_priority = manager.ROLE_CATEGORIES['devops_cloud']['priority']
        
        print(f"IT Support priority: {it_support_priority}")
        print(f"DevOps Cloud priority: {devops_priority}")
        
        if it_support_priority < devops_priority:
            print("🎉 Priority fix SUCCESS - IT Support has higher priority!")
            return True
        else:
            print("❌ Priority fix FAILED - DevOps still has higher priority")
            return False
            
    except Exception as e:
        print(f"❌ Error testing priority: {e}")
        return False

def test_keyword_expansion():
    """Test that IT support keywords include customer support terms"""
    print("\n📝 Testing Keyword Expansion")
    print("=" * 50)
    
    try:
        from cv_templates import CVTemplateManager
        manager = CVTemplateManager()
        
        it_support_keywords = manager.ROLE_CATEGORIES['it_support']['keywords']
        
        required_keywords = ['customer support', 'support engineer', 'user support', 'customer service']
        missing_keywords = []
        
        for keyword in required_keywords:
            if keyword not in it_support_keywords:
                missing_keywords.append(keyword)
        
        print(f"IT Support keywords: {it_support_keywords}")
        print(f"Required keywords present: {len(required_keywords) - len(missing_keywords)}/{len(required_keywords)}")
        
        if not missing_keywords:
            print("🎉 Keyword expansion SUCCESS - All customer support keywords present!")
            return True
        else:
            print(f"❌ Keyword expansion FAILED - Missing: {missing_keywords}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing keywords: {e}")
        return False

def test_kamstrup_detection():
    """Test that Kamstrup-specific keywords are present"""
    print("\n🏢 Testing Kamstrup Detection")
    print("=" * 50)
    
    try:
        from cv_templates import CVTemplateManager
        manager = CVTemplateManager()
        
        kamstrup_keywords = manager.ROLE_CATEGORIES['kamstrup']['keywords']
        
        required_keywords = ['kamstrup', 'customer support engineer']
        missing_keywords = []
        
        for keyword in required_keywords:
            if keyword not in kamstrup_keywords:
                missing_keywords.append(keyword)
        
        print(f"Kamstrup keywords: {kamstrup_keywords}")
        print(f"Required keywords present: {len(required_keywords) - len(missing_keywords)}/{len(required_keywords)}")
        
        if not missing_keywords:
            print("🎉 Kamstrup detection SUCCESS - All required keywords present!")
            return True
        else:
            print(f"❌ Kamstrup detection FAILED - Missing: {missing_keywords}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Kamstrup: {e}")
        return False

def test_ai_rules_update():
    """Test that AI analyzer has updated classification rules"""
    print("\n🤖 Testing AI Rules Update")
    print("=" * 50)
    
    try:
        with open('backend/ai_analyzer.py', 'r') as f:
            content = f.read()
        
        # Check for the new customer support priority rule
        has_priority_rule = 'takes priority over DevOps' in content
        has_distinction_section = 'CUSTOMER SUPPORT vs DEVOPS DISTINCTION' in content
        
        print(f"✓ Has customer support priority rule: {has_priority_rule}")
        print(f"✓ Has customer support vs DevOps distinction: {has_distinction_section}")
        
        if has_priority_rule and has_distinction_section:
            print("🎉 AI rules update SUCCESS!")
            return True
        else:
            print("❌ AI rules update FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AI rules: {e}")
        return False

def simulate_classification():
    """Simulate classification of Kamstrup Customer Support Engineer job"""
    print("\n🎯 Simulating Classification")
    print("=" * 50)
    
    # Sample job description
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
        from cv_templates import CVTemplateManager
        manager = CVTemplateManager()
        
        # Test keyword-based classification
        role_category = manager.analyze_job_role(job_description)
        print(f"Keyword-based classification: {role_category}")
        
        # Check if it's IT support or Kamstrup
        if role_category in ['it_support', 'kamstrup']:
            print("🎉 Classification SUCCESS - Detected as support role!")
            return True
        else:
            print(f"❌ Classification FAILED - Detected as {role_category}")
            return False
            
    except Exception as e:
        print(f"❌ Error simulating classification: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Kamstrup Customer Support Engineer Classification Fixes")
    print("=" * 70)
    
    # Run tests
    priority_ok = test_priority_fix()
    keywords_ok = test_keyword_expansion()
    kamstrup_ok = test_kamstrup_detection()
    ai_rules_ok = test_ai_rules_update()
    classification_ok = simulate_classification()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Priority Fix: {'✅ PASS' if priority_ok else '❌ FAIL'}")
    print(f"Keyword Expansion: {'✅ PASS' if keywords_ok else '❌ FAIL'}")
    print(f"Kamstrup Detection: {'✅ PASS' if kamstrup_ok else '❌ FAIL'}")
    print(f"AI Rules Update: {'✅ PASS' if ai_rules_ok else '❌ FAIL'}")
    print(f"Classification Simulation: {'✅ PASS' if classification_ok else '❌ FAIL'}")
    
    all_passed = all([priority_ok, keywords_ok, kamstrup_ok, ai_rules_ok, classification_ok])
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)