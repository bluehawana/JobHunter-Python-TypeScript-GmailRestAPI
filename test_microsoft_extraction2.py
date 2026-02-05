#!/usr/bin/env python3
"""Test Microsoft job extraction with noise"""

import re

def extract_company_and_title_from_text(job_description: str) -> tuple:
    """Extract company and title - LinkedIn format with noise handling"""
    lines = [line.strip() for line in job_description.split('\n') if line.strip()]
    company = 'Company'
    title = 'Position'
    
    # STRATEGY 1: Check first 5 lines for company + title pattern
    job_keywords = [
        'engineer', 'developer', 'specialist', 'manager', 'architect', 
        'lead', 'senior', 'junior', 'consultant', 'analyst', 'support',
        'coordinator', 'administrator', 'technician', 'designer', 'product',
    ]
    
    for i in range(min(5, len(lines) - 1)):
        potential_company = lines[i].strip()
        potential_title = lines[i + 1].strip()
        
        # Validate company
        invalid_company_patterns = [
            r'\d+\s*(hour|day|week|month|year|minute)s?\s*(ago)?',
            r'(engineer|developer|specialist|manager|architect|lead|senior|junior|consultant|analyst)',
            r'^(the|a|an)\s+',
            r'·',
            r'(services|solutions|systems)$',  # Generic words alone
        ]
        
        is_valid_company = (
            len(potential_company) < 60 and 
            len(potential_company) > 2 and
            not any(re.search(pattern, potential_company, re.IGNORECASE) for pattern in invalid_company_patterns)
        )
        
        # Validate title
        is_valid_title = (
            len(potential_title) < 100 and 
            len(potential_title) > 5 and
            any(keyword in potential_title.lower() for keyword in job_keywords)
        )
        
        if is_valid_company and is_valid_title:
            company = potential_company
            title = potential_title
            print(f"📍 LinkedIn format detected at line {i} - Company: {company}, Title: {title}")
            return (company, title)
    
    return (company, title)


# Test with noise before company
linkedin_job_with_noise = """all up services
Cloud Solution Architect-Power Platform
Gothenburg, Sweden"""

print("Test 1: With noise before company")
print("=" * 60)
company, title = extract_company_and_title_from_text(linkedin_job_with_noise)
print(f"✅ Company: {company}, Title: {title}\n")

# Test with clean format
linkedin_job_clean = """Microsoft
Cloud Solution Architect-Power Platform
Sweden · 1 hour ago"""

print("Test 2: Clean LinkedIn format")
print("=" * 60)
company, title = extract_company_and_title_from_text(linkedin_job_clean)
print(f"✅ Company: {company}, Title: {title}\n")

# The issue: "all up services" doesn't have job keywords, so it passes validation
# But "Cloud Solution Architect" DOES have "architect" keyword
# So it should match on line 1-2 pair
