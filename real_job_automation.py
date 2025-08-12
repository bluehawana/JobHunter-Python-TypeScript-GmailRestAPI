#!/usr/bin/env python3
"""
Real Job Automation - Only processes REAL jobs from Gmail in Gothenburg area
Uses exact LaTeX cover letter template and highlights soft skills
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealJobAutomation:
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
        self.recipient_email = 'hongzhili01@gmail.com'
        
        self.execution_log = []
        self.real_jobs_found = []
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
    
    def scan_real_jobs(self):
        """Scan Gmail for REAL jobs in Gothenburg area only"""
        self.log_action("Real Job Scanning", "RUNNING", "Scanning Gmail for real opportunities in Gothenburg area...")
        
        try:
            from real_job_scanner import scan_for_real_jobs
            
            real_jobs = scan_for_real_jobs()
            
            if real_jobs:
                self.real_jobs_found = real_jobs
                self.log_action("Real Job Scanning", "SUCCESS", f"Found {len(real_jobs)} REAL jobs in Gothenburg area")
                
                # Log each job found
                for job in real_jobs:
                    self.log_action("Job Found", "INFO", f"{job['company']} - {job['title']} in {job['location']}")
                
                return real_jobs
            else:
                self.log_action("Real Job Scanning", "INFO", "No new real jobs found in Gmail today")
                return []
                
        except Exception as e:
            self.log_action("Real Job Scanning", "ERROR", f"Gmail scanning failed: {e}")
            return []
    
    def generate_application_package(self, job):
        """Generate CV and exact cover letter for real job"""
        company = job['company']
        title = job['title']
        
        self.log_action("Application Generation", "RUNNING", f"Generating for {company} - {title}")
        
        try:
            # Generate enhanced CV
            from beautiful_pdf_generator import create_beautiful_multi_page_pdf
            cv_pdf = create_beautiful_multi_page_pdf(job)
            
            if not cv_pdf:
                self.log_action("CV Generation", "ERROR", f"Failed to generate CV for {company}")
                return None, None, None
            
            self.log_action("CV Generation", "SUCCESS", f"Enhanced CV generated ({len(cv_pdf):,} bytes)")
            
            # Generate EXACT cover letter using your template
            from exact_cover_letter_generator import create_exact_cover_letter
            cl_result = create_exact_cover_letter(job)
            
            if not cl_result['success']:
                self.log_action("Cover Letter Generation", "ERROR", f"Failed to generate cover letter for {company}")
                return cv_pdf, None, None
            
            self.log_action("Cover Letter Generation", "SUCCESS", 
                          f"Exact LaTeX cover letter generated ({cl_result['pdf_size']:,} bytes)")
            
            return cv_pdf, cl_result['pdf_content'], cl_result['latex_content']
            
        except Exception as e:
            self.log_action("Application Generation", "ERROR", f"Failed for {company}: {e}")
            return None, None, None
    
    def send_real_application_email(self, job, cv_pdf, cl_pdf, cl_latex):
        """Send application email for real job"""
        company = job['company']
        title = job['title']
        location = job['location']
        
        self.log_action("Email Sending", "RUNNING", f"Sending REAL application to {self.recipient_email}")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🎯 REAL JOB: {company} {title} - Gothenburg Application Package"
            
            # Email body
            body = f"""
🎯 REAL JOB APPLICATION GENERATED - {company.upper()}

Dear Hongzhi,

Your job automation system found a REAL job opportunity in the Gothenburg area and generated a complete application package!

📊 REAL JOB DETAILS:
Company: {company}
Position: {title}
Location: {location}
Source: Gmail (Real job posting)
Found: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 APPLICATION HIGHLIGHTS:
✅ LEGO Intelligence: Resume tailored specifically for {title} role
✅ Enhanced CV: Prometheus/Grafana monitoring expertise featured
✅ EXACT Cover Letter: Uses your precise LaTeX template with company info
✅ Soft Skills Focus: Cross-cultural communication and team collaboration highlighted
✅ Gothenburg Focus: Application tailored for local market

📄 ATTACHMENTS:
• Enhanced CV: Customized with LEGO intelligence for {company}
• Exact Cover Letter PDF: Professional LaTeX formatting with soft skills
• Cover Letter LaTeX: Source code for manual editing if needed

🎯 COVER LETTER HIGHLIGHTS (Not heavily featured in CV):
• Cross-cultural communication skills (Swedish/International environments)
• Team coaching and mentoring capabilities
• Bridge between technical teams and business stakeholders
• Multi-team collaboration and integration expertise
• Proactive problem-solving and results-driven approach

🚀 READY FOR REAL APPLICATION!

This is a GENUINE job opportunity found in your Gmail, specifically in the Gothenburg area as requested. The application materials are professionally crafted and ready for submission.

Next Steps:
1. Review the application materials
2. Submit directly to {company}
3. Follow up as appropriate

