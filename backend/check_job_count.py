#!/usr/bin/env python3
"""
Script to check job count in Supabase database
Shows jobs saved today and total job count
"""

import asyncio
import os
import sys
from datetime import datetime, date
from typing import Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import asyncpg
from app.core.config import settings

async def check_job_counts() -> Dict[str, Any]:
    """
    Check job counts in Supabase database
    """
    print("🔍 Connecting to Supabase database...")
    print("=" * 60)
    
    try:
        # Extract database connection details from DATABASE_URL
        # Format: postgresql://postgres.[password]@db.chcdebpjwallysedcfsq.supabase.co:5432/postgres
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        print(f"📊 Database URL: {database_url[:50]}...")
        
        # Connect to database
        conn = await asyncpg.connect(database_url)
        
        print("✅ Connected to Supabase database successfully!")
        print()
        
        # Check if tables exist
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('jobs', 'aggregated_jobs', 'applications', 'users');
        """
        
        existing_tables = await conn.fetch(tables_query)
        table_names = [row['table_name'] for row in existing_tables]
        
        print("📋 Available tables:")
        for table in table_names:
            print(f"   ✓ {table}")
        print()
        
        results = {}
        
        # Check jobs table
        if 'jobs' in table_names:
            print("🔍 Checking 'jobs' table...")
            
            # Total jobs
            total_jobs = await conn.fetchval("SELECT COUNT(*) FROM jobs")
            
            # Jobs created today
            today_jobs = await conn.fetchval("""
                SELECT COUNT(*) FROM jobs 
                WHERE DATE(created_at) = $1
            """, date.today())
            
            # Jobs by status
            status_counts = await conn.fetch("""
                SELECT status, COUNT(*) as count 
                FROM jobs 
                GROUP BY status 
                ORDER BY count DESC
            """)
            
            # Recent jobs (last 7 days)
            recent_jobs = await conn.fetch("""
                SELECT title, company, source, status, created_at
                FROM jobs 
                WHERE created_at >= NOW() - INTERVAL '7 days'
                ORDER BY created_at DESC
                LIMIT 10
            """)
            
            results['jobs'] = {
                'total_count': total_jobs,
                'today_count': today_jobs,
                'status_breakdown': {row['status']: row['count'] for row in status_counts},
                'recent_jobs': [dict(row) for row in recent_jobs]
            }
            
            print(f"   📊 Total jobs: {total_jobs}")
            print(f"   🆕 Jobs added today: {today_jobs}")
            print(f"   📈 Status breakdown:")
            for status, count in results['jobs']['status_breakdown'].items():
                print(f"      • {status}: {count}")
            print()
        
        # Check aggregated_jobs table (if exists)
        if 'aggregated_jobs' in table_names:
            print("🔍 Checking 'aggregated_jobs' table...")
            
            total_aggregated = await conn.fetchval("SELECT COUNT(*) FROM aggregated_jobs")
            today_aggregated = await conn.fetchval("""
                SELECT COUNT(*) FROM aggregated_jobs 
                WHERE DATE(discovered_at) = $1
            """, date.today())
            
            # Source breakdown
            source_counts = await conn.fetch("""
                SELECT source, COUNT(*) as count 
                FROM aggregated_jobs 
                GROUP BY source 
                ORDER BY count DESC
            """)
            
            results['aggregated_jobs'] = {
                'total_count': total_aggregated,
                'today_count': today_aggregated,
                'source_breakdown': {row['source']: row['count'] for row in source_counts}
            }
            
            print(f"   📊 Total aggregated jobs: {total_aggregated}")
            print(f"   🆕 Jobs discovered today: {today_aggregated}")
            print(f"   🔗 Source breakdown:")
            for source, count in results['aggregated_jobs']['source_breakdown'].items():
                print(f"      • {source}: {count}")
            print()
        
        # Check applications table
        if 'applications' in table_names:
            print("🔍 Checking 'applications' table...")
            
            total_applications = await conn.fetchval("SELECT COUNT(*) FROM applications")
            today_applications = await conn.fetchval("""
                SELECT COUNT(*) FROM applications 
                WHERE DATE(created_at) = $1
            """, date.today())
            
            results['applications'] = {
                'total_count': total_applications,
                'today_count': today_applications
            }
            
            print(f"   📊 Total applications: {total_applications}")
            print(f"   🆕 Applications created today: {today_applications}")
            print()
        
        # Check users table
        if 'users' in table_names:
            print("🔍 Checking 'users' table...")
            
            total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
            results['users'] = {'total_count': total_users}
            
            print(f"   📊 Total users: {total_users}")
            print()
        
        # Show recent activity summary
        print("📈 ACTIVITY SUMMARY FOR TODAY:")
        print("=" * 40)
        if 'jobs' in results:
            print(f"🔍 Regular jobs discovered: {results['jobs']['today_count']}")
        if 'aggregated_jobs' in results:
            print(f"🔗 Multi-source jobs: {results['aggregated_jobs']['today_count']}")
        if 'applications' in results:
            print(f"📄 Applications created: {results['applications']['today_count']}")
        
        print(f"📅 Date: {date.today().strftime('%Y-%m-%d')}")
        print("=" * 40)
        
        await conn.close()
        return results
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return {'error': str(e)}

async def main():
    """Main function"""
    print("JobHunter Database Status Check")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    results = await check_job_counts()
    
    if 'error' in results:
        print(f"\n❌ Failed to check database: {results['error']}")
        sys.exit(1)
    else:
        print("\n✅ Database check completed successfully!")
        
        # Calculate total jobs across all tables
        total_all_jobs = 0
        if 'jobs' in results:
            total_all_jobs += results['jobs']['total_count']
        if 'aggregated_jobs' in results:
            total_all_jobs += results['aggregated_jobs']['total_count']
        
        print(f"\n🎯 GRAND TOTAL: {total_all_jobs} jobs in database")

if __name__ == "__main__":
    asyncio.run(main())