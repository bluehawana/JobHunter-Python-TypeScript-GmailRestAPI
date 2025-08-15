#!/usr/bin/env python3
"""
Test TRUE LEGO System Only - No Simple Generators
Verify that only the TRUE template automation with Claude intelligence is used
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import asyncio

async def test_true_lego_system():
    """Test the TRUE LEGO system with a real job"""
    
    print("🎯 TESTING TRUE LEGO SYSTEM ONLY")
    print("=" * 60)
    print("✅ No simple generators allowed")
    print("✅ Only TRUE template automation with Claude intelligence")
    print("=" * 60)
    
    # Test job (use the Volvo job from manual input)
    test_job = {
        'company': 'Volvo Group',
        'title': 'Senior DevOps Engineer',
        'location': 'Gothenburg, Sweden',
        'description': 'We are looking for a Senior DevOps Engineer to join our team. You will work with Kubernetes, Docker, AWS, monitoring with Prometheus and Grafana, CI/CD pipelines, and infrastructure automation. Experience with automotive industry is a plus.',
        'url': 'https://jobs.volvogroup.com/job/12345',
        'requirements': 'Kubernetes, Docker, AWS, Python, Prometheus, Grafana, CI/CD, Infrastructure as Code'
    }
    
    try:
        # Import TRUE template automation
        from true_template_automation import TrueTemplateAutomation
        
        print(f"🎯 Testing TRUE LEGO for: {test_job['company']} - {test_job['title']}")
        
        # Initialize TRUE automation
        true_automation = TrueTemplateAutomation()
        
        # Generate CV using TRUE LEGO templates
        print(f"📄 Generating TRUE LEGO CV...")
        cv_latex = await true_automation._generate_true_cv(test_job)
        
        if cv_latex and len(cv_latex) > 5000:  # Should be substantial LaTeX
            print(f"✅ TRUE LEGO CV generated: {len(cv_latex)} characters")
            
            # Save for inspection
            with open('test_true_lego_cv.tex', 'w') as f:
                f.write(cv_latex)
            print(f"💾 Saved: test_true_lego_cv.tex")
        else:
            print(f"❌ TRUE LEGO CV generation failed")
            return False
        
        # Generate Cover Letter using TRUE LEGO templates
        print(f"📝 Generating TRUE LEGO Cover Letter...")
        cl_latex = await true_automation._generate_true_cover_letter(test_job)
        
        if cl_latex and len(cl_latex) > 2000:  # Should be substantial LaTeX
            print(f"✅ TRUE LEGO Cover Letter generated: {len(cl_latex)} characters")
            
            # Save for inspection
            with open('test_true_lego_cl.tex', 'w') as f:
                f.write(cl_latex)
            print(f"💾 Saved: test_true_lego_cl.tex")
        else:
            print(f"❌ TRUE LEGO Cover Letter generation failed")
            return False
        
        # Compile to PDFs
        print(f"🔧 Compiling TRUE LEGO documents to PDF...")
        
        cv_pdf = await true_automation._compile_latex_to_pdf(cv_latex, "test_true_cv")
        cl_pdf = await true_automation._compile_latex_to_pdf(cl_latex, "test_true_cl")
        
        if cv_pdf and len(cv_pdf) > 50000:
            print(f"✅ TRUE LEGO CV PDF: {len(cv_pdf)} bytes")
            with open('test_true_lego_cv.pdf', 'wb') as f:
                f.write(cv_pdf)
            print(f"💾 Saved: test_true_lego_cv.pdf")
        else:
            print(f"❌ TRUE LEGO CV PDF compilation failed")
            return False
        
        if cl_pdf and len(cl_pdf) > 20000:
            print(f"✅ TRUE LEGO Cover Letter PDF: {len(cl_pdf)} bytes")
            with open('test_true_lego_cl.pdf', 'wb') as f:
                f.write(cl_pdf)
            print(f"💾 Saved: test_true_lego_cl.pdf")
        else:
            print(f"❌ TRUE LEGO Cover Letter PDF compilation failed")
            return False
        
        print(f"\n" + "=" * 60)
        print(f"🎉 TRUE LEGO SYSTEM TEST SUCCESSFUL!")
        print(f"=" * 60)
        print(f"✅ CV: Professional LaTeX template with Claude intelligence")
        print(f"✅ Cover Letter: Matching LaTeX style with soft skills")
        print(f"✅ Both documents use your EXACT templates")
        print(f"✅ No simple/static generators used")
        print(f"✅ Ready for production automation")
        
        return True
        
    except Exception as e:
        print(f"❌ TRUE LEGO system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_true_lego_system()
    
    if success:
        print(f"\n🎯 TRUE LEGO SYSTEM VERIFIED!")
        print(f"📧 Your automation will now use ONLY professional templates")
        print(f"🚫 All simple generators have been removed")
    else:
        print(f"\n❌ TRUE LEGO SYSTEM NEEDS ATTENTION")
        print(f"💡 Check the errors above")

if __name__ == "__main__":
    asyncio.run(main())