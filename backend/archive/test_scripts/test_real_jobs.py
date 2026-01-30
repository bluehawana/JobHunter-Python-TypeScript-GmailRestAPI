#!/usr/bin/env python3
"""
Test script to check environment variables and test real job scraping
"""

import os
import asyncio
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment_variables():
    """Check what environment variables are set"""
    logger.info("🔍 Checking Environment Variables:")
    
    # Required variables
    required_vars = [
        'GMAIL_APP_PASSWORD', 'SENDER_EMAIL', 'SMTP_PASSWORD',
        'DATABASE_URL', 'SUPABASE_URL'
    ]
    
    # Optional variables
    optional_vars = [
        'GMAIL_CLIENT_ID', 'GMAIL_CLIENT_SECRET', 
        'LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET',
        'LINKEDIN_ACCESS_TOKEN'
    ]
    
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if value and value not in ['your_', 'your-']:  # Not placeholder
            logger.info(f"  ✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            logger.warning(f"  ❌ {var}: Not set or placeholder")
            missing_required.append(var)
    
    logger.info("\n📋 Optional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value and value not in ['your_', 'your-']:
            logger.info(f"  ✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            logger.info(f"  ⚠️  {var}: Not set")
    
    return missing_required

async def test_real_job_scraping():
    """Test the real job scraping functionality"""
    logger.info("\n🔧 Testing Real Job Scraping:")
    
    try:
        # Import scrapers
        from app.services.real_job_scrapers import (
            ArbetsformedlingenScraper, 
            IndeedJobScraper,
            CompanyCareerScraper
        )
        
        # Test Arbetsförmedlingen API (most likely to work)
        logger.info("Testing Arbetsförmedlingen API...")
        af_scraper = ArbetsformedlingenScraper()
        af_jobs = await af_scraper.scrape_arbetsformedlingen_jobs(max_jobs=3)
        logger.info(f"  Found {len(af_jobs)} Arbetsförmedlingen jobs")
        
        # Test Indeed scraping
        logger.info("Testing Indeed.se scraping...")
        indeed_scraper = IndeedJobScraper()
        indeed_jobs = await indeed_scraper.scrape_indeed_jobs(max_jobs=3)
        logger.info(f"  Found {len(indeed_jobs)} Indeed jobs")
        
        # Test Company Career scraping
        logger.info("Testing Company Career sites...")
        company_scraper = CompanyCareerScraper()
        company_jobs = await company_scraper.scrape_company_careers(max_jobs=3)
        logger.info(f"  Found {len(company_jobs)} Company career jobs")
        
        # Show sample jobs
        all_jobs = af_jobs + indeed_jobs + company_jobs
        if all_jobs:
            logger.info(f"\n📊 Sample Jobs Found:")
            for i, job in enumerate(all_jobs[:5], 1):
                logger.info(f"  {i}. {job['title']} at {job['company']}")
                logger.info(f"     Source: {job['source']} | Location: {job.get('location', 'N/A')}")
                if job.get('application_link'):
                    logger.info(f"     Apply: {job['application_link'][:60]}...")
        
        return len(all_jobs)
        
    except ImportError as e:
        logger.error(f"  ❌ Import error: {e}")
        return 0
    except Exception as e:
        logger.error(f"  ❌ Error testing job scraping: {e}")
        return 0

async def test_gmail_credentials():
    """Test Gmail credentials if available"""
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    gmail_user = os.getenv('GMAIL_USER', 'bluehawana@gmail.com')
    
    if not gmail_password or gmail_password.startswith('your'):
        logger.warning("  ❌ Gmail credentials not properly set")
        return False
    
    try:
        import imaplib
        logger.info("Testing Gmail connection...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")
        
        # Test a simple folder count
        status, messages = mail.search(None, 'ALL')
        if status == "OK":
            count = len(messages[0].split()) if messages[0] else 0
            logger.info(f"  ✅ Gmail connection successful! Found {count} emails in inbox")
            mail.close()
            mail.logout()
            return True
        else:
            logger.warning("  ❌ Gmail search failed")
            return False
            
    except Exception as e:
        logger.error(f"  ❌ Gmail test failed: {e}")
        return False

async def main():
    """Main test function"""
    logger.info("🚀 JobHunter System Test")
    logger.info("=" * 50)
    
    # Check environment variables
    missing_vars = check_environment_variables()
    
    # Test Gmail if credentials are available
    logger.info("\n📧 Testing Gmail Connection:")
    gmail_works = await test_gmail_credentials()
    
    # Test job scraping
    jobs_found = await test_real_job_scraping()
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📋 Test Summary:")
    logger.info(f"  Gmail Connection: {'✅ Working' if gmail_works else '❌ Not working'}")
    logger.info(f"  Jobs Found: {jobs_found}")
    logger.info(f"  Missing Required Vars: {len(missing_vars)}")
    
    if missing_vars:
        logger.info(f"  Missing: {', '.join(missing_vars)}")
        logger.info("\n💡 To fix missing variables:")
        logger.info("  1. Edit your .env file")
        logger.info("  2. Set the real values (not placeholders)")
        logger.info("  3. Restart the system")
    
    if jobs_found > 0:
        logger.info(f"\n🎉 Great! Found {jobs_found} real jobs from multiple sources!")
        logger.info("  The system should now send real job opportunities instead of mock data.")
    else:
        logger.warning("\n⚠️  No real jobs found - system will fall back to mock data")
        logger.info("  This is normal if scraping fails or sites block requests")
    
    # Instructions
    logger.info("\n🚀 Next Steps:")
    if gmail_works and jobs_found > 0:
        logger.info("  1. Your system is ready to send real job opportunities!")
        logger.info("  2. Run the enhanced job hunter:")
        logger.info("     cd /Users/bluehawana/Projects/Jobhunter/backend")
        logger.info("     source venv/bin/activate")
        logger.info("     python enhanced_job_hunter.py")
    else:
        logger.info("  1. Fix environment variables in .env file")
        logger.info("  2. Test Gmail connection")
        logger.info("  3. Re-run this test script")

if __name__ == "__main__":
    asyncio.run(main())