#!/usr/bin/env python3
"""
Fully Automated Job Hunter Scheduler
Runs completely hands-off with webhook triggers and notifications
"""
import asyncio
import schedule
import time
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.professional_latex_service import ProfessionalLaTeXService
from app.services.job_application_processor import JobApplicationProcessor
from app.services.twilio_notification_service import TwilioNotificationService

# Load environment variables
def load_env_file():
    try:
        env_path = Path(__file__).parent.parent / '.env'
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomatedJobHunter:
    """Fully automated job hunting system"""
    
    def __init__(self):
        self.latex_service = ProfessionalLaTeXService()
        self.job_processor = JobApplicationProcessor()
        self.sms_service = TwilioNotificationService()
        
        logger.info("🤖 Automated JobHunter initialized")
    
    async def run_daily_automation(self):
        """Main daily automation routine - completely hands-off"""
        try:
            logger.info("🚀 Starting daily automation at 6:00 AM")
            
            # Import email scanner
            from app.services.real_email_scanner import RealEmailScanner
            email_scanner = RealEmailScanner()
            
            # Scan Gmail for new jobs
            logger.info("📧 Scanning Gmail for job opportunities...")
            jobs = await email_scanner.scan_real_gmail_jobs(days_back=1)
            
            logger.info(f"🔍 Found {len(jobs)} job opportunities")
            
            if not jobs:
                logger.info("📭 No new jobs found today")
                await self.sms_service.send_daily_scan_complete(0, 0)
                return
            
            # Process each job automatically
            successful_applications = 0
            
            for i, job in enumerate(jobs, 1):
                try:
                    logger.info(f"🎯 Processing job {i}/{len(jobs)}: {job['title']} at {job['company']}")
                    
                    # Generate customized documents
                    cv_pdf = await self.latex_service.generate_customized_cv(job)
                    cl_pdf = await self.latex_service.generate_customized_cover_letter(job)
                    
                    if cv_pdf and cl_pdf:
                        # Send application email
                        processed_job = {
                            'job': job,
                            'cv_pdf': cv_pdf,
                            'cover_letter_pdf': cl_pdf,
                            'status': 'success'
                        }
                        
                        email_sent = await self.job_processor.send_job_application_email(processed_job)
                        
                        if email_sent:
                            successful_applications += 1
                            logger.info(f"✅ Application sent: {job['company']}")
                            
                            # Send urgent alert for Volvo Energy
                            if 'volvo' in job['company'].lower() and 'energy' in job.get('description', '').lower():
                                await self.sms_service.send_volvo_energy_alert()
                        else:
                            logger.error(f"❌ Email failed: {job['company']}")
                    else:
                        logger.error(f"❌ Document generation failed: {job['company']}")
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {job.get('title', 'Unknown')}: {e}")
            
            # Send completion notification
            await self.sms_service.send_daily_scan_complete(len(jobs), successful_applications)
            
            logger.info(f"🎉 Daily automation completed: {successful_applications}/{len(jobs)} successful")
            
        except Exception as e:
            logger.error(f"❌ Daily automation error: {e}")
            await self.sms_service.send_system_error("daily_automation")
    
    async def run_hourly_check(self):
        """Hourly check for urgent jobs - completely automated"""
        try:
            logger.info("⏰ Running hourly urgent job check")
            
            # Import email scanner
            from app.services.real_email_scanner import RealEmailScanner
            email_scanner = RealEmailScanner()
            
            # Scan for very recent jobs (last hour)
            jobs = await email_scanner.scan_real_gmail_jobs(days_back=0.04)  # ~1 hour
            
            # Filter for urgent keywords
            urgent_keywords = ['volvo', 'energy', 'IT support', 'technical support', 'urgent', 'immediate']
            urgent_jobs = []
            
            for job in jobs:
                job_content = f"{job.get('title', '')} {job.get('description', '')} {job.get('company', '')}".lower()
                if any(keyword in job_content for keyword in urgent_keywords):
                    urgent_jobs.append(job)
            
            if urgent_jobs:
                logger.info(f"🚨 Found {len(urgent_jobs)} urgent jobs")
                
                for job in urgent_jobs:
                    # Process urgent job immediately
                    cv_pdf = await self.latex_service.generate_customized_cv(job)
                    cl_pdf = await self.latex_service.generate_customized_cover_letter(job)
                    
                    if cv_pdf and cl_pdf:
                        processed_job = {
                            'job': job,
                            'cv_pdf': cv_pdf,
                            'cover_letter_pdf': cl_pdf,
                            'status': 'urgent'
                        }
                        
                        await self.job_processor.send_job_application_email(processed_job)
                        await self.sms_service.send_urgent_job_alert(job['title'], job['company'])
                        
                        logger.info(f"🚨 Urgent job processed: {job['company']}")
            
        except Exception as e:
            logger.error(f"❌ Hourly check error: {e}")
    
    def start_automation(self):
        """Start the fully automated system"""
        logger.info("🤖 Starting fully automated JobHunter system")
        
        # Schedule daily automation at 6:00 AM Stockholm time
        schedule.every().day.at("06:00").do(lambda: asyncio.run(self.run_daily_automation()))
        
        # Schedule hourly urgent checks
        schedule.every().hour.do(lambda: asyncio.run(self.run_hourly_check()))
        
        # Schedule weekly summary (Sundays at 18:00)
        schedule.every().sunday.at("18:00").do(lambda: asyncio.run(self.send_weekly_summary()))
        
        logger.info("📅 Automation schedule configured:")
        logger.info("   • Daily scan: 06:00 Stockholm time")
        logger.info("   • Hourly urgent checks")
        logger.info("   • Weekly summary: Sunday 18:00")
        
        # Run the scheduler
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("🛑 Automation stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    async def send_weekly_summary(self):
        """Send weekly summary"""
        try:
            # This would typically query a database for weekly stats
            # For now, send a simple summary
            await self.sms_service.send_weekly_summary(35, 28)  # Example numbers
            logger.info("📊 Weekly summary sent")
        except Exception as e:
            logger.error(f"❌ Weekly summary error: {e}")

def main():
    """Main function to start automation"""
    print("🤖 JobHunter Fully Automated System")
    print("=" * 50)
    print("✅ Completely hands-off operation")
    print("📧 Automatic Gmail scanning")
    print("📄 AI-powered document generation")
    print("📱 SMS notifications")
    print("🔄 24/7 monitoring")
    print("=" * 50)
    
    # Initialize and start automation
    hunter = AutomatedJobHunter()
    
    # Test run (optional)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running test automation...")
        asyncio.run(hunter.run_daily_automation())
    else:
        print("🚀 Starting continuous automation...")
        hunter.start_automation()

if __name__ == "__main__":
    main()