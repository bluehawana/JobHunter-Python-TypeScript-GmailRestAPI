#!/usr/bin/env python3
"""
Process First Real LinkedIn Job
Test with Ericsson Software Developer position
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

async def process_first_job():
    """Process the first high priority job: Ericsson Software Developer"""
    
    print("🎯 Processing First Real LinkedIn Job")
    print("=" * 50)
    
    # Claude system
    claude_system = ClaudeFinalSystem()
    
    # First job: Ericsson Software Developer in JAVA
    job_title = "Software developer in JAVA"
    company = "Ericsson"
    location = "Gothenburg"
    priority = "high"
    
    job_description = """
Join Ericsson's Software Development team in Gothenburg to build next-generation telecommunications solutions.

Requirements:
- 3+ years of Java development experience
- Strong knowledge of Spring Boot, Spring MVC
- Experience with RESTful APIs and microservices
- Knowledge of SQL databases (PostgreSQL, MySQL)
- Experience with Git, Maven/Gradle
- Understanding of software testing practices
- Agile development experience

Responsibilities:
- Develop and maintain Java-based applications for telecom infrastructure
- Design and implement RESTful APIs
- Collaborate with cross-functional teams
- Participate in code reviews and testing
- Work with cloud technologies and containerization

Ericsson offers competitive salary, flexible working, and opportunity to work on cutting-edge telecom technology.
    """
    
    job_link = "https://www.linkedin.com/jobs/view/ericsson-software-developer-java"
    
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
    asyncio.run(process_first_job())