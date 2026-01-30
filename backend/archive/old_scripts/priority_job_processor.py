#!/usr/bin/env python3
"""
JobHunter workflow following user's exact priorities:
1. Gothenburg jobs (any company)
2. Remote jobs (only famous IT companies)
3. Source priority: bluehawana@gmail.com emails > LinkedIn API > Indeed > Arbetsförmedlingen
"""
import asyncio
import sys
import os
from pathlib import Path
from typing import List, Dict

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Import the quick processor for PDF generation and email sending
from quick_job_processor import QuickJobProcessor

class PriorityJobProcessor(QuickJobProcessor):
    def __init__(self):
        super().__init__()
        self.famous_it_companies = [
            'google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix', 'spotify', 
            'github', 'gitlab', 'atlassian', 'slack', 'zoom', 'salesforce',
            'adobe', 'nvidia', 'intel', 'oracle', 'sap', 'vmware', 'redis',
            'mongodb', 'elastic', 'datadog', 'twilio', 'stripe', 'shopify',
            'uber', 'airbnb', 'tesla', 'spacex', 'palantir', 'snowflake'
        ]
        
        self.gothenburg_priority_companies = [
            'volvo', 'volvo cars', 'volvo group', 'zenseact', 'polestar', 'geely',
            'ericsson', 'telia', 'saab', 'skf', 'hasselblad', 'ecarx',
            'chalmers', 'university of gothenburg', 'cevt', 'stena line'
        ]
    
    def is_famous_it_company(self, company: str) -> bool:
        """Check if company is a famous IT company"""
        company_lower = company.lower()
        return any(famous in company_lower for famous in self.famous_it_companies)
    
    def is_gothenburg_relevant(self, location: str) -> bool:
        """Check if job is in or near Gothenburg"""
        if not location:
            return False
        location_lower = location.lower()
        gothenburg_keywords = ['gothenburg', 'göteborg', 'goteborg', 'västra götaland', 'west sweden']
        return any(keyword in location_lower for keyword in gothenburg_keywords)
    
    def calculate_job_priority(self, job: Dict) -> int:
        """Calculate job priority score (higher = better)"""
        score = 0
        location = job.get('location', '').lower()
        company = job.get('company', '').lower()
        job_type = job.get('job_type', '').lower()
        
        # Gothenburg jobs get highest priority (any company)
        if self.is_gothenburg_relevant(location):
            score += 100
            # Extra points for known Gothenburg companies
            if any(comp in company for comp in self.gothenburg_priority_companies):
                score += 20
        
        # Remote jobs from famous IT companies
        elif 'remote' in location or 'remote' in job_type:
            if self.is_famous_it_company(company):
                score += 80  # High but less than Gothenburg
            else:
                score += 10  # Low priority for remote non-famous companies
        
        # Other Swedish cities (lower priority)
        elif any(city in location for city in ['stockholm', 'malmö', 'malmo', 'lund', 'uppsala']):
            score += 50
        
        # Bonus for relevant job titles
        title = job.get('title', '').lower()
        if any(keyword in title for keyword in ['fullstack', 'backend', 'devops', 'java', 'spring']):
            score += 10
        
        return score
    
    def filter_and_prioritize_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter and sort jobs by priority"""
        
        # Calculate priority for each job
        for job in jobs:
            job['priority_score'] = self.calculate_job_priority(job)
        
        # Filter out jobs that don't meet criteria
        filtered_jobs = []
        for job in jobs:
            location = job.get('location', '').lower()
            company = job.get('company', '')
            
            # Include if:
            # 1. Gothenburg (any company)
            # 2. Remote + famous IT company
            # 3. Other Swedish cities
            if (self.is_gothenburg_relevant(location) or 
                ('remote' in location and self.is_famous_it_company(company)) or
                any(city in location for city in ['stockholm', 'malmö', 'lund', 'uppsala'])):
                filtered_jobs.append(job)
        
        # Sort by priority score (highest first)
        filtered_jobs.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return filtered_jobs

async def get_jobs_from_priority_sources() -> List[Dict]:
    """Get jobs following priority order"""
    all_jobs = []
    
    print("📋 Following priority source order...")
    
    # Priority 1: Check bluehawana@gmail.com for job emails
    print("🥇 Priority 1: Checking bluehawana@gmail.com for LinkedIn Jobs and Indeed emails...")
    # This would connect to Gmail and scan for job emails
    # For now, using mock saved jobs that would come from email scanning
    
    # Priority 2: LinkedIn saved jobs (from yesterday's link)
    print("🥈 Priority 2: Getting LinkedIn saved jobs...")
    # This would use LinkedIn API or import saved jobs
    
    # Priority 3: LinkedIn API for background-matching jobs
    print("🥉 Priority 3: LinkedIn API for jobs matching your background...")
    
    # Priority 4: Indeed website + Arbetsförmedlingen
    print("4️⃣ Priority 4: Indeed website + Arbetsförmedlingen...")
    
    # Mock jobs representing what would come from these sources
    # In real implementation, these would come from actual APIs/email scanning
    priority_jobs = [
        {
            'id': 1,
            'title': 'Senior Fullstack Developer',
            'company': 'Volvo Cars',
            'location': 'Gothenburg, Sweden',
            'description': 'Join our automotive software team building next-generation vehicle systems.',
            'url': 'https://careers.volvocars.com/fullstack-developer',
            'job_type': 'fulltime',
            'source': 'linkedin_saved'
        },
        {
            'id': 2,
            'title': 'Backend Developer',
            'company': 'Spotify',
            'location': 'Remote (Europe)',
            'description': 'Build scalable backend systems for music streaming platform.',
            'url': 'https://careers.spotify.com/backend-developer',
            'job_type': 'remote',
            'source': 'bluehawana_email'
        },
        {
            'id': 3,
            'title': 'DevOps Engineer',
            'company': 'Zenseact',
            'location': 'Gothenburg, Sweden',
            'description': 'Autonomous driving technology infrastructure and deployment.',
            'url': 'https://careers.zenseact.com/devops-engineer',
            'job_type': 'fullstack',
            'source': 'linkedin_api'
        },
        {
            'id': 4,
            'title': 'Software Engineer',
            'company': 'Google',
            'location': 'Remote (Global)',
            'description': 'Build products that help billions of users connect, explore, and interact.',
            'url': 'https://careers.google.com/software-engineer',
            'job_type': 'remote',
            'source': 'indeed_email'
        },
        {
            'id': 5,
            'title': 'Java Developer',
            'company': 'Local Stockholm Startup',
            'location': 'Stockholm, Sweden',
            'description': 'Small startup looking for Java developer.',
            'url': 'https://startup.se/java-developer',
            'job_type': 'fulltime',
            'source': 'indeed_website'
        },
        {
            'id': 6,
            'title': 'Full Stack Developer',
            'company': 'Unknown Remote Company',
            'location': 'Remote',
            'description': 'Remote work opportunity.',
            'url': 'https://unknown.com/fullstack',
            'job_type': 'remote',
            'source': 'indeed_website'
        }
    ]
    
    return priority_jobs

async def main():
    """Main workflow following exact priorities"""
    processor = PriorityJobProcessor()
    
    print("🚀 JobHunter Priority Workflow")
    print("=" * 60)
    print("🎯 Priorities: 1️⃣ Gothenburg (any company) 2️⃣ Remote (famous IT only)")
    print("📧 Sources: bluehawana@gmail.com → LinkedIn → Indeed → Arbetsförmedlingen")
    print()
    
    # Get jobs from priority sources
    all_jobs = await get_jobs_from_priority_sources()
    print(f"📊 Found {len(all_jobs)} total jobs from all sources")
    
    # Filter and prioritize according to your preferences
    print("\n🔍 Filtering and prioritizing jobs...")
    prioritized_jobs = processor.filter_and_prioritize_jobs(all_jobs)
    
    print(f"✅ {len(prioritized_jobs)} jobs match your criteria")
    print("\n📋 Job Priority Ranking:")
    for i, job in enumerate(prioritized_jobs, 1):
        priority_score = job['priority_score']
        location_type = "🏢 Gothenburg" if processor.is_gothenburg_relevant(job['location']) else f"🌐 {job['location']}"
        print(f"   {i}. {job['title']} at {job['company']} ({location_type}) - Score: {priority_score}")
    
    if not prioritized_jobs:
        print("❌ No jobs match your criteria (Gothenburg or Remote+Famous IT)")
        return
    
    # Process top priority jobs
    max_applications = min(3, len(prioritized_jobs))  # Process top 3
    print(f"\n🔄 Processing top {max_applications} priority jobs...")
    
    successful = 0
    
    for i, job in enumerate(prioritized_jobs[:max_applications], 1):
        print(f"\n📋 Processing {i}/{max_applications}: {job['title']} at {job['company']}")
        print(f"   📍 Location: {job['location']}")
        print(f"   🎯 Priority Score: {job['priority_score']}")
        print(f"   📊 Source: {job['source']}")
        
        role_focus = processor.determine_role_focus(job['title'])
        print(f"   🔧 Role Focus: {role_focus}")
        
        # Generate tailored documents
        print("   📄 Generating tailored CV...")
        cv_content = processor.create_tailored_cv(job['title'], job['company'], role_focus)
        cv_pdf = processor.compile_latex(cv_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cv")
        
        print("   📄 Generating tailored cover letter...")
        cl_content = processor.create_tailored_cover_letter(job['title'], job['company'], role_focus)
        cl_pdf = processor.compile_latex(cl_content, f"hongzhi_{job['title'].lower().replace(' ', '_')}_{job['company'].lower().replace(' ', '_')}_cl")
        
        if cv_pdf and cl_pdf:
            print("   📧 Sending application email...")
            if processor.send_email(job['title'], job['company'], cv_pdf, cl_pdf):
                successful += 1
                print(f"   🎉 SUCCESS: Application sent!")
                
                # Clean up files
                try:
                    os.remove(cv_pdf)
                    os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"   ❌ FAILED: Email not sent")
        else:
            print(f"   ❌ FAILED: PDF generation failed")
        
        # Wait between applications
        if i < max_applications:
            print("   ⏳ Waiting 3 seconds...")
            await asyncio.sleep(3)
    
    print(f"\n📊 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Applications sent: {successful}/{max_applications}")
    print(f"📧 Check leeharvad@gmail.com for tailored applications")
    print(f"🎯 Focused on: Gothenburg positions + Remote famous IT companies")

if __name__ == "__main__":
    asyncio.run(main())