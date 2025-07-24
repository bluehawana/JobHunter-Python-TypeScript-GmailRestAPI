#!/usr/bin/env python3
"""
Test script for job fetching functionality

This script demonstrates how to:
1. Set up the database table (run the SQL schema first)
2. Fetch jobs from URLs and save to database
3. Query and manage job applications

Before running this script:
1. Run the SQL schema in job_applications_schema.sql in your Supabase database
2. Set your SUPABASE_URL and SUPABASE_ANON_KEY environment variables
3. Install required dependencies: pip install -r requirements.txt
"""

import asyncio
import os
import sys
from typing import List

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.supabase_service import supabase_service
from app.services.job_link_fetcher import job_link_fetcher

async def test_job_fetching():
    """Test the job fetching functionality"""
    
    print("🚀 Starting Job Fetching Test")
    print("=" * 50)
    
    # Example job URLs - replace these with actual job URLs you want to test
    test_urls = [
        # Add your job URLs here
        # "https://www.linkedin.com/jobs/view/12345",
        # "https://se.indeed.com/viewjob?jk=abcd1234", 
        # "https://arbetsformedlingen.se/platsbanken/annonser/12345"
    ]
    
    if not test_urls:
        print("⚠️  No test URLs provided. Please add some job URLs to test_urls list.")
        print("\n📝 Example usage:")
        print('test_urls = ["https://linkedin.com/jobs/view/123", "https://indeed.com/viewjob?jk=456"]')
        return
    
    print(f"📋 Testing with {len(test_urls)} job URLs:")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    
    print("\n🔍 Fetching jobs from URLs...")
    
    try:
        # Fetch and save jobs
        results = await job_link_fetcher.fetch_and_save_jobs(test_urls)
        
        print(f"\n✅ Successfully processed {len(results)} jobs!")
        
        # Display results
        for i, job in enumerate(results, 1):
            print(f"\n📄 Job {i}:")
            print(f"  📋 Title: {job.get('job_title', 'N/A')}")
            print(f"  🏢 Company: {job.get('company_name', 'N/A')}")
            print(f"  📍 Location: {job.get('location', 'N/A')}")
            print(f"  💼 Work Type: {job.get('work_type', 'N/A')}")
            print(f"  📅 Status: {job.get('application_status', 'N/A')}")
            print(f"  🔗 Link: {job.get('application_link', 'N/A')}")
            print(f"  🆔 ID: {job.get('id', 'N/A')}")
        
        # Test querying jobs
        print(f"\n📊 Querying all job applications...")
        all_jobs = await supabase_service.get_job_applications(limit=10)
        print(f"📈 Found {len(all_jobs)} total job applications in database")
        
        # Test statistics
        print(f"\n📈 Getting application statistics...")
        stats = await supabase_service.get_application_statistics()
        print(f"📊 Total applications: {stats.get('total_applications', 0)}")
        print(f"📊 By status: {stats.get('by_status', {})}")
        print(f"📊 Recent applications: {stats.get('recent_applications', 0)}")
        
        print(f"\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

async def demo_job_management():
    """Demonstrate job application management features"""
    
    print("\n🔧 Job Management Demo")
    print("=" * 30)
    
    try:
        # Get all applications
        apps = await supabase_service.get_job_applications(limit=5)
        
        if not apps:
            print("ℹ️  No job applications found. Run the job fetching test first.")
            return
        
        # Take the first application for demo
        app = apps[0]
        app_id = app['id']
        
        print(f"📋 Working with application: {app.get('job_title')} at {app.get('company_name')}")
        print(f"🆔 Application ID: {app_id}")
        
        # Update status
        print(f"\n📝 Updating application status to 'applied'...")
        success = await supabase_service.update_application_status(
            app_id, 
            'applied', 
            'Applied through company website'
        )
        print(f"✅ Status update: {'Success' if success else 'Failed'}")
        
        # Add interview round
        print(f"\n📅 Adding interview round...")
        interview_data = {
            "round": 1,
            "type": "phone_screen", 
            "date": "2024-01-25",
            "interviewer": "John Doe - HR Manager",
            "notes": "Initial screening call - 30 minutes",
            "result": "pending"
        }
        
        success = await supabase_service.add_interview_round(app_id, interview_data)
        print(f"✅ Interview round added: {'Success' if success else 'Failed'}")
        
        # Add communication log
        print(f"\n📧 Adding communication log...")
        comm_data = {
            "date": "2024-01-20",
            "type": "email",
            "direction": "outgoing", 
            "subject": "Application for Backend Developer Position",
            "summary": "Sent initial application with resume and cover letter"
        }
        
        success = await supabase_service.add_communication_log(app_id, comm_data)
        print(f"✅ Communication log added: {'Success' if success else 'Failed'}")
        
        # Get updated application
        print(f"\n🔍 Retrieving updated application...")
        updated_app = await supabase_service.get_job_application(app_id)
        
        if updated_app:
            print(f"📋 Updated Status: {updated_app.get('application_status')}")
            print(f"📅 Interview Rounds: {len(updated_app.get('interview_rounds', []))}")
            print(f"📧 Communications: {len(updated_app.get('communications', []))}")
            print(f"📝 Last Updated: {updated_app.get('updated_at')}")
        
        print(f"\n🎉 Job management demo completed!")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    
    print("🔧 JobHunter - Job Fetching System Test")
    print("=" * 60)
    
    # Check environment variables
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_ANON_KEY"):
        print("❌ Missing environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY")
        print("\nExample:")
        print('export SUPABASE_URL="https://your-project.supabase.co"')
        print('export SUPABASE_ANON_KEY="your-anon-key"')
        return
    
    print("✅ Environment variables found")
    print(f"🔗 Supabase URL: {os.getenv('SUPABASE_URL')}")
    
    # Test basic connectivity
    try:
        stats = await supabase_service.get_application_statistics()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Make sure:")
        print("1. Your Supabase project is running")
        print("2. The job_applications table has been created (run job_applications_schema.sql)")
        print("3. Your environment variables are correct")
        return
    
    # Run tests
    await test_job_fetching()
    await demo_job_management()

if __name__ == "__main__":
    # Set up environment variables if not already set
    if not os.getenv("SUPABASE_URL"):
        print("⚠️  Setting example environment variables...")
        print("Please replace these with your actual Supabase credentials!")
        os.environ["SUPABASE_URL"] = "https://chcdebpjwallysedcfsq.supabase.co"
        os.environ["SUPABASE_ANON_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNoY2RlYnBqd2FsbHlzZWRjZnNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMzNTU5OTUsImV4cCI6MjA2ODkzMTk5NX0.YXdUPS9q1O1SF0aRwYD-qG8NfUQrGD4U4MJSOwp4IrM"
    
    asyncio.run(main())