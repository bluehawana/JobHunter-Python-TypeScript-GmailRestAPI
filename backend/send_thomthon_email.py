#!/usr/bin/env python3
"""
Send Thomthon Retuer PDFs via email with proper SMTP configuration
"""
import smtplib
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_thomthon_pdfs():
    """Send the generated Thomthon Retuer PDFs via email"""
    
    # Email configuration from .env
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "bluehawana@gmail.com"
    sender_password = "bazjdenzzsvtjatr"
    recipient_email = "leeharvad@gmail.com"
    
    # Check if PDF files exist
    cv_pdf = "thomthon_retuer_cv.pdf"
    cl_pdf = "thomthon_retuer_cover_letter.pdf"
    
    if not Path(cv_pdf).exists() or not Path(cl_pdf).exists():
        print("❌ PDF files not found. Please run generate_thomthon_pdfs.py first")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "✅ Thomthon Retuer Application Ready - PDF Resume & Cover Letter"
        
        # Email body
        body = f"""Hi!

🎉 Your application documents for Thomthon Retuer are ready!

📎 Files attached:
  ✅ Resume (PDF) - Ready to send directly to employers
  ✅ Cover Letter (PDF) - Ready to send directly to employers

📋 Application Details:
🏢 Company: Thomthon Retuer
💼 Position: Solution Developer
🎯 Role Focus: DevOps/Infrastructure
📍 Location: Sweden

🚀 READY TO SEND:
These PDFs are professionally formatted and ready for immediate use. You can send them directly to Thomthon Retuer without any additional editing.

📊 Content Summary:
• CV: 3-page professional format highlighting DevOps expertise, infrastructure optimization, and Kubernetes experience
• Cover Letter: Tailored for Solution Developer role with emphasis on technical leadership and automation skills
• Both documents optimized for ATS compatibility and professional presentation

💼 Your background perfectly matches their requirements:
- 5+ years of infrastructure automation experience
- Current IT/Infrastructure Specialist role at ECARX
- Kubernetes migration and cost optimization projects
- Spring Boot, microservices, and cloud platforms expertise

🔧 LinkedIn Jobs Automation:
Your system is configured to automatically process saved LinkedIn jobs tomorrow at 6am UTC via Heroku scheduler.

Best regards,
JobHunter Automation System"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDFs
        attachments = [
            (cv_pdf, "Thomthon_Retuer_Resume_Hongzhi_Li.pdf"),
            (cl_pdf, "Thomthon_Retuer_CoverLetter_Hongzhi_Li.pdf")
        ]
        
        for file_path, filename in attachments:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)
        
        # Send email
        print("📧 Sending email with Thomthon Retuer PDFs...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}")
        print(f"📎 Attached: {len(attachments)} PDF files")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

def main():
    """Send Thomthon Retuer application PDFs"""
    print("🎯 Sending Thomthon Retuer Application PDFs")
    print("=" * 50)
    
    success = send_thomthon_pdfs()
    
    if success:
        print("\n🎉 SUCCESS! Check leeharvad@gmail.com for your application documents")
        print("📋 You can now send these PDFs directly to Thomthon Retuer")
    else:
        print("\n❌ Failed to send email")

if __name__ == "__main__":
    main()