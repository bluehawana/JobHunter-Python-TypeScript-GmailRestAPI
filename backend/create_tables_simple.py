#!/usr/bin/env python3
"""
Create database tables using Supabase service key for direct SQL execution
"""

import os
import sys
from typing import List

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def create_tables_manually():
    """Create tables one by one with basic structure"""
    print("🚀 Creating Database Tables Manually")
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
        
        # Since we can't execute DDL with anon key, let's try inserting test data
        # to see what tables already exist
        
        test_tables = [
            ('users', {'email': 'test@example.com', 'full_name': 'Test User'}),
            ('jobs', {'title': 'Test Job', 'company': 'Test Company'}),
            ('applications', {'user_id': '123e4567-e89b-12d3-a456-426614174000', 'job_id': '123e4567-e89b-12d3-a456-426614174001'})
        ]
        
        existing_tables = []
        
        for table_name, test_data in test_tables:
            try:
                # Try to select from table to see if it exists
                result = supabase.table(table_name).select('*').limit(1).execute()
                existing_tables.append(table_name)
                print(f"   ✅ Table '{table_name}' exists")
            except Exception as e:
                print(f"   ❌ Table '{table_name}' does not exist: {str(e)[:100]}...")
        
        if existing_tables:
            print(f"\n📊 Found {len(existing_tables)} existing tables: {', '.join(existing_tables)}")
        else:
            print("\n❌ No tables found. You need to create them manually.")
            print("\n🔧 SOLUTIONS:")
            print("1. Update DATABASE_URL with real password")
            print("2. Use Supabase Dashboard SQL Editor")
            print("3. Get the service role key (not anon key)")
            
        return len(existing_tables) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_manual_instructions():
    """Show step-by-step manual instructions"""
    print("\n" + "=" * 60)
    print("📋 MANUAL DATABASE SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("Since automatic setup failed, here's what to do:")
    print()
    print("1. 🌐 Go to Supabase Dashboard:")
    print("   https://supabase.com/dashboard/project/chcdebpjwallysedcfsq")
    print()
    print("2. 🔧 Click 'SQL Editor' in the left sidebar")
    print()
    print("3. 📝 Create a new query and paste this SQL:")
    print()
    
    # Show essential table creation SQL
    essential_sql = """-- Essential tables for JobHunter
CREATE TABLE IF NOT EXISTS jobs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    requirements TEXT,
    salary_range VARCHAR(100),
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    posted_date DATE,
    apply_url TEXT,
    source VARCHAR(100),
    skills_matched TEXT[],
    match_score DECIMAL(3,2),
    status VARCHAR(50) DEFAULT 'found',
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS applications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'prepared',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);"""
    
    print(essential_sql)
    print()
    print("4. ▶️  Click 'RUN' to execute")
    print()
    print("5. ✅ Verify by running: python check_existing_tables.py")

def main():
    """Main function"""
    success = create_tables_manually()
    
    if not success:
        show_manual_instructions()
        print("\n🔧 After creating tables manually, your job hunting app will work!")
    else:
        print("\n🎉 Some tables already exist! Run check_existing_tables.py to verify.")

if __name__ == "__main__":
    main()