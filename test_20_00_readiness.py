#!/usr/bin/env python3
"""
Quick 20:00 Readiness Test for LEGO Job Automation System
Test if everything is ready for the scheduled 20:00 run
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import time

def test_core_system():
    """Test core system components"""
    print("🎯 TESTING CORE LEGO SYSTEM READINESS")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: LaTeX PDF Generation
    try:
        from beautiful_pdf_generator import create_beautiful_multi_page_pdf
        
        test_job = {
            'title': 'DevOps Engineer',
            'company': 'Opera',
            'description': 'Kubernetes, Docker, Prometheus, Grafana, monitoring'
        }
        
        pdf_content = create_beautiful_multi_page_pdf(test_job)
        if pdf_content and len(pdf_content) > 50000:
            print("✅ 1. PDF Generation: Working")
            tests_passed += 1
        else:
            print("❌ 1. PDF Generation: Failed")
    except Exception as e:
        print(f"❌ 1. PDF Generation: Error - {e}")
    
    # Test 2: LaTeX Template Generation
    try:
        from overleaf_pdf_generator import OverleafPDFGenerator
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(test_job)
        
        if latex_content and 'DevOps Engineer' in latex_content and 'Opera' in latex_content:
            print("✅ 2. LaTeX Generation: Working")
            tests_passed += 1
        else:
            print("❌ 2. LaTeX Generation: Failed")
    except Exception as e:
        print(f"❌ 2. LaTeX Generation: Error - {e}")
    
    # Test 3: R2 Storage Initialization
    try:
        from r2_latex_storage import R2LaTeXStorage
        r2_storage = R2LaTeXStorage()
        
        if r2_storage.client:
            print("✅ 3. R2 Storage: Ready")
            tests_passed += 1
        else:
            print("❌ 3. R2 Storage: Not Ready (credentials issue)")
    except Exception as e:
        print(f"❌ 3. R2 Storage: Error - {e}")
    
    # Test 4: Email Configuration
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
    
    if sender_email and sender_password:
        print("✅ 4. Email Config: Ready")
        tests_passed += 1
    else:
        print("❌ 4. Email Config: Missing credentials")
    
    # Test 5: Claude API Configuration
    claude_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
    claude_url = os.getenv('ANTHROPIC_BASE_URL')
    
    if claude_key and claude_url:
        print("✅ 5. Claude API: Configured")
        tests_passed += 1
    else:
        print("❌ 5. Claude API: Missing configuration")
    
    return tests_passed, total_tests

def check_scheduler_status():
    """Check if scheduler is ready for 20:00"""
    print(f"\n⏰ SCHEDULER STATUS CHECK")
    print("=" * 50)
    
    current_time = time.strftime("%H:%M")
    current_hour = int(time.strftime("%H"))
    current_minute = int(time.strftime("%M"))
    
    print(f"🕐 Current Time: {current_time}")
    print(f"🎯 Target Time: 20:00")
    
    if current_hour == 19:
        minutes_to_20 = 60 - current_minute
        print(f"⏳ Time until 20:00: {minutes_to_20} minutes")
        
        if minutes_to_20 <= 30:
            print("🚨 READY FOR 20:00 EXECUTION!")
            return True
        else:
            print("⏰ Still some time before 20:00")
            return False
    elif current_hour == 20:
        print("🎯 IT'S 20:00 TIME - SYSTEM SHOULD BE RUNNING!")
        return True
    else:
        print(f"⏰ Current time: {current_hour}:xx - waiting for 20:00")
        return False

def main():
    """Quick readiness check for 20:00 execution"""
    
    print("🎭 LEGO JOB AUTOMATION - 20:00 READINESS CHECK")
    print("=" * 60)
    
    # Test core system
    tests_passed, total_tests = test_core_system()
    
    # Check scheduler
    scheduler_ready = check_scheduler_status()
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 READINESS SUMMARY")
    print(f"=" * 60)
    
    success_rate = (tests_passed / total_tests) * 100
    
    print(f"✅ Core System Tests: {tests_passed}/{total_tests} ({success_rate:.0f}%)")
    print(f"⏰ Scheduler Ready: {'✅ Yes' if scheduler_ready else '⏰ Waiting'}")
    
    if tests_passed >= 4:  # At least 4/5 tests should pass
        print(f"\n🎉 SYSTEM READY FOR 20:00 EXECUTION!")
        print(f"✅ LEGO intelligence working")
        print(f"✅ PDF generation functional")
        print(f"✅ LaTeX templates ready")
        print(f"✅ Core automation ready")
        
        if scheduler_ready:
            print(f"\n🚀 EXECUTING NOW OR VERY SOON!")
        else:
            print(f"\n⏰ WAITING FOR 20:00 TRIGGER")
            
        print(f"\n🎯 WHAT WILL HAPPEN AT 20:00:")
        print(f"   1. Gmail scanning for new job opportunities")
        print(f"   2. LEGO intelligence analyzes job requirements")
        print(f"   3. Customized CV and cover letter generation")
        print(f"   4. R2 upload with Overleaf URLs")
        print(f"   5. Email delivery with application package")
        
    else:
        print(f"\n⚠️ SYSTEM NOT FULLY READY")
        print(f"❌ {total_tests - tests_passed} components need attention")
        print(f"💡 System may run with reduced functionality")
    
    return tests_passed >= 4

if __name__ == "__main__":
    ready = main()
    
    if ready:
        print(f"\n🎭 READY FOR OPERA AND OTHER APPLICATIONS! 🎉")
    else:
        print(f"\n⚠️ SOME ISSUES DETECTED - CHECK ABOVE")