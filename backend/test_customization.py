#!/usr/bin/env python3
"""
Test script to demonstrate resume customization for different job types
Shows how the system customizes your fullstack resume for specific roles
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.latex_resume_service import LaTeXResumeService

# Sample job postings to test with
sample_jobs = {
    "fullstack": {
        "title": "Senior Fullstack Developer",
        "company": "TechCorp AB",
        "description": """
        We are looking for a Senior Fullstack Developer with experience in Java Spring Boot, 
        React, PostgreSQL, and microservices architecture. You'll work with AWS cloud services 
        and implement RESTful APIs. Experience with Docker and CI/CD pipelines is preferred.
        """,
        "keywords": ["Java", "Spring Boot", "React", "PostgreSQL", "AWS", "Docker", "REST API"]
    },
    
    "cloud_engineer": {
        "title": "Cloud Engineer - DevOps",
        "company": "CloudTech Solutions",
        "description": """
        Join our cloud team as a Cloud Engineer! You'll work with Azure cloud infrastructure, 
        Kubernetes container orchestration, Terraform for infrastructure as code, and Jenkins 
        for CI/CD pipelines. Experience with monitoring tools like Grafana is a plus.
        """,
        "keywords": ["Azure", "Kubernetes", "Terraform", "Jenkins", "DevOps", "Grafana", "CI/CD"]
    },
    
    "devops": {
        "title": "Senior DevOps Specialist",
        "company": "InfraTech Nordic",
        "description": """
        We need a DevOps specialist to manage our container infrastructure using Kubernetes 
        and Docker. You'll implement CI/CD pipelines with Jenkins, manage cloud resources on AWS, 
        and work with infrastructure as code using Terraform. Monitoring with Prometheus/Grafana required.
        """,
        "keywords": ["DevOps", "Kubernetes", "Docker", "Jenkins", "AWS", "Terraform", "Prometheus"]
    },
    
    "frontend": {
        "title": "Senior Frontend Developer",
        "company": "UX Design Studio",
        "description": """
        Looking for a creative Senior Frontend Developer skilled in React, Angular, TypeScript, 
        and modern CSS frameworks. You'll work on responsive web applications with focus on 
        user experience and performance optimization. Experience with Node.js backend integration preferred.
        """,
        "keywords": ["React", "Angular", "TypeScript", "CSS", "JavaScript", "Node.js", "Frontend"]
    }
}

async def test_customization():
    """Test resume customization for different job types"""
    print("🧪 Testing Resume Customization Logic")
    print("=" * 60)
    
    latex_service = LaTeXResumeService()
    
    for job_type, job_data in sample_jobs.items():
        print(f"\n📋 JOB TYPE: {job_type.upper()}")
        print(f"Title: {job_data['title']}")
        print(f"Company: {job_data['company']}")
        print("-" * 40)
        
        # Test job role determination
        job_role = latex_service._determine_job_role(job_data['title'], job_data['keywords'])
        print(f"🎯 CV Header Role: {job_role}")
        
        # Test profile customization
        profile = latex_service._generate_customized_profile(
            job_data, job_data['description'], job_data['keywords']
        )
        print(f"📝 Profile Summary (first 100 chars): {profile[:100]}...")
        
        # Test skills relevance
        skills = latex_service._generate_relevant_skills(job_data['keywords'], job_data['description'])
        skills_lines = skills.split('\n')[:3]  # Show first 3 skill categories
        print("🔧 Top Relevant Skills:")
        for skill_line in skills_lines:
            if skill_line.strip():
                # Extract skill category from LaTeX formatting
                skill_clean = skill_line.replace('\\item \\textbf{', '').replace('}', ':').replace('\\', '')
                print(f"   • {skill_clean}")
        
        # Test cover letter customization
        cover_letter_body = latex_service._generate_cover_letter_body(job_data, job_data['description'])
        first_sentence = cover_letter_body.split('.')[0] + '.'
        print(f"💌 Cover Letter Opening: {first_sentence}")
        
        print()

def show_customization_summary():
    """Show how the customization works"""
    print("\n🎯 HOW CUSTOMIZATION WORKS:")
    print("=" * 60)
    print("""
1. JOB ROLE DETECTION:
   • Analyzes job title and keywords
   • Maps to appropriate role (Fullstack/DevOps/Cloud/Frontend Developer)
   • Updates CV header with targeted role

2. PROFILE SUMMARY:
   • Scans job description for key technologies
   • Emphasizes relevant experience (Java, Azure, React, etc.)
   • Maintains your core experience while highlighting job-relevant skills

3. SKILLS PRIORITIZATION:
   • Reorders your skill categories based on job requirements
   • Puts most relevant skills first (e.g., Cloud Platforms for DevOps roles)
   • Maintains your complete skill set

4. COVER LETTER:
   • Customizes opening based on job type
   • Mentions specific technologies from job posting
   • Aligns your experience with their requirements

5. COMPANY PERSONALIZATION:
   • Uses actual company name and job title
   • Generates appropriate hiring manager greeting
   • Creates professional, targeted application
    """)

async def main():
    """Main test function"""
    print("🚀 JobHunter Resume Customization Test")
    print("This shows how your fullstack resume gets customized for different roles")
    print()
    
    await test_customization()
    show_customization_summary()
    
    print("\n✅ SUMMARY:")
    print("Your base fullstack resume will be intelligently customized for:")
    print("• Cloud Engineer → Emphasizes Azure/AWS, Infrastructure, DevOps experience")
    print("• DevOps → Highlights CI/CD, Kubernetes, automation experience") 
    print("• Frontend → Focuses on React/Angular, UI/UX, frontend frameworks")
    print("• Fullstack → Balanced emphasis on both frontend and backend skills")
    print("\n💡 The system maintains your complete experience while emphasizing job-relevant aspects!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())