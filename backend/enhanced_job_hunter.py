#!/usr/bin/env python3
"""
Enhanced Job Hunter - Complete job scanning and application system
Supports multiple job sources: LinkedIn, Indeed, Arbetsförmedlingen, Company Career Sites, Gmail
Filters for developer positions with 5+ years experience
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.enhanced_job_hunter_orchestrator import EnhancedJobHunterOrchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_job_hunter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """
    Main function to run the enhanced job hunting system
    """
    try:
        logger.info("🚀 Starting Enhanced Job Hunter System")
        logger.info("=" * 60)
        
        # Initialize the orchestrator
        job_hunter = EnhancedJobHunterOrchestrator()
        
        # Run comprehensive job hunt
        logger.info("📊 Phase 1: Comprehensive Job Scanning")
        hunt_results = await job_hunter.hunt_jobs_comprehensive(max_jobs_per_source=20)
        
        # Display summary
        summary = hunt_results.get('summary', {})
        logger.info(f"✅ Job Hunt Complete!")
        logger.info(f"   Total Sources: {summary.get('total_sources', 0)}")
        logger.info(f"   Raw Jobs Found: {summary.get('total_raw_jobs', 0)}")
        logger.info(f"   Filtered Jobs: {summary.get('filtered_jobs', 0)}")
        logger.info(f"   Final Unique Jobs: {summary.get('final_unique_jobs', 0)}")
        logger.info(f"   Avg Experience Level: {summary.get('avg_experience_level', 'N/A')}")
        
        # Display top companies
        top_companies = summary.get('top_companies', [])[:5]
        if top_companies:
            logger.info("\n🏢 Top Companies:")
            for company in top_companies:
                logger.info(f"   • {company['company']}: {company['count']} jobs")
        
        # Display top tech keywords
        top_keywords = summary.get('top_keywords', [])[:10]
        if top_keywords:
            logger.info("\n🔧 Top Technologies:")
            tech_list = [f"{kw['keyword']} ({kw['count']})" for kw in top_keywords]
            logger.info(f"   {', '.join(tech_list)}")
        
        # Save results
        results_file = job_hunter.save_hunt_results(hunt_results)
        logger.info(f"\n💾 Results saved to: {results_file}")
        
        # Process top jobs with documents
        logger.info("\n📊 Phase 2: Document Generation for Top Jobs")
        top_jobs_with_docs = await job_hunter.process_top_jobs_with_documents(
            hunt_results, top_n=5
        )
        
        logger.info(f"✅ Generated documents for {len(top_jobs_with_docs)} top jobs")
        
        # Display top job opportunities
        logger.info("\n🎯 Top Job Opportunities:")
        logger.info("=" * 60)
        
        filtered_jobs = hunt_results.get('filtered_jobs', [])[:10]
        for i, job in enumerate(filtered_jobs, 1):
            quality_score = job.get('quality_score', 0)
            keywords = ', '.join(job.get('keywords', [])[:5])
            
            logger.info(f"\n{i}. {job['title']} at {job['company']}")
            logger.info(f"   📍 Location: {job.get('location', 'N/A')}")
            logger.info(f"   💼 Experience: {job.get('experience_level', 'N/A')}")
            logger.info(f"   🔗 Source: {job.get('source', 'N/A')}")
            logger.info(f"   ⭐ Quality Score: {quality_score}/100")
            logger.info(f"   🏷️ Tech: {keywords}")
            
            if job.get('salary'):
                logger.info(f"   💰 Salary: {job['salary']}")
            
            if job.get('application_link'):
                logger.info(f"   🔗 Apply: {job['application_link']}")
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Enhanced Job Hunt Complete!")
        logger.info("📧 Check your email for job notifications with customized CVs and cover letters.")
        logger.info(f"📁 Detailed results available in: {results_file}")
        
        # Instructions for next steps
        logger.info("\n🚀 Next Steps:")
        logger.info("1. Review the top job opportunities above")
        logger.info("2. Check generated CVs and cover letters in the results")
        logger.info("3. Apply to positions using the provided links")
        logger.info("4. Monitor your email for new job alerts")
        
    except Exception as e:
        logger.error(f"❌ Error in Enhanced Job Hunter: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ['GMAIL_APP_PASSWORD', 'SENDER_EMAIL', 'SMTP_PASSWORD']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these in your .env file or environment")
        sys.exit(1)
    
    # Run the enhanced job hunter
    asyncio.run(main())