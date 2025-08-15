#!/usr/bin/env python3
"""
06:00 Job Automation Execution - Complete Run
Uses anyrouter.top Claude API to scan Gmail, find jobs, and generate applications
Runs at 6:00 AM weekdays to deliver applications by 8:00 AM
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobAutomationRunner:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://anyrouter.top')
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'hongzhili01@gmail.com')
        
        self.execution_log = []
        self.jobs_found = []
        self.applications_sent = 0
        
    def log_action(self, action, status, details=""):
        """Log automation actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'status': status,
            'details': details
        }
        self.execution_log.append(log_entry)
        
        status_icon = "✅" if status == "SUCCESS" else "❌" if status == "ERROR" else "⏳"
        print(f"{status_icon} [{timestamp}] {action}: {details}")
    
    def scan_gmail_with_claude(self):
        """Scan REAL Gmail for actual job opportunities - NO FAKE JOBS"""
        self.log_action("Gmail Scanning", "RUNNING", "Scanning Gmail for REAL job opportunities...")
        
        try:
            # Import the simple Gmail scanner
            from simple_gmail_scanner import scan_real_gmail_jobs
            
            # Scan for real jobs in Gmail
            real_jobs = scan_real_gmail_jobs()
            
            if real_jobs:
                self.jobs_found = real_jobs
                self.log_action("Gmail Scanning", "SUCCESS", f"Found {len(real_jobs)} REAL job opportunities from Gmail")
                
                # Log each real job found
                for job in real_jobs:
                    self.log_action("Gmail Scanning", "SUCCESS", f"Real job: {job['company']} - {job['title']} in {job['location']}")
                
                return real_jobs
            else:
                self.log_action("Gmail Scanning", "INFO", "No new job opportunities found in Gmail today")
                return []
                
        except Exception as e:
            self.log_action("Gmail Scanning", "ERROR", f"Gmail scanning failed: {e}")
            # DO NOT use fallback fake jobs - return empty list instead
            return []
    
    def _no_fallback_jobs(self):
        """NO FALLBACK JOBS - Only process real opportunities"""
        self.log_action("Gmail Scanning", "INFO", "No fallback jobs - only processing real Gmail opportunities")
        return []
    
    def generate_application_REMOVED(self, job):
        """REMOVED: Old simple application generator - Use TRUE LEGO system only"""
        raise Exception("OLD SIMPLE GENERATORS REMOVED - Use TRUE LEGO automation system!")
    
    def _removed_simple_generator(self):
        """REMOVED: Simple generators deleted - only TRUE LEGO system allowed"""
        raise Exception("SIMPLE GENERATORS REMOVED - Use TRUE LEGO system only!")
    
    def send_application_email(self, job, cv_pdf, cover_letter_content):
        """Send application email"""
        company = job['company']
        title = job['title']
        
        self.log_action("Email Sending", "RUNNING", f"Sending application to {self.recipient_email}")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🎯 {company} {title} - Application Package Generated"
            
            # Email body
            body = f"""
🎯 JOB APPLICATION GENERATED - {company.upper()}

Dear Hongzhi,

Your automated job hunting system has generated a new application package!

📊 JOB DETAILS:
Company: {company}
Position: {title}
Location: {job.get('location', 'N/A')}

🎯 APPLICATION HIGHLIGHTS:
✅ LEGO Intelligence: Resume tailored for {title} role
✅ Enhanced CV: Prometheus/Grafana monitoring expertise featured
✅ Cross-cultural Communication: Cover letter adapted for {job.get('location', 'location')}
✅ Technical Focus: {job.get('requirements', 'Key requirements highlighted')}

📄 ATTACHMENTS:
• CV: Customized for {company} with relevant experience highlighted
• Cover Letter: Professional introduction with soft skills emphasis

🚀 READY FOR APPLICATION!

The documents are specifically tailored for this role with:
• Technical skills matching job requirements
• Current ECARX experience highlighted
• Infrastructure and monitoring expertise featured
• Professional presentation and formatting

---
Generated by JobHunter Automation System at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Next scan: Tomorrow 06:00 (weekdays only)
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach CV PDF
            if cv_pdf:
                cv_attachment = MIMEBase('application', 'octet-stream')
                cv_attachment.set_payload(cv_pdf)
                encoders.encode_base64(cv_attachment)
                cv_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CV_{company.replace(" ", "_")}_{title.replace(" ", "_")}.pdf"'
                )
                msg.attach(cv_attachment)
            
            # Attach Cover Letter as text file
            if cover_letter_content:
                cl_attachment = MIMEText(cover_letter_content)
                cl_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CoverLetter_{company.replace(" ", "_")}.txt"'
                )
                msg.attach(cl_attachment)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            self.applications_sent += 1
            self.log_action("Email Sending", "SUCCESS", f"Application sent for {company}")
            return True
            
        except Exception as e:
            self.log_action("Email Sending", "ERROR", f"Failed to send email for {company}: {e}")
            return False
    
    def send_application_email_with_both(self, job, cv_pdf, cl_pdf):
        """Send application email with BOTH CV and Cover Letter PDFs"""
        company = job['company']
        title = job['title']
        
        self.log_action("Email Sending", "RUNNING", f"Sending TRUE LEGO application to {self.recipient_email}")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🎯 {company} {title} - TRUE LEGO Application Package"
            
            # Email body
            body = f"""
