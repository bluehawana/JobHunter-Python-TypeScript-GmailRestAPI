#!/usr/bin/env python3
"""
Test the complete workflow with Emerson IT Business Analyst job
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description, build_lego_cv, build_lego_cover_letter

def test_emerson_workflow():
    """Test the complete workflow with Emerson job"""
    
    emerson_job_description = """
About the job
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
At Emerson, we prioritize a workplace where every employee is valued, respected, and empowered to grow. We foster an environment that encourages innovation, collaboration, and diverse perspectives—because we know that great ideas come from great teams. Our commitment to ongoing career development and growing an inclusive culture ensures you have the support to thrive. Whether through mentorship, training, or leadership opportunities, we invest in your success so you can make a lasting impact. We believe diverse teams, working together are key to driving growth and delivering business results.

About Us 
WHY EMERSON 
Our Commitment to Our People 
At Emerson, we are motivated by a spirit of collaboration that helps our diverse, multicultural teams across the world drive innovation that makes the world healthier, safer, smarter, and more sustainable. And we want you to join us in our bold aspiration.
We have built an engaged community of inquisitive, dedicated people who thrive knowing they are welcomed, trusted, celebrated, and empowered to solve the world's most complex problems — for our customers, our communities, and the planet. You'll contribute to this vital work while further developing your skills through our award-winning employee development programs. We are a proud corporate citizen in every city where we operate and are committed to our people, our communities, and the world at large. We take this responsibility seriously and strive to make a positive impact through every endeavor.
At Emerson, you'll see firsthand that our people are at the center of everything we do. So, let's go. Let's think differently. Learn, collaborate, and grow. Seek opportunity. Push boundaries. Be empowered to make things better. Speed up to break through. Let's go, together.
"""
    
    print("🔍 Testing Complete Workflow: Emerson IT Business Analyst")
    print("=" * 70)
    
    # Step 1: Analyze job description
    print("\n1️⃣ Analyzing job description...")
    analysis = analyze_job_description(emerson_job_description)
    
    print(f"   Role Category: {analysis.get('roleCategory', 'N/A')}")
    print(f"   Role Type: {analysis.get('roleType', 'N/A')}")
    print(f"   Company: {analysis.get('company', 'N/A')}")
    print(f"   Title: {analysis.get('title', 'N/A')}")
    print(f"   Extraction Success: {analysis.get('extractionStatus', {}).get('success', 'N/A')}")
    print(f"   Key Technologies: {analysis.get('keywords', [])[:5]}")
    
    # Step 2: Generate CV
    print("\n2️⃣ Generating CV...")
    cv_content = build_lego_cv(
        role_type=analysis.get('roleType', 'IT Business Analyst'),
        company='Emerson',
        title='IT Business Analyst',
        role_category=analysis.get('roleCategory', 'it_business_analyst'),
        job_description=emerson_job_description
    )
    
    # Save CV for inspection
    with open('test_emerson_cv.tex', 'w', encoding='utf-8') as f:
        f.write(cv_content)
    
    print(f"   CV Length: {len(cv_content)} characters")
    print(f"   CV Pages (estimated): {len(cv_content) // 2000} pages")
    print(f"   Contains Java/Spring: {'Java' in cv_content or 'Spring' in cv_content}")
    print(f"   Contains Business Analysis: {'business analysis' in cv_content.lower()}")
    print(f"   Uses LinkedIn Blue: {'linkedinblue' in cv_content}")
    
    # Step 3: Generate Cover Letter
    print("\n3️⃣ Generating Cover Letter...")
    cl_content = build_lego_cover_letter(
        role_type=analysis.get('roleType', 'IT Business Analyst'),
        company='Emerson',
        title='IT Business Analyst',
        role_category=analysis.get('roleCategory', 'it_business_analyst'),
        job_description=emerson_job_description
    )
    
    # Save CL for inspection
    with open('test_emerson_cl.tex', 'w', encoding='utf-8') as f:
        f.write(cl_content)
    
    print(f"   CL Length: {len(cl_content)} characters")
    print(f"   Has Professional Header: {'Large' in cl_content and 'textbf' in cl_content}")
    print(f"   Has Bold Sections: {'textbf{' in cl_content}")
    print(f"   Company Replaced: {'Emerson' in cl_content}")
    print(f"   Title Replaced: {'IT Business Analyst' in cl_content}")
    print(f"   Uses LinkedIn Blue: {'linkedinblue' in cl_content}")
    print(f"   Has Clean Footer: {'Ebbe Lieberathsgatan' in cl_content}")
    
    # Step 4: Verification
    print("\n4️⃣ Verification Results...")
    
    cv_issues = []
    cl_issues = []
    
    # CV Checks
    if len(cv_content) < 5000:
        cv_issues.append("CV too short (should be ~3 pages)")
    if 'darkblue' in cv_content:
        cv_issues.append("CV still uses dark blue instead of LinkedIn blue")
    if not ('linkedinblue' in cv_content):
        cv_issues.append("CV missing LinkedIn blue color")
    
    # CL Checks  
    if 'COMPANY\_NAME' in cl_content or 'JOB\_TITLE' in cl_content:
        cl_issues.append("CL has unreplaced placeholders")
    if not ('Large' in cl_content and 'textbf' in cl_content):
        cl_issues.append("CL missing professional header formatting")
    if not ('textbf{' in cl_content and cl_content.count('textbf{') >= 3):
        cl_issues.append("CL missing bold section headers")
    if 'linkedinblue' not in cl_content:
        cl_issues.append("CL missing LinkedIn blue styling")
    
    print(f"   CV Issues: {cv_issues if cv_issues else '✅ None'}")
    print(f"   CL Issues: {cl_issues if cl_issues else '✅ None'}")
    
    success = len(cv_issues) == 0 and len(cl_issues) == 0
    print(f"\n🎉 Overall Success: {'✅' if success else '❌'}")
    
    if success:
        print("\n🎊 All issues fixed! CV and CL generation working perfectly!")
    else:
        print(f"\n⚠️ Issues found: {cv_issues + cl_issues}")
    
    return success

if __name__ == '__main__':
    test_emerson_workflow()