#!/usr/bin/env python3
"""Test Stena Metall job extraction"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content

# Stena Metall job content
stena_content = """
Infrastructure Architect | Stena Metall

Are you passionate about designing infrastructure that enables business success and drives the transition to cloud solutions? If so, we have an exciting opportunity for you! 
As an Infrastructure Architect, you will ensure a robust, secure, and cost-effective IT infrastructure that supports our business needs and accelerates our journey toward cloud-based environments.
"""

stena_url = "https://www.stenametall.com/sv/jobba-hos-oss/lediga-tjanster/ledig-tjanst/infrastructure-architect-se-3215/"

print("🔍 Testing Stena Metall Job Extraction")
print("=" * 60)

result = extract_linkedin_job_info_from_content(stena_content, stena_url)

print(f"\n✅ Extraction Results:")
print(f"   Company: {result['company']}")
print(f"   Title: {result['title']}")
print(f"   Success: {result['success']}")
print(f"   Source: {result.get('source', 'N/A')}")

# Verify correct extraction
if result['company'] == 'Stena Metall' and result['title'] == 'Infrastructure Architect':
    print("\n✅ SUCCESS: Company and title extracted correctly!")
else:
    print(f"\n❌ FAILED: Expected 'Stena Metall' and 'Infrastructure Architect'")
    print(f"   Got: '{result['company']}' and '{result['title']}'")
