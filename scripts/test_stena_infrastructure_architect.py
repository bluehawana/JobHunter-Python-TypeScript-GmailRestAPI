#!/usr/bin/env python3
"""
Test Stena Infrastructure Architect job detection
"""

import sys
from pathlib import Path
sys.path.append('backend')

from app.lego_api import analyze_job_description, fetch_job_from_url

# Test URL
job_url = "https://www.stenametall.com/sv/jobba-hos-oss/lediga-tjanster/ledig-tjanst/infrastructure-architect-se-3215/"

print("🔍 Testing Stena Infrastructure Architect Job")
print("=" * 70)
print(f"URL: {job_url}\n")

# Try to fetch job description
print("1️⃣ Fetching job description...")
try:
    job_description = fetch_job_from_url(job_url)
    if job_description:
        print(f"✓ Fetched {len(job_description)} characters")
        print(f"\nFirst 500 chars:\n{job_description[:500]}\n")
    else:
        print("⚠️ Could not fetch job description from URL")
        print("Using manual job description instead...\n")
        
        # Manual job description
        job_description = """
Infrastructure Architect
Stena Metall
Gothenburg, Sweden

We are looking for an Infrastructure Architect to join our IT team. In this role, you will design and implement our infrastructure solutions, working with cloud platforms, networking, and system architecture.

Key Responsibilities:
- Design and implement infrastructure architecture solutions
- Work with cloud platforms (Azure, AWS)
- Manage networking, security, and system integration
- Lead infrastructure projects and technical initiatives
- Collaborate with development teams on infrastructure requirements
- Ensure scalability, reliability, and security of infrastructure

Requirements:
- Experience with infrastructure architecture and design
- Strong knowledge of cloud platforms (Azure, AWS)
- Experience with networking, security, and system integration
- Knowledge of containerization (Docker, Kubernetes)
- Experience with infrastructure as code (Terraform, Ansible)
- Strong communication and leadership skills
"""
except Exception as e:
    print(f"⚠️ Error fetching: {e}")
    print("Using manual job description...\n")
    
    job_description = """
Infrastructure Architect
Stena Metall
Gothenburg, Sweden

We are looking for an Infrastructure Architect to join our IT team. In this role, you will design and implement our infrastructure solutions, working with cloud platforms, networking, and system architecture.

Key Responsibilities:
- Design and implement infrastructure architecture solutions
- Work with cloud platforms (Azure, AWS)
- Manage networking, security, and system integration
- Lead infrastructure projects and technical initiatives
- Collaborate with development teams on infrastructure requirements
- Ensure scalability, reliability, and security of infrastructure

Requirements:
- Experience with infrastructure architecture and design
- Strong knowledge of cloud platforms (Azure, AWS)
- Experience with networking, security, and system integration
- Knowledge of containerization (Docker, Kubernetes)
- Experience with infrastructure as code (Terraform, Ansible)
- Strong communication and leadership skills
"""

# Analyze job
print("2️⃣ Analyzing job role...")
analysis = analyze_job_description(job_description)

print(f"\n📊 Analysis Results:")
print(f"   Role Category: {analysis.get('roleCategory', 'Unknown')}")
print(f"   Confidence: {analysis.get('confidence', 0)}%")
print(f"   AI Analysis: {analysis.get('aiAnalysis', 'N/A')}")

if 'reasoning' in analysis:
    print(f"\n💭 Reasoning:\n{analysis['reasoning']}")

print("\n" + "=" * 70)
print("Expected: devops or infrastructure_architect")
print(f"Actual: {analysis.get('roleCategory', 'Unknown')}")

if analysis.get('roleCategory') != 'devops':
    print("\n⚠️ ISSUE: Role not correctly detected as DevOps/Infrastructure!")
