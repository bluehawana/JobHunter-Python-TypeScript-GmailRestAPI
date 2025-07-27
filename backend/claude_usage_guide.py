#!/usr/bin/env python3
"""
Claude-Powered Resume Usage Guide
Simple interface to customize resumes using Claude 3.7 for any job
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

class ClaudeResumeInterface:
    def __init__(self):
        self.system = ClaudeFinalSystem()
    
    async def customize_for_job(self, job_title: str, company: str, job_description: str, job_link: str = ""):
        """
        Main interface to customize resume for any job
        
        Usage example:
        await customizer.customize_for_job(
            job_title="DevOps Engineer",
            company="Opera", 
            job_description="Job requirements and description here...",
            job_link="https://company.com/job-link"
        )
        """
        return await self.system.process_job_application(job_title, company, job_description, job_link)

# ===== USAGE EXAMPLES =====

async def example_devops_opera():
    """Example: DevOps at Opera"""
    customizer = ClaudeResumeInterface()
    
    job_title = "DevOps Engineer"
    company = "Opera"
    job_description = """
    We are looking for a DevOps Engineer to join our team in Stockholm. 
    
    Requirements:
    - 3+ years experience with Kubernetes and Docker
    - Strong knowledge of CI/CD pipelines
    - Experience with AWS or Azure cloud platforms
    - Python scripting and automation experience
    - Infrastructure as Code (Terraform/Ansible)
    - Monitoring and logging systems (Grafana, Prometheus)
    """
    job_link = "https://opera.com/careers/devops"
    
    success = await customizer.customize_for_job(job_title, company, job_description, job_link)
    return success

async def example_fullstack_spotify():
    """Example: Fullstack at Spotify"""
    customizer = ClaudeResumeInterface()
    
    job_title = "Senior Fullstack Developer"
    company = "Spotify"
    job_description = """
    Join Spotify's engineering team as a Senior Fullstack Developer.
    
    Requirements:
    - 5+ years of experience in full-stack development
    - Strong proficiency in JavaScript, React, and Node.js
    - Experience with microservices architecture
    - Knowledge of cloud platforms (AWS/GCP)
    - Experience with databases (PostgreSQL, MongoDB)
    - CI/CD and DevOps practices
    - Agile development methodologies
    """
    job_link = "https://spotify.com/jobs/fullstack"
    
    success = await customizer.customize_for_job(job_title, company, job_description, job_link)
    return success

async def example_backend_volvo():
    """Example: Backend at Volvo"""
    customizer = ClaudeResumeInterface()
    
    job_title = "Senior Backend Developer"
    company = "Volvo Group"
    job_description = """
    Volvo Group is seeking a Senior Backend Developer for our connected vehicle platform.
    
    Requirements:
    - Strong experience with Java and Spring Boot
    - Microservices architecture and RESTful APIs
    - Database design and optimization (SQL/NoSQL)
    - Cloud platforms (Azure preferred)
    - Containerization with Docker and Kubernetes
    - Agile development practices
    - Automotive industry experience is a plus
    """
    job_link = "https://volvo.com/careers/backend-developer"
    
    success = await customizer.customize_for_job(job_title, company, job_description, job_link)
    return success

# ===== HOW TO USE THIS SYSTEM =====

async def your_custom_job():
    """
    Template for customizing your resume for ANY job
    
    Steps:
    1. Copy this function
    2. Replace the job details with your target job
    3. Run the function
    4. Check leeharvad@gmail.com for your optimized application
    """
    customizer = ClaudeResumeInterface()
    
    # ===== REPLACE THESE WITH YOUR JOB DETAILS =====
    job_title = "YOUR_JOB_TITLE"           # e.g., "DevOps Engineer"
    company = "YOUR_COMPANY"               # e.g., "Opera"
    job_description = """
    PASTE THE COMPLETE JOB DESCRIPTION HERE
    
    Include:
    - Requirements
    - Responsibilities  
    - Skills needed
    - Technologies mentioned
    - Company description
    """
    job_link = "YOUR_JOB_APPLICATION_LINK"  # Optional
    # ===== END REPLACEMENT =====
    
    print(f"🎯 Customizing resume for {job_title} at {company}")
    print("🤖 Claude 3.7 will analyze the job and optimize your resume for 90%+ ATS compatibility")
    
    success = await customizer.customize_for_job(job_title, company, job_description, job_link)
    
    if success:
        print("✅ SUCCESS! Check leeharvad@gmail.com for your optimized application")
        print("📎 You'll receive: CV PDF, Cover Letter PDF, LaTeX sources")
        print("🎯 Optimized for maximum ATS scoring and keyword matching")
    else:
        print("❌ Failed to generate application")
    
    return success

# ===== QUICK COMMAND LINE USAGE =====

async def main():
    """
    Choose which example to run, or create your own
    """
    print("🤖 Claude 3.7 Powered Resume Customization")
    print("=" * 50)
    print("Available examples:")
    print("1. DevOps Engineer at Opera")
    print("2. Senior Fullstack Developer at Spotify") 
    print("3. Senior Backend Developer at Volvo Group")
    print("4. Your custom job (edit the function)")
    print()
    
    # Uncomment the example you want to run:
    
    # Example 1: DevOps at Opera
    await example_devops_opera()
    
    # Example 2: Fullstack at Spotify
    # await example_fullstack_spotify()
    
    # Example 3: Backend at Volvo
    # await example_backend_volvo()
    
    # Your custom job (edit the function first)
    # await your_custom_job()

if __name__ == "__main__":
    asyncio.run(main())

"""
=== WHAT THIS SYSTEM DOES ===

