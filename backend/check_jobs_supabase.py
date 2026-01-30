#!/usr/bin/env python3
"""
Script to check job count in Supabase database using Supabase client
Shows jobs saved today and total job count
"""

import os
import sys
from datetime import datetime, date
from typing import Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def check_job_counts() -> Dict[str, Any]:
    """
    Check job counts in Supabase database using Supabase client
    """
    print("🔍 Connecting to Supabase database...")
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
        
        results = {}
        today_str = date.today().isoformat()
        
        # Check jobs table
        print("🔍 Checking 'jobs' table...")
        
        try:
            # Total jobs
            total_jobs_response = supabase.table('jobs').select('id', count='exact').execute()
            total_jobs = total_jobs_response.count
            
            # Jobs created today
            today_jobs_response = supabase.table('jobs').select('id', count='exact').gte('created_at', today_str).execute()
            today_jobs = today_jobs_response.count
            
            # Jobs by status
            status_response = supabase.table('jobs').select('status, id', count='exact').execute()
            all_jobs = status_response.data
            
            # Count statuses manually since Supabase doesn't support GROUP BY with count
            status_counts = {}
            for job in all_jobs:
                status = job.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Recent jobs (last 7 days)
            recent_jobs_response = supabase.table('jobs').select('title, company, source, status, created_at').order('created_at', desc=True).limit(10).execute()
            recent_jobs = recent_jobs_response.data
            
            results['jobs'] = {
                'total_count': total_jobs,
                'today_count': today_jobs,
                'status_breakdown': status_counts,
                'recent_jobs': recent_jobs
            }
            
            print(f"   📊 Total jobs: {total_jobs}")
            print(f"   🆕 Jobs added today: {today_jobs}")
            print(f"   📈 Status breakdown:")
            for status, count in status_counts.items():
                print(f"      • {status}: {count}")
            print()
            
        except Exception as e:
            print(f"   ⚠️  Could not access 'jobs' table: {e}")
            results['jobs'] = {'error': str(e)}
        
        # Check applications table
        print("🔍 Checking 'applications' table...")
        
        try:
            # Total applications
            total_apps_response = supabase.table('applications').select('id', count='exact').execute()
            total_applications = total_apps_response.count
            
            # Applications created today
            today_apps_response = supabase.table('applications').select('id', count='exact').gte('created_at', today_str).execute()
            today_applications = today_apps_response.count
            
            results['applications'] = {
                'total_count': total_applications,
                'today_count': today_applications
            }
            
            print(f"   📊 Total applications: {total_applications}")
            print(f"   🆕 Applications created today: {today_applications}")
            print()
            
        except Exception as e:
            print(f"   ⚠️  Could not access 'applications' table: {e}")
            results['applications'] = {'error': str(e)}
        
        # Check users table
        print("🔍 Checking 'users' table...")
        
        try:
            total_users_response = supabase.table('users').select('id', count='exact').execute()
            total_users = total_users_response.count
            
            results['users'] = {'total_count': total_users}
            
            print(f"   📊 Total users: {total_users}")
            print()
            
        except Exception as e:
            print(f"   ⚠️  Could not access 'users' table: {e}")
            results['users'] = {'error': str(e)}
        
        # Show recent activity summary
        print("📈 ACTIVITY SUMMARY FOR TODAY:")
        print("=" * 40)
        if 'jobs' in results and 'error' not in results['jobs']:
            print(f"🔍 Jobs discovered: {results['jobs']['today_count']}")
        if 'applications' in results and 'error' not in results['applications']:
            print(f"📄 Applications created: {results['applications']['today_count']}")
        
        print(f"📅 Date: {date.today().strftime('%Y-%m-%d')}")
        print("=" * 40)
        
        return results
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return {'error': str(e)}

def main():
    """Main function"""
    print("JobHunter Database Status Check")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = check_job_counts()
    
    if 'error' in results:
        print(f"\n❌ Failed to check database: {results['error']}")
        sys.exit(1)
    else:
        print("\n✅ Database check completed successfully!")
        
        # Calculate total jobs
        total_jobs = 0
        if 'jobs' in results and 'error' not in results['jobs']:
            total_jobs = results['jobs']['total_count']
        
        print(f"\n🎯 TOTAL JOBS: {total_jobs} jobs in database")
        
        # Show some recent jobs if available
        if 'jobs' in results and 'recent_jobs' in results['jobs'] and results['jobs']['recent_jobs']:
            print(f"\n📋 RECENT JOBS (last 10):")
            for i, job in enumerate(results['jobs']['recent_jobs'][:5], 1):
                title = job.get('title', 'Unknown')
                company = job.get('company', 'Unknown')
                source = job.get('source', 'Unknown')
                created = job.get('created_at', '')[:10] if job.get('created_at') else 'Unknown'
                print(f"   {i}. {title} at {company} ({source}) - {created}")

if __name__ == "__main__":
    main()