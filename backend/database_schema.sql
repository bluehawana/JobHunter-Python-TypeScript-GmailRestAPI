"""
Database schema for Supabase PostgreSQL
Run this after setting up your Supabase project
"""

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Profile information
    skills TEXT[],
    experience_level VARCHAR(50),
    preferred_locations TEXT[],
    salary_min INTEGER,
    salary_max INTEGER,
    job_types TEXT[],
    
    -- Gmail integration
    gmail_connected BOOLEAN DEFAULT false,
    gmail_credentials JSONB,
    gmail_connected_at TIMESTAMP WITH TIME ZONE
);

-- Jobs table
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
    source VARCHAR(100), -- linkedin, indeed, etc.
    
    -- Job matching
    skills_matched TEXT[],
    match_score DECIMAL(3,2),
    
    -- Processing status
    status VARCHAR(50) DEFAULT 'found', -- found, processed, applied, rejected
    processed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Application documents
    cv_path VARCHAR(500),
    cover_letter_path VARCHAR(500),
    
    -- Email tracking
    email_sent BOOLEAN DEFAULT false,
    email_sent_at TIMESTAMP WITH TIME ZONE,
    email_subject VARCHAR(500),
    email_body TEXT,
    
    -- Application status
    status VARCHAR(50) DEFAULT 'prepared', -- prepared, sent, responded, rejected
    response_received BOOLEAN DEFAULT false,
    response_date TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, job_id)
);

-- Email monitoring table
CREATE TABLE IF NOT EXISTS email_monitoring (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Email details
    gmail_message_id VARCHAR(255),
    subject VARCHAR(500),
    sender VARCHAR(255),
    received_date TIMESTAMP WITH TIME ZONE,
    
    -- Job extraction
    job_title VARCHAR(500),
    company_name VARCHAR(255),
    job_url TEXT,
    
    -- Processing status
    processed BOOLEAN DEFAULT false,
    job_created BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    
    -- Job search preferences
    keywords TEXT[],
    excluded_companies TEXT[],
    preferred_remote BOOLEAN DEFAULT false,
    max_commute_distance INTEGER,
    
    -- Automation settings
    automation_enabled BOOLEAN DEFAULT false,
    daily_application_limit INTEGER DEFAULT 5,
    working_hours_start TIME DEFAULT '09:00',
    working_hours_end TIME DEFAULT '17:00',
    
    -- Notification preferences
    email_notifications BOOLEAN DEFAULT true,
    daily_summary BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_email_monitoring_processed ON email_monitoring(processed);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_monitoring ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Create policies (users can only access their own data)
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own applications" ON applications FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own email monitoring" ON email_monitoring FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own preferences" ON user_preferences FOR ALL USING (auth.uid() = user_id);

-- Jobs table is public (read-only for job discovery)
CREATE POLICY "Public jobs are viewable by everyone" ON jobs FOR SELECT USING (true);