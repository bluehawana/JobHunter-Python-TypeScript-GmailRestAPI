#!/usr/bin/env python3
"""
Test script for job application processor
Tests the complete workflow: job extraction -> document generation -> email sending
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

# Set environment variables for testing - check for required credentials
# Required environment variables (must be set by user)
required_vars = ['SMTP_USER', 'SMTP_PASSWORD']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set the following environment variables:")
    for var in missing_vars:
        if var == 'SMTP_USER':
            print(f"  export {var}='your-email@gmail.com'")
        elif var == 'SMTP_PASSWORD':
            print(f"  export {var}='your-app-password'")
    sys.exit(1)

# Set defaults for non-sensitive configuration
os.environ.setdefault('SMTP_HOST', 'smtp.gmail.com')
os.environ.setdefault('SMTP_PORT', '587')
os.environ.setdefault('EMAILS_FROM_EMAIL', os.getenv('SMTP_USER', ''))
os.environ.setdefault('EMAILS_FROM_NAME', 'JobHunter Bot')

from app.services.job_application_processor import JobApplicationProcessor
from app.services.simple_latex_service import SimpleLaTeXService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_job_application_processor():
    """Test the complete job application processing workflow"""
    try:
        logger.info("=== Testing Job Application Processor ===")
        
        # Initialize the processor with mock LaTeX service
        processor = JobApplicationProcessor()
        processor.latex_service = SimpleLaTeXService()
        
        # Test with sample jobs (representing the URLs you provided)
        logger.info("Processing sample jobs from your Gmail and LinkedIn...")
        results = await processor.process_sample_jobs()
        
        # Display results
        logger.info(f"\n=== PROCESSING RESULTS ===")
        logger.info(f"Total jobs processed: {len(results)}")
        
        for i, result in enumerate(results, 1):
            job = result.get('job', {})
            status = result.get('status', 'unknown')
            email_sent = result.get('email_sent', False)
            
            logger.info(f"\nJob {i}:")
            logger.info(f"  Title: {job.get('title', 'N/A')}")
            logger.info(f"  Company: {job.get('company', 'N/A')}")
            logger.info(f"  Location: {job.get('location', 'N/A')}")
            logger.info(f"  Source: {job.get('source', 'N/A')}")
            logger.info(f"  URL: {job.get('url', 'N/A')}")
            logger.info(f"  Keywords: {', '.join(job.get('keywords', []))}")
            logger.info(f"  Processing Status: {status}")
            logger.info(f"  Email Sent: {'✅ Success' if email_sent else '❌ Failed'}")
            
            if status == 'success':
                cv_size = len(result.get('cv_pdf', b''))
                cl_size = len(result.get('cover_letter_pdf', b''))
                logger.info(f"  CV PDF Size: {cv_size} bytes")
                logger.info(f"  Cover Letter PDF Size: {cl_size} bytes")
            
            if result.get('error'):
                logger.error(f"  Error: {result['error']}")
        
        # Summary
        successful_jobs = sum(1 for r in results if r.get('status') == 'success')
        emails_sent = sum(1 for r in results if r.get('email_sent'))
        
        logger.info(f"\n=== SUMMARY ===")
        logger.info(f"✅ Successfully processed: {successful_jobs}/{len(results)} jobs")
        logger.info(f"📧 Emails sent: {emails_sent}/{len(results)} jobs")
        logger.info(f"📩 Check leeharvad@gmail.com for the application emails!")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in job application processor test: {e}")
        import traceback
        traceback.print_exc()
        return []

async def test_single_job():
    """Test processing a single job with custom data"""
    try:
        logger.info("=== Testing Single Job Processing ===")
        
        processor = JobApplicationProcessor()
        processor.latex_service = SimpleLaTeXService()
        
        # Create a test job based on typical requirements
        test_job = {
            'id': 'test_job_1',
            'title': 'Senior Fullstack Developer',
            'company': 'TechCorp Sweden',
            'location': 'Gothenburg, Sweden',
            'description': '''We are seeking a Senior Fullstack Developer to join our innovative team.
            
            Key Requirements:
            • 5+ years experience with Java and Spring Boot
            • Strong knowledge of React and modern frontend technologies  
            • Experience with AWS cloud services and microservices architecture
            • Proficiency in PostgreSQL and database design
            • Knowledge of Docker, Kubernetes, and DevOps practices
            • Experience with Agile/Scrum methodologies
            
            Responsibilities:
            • Design and develop scalable web applications
            • Build and maintain RESTful APIs and microservices
            • Collaborate with cross-functional teams
            • Implement automated testing and CI/CD pipelines
            • Mentor junior developers
            
            We offer competitive salary, flexible work arrangements, and excellent benefits.''',
            'url': 'https://example.com/job/senior-fullstack-developer',
            'source': 'test',
            'keywords': ['java', 'spring boot', 'react', 'aws', 'microservices', 'postgresql', 'docker', 'kubernetes', 'restful api'],
            'job_type': 'fulltime',
            'remote_option': True,
            'posting_date': datetime.now(),
            'confidence_score': 0.9
        }
        
        # Process the job
        result = await processor.process_job_and_generate_documents(test_job)
        
        # Send email
        email_sent = await processor.send_job_application_email(result)
        result['email_sent'] = email_sent
        
        # Display result
        logger.info(f"Job processed: {result.get('status')}")
        logger.info(f"Email sent: {'✅ Success' if email_sent else '❌ Failed'}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in single job test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Choose which test to run
    if len(sys.argv) > 1 and sys.argv[1] == "single":
        asyncio.run(test_single_job())
    else:
        asyncio.run(test_job_application_processor())