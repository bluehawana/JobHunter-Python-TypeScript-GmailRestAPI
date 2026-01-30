#!/usr/bin/env python3
"""
Multi-Source Job Automation Script

This script runs daily job aggregation from all sources:
1. Gmail LinkedIn job emails
2. Gmail Indeed job emails  
3. LinkedIn saved jobs
4. Arbetsförmedlingen API
5. LinkedIn search API

Usage: python multi_source_job_automation.py
For Heroku Scheduler: python multi_source_job_automation.py
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.multi_source_job_aggregator import MultiSourceJobAggregator
from app.services.job_application_processor import JobApplicationProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_daily_job_automation():
    """
    Run complete daily job automation workflow
    """
    
    print("🚀 Starting Multi-Source Job Automation")
    print("=" * 60)
    
    try:
        # Initialize services
        print("📧 Initializing job aggregation services...")
        aggregator = MultiSourceJobAggregator()
        processor = JobApplicationProcessor()
        
        # Run job aggregation from all sources
        print("🔍 Running job aggregation from all sources...")
        print("   Sources: Gmail LinkedIn, Gmail Indeed, LinkedIn Saved, Arbetsförmedlingen, LinkedIn Search")
        
        # Use a default user ID - in production, this would be configurable
        user_id = "default_user"  # You might get this from environment or config
        
        results = await aggregator.aggregate_all_jobs(user_id)
        
        print(f"✅ Job aggregation completed!")
        print(f"   📊 Total jobs found: {results['total_jobs_found']}")
        print(f"   🆕 New jobs: {results['new_jobs']}")
        print(f"   🔄 Duplicates removed: {results['duplicates_removed']}")
        
        # Show results by source
        print("\n📋 Results by source:")
        for source, data in results['sources'].items():
            print(f"   {source}: {data['jobs_found']} found, {data['new_jobs']} new")
        
        # Show any errors
        if results['errors']:
            print("\n⚠️  Errors encountered:")
            for error in results['errors']:
                print(f"   ❌ {error}")
        
        # Process high-priority jobs automatically
        print("\n🎯 Processing high-priority jobs...")
        
        # Get high-priority saved jobs
        high_priority_jobs = await get_high_priority_jobs(user_id)
        
        if high_priority_jobs:
            print(f"   Found {len(high_priority_jobs)} high-priority jobs to process")
            
            processing_results = await aggregator.process_selected_jobs(
                user_id=user_id,
                job_ids=high_priority_jobs
            )
            
            print(f"   ✅ Processed: {processing_results['processed_jobs']}")
            print(f"   📄 Applications generated: {processing_results['successful_applications']}")
            
            if processing_results['errors']:
                print("   ⚠️  Processing errors:")
                for error in processing_results['errors']:
                    print(f"     ❌ {error}")
        else:
            print("   No high-priority jobs to process automatically")
        
        # Send daily summary email
        print("\n📧 Sending daily summary email...")
        await send_daily_summary_email(results, high_priority_jobs)
        
        print("\n🎉 Daily job automation completed successfully!")
        print("=" * 60)
        
        # Print summary for logs
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_jobs_found': results['total_jobs_found'],
            'new_jobs': results['new_jobs'],
            'high_priority_processed': len(high_priority_jobs) if high_priority_jobs else 0,
            'errors': len(results['errors'])
        }
        
        print(f"📊 SUMMARY: {summary}")
        
        return True
        
    except Exception as e:
        logger.error(f"Daily job automation failed: {e}")
        print(f"\n❌ Daily job automation failed: {e}")
        
        # Send error notification
        await send_error_notification(str(e))
        
        return False

async def get_high_priority_jobs(user_id: str) -> list:
    """
    Get list of high-priority job IDs that should be processed automatically
    """
    try:
        # In a real implementation, this would query the database for:
        # - Jobs with priority='high' or priority='urgent'
        # - Jobs with application_status='saved'
        # - Jobs discovered in the last 24 hours
        
        # For now, return empty list as placeholder
        return []
        
    except Exception as e:
        logger.error(f"Error getting high-priority jobs: {e}")
        return []

async def send_daily_summary_email(results: dict, processed_jobs: list):
    """
    Send daily summary email to leeharvad@gmail.com
    """
    try:
        from app.services.email_automation_service import EmailAutomationService
        
        email_service = EmailAutomationService()
        
        # Prepare email content
        subject = f"Daily Job Hunt Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = f"""
Dear Lee,

Here's your daily job hunting summary:

📊 JOB DISCOVERY RESULTS:
• Total jobs found: {results['total_jobs_found']}
• New jobs discovered: {results['new_jobs']}
• Duplicates removed: {results['duplicates_removed']}

📋 JOBS BY SOURCE:
"""
        
        for source, data in results['sources'].items():
            content += f"• {source}: {data['jobs_found']} found, {data['new_jobs']} new\n"
        
        if processed_jobs:
            content += f"\n🎯 HIGH-PRIORITY PROCESSING:\n"
            content += f"• {len(processed_jobs)} high-priority jobs processed automatically\n"
            content += f"• Application documents generated and ready for review\n"
        
        if results['errors']:
            content += f"\n⚠️ ERRORS ENCOUNTERED:\n"
            for error in results['errors']:
                content += f"• {error}\n"
        
        content += f"""

🔗 NEXT STEPS:
1. Review new jobs in your dashboard
2. Set priority levels for interesting positions
3. Review generated application documents
4. Apply to selected positions

Best regards,
JobHunter Automation System
Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""
        
        # Send email
        await email_service.send_summary_email(
            to_email="leeharvad@gmail.com",
            subject=subject,
            content=content
        )
        
        print("   ✅ Daily summary email sent to leeharvad@gmail.com")
        
    except Exception as e:
        logger.error(f"Error sending daily summary email: {e}")
        print(f"   ❌ Failed to send summary email: {e}")

async def send_error_notification(error_message: str):
    """
    Send error notification email
    """
    try:
        from app.services.email_automation_service import EmailAutomationService
        
        email_service = EmailAutomationService()
        
        subject = f"JobHunter Automation Error - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = f"""
Alert: JobHunter Automation Error

The daily job automation process encountered an error:

Error: {error_message}
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

Please check the application logs for more details.

Best regards,
JobHunter Automation System
"""
        
        await email_service.send_summary_email(
            to_email="leeharvad@gmail.com",
            subject=subject,
            content=content
        )
        
    except Exception as e:
        logger.error(f"Error sending error notification: {e}")

async def main():
    """Main function to run the daily job automation"""
    print("Multi-Source Job Automation - Daily Run")
    print("Aggregating jobs from all configured sources")
    print()
    
    success = await run_daily_job_automation()
    
    if success:
        print("\n✅ Daily job automation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Daily job automation failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())