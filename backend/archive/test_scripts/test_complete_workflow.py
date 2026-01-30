#!/usr/bin/env python3
"""
Complete workflow test: Email scanning -> Resume/Cover Letter customization -> PDF generation -> Email sending
This demonstrates the full JobHunter automation pipeline with template selection for job applications.
"""
import asyncio
import sys
import os
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

# Configure email settings - load from environment variables
required_smtp_vars = ['SMTP_USER', 'SMTP_PASSWORD']
missing_smtp_vars = [var for var in required_smtp_vars if not os.getenv(var)]
if missing_smtp_vars:
    print(f"❌ Missing required SMTP environment variables: {', '.join(missing_smtp_vars)}")
    print("Please set the following environment variables:")
    for var in missing_smtp_vars:
        if var == 'SMTP_USER':
            print(f"  export {var}='your-email@gmail.com'")
        elif var == 'SMTP_PASSWORD':
            print(f"  export {var}='your-app-password'")
    print("⚠️ Continuing with limited functionality...")

# Set defaults for non-sensitive configuration
os.environ.setdefault('SMTP_HOST', 'smtp.gmail.com')
os.environ.setdefault('SMTP_PORT', '587')
os.environ.setdefault('EMAILS_FROM_EMAIL', os.getenv('SMTP_USER', 'noreply@example.com'))
os.environ.setdefault('EMAILS_FROM_NAME', 'JobHunter Bot')
os.environ.setdefault('TARGET_EMAIL', 'recipient@example.com')

