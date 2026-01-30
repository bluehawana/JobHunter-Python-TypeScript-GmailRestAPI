#!/usr/bin/env python3
"""
Process jobs from LinkedIn and Gmail, generate PDFs, and send to email

This script will:
1. Fetch the job from LinkedIn URL using your LinkedIn credentials
2. Process the Gmail job search
3. Generate customized PDFs for both jobs
4. Send emails with job info and PDFs to leeharvad@gmail.com

Usage: python process_jobs_and_send.py
"""

import asyncio
import os
import sys
from typing import List, Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.job_processor import job_processor
from app.services.supabase_service import supabase_service

# Your job URLs
LINKEDIN_JOB_URL = "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4266325638"
GMAIL_JOB_URL = "https://mail.google.com/mail/u/0/#search/linkedin+jobs/FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx"
TARGET_EMAIL = "leeharvad@gmail.com"

async def process_jobs():
    """Process both jobs and send application materials"""
    
    print("🚀 Starting Job Processing and Application Generation")
    print("=" * 60)
    
    # Set up environment variables
    setup_environment()
    
    processed_jobs = []
    
    try:
        # Process LinkedIn job
        print(f"📋 Processing LinkedIn job...")
        print(f"🔗 URL: {LINKEDIN_JOB_URL}")
        
        linkedin_job = await job_processor.process_linkedin_job(LINKEDIN_JOB_URL)
        if linkedin_job:
            processed_jobs.append(linkedin_job)
            print(f"✅ LinkedIn job processed: {linkedin_job.get('job_title')} at {linkedin_job.get('company_name')}")
        else:
            print("❌ Failed to process LinkedIn job")
        
        # Process Gmail job
        print(f"\n📧 Processing Gmail job...")
        print(f"🔗 URL: {GMAIL_JOB_URL}")
        
        gmail_job = await job_processor.process_gmail_job(GMAIL_JOB_URL)
        if gmail_job:
            processed_jobs.append(gmail_job)
            print(f"✅ Gmail job processed: {gmail_job.get('job_title')} at {gmail_job.get('company_name')}")
        else:
            print("❌ Failed to process Gmail job")
        
        if not processed_jobs:
            print("❌ No jobs were successfully processed. Exiting.")
            return
        
        print(f"\n📄 Generating application materials for {len(processed_jobs)} job(s)...")
        
        # Process each job
        for i, job in enumerate(processed_jobs, 1):
            try:
                print(f"\n📋 Processing Job {i}: {job.get('job_title')} at {job.get('company_name')}")
                
                # Generate application materials
                print("🔄 Generating customized CV and cover letter...")
                materials = await job_processor.generate_application_materials(job)
                
                if materials.get('cv') and materials.get('cover_letter'):
                    print(f"✅ Generated {len(materials['cv'])} bytes CV and {len(materials['cover_letter'])} bytes cover letter")
                    
                    # Send email with materials
                    print(f"📧 Sending application materials to {TARGET_EMAIL}...")
                    await job_processor.send_job_application_email(job, materials, TARGET_EMAIL)
                    print("✅ Email sent successfully!")
                    
                    # Log communication
                    await supabase_service.add_communication_log(
                        job.get('id'),
                        {
                            "date": datetime.now().isoformat(),
                            "type": "email",
                            "direction": "outgoing",
                            "subject": f"Job Application Materials - {job.get('job_title')}",
                            "summary": f"Sent customized CV and cover letter to {TARGET_EMAIL}"
                        }
                    )
                    
                else:
                    print("❌ Failed to generate application materials")
                    
            except Exception as e:
                print(f"❌ Error processing job {i}: {e}")
                continue
        
        # Display summary
        print(f"\n📊 Processing Summary")
        print("=" * 30)
        print(f"Total jobs processed: {len(processed_jobs)}")
        print(f"Target email: {TARGET_EMAIL}")
        
        for job in processed_jobs:
            print(f"• {job.get('job_title')} at {job.get('company_name')}")
            print(f"  Status: {job.get('application_status')}")
            print(f"  Link: {job.get('application_link')}")
        
        print(f"\n🎉 Job processing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Critical error during job processing: {e}")
        import traceback
        traceback.print_exc()

def setup_environment():
    """Set up environment variables"""
    
    # Check required environment variables
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY", 
        "LINKEDIN_ACCESS_TOKEN",
        "LINKEDIN_CLIENT_ID",
        "LINKEDIN_CLIENT_SECRET"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these environment variables before running the script.")
        sys.exit(1)
    
    # Gmail app password (you'll need to set this up)
    if not os.getenv("GMAIL_APP_PASSWORD"):
        print("⚠️  WARNING: GMAIL_APP_PASSWORD not set!")
        print("To send emails, you need to:")
        print("1. Go to your Google Account settings")
        print("2. Enable 2-factor authentication")
        print("3. Generate an 'App Password' for JobHunter")
        print("4. Set: export GMAIL_APP_PASSWORD='your-16-char-app-password'")
        print("\nFor now, using a placeholder...")
        os.environ["GMAIL_APP_PASSWORD"] = "placeholder-password"

async def test_individual_components():
    """Test individual components"""
    
    print("\n🔧 Testing Individual Components")
    print("=" * 40)
    
    try:
        # Test database connection
        print("📊 Testing database connection...")
        stats = await supabase_service.get_application_statistics()
        print(f"✅ Database connected. Total applications: {stats.get('total_applications', 0)}")
        
        # Test LinkedIn service
        print("\n📋 Testing LinkedIn service...")
        from app.services.linkedin_service import LinkedInService
        linkedin_service = LinkedInService()
        
        # Try to get a sample job (this might fail if API limits are reached)
        try:
            jobs = await linkedin_service.search_jobs("developer", "Sweden", num_results=1)
            if jobs:
                print(f"✅ LinkedIn API working. Found: {jobs[0].get('title', 'Unknown')}")
            else:
                print("⚠️  LinkedIn API returned no results (might be rate limited)")
        except Exception as e:
            print(f"⚠️  LinkedIn API error (expected): {e}")
        
        # Test LaTeX service
        print("\n📄 Testing LaTeX service...")
        from app.services.latex_resume_service import LaTeXResumeService
        latex_service = LaTeXResumeService()
        
        test_job = {
            'title': 'Test Developer',
            'company': 'Test Company',
            'description': 'Test job for fullstack developer with React and Node.js',
            'keywords': ['react', 'nodejs', 'fullstack']
        }
        
        try:
            cv_pdf = await latex_service.generate_customized_cv(test_job)
            if cv_pdf and len(cv_pdf) > 0:
                print(f"✅ LaTeX service working. Generated {len(cv_pdf)} bytes PDF")
            else:
                print("❌ LaTeX service failed to generate PDF")
        except Exception as e:
            print(f"❌ LaTeX service error: {e}")
            print("Make sure pdflatex is installed: sudo apt-get install texlive-latex-base")
        
        print("\n✅ Component testing completed")
        
    except Exception as e:
        print(f"❌ Component testing failed: {e}")

if __name__ == "__main__":
    print("JobHunter - Automated Job Application System")
    print("Processing jobs for Hongzhi Li (Thomthon Retuier)")
    print("Target email: leeharvad@gmail.com")
    print()
    
    # Import datetime here since it's used in the async function
    from datetime import datetime
    
    # Run the processing
    asyncio.run(process_jobs())
    
    # Optionally run component tests
    print("\n" + "="*60)
    user_input = input("Run component tests? (y/n): ").lower().strip()
    if user_input == 'y':
        asyncio.run(test_individual_components())