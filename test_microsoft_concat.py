#!/usr/bin/env python3
"""Test Microsoft concatenated LinkedIn format"""

import re

def extract_company(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    company = 'Company'
    title = 'Position'
    
    # Check for Microsoft
    full_text = ' '.join(lines).lower()
    if 'microsoft' in full_text:
        company = 'Microsoft'
        print(f"📍 Found priority company: {company}")
    
    # LinkedIn concatenated format
    if len(lines) == 1 or (len(lines) > 0 and len(lines[0]) > 100):
        text_line = lines[0] if len(lines) > 0 else text
        # Split on location/time info
        text_before_location = re.split(r'Sweden|Gothenburg|Stockholm|Remote|·|\d+\s*(?:hour|day|week|month)s?\s*ago', text_line)[0]
        
        job_title_pattern = r'([A-Z][a-zA-Z\s\-/\.&]+(?:Engineer|Developer|Specialist|Manager|Architect|Lead|Senior|Consultant|Analyst|Coordinator|Administrator|Designer|Product)(?:\s+[A-Z][a-zA-Z\s\-/\.&]*)?)'
        title_matches = re.findall(job_title_pattern, text_before_location)
        
        if title_matches and company != 'Company':
            # Take the last match
            title = title_matches[-1].strip()
            # Clean up
            title = re.sub(r'(Sweden|Gothenburg|Stockholm|Remote).*$', '', title).strip()
            print(f"📍 Extracted title: {title}")
            return (company, title)
    
    return (company, title)


# Exact text you pasted
linkedin_concat = """MicrosoftShareShow more optionsCloud Solution Architect-Power PlatformSweden · 2 hours ago · 3 people clicked applyPromoted by hirer · Responses managed off LinkedInRemoteMatches your job preferences, workplace type is Remote. Full-timeMatches your job preferences, job type is Full-time.ApplySaveSave Cloud Solution Architect-Power Platform  at MicrosoftJob match is medium, review match detailsYour profile matches several of the required qualificationsShow match detailsTailor my resumeHelp me update my profileCreate cover letterBETAIs this information helpful?About the jobOverview With more than 45,000 employees and partners worldwide, the Customer Experience and Success (CE&S) organization is on a mission to empower customers to accelerate business value through differentiated customer experiences that leverage Microsoft's products and services, ignited by our people and culture. We drive cross-company alignment and execution, ensuring that we consistently exceed customers' expectations in every interaction, whether in-product, digital, or human-centered. CE&S is responsible for all up services across the company, including consulting, customer success, and support across Microsoft's portfolio of solutions and products. Join CE&S and help us accelerate AI transformation for our customers and the world."""

print("Testing Microsoft concatenated LinkedIn format...")
print("=" * 60)

company, title = extract_company(linkedin_concat)

print(f"\n✅ Company: {company}")
print(f"✅ Title: {title}")
print()

assert company == "Microsoft", f"Expected 'Microsoft', got '{company}'"
print("🎉 Test passed!")