from app.services.job_application_processor import JobApplicationProcessor
from app.services.simple_latex_service import SimpleLaTeXService
from app.services.email_scanner_service import EmailScannerService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def send_template_email(job_results):
    """Send email with job application templates to leeharvad@gmail.com"""
    try:
        # Email configuration
        smtp_server = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        sender_email = os.environ.get('EMAILS_FROM_EMAIL')
        sender_password = os.environ.get('SMTP_PASSWORD')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"JobHunter Bot <{sender_email}>"
        msg['To'] = os.getenv('TARGET_EMAIL', 'recipient@example.com')
        msg['Subject'] = "🎯 JobHunter Application Templates - Ready for Your Review"
        
        # Create email body with job templates
        email_body = f"""
        <html>
        <body>
            <h2>🎯 JobHunter Application Templates</h2>
            <p>Hi there!</p>
            
            <p>Your JobHunter automation system has processed <strong>{len(job_results)}</strong> job opportunities and generated customized application materials for each position.</p>
            
            <h3>📋 Processing Summary:</h3>
            <ul>
"""
        
        for i, result in enumerate(job_results, 1):
            job = result.get('job', {})
            status = result.get('status', 'unknown')
            cv_size = len(result.get('cv_pdf', b''))
            cl_size = len(result.get('cover_letter_pdf', b''))
            
            email_body += f"""
                <li>
                    <strong>Job {i}: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}</strong><br>
                    📍 Location: {job.get('location', 'N/A')}<br>
                    🔗 Source: {job.get('source', 'N/A')}<br>
                    🏷️ Keywords: {', '.join(job.get('keywords', [])[:5])}...<br>
                    ✅ Status: {status}<br>
                    📄 CV PDF: {cv_size} bytes generated<br>
                    📝 Cover Letter PDF: {cl_size} bytes generated<br>
                    <br>
                </li>
"""
        
        email_body += f"""
            </ul>
            
            <h3>📎 Attached Files:</h3>
            <p>Each job application includes:</p>
            <ul>
                <li>📄 <strong>Customized CV/Resume</strong> - Tailored to highlight relevant experience for the specific role</li>
                <li>📝 <strong>Personalized Cover Letter</strong> - Crafted to address the company and position requirements</li>
            </ul>
            
            <h3>🎯 Next Steps:</h3>
            <ol>
                <li>Review each application template attached to this email</li>
                <li>Choose which jobs to apply for based on your preferences</li>
                <li>Customize the templates further if needed</li>
                <li>Submit applications directly to the companies</li>
            </ol>
            
            <h3>📊 Job Details:</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Source</th>
                    <th>Top Keywords</th>
                </tr>
"""
        
        for result in job_results:
            job = result.get('job', {})
            email_body += f"""
                <tr>
                    <td>{job.get('title', 'N/A')}</td>
                    <td>{job.get('company', 'N/A')}</td>
                    <td>{job.get('location', 'N/A')}</td>
                    <td>{job.get('source', 'N/A')}</td>
                    <td>{', '.join(job.get('keywords', [])[:3])}</td>
                </tr>
"""
        
        email_body += f"""
            </table>
            
            <p><em>This email was automatically generated by your JobHunter automation system on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            
            <p>Happy job hunting! 🚀</p>
            
            <p>Best regards,<br>
            JobHunter Bot 🤖</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(email_body, 'html'))
        
        # Attach PDFs for each job
        for i, result in enumerate(job_results, 1):
            if result.get('status') == 'success':
                job = result.get('job', {})
                company_name = job.get('company', 'Company').replace(' ', '_')
                job_title = job.get('title', 'Position').replace(' ', '_')
                
                # Attach CV PDF
                if result.get('cv_pdf'):
                    cv_attachment = MIMEApplication(result['cv_pdf'], _subtype='pdf')
                    cv_attachment.add_header('Content-Disposition', 'attachment', 
                                           filename=f'cv_{company_name}_{job_title}.pdf')
                    msg.attach(cv_attachment)
                
                # Attach Cover Letter PDF
                if result.get('cover_letter_pdf'):
                    cl_attachment = MIMEApplication(result['cover_letter_pdf'], _subtype='pdf')
                    cl_attachment.add_header('Content-Disposition', 'attachment', 
                                           filename=f'cover_letter_{company_name}_{job_title}.pdf')
                    msg.attach(cl_attachment)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        logger.info(f"✅ Template email sent successfully to {os.getenv('TARGET_EMAIL', 'recipient@example.com')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send template email: {e}")
        return False

async def test_complete_workflow():
    """Test the complete JobHunter workflow from email scanning to application sending"""
    try:
        logger.info("🚀 === Starting Complete JobHunter Workflow Test ===")
        
        # Step 1: Initialize services
        logger.info("📧 Step 1: Initializing email scanning and job processing services...")
        processor = JobApplicationProcessor()
        processor.latex_service = SimpleLaTeXService()
        email_scanner = EmailScannerService()
        
        # Step 2: Process sample jobs (simulating email scan results)
        logger.info("🔍 Step 2: Processing job listings from email sources...")
        results = await processor.process_sample_jobs()
        
        # Step 3: Display processing results
        logger.info(f"📊 Step 3: Processing completed!")
        logger.info(f"✅ Jobs successfully processed: {len([r for r in results if r.get('status') == 'success'])}/{len(results)}")
        
        successful_results = [r for r in results if r.get('status') == 'success']
        
        if successful_results:
            # Step 4: Send template email with all applications
            logger.info(f"📤 Step 4: Sending application templates to {os.getenv('TARGET_EMAIL', 'recipient@example.com')}...")
            email_sent = await send_template_email(successful_results)
            
            if email_sent:
                logger.info("🎉 === Workflow Test Complete! ===")
                logger.info(f"📧 Check {os.getenv('TARGET_EMAIL', 'recipient@example.com')} for:")
                logger.info("   • Detailed job analysis")
                logger.info("   • Customized CV/Resume PDFs")
                logger.info("   • Personalized cover letter PDFs")
                logger.info("   • Application guidance and next steps")
            else:
                logger.error("❌ Email sending failed")
        else:
            logger.error("❌ No successful job processing results to send")
            
        # Step 5: Summary
        logger.info(f"\n📈 === Final Summary ===")
        for i, result in enumerate(results, 1):
            job = result.get('job', {})
            logger.info(f"Job {i}: {job.get('title')} at {job.get('company')} - {result.get('status', 'unknown')}")
        
        return results
        
    except Exception as e:
        logger.error(f"💥 Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    logger.info("🎯 JobHunter Complete Workflow Test")
    logger.info("This will demonstrate: Email scanning → Customization → PDF generation → Template delivery")
    asyncio.run(test_complete_workflow())