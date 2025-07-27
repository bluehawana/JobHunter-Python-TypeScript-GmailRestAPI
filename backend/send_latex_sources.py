#!/usr/bin/env python3
"""
Send LaTeX source files for manual review and compilation
"""
import asyncio
import os
import smtplib
import re
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Import the smart editor
import sys
sys.path.append(str(Path(__file__).parent))
from smart_latex_editor import SmartLaTeXEditor

async def send_latex_only():
    """Send only LaTeX source files for review"""
    editor = SmartLaTeXEditor()
    
    # Test jobs
    test_jobs = [
        ("Solution Developer", "Volvo Group", "Onsite Infrastructure Demand & Automation", "Sven Erikssons gata 7", "41755 Göteborg"),
        ("DevOps Engineer", "Spotify", "Infrastructure Team", "", "Stockholm"),
        ("Senior Backend Developer", "SKF Group", "Software Development", "", "Gothenburg")
    ]
    
    print("📧 Sending LaTeX Source Files for Manual Review")
    print("=" * 60)
    
    for job_title, company, department, address, city in test_jobs:
        print(f"\\n📋 Processing: {job_title} at {company}")
        
        role_focus = editor.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        # Make targeted edits
        cv_content = editor.edit_cv_for_job(job_title, company, role_focus)
        cl_content = editor.edit_cover_letter_for_job(job_title, company, department, address, city)
        
        # Save LaTeX files
        cv_tex, cl_tex = editor.save_latex_files(cv_content, cl_content, job_title, company)
        
        if cv_tex and cl_tex:
            print(f"💾 LaTeX files saved: {cv_tex}, {cl_tex}")
            
            # Send email with just LaTeX files
            success = send_latex_review_email(editor, job_title, company, cv_tex, cl_tex, role_focus)
            
            if success:
                print(f"🎉 SUCCESS: LaTeX source files sent for review!")
            else:
                print(f"❌ FAILED: Email not sent")
        
        await asyncio.sleep(1)
    
    print(f"\\n📧 Check {editor.recipient_email} for LaTeX source files!")
    print("🔨 Compile manually with: pdflatex filename.tex")

def send_latex_review_email(editor, job_title, company, cv_tex, cl_tex, role_focus):
    """Send email with LaTeX source files only"""
    
    if not editor.password:
        print("❌ SMTP_PASSWORD not set")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = editor.sender_email
        msg['To'] = editor.recipient_email
        msg['Subject'] = f"JobHunter LaTeX Sources: {job_title} at {company} - Ready for Review"
        
        body = f"""Hi,

LaTeX source files ready for your review and manual compilation:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Tailoring: {role_focus.title()} focus
📍 Priority: {'🏢 Gothenburg' if 'gothenburg' in company.lower() or 'volvo' in company.lower() else '🌐 Remote/Other'}

📎 LaTeX source files attached:
   • CV (LaTeX) - Your original template with targeted edits
   • Cover Letter (LaTeX) - Your original template with targeted edits

✏️  Smart edits made:
   ✅ Job title updated to: {job_title}
   ✅ Profile summary tailored for {role_focus} role
   ✅ Cover letter content customized for {company}
   ✅ Company information and contact details updated
   ✅ Hard/soft skills emphasized for this role type
   ✅ All original formatting and structure preserved

🔨 To compile to PDF:
   1. Download the .tex files
   2. Run: pdflatex filename.tex
   3. Run again: pdflatex filename.tex (for references)
   4. Check the generated PDF files

📋 Your original templates used as base - only necessary changes made.

If compilation fails, you may need to install missing LaTeX packages.
All edits are clearly marked and minimal to preserve your formatting.

Best regards,
Smart LaTeX Editor
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach LaTeX files
        attachments = [
            (cv_tex, f"CV_{company}_{job_title}_TAILORED.tex"),
            (cl_tex, f"CoverLetter_{company}_{job_title}_TAILORED.tex")
        ]
        
        for file_path, filename in attachments:
            if file_path and Path(file_path).exists():
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(editor.smtp_server, editor.smtp_port)
        server.starttls()
        server.login(editor.sender_email, editor.password)
        server.sendmail(editor.sender_email, editor.recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ LaTeX source files sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(send_latex_only())