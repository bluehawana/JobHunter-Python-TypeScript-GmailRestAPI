#!/usr/bin/env python3
"""
Quick test of LinkedIn saved jobs with our improved Claude system
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

async def test_linkedin_saved_jobs():
    """Test with sample LinkedIn saved jobs"""
    
    system = ClaudeFinalSystem()
    
    # Sample jobs that might be in your LinkedIn saved jobs
    test_jobs = [
        {
            "job_title": "Senior DevOps Engineer", 
            "company": "Spotify",
            "job_description": """
We are looking for a Senior DevOps Engineer to join our Platform team in Stockholm.

Requirements:
- 5+ years of experience in DevOps/SRE roles
- Strong expertise in Kubernetes and Docker containerization
- Experience with CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
- Proficiency in cloud platforms (AWS, GCP preferred)
- Infrastructure as Code (Terraform, Ansible, CloudFormation)
- Monitoring and observability (Prometheus, Grafana, ELK stack)
- Python/Go scripting for automation
- Experience with microservices architecture

Responsibilities:
- Design and maintain scalable infrastructure for music streaming platform
- Implement and optimize CI/CD pipelines for development teams
- Manage Kubernetes clusters and container orchestration
- Ensure high availability and performance of production systems
- Collaborate with engineering teams on deployment strategies
- Implement monitoring, alerting, and incident response procedures
            """,
            "job_link": "https://www.linkedin.com/jobs/view/spotify-devops"
        },
        {
            "job_title": "Fullstack Developer",
            "company": "Volvo Cars", 
            "job_description": """
Volvo Cars is seeking a Fullstack Developer to join our Connected Car platform team.

Requirements:
- 3+ years of fullstack development experience
- Strong proficiency in Java/Spring Boot for backend development
- Frontend experience with React, Angular, or Vue.js
- Database experience (PostgreSQL, MongoDB)
- RESTful API design and development
- Cloud platforms experience (Azure preferred)
- Knowledge of microservices architecture
- Automotive industry experience is a plus

Responsibilities:
- Develop and maintain connected car services and applications
- Build responsive web applications for vehicle management
- Design and implement RESTful APIs for mobile and web clients
- Collaborate with UX/UI designers on user experience
- Ensure scalability and performance of applications
- Work with cross-functional teams in agile environment
            """,
            "job_link": "https://www.linkedin.com/jobs/view/volvo-fullstack"
        }
    ]
    
    print("🎯 Testing LinkedIn Saved Jobs with Improved Claude System")
    print("=" * 70)
    print("🚀 This will demonstrate our powerful new features:")
    print("  ✅ Swedish B2 + driving licenses in resume")  
    print("  ✅ Quantifiable achievements (60% cost reduction, 40% faster deployment)")
    print("  ✅ Role-specific project highlights (AKS migration for DevOps, etc.)")
    print("  ✅ Powerful persuasive cover letters")
    print("  ✅ Real GitHub project integration")
    print()
    
    results = []
    
    for i, job in enumerate(test_jobs, 1):
        job_title = job["job_title"]
        company = job["company"]
        job_description = job["job_description"]
        job_link = job["job_link"]
        
        print(f"📋 Processing LinkedIn Job {i}/{len(test_jobs)}")
        print(f"🎯 {job_title} at {company}")
        print(f"🔗 {job_link}")
        print("-" * 50)
        
        try:
            success = await system.process_job_application(
                job_title, company, job_description, job_link
            )
            
            results.append({
                "job": f"{job_title} at {company}",
                "success": success
            })
            
            if success:
                print(f"✅ SUCCESS: {job_title} at {company} processed!")
            else:
                print(f"❌ FAILED: {job_title} at {company}")
                
        except Exception as e:
            print(f"❌ ERROR processing {job_title} at {company}: {e}")
            results.append({
                "job": f"{job_title} at {company}",
                "success": False
            })
        
        print()
        await asyncio.sleep(2)  # Brief delay between jobs
    
    # Print final results
    print("📊 LINKEDIN SAVED JOBS TEST COMPLETE!")
    print("=" * 50)
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"✅ Successfully processed: {successful}/{total} jobs")
    print(f"📧 Check leeharvad@gmail.com for applications!")
    print()
    
    print("📋 Results Summary:")
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {result['job']}")
    
    print()
    print("🎯 Each successful application now includes:")
    print("  • Powerful cover letter highlighting AKS migration (60% cost reduction)")
    print("  • Role-specific achievements (DevOps, Fullstack focus)")
    print("  • Swedish B2 language skills + driving licenses")
    print("  • Real GitHub project integration")
    print("  • 90%+ ATS optimized content")
    print("  • Both PDF (ready to submit) + LaTeX source files")

if __name__ == "__main__":
    asyncio.run(test_linkedin_saved_jobs())