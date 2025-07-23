import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Dict, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class EmailAutomationService:
    """Service for automated email sending with CV and cover letter attachments"""
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "hongzhili01@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")  # App password
        self.from_email = os.getenv("EMAILS_FROM_EMAIL", "hongzhili01@gmail.com")
        self.from_name = os.getenv("EMAILS_FROM_NAME", "Hongzhi Li")
    
    async def send_application_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        cv_content: bytes,
        cover_letter_content: bytes,
        job_data: Dict
    ) -> bool:
        """
        Send job application email with CV and cover letter attachments
        
        Args:
            to_email: Recipient email (leeharvad@gmail.com)
            subject: Email subject with job title and company
            body: Email body content
            cv_content: PDF content of customized CV
            cover_letter_content: PDF content of customized cover letter
            job_data: Job information dictionary
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Create HTML email body
            html_body = self._create_html_email_body(body, job_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach CV
            if cv_content:
                cv_attachment = MIMEApplication(cv_content, _subtype='pdf')
                company_name = job_data.get('company', 'Company').replace(' ', '_')
                job_title = job_data.get('title', 'Position').replace(' ', '_')
                cv_filename = f"CV_HongzhiLi_{company_name}_{job_title}.pdf"
                cv_attachment.add_header('Content-Disposition', 'attachment', filename=cv_filename)
                msg.attach(cv_attachment)
            
            # Attach Cover Letter
            if cover_letter_content:
                cl_attachment = MIMEApplication(cover_letter_content, _subtype='pdf')
                cl_filename = f"CoverLetter_HongzhiLi_{company_name}_{job_title}.pdf"
                cl_attachment.add_header('Content-Disposition', 'attachment', filename=cl_filename)
                msg.attach(cl_attachment)
            
            # Send email
            success = await self._send_email(msg)
            
            if success:
                logger.info("Successfully sent application email for %s at %s", 
                           job_data.get('title'), job_data.get('company'))
            else:
                logger.error("Failed to send application email for %s at %s", 
                           job_data.get('title'), job_data.get('company'))
            
            return success
            
        except Exception as e:
            logger.error("Error sending application email: %s", e)
            return False
    
    def _create_html_email_body(self, text_body: str, job_data: Dict) -> str:
        """Create HTML formatted email body"""
        
        job_title = job_data.get('title', 'Position')
        company_name = job_data.get('company', 'Company')
        job_url = job_data.get('url', '#')
        job_location = job_data.get('location', 'N/A')
        job_source = job_data.get('source', 'Job Board')
        posting_date = job_data.get('posting_date')
        
        # Format posting date
        if posting_date:
            if isinstance(posting_date, str):
                try:
                    posting_date = datetime.fromisoformat(posting_date.replace('Z', '+00:00'))
                except:
                    pass
            if isinstance(posting_date, datetime):
                formatted_date = posting_date.strftime('%Y-%m-%d')
            else:
                formatted_date = 'N/A'
        else:
            formatted_date = 'N/A'
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .job-info {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .application-link {{ background-color: #007bff; color: white; padding: 10px 20px; 
                            text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; 
                  font-size: 12px; color: #6c757d; }}
        .highlight {{ color: #007bff; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Job Application: <span class="highlight">{job_title}</span></h2>
        <h3>Company: <span class="highlight">{company_name}</span></h3>
    </div>
    
    <div class="job-info">
        <h4>Job Details:</h4>
        <ul>
            <li><strong>Position:</strong> {job_title}</li>
            <li><strong>Company:</strong> {company_name}</li>
            <li><strong>Location:</strong> {job_location}</li>
            <li><strong>Source:</strong> {job_source}</li>
            <li><strong>Posted:</strong> {formatted_date}</li>
        </ul>
        
        <p><strong>Application Link:</strong></p>
        <a href="{job_url}" class="application-link" target="_blank">
            🔗 Apply for this position
        </a>
    </div>
    
    <div style="white-space: pre-line; margin: 20px 0;">
{text_body}
    </div>
    
    <div style="margin: 20px 0;">
        <h4>📎 Attachments:</h4>
        <ul>
            <li>✅ Customized Resume (CV_HongzhiLi_{company_name.replace(' ', '_')}_{job_title.replace(' ', '_')}.pdf)</li>
            <li>✅ Customized Cover Letter (CoverLetter_HongzhiLi_{company_name.replace(' ', '_')}_{job_title.replace(' ', '_')}.pdf)</li>
        </ul>
    </div>
    
    <div class="footer">
        <p><strong>📧 Contact Information:</strong></p>
        <p>
            Hongzhi Li<br>
            📧 hongzhili01@gmail.com<br>
            📱 0728384299<br>
            🔗 <a href="https://www.linkedin.com/in/hzl/">LinkedIn</a> | 
            <a href="https://github.com/bluehawana">GitHub</a> | 
            <a href="https://www.bluehawana.com">Website</a>
        </p>
        
        <hr>
        <p><em>🤖 This application was automatically generated and sent on {datetime.utcnow().strftime('%Y-%m-%d at %H:%M UTC')} 
        using the JobHunter automation system.</em></p>
        
        <p><strong>🎯 Automation Details:</strong></p>
        <ul>
            <li>✅ Job automatically discovered from {job_source}</li>
            <li>✅ Requirements filtered for experience level and skills match</li>
            <li>✅ Resume customized based on job requirements</li>
            <li>✅ Cover letter personalized for {company_name}</li>
            <li>✅ Application sent to leeharvad@gmail.com for review</li>
        </ul>
        
        <p style="font-size: 10px; color: #999;">
            JobHunter v1.0 - Automated Job Application System<br>
            For questions about this application, please contact hongzhili01@gmail.com
        </p>
    </div>
</body>
</html>
        """
        
        return html_body
    
    async def _send_email(self, msg: MIMEMultipart) -> bool:
        """Send email using SMTP"""
        try:
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()  # Enable security
            
            # Login to email account
            server.login(self.smtp_user, self.smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email credentials.")
            return False
        except smtplib.SMTPRecipientsRefused:
            logger.error("SMTP Recipients refused. Check recipient email address.")
            return False
        except smtplib.SMTPServerDisconnected:
            logger.error("SMTP Server disconnected unexpectedly.")
            return False
        except Exception as e:
            logger.error("Unexpected error sending email: %s", e)
            return False
    
    async def send_daily_summary_email(
        self, 
        to_email: str, 
        automation_results: Dict,
        processed_jobs: list
    ) -> bool:
        """Send daily summary of automation results"""
        try:
            subject = f"JobHunter Daily Summary - {automation_results.get('applications_sent', 0)} Applications Sent"
            
            # Create summary HTML
            html_body = self._create_summary_html(automation_results, processed_jobs)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(html_body, 'html'))
            
            return await self._send_email(msg)
            
        except Exception as e:
            logger.error("Error sending daily summary email: %s", e)
            return False
    
    def _create_summary_html(self, results: Dict, jobs: list) -> str:
        """Create HTML summary of daily automation results"""
        
        total_fetched = results.get('total_jobs_fetched', 0)
        after_filtering = results.get('jobs_after_filtering', 0)
        applications_sent = results.get('applications_sent', 0)
        
        # Create jobs table
        jobs_table = ""
        if jobs:
            jobs_table = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
            jobs_table += "<tr style='background-color: #f8f9fa;'><th>Company</th><th>Position</th><th>Location</th><th>Source</th></tr>"
            
            for job in jobs[:10]:  # Show max 10 jobs
                jobs_table += f"""
                <tr>
                    <td>{job.get('company', 'N/A')}</td>
                    <td>{job.get('job_title', 'N/A')}</td>
                    <td>{job.get('location', 'N/A')}</td>
                    <td>{job.get('source', 'N/A')}</td>
                </tr>
                """
            
            if len(jobs) > 10:
                jobs_table += f"<tr><td colspan='4'><em>... and {len(jobs) - 10} more applications</em></td></tr>"
            
            jobs_table += "</table>"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .stats {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .stat-item {{ display: inline-block; margin: 10px 20px; text-align: center; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .jobs-table {{ margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🎯 JobHunter Daily Automation Summary</h2>
        <p>Automated job search and application results for {datetime.utcnow().strftime('%Y-%m-%d')}</p>
    </div>
    
    <div class="stats">
        <h3>📊 Today's Statistics</h3>
        <div class="stat-item">
            <div class="stat-number">{total_fetched}</div>
            <div>Jobs Fetched</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{after_filtering}</div>
            <div>After Filtering</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{applications_sent}</div>
            <div>Applications Sent</div>
        </div>
    </div>
    
    <div>
        <h4>🎯 Filtering Criteria Applied:</h4>
        <ul>
            <li>✅ Jobs posted within last 2 weeks</li>
            <li>✅ Maximum 5 years experience required</li>
            <li>✅ Swedish language requirement ≤ B2 level</li>
            <li>✅ Skills matching your technical stack</li>
            <li>✅ Quality job postings with complete information</li>
        </ul>
    </div>
    
    {f'<div class="jobs-table"><h4>📋 Applications Sent Today:</h4>{jobs_table}</div>' if jobs_table else ''}
    
    <div class="footer">
        <p><strong>🤖 Automation System Status:</strong> ✅ Active</p>
        <p><strong>📅 Next Run:</strong> Tomorrow at 06:00 CET (Weekdays only)</p>
        <p><strong>📧 All applications forwarded to:</strong> leeharvad@gmail.com</p>
        
        <hr>
        <p><em>JobHunter Automation System - Generated on {datetime.utcnow().strftime('%Y-%m-%d at %H:%M UTC')}</em></p>
    </div>
</body>
</html>
        """
        
        return html_content
    
    async def test_email_connection(self) -> Dict:
        """Test email connection and configuration"""
        try:
            # Test SMTP connection
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.quit()
            
            return {
                "status": "success",
                "message": "Email connection successful",
                "smtp_host": self.smtp_host,
                "smtp_port": self.smtp_port,
                "smtp_user": self.smtp_user
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                "status": "error",
                "message": "SMTP Authentication failed. Check email credentials.",
                "smtp_host": self.smtp_host,
                "smtp_port": self.smtp_port,
                "smtp_user": self.smtp_user
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Email connection failed: {str(e)}",
                "smtp_host": self.smtp_host,
                "smtp_port": self.smtp_port,
                "smtp_user": self.smtp_user
            }