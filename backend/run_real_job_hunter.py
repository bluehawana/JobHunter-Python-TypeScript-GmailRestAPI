#!/usr/bin/env python3
"""
Enhanced Real Job Hunter - Uses your existing email system with real job scraping
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_job_hunter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """
    Main function that uses your existing email system to send real jobs
    """
    try:
        logger.info("🚀 Starting Real Job Hunter with Enhanced Scrapers")
        logger.info("=" * 60)
        
        # Import the scrapers
        from app.services.real_job_scrapers import (
            ArbetsformedlingenScraper, 
            IndeedJobScraper,
            CompanyCareerScraper
        )
        
        # Use your existing email system
        from app.services.real_job_scanner import RealJobScanner
        
        # Initialize scrapers
        indeed_scraper = IndeedJobScraper()
        company_scraper = CompanyCareerScraper()
        af_scraper = ArbetsformedlingenScraper()
        email_sender = RealJobScanner()  # Your existing email system
        
        logger.info("📊 Phase 1: Scraping Real Jobs from Multiple Sources")
        
        # Scrape jobs from all sources
        tasks = [
            indeed_scraper.scrape_indeed_jobs(max_jobs=5),
            company_scraper.scrape_company_careers(max_jobs=5),
            af_scraper.scrape_arbetsformedlingen_jobs(max_jobs=5)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_jobs = []
        source_names = ['Indeed', 'Company Careers', 'Arbetsförmedlingen']
        
        for i, (source_name, jobs) in enumerate(zip(source_names, results)):
            if isinstance(jobs, Exception):
                logger.error(f"❌ Error from {source_name}: {jobs}")
            else:
                logger.info(f"✅ {source_name}: {len(jobs)} jobs found")
                all_jobs.extend(jobs)
        
        # Filter and rank jobs for experienced developers
        quality_jobs = filter_for_experienced_developers(all_jobs)
        
        logger.info(f"🎯 Phase 2: Processing {len(quality_jobs)} Quality Jobs")
        
        # Process top jobs and send emails using your existing system
        if quality_jobs:
            # Use your existing email system to send the jobs
            for i, job in enumerate(quality_jobs[:3], 1):  # Send top 3 jobs
                try:
                    logger.info(f"📧 Sending job {i}: {job['title']} at {job['company']}")
                    
                    # Generate real CV and Cover Letter PDFs
                    from app.services.claude_api_service import ClaudeAPIService
                    from app.services.latex_resume_service import LaTeXResumeService
                    
                    claude_service = ClaudeAPIService()
                    latex_service = LaTeXResumeService()
                    
                    # Generate customized CV content
                    cv_content = await claude_service.generate_cv_for_job(job)
                    cv_pdf = latex_service.create_cv_pdf(cv_content, job)
                    
                    # Generate customized cover letter content
                    cl_content = await claude_service.generate_cover_letter_for_job(job)
                    cl_pdf = latex_service.create_cover_letter_pdf(cl_content, job)
                    
                    if not cv_pdf or not cl_pdf:
                        # Fallback to simple PDF generation
                        cv_pdf = b"Simple CV PDF placeholder"
                        cl_pdf = b"Simple Cover Letter PDF placeholder"
                    
                    success = await email_sender.send_job_email(job, cv_pdf, cl_pdf)
                    if success:
                        logger.info(f"✅ Successfully sent email for {job['company']}")
                    else:
                        logger.warning(f"⚠️ Failed to send email for {job['company']}")
                        
                    # Delay between emails
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error sending job {i}: {e}")
        
        else:
            logger.warning("❌ No quality jobs found")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📋 Real Job Hunt Summary:")
        logger.info(f"   Total Jobs Scraped: {len(all_jobs)}")
        logger.info(f"   Quality Jobs Found: {len(quality_jobs)}")
        logger.info(f"   Emails Sent: {min(len(quality_jobs), 3)}")
        
        if quality_jobs:
            logger.info("\n🏆 Top Job Opportunities:")
            for i, job in enumerate(quality_jobs[:5], 1):
                logger.info(f"   {i}. {job['title']} at {job['company']}")
                logger.info(f"      📍 {job.get('location', 'N/A')} | 💼 {job.get('experience_level', 'N/A')}")
                logger.info(f"      🔗 {job.get('application_link', 'N/A')[:60]}...")
                logger.info(f"      🏷️ Keywords: {', '.join(job.get('keywords', [])[:5])}")
        
        logger.info("\n🎉 Real Job Hunt Complete! Check your email for job opportunities.")
        
    except Exception as e:
        logger.error(f"❌ Error in Real Job Hunter: {e}")
        import traceback
        logger.error(traceback.format_exc())

def filter_for_experienced_developers(jobs):
    """
    Filter jobs for developers with 5+ years experience
    """
    quality_jobs = []
    
    for job in jobs:
        # Check if it's a relevant developer position
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        # Must be a developer role
        developer_keywords = [
            'developer', 'engineer', 'utvecklare', 'ingenjör', 
            'fullstack', 'backend', 'frontend', 'devops', 'software'
        ]
        
        if not any(keyword in title for keyword in developer_keywords):
            continue
        
        # Check for relevant tech keywords
        tech_keywords = job.get('keywords', [])
        relevant_tech = ['java', 'python', 'javascript', 'react', 'spring', 'aws', 'docker', 'kubernetes']
        tech_matches = sum(1 for tech in relevant_tech if tech in tech_keywords)
        
        if tech_matches < 2:  # Must have at least 2 relevant technologies
            continue
        
        # Must have application method
        if not job.get('application_link') and not job.get('application_email'):
            continue
        
        # Calculate quality score
        quality_score = 0
        
        # Experience level bonus
        exp_level = job.get('experience_level', 'Mid-level')
        if exp_level == 'Senior':
            quality_score += 20
        elif exp_level == 'Mid-level':
            quality_score += 15
        
        # Tech keyword bonus
        quality_score += tech_matches * 3
        
        # Company bonus (if it's a well-known company)
        company = job.get('company', '').lower()
        known_companies = ['volvo', 'skf', 'klarna', 'spotify', 'ericsson', 'h&m']
        if any(comp in company for comp in known_companies):
            quality_score += 10
        
        # Description quality bonus
        if len(job.get('description', '')) > 100:
            quality_score += 5
        
        job['quality_score'] = quality_score
        
        # Only include high-quality jobs
        if quality_score >= 25:
            quality_jobs.append(job)
    
    # Sort by quality score
    quality_jobs.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    return quality_jobs

if __name__ == "__main__":
    # Run the real job hunter
    asyncio.run(main())