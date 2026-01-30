#!/usr/bin/env python3
"""
Daily job scanning automation script
Add this to your cron job to run automatic job scanning and application generation
"""
import asyncio
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.job_hunter_orchestrator import JobHunterOrchestrator

# Setup logging to file
log_file = f"job_scan_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def run_daily_scan():
    """Run the daily job scanning workflow"""
    
    logger.info("🚀 Starting daily job scanning automation")
    logger.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize orchestrator
        orchestrator = JobHunterOrchestrator()
        
        # Check if required environment variables are set
        required_vars = ['SENDER_EMAIL', 'SMTP_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"❌ Missing required environment variables: {missing_vars}")
            return False
        
        # Run the daily job scan
        results = await orchestrator.run_daily_job_scan()
        
        # Log results
        if 'error' in results:
            logger.error(f"❌ Daily scan failed: {results['error']}")
            return False
        
        logger.info("📊 Daily job scan results:")
        logger.info(f"   📧 Total jobs found: {results.get('total_found', 0)}")
        logger.info(f"   🆕 New jobs: {results.get('new_jobs', 0)}")
        logger.info(f"   ✅ Successful emails: {results.get('successful_emails', 0)}")
        logger.info(f"   ❌ Failed emails: {results.get('failed_emails', 0)}")
        
        # Log processed jobs
        if results.get('jobs_processed'):
            logger.info("📋 Jobs processed today:")
            for job in results['jobs_processed']:
                status_emoji = "✅" if job['status'] == 'success' else "❌"
                logger.info(f"   {status_emoji} {job['company']} - {job['title']}")
        
        # Clean up old processed jobs (keep last 30 days)
        await orchestrator.cleanup_old_processed_jobs(days_to_keep=30)
        
        # Success summary
        if results.get('successful_emails', 0) > 0:
            logger.info(f"🎉 Daily scan completed successfully!")
            logger.info(f"📧 {results['successful_emails']} job notification emails sent to hongzhili01@gmail.com")
            logger.info("💡 Check your email for new job opportunities with tailored CV/CL!")
        else:
            logger.info("✅ Daily scan completed - no new jobs found today")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Daily scan failed with error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def setup_cron_reminder():
    """Print cron setup instructions"""
    print("\n📅 CRON JOB SETUP INSTRUCTIONS:")
    print("=" * 50)
    print("Add this to your crontab (run 'crontab -e'):")
    print("")
    print("# Daily job scanning at 9:00 AM on weekdays")
    print("0 9 * * 1-5 cd /Users/bluehawana/Projects/Jobhunter/backend && python3 run_daily_job_scan.py")
    print("")
    print("# Alternative: Run every 3 hours on weekdays")
    print("0 */3 * * 1-5 cd /Users/bluehawana/Projects/Jobhunter/backend && python3 run_daily_job_scan.py")
    print("")
    print("Make sure to:")
    print("1. Set GMAIL_APP_PASSWORD in .env for bluehawana@gmail.com")
    print("2. Enable 2-factor authentication on Gmail")
    print("3. Generate app password: Gmail Settings > Security > App passwords")
    print("4. Test the script manually first")
    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_cron_reminder()
    else:
        # Run the daily scan
        success = asyncio.run(run_daily_scan())
        
        if success:
            print("✅ Daily job scan completed successfully!")
            sys.exit(0)
        else:
            print("❌ Daily job scan failed!")
            sys.exit(1)