-- Job Applications Tracking Table for JobHunter
-- This table tracks all job applications and their progress

CREATE TABLE job_applications (
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
    interview_rounds JSONB DEFAULT '[]', -- Array of interview objects
    interview_notes TEXT,
    
    -- Communication Log
    communications JSONB DEFAULT '[]', -- Array of communication objects
    
    -- Final Result
    final_result VARCHAR(50) CHECK (
        final_result IN ('pending', 'hired', 'rejected', 'withdrawn', 'no_response')
    ) DEFAULT 'pending',
    result_date DATE,
    
    -- Additional Information
    salary_range VARCHAR(100),
    location VARCHAR(255),
    work_type VARCHAR(50) CHECK (work_type IN ('remote', 'hybrid', 'onsite')),
    priority_level INTEGER DEFAULT 3 CHECK (priority_level BETWEEN 1 AND 5), -- 1=highest, 5=lowest
    
    -- Notes and Memo
    memo TEXT,
    internal_notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Email Integration
    email_thread_id VARCHAR(255), -- For tracking email conversations
    last_email_received TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX idx_job_applications_company ON job_applications(company_name);
CREATE INDEX idx_job_applications_status ON job_applications(application_status);
CREATE INDEX idx_job_applications_applied_date ON job_applications(applied_date);
CREATE INDEX idx_job_applications_final_result ON job_applications(final_result);
CREATE INDEX idx_job_applications_email_thread ON job_applications(email_thread_id);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_job_applications_updated_at 
    BEFORE UPDATE ON job_applications 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Example of how interview_rounds JSONB might look:
-- [
--   {
--     "round": 1,
--     "type": "phone_screen",
--     "date": "2024-01-15",
--     "interviewer": "John Doe",
--     "notes": "Good technical discussion",
--     "result": "passed"
--   },
--   {
--     "round": 2,
--     "type": "technical",
--     "date": "2024-01-22",
--     "interviewer": "Jane Smith",
--     "notes": "Coding challenge completed",
--     "result": "passed"
--   }
-- ]

-- Example of how communications JSONB might look:
-- [
--   {
--     "date": "2024-01-10",
--     "type": "email",
--     "direction": "outgoing",
--     "subject": "Application for Backend Developer Position",
--     "summary": "Initial application sent"
--   },
--   {
--     "date": "2024-01-12",
--     "type": "email",
--     "direction": "incoming",
--     "subject": "Re: Application for Backend Developer Position",
--     "summary": "Interview invitation received"
--   }
-- ]