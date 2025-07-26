#!/usr/bin/env python3
"""
Create the job_applications table in Supabase database

This script runs the SQL schema to create the table with all required columns.
"""

import asyncio
import os
from supabase import create_client, Client

# Supabase configuration - load from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("❌ Missing required environment variables: SUPABASE_URL and SUPABASE_ANON_KEY")
    print("Please set these environment variables before running the script.")
    exit(1)

def create_table():
    """Create the job_applications table"""
    
    print("🗄️  Creating job_applications table in Supabase...")
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # SQL to create the table
        sql_schema = """
        -- Job Applications Tracking Table for JobHunter
        CREATE TABLE IF NOT EXISTS job_applications (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            
            -- Basic Job Information
            company_name VARCHAR(255) NOT NULL,
            job_title VARCHAR(255) NOT NULL,
            job_description TEXT,
            published_date DATE,
            application_link TEXT,
            
            -- Contact Information
            contact_person VARCHAR(255),
            contact_email VARCHAR(255),
            contact_phone VARCHAR(50),
            
            -- Application Status
            application_status VARCHAR(50) DEFAULT 'applied' CHECK (
                application_status IN (
                    'found', 'applied', 'under_review', 'interview_scheduled', 
                    'interviewed', 'offer_received', 'rejected', 'withdrawn', 'no_response'
                )
            ),
            applied_date DATE DEFAULT CURRENT_DATE,
            
            -- Interview Process
            interview_rounds JSONB DEFAULT '[]',
            interview_notes TEXT,
            
            -- Communication Log
            communications JSONB DEFAULT '[]',
            
            -- Final Result
            final_result VARCHAR(50) CHECK (
                final_result IN ('pending', 'hired', 'rejected', 'withdrawn', 'no_response')
            ) DEFAULT 'pending',
            result_date DATE,
            
            -- Additional Information
            salary_range VARCHAR(100),
            location VARCHAR(255),
            work_type VARCHAR(50) CHECK (work_type IN ('remote', 'hybrid', 'onsite')),
            priority_level INTEGER DEFAULT 3 CHECK (priority_level BETWEEN 1 AND 5),
            
            -- Notes and Memo
            memo TEXT,
            internal_notes TEXT,
            
            -- Metadata
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Email Integration
            email_thread_id VARCHAR(255),
            last_email_received TIMESTAMP WITH TIME ZONE
        );
        
        -- Create indexes for better query performance
        CREATE INDEX IF NOT EXISTS idx_job_applications_company ON job_applications(company_name);
        CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(application_status);
        CREATE INDEX IF NOT EXISTS idx_job_applications_applied_date ON job_applications(applied_date);
        CREATE INDEX IF NOT EXISTS idx_job_applications_final_result ON job_applications(final_result);
        CREATE INDEX IF NOT EXISTS idx_job_applications_email_thread ON job_applications(email_thread_id);
        
        -- Create updated_at trigger function
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        -- Create trigger
        DROP TRIGGER IF EXISTS update_job_applications_updated_at ON job_applications;
        CREATE TRIGGER update_job_applications_updated_at 
            BEFORE UPDATE ON job_applications 
            FOR EACH ROW 
            EXECUTE FUNCTION update_updated_at_column();
        """
        
        # Execute the SQL
        result = supabase.rpc('exec_sql', {'sql': sql_schema})
        print("✅ Table created successfully!")
        
        # Test the table by inserting a sample record
        test_data = {
            'company_name': 'Test Company',
            'job_title': 'Test Job',
            'job_description': 'This is a test job to verify the table structure',
            'application_status': 'found',
            'final_result': 'pending'
        }
        
        result = supabase.table('job_applications').insert(test_data).execute()
        if result.data:
            print("✅ Test record inserted successfully!")
            
            # Clean up test record
            test_id = result.data[0]['id']
            supabase.table('job_applications').delete().eq('id', test_id).execute()
            print("✅ Test record cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        print("\n💡 Alternative: Run this SQL manually in your Supabase SQL editor:")
        print("\n" + sql_schema)
        return False

if __name__ == "__main__":
    print("JobHunter Database Setup")
    print("=" * 30)
    
    success = create_table()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the job processing script.")
    else:
        print("\n⚠️  Database setup failed.")
        print("Please create the table manually in Supabase SQL editor.")