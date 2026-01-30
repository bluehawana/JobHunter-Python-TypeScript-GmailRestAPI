#!/usr/bin/env python3
"""
Script to create database tables in Supabase from SQL schema files
"""

import os
import sys
from typing import List

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def read_sql_file(file_path: str) -> str:
    """Read SQL content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""

def execute_sql_statements(supabase: Client, sql_content: str, schema_name: str) -> bool:
    """Execute SQL statements one by one"""
    print(f"🔧 Executing {schema_name} schema...")
    
    # Split SQL content into individual statements
    # Remove comments and empty lines, split by semicolon
    statements = []
    lines = sql_content.split('\n')
    current_statement = []
    
    for line in lines:
        # Skip comment lines and empty lines
        line = line.strip()
        if line.startswith('--') or line.startswith('"""') or not line:
            continue
            
        current_statement.append(line)
        
        # If line ends with semicolon, we have a complete statement
        if line.endswith(';'):
            statement = ' '.join(current_statement).strip()
            if statement and statement != ';':
                statements.append(statement)
            current_statement = []
    
    # Add any remaining statement
    if current_statement:
        statement = ' '.join(current_statement).strip()
        if statement:
            statements.append(statement)
    
    print(f"   Found {len(statements)} SQL statements to execute")
    
    success_count = 0
    for i, statement in enumerate(statements, 1):
        try:
            # For table creation and other DDL, we use rpc with a custom function
            # or direct SQL execution if available
            print(f"   Executing statement {i}/{len(statements)}...")
            
            # Try to execute the statement
            # Note: Supabase client might not support all DDL operations directly
            # We might need to use the REST API or PostgreSQL connection
            result = supabase.rpc('exec_sql', {'sql': statement}).execute()
            print(f"   ✅ Statement {i} executed successfully")
            success_count += 1
            
        except Exception as e:
            # Some statements might fail if tables already exist, that's OK
            error_msg = str(e).lower()
            if 'already exists' in error_msg or 'relation' in error_msg:
                print(f"   ⚠️  Statement {i} - already exists (skipping): {statement[:50]}...")
                success_count += 1
            else:
                print(f"   ❌ Statement {i} failed: {e}")
                print(f"      SQL: {statement[:100]}...")
    
    print(f"   📊 Successfully executed {success_count}/{len(statements)} statements")
    return success_count == len(statements)

def create_tables_with_direct_sql(supabase: Client, sql_content: str, schema_name: str) -> bool:
    """Alternative method: try to create tables using direct SQL execution"""
    print(f"🔧 Attempting direct SQL execution for {schema_name}...")
    
    try:
        # Try executing the entire SQL content at once
        # This might work if the Supabase client supports it
        result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()
        print(f"   ✅ {schema_name} schema executed successfully")
        return True
    except Exception as e:
        print(f"   ❌ Direct SQL execution failed: {e}")
        return False

def setup_database_schema():
    """
    Set up the complete database schema
    """
    print("🚀 JobHunter Database Setup")
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
        
        # Read SQL schema files
        schema_files = [
            ('database_schema.sql', 'Main Database Schema'),
        ]
        
        all_success = True
        
        for file_name, description in schema_files:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            
            if not os.path.exists(file_path):
                print(f"❌ Schema file not found: {file_path}")
                all_success = False
                continue
            
            print(f"📋 Processing {description}")
            print(f"   File: {file_path}")
            
            sql_content = read_sql_file(file_path)
            if not sql_content:
                print(f"   ❌ Could not read SQL content from {file_name}")
                all_success = False
                continue
            
            # Try to execute the SQL
            print(f"   ⚠️  Note: Direct SQL execution might not be supported by Supabase client")
            print(f"   📋 SQL content length: {len(sql_content)} characters")
            print()
            print("   🔧 MANUAL EXECUTION REQUIRED:")
            print("   1. Copy the SQL content below")
            print("   2. Go to your Supabase Dashboard")
            print("   3. Navigate to SQL Editor")
            print("   4. Paste and execute the SQL")
            print()
            print("=" * 60)
            print(f"-- {description}")
            print("=" * 60)
            print(sql_content)
            print("=" * 60)
            print()
        
        return all_success
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def main():
    """Main function"""
    success = setup_database_schema()
    
    if success:
        print("✅ Database schema setup completed!")
        print("\n🔧 NEXT STEPS:")
        print("1. Execute the SQL shown above in your Supabase Dashboard")
        print("2. Run 'python check_existing_tables.py' to verify tables were created")
        print("3. Run 'python check_job_count.py' to test the setup")
    else:
        print("❌ Database schema setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()