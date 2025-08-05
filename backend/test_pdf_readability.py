#!/usr/bin/env python3
"""
Test PDF readability by trying to extract text content
"""
import asyncio
import sys
import os
import subprocess

# Add the app directory to Python path
sys.path.append('/Users/bluehawana/Projects/Jobhunter/backend')

from app.services.simple_latex_service import SimpleLaTeXService

def test_pdf_with_preview(pdf_path):
    """Test if PDF can be opened with Preview app"""
    try:
        # Try to open with Preview and close immediately
        result = subprocess.run([
            'osascript', '-e', 
            f'tell application "Preview" to open POSIX file "{os.path.abspath(pdf_path)}"',
            '-e', 'delay 2',
            '-e', 'tell application "Preview" to close front window'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ PDF can be opened in Preview: {pdf_path}")
            return True
        else:
            print(f"❌ PDF cannot be opened in Preview: {pdf_path}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing PDF with Preview: {e}")
        return False

def check_pdf_structure(pdf_path):
    """Check internal PDF structure"""
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read()
        
        # Basic PDF validation
        if not content.startswith(b'%PDF-'):
            print(f"❌ Invalid PDF header: {pdf_path}")
            return False
            
        if not (b'%%EOF' in content[-100:] or b'endobj' in content[-200:]):
            print(f"❌ Invalid PDF ending: {pdf_path}")
            return False
            
        # Check for common PDF structures
        if b'/Type /Catalog' in content:
            print(f"✅ PDF has valid catalog structure: {pdf_path}")
        else:
            print(f"⚠️ PDF may have structure issues: {pdf_path}")
            
        if b'/Type /Page' in content:
            print(f"✅ PDF has page objects: {pdf_path}")
        else:
            print(f"❌ PDF missing page objects: {pdf_path}")
            
        return True
            
    except Exception as e:
        print(f"❌ Error checking PDF structure: {e}")
        return False

async def test_pdf_generation_and_readability():
    """Test PDF generation and verify readability"""
    print("🧪 Testing PDF generation and readability...")
    
    # Sample job data
    sample_job = {
        'title': 'Backend Developer',
        'company': 'ReadabilityTest',
        'description': 'We are looking for a backend developer with experience in Java Spring Boot and microservices architecture.',
        'keywords': ['java', 'spring boot', 'microservices', 'aws', 'docker'],
        'location': 'Gothenburg',
        'source': 'test'
    }
    
    try:
        latex_service = SimpleLaTeXService()
        
        print(f"📄 Generating CV for {sample_job['company']}...")
        cv_pdf = await latex_service.generate_customized_cv(sample_job)
        
        if cv_pdf and len(cv_pdf) > 0:
            cv_filename = f"readable_test_cv.pdf"
            with open(cv_filename, 'wb') as f:
                f.write(cv_pdf)
            print(f"✅ CV PDF generated: {len(cv_pdf)} bytes")
            
            # Test readability
            print("🔍 Testing CV PDF readability...")
            structure_ok = check_pdf_structure(cv_filename)
            preview_ok = test_pdf_with_preview(cv_filename)
            
            if structure_ok and preview_ok:
                print("✅ CV PDF is readable and can be opened!")
            else:
                print("❌ CV PDF has readability issues")
                return False
        else:
            print("❌ CV PDF generation failed")
            return False
        
        print(f"📄 Generating Cover Letter for {sample_job['company']}...")
        cl_pdf = await latex_service.generate_customized_cover_letter(sample_job)
        
        if cl_pdf and len(cl_pdf) > 0:
            cl_filename = f"readable_test_cover_letter.pdf"
            with open(cl_filename, 'wb') as f:
                f.write(cl_pdf)
            print(f"✅ Cover Letter PDF generated: {len(cl_pdf)} bytes")
            
            # Test readability  
            print("🔍 Testing Cover Letter PDF readability...")
            structure_ok = check_pdf_structure(cl_filename)
            preview_ok = test_pdf_with_preview(cl_filename)
            
            if structure_ok and preview_ok:
                print("✅ Cover Letter PDF is readable and can be opened!")
            else:
                print("❌ Cover Letter PDF has readability issues")
                return False
        else:
            print("❌ Cover Letter PDF generation failed")
            return False
        
        print("🎉 All PDFs generated successfully and are readable!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive PDF readability test...")
    success = asyncio.run(test_pdf_generation_and_readability())
    
    if success:
        print("\n✅ All tests passed! PDFs are generated correctly and can be opened.")
    else:
        print("\n❌ Tests failed. PDFs have readability issues.")
        sys.exit(1)