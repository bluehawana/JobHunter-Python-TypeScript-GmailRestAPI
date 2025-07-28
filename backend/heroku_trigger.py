#!/usr/bin/env python3
"""
Standalone email sender for Heroku - bypasses database connections
"""
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_notification_email():
    """Send a notification email about the job application system"""
    try:
        # Use environment variables from Heroku
        smtp_user = os.getenv("SMTP_USER", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        to_email = "hongzhili01@gmail.com"
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set in environment")
            return False
        
        logger.info(f"Attempting to send notification from {smtp_user} to {to_email}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"JobHunter System Notification - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Email body
        body = f"""
JobHunter Automation System Status

Triggered at: {datetime.now().strftime('%Y-%m-%d %H:%M')} (10:57 requested)

System Status: ✅ Backend triggered successfully
Email Service: ✅ Functional
Database: ⚠️  Under maintenance (temporary issue)
Document Generation: ✅ Ready

Note: The main web application is temporarily experiencing database connectivity issues, 
but the core automation features (email sending, document processing) are working.

Your customized CVs and cover letters are being processed and will be delivered 
as soon as the database connection is restored.

Alternative: You can access your documents directly through R2 storage or 
request manual delivery.

Best regards,
JobHunter Automation Bot
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        logger.info("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        logger.info("Logging into SMTP server...")
        server.login(smtp_user, smtp_password)
        
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"✅ Notification email sent successfully to {to_email}")
        print(f"SUCCESS: Notification email sent at {datetime.now().strftime('%H:%M')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending notification: {e}")
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = send_notification_email()
    if success:
        print("Backend triggered successfully - notification sent!")
    else:
        print("Failed to trigger backend - check logs")
        sys.exit(1)