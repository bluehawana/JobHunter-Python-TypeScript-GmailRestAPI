#!/usr/bin/env python3
"""
Simple test to send existing CV and cover letter PDFs to leeharvad@gmail.com
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_test_email():
    """Send test email with existing PDFs"""
    
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "bluehawanan@gmail.com"
    password = os.getenv('SMTP_PASSWORD')
    recipient_email = "leeharvad@gmail.com"
    
    if not password:
        print("❌ SMTP_PASSWORD environment variable not set")
        print("💡 Set it with: export SMTP_PASSWORD='your_gmail_app_password'")
        return False
    
    # Find the new properly formatted PDFs
    target_pdfs = ["hongzhi_devops_cv.pdf", "hongzhi_devops_opera.pdf"]
    pdf_files = []
    
    for pdf_name in target_pdfs:
        if Path(pdf_name).exists():
            pdf_files.append(Path(pdf_name))
    
    if not pdf_files:
        print("❌ No properly formatted PDF files found")
        print("💡 Run: python3 create_basic_cv.py && python3 create_simple_pdfs.py")
        return False
    
    print(f"📎 Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"   • {pdf.name}")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "JobHunter Application: Hongzhi Li - DevOps Engineer"
    
    # Email body
    body = f"""
Hi,

This is a test email from the JobHunter automation system.

📋 Test Purpose: Verify email delivery during working days
🎯 Target: leeharvad@gmail.com
📊 Documents: {len(pdf_files)} PDF files attached

📎 Attachments:
"""
    
    for pdf in pdf_files:
        body += f"   • {pdf.name}\n"
    
    body += """
✅ If you receive this email, the automation is working correctly!

Best regards,
JobHunter Automation System
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDFs
    for pdf_file in pdf_files:
        try:
            with open(pdf_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {pdf_file.name}'
            )
            msg.attach(part)
            print(f"✅ Attached: {pdf_file.name}")
        except Exception as e:
            print(f"❌ Failed to attach {pdf_file.name}: {e}")
    
    # Send email
    try:
        print("\n📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        
        print("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("🎉 SUCCESS! Test email sent to leeharvad@gmail.com")
        print(f"📎 {len(pdf_files)} PDF documents attached")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

if __name__ == "__main__":
    print("📧 JobHunter Email Test")
    print("=" * 40)
    print("🎯 Sending test email to leeharvad@gmail.com")
    print()
    
    success = send_test_email()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("📧 Check your inbox at leeharvad@gmail.com")
    else:
        print("\n❌ Test failed - check configuration")