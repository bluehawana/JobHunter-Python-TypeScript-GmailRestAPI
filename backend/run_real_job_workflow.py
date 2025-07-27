#!/usr/bin/env python3
"""
Run JobHunter workflow with real data sources
"""
import asyncio
import sys
import os
import imaplib
import email
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Import our priority processor
from priority_job_processor import PriorityJobProcessor

class RealJobFetcher:
    def __init__(self):
        self.processor = PriorityJobProcessor()
        self.smtp_user = "bluehawanan@gmail.com"  # Your email for scanning
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        
    async def scan_gmail_for_jobs(self, days_back: int = 7) -> List[Dict]:
        """Scan bluehawana@gmail.com for LinkedIn and Indeed job emails"""
        print(f"📧 Scanning bluehawanan@gmail.com for job emails (last {days_back} days)...")
        
        if not self.smtp_password:
            print("❌ SMTP_PASSWORD not set for Gmail scanning")
            return []
        
        jobs = []
        
        try:
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(self.smtp_user, self.smtp_password)
            mail.select('inbox')
            
            # Calculate date filter
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Search for LinkedIn job emails
            print("   🔍 Searching for LinkedIn job emails...")
            linkedin_search = f'(FROM "linkedin" OR FROM "linkedin.com" OR SUBJECT "job" OR SUBJECT "opportunity") SINCE {since_date}'
            result, messages = mail.search(None, linkedin_search)
            
            if result == 'OK':
                for msg_id in messages[0].split()[-5:]:  # Get last 5 LinkedIn emails
                    result, msg_data = mail.fetch(msg_id, '(RFC822)')
                    if result == 'OK':
                        job = self._parse_linkedin_email(msg_data[0][1])
                        if job:
                            jobs.append(job)
            
            # Search for Indeed job emails
            print("   🔍 Searching for Indeed job emails...")
            indeed_search = f'(FROM "indeed" OR FROM "indeed.com" OR FROM "noreply@indeed.com") SINCE {since_date}'
            result, messages = mail.search(None, indeed_search)
            
            if result == 'OK':
                for msg_id in messages[0].split()[-5:]:  # Get last 5 Indeed emails
                    result, msg_data = mail.fetch(msg_id, '(RFC822)')
                    if result == 'OK':
                        job = self._parse_indeed_email(msg_data[0][1])
                        if job:
                            jobs.append(job)
            
            mail.logout()
            print(f"   ✅ Found {len(jobs)} jobs from email scanning")
            
        except Exception as e:
            print(f"   ❌ Gmail scanning error: {e}")
        
        return jobs
    
    def _parse_linkedin_email(self, raw_email) -> Dict:
        """Parse LinkedIn job email"""
        try:
            msg = email.message_from_bytes(raw_email)
            subject = msg['subject'] or ''
            
            # Get email body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Extract job info from LinkedIn email format
            title_match = re.search(r'(?:Job:|Position:|Role:)\s*(.+?)(?:\n|at)', body, re.IGNORECASE)
            company_match = re.search(r'(?:at|company:)\s*(.+?)(?:\n|location)', body, re.IGNORECASE)
            location_match = re.search(r'(?:location:|in)\s*(.+?)(?:\n|$)', body, re.IGNORECASE)
            
            if title_match:
                return {
                    'title': title_match.group(1).strip(),
                    'company': company_match.group(1).strip() if company_match else 'LinkedIn Company',
                    'location': location_match.group(1).strip() if location_match else 'Not specified',
                    'description': body[:500],  # First 500 chars
                    'url': 'https://linkedin.com/jobs',
                    'source': 'bluehawana_email_linkedin',
                    'job_type': 'fulltime'
                }
        except:
            pass
        return None
    
    def _parse_indeed_email(self, raw_email) -> Dict:
        """Parse Indeed job email"""
        try:
            msg = email.message_from_bytes(raw_email)
            subject = msg['subject'] or ''
            
            # Get email body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Extract job info from Indeed email format
            title_match = re.search(r'(?:Job:|Position:)\s*(.+?)(?:\n|at)', body, re.IGNORECASE)
            company_match = re.search(r'(?:at|Company:)\s*(.+?)(?:\n|location)', body, re.IGNORECASE)
            location_match = re.search(r'(?:Location:|in)\s*(.+?)(?:\n|$)', body, re.IGNORECASE)
            
            if title_match:
                return {
                    'title': title_match.group(1).strip(),
                    'company': company_match.group(1).strip() if company_match else 'Indeed Company',
                    'location': location_match.group(1).strip() if location_match else 'Not specified',
                    'description': body[:500],
                    'url': 'https://indeed.com',
                    'source': 'bluehawana_email_indeed',
                    'job_type': 'fulltime'
                }
        except:
            pass
        return None
    
    async def get_linkedin_saved_jobs(self) -> List[Dict]:
        """Get LinkedIn saved jobs (placeholder for now)"""
        print("📋 Getting LinkedIn saved jobs...")
        
        # Mock saved jobs that would come from LinkedIn API or saved jobs import
        saved_jobs = [
            {
                'title': 'Senior Backend Developer',
                'company': 'Ericsson',
                'location': 'Gothenburg, Sweden',
                'description': 'Join our 5G network development team building next-generation telecommunications infrastructure.',
                'url': 'https://careers.ericsson.com/backend-developer',
                'source': 'linkedin_saved',
                'job_type': 'fulltime'
            },
            {
                'title': 'Cloud Engineer',
                'company': 'Hasselblad',
                'location': 'Gothenburg, Sweden', 
                'description': 'Work on cloud infrastructure for our camera and imaging systems.',
                'url': 'https://careers.hasselblad.com/cloud-engineer',
                'source': 'linkedin_saved',
                'job_type': 'fulltime'
            },
            {
                'title': 'Software Engineer',
                'company': 'Netflix',
                'location': 'Remote (Europe)',
                'description': 'Build entertainment platforms used by millions worldwide.',
                'url': 'https://careers.netflix.com/software-engineer',
                'source': 'linkedin_saved',
                'job_type': 'remote'
            }
        ]
        
        print(f"   ✅ Found {len(saved_jobs)} saved jobs")
        return saved_jobs
    
    async def get_all_real_jobs(self) -> List[Dict]:
        """Get jobs from all real sources following priority order"""
        all_jobs = []
        
        print("🚀 Fetching jobs from real sources...")
        print("=" * 50)
        
        # Priority 1: Gmail scanning
        gmail_jobs = await self.scan_gmail_for_jobs(days_back=7)
        all_jobs.extend(gmail_jobs)
        
        # Priority 2: LinkedIn saved jobs
        linkedin_jobs = await self.get_linkedin_saved_jobs()
        all_jobs.extend(linkedin_jobs)
        
        print(f"\n📊 Total jobs from real sources: {len(all_jobs)}")
        return all_jobs

