#!/usr/bin/env python3
"""
Test script for Lime Software Engineer job classification
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.cv_templates import CVTemplateManager
import logging

# Configure logging to see detailed analysis
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

def test_lime_job_classification():
    """Test Lime Software Engineer job classification"""
    
    # Lime Software Engineer job description
    lime_job = """
    Software Engineer at Lime
    
    We're looking for a Software Engineer to join our team and help build the future of micromobility. 
    You'll work on our platform that powers millions of rides worldwide.
    
    What you'll do:
    - Build and maintain web applications using Vue.js and TypeScript
    - Develop backend services using C# and .NET Core
    - Work with cloud infrastructure on AWS including ECS, Lambda, and RDS
    - Implement CI/CD pipelines using GitHub Actions
    - Monitor applications using DataDog and CloudWatch
    - Collaborate with product and design teams
    - Write clean, testable code with good test coverage
    - Participate in code reviews and technical discussions
    
    What we're looking for:
    - 3+ years of software development experience
    - Strong experience with C# and .NET ecosystem
    - Frontend development experience with Vue.js or similar frameworks
    - Experience with TypeScript and modern JavaScript
    - Knowledge of AWS services and cloud deployment
    - Experience with containerization (Docker) and orchestration (Kubernetes)
    - Understanding of CI/CD practices and tools
    - Experience with monitoring and observability tools
    - Strong problem-solving skills and attention to detail
    
    Nice to have:
    - Experience with microservices architecture
    - Knowledge of event-driven systems
    - Experience with infrastructure as code (Terraform)
    - Background in transportation or mobility industry
    """
    
    print("=" * 80)
    print("LIME SOFTWARE ENGINEER JOB CLASSIFICATION TEST")
    print("=" * 80)
    
    manager = CVTemplateManager()
    
    # Analyze the job
    print(f"\nJob Description Preview:")
    print(f"Length: {len(lime_job)} characters")
    print(f"First 200 chars: {lime_job[:200]}...")
    
    # Get role classification
    detected_role = manager.analyze_job_role(lime_job)
    print(f"\nDetected Role: {detected_role}")
    
    # Get detailed breakdown
    breakdown = manager.get_role_breakdown(lime_job, threshold=1.0)
    print(f"\nDetailed Role Breakdown (>1%):")
    for role, percentage in breakdown:
        print(f"  {role}: {percentage:.1f}%")
    
    # Get all percentages for analysis
    all_percentages = manager.get_role_percentages(lime_job)
    print(f"\nComplete Role Analysis:")
    for role, percentage in sorted(all_percentages.items(), key=lambda x: x[1], reverse=True):
        if percentage > 0:
            print(f"  {role}: {percentage:.2f}%")
    
    # Expected vs Actual
    print(f"\n" + "="*50)
    print(f"ANALYSIS SUMMARY")
    print(f"="*50)
    print(f"Expected Role: fullstack_developer or backend_developer")
    print(f"Actual Role: {detected_role}")
    
    if detected_role in ['fullstack_developer', 'backend_developer']:
        print("✅ CLASSIFICATION CORRECT")
    else:
        print("❌ CLASSIFICATION INCORRECT")
        print(f"Issue: Job has strong fullstack indicators (Vue.js, C#, TypeScript)")
        print(f"But DevOps keywords (AWS, Kubernetes, CI/CD) are getting higher weight")

if __name__ == '__main__':
    test_lime_job_classification()