🎯 TRUE LEGO JOB APPLICATION - {company.upper()}

Dear Hongzhi,

Your TRUE LEGO automation system has generated a professional application package!

📊 JOB DETAILS:
Company: {company}
Position: {title}
Location: {job.get('location', 'N/A')}

🎯 TRUE LEGO HIGHLIGHTS:
✅ EXACT LaTeX Templates: Your professional CV template with LEGO intelligence
✅ Matching Cover Letter: Same LaTeX style and formatting
✅ Claude 3.5 Customization: Intelligent content adaptation
✅ Overleaf Quality: Professional LaTeX compilation
✅ REAL Job Processing: No fake jobs, only genuine opportunities

📄 ATTACHMENTS:
• CV: Your exact LaTeX template with intelligent customization
• Cover Letter: Matching LaTeX style with soft skills emphasis

🚀 READY FOR APPLICATION!

The documents use your EXACT LaTeX templates with:
• Intelligent LEGO customization based on job requirements
• Professional formatting matching Overleaf quality
• Consistent styling between CV and cover letter
• Real job processing (no fake Spotify/Klarna jobs)

---
Generated by TRUE LEGO Automation System at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Next scan: Tomorrow 06:00 (weekdays only)
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach CV PDF
            if cv_pdf:
                cv_attachment = MIMEBase('application', 'octet-stream')
                cv_attachment.set_payload(cv_pdf)
                encoders.encode_base64(cv_attachment)
                cv_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CV_{company.replace(" ", "_")}_{title.replace(" ", "_")}.pdf"'
                )
                msg.attach(cv_attachment)
            
            # Attach Cover Letter PDF
            if cl_pdf:
                cl_attachment = MIMEBase('application', 'octet-stream')
                cl_attachment.set_payload(cl_pdf)
                encoders.encode_base64(cl_attachment)
                cl_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CoverLetter_{company.replace(" ", "_")}.pdf"'
                )
                msg.attach(cl_attachment)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            self.log_action("Email Sending", "SUCCESS", f"TRUE LEGO application sent for {company}")
            return True
            
        except Exception as e:
            self.log_action("Email Sending", "ERROR", f"Failed to send TRUE LEGO email for {company}: {e}")
            return False
    
    def send_daily_summary(self):
        """Send daily summary email"""
        self.log_action("Daily Summary", "RUNNING", "Preparing daily summary email")
        
        try:
            # Create summary message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"📊 Daily Job Automation Summary - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Summary body
            summary_body = f"""
📊 DAILY JOB AUTOMATION SUMMARY
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 EXECUTION RESULTS:
✅ Jobs Found: {len(self.jobs_found)}
✅ Applications Generated: {self.applications_sent}
✅ System Status: {'OPERATIONAL' if self.applications_sent > 0 else 'NO JOBS PROCESSED'}

📋 JOBS PROCESSED TODAY:
"""
            
            for i, job in enumerate(self.jobs_found, 1):
                summary_body += f"""
{i}. {job['company']} - {job['title']}
   Location: {job.get('location', 'N/A')}
   Status: {'✅ APPLICATION SENT' if i <= self.applications_sent else '⏳ PENDING'}
"""
            
            summary_body += f"""

🔧 SYSTEM LOG:
"""
            
            for log_entry in self.execution_log[-10:]:  # Last 10 entries
                status_icon = "✅" if log_entry['status'] == "SUCCESS" else "❌" if log_entry['status'] == "ERROR" else "⏳"
                summary_body += f"{status_icon} [{log_entry['timestamp']}] {log_entry['action']}: {log_entry['details']}\n"
            
            summary_body += f"""

🚀 NEXT EXECUTION: Next weekday 06:00

---
JobHunter Automation System
LEGO Intelligence Active | Overleaf Integration Ready
            """
            
            msg.attach(MIMEText(summary_body, 'plain'))
            
            # Send summary
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            self.log_action("Daily Summary", "SUCCESS", "Summary email sent")
            return True
            
        except Exception as e:
            self.log_action("Daily Summary", "ERROR", f"Failed to send summary: {e}")
            return False
    
    async def run_automation(self):
        """Run complete automation workflow"""
        print("🎯 06:00 JOB AUTOMATION EXECUTION - TRUE LEGO SYSTEM")
        print("=" * 60)
        print(f"🕐 Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 Using TRUE LEGO Templates with Claude Intelligence")
        print("=" * 60)
        
        # Step 1: Scan Gmail for REAL jobs only
        jobs = self.scan_gmail_with_claude()
        
        if not jobs:
            self.log_action("Automation", "INFO", "No new job opportunities found in Gmail today - this is normal")
            self.send_daily_summary()  # Still send summary even if no jobs
            return
        
        # Step 2: Process each job using TRUE LEGO system
        for job in jobs[:2]:  # Process first 2 jobs to avoid spam
            try:
                # Use WORKING LEGO systems
                from beautiful_pdf_generator import create_beautiful_multi_page_pdf
                from exact_cover_letter_generator import create_exact_cover_letter
                
                # Generate CV using LEGO intelligence
                cv_pdf = create_beautiful_multi_page_pdf(job)
                
                # Generate Cover Letter using exact LaTeX template
                cl_result = create_exact_cover_letter(job)
                cl_pdf = cl_result.get('pdf_content', b'')
                
                if cv_pdf and cl_pdf:
                    # Step 3: Send application with BOTH CV and Cover Letter
                    self.send_application_email_with_both(job, cv_pdf, cl_pdf)
                    self.applications_sent += 1
                    self.log_action("Application Complete", "SUCCESS", f"LEGO application sent for {job['company']}")
                else:
                    self.log_action("Application Generation", "ERROR", f"PDF generation failed for {job['company']}")
                
                # Small delay between applications
                time.sleep(2)
                
            except Exception as e:
                self.log_action("Application Processing", "ERROR", f"Failed for {job.get('company', 'Unknown')}: {e}")
                continue
        
        # Step 4: Send daily summary
        self.send_daily_summary()
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 AUTOMATION EXECUTION COMPLETE")
        print("=" * 60)
        print(f"🎯 Jobs Found: {len(self.jobs_found)}")
        print(f"📧 Applications Sent: {self.applications_sent}")
        print(f"⏰ Execution Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"📧 Check your email: {self.recipient_email}")
        
        if self.applications_sent > 0:
            print(f"\n🎉 SUCCESS! {self.applications_sent} applications sent!")
        else:
            print(f"\n⚠️ No applications sent - check logs above")

async def main():
    """Main execution function"""
    runner = JobAutomationRunner()
    await runner.run_automation()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())