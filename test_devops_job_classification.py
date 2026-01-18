#!/usr/bin/env python3
"""
Test script for DevOps job classification to ensure we haven't broken DevOps detection
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

def test_devops_job_classification():
    """Test DevOps job classification"""
    
    # Pure DevOps job description
    devops_job = """
    DevOps Engineer at TechCorp
    
    We are seeking a skilled DevOps Engineer to join our infrastructure team. You will be responsible 
    for building and maintaining our cloud infrastructure and CI/CD pipelines.
    
    Key Responsibilities:
    - Design and implement CI/CD pipelines using Jenkins, GitLab CI, or GitHub Actions
    - Manage AWS cloud infrastructure including EC2, S3, RDS, and Lambda
    - Deploy and manage Kubernetes clusters and containerized applications
    - Implement Infrastructure as Code using Terraform and CloudFormation
    - Monitor system performance using CloudWatch, Prometheus, and Grafana
    - Automate deployment processes and infrastructure provisioning
    - Ensure security best practices across all environments
    - Collaborate with development teams on deployment strategies
    
    Required Skills:
    - 3+ years of DevOps or Infrastructure experience
    - Strong experience with AWS services and cloud architecture
    - Proficiency with Kubernetes and Docker containerization
    - Experience with Infrastructure as Code tools (Terraform, CloudFormation)
    - Knowledge of CI/CD tools and practices
    - Experience with monitoring and logging solutions
    - Scripting skills in Python, Bash, or PowerShell
    - Understanding of networking and security principles
    
    Nice to Have:
    - AWS certifications (Solutions Architect, DevOps Engineer)
    - Experience with Helm charts and ArgoCD
    - Knowledge of service mesh technologies (Istio, Linkerd)
    - Experience with GitOps workflows
    """
    
    print("=" * 80)
    print("DEVOPS JOB CLASSIFICATION TEST")
    print("=" * 80)
    
    manager = CVTemplateManager()
    
    # Analyze the job
    print(f"\nJob Description Preview:")
    print(f"Length: {len(devops_job)} characters")
    print(f"First 200 chars: {devops_job[:200]}...")
    
    # Get role classification
    detected_role = manager.analyze_job_role(devops_job)
    print(f"\nDetected Role: {detected_role}")
    
    # Get detailed breakdown
    breakdown = manager.get_role_breakdown(devops_job, threshold=1.0)
    print(f"\nDetailed Role Breakdown (>1%):")
    for role, percentage in breakdown:
        print(f"  {role}: {percentage:.1f}%")
    
    # Get all percentages for analysis
    all_percentages = manager.get_role_percentages(devops_job)
    print(f"\nComplete Role Analysis:")
    for role, percentage in sorted(all_percentages.items(), key=lambda x: x[1], reverse=True):
        if percentage > 0:
            print(f"  {role}: {percentage:.2f}%")
    
    # Expected vs Actual
    print(f"\n" + "="*50)
    print(f"ANALYSIS SUMMARY")
    print(f"="*50)
    print(f"Expected Role: devops_cloud")
    print(f"Actual Role: {detected_role}")
    
    if detected_role == 'devops_cloud':
        print("✅ CLASSIFICATION CORRECT")
    else:
        print("❌ CLASSIFICATION INCORRECT")
        print(f"Issue: Pure DevOps job should classify as devops_cloud")

if __name__ == '__main__':
    test_devops_job_classification()