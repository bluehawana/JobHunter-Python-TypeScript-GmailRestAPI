import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import re

from app.services.linkedin_service import LinkedInService
from app.services.gmail_service import GmailService
from app.services.latex_resume_service import LaTeXResumeService
from app.services.supabase_service import supabase_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class JobProcessor:
    """Service to process jobs from various sources and generate customized applications"""
    
    def __init__(self):
        self.linkedin_service = LinkedInService()
        self.latex_service = LaTeXResumeService()
        
    async def process_linkedin_job(self, job_url: str) -> Optional[Dict[str, Any]]:
        """Process a LinkedIn job from URL"""
        try:
            # Extract job ID from LinkedIn URL
            job_id = self._extract_linkedin_job_id(job_url)
            if not job_id:
                logger.error(f"Could not extract job ID from URL: {job_url}")
                return None
            
            logger.info(f"Fetching LinkedIn job with ID: {job_id}")
            
            # Get job details using LinkedIn API
            job_data = await self.linkedin_service.get_job_details(job_id)
            
            if not job_data:
                # Fallback: Try to get job through search if direct API fails
                logger.info("Direct API failed, trying search approach...")
                job_data = await self._fallback_linkedin_search(job_id)
            
            if job_data:
                # Save to database
                db_job = await self._save_job_to_database(job_data)
                return db_job
            else:
                logger.error(f"Could not fetch LinkedIn job: {job_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing LinkedIn job {job_url}: {e}")
            return None
    
    async def process_gmail_job(self, gmail_url: str) -> Optional[Dict[str, Any]]:
        """Process a job from Gmail email"""
        try:
            # Extract search parameters from Gmail URL
            search_params = self._extract_gmail_search_params(gmail_url)
            
            logger.info(f"Searching Gmail for: {search_params}")
            
            # For now, create a mock job from the Gmail URL since we need proper OAuth setup
            # In production, you'd use the Gmail API to fetch the actual email content
            job_data = await self._create_mock_gmail_job(gmail_url, search_params)
            
            if job_data:
                # Save to database
                db_job = await self._save_job_to_database(job_data)
                return db_job
            else:
                logger.error(f"Could not process Gmail job: {gmail_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing Gmail job {gmail_url}: {e}")
            return None
    
    async def generate_application_materials(self, job_data: Dict[str, Any]) -> Dict[str, bytes]:
        """Generate customized resume and cover letter for a job"""
        try:
            logger.info(f"Generating application materials for: {job_data.get('job_title')} at {job_data.get('company_name')}")
            
            # Generate customized CV
            cv_pdf = await self.latex_service.generate_customized_cv(job_data)
            
            # Generate customized cover letter
            cover_letter_pdf = await self.latex_service.generate_customized_cover_letter(job_data)
            
            return {
                'cv': cv_pdf,
                'cover_letter': cover_letter_pdf
            }
            
        except Exception as e:
            logger.error(f"Error generating application materials: {e}")
            return {}
    
    async def send_job_application_email(self, job_data: Dict[str, Any], materials: Dict[str, bytes], recipient_email: str):
        """Send job application email with PDFs and job info"""
        try:
            logger.info(f"Sending application email to: {recipient_email}")
            
            # Create email content
            subject = f"Job Application Materials - {job_data.get('job_title', 'Position')} at {job_data.get('company_name', 'Company')}"
            
            # HTML email body
            html_body = self._create_email_body(job_data)
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = "hongzhili01@gmail.com"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Attach PDFs
            if materials.get('cv'):
                cv_attachment = MIMEBase('application', 'pdf')
                cv_attachment.set_payload(materials['cv'])
                encoders.encode_base64(cv_attachment)
                cv_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="CV_{job_data.get("company_name", "Company")}_Hongzhi_Li.pdf"'
                )
                msg.attach(cv_attachment)
            
            if materials.get('cover_letter'):
                cl_attachment = MIMEBase('application', 'pdf')
                cl_attachment.set_payload(materials['cover_letter'])
                encoders.encode_base64(cl_attachment)
                cl_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="CoverLetter_{job_data.get("company_name", "Company")}_Hongzhi_Li.pdf"'
                )
                msg.attach(cl_attachment)
            
            # Send email using Gmail SMTP
            await self._send_email_via_smtp(msg, recipient_email)
            
            # Update job status in database
            await supabase_service.update_application_status(
                job_data.get('id'), 
                'applied', 
                f'Application materials sent to {recipient_email}'
            )
            
            logger.info(f"Successfully sent application email for job: {job_data.get('job_title')}")
            
        except Exception as e:
            logger.error(f"Error sending application email: {e}")
            raise
    
    def _extract_linkedin_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from LinkedIn URL"""
        # Pattern: https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4266325638
        # Or: https://www.linkedin.com/jobs/view/4266325638
        
        patterns = [
            r'currentJobId=(\d+)',
            r'/jobs/view/(\d+)',
            r'jobId=(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_gmail_search_params(self, url: str) -> str:
        """Extract search parameters from Gmail URL"""
        # Pattern: https://mail.google.com/mail/u/0/#search/linkedin+jobs/FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx
        
        match = re.search(r'#search/([^/]+)', url)
        if match:
            search_term = match.group(1).replace('+', ' ')
            return search_term
        
        return "linkedin jobs"
    
    async def _fallback_linkedin_search(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Fallback method to search for LinkedIn job"""
        try:
            # Search for jobs and try to find the one with matching ID
            jobs = await self.linkedin_service.search_jobs("fullstack developer", "Sweden", num_results=50)
            
            for job in jobs:
                if job.get('job_id') == job_id or job_id in job.get('url', ''):
                    return job
            
            # If not found, create a mock job with the ID
            return {
                'title': 'Fullstack Developer',
                'company': 'LinkedIn Company',
                'location': 'Sweden',
                'description': 'Full-stack development position with modern technologies. Experience with React, Node.js, and cloud platforms preferred.',
                'url': f'https://www.linkedin.com/jobs/view/{job_id}',
                'source': 'linkedin.com',
                'posting_date': datetime.utcnow(),
                'job_type': 'fulltime',
                'experience_level': 'mid',
                'remote_option': True,
                'keywords': ['javascript', 'react', 'node.js', 'fullstack', 'cloud'],
                'job_id': job_id,
                'confidence_score': 0.7
            }
            
        except Exception as e:
            logger.error(f"Fallback LinkedIn search failed: {e}")
            return None
    
    async def _create_mock_gmail_job(self, gmail_url: str, search_params: str) -> Dict[str, Any]:
        """Create a mock job from Gmail search (placeholder for actual Gmail API integration)"""
        
        # In production, this would:
        # 1. Use Gmail API to fetch the actual email
        # 2. Parse the email content to extract job information
        # 3. Identify if it's from LinkedIn, Indeed, etc. and parse accordingly
        
        return {
            'title': 'Senior Backend Developer',
            'company': 'Tech Startup Sweden',
            'location': 'Stockholm, Sweden',
            'description': '''We are looking for a Senior Backend Developer to join our growing team. 
            
            Requirements:
            • 5+ years of experience with Java/Spring Boot
            • Experience with microservices architecture
            • Knowledge of cloud platforms (AWS/Azure)
            • Strong database skills (PostgreSQL, MongoDB)
            • Experience with CI/CD pipelines
            
            What we offer:
            • Competitive salary
            • Flexible working hours
            • Remote work options
            • Great team culture
            
            This position was shared via LinkedIn Jobs email notification.''',
            'url': gmail_url,
            'source': 'gmail_linkedin',
            'posting_date': datetime.utcnow(),
            'job_type': 'fulltime',
            'experience_level': 'senior',
            'remote_option': True,
            'keywords': ['java', 'spring boot', 'microservices', 'aws', 'azure', 'postgresql', 'mongodb', 'ci/cd'],
            'email_thread_id': 'FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx',
            'confidence_score': 0.8
        }
    
    async def _save_job_to_database(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save job to Supabase database"""
        try:
            # Map job data to database schema
            db_data = {
                'company_name': job_data.get('company', ''),
                'job_title': job_data.get('title', ''),
                'job_description': job_data.get('description', ''),
                'published_date': job_data.get('posting_date'),
                'application_link': job_data.get('url', ''),
                'location': job_data.get('location', ''),
                'work_type': 'remote' if job_data.get('remote_option') else 'onsite',
                'application_status': 'found',
                'final_result': 'pending',
                'memo': f"Job sourced from {job_data.get('source', 'unknown')}",
                'email_thread_id': job_data.get('email_thread_id'),
                'last_email_received': job_data.get('posting_date')
            }
            
            # Add salary information if available
            salary = job_data.get('salary')
            if salary:
                if isinstance(salary, dict):
                    if 'min' in salary and 'max' in salary:
                        db_data['salary_range'] = f"{salary.get('min', 0)}-{salary.get('max', 0)} {salary.get('currency', 'SEK')}"
                    elif 'min' in salary:
                        db_data['salary_range'] = f"From {salary.get('min', 0)} {salary.get('currency', 'SEK')}"
                    elif 'max' in salary:
                        db_data['salary_range'] = f"Up to {salary.get('max', 0)} {salary.get('currency', 'SEK')}"
            
            # Save to database
            saved_job = await supabase_service.create_job_application(db_data)
            logger.info(f"Saved job to database with ID: {saved_job.get('id')}")
            
            return saved_job
            
        except Exception as e:
            logger.error(f"Error saving job to database: {e}")
            raise
    
    def _create_email_body(self, job_data: Dict[str, Any]) -> str:
        """Create HTML email body with job information"""
        
        job_title = job_data.get('job_title', 'Position')
        company_name = job_data.get('company_name', 'Company')
        location = job_data.get('location', 'Location not specified')
        application_link = job_data.get('application_link', '#')
        description = job_data.get('job_description', 'No description available')
        
        # Truncate description for email
        if len(description) > 1000:
            description = description[:1000] + "... [truncated]"
        
        html_body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0066cc; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .job-info {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0066cc; margin: 20px 0; }}
                .footer {{ background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 0.9em; }}
                .btn {{ display: inline-block; padding: 10px 20px; background-color: #0066cc; color: white; text-decoration: none; border-radius: 5px; }}
                .description {{ background-color: white; padding: 15px; border: 1px solid #ddd; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Job Application Materials</h1>
                <p>Generated for Hongzhi Li</p>
            </div>
            
            <div class="content">
                <h2>Job Details</h2>
                
                <div class="job-info">
                    <h3>📋 {job_title}</h3>
                    <p><strong>🏢 Company:</strong> {company_name}</p>
                    <p><strong>📍 Location:</strong> {location}</p>
                    <p><strong>🔗 Application Link:</strong> <a href="{application_link}" target="_blank">View Job Posting</a></p>
                    <p><strong>📅 Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>
                
                <h3>Job Description</h3>
                <div class="description">
                    {description.replace(chr(10), '<br>')}
                </div>
                
                <h3>📎 Attached Documents</h3>
                <ul>
                    <li><strong>CV:</strong> Customized resume highlighting relevant experience</li>
                    <li><strong>Cover Letter:</strong> Personalized cover letter for this position</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{application_link}" class="btn" target="_blank">Apply for this Position</a>
                </div>
                
                <h3>Next Steps</h3>
                <ol>
                    <li>Review the attached CV and cover letter</li>
                    <li>Visit the job posting link to apply</li>
                    <li>Upload the customized documents</li>
                    <li>Submit your application</li>
                </ol>
            </div>
            
            <div class="footer">
                <p>Generated by JobHunter Application System</p>
                <p>Hongzhi Li | hongzhili01@gmail.com | +46 728 384 299</p>
                <p><a href="https://www.linkedin.com/in/hzl/">LinkedIn</a> | <a href="https://github.com/bluehawana">GitHub</a> | <a href="https://www.bluehawana.com">Portfolio</a></p>
            </div>
        </body>
        </html>
        '''
        
        return html_body
    
    async def _send_email_via_smtp(self, msg: MIMEMultipart, recipient_email: str):
        """Send email using Gmail SMTP"""
        try:
            # Gmail SMTP configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "hongzhili01@gmail.com"
            
            # You'll need to set up an app password for Gmail
            # For now, using a placeholder - in production, store this securely
            sender_password = os.getenv("GMAIL_APP_PASSWORD", "your-gmail-app-password")
            
            # Create SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient_email}")
            
        except Exception as e:
            logger.error(f"Error sending email via SMTP: {e}")
            raise

# Create singleton instance
job_processor = JobProcessor()