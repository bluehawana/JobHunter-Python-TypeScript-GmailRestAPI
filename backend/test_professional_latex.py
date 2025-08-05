#!/usr/bin/env python3
"""
Test the new Professional LaTeX Service with Claude API
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

from app.services.professional_latex_service import ProfessionalLaTeXService

async def test_professional_latex():
    """Test the professional LaTeX service"""
    
    print("🚀 Testing Professional LaTeX Service with Claude API")
    print("=" * 60)
    
    # Sample job for testing
    sample_job = {
        'title': 'Senior Backend Developer',
        'company': 'Volvo Energy',
        'description': 'We are looking for a Senior Backend Developer with expertise in Java, Spring Boot, microservices architecture, and cloud platforms. You will work on building scalable backend systems for our energy management solutions.',
        'keywords': ['java', 'spring boot', 'microservices', 'aws', 'postgresql', 'rest api', 'docker', 'kubernetes'],
        'location': 'Gothenburg, Sweden',
        'hiring_manager': 'Anna Andersson'
    }
    
    try:
        # Initialize the professional LaTeX service
        latex_service = ProfessionalLaTeXService()
        
        print(f"📄 Testing CV generation for {sample_job['company']} - {sample_job['title']}")
        print("🤖 Using Claude API for customization...")
        
        # Generate customized CV
        cv_pdf = await latex_service.generate_customized_cv(sample_job)
        
        if cv_pdf:
            cv_filename = f"test_cv_{sample_job['company']}_{sample_job['title'].replace(' ', '_')}.pdf"
            with open(cv_filename, 'wb') as f:
                f.write(cv_pdf)
            print(f"✅ CV generated successfully: {cv_filename} ({len(cv_pdf)} bytes)")
        else:
            print("❌ CV generation failed")
        
        print()
        print(f"📝 Testing Cover Letter generation for {sample_job['company']} - {sample_job['title']}")
        
        # Generate customized cover letter
        cl_pdf = await latex_service.generate_customized_cover_letter(sample_job)
        
        if cl_pdf:
            cl_filename = f"test_cl_{sample_job['company']}_{sample_job['title'].replace(' ', '_')}.pdf"
            with open(cl_filename, 'wb') as f:
                f.write(cl_pdf)
            print(f"✅ Cover Letter generated successfully: {cl_filename} ({len(cl_pdf)} bytes)")
        else:
            print("❌ Cover Letter generation failed")
        
        print()
        print("🎉 Professional LaTeX Service test completed!")
        
        if cv_pdf and cl_pdf:
            print("✅ Both CV and Cover Letter generated successfully")
            print("📂 Check the generated PDF files in the current directory")
            return True
        else:
            print("❌ Some documents failed to generate")
            return False
            
    except Exception as e:
        print(f"❌ Error testing professional LaTeX service: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_professional_latex())