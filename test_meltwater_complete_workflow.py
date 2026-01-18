#!/usr/bin/env python3
"""
Test complete workflow for Meltwater job with LinkedIn URL
This should fix the cover letter placeholder issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

from backend.app.lego_api import analyze_job_description

def test_meltwater_complete_workflow():
    """Test the complete workflow with Meltwater job"""
    
    # Meltwater job description
    meltwater_job = """
    As a Software Engineer with the information retrieval team at Meltwater you will be building 
    petabyte-scale search and analytics systems using Elasticsearch running on AWS. Every day, 
    we add 1.3B new documents into our search platform and process over 6B engagement activities 
    to provide the most complete dataset possible. This data fuels our products with robust insights 
    that span key areas that include media, social, influencer, sales, and consumer intelligence.

    In addition to working with large-scale distributed systems, you will also have the opportunity 
    to work on cutting-edge vector search technologies and explore use cases powered by Large Language 
    Models (LLMs). These initiatives enable semantic search capabilities, enhanced content understanding, 
    and more intelligent data discovery experiences for our users.

    Our culture is based on a fundamental belief in people with a passion for learning new things 
    and a desire to help those around you. We are strong believers in team autonomy, DevOps culture 
    and continuous delivery. Meltwater development teams fully own and operate their subsystems 
    and infrastructure and run on-call rotations.

    We run on AWS and are heavy users of AWS services, Elasticsearch, Cassandra, Terraform, Docker; 
    with a sprinkling of other database and messaging technologies depending on the need.

    For this role, you will benefit by having some experience with search engines, big data analytics, 
    infrastructure, systems engineering and distributed systems. Experience with vector search and 
    applied use of Large Language Models (LLMs) is also a plus. In our team you will get an opportunity 
    to explore and push the technologies we use to their limits. This sometimes requires low level 
    modifications to open-source libraries, other times it involves combining two existing technologies 
    in an innovative way.

    On the software side we're heavy on Java and Kotlin, with some Spring, RxJava and plenty of 
    microservices thrown in. We use Python for data science, machine learning and linear optimization 
    purposes. Long experience with Java or Python is however not a requirement, instead we prefer 
    an engineer with a history of rapidly acquiring new skills.

    For this position we are looking for Software Engineers that want to further grow in an organization 
    based on collaboration across team and country boundaries. With the massive production scale of 
    our systems, small decisions you make may have a big impact on our product and our many customers. 
    If you get excited when talking about distributed systems at scale, or innovating on new ways 
    to gain insights from all the world's information then you will love working with us.
    """
    
    linkedin_url = "https://www.linkedin.com/jobs/view/4357664024"
    
    print("🔍 Testing Complete Meltwater Workflow")
    print("=" * 60)
    print(f"LinkedIn URL: {linkedin_url}")
    print(f"Job Description Length: {len(meltwater_job)} characters")
    
    # Test the job analysis with LinkedIn URL
    print(f"\n📊 Running job analysis...")
    
    try:
        analysis = analyze_job_description(meltwater_job, linkedin_url)
        
        print(f"\n✅ Analysis Results:")
        print(f"  Company: '{analysis.get('company', 'NOT_FOUND')}'")
        print(f"  Title: '{analysis.get('title', 'NOT_FOUND')}'")
        print(f"  Role Category: {analysis.get('roleCategory', 'NOT_FOUND')}")
        print(f"  Role Type: {analysis.get('roleType', 'NOT_FOUND')}")
        print(f"  Confidence: {analysis.get('confidence', 0):.1%}")
        
        # Check if the cover letter issue is fixed
        company = analysis.get('company', '')
        title = analysis.get('title', '')
        
        print(f"\n🔍 Cover Letter Fix Check:")
        if company == 'Meltwater' and title == 'Software Engineer':
            print("  ✅ FIXED! Company and title extracted correctly")
            print("  ✅ Cover letter should now show:")
            print("     'Dear Hiring Manager at Meltwater'")
            print("     'Software Engineer position at Meltwater'")
            print("  ✅ No more 'You'll Bring' or '[Position]' placeholders!")
        elif company != 'Company' and title != 'Position':
            print(f"  ⚠️ PARTIAL FIX: Got '{title}' at '{company}'")
            print("  ⚠️ Better than placeholders, but not perfect extraction")
        else:
            print("  ❌ STILL BROKEN: Using generic placeholders")
            print(f"     Company: '{company}' (should be 'Meltwater')")
            print(f"     Title: '{title}' (should be 'Software Engineer')")
        
        # Check role classification
        role_category = analysis.get('roleCategory', '')
        print(f"\n🎯 Role Classification Check:")
        if role_category == 'backend_developer':
            print("  ✅ CORRECT: Classified as backend_developer")
            print("  ✅ Should use backend-focused CV template")
        else:
            print(f"  ⚠️ Got: {role_category}")
            print("  ⚠️ Expected: backend_developer (based on Java/Kotlin/Spring)")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    print("🚀 Testing Meltwater Job Complete Workflow\n")
    
    analysis = test_meltwater_complete_workflow()
    
    print(f"\n" + "=" * 60)
    if analysis:
        company = analysis.get('company', '')
        title = analysis.get('title', '')
        
        if company == 'Meltwater' and title == 'Software Engineer':
            print("🎉 SUCCESS! Cover letter issue should be FIXED!")
            print("\n✅ The system now correctly extracts:")
            print("   • Company: Meltwater")
            print("   • Title: Software Engineer")
            print("\n✅ Cover letters will no longer show:")
            print("   • 'You'll Bring' (generic placeholder)")
            print("   • '[Position]' (generic placeholder)")
            print("\n🚀 Ready to deploy to VPS!")
        else:
            print("⚠️ Partial success - extraction working but needs refinement")
    else:
        print("❌ Test failed - check error messages above")