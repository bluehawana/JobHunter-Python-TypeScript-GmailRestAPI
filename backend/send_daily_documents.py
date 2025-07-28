#!/usr/bin/env python3
"""
Daily document sender for Heroku Scheduler
Sends tailored CV and cover letter documents to leeharvad@gmail.com
Run with: python send_daily_documents.py
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import glob
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_recent_pdfs():
    """Get recently generated PDF documents"""
    pdf_patterns = [
        "*.pdf",
        "job_application_package/*.pdf", 
        "simple_pdfs/*.pdf"
    ]
    
    recent_pdfs = []
    for pattern in pdf_patterns:
        files = glob.glob(pattern)
        for file in files:
            if os.path.exists(file):
                recent_pdfs.append(file)
    
    # Sort by modification time, get most recent 10
    recent_pdfs.sort(key=os.path.getmtime, reverse=True)
    return recent_pdfs[:10]

def send_daily_documents():
    """Send daily CV/CL documents via email"""
    try:
        # Email configuration from environment
        smtp_user = os.getenv("SMTP_USER", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        to_email = "hongzhili01@gmail.com"
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"Daily Job Application Documents - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Email body
        body = f"""
Daily Job Application Documents

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

These are the latest tailored CV and cover letter documents from your JobHunter automation system.

Best regards,
JobHunter Automation Bot
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach recent PDFs
        recent_pdfs = get_recent_pdfs()
        attached_count = 0
        
        for pdf_path in recent_pdfs:
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                    
                pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                        filename=os.path.basename(pdf_path))
                msg.attach(pdf_attachment)
                attached_count += 1
                logger.info(f"Attached: {pdf_path}")
                
            except Exception as e:
                logger.warning(f"Failed to attach {pdf_path}: {e}")
        
        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"Daily documents sent successfully! Attached {attached_count} files to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending daily documents: {e}")
        return False

if __name__ == "__main__":
    success = send_daily_documents()
    if not success:
        exit(1)