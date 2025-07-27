#!/usr/bin/env python3
"""
Test Fixed Template with Thomson Reuters Software Engineer
Verify hyperlinks and blue colors work correctly
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

async def test_fixed_template():
    """Test the fixed LaTeX template with Thomson Reuters job"""
    
    print("🔧 Testing Fixed LaTeX Template")
    print("=" * 50)
    
    # Claude system
    claude_system = ClaudeFinalSystem()
    
    # Thomson Reuters Software Development Engineer job
    job_title = "Software Development Engineer - Pagero"
    company = "Thomson Reuters"
    location = "Gothenburg (Hybrid)"
    priority = "high"
    
    job_description = """
Thomson Reuters Pagero team is seeking a Software Development Engineer to build innovative financial technology solutions.

Requirements:
- 3+ years of software development experience
- Strong programming skills in Java, Python, or .NET
- Experience with web development frameworks
- Knowledge of databases and SQL
- RESTful API development experience
- Agile development methodology experience
- Cloud platform knowledge (AWS/Azure)

Responsibilities:
- Develop and maintain financial software applications
- Design and implement scalable web services
- Collaborate with product teams on feature development
- Participate in code reviews and testing
- Work with modern cloud technologies and microservices

Join a leading provider of business information services with hybrid working options in Gothenburg.
    """
    
    job_link = "https://www.linkedin.com/jobs/view/thomson-reuters-software-development-engineer"
    
    print(f"📋 Job: {job_title}")
    print(f"🏢 Company: {company}")
    print(f"📍 Location: {location}")
    print(f"🎯 Priority: {priority}")
    print(f"🔗 Link: {job_link}")
    print("-" * 50)
    print("🔧 Testing:")
    print("  ✅ Hyperlinks in header (email, phone, LinkedIn, GitHub)")
    print("  ✅ Dark blue colors for sections and contact info")
    print("  ✅ Proper enumitem formatting")
    print("  ✅ Customer website links in additional info")
    print("-" * 50)
    
    try:
        success = await claude_system.process_job_application(
            job_title, company, job_description, job_link
        )
        
        if success:
            print(f"✅ SUCCESS: {job_title} at {company}")
            print("📧 Application sent to leeharvad@gmail.com")
            print("📄 Check PDF to verify:")
            print("  🔗 Email, LinkedIn, GitHub are clickable blue links")
            print("  🎨 Section headers are dark blue with horizontal lines")
            print("  📋 Proper bullet points and formatting")
            print("  🌐 Website links are clickable")
        else:
            print(f"❌ FAILED: {job_title} at {company}")
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_fixed_template())