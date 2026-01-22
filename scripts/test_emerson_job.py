#!/usr/bin/env python3
"""
Test the complete workflow with Emerson IT Business Analyst job
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content
from app.lego_api import analyze_job_description, customize_cover_letter, build_lego_cv, build_lego_cover_letter
from cv_templates import CVTemplateManager

def test_emerson_job():
    """Test the complete workflow with Emerson job"""

    emerson_job_description = """
    Job Description

    Are you eager to take your career to the next level? If yes, we encourage your application for IT Business Analyst role!

    In this role you be responsible for supporting and developing the IT function, while acting as a link for our business.

    By joining us as an IT Business Analyst in Mölnlycke, this role can be a strong foundation for your future career within Emerson. We encourage advancement and offer tangible development opportunities!

    In This Role, Your Responsibilities Will Be:

    Managing IT initiatives with a focus on digitalization and automation
    Analysing & document business processes and requirements
    Improving business processes using IT, business intelligence and automation
    Acting as project manager for identified initiatives. This includes project leadership, change management, analysing, developing specifications, planning, user training and implementation
    Developing IT solutions according to specification. Beside systemization and programming the development can include investigation, management documentation, user manuals, user training and implementation
    Providing the business with support in areas within the IT & Digitalization team's responsibility
    Applying best practices in development/support using tools in line with Emerson standards

    Who You Are:

    You acquire data from multiple and diverse sources when solving problems and provide timely and helpful information to individuals across the organization. You make decisions and take actions without the total picture, while breaking down objectives into appropriate initiatives and actions.

    You also convert ideas into actions and produce results with new initiatives. You build and deliver solutions that meet customer expectations and you stay on top of new communications technologies.

    For This Role, You Will Need:

    Experience in business analysis and process improvement
    Project management skills with the ability to organize, structure, and plan effectively
    Experience with ERP systems and a solid understanding of business processes
    University degree in IT or equivalent experience
    Fluency in Swedish
    Proficiency in English language (verbal and written)
    General IT knowledge and at least 3 years of relevant professional experience

    Preferred Qualifications that Set You Apart:

    Experience in workshop facilitation and change management
    Professional experience from development of BI reports or RPA automations
    Experience from a manufacturing company
    Knowledge of Lean, Agile, and an interest in AI

    Our Culture and Commitment to You

    At Emerson, we prioritize a workplace where every employee is valued, respected, and empowered to grow.

    About Emerson

    Emerson is a global leader in automation technology and software.
    """

    emerson_url = "https://www.linkedin.com/jobs/view/emerson-it-business-analyst"

    print("=" * 70)
    print("🔍 Testing Emerson IT Business Analyst Job Analysis")
    print("=" * 70)

    # Step 1: Extract job info from content
    print("\n1️⃣ STEP 1: Extract Job Information")
    print("-" * 50)
    job_info = extract_linkedin_job_info_from_content(emerson_job_description, emerson_url)
    print(f"   Company: {job_info['company']}")
    print(f"   Title: {job_info['title']}")
    print(f"   Success: {job_info['success']}")
    print(f"   Source: {job_info.get('source', 'N/A')}")

    # Step 2: Analyze job description
    print("\n2️⃣ STEP 2: Analyze Job Description (Role Detection)")
    print("-" * 50)
    analysis = analyze_job_description(emerson_job_description, emerson_url)
    print(f"   Role Category: {analysis.get('roleCategory', 'N/A')}")
    print(f"   Role Type: {analysis.get('roleType', 'N/A')}")
    print(f"   Company: {analysis.get('company', 'N/A')}")
    print(f"   Title: {analysis.get('title', 'N/A')}")
    print(f"   Confidence: {analysis.get('confidence', 0):.0%}")
    print(f"   Keywords: {analysis.get('keywords', [])[:10]}")

    # Step 3: Check which template would be used
    print("\n3️⃣ STEP 3: Template Selection")
    print("-" * 50)
    template_manager = CVTemplateManager()
    role_category = analysis.get('roleCategory', 'backend_developer')

    cv_template_path = template_manager.ROLE_CATEGORIES.get(role_category, {}).get('cv_template', 'N/A')
    cl_template_path = template_manager.ROLE_CATEGORIES.get(role_category, {}).get('cl_template', 'N/A')

    print(f"   Role Category: {role_category}")
    print(f"   CV Template: {cv_template_path}")
    print(f"   CL Template: {cl_template_path}")

    # Step 4: Test CL customization
    print("\n4️⃣ STEP 4: Cover Letter Customization Test")
    print("-" * 50)

    company = analysis.get('company', 'Emerson')
    title = analysis.get('title', 'IT Business Analyst')

    # Load the actual CL template
    cl_template = template_manager.load_template(role_category, 'cl')
    if cl_template:
        customized_cl = customize_cover_letter(cl_template, company, title)

        # Show the header part
        lines = customized_cl.split('\n')
        header_lines = []
        in_header = False
        for line in lines:
            if 'begin{document}' in line:
                in_header = True
            if in_header:
                header_lines.append(line)
                if 'Dear' in line or len(header_lines) > 20:
                    break

        print("   CL Header Preview:")
        print("   " + "─" * 45)
        for line in header_lines[:15]:
            if line.strip():
                print(f"   {line[:70]}")
        print("   " + "─" * 45)

        # Verify placeholders are replaced
        has_company_placeholder = 'COMPANY_NAME' in customized_cl or 'COMPANY\\_NAME' in customized_cl
        has_title_placeholder = 'JOB_TITLE' in customized_cl or 'JOB\\_TITLE' in customized_cl

        print(f"\n   ✅ Company in CL: {'❌ PLACEHOLDER FOUND' if has_company_placeholder else '✅ ' + company}")
        print(f"   ✅ Title in CL: {'❌ PLACEHOLDER FOUND' if has_title_placeholder else '✅ ' + title}")
    else:
        print("   ⚠️ No CL template found for this role")

    # Step 5: Summary
    print("\n" + "=" * 70)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"   Company Detected: {analysis.get('company', 'N/A')}")
    print(f"   Job Title: {analysis.get('title', 'N/A')}")
    print(f"   Role Category: {role_category}")
    print(f"   CV Template: {cv_template_path.split('/')[-1] if cv_template_path != 'N/A' else 'N/A'}")
    print(f"   CL Template: {cl_template_path.split('/')[-1] if cl_template_path != 'N/A' else 'N/A'}")

    # Verification
    print("\n" + "=" * 70)
    print("✅ VERIFICATION")
    print("=" * 70)

    issues = []
    if analysis.get('company', '') in ['Company', 'Technology Company', '']:
        issues.append("❌ Company name not extracted properly")
    else:
        print(f"   ✅ Company extracted: {analysis.get('company')}")

    if analysis.get('title', '') in ['Position', 'Software Engineer', '']:
        issues.append("❌ Job title not extracted properly")
    else:
        print(f"   ✅ Job title extracted: {analysis.get('title')}")

    if role_category == 'it_business_analyst':
        print(f"   ✅ Correct role category: {role_category}")
    else:
        issues.append(f"⚠️ Role category might be wrong: {role_category} (expected: it_business_analyst)")

    if issues:
        print("\n   Issues found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n   🎉 All checks passed!")

    return analysis

if __name__ == '__main__':
    test_emerson_job()
