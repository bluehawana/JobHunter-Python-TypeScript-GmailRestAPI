#!/usr/bin/env python3
"""
Test single job application generation with customized CV and cover letter
"""

import asyncio
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

sys.path.append('.')
from app.services.enhanced_job_hunter_orchestrator import EnhancedJobHunterOrchestrator

async def test_and_send_application():
    """Test full workflow: job analysis → CV/CL generation → email sending"""
    
    # Sample job from the previous results
    sample_job = {
        'title': 'Senior Backend Developer',
        'company': 'Volvo Cars',
        'location': 'Stockholm, Sweden', 
        'description': '''We are seeking a Senior Backend Developer to join our Connected Services team. 
        You will be responsible for developing and maintaining scalable backend systems that power our connected car services.
        
        Key Requirements:
        - 5+ years of experience with Java and Spring Boot
        - Strong knowledge of microservices architecture
        - Experience with AWS cloud services (EC2, S3, RDS, Lambda)
        - Proficiency in PostgreSQL and Redis
        - Experience with Docker and Kubernetes
        - Knowledge of CI/CD pipelines and DevOps practices
        
        What you'll do:
        - Design and implement RESTful APIs
        - Develop microservices for vehicle data processing
        - Collaborate with frontend teams and product managers
        - Ensure high availability and performance of backend systems
        - Participate in code reviews and technical discussions
        ''',
        'application_link': 'https://careers.volvocars.com/job/backend-developer-stockholm',
        'keywords': ['java', 'spring boot', 'aws', 'microservices', 'postgresql'],
        'quality_score': 92
    }
    
    print("🎯 Testing Complete Job Application Workflow")
    print("=" * 60)
    print(f"Job: {sample_job['title']} at {sample_job['company']}")
    print(f"Location: {sample_job['location']}")
    print(f"Quality Score: {sample_job['quality_score']}/100")
    print()
    
    # Initialize orchestrator
    orchestrator = EnhancedJobHunterOrchestrator()
    
    print("📊 Step 1: Generating customized application documents...")
    result = await orchestrator.generate_application_documents(sample_job)
    
    if 'error' in result:
        print(f"❌ Error generating documents: {result['error']}")
        return False
    
    print("✅ Documents generated successfully!")
    
    # Extract results
    job_info = result.get('job_info', {})
    cv_content = result.get('cv', '')
    cl_content = result.get('cover_letter', '')
    
    print(f"📄 CV content length: {len(cv_content)} characters")
    print(f"📄 Cover Letter content length: {len(cl_content)} characters")
    
    if len(cv_content) < 100 or len(cl_content) < 100:
        print("⚠️  Warning: Generated content seems too short")
    
    print("\n📧 Step 2: Sending application email...")
    
    # Create and send email
    success = await send_application_email(sample_job, cv_content, cl_content)
    
    if success:
        print("✅ Application email sent successfully!")
        print(f"📬 Check hongzhili01@gmail.com for your customized application")
        return True
    else:
        print("❌ Failed to send application email")
        return False

async def send_application_email(job, cv_content, cl_content):
    """Send application email with customized documents"""
    try:
        # Email configuration
        smtp_user = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        to_email = "hongzhili01@gmail.com"
        
        if not smtp_password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"🎯 CUSTOMIZED APPLICATION: {job['title']} at {job['company']}"
        
        # Email body
        email_body = f"""
🎯 CUSTOMIZED JOB APPLICATION READY
============================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your AI-powered JobHunter system has generated a highly customized application for:

🏢 COMPANY: {job['company']}
💼 POSITION: {job['title']}
📍 LOCATION: {job['location']}
⭐ QUALITY SCORE: {job['quality_score']}/100
🔗 APPLICATION LINK: {job['application_link']}

📄 GENERATED DOCUMENTS:
✅ Customized CV tailored to job requirements
✅ Personalized Cover Letter with company research
✅ Both documents optimized for ATS systems

📝 CUSTOMIZED CV PREVIEW:
{cv_content[:500]}...

📝 CUSTOMIZED COVER LETTER PREVIEW:
{cl_content[:500]}...

🚀 NEXT STEPS:
1. Review the generated documents above
2. If satisfied, visit the application link to apply
3. Copy and paste the content into application forms
4. The system will continue monitoring for more opportunities

💡 These documents were specifically tailored using Claude AI analysis of the job requirements and optimized for high ATS compatibility.

🤖 Enhanced JobHunter System - AI-Powered Job Applications
Generated with advanced CV/CL customization
"""
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Set environment variables
    os.environ['GMAIL_APP_PASSWORD'] = 'vsodrpyblpgtujof'
    os.environ['SENDER_EMAIL'] = 'leeharvad@gmail.com'  
    os.environ['SMTP_PASSWORD'] = 'vsdclxhjnklrccsf'
    
    success = asyncio.run(test_and_send_application())
    sys.exit(0 if success else 1)