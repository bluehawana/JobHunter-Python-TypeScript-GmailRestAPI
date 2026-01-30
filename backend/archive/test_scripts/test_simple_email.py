#!/usr/bin/env python3
"""
Simple email test without attachments
"""
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_simple_email():
    try:
        smtp_user = os.getenv("SMTP_USER", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set")
            print("❌ SMTP_PASSWORD environment variable not set")
            return False
        to_email = "hongzhili01@gmail.com"
        
        # Create simple message
        msg = MIMEText(f"Test email from JobHunter system at {datetime.now()}")
        msg['Subject'] = "JobHunter Email Test"
        msg['From'] = smtp_user
        msg['To'] = to_email
        
        # Send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Simple email test successful!")
        return True
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    test_simple_email()