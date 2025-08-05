#!/usr/bin/env python3
"""
Automated Job Application System
Sends individual emails for each job with matching CV/CL documents
"""
import smtplib
import os
import sys
import glob
import json
from datetime import datetime
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load environment variables manually from .env file
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove inline comments
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobApplicationMatcher:
    """Matches job opportunities with their corresponding CV/CL documents"""
    
    def __init__(self):
        self.company_keywords = {
            'ericsson': ['ericsson'],
            'hasselblad': ['hasselblad'],
            'netflix': ['netflix'],
            'spotify': ['spotify'],
            'volvo': ['volvo'],
            'skf': ['skf'],
            'zenseact': ['zenseact']
        }
        
    def get_job_opportunities(self):
        """Get individual job opportunities from processed_jobs.json"""
        try:
            with open('processed_jobs.json', 'r') as f:
                jobs = json.load(f)
                return jobs if isinstance(jobs, list) else []
        except FileNotFoundError:
            logger.warning("processed_jobs.json not found")
            return []
        except Exception as e:
            logger.error(f"Error reading job opportunities: {e}")
            return []
    
    def find_matching_documents(self, job):
        """Find CV and Cover Letter that match a specific job"""
        company = job.get('company', '').lower()
        title = job.get('title', '').lower()
        
        # Search for PDFs in multiple locations
        search_paths = ["..", ".", "job_application_package", "simple_pdfs"]
        
        matching_cv = None
        matching_cl = None
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                pdf_pattern = os.path.join(search_path, "*.pdf")
                files = glob.glob(pdf_pattern)
                
                for file in files:
                    if os.path.exists(file) and os.path.getsize(file) > 1000:
                        basename = os.path.basename(file).lower()
                        
                        # Skip test files
                        if basename.startswith('test_'):
                            continue
                            
                        # Check if this PDF matches the job's company
                        company_match = False
                        for comp_key, keywords in self.company_keywords.items():
                            if any(keyword in basename for keyword in keywords):
                                if comp_key in company or any(keyword in company for keyword in keywords):
                                    company_match = True
                                    break
                        
                        if company_match:
                            if 'cv' in basename and not matching_cv:
                                matching_cv = file
                            elif ('cl' in basename or 'cover' in basename) and not matching_cl:
                                matching_cl = file
        
        return matching_cv, matching_cl
    
    def get_job_document_pairs(self):
        """Get all job opportunities paired with their matching documents"""
        jobs = self.get_job_opportunities()
        job_document_pairs = []
        
        for job in jobs:
            cv_path, cl_path = self.find_matching_documents(job)
            
            if cv_path and cl_path:
                job_document_pairs.append({
                    'job': job,
                    'cv_path': cv_path,
                    'cl_path': cl_path,
                    'cv_filename': os.path.basename(cv_path),
                    'cl_filename': os.path.basename(cl_path)
                })
                logger.info(f"✅ Matched {job['company']} - {job['title']}")
            else:
                logger.warning(f"❌ No matching documents for {job['company']} - {job['title']}")
        
        return job_document_pairs

class AutomatedJobEmailSender:
    """Sends individual emails for each job application"""
    
    def __init__(self):
        self.smtp_user = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.to_email = "hongzhili01@gmail.com"
        
        if not self.smtp_password:
            raise ValueError("SMTP_PASSWORD not set in environment")
    
    def create_job_email(self, job_pair):
        """Create email for a single job application"""
        job = job_pair['job']
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = self.to_email
        msg['Subject'] = f"🎯 Job Application Ready: {job['title']} at {job['company']}"
        
        # Email body for single job
        body = f"""
🎯 AUTOMATED JOB APPLICATION READY
============================================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your JobHunter system has prepared a tailored application package for this specific opportunity:

🏢 COMPANY: {job['company']}
💼 POSITION: {job['title']}
📍 LOCATION: {job.get('location', 'Not specified')}

🔗 DIRECT APPLICATION LINK:
{job['url']}

📄 ATTACHED DOCUMENTS:
==================================================
✅ Customized CV: {job_pair['cv_filename']}
✅ Tailored Cover Letter: {job_pair['cl_filename']}

Both documents are specifically optimized for:
• {job['company']}'s company culture and values
• {job['title']} role requirements
• ATS (Applicant Tracking System) compatibility
• Industry-specific keywords and terminology

🎯 NEXT STEPS:
1. Click the application link above
2. Upload the attached CV and Cover Letter
3. Complete the application form
4. Submit your application

💡 SUCCESS TIP: These documents are pre-customized for maximum impact at {job['company']}. The CV highlights relevant experience and the cover letter addresses their specific needs.

🤖 This is an automated application prepared by your JobHunter system.

Best of luck with your application!

---
JobHunter Automation System
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CV
        try:
            with open(job_pair['cv_path'], 'rb') as f:
                cv_content = f.read()
            cv_attachment = MIMEApplication(cv_content, _subtype='pdf')
            cv_attachment.add_header('Content-Disposition', 'attachment', 
                                   filename=job_pair['cv_filename'])
            msg.attach(cv_attachment)
            logger.info(f"✅ Attached CV: {job_pair['cv_filename']}")
        except Exception as e:
            logger.error(f"❌ Failed to attach CV: {e}")
            return None
        
        # Attach Cover Letter
        try:
            with open(job_pair['cl_path'], 'rb') as f:
                cl_content = f.read()
            cl_attachment = MIMEApplication(cl_content, _subtype='pdf')
            cl_attachment.add_header('Content-Disposition', 'attachment', 
                                   filename=job_pair['cl_filename'])
            msg.attach(cl_attachment)
            logger.info(f"✅ Attached CL: {job_pair['cl_filename']}")
        except Exception as e:
            logger.error(f"❌ Failed to attach Cover Letter: {e}")
            return None
        
        return msg
    
    def send_job_applications(self, max_jobs=5):
        """Send individual emails for each job application"""
        matcher = JobApplicationMatcher()
        job_pairs = matcher.get_job_document_pairs()
        
        if not job_pairs:
            logger.warning("No job-document pairs found to send")
            return False
        
        # Limit number of jobs to send
        job_pairs = job_pairs[:max_jobs]
        
        try:
            # Connect to SMTP server once
            logger.info("Connecting to SMTP server...")
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            
            sent_count = 0
            
            for i, job_pair in enumerate(job_pairs, 1):
                job = job_pair['job']
                logger.info(f"📧 Sending email {i}/{len(job_pairs)}: {job['company']} - {job['title']}")
                
                # Create email for this job
                msg = self.create_job_email(job_pair)
                if msg:
                    # Send email
                    server.sendmail(self.smtp_user, self.to_email, msg.as_string())
                    sent_count += 1
                    logger.info(f"✅ Sent: {job['company']} - {job['title']}")
                else:
                    logger.error(f"❌ Failed to create email for {job['company']} - {job['title']}")
            
            server.quit()
            
            logger.info(f"🎉 Successfully sent {sent_count} job application emails!")
            print(f"SUCCESS: Sent {sent_count} individual job application emails")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending job applications: {e}")
            print(f"ERROR: {e}")
            return False

def main():
    """Main function to run automated job applications"""
    try:
        sender = AutomatedJobEmailSender()
        success = sender.send_job_applications(max_jobs=5)
        return 0 if success else 1
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print(f"FATAL ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())