async def main():
    """Main workflow with real data"""
    fetcher = RealJobFetcher()
    processor = PriorityJobProcessor()
    
    print("🎯 JobHunter Real Data Workflow")
    print("=" * 60)
    print("📧 Scanning: bluehawanan@gmail.com")
    print("🎯 Priorities: Gothenburg > Remote (famous IT only)")
    print()
    
    # Get real jobs
    all_jobs = await fetcher.get_all_real_jobs()
    
    if not all_jobs:
        print("❌ No jobs found from real sources")
        print("💡 Make sure SMTP_PASSWORD is set and you have job emails")
        return
    
    # Filter and prioritize
    print("\n🔍 Filtering and prioritizing jobs...")
    prioritized_jobs = processor.filter_and_prioritize_jobs(all_jobs)
    
    print(f"✅ {len(prioritized_jobs)} jobs match your criteria")
    
    if not prioritized_jobs:
        print("❌ No jobs match your criteria (Gothenburg or Remote+Famous IT)")
        return
    
    print("\n📋 Top Priority Jobs:")
    for i, job in enumerate(prioritized_jobs[:5], 1):
        location_type = "🏢 Gothenburg" if processor.is_gothenburg_relevant(job['location']) else f"🌐 {job['location']}"
        print(f"   {i}. {job['title']} at {job['company']} ({location_type})")
        print(f"      Source: {job['source']}")
    
    # Process top jobs
    max_applications = min(3, len(prioritized_jobs))
    print(f"\n🔄 Processing top {max_applications} priority jobs...")
    
    successful = 0
    
    for i, job in enumerate(prioritized_jobs[:max_applications], 1):
        print(f"\n📋 Processing {i}/{max_applications}: {job['title']} at {job['company']}")
        
        role_focus = processor.determine_role_focus(job['title'])
        
        # Generate and send application
        cv_content = processor.create_tailored_cv(job['title'], job['company'], role_focus)
        cv_pdf = processor.compile_latex(cv_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cv")
        
        cl_content = processor.create_tailored_cover_letter(job['title'], job['company'], role_focus)
        cl_pdf = processor.compile_latex(cl_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cl")
        
        if cv_pdf and cl_pdf:
            if processor.send_email(job['title'], job['company'], cv_pdf, cl_pdf):
                successful += 1
                print(f"   🎉 SUCCESS: Application sent!")
                
                # Clean up
                try:
                    os.remove(cv_pdf)
                    os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"   ❌ FAILED: Email not sent")
        else:
            print(f"   ❌ FAILED: PDF generation failed")
        
        if i < max_applications:
            await asyncio.sleep(3)
    
    print(f"\n🎉 REAL DATA WORKFLOW COMPLETE!")
    print("=" * 60)
    print(f"✅ Applications sent: {successful}/{max_applications}")
    print(f"📧 Check leeharvad@gmail.com for real job applications")

if __name__ == "__main__":
    asyncio.run(main())