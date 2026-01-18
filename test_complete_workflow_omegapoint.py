#!/usr/bin/env python3
"""
Test the complete workflow with Omegapoint job URL
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content
from app.lego_api import analyze_job_description, customize_cover_letter

def test_complete_workflow():
    """Test the complete workflow from URL to customized cover letter"""
    
    # Omegapoint job details
    omegapoint_url = "https://jobb.omegapoint.se/jobs/5647581-java-software-developer-goteborg"
    omegapoint_content = """
    Java software developer Göteborg - Omegapoint
    
    🔐 Utveckla framtiden med oss! Vill du arbeta i teknologins framkant och säkra både din och våra kunders utveckling? Vi växer och letar nu efter fler vassa systemutvecklare inom Java som vill ta både sin egen och våra kunders utveckling till nästa nivå.
    
    👀 Är du den vi söker?
    Vi söker dig som har stor erfarenhet inom systemutveckling, framför allt inom Java med tillhörande ramverk, exempelvis Spring eller Quarkus. Självklart värderar vi kompetens inom tex molntjänster och agila metoder också.
    """
    
    print("🔍 Testing Complete Workflow: Omegapoint Job")
    print("=" * 60)
    
    # Step 1: Extract job info from URL
    print("\n1️⃣ Extracting job information...")
    job_info = extract_linkedin_job_info_from_content(omegapoint_content, omegapoint_url)
    print(f"   Company: {job_info['company']}")
    print(f"   Title: {job_info['title']}")
    print(f"   Success: {job_info['success']}")
    
    # Step 2: Analyze job description
    print("\n2️⃣ Analyzing job description...")
    analysis = analyze_job_description(omegapoint_content, omegapoint_url)
    print(f"   Role Category: {analysis.get('roleCategory', 'N/A')}")
    print(f"   Company: {analysis.get('company', 'N/A')}")
    print(f"   Title: {analysis.get('title', 'N/A')}")
    
    # Step 3: Test template customization
    print("\n3️⃣ Testing template customization...")
    
    # Sample template content with placeholders
    template_content = """
COMPANY\_NAME\\
JOB\_TITLE\\
Gothenburg, Sweden

Dear Hiring Manager,

I am excited to apply for the JOB\_TITLE position at COMPANY\_NAME. As a backend developer with expertise in Java and Spring Boot...

Sincerely,\\
Harvad (Hongzhi) Li
"""
    
    customized = customize_cover_letter(
        template_content, 
        analysis.get('company', 'Omegapoint'), 
        analysis.get('title', 'Java Software Developer')
    )
    
    print("   Customized template preview:")
    print("   " + "─" * 50)
    for line in customized.split('\n')[:10]:
        if line.strip():
            print(f"   {line}")
    print("   " + "─" * 50)
    
    # Step 4: Verify placeholders are replaced
    print("\n4️⃣ Verification...")
    has_company_placeholder = 'COMPANY\_NAME' in customized or 'COMPANY_NAME' in customized
    has_title_placeholder = 'JOB\_TITLE' in customized or 'JOB_TITLE' in customized
    
    print(f"   ✅ Company placeholder replaced: {'❌' if has_company_placeholder else '✅'}")
    print(f"   ✅ Title placeholder replaced: {'❌' if has_title_placeholder else '✅'}")
    print(f"   ✅ Contains 'Omegapoint': {'✅' if 'Omegapoint' in customized else '❌'}")
    print(f"   ✅ Contains 'Java': {'✅' if 'Java' in customized else '❌'}")
    
    success = not has_company_placeholder and not has_title_placeholder
    print(f"\n🎉 Overall Success: {'✅' if success else '❌'}")
    
    return success

if __name__ == '__main__':
    test_complete_workflow()