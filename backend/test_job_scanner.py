#!/usr/bin/env python3
"""
Test script for the complete job scanning and application workflow 
"""
import asyncio
import logging
import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.job_hunter_orchestrator import JobHunterOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_complete_workflow():
    """Test the complete job hunting workflow"""
    
    print("🚀 JobHunter Complete Workflow Test")
    print("=" * 50)
    
    try:
        # Initialize orchestrator
        orchestrator = JobHunterOrchestrator()
        
        # Test 1: Check Gmail connection (if credentials available)
        print("\n📧 Testing Gmail Connection...")
        gmail_connected = await orchestrator.test_gmail_connection()
        
        if gmail_connected:
            print("✅ Gmail connection successful!")
        else:
            print("⚠️  Gmail connection failed - check app password setup")
            print("   You need to set GMAIL_APP_PASSWORD in .env for bluehawana@gmail.com")
        
        # Test 2: Process a mock job to test document generation and email sending
        print("\n📄 Testing Document Generation & Email Sending...")
        
        mock_job = {
            'source': 'test',
            'title': 'Senior Fullstack Developer',
            'company': 'InnovaTech Solutions',
            'location': 'Stockholm, Sweden',
            'description': '''
            We are seeking a Senior Fullstack Developer to join our innovative team. 
            You will work with React, Node.js, Python, and AWS to build scalable web applications.
            Experience with Docker, Kubernetes, and CI/CD pipelines is highly valued.
            You'll collaborate with cross-functional teams and mentor junior developers.
            ''',
            'application_link': 'https://www.linkedin.com/jobs/view/3721234567',
            'keywords': ['react', 'nodejs', 'python', 'aws', 'docker', 'kubernetes', 'fullstack'],
            'salary': '650,000 - 800,000 SEK',
            'employment_type': 'Permanent',
            'date_received': datetime.now().strftime('%Y-%m-%d'),
            'hiring_manager': 'Anna Larsson'
        }
        
        success = await orchestrator.process_single_job(mock_job)
        
        if success:
            print("✅ Mock job processed successfully!")
            print("   📧 Check hongzhili01@gmail.com for the job notification email")
            print("   📎 Email includes customized CV and Cover Letter")
            print("   🔗 Email includes direct application link")
        else:
            print("❌ Mock job processing failed")
        
        # Test 3: Get job processing summary
        print("\n📊 Job Processing Summary...")
        summary = await orchestrator.get_job_summary()
        
        print(f"   Total processed jobs: {summary.get('total_processed', 0)}")
        print(f"   Jobs by date: {summary.get('jobs_by_date', {})}")
        
        # Test 4: Run daily scan (if Gmail is connected)
        if gmail_connected:
            print("\n🔍 Running Daily Job Scan (limited to 2 jobs for testing)...")
            orchestrator.max_jobs_per_run = 2  # Limit for testing
            
            results = await orchestrator.run_daily_job_scan()
            
            print("📈 Scan Results:")
            print(f"   📧 Total jobs found: {results.get('total_found', 0)}")
            print(f"   🆕 New jobs: {results.get('new_jobs', 0)}")
            print(f"   ✅ Successful emails: {results.get('successful_emails', 0)}")
            print(f"   ❌ Failed emails: {results.get('failed_emails', 0)}")
            
            if results.get('jobs_processed'):
                print("   📋 Jobs processed:")
                for job in results['jobs_processed']:
                    print(f"      • {job['company']} - {job['title']} ({job['status']})")
        
        print("\n🎉 Complete workflow test finished!")
        print("\n💡 Next Steps:")
        print("   1. Set up Gmail app password for bluehawana@gmail.com")
        print("   2. Update GMAIL_APP_PASSWORD in .env file")
        print("   3. Add to your daily cron job: 'python3 run_daily_job_scan.py'")
        print("   4. Check hongzhili01@gmail.com for job notifications")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

async def test_email_formats():
    """Test different email parsing scenarios"""
    print("\n📧 Testing Email Format Parsing...")
    
    from app.services.job_scanner_service import JobScannerService
    scanner = JobScannerService()
    
    # Test job detection
    test_subjects = [
        "New Job Alert: Senior Developer at TechCorp",
        "Job Opportunity: Fullstack Engineer - Stockholm",
        "We're Hiring: Python Developer",
        "Newsletter Update",  # Should be filtered out
        "Apply Now: DevOps Engineer at InnovateAB"
    ]
    
    for subject in test_subjects:
        is_job = scanner._is_job_email(subject, "job description content")
        print(f"   '{subject}' -> {'✅ Job' if is_job else '❌ Not Job'}")
    
    # Test link extraction
    test_content = """
    Apply for this position at: https://www.linkedin.com/jobs/view/3721234567
    or visit our website: https://company.com/careers
    Indeed link: https://se.indeed.com/viewjob?jk=abc123def456
    """
    
    link = scanner._extract_application_link(test_content)
    print(f"   Extracted link: {link}")

if __name__ == "__main__":
    print("🎯 JobHunter Automation Test Suite")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_email_formats())
    asyncio.run(test_complete_workflow())
    
    print("\n" + "=" * 60)
    print("✨ Test suite completed!")
    print("Check the logs above for detailed results.")