---
Generated by Real Job Automation System
Only processes genuine opportunities in Gothenburg area
Next scan: Tomorrow 20:00
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach Enhanced CV PDF
            if cv_pdf:
                cv_attachment = MIMEBase('application', 'octet-stream')
                cv_attachment.set_payload(cv_pdf)
                encoders.encode_base64(cv_attachment)
                cv_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_Enhanced_CV_{company.replace(" ", "_")}_{title.replace(" ", "_")}.pdf"'
                )
                msg.attach(cv_attachment)
            
            # Attach Exact Cover Letter PDF
            if cl_pdf:
                cl_attachment = MIMEBase('application', 'octet-stream')
                cl_attachment.set_payload(cl_pdf)
                encoders.encode_base64(cl_attachment)
                cl_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CoverLetter_{company.replace(" ", "_")}_LaTeX.pdf"'
                )
                msg.attach(cl_attachment)
            
            # Attach LaTeX source for manual editing
            if cl_latex:
                latex_attachment = MIMEText(cl_latex)
                latex_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Hongzhi_Li_CoverLetter_{company.replace(" ", "_")}.tex"'
                )
                msg.attach(latex_attachment)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            self.applications_sent += 1
            self.log_action("Email Sending", "SUCCESS", f"REAL application sent for {company}")
            return True
            
        except Exception as e:
            self.log_action("Email Sending", "ERROR", f"Failed to send email for {company}: {e}")
            return False
    
    def send_real_job_summary(self):
        """Send summary of real job processing"""
        self.log_action("Daily Summary", "RUNNING", "Preparing real job summary")
        
        try:
            # Create summary message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"📊 Real Job Automation Summary - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Summary body
            summary_body = f"""
📊 REAL JOB AUTOMATION SUMMARY
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 EXECUTION RESULTS:
✅ Real Jobs Found: {len(self.real_jobs_found)} (Gothenburg area only)
✅ Applications Generated: {self.applications_sent}
✅ System Status: {'OPERATIONAL - REAL JOBS PROCESSED' if self.applications_sent > 0 else 'NO REAL JOBS FOUND TODAY'}

📋 REAL JOBS PROCESSED TODAY:
"""
            
            if self.real_jobs_found:
                for i, job in enumerate(self.real_jobs_found, 1):
                    summary_body += f"""
{i}. {job['company']} - {job['title']}
   Location: {job['location']}
   Source: Gmail (Real posting)
   Status: {'✅ APPLICATION SENT' if i <= self.applications_sent else '⏳ PENDING'}
"""
            else:
                summary_body += "\nNo real job opportunities found in Gmail today.\n"
            
            summary_body += f"""

🔧 SYSTEM CONFIGURATION:
✅ Location Filter: Gothenburg + 20km radius ONLY
✅ Job Source: Real Gmail scanning (No fake jobs)
✅ Cover Letter: Exact LaTeX template with soft skills
✅ CV Enhancement: LEGO intelligence with monitoring expertise

🔧 SYSTEM LOG:
"""
            
            for log_entry in self.execution_log[-15:]:  # Last 15 entries
                status_icon = "✅" if log_entry['status'] == "SUCCESS" else "❌" if log_entry['status'] == "ERROR" else "⏳"
                summary_body += f"{status_icon} [{log_entry['timestamp']}] {log_entry['action']}: {log_entry['details']}\n"
            
            summary_body += f"""

🚀 NEXT EXECUTION: Tomorrow 20:00
📧 Only real jobs in Gothenburg area will be processed

---
Real Job Automation System
✅ No fake jobs | ✅ Gothenburg focus | ✅ Exact LaTeX templates
            """
            
            msg.attach(MIMEText(summary_body, 'plain'))
            
            # Send summary
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)
            server.quit()
            
            self.log_action("Daily Summary", "SUCCESS", "Real job summary sent")
            return True
            
        except Exception as e:
            self.log_action("Daily Summary", "ERROR", f"Failed to send summary: {e}")
            return False
    
    def run_real_job_automation(self):
        """Run complete real job automation"""
        print("🎯 REAL JOB AUTOMATION - GOTHENBURG AREA ONLY")
        print("=" * 60)
        print(f"🕐 Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 Location Filter: Gothenburg + 20km radius")
        print(f"📧 Source: Real Gmail scanning only")
        print("=" * 60)
        
        # Step 1: Scan for REAL jobs in Gothenburg area
        real_jobs = self.scan_real_jobs()
        
        if not real_jobs:
            self.log_action("Automation", "INFO", "No real jobs found today - sending summary")
            self.send_real_job_summary()
            return
        
        # Step 2: Process each REAL job
        for job in real_jobs[:3]:  # Process max 3 jobs to avoid spam
            cv_pdf, cl_pdf, cl_latex = self.generate_application_package(job)
            
            if cv_pdf and cl_pdf:
                # Step 3: Send application for REAL job
                self.send_real_application_email(job, cv_pdf, cl_pdf, cl_latex)
                
                # Small delay between applications
                time.sleep(3)
        
        # Step 4: Send summary
        self.send_real_job_summary()
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 REAL JOB AUTOMATION COMPLETE")
        print("=" * 60)
        print(f"🎯 Real Jobs Found: {len(self.real_jobs_found)}")
        print(f"📧 Applications Sent: {self.applications_sent}")
        print(f"📍 Location: Gothenburg area only")
        print(f"📧 Check your email: {self.recipient_email}")
        
        if self.applications_sent > 0:
            print(f"\n🎉 SUCCESS! {self.applications_sent} REAL applications sent!")
            print(f"✅ All jobs are genuine opportunities from your Gmail")
            print(f"✅ All applications use exact LaTeX cover letter template")
            print(f"✅ All jobs are in Gothenburg area as requested")
        else:
            print(f"\n📧 No real jobs found in Gmail today")
            print(f"💡 System will continue scanning tomorrow at 20:00")

def main():
    """Main execution function"""
    automation = RealJobAutomation()
    automation.run_real_job_automation()

if __name__ == "__main__":
    main()