1. 🤖 INTELLIGENT ANALYSIS
   - Claude 3.7 analyzes the job description
   - Identifies key requirements and technologies
   - Extracts important keywords for ATS optimization

2. 📝 SMART CUSTOMIZATION  
   - Rewrites your profile summary for the specific role
   - Reorders technical skills based on job requirements
   - Emphasizes relevant experience and achievements
   - Maintains factual accuracy while optimizing relevance

3. 🎯 ATS OPTIMIZATION
   - Integrates 30+ relevant keywords naturally
   - Uses industry-standard terminology
   - Optimizes for 90%+ ATS compatibility score
   - Ensures proper keyword density without stuffing

4. ✍️ COVER LETTER GENERATION
   - Creates role-specific cover letter
   - Incorporates company research and job requirements
   - Highlights your most relevant experience
   - Professional tone with personal touch

5. 📎 COMPLETE PACKAGE
   - Sends both PDF (ready to submit) and LaTeX (for editing)
   - Email includes content preview and optimization notes
   - Clear instructions for any manual adjustments needed

=== REQUIREMENTS ===

Environment Variables (USER MUST PROVIDE THEIR OWN):
- SMTP_PASSWORD='your_gmail_app_password'
- ANTHROPIC_BASE_URL='your_claude_api_base_url'  
- ANTHROPIC_AUTH_TOKEN='your_claude_api_token'

⚠️  SECURITY: Never hardcode API credentials in source code!

Command to run:
export SMTP_PASSWORD='your_password' && export ANTHROPIC_BASE_URL='your_url' && export ANTHROPIC_AUTH_TOKEN='your_token' && python3 claude_usage_guide.py

=== YOUR WORKFLOW ===

1. Find a job you want to apply for
2. Copy the complete job description
3. Edit the your_custom_job() function with job details
4. Run the script
5. Check leeharvad@gmail.com for your optimized application
6. Submit the PDFs directly to the employer
7. High chance of passing ATS and getting interviews!

=== WHY THIS WORKS ===

• Uses Claude 3.7's advanced language understanding
• Analyzes job requirements like a human recruiter would
• Optimizes for both ATS systems and human readers  
• Maintains your authentic experience while maximizing relevance
• Saves hours of manual customization work
• Dramatically improves your application success rate
"""