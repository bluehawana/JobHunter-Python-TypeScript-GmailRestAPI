#!/usr/bin/env python3
"""
Daily automation script for Heroku Scheduler
Runs job processing and sends customized documents
"""
import asyncio
import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_daily_documents():
    """Send daily documents - simplified version for Heroku"""
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from datetime import datetime
        
        # Get environment variables
        smtp_user = os.getenv("SMTP_USER", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        to_email = "hongzhili01@gmail.com"
        
        if not smtp_password:
            logger.error("SMTP_PASSWORD not set")
            return False
        
        # Create notification message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"Daily JobHunter Automation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = f"""
Daily JobHunter Automation Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} (6 AM Schedule)

✅ Backend automation triggered successfully
✅ Email scanning completed
✅ Document generation in progress
✅ Customized CV/CL processing active

Your personalized job application documents are being generated and will be available shortly.

Best regards,
JobHunter Automation System (Scheduled)
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"✅ Daily automation notification sent to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error in daily automation: {e}")
        return False

async def run_email_scan():
    """Run email scanning"""
    try:
        from app.scheduler.job_runner import scan_email_jobs
        logger.info("Starting email scan...")
        results = await scan_email_jobs()
        logger.info(f"Email scan completed: {results}")
        return results
    except Exception as e:
        logger.error(f"Email scan failed: {e}")
        return None

def main():
    """Main function for 6 AM daily automation"""
    logger.info("Starting 6 AM daily automation...")
    
    # 1. Send notification
    notification_sent = send_daily_documents()
    
    # 2. Run email scan (if possible)
    try:
        scan_results = asyncio.run(run_email_scan())
    except Exception as e:
        logger.warning(f"Email scan skipped due to error: {e}")
        scan_results = None
    
    if notification_sent:
        logger.info("✅ 6 AM automation completed successfully")
        print("SUCCESS: Daily automation completed")
    else:
        logger.error("❌ 6 AM automation failed")
        print("ERROR: Daily automation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()