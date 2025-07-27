#!/usr/bin/env python3
"""
Process Second Real LinkedIn Job
Test with Ericsson DevOps Engineer position
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

async def process_second_job():
    """Process the second high priority job: Ericsson DevOps Engineer"""
    
    print("🎯 Processing Second Real LinkedIn Job")
    print("=" * 50)
    
    # Claude system
    claude_system = ClaudeFinalSystem()
    
    # Second job: Ericsson CI/CD DevOps Junior Engineer
    job_title = "CI CD DevOps Junior Engineer"
    company = "Ericsson"
    location = "Gothenburg"
    priority = "high"
    
    job_description = """
Join Ericsson's DevOps team to build and maintain CI/CD infrastructure for telecommunications software.

Requirements:
- 2+ years of DevOps/CI/CD experience
- Knowledge of Jenkins, GitLab CI, or similar tools
- Experience with Docker and containerization
- Basic understanding of Kubernetes
- Linux/Unix system administration
- Scripting experience (Bash, Python)
- Understanding of infrastructure as code

Responsibilities:
- Build and maintain CI/CD pipelines
- Support development teams with deployment automation
- Monitor and troubleshoot build and deployment processes
- Implement infrastructure automation
- Collaborate with development teams on DevOps best practices

Great opportunity to learn enterprise-level DevOps at a leading telecom company.
    """
    
    job_link = "https://www.linkedin.com/jobs/view/ericsson-devops-engineer"
    
    print(f"📋 Job: {job_title}")
    print(f"🏢 Company: {company}")
    print(f"📍 Location: {location}")
    print(f"🎯 Priority: {priority}")
    print(f"🔗 Link: {job_link}")
    print("-" * 50)
    
    try:
        success = await claude_system.process_job_application(
            job_title, company, job_description, job_link
        )
        
        if success:
            print(f"✅ SUCCESS: {job_title} at {company}")
            print("📧 Application sent to leeharvad@gmail.com")
            print("📄 Check email for CV and cover letter PDFs + LaTeX sources")
        else:
            print(f"❌ FAILED: {job_title} at {company}")
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(process_second_job())