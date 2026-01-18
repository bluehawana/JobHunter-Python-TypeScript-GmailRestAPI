#!/usr/bin/env python3
"""
Test the enhanced job extractor with Omegapoint content
"""

from backend.linkedin_job_extractor import extract_linkedin_job_info_from_content

def test_omegapoint_extraction():
    """Test extraction from Omegapoint job page"""
    
    # Sample content from the Omegapoint job page
    omegapoint_content = """
    Java software developer Göteborg - Omegapoint
    
    🔐 Utveckla framtiden med oss! Vill du arbeta i teknologins framkant och säkra både din och våra kunders utveckling? Vi växer och letar nu efter fler vassa systemutvecklare inom Java som vill ta både sin egen och våra kunders utveckling till nästa nivå.
    
    👀 Är du den vi söker?
    Vi söker dig som har stor erfarenhet inom systemutveckling, framför allt inom Java med tillhörande ramverk, exempelvis Spring eller Quarkus.
    """
    
    omegapoint_url = "https://jobb.omegapoint.se/jobs/5647581-java-software-developer-goteborg"
    
    print("🔍 Testing Omegapoint Job Extraction")
    print("=" * 50)
    print(f"URL: {omegapoint_url}")
    print(f"Content preview: {omegapoint_content[:100]}...")
    
    result = extract_linkedin_job_info_from_content(omegapoint_content, omegapoint_url)
    
    print(f"\nResults:")
    print(f"  Company: {result['company']}")
    print(f"  Title: {result['title']}")
    print(f"  Success: {result['success']}")
    print(f"  Source: {result['source']}")
    
    if not result['success']:
        print(f"  Error: {result.get('error', 'Unknown error')}")
    
    # Test expected results
    expected_company = "Omegapoint"
    expected_title = "Java Software Developer Göteborg"
    
    print(f"\n✅ Expected vs Actual:")
    print(f"  Company: {expected_company} vs {result['company']} {'✅' if result['company'] == expected_company else '❌'}")
    print(f"  Title: Expected something with 'Java' and 'Developer' {'✅' if 'java' in result['title'].lower() and 'developer' in result['title'].lower() else '❌'}")

if __name__ == '__main__':
    test_omegapoint_extraction()