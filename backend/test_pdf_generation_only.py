#!/usr/bin/env python3
"""
Test script for PDF generation only (no email sending)
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

from app.services.simple_latex_service import SimpleLaTeXService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_pdf_generation():
    """Test PDF generation for the specific jobs mentioned"""
    try:
        logger.info("=== Testing PDF Generation ===")
        
        # Initialize LaTeX service
        latex_service = SimpleLaTeXService()
        
        # Sample jobs based on your URLs
        test_jobs = [
            {
                'id': 'linkedin_job',
                'title': 'Senior Fullstack Developer',
                'company': 'TechCorp Sweden',
                'location': 'Gothenburg, Sweden',
                'description': '''We are looking for a Senior Fullstack Developer to join our innovative team.

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

We offer competitive salary, flexible work arrangements, and excellent benefits.''',
                'url': 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4266325638',
                'source': 'linkedin',
                'keywords': ['java', 'spring boot', 'react', 'aws', 'microservices', 'postgresql', 'docker', 'kubernetes', 'restful api'],
                'job_type': 'fulltime',
                'remote_option': True,
                'posting_date': datetime.now(),
                'confidence_score': 0.9
            },
            {
                'id': 'gmail_linkedin_job',
                'title': 'Backend Developer',
                'company': 'Growing Startup',
                'location': 'Stockholm, Sweden',
                'description': '''Join our growing startup as a Backend Developer!

What you'll do:
• Build scalable backend services using Java and Spring Boot
• Design and implement cloud-native solutions on AWS
• Work with microservices architecture and API development
• Optimize database performance with PostgreSQL
• Implement DevOps practices and CI/CD pipelines

What we're looking for:
• 3+ years of Java development experience
• Strong experience with Spring Framework
• Cloud experience (AWS preferred)
• Knowledge of containerization (Docker/Kubernetes)

Great benefits and competitive salary package!''',
                'url': 'https://mail.google.com/mail/u/0/#search/linkedin+jobs/FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx',
                'source': 'gmail_linkedin',
                'keywords': ['java', 'spring boot', 'aws', 'microservices', 'postgresql', 'docker', 'kubernetes'],
                'job_type': 'fulltime',
                'remote_option': False,
                'posting_date': datetime.now(),
                'confidence_score': 0.9
            }
        ]
        
        results = []
        
        for i, job in enumerate(test_jobs, 1):
            logger.info(f"\n--- Processing Job {i}: {job['title']} at {job['company']} ---")
            
            try:
                # Generate CV
                logger.info("Generating customized CV...")
                cv_pdf = await latex_service.generate_customized_cv(job)
                cv_size = len(cv_pdf)
                logger.info(f"CV generated: {cv_size} bytes")
                
                # Generate cover letter
                logger.info("Generating customized cover letter...")
                cl_pdf = await latex_service.generate_customized_cover_letter(job)
                cl_size = len(cl_pdf)
                logger.info(f"Cover letter generated: {cl_size} bytes")
                
                # Save PDFs for inspection
                cv_filename = f"cv_{job['company'].replace(' ', '_')}_{job['title'].replace(' ', '_')}.pdf"
                cl_filename = f"cover_letter_{job['company'].replace(' ', '_')}_{job['title'].replace(' ', '_')}.pdf"
                
                with open(cv_filename, 'wb') as f:
                    f.write(cv_pdf)
                with open(cl_filename, 'wb') as f:
                    f.write(cl_pdf)
                
                logger.info(f"PDFs saved: {cv_filename}, {cl_filename}")
                
                result = {
                    'job': job,
                    'cv_pdf': cv_pdf,
                    'cv_size': cv_size,
                    'cover_letter_pdf': cl_pdf,
                    'cl_size': cl_size,
                    'cv_filename': cv_filename,
                    'cl_filename': cl_filename,
                    'status': 'success'
                }
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing job {i}: {e}")
                results.append({
                    'job': job,
                    'status': 'error',
                    'error': str(e)
                })
        
        # Summary
        logger.info(f"\n=== SUMMARY ===")
        successful = sum(1 for r in results if r.get('status') == 'success')
        logger.info(f"✅ Successfully processed: {successful}/{len(results)} jobs")
        
        if successful > 0:
            logger.info("📁 Generated files:")
            for result in results:
                if result.get('status') == 'success':
                    logger.info(f"   • {result['cv_filename']} ({result['cv_size']} bytes)")
                    logger.info(f"   • {result['cl_filename']} ({result['cl_size']} bytes)")
        
        # Show job details summary
        logger.info(f"\n=== JOB DETAILS PROCESSED ===")
        for i, result in enumerate(results, 1):
            job = result['job']
            logger.info(f"\nJob {i}:")
            logger.info(f"  📋 Title: {job['title']}")
            logger.info(f"  🏢 Company: {job['company']}")
            logger.info(f"  📍 Location: {job['location']}")
            logger.info(f"  🔗 URL: {job['url']}")
            logger.info(f"  🏷️ Keywords: {', '.join(job['keywords'])}")
            logger.info(f"  💼 Type: {job['job_type']}")
            logger.info(f"  🏠 Remote: {'Yes' if job['remote_option'] else 'No'}")
            logger.info(f"  ✅ Status: {result.get('status', 'unknown')}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in PDF generation test: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    asyncio.run(test_pdf_generation())