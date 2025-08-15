#!/usr/bin/env python3
"""
Manual Job Input - For testing real job applications
Add real jobs you received in bluehawana@gmail.com here
"""
from typing import List, Dict, Any
from datetime import datetime

def get_real_jobs_from_bluehawana() -> List[Dict[str, Any]]:
    """
    Manually input real jobs from bluehawana@gmail.com
    Update this list with actual job opportunities you received
    """
    
    # Example real jobs - REPLACE WITH ACTUAL JOBS FROM YOUR EMAIL
    real_jobs = [
        # Test job for TRUE LEGO system
        {
            'company': 'Volvo Group',
            'title': 'Senior DevOps Engineer',
            'location': 'Gothenburg, Sweden',
            'description': 'We are looking for a Senior DevOps Engineer to join our team. You will work with Kubernetes, Docker, AWS, monitoring with Prometheus and Grafana, CI/CD pipelines, and infrastructure automation. Experience with automotive industry is a plus.',
            'url': 'https://jobs.volvogroup.com/job/12345',
            'source': 'linkedin_email',
            'requirements': 'Kubernetes, Docker, AWS, Python, Prometheus, Grafana, CI/CD, Infrastructure as Code',
            'from': 'jobs-noreply@linkedin.com',
            'subject': 'New job opportunity: Senior DevOps Engineer at Volvo Group',
            'date': '2025-08-14'
        }
    ]
    
    # If no manual jobs, return empty list (no fake jobs)
    return real_jobs

def add_job_manually(company: str, title: str, location: str, description: str, url: str = "", requirements: str = "") -> Dict[str, Any]:
    """
    Helper function to add a job manually
    """
    return {
        'company': company,
        'title': title,
        'location': location,
        'description': description,
        'url': url,
        'source': 'manual_input',
        'requirements': requirements,
        'from': 'manual@input.com',
        'subject': f'Manual job: {title} at {company}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'email_body': description
    }

if __name__ == "__main__":
    jobs = get_real_jobs_from_bluehawana()
    
    print("📧 MANUAL JOB INPUT")
    print("=" * 40)
    print(f"Real jobs available: {len(jobs)}")
    
    if jobs:
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['company']} - {job['title']}")
            print(f"   📍 {job['location']}")
            print(f"   📧 From: {job['from']}")
    else:
        print("\n💡 No jobs added yet.")
        print("📝 To add real jobs:")
        print("   1. Check bluehawana@gmail.com for LinkedIn/Indeed alerts")
        print("   2. Edit manual_job_input.py")
        print("   3. Add real job details to the real_jobs list")
        print("   4. Run the automation")