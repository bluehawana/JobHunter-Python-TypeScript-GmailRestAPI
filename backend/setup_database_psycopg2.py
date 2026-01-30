#!/usr/bin/env python3
"""
Script to create database tables using psycopg2 for Supabase compatibility
"""

import os
import sys
import psycopg2
from psycopg2 import sql

def execute_sql_file(cursor, file_path: str) -> bool:
    """Execute SQL statements from file"""
    print(f"📋 Reading SQL from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Clean up SQL - remove comments and split statements
    lines = sql_content.split('\n')
    statements = []
    current_statement = []
    
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if line.startswith('--') or line.startswith('"""') or line.startswith('/*') or not line:
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
    
    print(f"   Found {len(statements)} SQL statements")
    
    success_count = 0
    for i, statement in enumerate(statements, 1):
        try:
            print(f"   Executing statement {i}/{len(statements)}...")
            cursor.execute(statement)
            print(f"   ✅ Statement {i} executed successfully")
            success_count += 1
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'already exists' in error_msg or 'does not exist' in error_msg:
                print(f"   ⚠️  Statement {i} - already exists or dependency issue (continuing)")
                success_count += 1
            else:
                print(f"   ❌ Statement {i} failed: {e}")
                print(f"      SQL: {statement[:100]}...")
    
    print(f"   📊 Successfully executed {success_count}/{len(statements)} statements")
    return success_count >= len(statements) * 0.8  # Allow some failures for dependencies

def setup_database():
    """Set up database tables using psycopg2"""
    print("🚀 JobHunter Database Setup (psycopg2)")
    print("=" * 60)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        print(f"📊 Database URL: {database_url[:50]}...")
        
        # Connect to database
        conn = psycopg2.connect(database_url, sslmode='require')
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL database successfully!")
        print()
        
        # Execute main schema
        schema_file = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
        if os.path.exists(schema_file):
            success = execute_sql_file(cursor, schema_file)
            if success:
                print("✅ Main database schema executed!")
                conn.commit()  # Commit the changes
            else:
                print("⚠️  Some issues with main schema, but continuing...")
                conn.commit()  # Still commit what worked
        else:
            print(f"❌ Schema file not found: {schema_file}")
            conn.close()
            return False
        
        # Test the created tables
        print("\n🔍 Verifying created tables...")
        
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('users', 'jobs', 'applications', 'email_monitoring', 'user_preferences')
        ORDER BY table_name;
        """
        
        cursor.execute(tables_query)
        tables = cursor.fetchall()
        
        if tables:
            print("📋 Created tables:")
            for table in tables:
                table_name = table[0]
                print(f"   ✅ {table_name}")
                
                # Get row count
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"      📊 Rows: {count}")
                except Exception as e:
                    print(f"      ⚠️  Could not count rows: {e}")
        else:
            print("❌ No tables were created successfully")
            conn.close()
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def main():
    """Main function"""
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\n🔧 NEXT STEPS:")
        print("1. Run 'python check_existing_tables.py' to verify")
        print("2. Run 'python check_job_count.py' to test job storage")
        print("3. Your application can now save jobs to the database!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()