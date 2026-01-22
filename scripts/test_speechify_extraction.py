#!/usr/bin/env python3
"""Test Speechify job extraction"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content

# Speechify job content - paste the actual job description here
speechify_content = """
Software Engineer, Platform

Gothenburg, Sweden at Speechify

Job Application for Software Engineer, Platform

[Paste the full job description here]
"""

speechify_url = "https://speechify.com/careers"  # or actual URL

print("🔍 Testing Speechify Job Extraction")
print("=" * 60)

result = extract_linkedin_job_info_from_content(speechify_content, speechify_url)

print(f"\n✅ Extraction Results:")
print(f"   Company: {result['company']}")
print(f"   Title: {result['title']}")
print(f"   Success: {result['success']}")
print(f"   Source: {result.get('source', 'N/A')}")

# Verify correct extraction
expected_company = "Speechify"
expected_title = "Software Engineer, Platform"

if result['company'] == expected_company and result['title'] == expected_title:
    print(f"\n✅ SUCCESS: Company and title extracted correctly!")
else:
    print(f"\n❌ FAILED: Extraction incorrect")
    print(f"   Expected: '{expected_title}' at '{expected_company}'")
    print(f"   Got: '{result['title']}' at '{result['company']}'")
