#!/usr/bin/env python3
"""
Script to check what tables exist in Supabase database
"""

import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def check_existing_tables():
    """
    Check what tables exist in the Supabase database
    """
    print("🔍 Checking existing tables in Supabase database...")
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
        
        # Try to get schema information using a direct SQL query
        try:
            # Query to get all tables
            result = supabase.rpc('get_schema_info').execute()
            print("📋 Schema info:", result)
        except Exception as e:
            print(f"   ⚠️  Could not get schema info: {e}")
        
        # Try some common table names that might exist
        common_tables = ['users', 'jobs', 'applications', 'profiles', 'auth', 'storage']
        
        existing_tables = []
        for table_name in common_tables:
            try:
                response = supabase.table(table_name).select('*').limit(1).execute()
                existing_tables.append(table_name)
                print(f"   ✅ Table '{table_name}' exists")
            except Exception as e:
                print(f"   ❌ Table '{table_name}' does not exist: {e}")
        
        print()
        print(f"📊 SUMMARY:")
        print(f"   Found {len(existing_tables)} tables: {', '.join(existing_tables) if existing_tables else 'None'}")
        
        if not existing_tables:
            print()
            print("💡 RECOMMENDATION:")
            print("   Your Supabase database appears to be empty.")
            print("   You need to run the database schema setup first.")
            print("   The schema is defined in: backend/database_schema.sql")
            print()
            print("🔧 NEXT STEPS:")
            print("   1. Go to your Supabase dashboard")
            print("   2. Navigate to SQL Editor")
            print("   3. Run the SQL commands from database_schema.sql")
            print("   4. Or use the Supabase CLI to apply migrations")
        
        return existing_tables
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return []

def main():
    """Main function"""
    print("JobHunter Database Schema Check")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tables = check_existing_tables()
    
    if not tables:
        print("\n🚨 Database is empty - tables need to be created")
        sys.exit(1)
    else:
        print(f"\n✅ Found {len(tables)} existing tables")

if __name__ == "__main__":
    main()