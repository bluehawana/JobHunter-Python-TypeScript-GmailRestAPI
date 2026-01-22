#!/usr/bin/env python3
"""Test Volvo Verama job extraction"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content

# Volvo Verama job content
volvo_content = """CI/CD DevOps DeveloperJR-48785Published on 21 Jan 2026 byVolvo Personvagnar Aktiebolag (Volvo Cars)Rolesoftware EngineerSeniority levelSeniorLocationGothenburg (SE)Remote0%Assignment period26 Jan 202631 Dec 2026Application deadline23 Jan 2026 23:59 (1 day left)Assignment descriptionFor our client we are looking for a CI/CD DevOps Developer.In the Connectivity and Cloud Platform team, we work build products that make owning a carbetter. We work on platforms such as Connected Car Cloud Platform, Telematics Platformand Mobile Network Access to connect our cars all over the world."""

volvo_url = "https://app.verama.com/app/job-requests/75361"

print("🔍 Testing Volvo Verama Job Extraction")
print("=" * 60)

result = extract_linkedin_job_info_from_content(volvo_content, volvo_url)

print(f"\n✅ Extraction Results:")
print(f"   Company: {result['company']}")
print(f"   Title: {result['title']}")
print(f"   Success: {result['success']}")
print(f"   Source: {result.get('source', 'N/A')}")

# Verify correct extraction
expected_company = "Volvo Cars"
expected_title = "CI/CD DevOps Developer"

if result['company'] == expected_company and result['title'] == expected_title:
    print(f"\n✅ SUCCESS: Company and title extracted correctly!")
elif 'Volvo' in result['company'] and 'DevOps' in result['title']:
    print(f"\n⚠️  PARTIAL: Close but not exact match")
    print(f"   Expected: '{expected_title}' at '{expected_company}'")
else:
    print(f"\n❌ FAILED: Extraction incorrect")
    print(f"   Expected: '{expected_title}' at '{expected_company}'")
    print(f"   Got: '{result['title']}' at '{result['company']}'")
