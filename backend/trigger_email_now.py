#!/usr/bin/env python3
"""
Immediate trigger for sending daily documents
This script bypasses the Heroku app and directly sends emails with recent PDFs
"""
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import glob
import json
from datetime import datetime
import logging

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

def get_recent_pdfs():
    """Get recently generated PDF documents with metadata"""
    recent_pdfs = []
    
    # Search for PDFs in multiple locations, prioritizing newest ones
    search_paths = [
        "..",                   # parent directory (main project) - PRIORITY for newest files
        ".",                    # current directory (backend)
        "job_application_package",
        "simple_pdfs"
    ]
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            pdf_pattern = os.path.join(search_path, "*.pdf")
            files = glob.glob(pdf_pattern)
            for file in files:
                if os.path.exists(file) and os.path.getsize(file) > 1000:  # Only PDFs > 1KB
                    basename = os.path.basename(file)
                    # Skip test files
                    if not basename.startswith('test_'):
                        job_info = extract_job_info_from_filename(basename)
                        recent_pdfs.append({
                            'path': file,
                            'filename': basename,
                            'job_info': job_info,
                            'modified': os.path.getmtime(file)
                        })
    
    # Sort by modification time, get most recent 10
    recent_pdfs.sort(key=lambda x: x['modified'], reverse=True)
    return recent_pdfs[:10]

def extract_job_info_from_filename(filename):
    """Extract job information from PDF filename"""
    # Remove extension
    name = filename.replace('.pdf', '')
    
    # Common patterns to extract company and position
    if 'cv_' in name.lower():
        parts = name.replace('cv_', '').replace('CV_', '').split('_')
    elif 'cover_letter_' in name.lower():
        parts = name.replace('cover_letter_', '').replace('Cover_Letter_', '').split('_')
    else:
        parts = name.split('_')
    
    # Try to identify company and position
    company = ""
    position = ""
    
    if len(parts) >= 2:
        # Look for known company patterns
        potential_companies = ['Spotify', 'Volvo', 'Ericsson', 'SKF', 'Hasselblad', 'Netflix', 'Zenseact']
        for part in parts:
            for known_company in potential_companies:
                if known_company.lower() in part.lower():
                    company = known_company
                    break
        
        # Extract position (usually contains words like developer, engineer, etc.)
        position_keywords = ['developer', 'engineer', 'devops', 'backend', 'frontend', 'fullstack', 'senior']
        position_parts = []
        for part in parts:
            if any(keyword in part.lower() for keyword in position_keywords):
                position_parts.append(part.replace('_', ' ').title())
        
        position = ' '.join(position_parts) if position_parts else 'Software Position'
        if not company:
            company = parts[0].replace('_', ' ').title()
    
    return {
        'company': company or 'Unknown Company',
        'position': position or 'Software Position',
        'type': 'CV' if 'cv' in filename.lower() else 'Cover Letter'
    }

