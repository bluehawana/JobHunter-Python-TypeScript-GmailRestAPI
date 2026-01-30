#!/usr/bin/env python3
"""
Mock 8PM Daily Automation Test
Simulates tonight 8pm when JobHunter automation starts automatically
Optimal time for Claude API (Chinese users sleeping, less API load)
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import time

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Import our priority processor
from priority_job_processor import PriorityJobProcessor

class MockDailyAutomation:
    def __init__(self):
        self.processor = PriorityJobProcessor()
        self.current_time = datetime.now()
        self.mock_tonight_8pm = self.current_time.replace(hour=20, minute=0, second=0)
        
    def print_automation_header(self):
        """Print automation startup header"""
        print("🌅" + "=" * 70 + "🌅")
        print("🤖 JOBHUNTER DAILY AUTOMATION STARTED")
        print("=" * 72)
        print(f"⏰ Current Time: {self.mock_tonight_8pm.strftime('%Y-%m-%d 20:00:00')} (Simulated)")
        print(f"📅 Day: {self.mock_tonight_8pm.strftime('%A, %B %d, %Y')}")
        print(f"🧠 Claude API Optimization: Running when Chinese users are sleeping")
        print(f"🎯 Mode: Daily Job Search Automation")
        print(f"📧 Target Email: leeharvad@gmail.com")
        print("=" * 72)
        print()
    
    async def simulate_system_startup(self):
        """Simulate system startup sequence"""
        print("🔧 SYSTEM STARTUP SEQUENCE")
        print("-" * 30)
        
        startup_steps = [
            ("Initializing JobHunter services", 1),
            ("Loading user preferences and priorities", 0.5),
            ("Connecting to email services", 1),
            ("Establishing database connections", 0.5),
            ("Loading job source APIs", 1),
            ("Verifying SMTP configuration", 0.5),
            ("Starting job scanning modules", 1)
        ]
        
        for step, delay in startup_steps:
            print(f"   ⚙️  {step}...")
            await asyncio.sleep(delay)
            print(f"   ✅ {step} - Complete")
        
        print("\n🎉 All systems operational!")
        await asyncio.sleep(1)
    
    async def simulate_daily_job_scan(self) -> List[Dict]:
        """Simulate scanning all job sources following priority order"""
        print("\n📊 DAILY JOB SCANNING")
        print("-" * 30)
        
        all_jobs = []
        
        # Priority 1: bluehawana@gmail.com emails
        print("🥇 Priority 1: Scanning bluehawana@gmail.com...")
        await asyncio.sleep(2)
        
        gmail_jobs = [
            {
                'title': 'Senior Java Developer',
                'company': 'Volvo Group',
                'location': 'Gothenburg, Sweden',
                'description': 'Join our software development team building next-generation truck systems using Java and Spring Boot.',
                'url': 'https://careers.volvogroup.com/java-developer',
                'source': 'bluehawana_email_linkedin',
                'job_type': 'fulltime',
                'received_time': '6 hours ago',
                'sender': 'LinkedIn Jobs <jobs-noreply@linkedin.com>'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Spotify',
                'location': 'Remote (Europe)',
                'description': 'Build and maintain infrastructure for music streaming platform. Kubernetes, Docker, AWS experience required.',
                'url': 'https://careers.spotify.com/devops-engineer',
                'source': 'bluehawana_email_indeed',
                'job_type': 'remote',
                'received_time': '2 hours ago',
                'sender': 'Indeed <noreply@indeed.com>'
            }
        ]
        
        print(f"   ✅ Found {len(gmail_jobs)} jobs from email scanning")
        for job in gmail_jobs:
            print(f"      📧 {job['title']} at {job['company']} (from {job['sender']})")
        
        all_jobs.extend(gmail_jobs)
        
        # Priority 2: LinkedIn Saved Jobs
        print("\n🥈 Priority 2: Checking LinkedIn saved jobs...")
        await asyncio.sleep(1.5)
        
        linkedin_saved = [
            {
                'title': 'Backend Developer',
                'company': 'Zenseact',
                'location': 'Gothenburg, Sweden',
                'description': 'Autonomous driving software development using modern backend technologies.',
                'url': 'https://careers.zenseact.com/backend-developer',
                'source': 'linkedin_saved',
                'job_type': 'fulltime',
                'saved_date': 'Yesterday'
            },
            {
                'title': 'Software Engineer',
                'company': 'Google',
                'location': 'Remote (Global)',
                'description': 'Build products that help billions of users worldwide.',
                'url': 'https://careers.google.com/software-engineer',
                'source': 'linkedin_saved',
                'job_type': 'remote',
                'saved_date': '2 days ago'
            }
        ]
        
        print(f"   ✅ Found {len(linkedin_saved)} saved jobs")
        for job in linkedin_saved:
            print(f"      📋 {job['title']} at {job['company']} (saved {job['saved_date']})")
        
        all_jobs.extend(linkedin_saved)
        
        # Priority 3: LinkedIn API
        print("\n🥉 Priority 3: LinkedIn API job matching...")
        await asyncio.sleep(1)
        
        linkedin_api = [
            {
                'title': 'Fullstack Developer',
                'company': 'SKF Group',
                'location': 'Gothenburg, Sweden',
                'description': 'Industrial technology company seeking fullstack developer for digital transformation projects.',
                'url': 'https://careers.skf.com/fullstack-developer',
                'source': 'linkedin_api',
                'job_type': 'fulltime',
                'match_score': 95
            }
        ]
        
        print(f"   ✅ Found {len(linkedin_api)} matching jobs")
        for job in linkedin_api:
            print(f"      🎯 {job['title']} at {job['company']} (match: {job['match_score']}%)")
        
        all_jobs.extend(linkedin_api)
        
        # Priority 4: Indeed + Arbetsförmedlingen
        print("\n4️⃣ Priority 4: Indeed website + Arbetsförmedlingen...")
        await asyncio.sleep(1)
        
        other_sources = [
            {
                'title': 'Cloud Engineer',
                'company': 'Ericsson',
                'location': 'Gothenburg, Sweden',
                'description': '5G network infrastructure development and cloud engineering.',
                'url': 'https://careers.ericsson.com/cloud-engineer',
                'source': 'indeed_website',
                'job_type': 'fulltime'
            }
        ]
        
        print(f"   ✅ Found {len(other_sources)} additional jobs")
        for job in other_sources:
            print(f"      🌐 {job['title']} at {job['company']}")
        
        all_jobs.extend(other_sources)
        
        print(f"\n📊 SCAN COMPLETE: Total {len(all_jobs)} jobs found from all sources")
        return all_jobs
    
    async def simulate_job_processing(self, jobs: List[Dict]) -> int:
        """Simulate processing and applying to prioritized jobs"""
        print("\n🎯 JOB PRIORITIZATION & PROCESSING")
        print("-" * 40)
        
        # Filter and prioritize
        print("🔍 Filtering jobs by your preferences...")
        await asyncio.sleep(1)
        
        prioritized_jobs = self.processor.filter_and_prioritize_jobs(jobs)
        
        print(f"✅ {len(prioritized_jobs)} jobs match your criteria:")
        print("   📍 Gothenburg (any company) OR Remote (famous IT only)")
        print()
        
        print("📋 Priority Ranking:")
        for i, job in enumerate(prioritized_jobs, 1):
            location_type = "🏢 Gothenburg" if self.processor.is_gothenburg_relevant(job['location']) else f"🌐 {job['location']}"
            priority_score = job.get('priority_score', 0)
            print(f"   {i}. {job['title']} at {job['company']} ({location_type}) - Score: {priority_score}")
        
        # Process top 3 jobs
        max_to_process = min(3, len(prioritized_jobs))
        print(f"\n🚀 Processing top {max_to_process} priority jobs...")
        
        successful_applications = 0
        
        for i, job in enumerate(prioritized_jobs[:max_to_process], 1):
            print(f"\n📝 Application {i}/{max_to_process}: {job['title']} at {job['company']}")
            print(f"   📊 Source: {job['source']}")
            print(f"   📍 Location: {job['location']}")
            
            # Simulate role determination
            role_focus = self.processor.determine_role_focus(job['title'])
            print(f"   🎯 Role Focus: {role_focus}")
            
            # Simulate document generation
            print("   📄 Generating tailored CV...")
            await asyncio.sleep(0.5)
            
            print("   📄 Generating tailored cover letter...")
            await asyncio.sleep(0.5)
            
            # Simulate PDF compilation
            print("   🔨 Compiling LaTeX to PDF...")
            await asyncio.sleep(1)
            
            # Generate actual PDFs
            cv_content = self.processor.create_tailored_cv(job['title'], job['company'], role_focus)
            cv_pdf = self.processor.compile_latex(cv_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cv")
            
            cl_content = self.processor.create_tailored_cover_letter(job['title'], job['company'], role_focus)
            cl_pdf = self.processor.compile_latex(cl_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cl")
            
            if cv_pdf and cl_pdf:
                print("   ✅ PDFs generated successfully")
                
                # Simulate email sending
                print("   📧 Sending application email...")
                await asyncio.sleep(1)
                
                # Send actual email
                email_sent = self.processor.send_email(job['title'], job['company'], cv_pdf, cl_pdf)
                
                if email_sent:
                    successful_applications += 1
                    print("   🎉 SUCCESS: Application sent to leeharvad@gmail.com")
                    
                    # Clean up files
                    try:
                        os.remove(cv_pdf)
                        os.remove(cl_pdf)
                    except:
                        pass
                else:
                    print("   ❌ FAILED: Email sending error")
            else:
                print("   ❌ FAILED: PDF generation error")
            
            if i < max_to_process:
                print("   ⏳ Waiting before next application...")
                await asyncio.sleep(2)
        
        return successful_applications
    
    async def simulate_daily_summary(self, total_jobs: int, processed_jobs: int, successful_apps: int):
        """Simulate sending daily summary"""
        print(f"\n📊 DAILY AUTOMATION SUMMARY")
        print("-" * 40)
        
        print("📈 Statistics:")
        print(f"   • Total jobs scanned: {total_jobs}")
        print(f"   • Jobs matching criteria: {processed_jobs}")
        print(f"   • Applications sent: {successful_apps}")
        print(f"   • Success rate: {(successful_apps/max(processed_jobs, 1)*100):.1f}%")
        
        print("\n📧 Email Summary:")
        print(f"   • Target: leeharvad@gmail.com")
        print(f"   • Individual application emails: {successful_apps}")
        print(f"   • Daily summary email: 1")
        
        print("\n🔄 Next Actions:")
        print("   • Continue monitoring job sources")
        print("   • Next automated scan: Tonight 20:00 (8 PM)")
        print("   • Manual scan available anytime")
        
    async def run_complete_mock_test(self):
        """Run complete 6am automation mock test"""
        
        # Startup
        self.print_automation_header()
        await self.simulate_system_startup()
        
        # Job scanning
        jobs = await self.simulate_daily_job_scan()
        
        # Job processing and applications
        successful_apps = await self.simulate_job_processing(jobs)
        
        # Daily summary
        await self.simulate_daily_summary(len(jobs), min(3, len(jobs)), successful_apps)
        
        # Completion
        print(f"\n🌙 8PM AUTOMATION COMPLETE!")
        print("=" * 72)
        print(f"⏰ Automation finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 {successful_apps} job applications sent automatically")
        print(f"📧 Check leeharvad@gmail.com for applications")
        print(f"💤 System will sleep until next scheduled run")
        print("🌅" + "=" * 70 + "🌅")

async def main():
    """Run the complete 8pm automation mock test"""
    automation = MockDailyAutomation()
    await automation.run_complete_mock_test()

if __name__ == "__main__":
    asyncio.run(main())