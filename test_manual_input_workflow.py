#!/usr/bin/env python3
"""
Test the manual input workflow when automatic extraction fails
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description

def test_manual_input_workflow():
    """Test workflow when extraction fails and manual input is required"""
    
    # Job description without clear company/title information
    unclear_job_description = """
    We are looking for a talented individual to join our team. 
    The successful candidate will work with modern technologies and contribute to exciting projects.
    
    Requirements:
    - Experience with Python and JavaScript
    - Knowledge of cloud platforms
    - Strong problem-solving skills
    
    We offer competitive salary and great benefits.
    """
    
    print("🔍 Testing Manual Input Workflow")
    print("=" * 50)
    
    # Step 1: Analyze job with unclear information
    print("\n1️⃣ Analyzing unclear job description...")
    analysis = analyze_job_description(unclear_job_description)
    
    print(f"   Company: '{analysis.get('company', 'N/A')}'")
    print(f"   Title: '{analysis.get('title', 'N/A')}'")
    print(f"   Extraction Success: {analysis.get('extractionStatus', {}).get('success', 'N/A')}")
    print(f"   Requires Manual Input: {analysis.get('extractionStatus', {}).get('requiresManualInput', 'N/A')}")
    print(f"   Issues: {analysis.get('extractionStatus', {}).get('issues', [])}")
    
    # Step 2: Simulate manual input
    print("\n2️⃣ Simulating manual input...")
    manual_company = "TechCorp AB"
    manual_title = "Senior Python Developer"
    
    # Update analysis with manual input (simulating the API call)
    analysis['company'] = manual_company
    analysis['title'] = manual_title
    analysis['extractionStatus'] = {
        'success': True,
        'issues': [],
        'requiresManualInput': False,
        'message': 'Company and job title provided manually',
        'source': 'manual_input'
    }
    
    print(f"   Manual Company: {manual_company}")
    print(f"   Manual Title: {manual_title}")
    
    # Step 3: Verify the updated analysis
    print("\n3️⃣ Verification after manual input...")
    print(f"   ✅ Company updated: {analysis['company']}")
    print(f"   ✅ Title updated: {analysis['title']}")
    print(f"   ✅ Extraction now successful: {analysis['extractionStatus']['success']}")
    print(f"   ✅ Source: {analysis['extractionStatus']['source']}")
    
    # Step 4: Test template customization with manual input
    print("\n4️⃣ Testing template customization with manual input...")
    from app.lego_api import customize_cover_letter
    
    template_content = """
COMPANY\_NAME\\
JOB\_TITLE\\
Gothenburg, Sweden

Dear Hiring Manager,

I am excited to apply for the JOB\_TITLE position at COMPANY\_NAME...
"""
    
    customized = customize_cover_letter(template_content, manual_company, manual_title)
    
    print("   Customized template preview:")
    print("   " + "─" * 40)
    for line in customized.split('\n')[:6]:
        if line.strip():
            print(f"   {line}")
    print("   " + "─" * 40)
    
    # Final verification
    success = (
        analysis['extractionStatus']['success'] and
        analysis['company'] == manual_company and
        analysis['title'] == manual_title and
        manual_company in customized and
        manual_title in customized
    )
    
    print(f"\n🎉 Manual Input Workflow Success: {'✅' if success else '❌'}")
    
    return success

if __name__ == '__main__':
    test_manual_input_workflow()