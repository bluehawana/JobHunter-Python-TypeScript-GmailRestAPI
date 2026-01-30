#!/usr/bin/env python3
"""
Complete JobHunter Mock Test - Full 6AM Automation
Simulates tomorrow morning's complete workflow:
1. System startup at 6AM
2. Job scanning from all priority sources
3. Smart LaTeX editing with your templates
4. Priority filtering and processing
5. Email delivery for review
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Import our smart editor
from smart_latex_editor import SmartLaTeXEditor

class CompleteMockTest:
    def __init__(self):
        self.editor = SmartLaTeXEditor()
        self.current_time = datetime.now()
        self.mock_6am = self.current_time.replace(hour=6, minute=0, second=0) + timedelta(days=1)
        
        # Famous IT companies for remote job filtering
        self.famous_it_companies = [
            'google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix', 'spotify', 
            'github', 'gitlab', 'atlassian', 'slack', 'zoom', 'salesforce',
            'adobe', 'nvidia', 'intel', 'oracle', 'sap', 'vmware', 'redis',
            'mongodb', 'elastic', 'datadog', 'twilio', 'stripe', 'shopify'
        ]
        
        # Gothenburg priority companies
        self.gothenburg_companies = [
            'volvo', 'volvo cars', 'volvo group', 'zenseact', 'polestar', 'geely',
            'ericsson', 'telia', 'saab', 'skf', 'hasselblad', 'ecarx',
            'synteda', 'addcell', 'pembio'
        ]
    
    def print_6am_header(self):
        """Print 6AM automation header"""
        print("🌅" + "=" * 80 + "🌅")
        print("🤖 JOBHUNTER 6AM DAILY AUTOMATION - COMPLETE MOCK TEST")
        print("=" * 82)
        print(f"⏰ Simulated Time: {self.mock_6am.strftime('%Y-%m-%d 06:00:00')}")
        print(f"📅 Day: {self.mock_6am.strftime('%A, %B %d, %Y')}")
        print(f"🎯 Mode: Full Production Workflow Simulation")
        print(f"📧 Target: leeharvad@gmail.com")
        print(f"📝 Method: Smart LaTeX editing with your exact templates")
        print("=" * 82)
        print()
    
    async def simulate_system_startup(self):
        """Simulate complete system startup"""
        print("🔧 SYSTEM STARTUP SEQUENCE")
        print("-" * 40)
        
        startup_steps = [
            ("🚀 Initializing JobHunter core services", 1.5),
            ("📋 Loading user preferences and job priorities", 1),
            ("📧 Connecting to bluehawana@gmail.com email services", 1.5),
            ("🔗 Establishing LinkedIn API connections", 1),
            ("🌐 Connecting to Indeed and Arbetsförmedlingen APIs", 1),
            ("📊 Loading Supabase job database", 1),
            ("✉️  Verifying SMTP configuration for notifications", 0.5),
            ("🎯 Loading smart LaTeX editing templates", 1),
            ("🔍 Starting job scanning and filtering modules", 1)
        ]
        
        for step, delay in startup_steps:
            print(f"   {step}...")
            await asyncio.sleep(delay)
            print(f"   ✅ Complete")
        
        print("\n🎉 All systems operational and ready for job processing!")
        await asyncio.sleep(1)
    
    async def scan_all_job_sources(self) -> List[Dict]:
        """Simulate scanning all job sources in priority order"""
        print("\n📊 DAILY JOB SOURCE SCANNING")
        print("-" * 50)
        
        all_jobs = []
        
        # Priority 1: bluehawana@gmail.com email scanning
        print("🥇 Priority 1: Scanning bluehawana@gmail.com...")
        await asyncio.sleep(2)
        
        email_jobs = [
            {
                'title': 'Senior Solution Developer',
                'company': 'Volvo Group',
                'location': 'Gothenburg, Sweden',
                'department': 'Onsite Infrastructure Demand & Automation',
                'address': 'Sven Erikssons gata 7',
                'city': '41755 Göteborg',
                'description': 'Join our automation team to streamline manual processes and drive digital transformation across Volvo Group factories and warehouses. Expertise in Python, Ansible, Terraform, Docker, Kubernetes required.',
                'source': 'bluehawana_email_linkedin',
                'job_type': 'fulltime',
                'received_time': '4 hours ago',
                'sender': 'LinkedIn Jobs <jobs-noreply@linkedin.com>'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Spotify',
                'location': 'Remote (Europe)',
                'description': 'Build and maintain infrastructure for music streaming platform. Kubernetes, Docker, AWS, CI/CD experience required.',
                'source': 'bluehawana_email_indeed',
                'job_type': 'remote',
                'received_time': '6 hours ago',
                'sender': 'Indeed <noreply@indeed.com>'
            },
            {
                'title': 'Backend Developer',
                'company': 'Random Startup',
                'location': 'Remote',
                'description': 'Remote backend development opportunity.',
                'source': 'bluehawana_email_linkedin',
                'job_type': 'remote',
                'received_time': '8 hours ago',
                'sender': 'LinkedIn Jobs <jobs-noreply@linkedin.com>'
            }
        ]
        
        print(f"   ✅ Found {len(email_jobs)} jobs from email scanning:")
        for job in email_jobs:
            print(f"      📧 {job['title']} at {job['company']} (from {job['sender']})")
        
        all_jobs.extend(email_jobs)
        
        # Priority 2: LinkedIn Saved Jobs
        print("\n🥈 Priority 2: Processing LinkedIn saved jobs...")
        await asyncio.sleep(1.5)
        
        linkedin_saved = [
            {
                'title': 'Infrastructure Engineer',
                'company': 'Zenseact',
                'location': 'Gothenburg, Sweden',
                'description': 'Autonomous driving infrastructure and cloud engineering.',
                'source': 'linkedin_saved',
                'job_type': 'fulltime',
                'saved_date': 'Yesterday'
            },
            {
                'title': 'Cloud Platform Engineer',
                'company': 'SKF Group',
                'location': 'Gothenburg, Sweden',
                'description': 'Industrial IoT and cloud platform development.',
                'source': 'linkedin_saved',
                'job_type': 'fulltime',
                'saved_date': '2 days ago'
            },
            {
                'title': 'Software Engineer',
                'company': 'Netflix',
                'location': 'Remote (Global)',
                'description': 'Build entertainment platforms used by millions worldwide.',
                'source': 'linkedin_saved',
                'job_type': 'remote',
                'saved_date': '3 days ago'
            }
        ]
        
        print(f"   ✅ Found {len(linkedin_saved)} saved jobs:")
        for job in linkedin_saved:
            print(f"      📋 {job['title']} at {job['company']} (saved {job['saved_date']})")
        
        all_jobs.extend(linkedin_saved)
        
        # Priority 3: LinkedIn API job matching
        print("\n🥉 Priority 3: LinkedIn API background matching...")
        await asyncio.sleep(1)
        
        linkedin_api = [
            {
                'title': 'Fullstack Developer',
                'company': 'Ericsson',
                'location': 'Gothenburg, Sweden',
                'description': '5G network development with modern fullstack technologies.',
                'source': 'linkedin_api',
                'job_type': 'fulltime',
                'match_score': 92
            }
        ]
        
        print(f"   ✅ Found {len(linkedin_api)} API-matched jobs:")
        for job in linkedin_api:
            print(f"      🎯 {job['title']} at {job['company']} (match: {job['match_score']}%)")
        
        all_jobs.extend(linkedin_api)
        
        # Priority 4: Indeed + Arbetsförmedlingen
        print("\n4️⃣ Priority 4: Indeed website + Arbetsförmedlingen...")
        await asyncio.sleep(1)
        
        other_sources = [
            {
                'title': 'Platform Engineer',
                'company': 'Hasselblad',
                'location': 'Gothenburg, Sweden',
                'description': 'Camera technology platform development and cloud engineering.',
                'source': 'indeed_website',
                'job_type': 'fulltime'
            }
        ]
        
        print(f"   ✅ Found {len(other_sources)} additional jobs:")
        for job in other_sources:
            print(f"      🌐 {job['title']} at {job['company']}")
        
        all_jobs.extend(other_sources)
        
        print(f"\n📊 SCAN COMPLETE: {len(all_jobs)} total jobs found from all sources")
        return all_jobs
    
    def calculate_job_priority(self, job: Dict) -> int:
        """Calculate job priority score"""
        score = 0
        location = job.get('location', '').lower()
        company = job.get('company', '').lower()
        job_type = job.get('job_type', '').lower()
        
        # Gothenberg jobs get highest priority (any company)
        if any(keyword in location for keyword in ['gothenburg', 'göteborg', 'goteborg']):
            score += 100
            # Extra points for known Gothenburg companies
            if any(comp in company for comp in self.gothenburg_companies):
                score += 20
        
        # Remote jobs from famous IT companies
        elif 'remote' in location or 'remote' in job_type:
            if any(famous in company for famous in self.famous_it_companies):
                score += 80  # High but less than Gothenburg
            else:
                score += 10  # Low priority for remote non-famous companies
        
        # Other Swedish cities
        elif any(city in location for city in ['stockholm', 'malmö', 'lund', 'uppsala']):
            score += 50
        
        # Bonus for relevant job titles
        title = job.get('title', '').lower()
        if any(keyword in title for keyword in ['fullstack', 'backend', 'devops', 'solution', 'platform']):
            score += 10
        
        return score
    
    def filter_and_prioritize_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter and prioritize jobs according to user preferences"""
        print("\n🎯 JOB FILTERING & PRIORITIZATION")
        print("-" * 50)
        
        print("🔍 Applying your job preferences:")
        print("   1️⃣ Gothenburg (any company) - HIGHEST priority")
        print("   2️⃣ Remote (famous IT companies only) - MEDIUM priority")
        print("   ❌ Remote (non-famous companies) - FILTERED OUT")
        
        # Calculate priority for each job
        for job in jobs:
            job['priority_score'] = self.calculate_job_priority(job)
        
        # Filter jobs
        filtered_jobs = []
        filtered_out = []
        
        for job in jobs:
            location = job.get('location', '').lower()
            company = job.get('company', '')
            
            # Include if: Gothenburg OR Remote+Famous IT OR Other Swedish cities
            if (any(keyword in location for keyword in ['gothenburg', 'göteborg']) or 
                ('remote' in location and any(famous in company.lower() for famous in self.famous_it_companies)) or
                any(city in location for city in ['stockholm', 'malmö', 'lund', 'uppsala'])):
                filtered_jobs.append(job)
            else:
                filtered_out.append(job)
        
        # Sort by priority score
        filtered_jobs.sort(key=lambda x: x['priority_score'], reverse=True)
        
        print(f"\n✅ {len(filtered_jobs)} jobs match your criteria:")
        for i, job in enumerate(filtered_jobs, 1):
            location_type = "🏢 Gothenburg" if 'gothenburg' in job['location'].lower() else f"🌐 {job['location']}"
            print(f"   {i}. {job['title']} at {job['company']} ({location_type}) - Score: {job['priority_score']}")
        
        if filtered_out:
            print(f"\n❌ {len(filtered_out)} jobs filtered out:")
            for job in filtered_out:
                print(f"   • {job['title']} at {job['company']} - {job['location']} (doesn't meet criteria)")
        
        return filtered_jobs
    
    async def process_priority_jobs(self, jobs: List[Dict]) -> int:
        """Process top priority jobs with smart LaTeX editing"""
        print(f"\n🚀 SMART JOB PROCESSING")
        print("-" * 40)
        
        max_to_process = min(3, len(jobs))
        print(f"📋 Processing top {max_to_process} priority jobs with smart LaTeX editing...")
        print()
        
        successful_applications = 0
        
        for i, job in enumerate(jobs[:max_to_process], 1):
            print(f"📝 Application {i}/{max_to_process}: {job['title']} at {job['company']}")
            print(f"   📊 Source: {job['source']}")
            print(f"   📍 Location: {job['location']}")
            print(f"   🎯 Priority Score: {job['priority_score']}")
            
            # Determine role focus
            role_focus = self.editor.determine_role_focus(job['title'])
            print(f"   🔧 Role Focus: {role_focus}")
            
            try:
                # Smart LaTeX editing
                print("   ✏️  Making targeted edits to your LaTeX templates...")
                cv_content = self.editor.edit_cv_for_job(job['title'], job['company'], role_focus)
                
                # Handle department/address info for cover letter
                department = job.get('department', f"{job['title']} Team")
                address = job.get('address', "Hiring Department")
                city = job.get('city', job.get('location', 'Sweden'))
                
                cl_content = self.editor.edit_cover_letter_for_job(
                    job['title'], job['company'], department, address, city
                )
                
                # Save LaTeX files
                cv_tex, cl_tex = self.editor.save_latex_files(cv_content, cl_content, job['title'], job['company'])
                
                if cv_tex and cl_tex:
                    print(f"   💾 LaTeX files saved: {cv_tex}, {cl_tex}")
                    
                    # Send for review
                    print("   📧 Sending LaTeX files for review...")
                    
                    # Use the send function from our previous script
                    success = await self.send_review_email(job, cv_tex, cl_tex, role_focus)
                    
                    if success:
                        successful_applications += 1
                        print("   🎉 SUCCESS: Review files sent!")
                    else:
                        print("   ❌ FAILED: Email sending error")
                else:
                    print("   ❌ FAILED: Could not save LaTeX files")
                    
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
            
            if i < max_to_process:
                print("   ⏳ Waiting before next application...")
                await asyncio.sleep(3)
            
            print()
        
        return successful_applications
    
    async def send_review_email(self, job: Dict, cv_tex: str, cl_tex: str, role_focus: str) -> bool:
        """Send review email with LaTeX files"""
        try:
            # Import email sending functionality
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            
            msg = MIMEMultipart()
            msg['From'] = self.editor.sender_email
            msg['To'] = self.editor.recipient_email
            msg['Subject'] = f"6AM JobHunter: {job['title']} at {job['company']} - LaTeX Review"
            
            body = f"""Hi,

6AM automation has found and processed a high-priority job:

🏢 Company: {job['company']}
💼 Position: {job['title']}
🎯 Role Focus: {role_focus.title()}
📍 Location: {job['location']}
📊 Source: {job['source']}
🎖️  Priority Score: {job.get('priority_score', 'N/A')}

📎 Smart-edited LaTeX files attached:
   • CV (LaTeX source) - Your template with targeted {role_focus} edits
   • Cover Letter (LaTeX source) - Customized for {job['company']}

✏️  Targeted edits made:
   ✅ Job title: {job['title']}
   ✅ Profile summary: Tailored for {role_focus} role
   ✅ Cover letter: Customized content for {job['company']}
   ✅ Contact info: Updated for this application
   ✅ Skills emphasis: Highlighted {role_focus} expertise

🔨 To compile PDFs:
   1. Download .tex files
   2. Run: pdflatex filename.tex (twice for references)
   3. Review PDFs and send if approved

This was generated by your 6AM daily automation system.

Best regards,
JobHunter 6AM Automation
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach LaTeX files
            for file_path, filename in [(cv_tex, f"CV_{job['company']}_{job['title']}_6AM.tex"),
                                      (cl_tex, f"CL_{job['company']}_{job['title']}_6AM.tex")]:
                if Path(file_path).exists():
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.editor.smtp_server, self.editor.smtp_port)
            server.starttls()
            server.login(self.editor.sender_email, self.editor.password)
            server.sendmail(self.editor.sender_email, self.editor.recipient_email, msg.as_string())
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    async def generate_daily_summary(self, total_jobs: int, filtered_jobs: int, successful_apps: int):
        """Generate daily automation summary"""
        print(f"📊 6AM AUTOMATION SUMMARY")
        print("-" * 40)
        
        print("📈 Daily Statistics:")
        print(f"   • Total jobs scanned: {total_jobs}")
        print(f"   • Jobs matching criteria: {filtered_jobs}")
        print(f"   • Applications processed: {successful_apps}")
        print(f"   • Success rate: {(successful_apps/max(filtered_jobs, 1)*100):.1f}%")
        
        print("\n📧 Notification Summary:")
        print(f"   • Target email: {self.editor.recipient_email}")
        print(f"   • LaTeX review emails sent: {successful_apps}")
        print(f"   • Ready for manual compilation and review")
        
        print("\n🎯 Job Priority Results:")
        print("   • Gothenburg companies: PRIORITIZED")
        print("   • Remote famous IT: INCLUDED") 
        print("   • Remote non-famous: FILTERED OUT")
        
        print(f"\n🔄 Next Actions:")
        print("   • Review LaTeX files in email")
        print("   • Compile PDFs manually") 
        print("   • Send approved applications")
        print("   • Next scan: Tomorrow 6:00 AM")
    
    async def run_complete_mock_test(self):
        """Run the complete 6AM automation mock test"""
        
        # Print header
        self.print_6am_header()
        
        # System startup
        await self.simulate_system_startup()
        
        # Job scanning
        all_jobs = await self.scan_all_job_sources()
        
        # Job filtering and prioritization  
        prioritized_jobs = self.filter_and_prioritize_jobs(all_jobs)
        
        # Process priority jobs
        successful_apps = await self.process_priority_jobs(prioritized_jobs)
        
        # Daily summary
        await self.generate_daily_summary(len(all_jobs), len(prioritized_jobs), successful_apps)
        
        # Completion
        print(f"\n🌅 6AM DAILY AUTOMATION COMPLETE!")
        print("=" * 82)
        print(f"⏰ Mock test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 {successful_apps} high-priority applications processed and sent for review")
        print(f"📧 Check {self.editor.recipient_email} for LaTeX review emails")
        print(f"💤 System ready for production - will activate at next 6AM")
        print("🌅" + "=" * 80 + "🌅")

async def main():
    """Run the complete mock test"""
    mock_test = CompleteMockTest()
    await mock_test.run_complete_mock_test()

if __name__ == "__main__":
    asyncio.run(main())