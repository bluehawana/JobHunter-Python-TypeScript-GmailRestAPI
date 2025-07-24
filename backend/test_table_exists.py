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
    # Set up environment
    os.environ["SUPABASE_URL"] = "https://chcdebpjwallysedcfsq.supabase.co"
    os.environ["SUPABASE_ANON_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNoY2RlYnBqd2FsbHlzZWRjZnNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMzNTU5OTUsImV4cCI6MjA2ODkzMTk5NX0.YXdUPS9q1O1SF0aRwYD-qG8NfUQrGD4U4MJSOwp4IrM"
    
    result = asyncio.run(test_table())
    
    if result:
        print("\n🎉 Database is ready! You can now run the job processing script.")
    else:
        print("\n⚠️  Database table needs to be created or fixed.")