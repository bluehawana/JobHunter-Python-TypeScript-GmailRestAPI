#!/usr/bin/env python3
"""
Test script to save sample jobs to the database
"""

import os
import sys
from datetime import datetime, date
from typing import List, Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def create_sample_jobs() -> List[Dict[str, Any]]:
    """Create sample job data"""
    return [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Sweden",
            "location": "Stockholm, Sweden",
            "description": "We are looking for a senior Python developer to join our team...",
            "requirements": "5+ years Python experience, FastAPI, PostgreSQL",
            "salary_range": "600,000 - 800,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://techcorp.se/careers/python-developer",
            "source": "company_website",
            "skills_matched": ["Python", "FastAPI", "PostgreSQL", "REST API"],
            "match_score": 0.95,
            "status": "found"
        },
        {
            "title": "Backend Developer",
            "company": "Growing Startup",
            "location": "Gothenburg, Sweden",
            "description": "Join our fast-growing startup as a backend developer...",
            "requirements": "Python, Django/FastAPI, PostgreSQL, AWS",
            "salary_range": "500,000 - 650,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://startup.com/jobs/backend-dev",
            "source": "linkedin",
            "skills_matched": ["Python", "Django", "PostgreSQL", "AWS"],
            "match_score": 0.88,
            "status": "found"
        },
        {
            "title": "Full Stack Developer",
            "company": "Digital Agency",
            "location": "Malmö, Sweden",
            "description": "Looking for a full stack developer with Python and React experience...",
            "requirements": "Python, FastAPI, React, TypeScript, PostgreSQL",
            "salary_range": "550,000 - 700,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://digitalagency.se/careers",
            "source": "indeed",
            "skills_matched": ["Python", "FastAPI", "React", "TypeScript"],
            "match_score": 0.92,
            "status": "found"
        },
        {
            "title": "DevOps Engineer",
            "company": "FinTech Solutions",
            "location": "Remote, Sweden",
            "description": "Remote DevOps engineer position with focus on Python automation...",
            "requirements": "Python, Docker, Kubernetes, AWS, CI/CD",
            "salary_range": "650,000 - 850,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://fintech.se/jobs/devops",
            "source": "arbetsformedlingen",
            "skills_matched": ["Python", "Docker", "Kubernetes", "AWS"],
            "match_score": 0.85,
            "status": "found"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Research Lab",
            "location": "Uppsala, Sweden",
            "description": "ML engineer position working on cutting-edge AI projects...",
            "requirements": "Python, TensorFlow, PyTorch, SQL, Machine Learning",
            "salary_range": "700,000 - 900,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://ailab.se/careers/ml-engineer",
            "source": "google_jobs",
            "skills_matched": ["Python", "TensorFlow", "Machine Learning"],
            "match_score": 0.78,
            "status": "found"
        }
    ]

def save_jobs_to_database():
    """Save sample jobs to Supabase database"""
    print("🚀 Testing Job Saving Functionality")
    print("=" * 60)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY not found in environment variables")
        
        print(f"📊 Supabase URL: {supabase_url}")
        
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase successfully!")
        print()
        
        # Create sample jobs
        sample_jobs = create_sample_jobs()
        print(f"📋 Created {len(sample_jobs)} sample jobs")
        
        # Save jobs one by one
        saved_jobs = []
        for i, job_data in enumerate(sample_jobs, 1):
            try:
                print(f"💾 Saving job {i}/{len(sample_jobs)}: {job_data['title']} at {job_data['company']}")
                
                result = supabase.table('jobs').insert(job_data).execute()
                
                if result.data:
                    saved_job = result.data[0]
                    saved_jobs.append(saved_job)
                    print(f"   ✅ Saved with ID: {saved_job['id']}")
                else:
                    print(f"   ❌ Failed to save: no data returned")
                    
            except Exception as e:
                print(f"   ❌ Error saving job: {e}")
        
        print()
        print(f"📊 RESULTS:")
        print(f"   💾 Successfully saved: {len(saved_jobs)}/{len(sample_jobs)} jobs")
        
        if saved_jobs:
            print("\n📋 Saved jobs:")
            for job in saved_jobs:
                print(f"   • {job['title']} at {job['company']} ({job['source']})")
        
        return len(saved_jobs) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("JobHunter Job Saving Test")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = save_jobs_to_database()
    
    if success:
        print("\n🎉 Job saving test completed successfully!")
        print("\n🔧 NEXT STEPS:")
        print("1. Run 'python check_jobs_supabase.py' to verify saved jobs")
        print("2. Run your job aggregation services to collect real jobs")
        print("3. Check the Supabase dashboard to see the saved data")
    else:
        print("\n❌ Job saving test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()