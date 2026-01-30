#!/usr/bin/env python3
"""
Test script for dynamic cover letter generation
"""

from services.dynamic_cover_letter_generator import generate_dynamic_cover_letter, preview_extracted_info

def test_url_extraction():
    """Test company information extraction from various job board URLs"""
    
    test_urls = [
        "https://www.linkedin.com/jobs/view/3021234567/",  # Example LinkedIn URL
        "https://www.glassdoor.com/job-listing/senior-developer-volvo-JV_IC123456.htm",  # Example Glassdoor URL
        "https://www.indeed.com/viewjob?jk=abc123def456"  # Example Indeed URL
    ]
    
    print("Testing company information extraction:")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            info = preview_extracted_info(url)
            print(f"Company Name: {info['company_name']}")
            print(f"Address: {info['company_address']}")
            print(f"Greeting: {info['greeting']}")
        except Exception as e:
            print(f"Error: {e}")

def test_dynamic_generation():
    """Test full dynamic cover letter generation"""
    
    # Example job data
    job_data = {
        'title': 'Senior Backend Developer',
        'description': 'We are looking for a Python developer with DevOps experience to join our team. Experience with Kubernetes, Docker, and AWS is preferred.'
    }
    
    # Test URL (you can replace with real URL)
    test_url = "https://www.linkedin.com/jobs/view/example/"
    
    print("\n" + "=" * 50)
    print("Testing dynamic cover letter generation:")
    print("=" * 50)
    
    try:
        cover_letter = generate_dynamic_cover_letter(test_url, job_data)
        print("Generated cover letter:")
        print(cover_letter[:500] + "..." if len(cover_letter) > 500 else cover_letter)
    except Exception as e:
        print(f"Error generating cover letter: {e}")

if __name__ == "__main__":
    test_url_extraction()
    test_dynamic_generation()