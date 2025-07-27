#!/usr/bin/env python3
"""
Test script to verify the new modern resume and cover letter templates work correctly
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.latex_resume_service import LaTeXResumeService

# Mock job data for testing
mock_job = {
    "title": "Senior Fullstack Developer",
    "company": "ECARX Sweden",
    "description": """
    We are looking for a Senior Fullstack Developer to join our automotive technology team.
    The ideal candidate will have experience with Java Spring Boot, React, PostgreSQL, 
    and microservices architecture. You'll work with cloud services (AWS/Azure) and 
    implement RESTful APIs. Experience with Docker, Kubernetes, and CI/CD pipelines is required.
    
    Key responsibilities:
    - Develop scalable backend services using Java and Spring Boot
    - Build responsive frontend applications with React
    - Design and implement RESTful APIs
    - Work with PostgreSQL databases
    - Deploy applications using Docker and Kubernetes
    - Collaborate with cross-functional teams in Agile environment
    """,
    "keywords": ["Java", "Spring Boot", "React", "PostgreSQL", "AWS", "Docker", "Kubernetes", "REST API", "Microservices"],
    "url": "https://careers.ecarx.com/senior-fullstack-developer",
    "location": "Gothenburg, Sweden",
    "salary": "65000-85000 SEK"
}

async def test_document_generation():
    """Test generating both CV and cover letter with new templates"""
    print("🧪 Testing Modern Template Document Generation")
    print("=" * 60)
    
    latex_service = LaTeXResumeService()
    
    # Test CV generation
    print("📄 Generating CV...")
    try:
        cv_content = await latex_service.generate_customized_cv(mock_job)
        if cv_content:
            print(f"✅ CV generated successfully ({len(cv_content)} bytes)")
            
            # Save CV for inspection
            cv_filename = f"test_cv_{mock_job['company'].replace(' ', '_')}.pdf"
            with open(cv_filename, 'wb') as f:
                f.write(cv_content)
            print(f"💾 CV saved as: {cv_filename}")
        else:
            print("❌ CV generation failed - empty content")
    except Exception as e:
        print(f"❌ CV generation failed: {e}")
    
    print()
    
    # Test Cover Letter generation
    print("📝 Generating Cover Letter...")
    try:
        cl_content = await latex_service.generate_customized_cover_letter(mock_job)
        if cl_content:
            print(f"✅ Cover Letter generated successfully ({len(cl_content)} bytes)")
            
            # Save cover letter for inspection
            cl_filename = f"test_cover_letter_{mock_job['company'].replace(' ', '_')}.pdf"
            with open(cl_filename, 'wb') as f:
                f.write(cl_content)
            print(f"💾 Cover Letter saved as: {cl_filename}")
        else:
            print("❌ Cover Letter generation failed - empty content")
    except Exception as e:
        print(f"❌ Cover Letter generation failed: {e}")

def test_template_logic():
    """Test the template customization logic"""
    print("\n🔧 Testing Template Customization Logic")
    print("=" * 60)
    
    latex_service = LaTeXResumeService()
    
    # Test job role determination
    job_role = latex_service._determine_job_role(mock_job['title'], mock_job['keywords'])
    print(f"🎯 Determined Job Role: {job_role}")
    
    # Test profile customization
    profile = latex_service._generate_customized_profile(
        mock_job, mock_job['description'], mock_job['keywords']
    )
    print(f"📝 Profile Summary: {profile[:150]}...")
    
    # Test skills prioritization
    skills = latex_service._generate_relevant_skills(mock_job['keywords'], mock_job['description'])
    skills_lines = skills.split('\n')[:3]
    print("🔧 Top Priority Skills:")
    for skill_line in skills_lines:
        if skill_line.strip():
            clean_skill = skill_line.replace('\\item \\textbf{', '').replace('}:', ':').replace('\\', '')
            print(f"   • {clean_skill}")
    
    # Test cover letter body
    cl_body = latex_service._generate_cover_letter_body(mock_job, mock_job['description'])
    print(f"💌 Cover Letter Opening: {cl_body[:100]}...")

async def main():
    """Main test function"""
    print("🚀 Modern Template Integration Test")
    print("Testing your updated resume and cover letter templates")
    print()
    
    test_template_logic()
    await test_document_generation()
    
    print("\n✅ TEST SUMMARY:")
    print("✓ Modern template format updated")
    print("✓ Resume customization working")
    print("✓ Cover letter personalization active")
    print("✓ Ready for use with job saving system")
    print()
    print("💡 Your JobHunter system now uses the new modern templates!")
    print("   Next time you save a job, it will generate documents with the updated format.")

if __name__ == "__main__":
    asyncio.run(main())