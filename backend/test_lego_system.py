#!/usr/bin/env python3
"""
Test LEGO Component System - Verify that different job types generate different resumes
"""
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from templates.cv_template import generate_tailored_cv

def test_lego_system():
    """Test LEGO system with different job types"""
    
    # Test jobs with different focuses
    test_jobs = [
        {
            'title': 'DevOps Engineer',
            'company': 'Netflix',
            'description': 'We are looking for a DevOps Engineer with experience in Kubernetes, Docker, AWS, and CI/CD pipelines. You will manage our cloud infrastructure and deployment automation.'
        },
        {
            'title': 'Backend Developer',
            'company': 'Spotify',
            'description': 'Join our backend team to build scalable APIs using Java, Spring Boot, and microservices architecture. Experience with PostgreSQL and REST APIs required.'
        },
        {
            'title': 'Frontend Developer', 
            'company': 'Airbnb',
            'description': 'We need a Frontend Developer skilled in React, TypeScript, and modern JavaScript. You will build responsive user interfaces and work with our design team.'
        },
        {
            'title': 'Fullstack Developer',
            'company': 'Uber',
            'description': 'Looking for a Fullstack Developer with experience in both frontend and backend technologies. React, Node.js, and database experience preferred.'
        }
    ]
    
    print("🧪 Testing LEGO Component System...")
    print("=" * 60)
    
    results = []
    
    for i, job in enumerate(test_jobs, 1):
        print(f"\n🔧 Test {i}: {job['title']} at {job['company']}")
        print("-" * 40)
        
        # Generate tailored resume
        latex_content = generate_tailored_cv(job)
        
        # Extract key sections for comparison
        lines = latex_content.split('\n')
        
        # Find role title
        role_title = None
        for line in lines:
            if '\\textit{' in line and 'Developer' in line:
                role_title = line.strip()
                break
        
        # Find profile summary
        profile_summary = None
        in_summary = False
        for line in lines:
            if 'Profile Summary' in line:
                in_summary = True
                continue
            if in_summary and line.strip() and not line.startswith('%') and not line.startswith('\\'):
                profile_summary = line.strip()[:100] + "..."
                break
        
        # Count technical skills
        skills_count = latex_content.count('\\item \\textbf{')
        
        # Store results
        result = {
            'job': f"{job['title']} at {job['company']}",
            'role_title': role_title,
            'profile_summary': profile_summary,
            'skills_count': skills_count,
            'latex_length': len(latex_content)
        }
        results.append(result)
        
        print(f"Role Title: {role_title}")
        print(f"Profile Summary: {profile_summary}")
        print(f"Skills Count: {skills_count}")
        print(f"LaTeX Length: {len(latex_content)} chars")
    
    print("\n" + "=" * 60)
    print("📊 LEGO SYSTEM ANALYSIS")
    print("=" * 60)
    
    # Check for differences
    role_titles = [r['role_title'] for r in results]
    summaries = [r['profile_summary'] for r in results]
    
    unique_titles = len(set(role_titles))
    unique_summaries = len(set(summaries))
    
    print(f"Unique Role Titles: {unique_titles}/4")
    print(f"Unique Summaries: {unique_summaries}/4")
    
    if unique_titles >= 3 and unique_summaries >= 3:
        print("✅ LEGO SYSTEM WORKING: Generating different resumes for different jobs!")
    else:
        print("❌ LEGO SYSTEM FAILED: Resumes are too similar!")
        print("\nRole Titles:")
        for i, title in enumerate(role_titles, 1):
            print(f"  {i}. {title}")
        print("\nSummaries:")
        for i, summary in enumerate(summaries, 1):
            print(f"  {i}. {summary}")
    
    return results

if __name__ == "__main__":
    test_lego_system()