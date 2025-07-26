#!/usr/bin/env python3
"""
LinkedIn Saved Jobs Quick Import Tool
Use this to quickly add your LinkedIn saved jobs to the database
"""

import os
import sys
from datetime import datetime, date

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def save_linkedin_job(title: str, company: str, location: str = "Gothenburg, Sweden", 
                     description: str = "", requirements: str = "", 
                     apply_url: str = "", salary_range: str = "",
                     experience_level: str = "Mid-level"):
    """Save a LinkedIn job to database with high priority"""
    
    job_data = {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "requirements": requirements,
        "salary_range": salary_range,
        "job_type": "Full-time",
        "experience_level": experience_level,
        "posted_date": date.today().isoformat(),
        "apply_url": apply_url,
        "source": "linkedin_saved",
        "skills_matched": ["Python", "Backend", "Software Development"],
        "match_score": 0.95,  # High priority for saved jobs
        "status": "saved"  # Special status for LinkedIn saved jobs
    }
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        result = supabase.table('jobs').insert(job_data).execute()
        if result.data:
            job_id = result.data[0]['id']
            print(f"✅ Saved: {title} at {company} (ID: {job_id[:8]}...)")
            return True
        else:
            print(f"❌ Failed to save: {title}")
            return False
            
    except Exception as e:
        if 'duplicate' in str(e).lower():
            print(f"⚠️  Already exists: {title} at {company}")
            return True
        else:
            print(f"❌ Error saving: {e}")
            return False

def main():
    """Import your LinkedIn saved jobs here"""
    print("🔗 LinkedIn Saved Jobs Import")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 Instructions:")
    print("1. Go to your LinkedIn saved jobs page")
    print("2. Copy job details from each saved job")
    print("3. Add them using save_linkedin_job() calls below")
    print("4. Run this script to import them")
    print()
    
    print("💾 Importing your LinkedIn saved jobs...")
    
    saved_count = 0
    
    # ADD YOUR LINKEDIN SAVED JOBS HERE
    # Example template - replace with your actual saved jobs:
    
    # saved_count += save_linkedin_job(
    #     title="Backend Developer",
    #     company="Volvo Cars",
    #     location="Gothenburg, Sweden",
    #     description="Develop backend systems for connected cars...",
    #     apply_url="https://linkedin.com/jobs/view/123456",
    #     salary_range="600,000 - 800,000 SEK"
    # )
    
    # Add more jobs here by copying the template above
    
    print(f"\n🎯 IMPORT RESULTS:")
    print(f"   💾 Jobs imported: {saved_count}")
    
    if saved_count == 0:
        print("\n📝 TO ADD YOUR JOBS:")
        print("1. Edit this file (linkedin_saved_jobs_import.py)")
        print("2. Uncomment and modify the save_linkedin_job() calls")
        print("3. Replace with your actual LinkedIn saved job details")
        print("4. Run the script again")
        print()
        print("🔗 Your LinkedIn saved jobs URL:")
        print("https://www.linkedin.com/my-items/saved-jobs/")
    else:
        print(f"\n✅ Successfully imported {saved_count} jobs!")
        print("Run 'python check_jobs_supabase.py' to see all jobs")

if __name__ == "__main__":
    main()