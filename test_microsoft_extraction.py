#!/usr/bin/env python3
"""Test Microsoft job extraction - standalone version"""

import re

def extract_company_and_title_from_text(job_description: str) -> tuple:
    """Extract company and title - LinkedIn format first"""
    lines = [line.strip() for line in job_description.split('\n') if line.strip()]
    company = 'Company'
    title = 'Position'
    
    # STRATEGY 1: LinkedIn format - First line is company, second line is title
    if len(lines) >= 2:
        potential_company = lines[0].strip()
        potential_title = lines[1].strip()
        
        # Validate company
        invalid_company_patterns = [
            r'\d+\s*(hour|day|week|month|year|minute)s?\s*(ago)?',
            r'(engineer|developer|specialist|manager|architect|lead|senior|junior|consultant|analyst)',
            r'^(the|a|an)\s+',
            r'·',
        ]
        
        is_valid_company = (
            len(potential_company) < 60 and 
            len(potential_company) > 2 and
            not any(re.search(pattern, potential_company, re.IGNORECASE) for pattern in invalid_company_patterns)
        )
        
        # Validate title
        job_keywords = [
            'engineer', 'developer', 'specialist', 'manager', 'architect', 
            'lead', 'senior', 'junior', 'consultant', 'analyst', 'support',
            'coordinator', 'administrator', 'technician', 'designer', 'product',
        ]
        
        is_valid_title = (
            len(potential_title) < 100 and 
            len(potential_title) > 5 and
            any(keyword in potential_title.lower() for keyword in job_keywords)
        )
        
        if is_valid_company and is_valid_title:
            company = potential_company
            title = potential_title
            print(f"📍 LinkedIn format detected - Company: {company}, Title: {title}")
            return (company, title)
    
    return (company, title)


# Test with Microsoft job
linkedin_job = """Microsoft
Cloud Solution Architect-Power Platform
Sweden · 1 hour ago · 1 person clicked apply
Promoted by hirer · Responses managed off LinkedIn
Remote
Full-time

About the job
Overview With more than 45,000 employees and partners worldwide..."""

print("Testing Microsoft job extraction...")
print("=" * 60)

company, title = extract_company_and_title_from_text(linkedin_job)

print(f"\n✅ Extracted Company: {company}")
print(f"✅ Extracted Title: {title}")
print()

# Verify
assert company == "Microsoft", f"Expected 'Microsoft', got '{company}'"
assert title == "Cloud Solution Architect-Power Platform", f"Expected 'Cloud Solution Architect-Power Platform', got '{title}'"

print("🎉 All tests passed! LinkedIn format extraction works perfectly!")
