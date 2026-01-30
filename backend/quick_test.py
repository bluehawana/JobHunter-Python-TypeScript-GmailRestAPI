#!/usr/bin/env python3
"""
Quick test of our improved system with one LinkedIn job
"""
import asyncio
from claude_final_system import ClaudeFinalSystem

async def main():
    """Quick test with one job"""
    
    system = ClaudeFinalSystem()
    
    # Test with one realistic LinkedIn saved job
    job_title = "Senior DevOps Engineer"
    company = "Spotify"
    job_description = """
We are looking for a Senior DevOps Engineer to join our Platform team in Stockholm.

Requirements:
- 5+ years experience in DevOps/SRE roles
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
    """
    job_link = "https://www.linkedin.com/jobs/view/spotify-devops"
    
    print("🎯 Testing Improved Claude System")
    print("=" * 40)
    print(f"📋 Job: {job_title} at {company}")
    print("🚀 New Features Being Tested:")
    print("  ✅ Swedish B2 + driving licenses")
    print("  ✅ AKS migration achievements (60% cost reduction)")
    print("  ✅ Powerful persuasive cover letters")
    print("  ✅ Role-specific project highlights")
    print()
    
    success = await system.process_job_application(job_title, company, job_description, job_link)
    
    if success:
        print("🎉 SUCCESS! Improved system working perfectly!")
        print("📧 Check leeharvad@gmail.com for the powerful application!")
    else:
        print("❌ Test failed")

if __name__ == "__main__":
    asyncio.run(main())