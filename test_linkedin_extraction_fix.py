#!/usr/bin/env python3
"""
Test LinkedIn job extraction fix for the cover letter issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.linkedin_job_extractor import extract_linkedin_job_info_from_content

def test_meltwater_extraction():
    """Test extraction with the Meltwater job description"""
    
    # Meltwater job description from LinkedIn
    meltwater_job = """
    As a Software Engineer with the information retrieval team at Meltwater you will be building 
    petabyte-scale search and analytics systems using Elasticsearch running on AWS. Every day, 
    we add 1.3B new documents into our search platform and process over 6B engagement activities 
    to provide the most complete dataset possible. This data fuels our products with robust insights 
    that span key areas that include media, social, influencer, sales, and consumer intelligence.

    In addition to working with large-scale distributed systems, you will also have the opportunity 
    to work on cutting-edge vector search technologies and explore use cases powered by Large Language 
    Models (LLMs). These initiatives enable semantic search capabilities, enhanced content understanding, 
    and more intelligent data discovery experiences for our users.

    Our culture is based on a fundamental belief in people with a passion for learning new things 
    and a desire to help those around you. We are strong believers in team autonomy, DevOps culture 
    and continuous delivery. Meltwater development teams fully own and operate their subsystems 
    and infrastructure and run on-call rotations.

    We run on AWS and are heavy users of AWS services, Elasticsearch, Cassandra, Terraform, Docker; 
    with a sprinkling of other database and messaging technologies depending on the need.

    For this role, you will benefit by having some experience with search engines, big data analytics, 
    infrastructure, systems engineering and distributed systems. Experience with vector search and 
    applied use of Large Language Models (LLMs) is also a plus.
    """
    
    print("🔍 Testing LinkedIn Job Extraction Fix")
    print("=" * 60)
    print("Testing with Meltwater job description...")
    
    # Test the extraction
    result = extract_linkedin_job_info_from_content(meltwater_job, "https://www.linkedin.com/jobs/view/4357664024")
    
    print(f"\nExtraction Results:")
    print(f"  Company: '{result['company']}'")
    print(f"  Title: '{result['title']}'")
    print(f"  Success: {result['success']}")
    print(f"  Source: {result['source']}")
    
    # Check if extraction was successful
    if result['success'] and result['company'] == 'Meltwater' and result['title'] == 'Software Engineer':
        print("\n✅ SUCCESS: Extraction worked correctly!")
        print("   This should fix the cover letter issue where it showed:")
        print("   'You'll Bring' instead of 'Meltwater'")
        print("   '[Position]' instead of 'Software Engineer'")
    else:
        print("\n❌ ISSUE: Extraction didn't work as expected")
        print("   Expected: Company='Meltwater', Title='Software Engineer'")
        print(f"   Got: Company='{result['company']}', Title='{result['title']}'")
    
    return result['success']

def test_generic_job():
    """Test with a generic job description without clear company name"""
    
    generic_job = """
    We are looking for a Senior DevOps Engineer to join our team. You will work with 
    Kubernetes, Docker, and AWS to build scalable infrastructure. Experience with 
    CI/CD pipelines and monitoring tools is required.
    """
    
    print(f"\n🧪 Testing with generic job description...")
    
    result = extract_linkedin_job_info_from_content(generic_job, "")
    
    print(f"  Company: '{result['company']}'")
    print(f"  Title: '{result['title']}'")
    print(f"  Success: {result['success']}")
    
    # Should fall back to defaults
    if result['company'] == 'Technology Company' and 'Engineer' in result['title']:
        print("  ✅ Fallback working correctly")
    else:
        print("  ⚠️ Fallback may need adjustment")

if __name__ == '__main__':
    print("🚀 Testing LinkedIn Job Extraction Fix for Cover Letter Issue\n")
    
    success = test_meltwater_extraction()
    test_generic_job()
    
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 SOLUTION READY!")
        print("The LinkedIn job extraction should now correctly identify:")
        print("  • Company: Meltwater")
        print("  • Title: Software Engineer")
        print("\nThis will fix the cover letter template placeholders!")
    else:
        print("⚠️ NEEDS MORE WORK")
        print("The extraction logic may need refinement.")
    
    print(f"\n💡 Next Steps:")
    print("1. Test the full application with the LinkedIn URL")
    print("2. Verify cover letter generation uses correct company/title")
    print("3. Push changes to VPS for production use")