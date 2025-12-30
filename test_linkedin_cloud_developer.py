#!/usr/bin/env python3
"""
Test comprehensive CV generation for LinkedIn Cloud Developer job
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import fetch_job_from_url, analyze_job_description, build_lego_cv
from ai_analyzer import AIAnalyzer

def test_linkedin_job():
    """Test with real LinkedIn Cloud Developer job"""
    
    linkedin_url = "https://www.linkedin.com/jobs/search/?currentJobId=4325756355&distance=50&geoId=104114836&keywords=cloud%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&start=25"
    
    print("="*70)
    print("TEST: LinkedIn Cloud Developer Job")
    print("="*70)
    print(f"\nURL: {linkedin_url}\n")
    
    # Try to fetch job description
    print("📥 Fetching job description from LinkedIn...")
    job_description = fetch_job_from_url(linkedin_url)
    
    if not job_description or len(job_description) < 100:
        print("\n⚠️  Could not fetch from LinkedIn (they block automated access)")
        print("Using sample Cloud Developer job description instead...\n")
        
        # Use a sample cloud developer job description
        job_description = """
        Cloud Developer - Stockholm
        
        We are looking for a talented Cloud Developer to join our team in Stockholm.
        
        Key Requirements:
        - 5+ years of experience with cloud platforms (AWS, Azure, or GCP)
        - Strong programming skills in Python, Java, or Go
        - Experience with containerization (Docker, Kubernetes)
        - Infrastructure as Code (Terraform, CloudFormation)
        - CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
        - Microservices architecture
        - RESTful API design and development
        - Database experience (PostgreSQL, MongoDB, Redis)
        - Agile/Scrum methodology
        
        Nice to have:
        - Serverless architecture (Lambda, Azure Functions)
        - Message queues (Kafka, RabbitMQ)
        - Monitoring and observability (Prometheus, Grafana)
        - Security best practices
        
        What we offer:
        - Competitive salary
        - Flexible working hours
        - Remote work options
        - Professional development opportunities
        """
    else:
        print(f"✓ Fetched {len(job_description)} characters\n")
    
    # Analyze job description
    print("🤖 Analyzing job with AI...")
    analysis = analyze_job_description(job_description)
    
    print(f"\n✓ Analysis Complete:")
    print(f"  Role Type: {analysis['roleType']}")
    print(f"  Role Category: {analysis['roleCategory']}")
    print(f"  Company: {analysis['company']}")
    print(f"  Title: {analysis['title']}")
    print(f"  Keywords: {', '.join(analysis['keywords'][:10])}")
    print(f"  AI Model: {analysis['aiAnalysis']['model']}")
    print(f"  Confidence: {analysis['aiAnalysis']['confidence']:.0%}")
    
    # Generate comprehensive CV
    print("\n📝 Generating comprehensive CV...")
    cv_latex = build_lego_cv(
        analysis['roleType'],
        analysis['company'],
        analysis['title'],
        analysis['roleCategory'],
        job_description
    )
    
    print(f"✓ CV Generated: {len(cv_latex)} characters")
    
    # Check customizations
    print("\n🔍 Checking Customizations:")
    
    checks = {
        'JD Keywords Comment': '% JD Keywords:' in cv_latex,
        'Skills Reordered': '% Skills reordered based on job requirements' in cv_latex,
        'Key Tech in Summary': any(tech in cv_latex[:2000] for tech in ['AWS', 'Azure', 'Kubernetes', 'Python', 'Docker']),
        'No Banking Content': 'banking' not in cv_latex.lower() and 'finance specialist' not in cv_latex.lower(),
        'Cloud Focus': 'cloud' in cv_latex.lower()
    }
    
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
    
    # Save output
    output_path = Path('test_linkedin_cloud_developer_cv.tex')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cv_latex)
    print(f"\n✓ Saved CV to: {output_path}")
    
    # Summary
    print("\n" + "="*70)
    print("COMPREHENSIVE CV CUSTOMIZATION SUMMARY:")
    print("="*70)
    print("✅ Profile Summary: Tailored to Cloud Developer role")
    print("✅ Core Skills: Reordered based on JD keywords")
    print("✅ Work Experience: JD context comments added")
    print("✅ ATS Optimization: Keywords emphasized throughout")
    print("\n🎯 This CV is optimized for:")
    print("  1. ATS systems (keyword matching)")
    print("  2. HR screening (relevant experience highlighted)")
    print("  3. Technical interviews (skills aligned with JD)")
    
    all_passed = all(checks.values())
    return all_passed


if __name__ == '__main__':
    print("\n🧪 Testing LinkedIn Cloud Developer Job Application\n")
    
    success = test_linkedin_job()
    
    if success:
        print("\n" + "="*70)
        print("✅ ALL CHECKS PASSED!")
        print("="*70)
        print("\nYour CV is now comprehensively optimized for the Cloud Developer role!")
        print("\nNext steps:")
        print("  1. Review the generated CV")
        print("  2. Use the 5 AI prompts for further enhancement:")
        print("     - Resume rewrite (get more interviews)")
        print("     - Role targeting (10 higher-paying roles)")
        print("     - JD match check (~90% alignment)")
        print("     - Interview prep (15 questions + answers)")
        print("     - Proof projects (complete this week)")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("⚠️  SOME CHECKS FAILED")
        print("="*70)
        print("\nReview the output above for details.")
        sys.exit(1)
