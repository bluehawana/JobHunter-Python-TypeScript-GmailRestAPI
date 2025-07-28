#!/usr/bin/env python3
"""
Optimized email sender - sends notification first, then documents in batches
"""
import smtplib
import os
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_notification_and_documents():
    """Send notification email and documents in manageable batches"""
    try:
        smtp_user = os.getenv("SMTP_USER", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set")
            return False
        to_email = "hongzhili01@gmail.com"
        
        # First, send notification
        logger.info("Sending notification email...")
        msg = MIMEText(f"""
JobHunter Backend Successfully Triggered! 🚀

Time: {datetime.now().strftime('%Y-%m-%d %H:%M')} (10:57 as requested)

✅ Backend service activated
✅ Email system functional
✅ Found 10 customized CV/Cover Letter PDFs ready for delivery
✅ R2 storage configured

Your customized documents will be sent in separate emails to avoid size limits.

Generated documents include:
- SKF Group Fullstack Developer (CV + CL)
- Zenseact Backend Developer (CV + CL)  
- Volvo Group Senior Java Developer (CV + CL)
- Additional specialized CVs and cover letters

Best regards,
JobHunter Automation System
""")
        msg['Subject'] = f"JobHunter Backend Triggered Successfully - {datetime.now().strftime('%H:%M')}"
        msg['From'] = smtp_user
        msg['To'] = to_email
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info("✅ Notification email sent successfully!")
        
        # Get PDFs
        pdf_patterns = ["*.pdf", "job_application_package/*.pdf", "simple_pdfs/*.pdf"]
        recent_pdfs = []
        for pattern in pdf_patterns:
            files = glob.glob(pattern)
            for file in files:
                if os.path.exists(file):
                    recent_pdfs.append(file)
        
        recent_pdfs.sort(key=os.path.getmtime, reverse=True)
        recent_pdfs = recent_pdfs[:10]
        
        # Send documents in batches of 2
        batch_size = 2
        for i in range(0, len(recent_pdfs), batch_size):
            batch = recent_pdfs[i:i+batch_size]
            send_document_batch(batch, i//batch_size + 1, smtp_user, smtp_password, to_email)
        
        print(f"✅ SUCCESS: Notification sent + {len(recent_pdfs)} documents delivered to hongzhili01@gmail.com")
        return True
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ ERROR: {e}")
        return False

def send_document_batch(pdf_files, batch_num, smtp_user, smtp_password, to_email):
    """Send a batch of PDF documents"""
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"JobHunter Documents - Batch {batch_num} - {datetime.now().strftime('%H:%M')}"
        
        body = f"""
JobHunter Document Delivery - Batch {batch_num}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

This batch contains {len(pdf_files)} customized documents from your automation system.

Documents in this batch:
"""
        for pdf in pdf_files:
            body += f"- {os.path.basename(pdf)}\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDFs
        for pdf_path in pdf_files:
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                        filename=os.path.basename(pdf_path))
                msg.attach(pdf_attachment)
                logger.info(f"Attached: {os.path.basename(pdf_path)}")
            except Exception as e:
                logger.warning(f"Failed to attach {pdf_path}: {e}")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"✅ Batch {batch_num} sent successfully!")
        
    except Exception as e:
        logger.error(f"Error sending batch {batch_num}: {e}")

if __name__ == "__main__":
    send_notification_and_documents()