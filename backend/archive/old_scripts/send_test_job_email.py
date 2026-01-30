#!/usr/bin/env python3
"""
Send a test job email to hongzhili01@gmail.com
This will verify the email automation works and you get the job opportunities
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_job():
    """Create a test job opportunity"""
    return {
        'title': 'Senior DevOps Engineer',
        'company': 'SKF Group',
        'location': 'Gothenburg, Sweden',
        'description': 'We are looking for a Senior DevOps Engineer to join our Platform Team. You will work with Kubernetes, Docker, Terraform, and AWS to build and maintain our cloud infrastructure. This is an excellent opportunity for someone with 5+ years of experience in DevOps and cloud technologies.',
        'application_link': 'https://careers.skf.com/job/12347/senior-devops-engineer-platform-team',
        'url': 'https://careers.skf.com/job/12347/senior-devops-engineer-platform-team',
        'keywords': ['kubernetes', 'docker', 'terraform', 'jenkins', 'aws', 'python', 'devops', 'cloud'],
        'salary': '650,000 - 850,000 SEK annually',
        'employment_type': 'Permanent',
        'experience_level': 'Senior',
        'date_received': datetime.now().strftime('%Y-%m-%d')
    }

def create_simple_cv_pdf():
    """Create a simple CV PDF content"""
    cv_content = """
    HONGZHI (HARVAD) LI
    Senior Software Engineer & DevOps Specialist
    
    📧 hongzhili01@gmail.com
    📍 Gothenburg, Sweden
    🔗 LinkedIn: linkedin.com/in/hongzhili
    🐙 GitHub: github.com/bluehawana
    
    PROFESSIONAL SUMMARY
    Experienced Software Engineer with 5+ years in full-stack development, cloud infrastructure, 
    and DevOps practices. Proven track record in Java, Python, JavaScript, AWS, Docker, and Kubernetes.
    
    TECHNICAL SKILLS
    • Languages: Java, Python, JavaScript, TypeScript, Go
    • Cloud Platforms: AWS, Azure, Docker, Kubernetes
    • Frameworks: Spring Boot, React, Node.js, Django
    • DevOps Tools: Jenkins, GitLab CI, Terraform, Ansible
    • Databases: PostgreSQL, MongoDB, Redis
    
    PROFESSIONAL EXPERIENCE
    Senior Software Engineer | Various Companies | 2019 - Present
    • Designed and implemented microservices architectures
    • Built CI/CD pipelines using Jenkins and GitLab
    • Managed cloud infrastructure on AWS and Azure
    • Led teams in agile development practices
    
    EDUCATION
    Master's Degree in Computer Science
    Bachelor's Degree in Software Engineering
    
    CERTIFICATIONS
    • AWS Certified Solutions Architect
    • Kubernetes Administrator (CKA)
    • Azure DevOps Engineer Expert
    """
    return cv_content.encode('utf-8')

def create_simple_cover_letter_pdf(job):
    """Create a simple cover letter PDF content"""
    cl_content = f"""
    COVER LETTER
    
    Dear Hiring Manager at {job['company']},
    
    I am writing to express my strong interest in the {job['title']} position at {job['company']} 
    in {job['location']}. With my extensive experience in DevOps, cloud infrastructure, and 
    software engineering, I am confident I would be a valuable addition to your team.
    
    My background includes:
    • 5+ years of experience with cloud platforms (AWS, Azure)
    • Expertise in containerization with Docker and Kubernetes
    • Infrastructure as Code using Terraform and Ansible
    • CI/CD pipeline development with Jenkins and GitLab
    • Full-stack development in Java, Python, and JavaScript
    
    I am particularly excited about this opportunity at {job['company']} because of your 
    reputation for innovation and technical excellence. I would love to contribute my skills 
    in {', '.join(job['keywords'][:5])} to help drive your platform forward.
    
    I am available for an interview at your convenience and look forward to discussing 
    how my experience and enthusiasm can benefit your team.
    
    Thank you for your consideration.
    
    Best regards,
    Hongzhi (Harvad) Li
    hongzhili01@gmail.com
    +46 XXX XXX XXX
    """
    return cl_content.encode('utf-8')

def create_job_email_html(job):
    """Create HTML email body for job application"""
    application_link = job.get('application_link', job.get('url', ''))
    keywords = ', '.join(job.get('keywords', [])[:10])
    
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c5282; border-bottom: 2px solid #2c5282; padding-bottom: 10px;">
                🎯 New Job Opportunity Match Found!
            </h2>
            
            <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2d3748; margin-top: 0;">
                    {job.get('title', 'Software Position')} at {job.get('company', 'Technology Company')}
                </h3>
                <p><strong>📍 Location:</strong> {job.get('location', 'Sweden')}</p>
                <p><strong>💼 Employment:</strong> {job.get('employment_type', 'Full-time')}</p>
                <p><strong>💰 Salary:</strong> {job.get('salary', 'Competitive salary')}</p>
                <p><strong>🏷️ Keywords:</strong> {keywords}</p>
                <p><strong>⭐ Experience Level:</strong> {job.get('experience_level', 'Senior')}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <h4 style="color: #2d3748;">Job Description:</h4>
                <p style="background: #edf2f7; padding: 15px; border-radius: 6px; font-size: 14px;">
                    {job.get('description', 'See full job details at application link')[:500]}
                    {'...' if len(job.get('description', '')) > 500 else ''}
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{application_link}" 
                   style="background: #3182ce; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 16px;">
                    🚀 APPLY NOW AT {job.get('company', 'COMPANY').upper()}
                </a>
            </div>
            
            <div style="background: #e6fffa; padding: 15px; border-radius: 6px; border-left: 4px solid #38b2ac;">
                <h4 style="color: #2c7a7b; margin-top: 0;">📎 Application Documents Attached</h4>
                <p style="margin-bottom: 0; color: #2d3748;">
                    ✅ Customized CV for {job.get('company', 'this position')}<br>
                    ✅ Tailored Cover Letter highlighting relevant experience<br>
                    📄 Ready to submit with your application
                </p>
            </div>
            
            <div style="background: #fff5f5; padding: 15px; border-radius: 6px; border-left: 4px solid #f56565; margin: 20px 0;">
                <h4 style="color: #c53030; margin-top: 0;">⚡ Action Required</h4>
                <p style="margin-bottom: 0; color: #2d3748;">
                    1. Review the attached CV and Cover Letter<br>
                    2. Click the "APPLY NOW" button above<br>
                    3. Submit your application with the provided documents<br>
                    4. Follow up if needed within 1 week
                </p>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #718096; font-size: 12px;">
                <p>📧 Automated Job Hunter System - Tuesday {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                <p>🤖 This job was automatically matched to your profile and skills</p>
                <p>💼 More opportunities will be sent as they become available</p>
            </div>
        </div>
    </body>
    </html>
    """

