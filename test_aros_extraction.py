#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.services.job_url_extractor import JobUrlExtractor

url = "https://career.computerswedenrecruitment.se/jobs/6602293-fullstackutvecklare-till-aros-kapital"

extractor = JobUrlExtractor()
result = extractor.extract_job_details(url)

print("=" * 60)
print("EXTRACTION RESULT:")
print("=" * 60)
print(f"Success: {result.get('success')}")
if result.get('job_details'):
    details = result['job_details']
    print(f"Company: {details.get('company')}")
    print(f"Title: {details.get('title')}")
    print(f"Location: {details.get('location')}")
    print(f"Source: {details.get('source')}")
else:
    print(f"Error: {result.get('error')}")
