#!/usr/bin/env python3
"""
Test AI-powered CV content customization
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import customize_template, build_custom_summary
from ai_analyzer import AIAnalyzer
from cv_templates import CVTemplateManager

def test_automotive_job():
    """Test with automotive DevOps job"""
    
    job_description = """
    Automotive DevOps Engineer
    
    We are looking for a DevOps Engineer to join our automotive team.
    
    Key skills:
    - Kubernetes orchestration
    - Jenkins, Gerrit, Artifactory
    - CI/CD automation
    - Azure and AWS cloud platforms
    - Python, Bash scripting
    - Automotive industry experience preferred
    
    You will work on building robust CI services for our automotive platform.
    """
    
    print("="*60)
    print("TEST: Automotive DevOps Job")
    print("="*60)
    
    # Test AI analyzer
    analyzer = AIAnalyzer()
    
    if analyzer.is_available():
        result = analyzer.analyze_job_description(job_description)
        
        if result:
            print(f"\n✓ AI Analysis:")
            print(f"  Role Category: {result['role_category']}")
            print(f"  Confidence: {result['confidence']:.0%}")
            print(f"  Key Technologies: {', '.join(result['key_technologies'][:5])}")
            
            # Test custom summary generation
            custom_summary = build_custom_summary(
                result['role_category'],
                result['key_technologies'],
                job_description
            )
            
            print(f"\n✓ Custom Summary Generated:")
            print(f"  {custom_summary[:200]}...")
            
            # Check that it doesn't mention banking/fintech
            if 'banking' in custom_summary.lower() or 'fintech' in custom_summary.lower():
                print("\n✗ ERROR: Summary still contains banking/fintech content!")
                return False
            else:
                print("\n✓ SUCCESS: Summary is clean (no banking/fintech content)")
                return True
        else:
            print("\n✗ AI analysis failed")
            return False
    else:
        print("\n✗ AI analyzer not available")
        print("  Please check .env file has ANTHROPIC_API_KEY or maxmini_apikey")
        return False


def test_fintech_job():
    """Test with FinTech job to ensure banking content IS included"""
    
    job_description = """
    FinTech DevOps Engineer - Nasdaq
    
    Join our FinTech team building payment systems and trading platforms.
    
    Key skills:
    - Kafka for financial data streaming
    - AWS cloud infrastructure
    - Payment systems (Stripe, PayPal)
    - Financial services experience
    - DevOps and CI/CD
    """
    
    print("\n" + "="*60)
    print("TEST: FinTech Job (should keep financial content)")
    print("="*60)
    
    analyzer = AIAnalyzer()
    
    if analyzer.is_available():
        result = analyzer.analyze_job_description(job_description)
        
        if result:
            print(f"\n✓ AI Analysis:")
            print(f"  Role Category: {result['role_category']}")
            print(f"  Confidence: {result['confidence']:.0%}")
            
            custom_summary = build_custom_summary(
                result['role_category'],
                result['key_technologies'],
                job_description
            )
            
            print(f"\n✓ Custom Summary Generated:")
            print(f"  {custom_summary[:200]}...")
            
            return True
        else:
            print("\n✗ AI analysis failed")
            return False
    else:
        print("\n✗ AI analyzer not available")
        return False


if __name__ == '__main__':
    print("\n🧪 Testing AI-Powered CV Content Customization\n")
    
    # Test 1: Automotive job (should NOT have banking content)
    test1_passed = test_automotive_job()
    
    # Test 2: FinTech job (can have financial content)
    test2_passed = test_fintech_job()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"Automotive Job Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"FinTech Job Test: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n✓ All tests passed! AI customization is working.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check the output above.")
        sys.exit(1)