def get_job_application_links():
    """Get job application links from recent job processing"""
    try:
        # Check for job processing files that might contain URLs
        job_files = [
            'processed_jobs.json',
            'linkedin_saved_jobs.json', 
            'recent_job_data.json'
        ]
        
        job_links = []
        
        for job_file in job_files:
            if os.path.exists(job_file):
                try:
                    with open(job_file, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for job in data:
                                if isinstance(job, dict) and 'url' in job:
                                    job_links.append({
                                        'company': job.get('company', 'Unknown'),
                                        'title': job.get('title', 'Position'),
                                        'url': job.get('url', '#'),
                                        'location': job.get('location', 'N/A')
                                    })
                        elif isinstance(data, dict):
                            for key, jobs in data.items():
                                if isinstance(jobs, list):
                                    for job in jobs:
                                        if isinstance(job, dict) and 'url' in job:
                                            job_links.append({
                                                'company': job.get('company', 'Unknown'),
                                                'title': job.get('title', 'Position'),
                                                'url': job.get('url', '#'),
                                                'location': job.get('location', 'N/A')
                                            })
                except Exception as e:
                    logger.warning(f"Could not parse {job_file}: {e}")
        
        # Add some default LinkedIn job links if no data found
        if not job_links:
            job_links = [
                {
                    'company': 'Ericsson',
                    'title': 'Senior Backend Developer',
                    'url': 'https://www.linkedin.com/jobs/search/?keywords=backend%20developer%20ericsson%20gothenburg',
                    'location': 'Gothenburg'
                },
                {
                    'company': 'Hasselblad',
                    'title': 'Cloud Engineer',
                    'url': 'https://www.linkedin.com/jobs/search/?keywords=cloud%20engineer%20hasselblad',
                    'location': 'Gothenburg'
                },
                {
                    'company': 'Netflix',
                    'title': 'Software Engineer',
                    'url': 'https://jobs.netflix.com/search?q=software%20engineer&location=europe',
                    'location': 'Remote (Europe)'
                }
            ]
        
        return job_links[:5]  # Limit to top 5 jobs
        
    except Exception as e:
        logger.error(f"Error getting job links: {e}")
        return []

def send_daily_documents():
    """Send daily CV/CL documents via email with updated credentials"""
    try:
        # Email configuration from environment
        smtp_user = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set")
            print("ERROR: SMTP_PASSWORD environment variable not set")
            return False
        to_email = "hongzhili01@gmail.com"
        
        logger.info(f"Attempting to send email from {smtp_user} to {to_email}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"Daily Job Application Documents - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Get job application links and PDF info
        job_links = get_job_application_links()
        recent_pdfs = get_recent_pdfs()
        
        # Build job links section
        job_links_text = ""
        if job_links:
            job_links_text = "\n🔗 JOB APPLICATION LINKS:\n" + "="*50 + "\n"
            for i, job in enumerate(job_links, 1):
                job_links_text += f"{i}. {job['title']} at {job['company']}\n"
                job_links_text += f"   📍 Location: {job['location']}\n"
                job_links_text += f"   🔗 Apply: {job['url']}\n\n"
        
        # Build PDF summary
        pdf_summary = ""
        if recent_pdfs:
            pdf_summary = "\n📄 ATTACHED DOCUMENTS:\n" + "="*50 + "\n"
            for i, pdf in enumerate(recent_pdfs, 1):
                job_info = pdf['job_info']
                pdf_summary += f"{i}. {pdf['filename']}\n"
                pdf_summary += f"   📋 {job_info['type']} for {job_info['position']} at {job_info['company']}\n"
                pdf_summary += f"   📅 Modified: {datetime.fromtimestamp(pdf['modified']).strftime('%Y-%m-%d %H:%M')}\n\n"

        # Email body
        body = f"""
🤖 JOBHUNTER DAILY APPLICATION REPORT
============================================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your JobHunter automation system has prepared the latest tailored CV and cover letter documents for your job applications.

{job_links_text}
{pdf_summary}

📧 EMAIL INSTRUCTIONS:
- PDFs are attached and ready to download
- Click the job links above to apply directly
- Each CV/CL is customized for the specific role and company
- Documents are optimized for ATS (Applicant Tracking Systems)

🎯 NEXT STEPS:
1. Download the attached PDFs
2. Review each document for accuracy
3. Click the job application links above
4. Submit your applications with the corresponding documents

💡 TIP: Each document is specifically tailored to match the job requirements and company culture for maximum impact.

Best regards,
🤖 JobHunter Automation System
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach recent PDFs
        attached_count = 0
        
        logger.info(f"Found {len(recent_pdfs)} PDF files to attach")
        
        for pdf_data in recent_pdfs:
            pdf_path = pdf_data['path']
            filename = pdf_data['filename']
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                    
                pdf_attachment = MIMEApplication(pdf_content, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(pdf_attachment)
                attached_count += 1
                logger.info(f"Attached: {filename} ({pdf_path})")
                
            except Exception as e:
                logger.warning(f"Failed to attach {pdf_path}: {e}")
        
        if attached_count == 0:
            logger.warning("No PDFs were attached to the email")
        
        # Send email
        logger.info("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        logger.info("Logging into SMTP server...")
        server.login(smtp_user, smtp_password)
        
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"✅ Daily documents sent successfully! Attached {attached_count} files to {to_email}")
        print(f"SUCCESS: Email sent with {attached_count} PDF attachments")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending daily documents: {e}")
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = send_daily_documents()
    if not success:
        sys.exit(1)