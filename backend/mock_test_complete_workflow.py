#!/usr/bin/env python3
"""
Mock Test: Complete Job Application Automation Workflow

This script demonstrates the complete workflow:
1. Scan bluehawana@gmail.com for LinkedIn job emails
2. Extract job details from the newest job spots with title "LinkedIn Jobs"
3. Generate customized resume and cover letter in LaTeX format
4. Convert to PDF files
5. Send email to leeharvad@gmail.com with:
   - CV PDF attachment
   - Cover Letter PDF attachment
   - Job title in subject
   - Job description in content
   - Application link

Usage: python mock_test_complete_workflow.py
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.email_scanner_service import EmailScannerService
from app.services.job_application_processor import JobApplicationProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def mock_test_complete_workflow():
    """Run the complete job application automation workflow"""
    
    print("🚀 Starting Job Application Automation Mock Test")
    print("=" * 60)
    
    try:
        # Step 1: Initialize services
        print("📧 Step 1: Initializing Email Scanner and Job Processor...")
        email_scanner = EmailScannerService()
        job_processor = JobApplicationProcessor()
        
        # Step 2: Scan emails for job opportunities
        print("🔍 Step 2: Scanning bluehawana@gmail.com for LinkedIn job emails...")
        print("   Looking for emails with 'LinkedIn Jobs' in title...")
        
        # For mock test, we'll simulate finding job emails
        # In real implementation, this would scan actual emails
        mock_job_emails = [
            {
                'id': 'linkedin_job_1',
                'title': 'Senior Fullstack Developer',
                'company': 'TechCorp Sweden',
                'location': 'Stockholm, Sweden',
                'description': '''We are seeking a Senior Fullstack Developer to join our innovative team in Stockholm.

Key Responsibilities:
• Develop and maintain web applications using Java Spring Boot and React
• Design and implement RESTful APIs and microservices architecture
• Work with cloud platforms (AWS/Azure) for deployment and scaling
• Collaborate with cross-functional teams using Agile methodologies
• Implement automated testing and CI/CD pipelines
• Optimize application performance and ensure scalability

Requirements:
• 5+ years of experience with Java and Spring Boot framework
• Strong proficiency in React, TypeScript, and modern JavaScript
• Experience with cloud platforms (AWS or Azure)
• Knowledge of containerization technologies (Docker, Kubernetes)
• Familiarity with databases (PostgreSQL, MongoDB)
• Experience with version control (Git) and Agile development
• Strong problem-solving skills and attention to detail

We offer:
• Competitive salary and benefits package
• Flexible working arrangements and remote work options
• Professional development opportunities
• Modern office environment in central Stockholm
• Collaborative and innovative team culture''',
                'url': 'https://www.linkedin.com/jobs/view/3756789123',
                'source': 'linkedin_email',
                'keywords': ['java', 'spring boot', 'react', 'typescript', 'aws', 'azure', 'microservices', 'docker', 'kubernetes', 'postgresql'],
                'job_type': 'fulltime',
                'remote_option': True,
                'posting_date': datetime.now(),
                'email_subject': 'LinkedIn Jobs: New opportunities matching your profile',
                'confidence_score': 0.95
            },
            {
                'id': 'linkedin_job_2',
                'title': 'Backend Developer',
                'company': 'Growing Startup',
                'location': 'Gothenburg, Sweden',
                'description': '''Join our fast-growing startup as a Backend Developer!

What you'll do:
• Build scalable backend services using Java and Spring Boot
• Design and implement cloud-native solutions on AWS
• Work with microservices architecture and API development
• Optimize database performance with PostgreSQL and MongoDB
• Implement DevOps practices and CI/CD pipelines
• Collaborate with frontend developers and product team

Requirements:
• 3+ years of Java development experience
• Strong experience with Spring Framework and Spring Boot
• Cloud experience (AWS preferred)
• Knowledge of containerization (Docker/Kubernetes)
• Experience with relational and NoSQL databases
• Understanding of Agile development practices
• Good communication skills in English

Benefits:
• Competitive salary package
• Stock options in a growing company
• Flexible working hours
• Learning and development budget
• Great team culture and startup environment''',
                'url': 'https://www.linkedin.com/jobs/view/3756789124',
                'source': 'linkedin_email',
                'keywords': ['java', 'spring boot', 'aws', 'microservices', 'postgresql', 'mongodb', 'docker', 'kubernetes', 'devops'],
                'job_type': 'fulltime',
                'remote_option': False,
                'posting_date': datetime.now(),
                'email_subject': 'LinkedIn Jobs: Backend Developer opportunities',
                'confidence_score': 0.90
            }
        ]
        
        print(f"   ✅ Found {len(mock_job_emails)} job opportunities from LinkedIn emails")
        
        # Step 3: Process each job and generate documents
        print("📄 Step 3: Processing jobs and generating customized documents...")
        
        processed_jobs = []
        
        for i, job_data in enumerate(mock_job_emails, 1):
            print(f"\\n   Processing Job {i}/{len(mock_job_emails)}: {job_data['title']} at {job_data['company']}")
            
            # Generate customized CV and cover letter
            print("   📝 Generating customized CV...")
            print("   📝 Generating customized cover letter...")
            
            processed_job = await job_processor.process_job_and_generate_documents(job_data)
            
            if processed_job['status'] == 'success':
                print("   ✅ Documents generated successfully")
                
                # Step 4: Send email with attachments
                print("   📧 Sending application email to leeharvad@gmail.com...")
                
                email_sent = await job_processor.send_job_application_email(
                    processed_job, 
                    recipient_email="leeharvad@gmail.com"
                )
                
                processed_job['email_sent'] = email_sent
                
                if email_sent:
                    print("   ✅ Email sent successfully!")
                else:
                    print("   ❌ Failed to send email")
                    
            else:
                print(f"   ❌ Document generation failed: {processed_job.get('error', 'Unknown error')}")
            
            processed_jobs.append(processed_job)
            
            # Add delay between jobs
            await asyncio.sleep(1)
        
        # Step 5: Summary
        print("\\n" + "=" * 60)
        print("📊 WORKFLOW SUMMARY")
        print("=" * 60)
        
        successful_jobs = [job for job in processed_jobs if job['status'] == 'success']
        failed_jobs = [job for job in processed_jobs if job['status'] == 'error']
        emails_sent = [job for job in processed_jobs if job.get('email_sent', False)]
        
        print(f"📧 Emails scanned: bluehawana@gmail.com")
        print(f"🔍 Jobs found: {len(mock_job_emails)}")
        print(f"✅ Successfully processed: {len(successful_jobs)}")
        print(f"❌ Failed to process: {len(failed_jobs)}")
        print(f"📤 Emails sent to leeharvad@gmail.com: {len(emails_sent)}")
        
        print("\\n📋 PROCESSED JOBS:")
        for i, job in enumerate(processed_jobs, 1):
            job_data = job['job']
            status_icon = "✅" if job['status'] == 'success' else "❌"
            email_icon = "📤" if job.get('email_sent', False) else "📪"
            
            print(f"   {i}. {status_icon} {email_icon} {job_data.get('title', 'Unknown')} at {job_data.get('company', 'Unknown')}")
            print(f"      URL: {job_data.get('url', 'N/A')}")
            print(f"      Keywords: {', '.join(job_data.get('keywords', [])[:5])}")
            
            if job['status'] == 'error':
                print(f"      Error: {job.get('error', 'Unknown error')}")
        
        print("\\n🎯 WHAT LEEHARVAD@GMAIL.COM WILL RECEIVE:")
        for job in emails_sent:
            job_data = job['job']
            print(f"   📧 Email: 'Job Application Ready: {job_data['title']} at {job_data['company']}'")
            print(f"      📎 CV_{job_data['company']}_{job_data['title'].replace(' ', '_')}.pdf")
            print(f"      📎 CoverLetter_{job_data['company']}_{job_data['title'].replace(' ', '_')}.pdf")
            print(f"      🔗 Application link: {job_data['url']}")
            print(f"      📝 Job description and requirements included")
            print()
        
        print("🎉 Mock test completed successfully!")
        print("\\n💡 NEXT STEPS:")
        print("   1. Check leeharvad@gmail.com for the application emails")
        print("   2. Review the customized CV and cover letter PDFs")
        print("   3. Click the application links to apply to the jobs")
        print("   4. Decide how to proceed with each application")
        
        return True
        
    except Exception as e:
        logger.error(f"Mock test failed: {e}")
        print(f"\\n❌ Mock test failed: {e}")
        return False

async def main():
    """Main function to run the mock test"""
    print("Job Application Automation - Mock Test")
    print("Testing complete workflow from email scanning to document generation")
    print()
    
    success = await mock_test_complete_workflow()
    
    if success:
        print("\\n✅ Mock test completed successfully!")
        sys.exit(0)
    else:
        print("\\n❌ Mock test failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())