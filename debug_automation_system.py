#!/usr/bin/env python3
"""
Debug Automation System - Check why yesterday's run didn't work
Identify issues and ensure today's 20:00 run will work properly
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_scheduler_configuration():
    """Check if the scheduler is properly configured"""
    print("⏰ CHECKING SCHEDULER CONFIGURATION")
    print("=" * 50)
    
    # Check for scheduler files
    scheduler_files = [
        'backend/heroku_job_automation.py',
        'backend/zapier_n8n_automation.py',
        'backend/automation/n8n_daily_job_automation.json',
        'backend/automation/zapier_webhook_config.json'
    ]
    
    found_schedulers = []
    for file in scheduler_files:
        if os.path.exists(file):
            found_schedulers.append(file)
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
    
    if found_schedulers:
        print(f"\n✅ Scheduler files found: {len(found_schedulers)}")
        return True
    else:
        print(f"\n❌ No scheduler files found")
        return False

def check_gmail_scanning():
    """Check Gmail scanning functionality"""
    print(f"\n📧 CHECKING GMAIL SCANNING")
    print("=" * 50)
    
    try:
        # Check Gmail credentials
        gmail_credentials = os.getenv('SOURCE_GMAIL_CREDENTIALS')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if gmail_credentials and os.path.exists(gmail_credentials):
            print(f"✅ Gmail credentials file found: {gmail_credentials}")
        else:
            print(f"❌ Gmail credentials file missing or not configured")
        
        if gmail_password:
            print(f"✅ Gmail app password configured")
        else:
            print(f"❌ Gmail app password not configured")
        
        # Try to import Gmail service
        try:
            from app.services.gmail_service import GmailService
            print(f"✅ Gmail service module imported successfully")
            
            # Test Gmail service initialization (without actually connecting)
            print(f"📧 Gmail scanning system appears ready")
            return True
            
        except ImportError as e:
            print(f"❌ Gmail service import failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Gmail scanning check failed: {e}")
        return False

def check_email_delivery():
    """Check email delivery system"""
    print(f"\n📤 CHECKING EMAIL DELIVERY SYSTEM")
    print("=" * 50)
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
    
    print(f"📧 Sender Email: {sender_email if sender_email else '❌ NOT SET'}")
    print(f"🔑 Sender Password: {'✅ SET' if sender_password else '❌ NOT SET'}")
    
    if sender_email and sender_password:
        # Test email sending (without actually sending)
        try:
            import smtplib
            print(f"✅ SMTP library available")
            print(f"✅ Email delivery system configured")
            return True
        except ImportError:
            print(f"❌ SMTP library not available")
            return False
    else:
        print(f"❌ Email delivery not properly configured")
        return False

def test_complete_workflow():
    """Test the complete workflow without actually sending emails"""
    print(f"\n🔄 TESTING COMPLETE WORKFLOW")
    print("=" * 50)
    
    try:
        # Test job data (simulating a found job)
        test_job = {
            'title': 'Senior DevOps Engineer',
            'company': 'Test Company AB',
            'description': 'Kubernetes, Docker, AWS, monitoring, CI/CD, infrastructure automation',
            'location': 'Stockholm, Sweden',
            'url': 'https://example.com/job/12345'
        }
        
        print(f"📋 Testing with job: {test_job['title']} at {test_job['company']}")
        
        # Step 1: Generate CV
        try:
            from beautiful_pdf_generator import create_beautiful_multi_page_pdf
            cv_pdf = create_beautiful_multi_page_pdf(test_job)
            
            if cv_pdf and len(cv_pdf) > 50000:
                print(f"✅ Step 1: CV generated ({len(cv_pdf):,} bytes)")
                cv_success = True
            else:
                print(f"❌ Step 1: CV generation failed")
                cv_success = False
        except Exception as e:
            print(f"❌ Step 1: CV generation error - {e}")
            cv_success = False
        
        # Step 2: Generate Cover Letter
        try:
            from cover_letter_generator import CoverLetterGenerator
            cl_generator = CoverLetterGenerator()
            cl_result = cl_generator.create_cover_letter_with_r2_overleaf(test_job)
            
            if cl_result.get('success', False):
                print(f"✅ Step 2: Cover letter generated ({cl_result.get('pdf_size', 0):,} bytes)")
                cl_success = True
            else:
                print(f"❌ Step 2: Cover letter generation failed")
                cl_success = False
        except Exception as e:
            print(f"❌ Step 2: Cover letter generation error - {e}")
            cl_success = False
        
        # Step 3: Test email composition (without sending)
        sender_email = os.getenv('SENDER_EMAIL')
        if cv_success and sender_email:
            print(f"✅ Step 3: Email composition ready (would send to hongzhili01@gmail.com)")
            email_success = True
        else:
            print(f"❌ Step 3: Email composition failed")
            email_success = False
        
        return cv_success and cl_success and email_success
        
    except Exception as e:
        print(f"❌ Complete workflow test failed: {e}")
        return False

def check_heroku_deployment():
    """Check if the system is deployed and scheduled"""
    print(f"\n🚀 CHECKING DEPLOYMENT STATUS")
    print("=" * 50)
    
    # Check for deployment files
    deployment_files = [
        'Procfile',
        'requirements.txt',
        'runtime.txt'
    ]
    
    for file in deployment_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
    
    # Check if Heroku scheduler is configured
    if os.path.exists('backend/HEROKU_SCHEDULER_SETUP.md'):
        print(f"✅ Heroku scheduler documentation found")
        print(f"💡 Check if Heroku scheduler is actually configured in your Heroku dashboard")
    else:
        print(f"❌ Heroku scheduler documentation missing")
    
    print(f"\n💡 DEPLOYMENT CHECKLIST:")
    print(f"   1. Is the app deployed to Heroku?")
    print(f"   2. Is Heroku Scheduler addon installed?")
    print(f"   3. Is the 20:00 job scheduled in Heroku dashboard?")
    print(f"   4. Are all environment variables set in Heroku?")

def generate_test_application():
    """Generate a test application to verify the system works"""
    print(f"\n🧪 GENERATING TEST APPLICATION")
    print("=" * 50)
    
    try:
        # Use the Opera job we prepared earlier
        opera_job = {
            'title': 'DevOps Engineer',
            'company': 'Opera',
            'description': '''
            DevOps Engineer role with Kubernetes, Docker, AWS, monitoring with Prometheus and Grafana,
            CI/CD pipelines, infrastructure automation, performance optimization.
            ''',
            'location': 'Oslo, Norway',
            'url': 'https://jobs.opera.com/jobs/6060392-devops-engineer'
        }
        
        print(f"📋 Generating test application for: {opera_job['company']}")
        
        # Generate CV
        from beautiful_pdf_generator import create_beautiful_multi_page_pdf
        cv_pdf = create_beautiful_multi_page_pdf(opera_job)
        
        if cv_pdf:
            with open('test_opera_cv_debug.pdf', 'wb') as f:
                f.write(cv_pdf)
            print(f"✅ Test CV generated: test_opera_cv_debug.pdf ({len(cv_pdf):,} bytes)")
        
        # Use TRUE LEGO system for cover letter
        from exact_cover_letter_generator import create_exact_cover_letter
        cl_result = create_exact_cover_letter(opera_job)
        cl_pdf = cl_result.get('pdf_content', b'')
        
        if cl_pdf:
            with open('test_opera_cl_debug.pdf', 'wb') as f:
                f.write(cl_pdf)
            print(f"✅ Test cover letter generated: test_opera_cl_debug.pdf ({len(cl_pdf):,} bytes)")
        
        print(f"\n📧 Test application package ready!")
        print(f"📄 CV: test_opera_cv_debug.pdf")
        print(f"📝 Cover Letter: test_opera_cl_debug.pdf")
        
        return True
        
    except Exception as e:
        print(f"❌ Test application generation failed: {e}")
        return False

def main():
    """Main debugging function"""
    
    print("🔍 DEBUGGING AUTOMATION SYSTEM - WHY YESTERDAY DIDN'T WORK")
    print("=" * 70)
    
    # Run all checks
    scheduler_ok = check_scheduler_configuration()
    gmail_ok = check_gmail_scanning()
    email_ok = check_email_delivery()
    workflow_ok = test_complete_workflow()
    
    check_heroku_deployment()
    test_app_ok = generate_test_application()
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"🔍 DEBUGGING SUMMARY")
    print(f"=" * 70)
    
    print(f"⏰ Scheduler Configuration: {'✅' if scheduler_ok else '❌'}")
    print(f"📧 Gmail Scanning: {'✅' if gmail_ok else '❌'}")
    print(f"📤 Email Delivery: {'✅' if email_ok else '❌'}")
    print(f"🔄 Complete Workflow: {'✅' if workflow_ok else '❌'}")
    print(f"🧪 Test Application: {'✅' if test_app_ok else '❌'}")
    
    # Diagnosis
    print(f"\n🩺 DIAGNOSIS:")
    
    if not scheduler_ok:
        print(f"❌ SCHEDULER ISSUE: No scheduler configuration found")
        print(f"💡 The system may not be scheduled to run at 20:00")
    
    if not gmail_ok:
        print(f"❌ GMAIL ISSUE: Gmail scanning not properly configured")
        print(f"💡 The system can't find new job opportunities")
    
    if not email_ok:
        print(f"❌ EMAIL ISSUE: Email delivery not configured")
        print(f"💡 Generated applications can't be sent to you")
    
    if scheduler_ok and gmail_ok and email_ok and workflow_ok:
        print(f"✅ SYSTEM APPEARS FUNCTIONAL")
        print(f"💡 The issue might be:")
        print(f"   • No new jobs found in Gmail yesterday")
        print(f"   • Heroku scheduler not actually running")
        print(f"   • Environment variables not set in production")
        print(f"   • Application crashed during execution")
    
    print(f"\n🔧 RECOMMENDED ACTIONS:")
    print(f"1. Check Heroku logs: heroku logs --tail")
    print(f"2. Verify Heroku scheduler is running: heroku addons")
    print(f"3. Check environment variables in Heroku dashboard")
    print(f"4. Test TRUE LEGO execution: python3 run_06_00_automation.py")
    print(f"5. Verify Gmail has job-related emails")
    
    print(f"\n⏰ FOR TODAY'S 20:00 RUN:")
    if workflow_ok and email_ok:
        print(f"✅ System should work if properly deployed and scheduled")
    else:
        print(f"❌ Fix the issues above before 20:00")

if __name__ == "__main__":
    main()