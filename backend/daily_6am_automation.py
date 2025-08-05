#!/usr/bin/env python3
"""
Daily 6 AM Job Automation
1. Scans real Gmail for job opportunities
2. Processes each job individually 
3. Sends focused application emails
"""
import os
import json
import subprocess
from datetime import datetime
from simple_real_job_collector import scan_gmail_for_real_jobs

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

def run_daily_automation():
    """Run complete daily job automation workflow"""
    print(f"🌅 Daily Job Automation Started - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Step 1: Scan real jobs from Gmail
    print("📧 Step 1: Scanning Gmail for real job opportunities...")
    real_jobs = scan_gmail_for_real_jobs(days_back=1)  # Yesterday's jobs
    
    if not real_jobs:
        print("ℹ️  No new jobs found in Gmail today")
        return True
    
    print(f"✅ Found {len(real_jobs)} real job opportunities")
    
    # Step 2: Process each job individually
    sent_count = 0
    failed_count = 0
    
    for i, job in enumerate(real_jobs, 1):
        print(f"\n🎯 Processing Job {i}/{len(real_jobs)}: {job['company']} - {job['title']}")
        print("-" * 50)
        
        try:
            # Create individual job application
            success = create_and_send_job_application(job)
            
            if success:
                sent_count += 1
                print(f"✅ SUCCESS: Application sent for {job['company']}")
            else:
                failed_count += 1
                print(f"❌ FAILED: Could not process {job['company']}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ ERROR processing {job['company']}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🎉 Daily Automation Complete - {datetime.now().strftime('%H:%M')}")
    print(f"📊 Results:")
    print(f"   📧 Jobs found: {len(real_jobs)}")
    print(f"   ✅ Successful applications: {sent_count}")
    print(f"   ❌ Failed applications: {failed_count}")
    
    if sent_count > 0:
        print(f"\n💌 {sent_count} personalized job applications sent to hongzhili01@gmail.com")
        print("📱 Check your email for individual job opportunities!")
    
    return sent_count > 0

def create_and_send_job_application(job):
    """Create personalized application for a specific job"""
    try:
        # Extract job details
        company = job['company']
        title = job['title']
        location = job['location']
        url = job['url']
        
        # Clean up title and company names
        if title == "Software Developer":
            title = f"Software Developer"
        if company == "Tech Company":
            company = extract_real_company_from_url(url)
        
        # Create individual email for this job
        email_content = create_job_email(company, title, location, url)
        
        # Send email using existing email system
        success = send_individual_job_email(email_content, company, title)
        
        return success
        
    except Exception as e:
        print(f"Error creating application: {e}")
        return False

def extract_real_company_from_url(url):
    """Extract real company name from job URL"""
    if "linkedin.com" in url:
        return "LinkedIn Job"
    elif "indeed.com" in url:
        if "devops" in url:
            return "DevOps Position"
        elif "azure" in url:
            return "Azure/Cloud Role"
        else:
            return "Indeed Job"
    else:
        return "Technology Company"

def create_job_email(company, title, location, url):
    """Create personalized email content for a job"""
    return f"""
🎯 REAL JOB OPPORTUNITY READY FOR APPLICATION
============================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your JobHunter system found a real job opportunity from your Gmail:

🏢 COMPANY: {company}
💼 POSITION: {title}
📍 LOCATION: {location}
🔗 APPLICATION LINK: {url}

📄 NEXT STEPS:
1. Click the application link above
2. This is a REAL job from your Gmail alerts
3. Apply directly through the link
4. The system will continue monitoring for more opportunities

💡 This job was automatically detected from your LinkedIn/Indeed email alerts.

🤖 JobHunter Real-Time Job Detection System
Generated from Gmail scan at 6:00 AM
"""

def send_individual_job_email(content, company, title):
    """Send individual email for job application"""
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        # Email configuration
        smtp_user = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        smtp_password = os.getenv("SMTP_PASSWORD")
        to_email = "hongzhili01@gmail.com"
        
        if not smtp_password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = f"🚨 REAL Job Alert: {title} at {company}"
        
        msg.attach(MIMEText(content, 'plain'))
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def setup_cron_job():
    """Show cron job setup instructions"""
    print("\n📅 CRON JOB SETUP FOR 6 AM DAILY AUTOMATION:")
    print("=" * 60)
    print("Add this to your crontab (run 'crontab -e'):")
    print("")
    print("# Daily job automation at 6:00 AM on weekdays")
    print("0 6 * * 1-5 cd /Users/bluehawana/Projects/Jobhunter/backend && python3 daily_6am_automation.py")
    print("")
    print("# Or test it every hour during work hours:")
    print("0 9-17 * * 1-5 cd /Users/bluehawana/Projects/Jobhunter/backend && python3 daily_6am_automation.py")
    print("")
    print("✅ This will:")
    print("   📧 Scan your Gmail for new job alerts")
    print("   🎯 Process each job individually")
    print("   📱 Send focused email alerts with real application links")
    print("   ⏰ Run automatically every weekday at 6 AM")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_cron_job()
    else:
        success = run_daily_automation()
        sys.exit(0 if success else 1)