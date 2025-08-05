#!/usr/bin/env python3
"""
Simple test for PDF generation without external dependencies
"""
import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.simple_latex_service import SimpleLaTeXService

async def test_pdf_generation():
    """Test PDF generation with a sample job"""
    print("🧪 Testing PDF generation with simplified LaTeX templates...")
    
    # Sample job data
    sample_job = {
        'title': 'Backend Developer',
        'company': 'Test Company',
        'description': 'We are looking for a backend developer with experience in Java Spring Boot and microservices architecture. Knowledge of AWS cloud platforms and Docker containerization is preferred.',
        'keywords': ['java', 'spring boot', 'microservices', 'aws', 'docker', 'postgresql'],
        'location': 'Gothenburg',
        'source': 'test'
    }
    
    try:
        # Initialize LaTeX service
        latex_service = SimpleLaTeXService()
        
        print(f"📄 Generating CV for {sample_job['company']} - {sample_job['title']}...")
        
        # Generate CV
        cv_pdf = await latex_service.generate_customized_cv(sample_job)
        
        if cv_pdf and len(cv_pdf) > 0:
            print(f"✅ CV PDF generated successfully: {len(cv_pdf)} bytes")
            
            # Save for inspection
            cv_filename = f"test_cv_{sample_job['company']}.pdf"
            with open(cv_filename, 'wb') as f:
                f.write(cv_pdf)
            print(f"💾 CV saved as: {cv_filename}")
        else:
            print("❌ CV PDF generation failed")
            return False
        
        print(f"📄 Generating Cover Letter for {sample_job['company']} - {sample_job['title']}...")
        
        # Generate Cover Letter
        cl_pdf = await latex_service.generate_customized_cover_letter(sample_job)
        
        if cl_pdf and len(cl_pdf) > 0:
            print(f"✅ Cover Letter PDF generated successfully: {len(cl_pdf)} bytes")
            
            # Save for inspection
            cl_filename = f"test_cover_letter_{sample_job['company']}.pdf"
            with open(cl_filename, 'wb') as f:
                f.write(cl_pdf)
            print(f"💾 Cover Letter saved as: {cl_filename}")
        else:
            print("❌ Cover Letter PDF generation failed")
            return False
        
        print("🎉 PDF generation test completed successfully!")
        print("📂 Check the generated PDF files to verify they can be opened properly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting PDF generation test...")
    success = asyncio.run(test_pdf_generation())
    
    if success:
        print("\n✅ All tests passed! PDF generation is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the LaTeX installation and template issues.")
        sys.exit(1)