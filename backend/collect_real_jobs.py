#!/usr/bin/env python3
"""
Test real job collection from various sources
"""

import os
import sys
import asyncio
from datetime import datetime, date
from typing import List, Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.services.google_jobs_service import GoogleJobsService
    from app.services.arbetsformedlingen_service import ArbetsformedlingenService
    from app.services.supabase_service import SupabaseService
    from supabase import create_client, Client
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

async def test_google_jobs():
    """Test Google Jobs service"""
    print("🔍 Testing Google Jobs Service...")
    try:
        service = GoogleJobsService()
        jobs = await service.search_jobs('python developer', 'Sweden', num_results=5)
        print(f"   📊 Found {len(jobs)} jobs from Google Jobs")
        
        if jobs:
            print("   📋 Sample jobs:")
            for job in jobs[:3]:
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                print(f"      • {title} at {company} ({location})")
        
        return jobs
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

async def test_arbetsformedlingen():
    """Test Arbetsförmedlingen service"""
    print("🔍 Testing Arbetsförmedlingen Service...")
    try:
        service = ArbetsformedlingenService()
        jobs = await service.search_jobs('developer', 'Stockholm', num_results=5)
        print(f"   📊 Found {len(jobs)} jobs from Arbetsförmedlingen")
        
        if jobs:
            print("   📋 Sample jobs:")
            for job in jobs[:3]:
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                print(f"      • {title} at {company} ({location})")
        
        return jobs
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def save_jobs_to_database(jobs: List[Dict[str, Any]], source: str):
    """Save collected jobs to database"""
    if not jobs:
        print(f"   ⚠️  No jobs to save from {source}")
        return 0
    
    print(f"💾 Saving {len(jobs)} jobs from {source} to database...")
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        saved_count = 0
        for job in jobs:
            try:
                # Prepare job data for database
                job_data = {
                    "title": job.get('title', 'Unknown Title'),
                    "company": job.get('company', 'Unknown Company'),
                    "location": job.get('location', ''),
                    "description": job.get('description', ''),
                    "requirements": job.get('requirements', ''),
                    "salary_range": job.get('salary_range', ''),
                    "job_type": job.get('job_type', 'Full-time'),
                    "experience_level": job.get('experience_level', ''),
                    "posted_date": job.get('posted_date', date.today().isoformat()),
                    "apply_url": job.get('apply_url', ''),
                    "source": source,
                    "skills_matched": job.get('skills_matched', []),
                    "match_score": job.get('match_score', 0.0),
                    "status": "found"
                }
                
                result = supabase.table('jobs').insert(job_data).execute()
                if result.data:
                    saved_count += 1
                    print(f"   ✅ Saved: {job_data['title']} at {job_data['company']}")
                
            except Exception as e:
                error_msg = str(e).lower()
                if 'duplicate' in error_msg or 'unique' in error_msg:
                    print(f"   ⚠️  Duplicate job skipped: {job.get('title', 'Unknown')}")
                else:
                    print(f"   ❌ Error saving job: {e}")
        
        print(f"   📊 Successfully saved {saved_count}/{len(jobs)} jobs from {source}")
        return saved_count
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return 0

def main():
    """Main function to collect and save real jobs"""
    print("🚀 JobHunter Real Job Collection")
    print("=" * 60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    async def run_collection():
        total_saved = 0
        
        # Test Google Jobs
        google_jobs = await test_google_jobs()
        if google_jobs:
            total_saved += save_jobs_to_database(google_jobs, 'google_jobs')
        print()
        
        # Test Arbetsförmedlingen
        af_jobs = await test_arbetsformedlingen()
        if af_jobs:
            total_saved += save_jobs_to_database(af_jobs, 'arbetsformedlingen')
        print()
        
        print(f"🎯 TOTAL RESULTS:")
        print(f"   💾 Total jobs saved: {total_saved}")
        
        if total_saved > 0:
            print("\n✅ Real job collection completed successfully!")
            print("\n🔧 NEXT STEPS:")
            print("1. Run 'python check_jobs_supabase.py' to see all saved jobs")
            print("2. Check your Supabase dashboard to view the data")
        else:
            print("\n⚠️  No real jobs were collected. This might be due to:")
            print("- API rate limits")
            print("- Service configuration issues")
            print("- Network connectivity")
            print("- Search parameters too restrictive")
    
    # Run the async collection
    asyncio.run(run_collection())

if __name__ == "__main__":
    main()