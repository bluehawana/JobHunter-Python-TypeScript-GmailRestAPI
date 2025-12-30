#!/usr/bin/env python3
"""
Test comprehensive CV generation for LinkedIn Senior DevOps job
URL: https://www.linkedin.com/jobs/search/?currentJobId=4349673221
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description, build_lego_cv, generate_ai_enhancement_prompts
from ai_analyzer import AIAnalyzer

def test_senior_devops_job():
    """Test with Senior DevOps job from LinkedIn"""
    
    # Since LinkedIn blocks scraping, use a realistic Senior DevOps job description
    job_description = """
    Senior DevOps Engineer
    
    We are seeking an experienced Senior DevOps Engineer to join our team.
    
    Key Responsibilities:
    - Design and implement CI/CD pipelines using Jenkins, GitLab CI, and GitHub Actions
    - Manage Kubernetes clusters and container orchestration
    - Implement Infrastructure as Code using Terraform and Ansible
    - Monitor and optimize cloud infrastructure on AWS and Azure
    - Ensure high availability and disaster recovery
    - Mentor junior team members on DevOps best practices
    - Implement security best practices and compliance requirements
    
    Required Skills:
    - 5+ years of DevOps experience
    - Expert knowledge of Kubernetes and Docker
    - Strong experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
    - Proficiency in Infrastructure as Code (Terraform, CloudFormation, Ansible)
    - Cloud platforms: AWS and Azure
    - Scripting: Python, Bash, PowerShell
    - Monitoring: Prometheus, Grafana, ELK Stack
    - Version control: Git, GitHub, GitLab
    
    Nice to Have:
    - Experience with service mesh (Istio, Linkerd)
    - Knowledge of security scanning tools
    - Certification: AWS Solutions Architect, CKA, CKAD
    - Experience with GitOps (ArgoCD, Flux)
    
    What We Offer:
    - Competitive salary
    - Remote work options
    - Professional development budget
    - Modern tech stack
    """
    
    print("="*70)
    print("TEST: Senior DevOps Engineer Job - Comprehensive System")
    print("="*70)
    print("\n📋 Job Description:")
    print(job_description[:300] + "...\n")
    
    # Step 1: Analyze job description
    print("🤖 Step 1: AI Analysis...")
    analysis = analyze_job_description(job_description)
    
    print(f"\n✓ Analysis Complete:")
    print(f"  Role Type: {analysis['roleType']}")
    print(f"  Role Category: {analysis['roleCategory']}")
    print(f"  Company: {analysis['company']}")
    print(f"  Title: {analysis['title']}")
    print(f"  Top Keywords: {', '.join(analysis['keywords'][:8])}")
    print(f"  AI Confidence: {analysis['aiAnalysis']['confidence']:.0%}")
    print(f"  AI Model: {analysis['aiAnalysis']['model']}")
    
    # Step 2: Generate comprehensive CV
    print("\n📝 Step 2: Generate Comprehensive CV...")
    cv_latex = build_lego_cv(
        analysis['roleType'],
        analysis['company'],
        analysis['title'],
        analysis['roleCategory'],
        job_description
    )
    
    print(f"✓ CV Generated: {len(cv_latex)} characters")
    
    # Step 3: Check all customizations
    print("\n🔍 Step 3: Verify Customizations...")
    
    checks = {
        '1. JD Keywords Comment': '% JD Keywords:' in cv_latex,
        '2. Skills Reordered': '% Skills reordered based on job requirements' in cv_latex,
        '3. Key Tech in Summary': any(tech in cv_latex[:2000] for tech in ['Kubernetes', 'Jenkins', 'Terraform', 'AWS', 'Docker']),
        '4. No Banking Content': 'banking' not in cv_latex.lower() and 'finance specialist' not in cv_latex.lower(),
        '5. DevOps Focus': 'devops' in cv_latex.lower() or 'ci/cd' in cv_latex.lower(),
        '6. Profile Customized': 'Expert in' in cv_latex[:2000]
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False
    
    # Step 4: Generate 5 AI Enhancement Prompts
    print("\n🎯 Step 4: Generate 5 AI Enhancement Prompts...")
    prompts = generate_ai_enhancement_prompts(
        job_description,
        cv_latex,
        analysis['company'],
        analysis['title']
    )
    
    print(f"✓ Generated {len(prompts)} AI prompts:")
    print(f"  1. Resume Rewrite - {len(prompts['resume_rewrite'])} chars")
    print(f"  2. Role Targeting - {len(prompts['role_targeting'])} chars")
    print(f"  3. JD Match Check - {len(prompts['jd_match'])} chars")
    print(f"  4. Interview Prep - {len(prompts['interview_prep'])} chars")
    print(f"  5. Proof Projects - {len(prompts['proof_projects'])} chars")
    
    # Save outputs
    output_dir = Path('test_output_senior_devops')
    output_dir.mkdir(exist_ok=True)
    
    # Save CV
    cv_path = output_dir / 'senior_devops_cv.tex'
    with open(cv_path, 'w', encoding='utf-8') as f:
        f.write(cv_latex)
    print(f"\n✓ Saved CV to: {cv_path}")
    
    # Save prompts
    import json
    prompts_path = output_dir / 'ai_enhancement_prompts.json'
    with open(prompts_path, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved AI prompts to: {prompts_path}")
    
    # Summary
    print("\n" + "="*70)
    print("COMPREHENSIVE SYSTEM TEST RESULTS:")
    print("="*70)
    
    if all_passed:
        print("✅ ALL CUSTOMIZATIONS PASSED!")
        print("\n📦 Complete Package Generated:")
        print("  1. ✅ Tailored CV (Profile, Skills, Experience optimized)")
        print("  2. ✅ JD Context Comments (ATS optimization)")
        print("  3. ✅ Skills Reordered (Most relevant first)")
        print("  4. ✅ 5 AI Enhancement Prompts (Ready to use)")
        print("\n🎯 This CV is optimized for:")
        print("  • ATS systems (keyword matching)")
        print("  • HR screening (relevant experience highlighted)")
        print("  • Technical interviews (skills aligned with JD)")
        print("\n💡 Next Steps:")
        print("  1. Review the generated CV")
        print("  2. Copy AI prompts to ChatGPT/Claude:")
        print("     - Resume Rewrite → Get polished version")
        print("     - Role Targeting → Discover 10 higher-paying roles")
        print("     - JD Match Check → Optimize for ~90% alignment")
        print("     - Interview Prep → Practice 15 questions")
        print("     - Proof Projects → Build 3 projects this week")
        print("  3. Apply with confidence! 🚀")
    else:
        print("⚠️  SOME CHECKS FAILED - Review output above")
    
    return all_passed


if __name__ == '__main__':
    print("\n🧪 Testing Senior DevOps Job - Comprehensive System\n")
    
    success = test_senior_devops_job()
    
    if success:
        print("\n" + "="*70)
        print("✅ SUCCESS! Complete job application package ready!")
        print("="*70)
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("⚠️  Review failed checks above")
        print("="*70)
        sys.exit(1)
