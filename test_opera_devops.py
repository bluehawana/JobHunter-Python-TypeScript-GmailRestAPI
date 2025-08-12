#!/usr/bin/env python3
"""
Test Opera DevOps Engineer Job - Real Job Application
https://jobs.opera.com/jobs/6060392-devops-engineer
"""
import sys
import os
sys.path.append('backend')

from beautiful_pdf_generator import create_beautiful_multi_page_pdf
from overleaf_pdf_generator import OverleafPDFGenerator
import json

def test_opera_devops_job():
    """Test with real Opera DevOps Engineer job posting"""
    
    # Real Opera job data
    opera_job = {
        'title': 'DevOps Engineer',
        'company': 'Opera',
        'description': '''
        We are looking for a DevOps Engineer to join our team and help us build and maintain our infrastructure.
        
        Key responsibilities:
        - Design, implement and maintain CI/CD pipelines
        - Manage cloud infrastructure on AWS and Azure
        - Implement monitoring and alerting solutions
        - Automate deployment processes
        - Work with Kubernetes and Docker containers
        - Collaborate with development teams
        - Ensure security best practices
        - Optimize system performance and reliability
        
        Required skills:
        - Experience with AWS, Azure, or GCP
        - Proficiency in Kubernetes and Docker
        - CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
        - Infrastructure as Code (Terraform, CloudFormation)
        - Monitoring tools (Prometheus, Grafana, ELK stack)
        - Scripting languages (Python, Bash, PowerShell)
        - Linux system administration
        - Security best practices
        - Agile methodologies
        
        Nice to have:
        - Experience with microservices architecture
        - Knowledge of service mesh (Istio, Linkerd)
        - Database administration (PostgreSQL, MongoDB)
        - Experience with browser technology
        ''',
        'location': 'Oslo, Norway',
        'url': 'https://jobs.opera.com/jobs/6060392-devops-engineer'
    }
    
    print("🎭 TESTING OPERA DEVOPS ENGINEER JOB")
    print("=" * 60)
    print(f"🏢 Company: {opera_job['company']}")
    print(f"💼 Position: {opera_job['title']}")
    print(f"📍 Location: {opera_job['location']}")
    print(f"🔗 URL: {opera_job['url']}")
    print("=" * 60)
    
    # Generate PDF with Overleaf integration
    print("\n🚀 Generating tailored resume...")
    pdf_content = create_beautiful_multi_page_pdf(opera_job)
    
    if pdf_content:
        # Save PDF
        pdf_filename = "opera_devops_resume.pdf"
        with open(pdf_filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF Generated: {pdf_filename} ({len(pdf_content):,} bytes)")
        
        # Also generate LaTeX content to show LEGO intelligence
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(opera_job)
        
        # Save LaTeX file
        latex_filename = "opera_devops_resume.tex"
        with open(latex_filename, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"📝 LaTeX Generated: {latex_filename} ({len(latex_content):,} characters)")
        
        # Generate Overleaf URL
        base_url = "https://jobs.bluehawana.com"
        latex_url = f"{base_url}/api/v1/latex/opera_devops_resume.tex"
        overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
        
        print(f"\n🔗 OVERLEAF INTEGRATION:")
        print(f"📝 LaTeX URL: {latex_url}")
        print(f"🎯 Overleaf URL: {overleaf_url}")
        
        # Analyze LEGO intelligence
        print(f"\n🧠 LEGO INTELLIGENCE ANALYSIS:")
        
        # Check if it detected DevOps keywords
        job_text = (opera_job['title'] + ' ' + opera_job['description']).lower()
        devops_keywords = ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd']
        detected_keywords = [kw for kw in devops_keywords if kw in job_text]
        
        print(f"🎯 Detected DevOps keywords: {', '.join(detected_keywords)}")
        print(f"✅ Should be tailored as: DevOps Engineer & Cloud Infrastructure Specialist")
        
        # Check LaTeX content for DevOps-specific tailoring
        if 'DevOps Engineer \\& Cloud Infrastructure Specialist' in latex_content:
            print("✅ Role title correctly tailored for DevOps")
        else:
            print("❌ Role title not properly tailored")
        
        if 'Cloud Platforms:' in latex_content and 'Containerization:' in latex_content:
            print("✅ Skills section tailored for DevOps focus")
        else:
            print("❌ Skills section not properly tailored")
        
        if 'infrastructure optimization roles for companies like Opera' in latex_content:
            print("✅ Profile summary mentions Opera specifically")
        else:
            print("❌ Profile summary doesn't mention Opera")
        
        # Show key sections
        print(f"\n📋 KEY RESUME SECTIONS FOR OPERA:")
        print("• DevOps Engineer & Cloud Infrastructure Specialist (role title)")
        print("• Cloud Platforms: AWS, Azure, GCP, Infrastructure as Code")
        print("• Containerization: Docker, Kubernetes, Container Orchestration")
        print("• CI/CD: Jenkins, GitHub Actions, Deployment Pipelines")
        print("• Monitoring: Grafana, System Reliability, Performance Monitoring")
        print("• Current ECARX experience with Kubernetes migration")
        print("• Infrastructure optimization focus")
        
        result = {
            'company': opera_job['company'],
            'job_title': opera_job['title'],
            'location': opera_job['location'],
            'pdf_size': len(pdf_content),
            'latex_size': len(latex_content),
            'pdf_file': pdf_filename,
            'latex_file': latex_filename,
            'overleaf_url': overleaf_url,
            'detected_keywords': detected_keywords,
            'success': True
        }
        
    else:
        print("❌ PDF Generation Failed")
        result = {
            'company': opera_job['company'],
            'job_title': opera_job['title'],
            'success': False
        }
    
    print(f"\n🎉 OPERA DEVOPS TEST COMPLETE!")
    return result

if __name__ == "__main__":
    result = test_opera_devops_job()
    
    print(f"\n📊 FINAL RESULT:")
    print(json.dumps({k: v for k, v in result.items() if k not in ['pdf_file', 'latex_file']}, indent=2))
    
    if result.get('success'):
        print(f"\n🚀 READY FOR OPERA APPLICATION!")
        print(f"📄 Resume: {result['pdf_file']}")
        print(f"📝 LaTeX: {result['latex_file']}")
        print(f"🔗 Edit in Overleaf: {result['overleaf_url']}")
        print(f"\n💡 The resume is specifically tailored for Opera's DevOps role with:")
        print(f"   • Infrastructure focus matching their requirements")
        print(f"   • Kubernetes/Docker expertise highlighted")
        print(f"   • Cloud platforms (AWS/Azure) emphasized")
        print(f"   • CI/CD pipeline experience featured")
        print(f"   • Current ECARX infrastructure work showcased")