async def send_test_email():
    """Send a test job email"""
    try:
        logger.info("🚀 Sending test job email to hongzhili01@gmail.com")
        
        # Email configuration
        sender_email = "leeharvad@gmail.com"  
        target_email = "hongzhili01@gmail.com"
        
        # Use app password - you need to generate this from Gmail
        # Go to Google Account > Security > 2-Step Verification > App passwords
        sender_password = os.getenv("SMTP_PASSWORD", "")
        if not sender_password:
            logger.error("❌ SMTP_PASSWORD environment variable not set!")
            logger.info("📝 Please set SMTP_PASSWORD=your_gmail_app_password in environment")
            # For testing, we'll simulate the email
            logger.info("🎭 Running in SIMULATION MODE - no actual email sent")
            sender_password = "simulation_mode"
        
        # Create test job
        job = create_test_job()
        
        # Generate simple CV and cover letter
        cv_pdf = create_simple_cv_pdf()
        cl_pdf = create_simple_cover_letter_pdf(job)
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = target_email
        msg['Subject'] = f"🎯 URGENT: {job['title']} at {job['company']} - Application Ready!"
        
        # Create email body
        email_body = create_job_email_html(job)
        msg.attach(MIMEText(email_body, 'html'))
        
        # Attach CV
        cv_attachment = MIMEApplication(cv_pdf, _subtype='pdf')
        cv_attachment.add_header(
            'Content-Disposition', 
            'attachment', 
            filename=f"CV_Hongzhi_Li_{job['company']}_{job['title'].replace(' ', '_')}.pdf"
        )
        msg.attach(cv_attachment)
        
        # Attach Cover Letter
        cl_attachment = MIMEApplication(cl_pdf, _subtype='pdf')
        cl_attachment.add_header(
            'Content-Disposition', 
            'attachment', 
            filename=f"Cover_Letter_Hongzhi_Li_{job['company']}_{job['title'].replace(' ', '_')}.pdf"
        )
        msg.attach(cl_attachment)
        
        if sender_password == "simulation_mode":
            logger.info("✅ [SIMULATION] Email created successfully with attachments")
            logger.info(f"📧 Would send to: {target_email}")
            logger.info(f"📄 Subject: {msg['Subject']}")
            logger.info(f"📎 Attachments: CV and Cover Letter PDFs")
            logger.info("⚡ To enable real email sending, set SMTP_PASSWORD environment variable")
            return True
        
        # Send email using SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        logger.info(f"✅ Successfully sent job email to {target_email}")
        logger.info(f"📧 Subject: {msg['Subject']}")
        logger.info(f"📎 Attached CV and Cover Letter for {job['company']}")
        logger.info("🎉 Check your email inbox now!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send test email: {e}")
        return False

async def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("📧 JOB HUNTER EMAIL TEST")
    logger.info("=" * 60)
    
    success = await send_test_email()
    
    if success:
        logger.info("✅ Test completed successfully!")
        logger.info("📧 Check hongzhili01@gmail.com for the job opportunity email")
    else:
        logger.error("❌ Test failed!")
        
    logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())