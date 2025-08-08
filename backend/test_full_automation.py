#!/usr/bin/env python3
"""
Test the full automation with Claude integration
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

async def test_automation():
    """Test the full automation with a mock job"""
    print("🚀 Testing full automation with Claude integration...")
    
    # Mock job data
    mock_job = {
        'title': 'Senior Backend Developer',
        'company': 'Volvo Group',
        'description': 'We are looking for a Senior Backend Developer with expertise in Java, Spring Boot, microservices architecture, and cloud platforms. Experience with Kubernetes, Docker, and AWS is highly valued. The role involves building scalable APIs for automotive systems and working with international teams across Sweden and China.',
        'url': 'https://jobs.volvo.com/test',
        'location': 'Gothenburg, Sweden',
        'email_subject': 'Volvo Group söker nu fler talanger till Senior Backend Developer',
        'body': 'Join Volvo Group as a Senior Backend Developer. We need someone with Java, Spring Boot, and cloud experience.',
        'sender': 'careers@volvo.com'
    }
    
    try:
        from improved_working_automation import ImprovedWorkingAutomation
        automation = ImprovedWorkingAutomation()
        
        print("📋 Processing mock job...")
        improved_job = automation._improve_job_data(mock_job)
        print(f"✅ Improved job data: {improved_job['company']} - {improved_job['title']}")
        
        print("📄 Generating Claude-powered CV...")
        cv_pdf = automation._generate_cv_pdf(improved_job)
        print(f"✅ CV generated: {len(cv_pdf)} bytes")
        
        print("💌 Generating Claude-powered cover letter...")
        cl_pdf = automation._generate_cover_letter_pdf(improved_job)
        print(f"✅ Cover letter generated: {len(cl_pdf)} bytes")
        
        # Save PDFs for inspection
        if cv_pdf:
            with open('test_claude_cv.pdf', 'wb') as f:
                f.write(cv_pdf)
            print("📁 Saved test_claude_cv.pdf")
        
        if cl_pdf:
            with open('test_claude_cover_letter.pdf', 'wb') as f:
                f.write(cl_pdf)
            print("📁 Saved test_claude_cover_letter.pdf")
        
        print("🎉 Full automation test completed!")
        
    except Exception as e:
        print(f"❌ Automation test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_automation())