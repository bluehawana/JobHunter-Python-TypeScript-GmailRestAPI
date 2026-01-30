#!/usr/bin/env python3
"""
Test if the job_applications table exists in Supabase
"""

import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.supabase_service import supabase_service

async def test_table():
    """Test if the table exists and is accessible"""
    
    print("🔍 Testing job_applications table...")
    
    try:
        # Try to get applications (should work even if empty)
        applications = await supabase_service.get_job_applications(limit=5)
        print(f"✅ Table exists! Found {len(applications)} existing applications")
        
        # Test statistics
        stats = await supabase_service.get_application_statistics()
        print(f"📊 Total applications in database: {stats.get('total_applications', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return False

if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set the following environment variables:")
        for var in missing_vars:
            if var == 'SUPABASE_URL':
                print(f"  export {var}='https://your-project.supabase.co'")
            elif var == 'SUPABASE_ANON_KEY':
                print(f"  export {var}='your-anon-key'")
        sys.exit(1)
    
    result = asyncio.run(test_table())
    
    if result:
        print("\n🎉 Database is ready! You can now run the job processing script.")
    else:
        print("\n⚠️  Database table needs to be created or fixed.")