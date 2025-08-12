#!/usr/bin/env python3
"""
Check R2 + Overleaf Integration Status for Opera Application
Simple test without external dependencies
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

def check_r2_configuration():
    """Check if R2 is properly configured"""
    print("🔧 R2 CONFIGURATION CHECK")
    print("=" * 40)
    
    configs = {
        'R2_ENDPOINT_URL': os.getenv('R2_ENDPOINT_URL'),
        'R2_PUBLIC_DOMAIN': os.getenv('R2_PUBLIC_DOMAIN'), 
        'R2_BUCKET_NAME': os.getenv('R2_BUCKET_NAME'),
        'R2_ACCESS_KEY_ID': os.getenv('R2_ACCESS_KEY_ID'),
        'R2_SECRET_ACCESS_KEY': os.getenv('R2_SECRET_ACCESS_KEY')
    }
    
    print("📊 Current R2 Configuration:")
    for key, value in configs.items():
        if value:
            if 'KEY' in key:
                display = f"{value[:8]}..." if len(value) > 8 else value
            else:
                display = value
            print(f"   ✅ {key}: {display}")
        else:
            print(f"   ❌ {key}: NOT SET")
    
    missing = [k for k, v in configs.items() if not v]
    
    if missing:
        print(f"\n❌ MISSING CONFIGURATIONS:")
        for config in missing:
            print(f"   • {config}")
        print(f"\n💡 Add these to backend/.env:")
        for config in missing:
            print(f"   {config}=your_value_here")
        return False
    else:
        print(f"\n✅ ALL R2 CONFIGURATIONS PRESENT")
        return True

def test_latex_generation():
    """Test LaTeX generation for Opera"""
    print(f"\n📝 LATEX GENERATION TEST")
    print("=" * 40)
    
    try:
        from overleaf_pdf_generator import OverleafPDFGenerator
        
        opera_job = {
            'title': 'DevOps Engineer',
            'company': 'Opera',
            'description': 'Kubernetes, Docker, Prometheus, Grafana, monitoring, CI/CD, infrastructure'
        }
        
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(opera_job)
        
        print(f"✅ LaTeX generated successfully")
        print(f"   📏 Content length: {len(latex_content)} characters")
        
        # Check for key content
        checks = [
            ('DevOps Engineer', 'Role title'),
            ('Opera', 'Company name'),
            ('Prometheus', 'Monitoring tool'),
            ('Grafana', 'Dashboard tool'),
            ('ECARX', 'Current company'),
            ('Kubernetes', 'Container orchestration')
        ]
        
        print(f"\n🔍 Content verification:")
        for check, description in checks:
            if check in latex_content:
                print(f"   ✅ {description}: Found")
            else:
                print(f"   ❌ {description}: Missing")
        
        # Save LaTeX for inspection
        with open('opera_test_latex.tex', 'w') as f:
            f.write(latex_content)
        print(f"\n💾 LaTeX saved: opera_test_latex.tex")
        
        return latex_content
        
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return None

def test_r2_integration_readiness():
    """Test if R2 integration components are ready"""
    print(f"\n☁️ R2 INTEGRATION READINESS")
    print("=" * 40)
    
    try:
        # Test R2 storage import
        try:
            from r2_latex_storage import R2LaTeXStorage
            print("✅ R2LaTeXStorage module imported successfully")
            
            # Try to initialize (might fail without credentials)
            try:
                r2_storage = R2LaTeXStorage()
                if r2_storage.client:
                    print("✅ R2 client initialized successfully")
                    return True
                else:
                    print("❌ R2 client initialization failed")
                    print("💡 Check your R2 credentials in backend/.env")
                    return False
            except Exception as e:
                print(f"❌ R2 client initialization error: {e}")
                return False
                
        except ImportError as e:
            print(f"❌ R2LaTeXStorage import failed: {e}")
            print("💡 Install boto3: pip install boto3")
            return False
            
    except Exception as e:
        print(f"❌ R2 integration test failed: {e}")
        return False

def generate_expected_urls():
    """Generate expected URLs for Opera application"""
    print(f"\n🔗 EXPECTED OVERLEAF URLS")
    print("=" * 40)
    
    r2_domain = os.getenv('R2_PUBLIC_DOMAIN', 'pub-2c3ec75a299b4921821bb5ad0f311531.r2.dev')
    
    # Generate expected filenames
    import time
    timestamp = int(time.time())
    
    resume_filename = f"resume_opera_devops_engineer_{timestamp}_abc123.tex"
    cover_letter_filename = f"cover_letter_opera_devops_engineer_{timestamp}_def456.tex"
    
    resume_url = f"https://{r2_domain}/{resume_filename}"
    cover_letter_url = f"https://{r2_domain}/{cover_letter_filename}"
    
    resume_overleaf = f"https://www.overleaf.com/docs?snip_uri={resume_url}"
    cover_letter_overleaf = f"https://www.overleaf.com/docs?snip_uri={cover_letter_url}"
    
    print(f"📄 Expected Resume URLs:")
    print(f"   LaTeX: {resume_url}")
    print(f"   Overleaf: {resume_overleaf}")
    
    print(f"\n📝 Expected Cover Letter URLs:")
    print(f"   LaTeX: {cover_letter_url}")
    print(f"   Overleaf: {cover_letter_overleaf}")
    
    return {
        'resume_overleaf': resume_overleaf,
        'cover_letter_overleaf': cover_letter_overleaf
    }

def test_pdf_generation():
    """Test local PDF generation"""
    print(f"\n📄 PDF GENERATION TEST")
    print("=" * 40)
    
    try:
        from beautiful_pdf_generator import create_beautiful_multi_page_pdf
        
        opera_job = {
            'title': 'DevOps Engineer',
            'company': 'Opera',
            'description': 'Kubernetes, Docker, Prometheus, Grafana, monitoring, CI/CD'
        }
        
        pdf_content = create_beautiful_multi_page_pdf(opera_job)
        
        if pdf_content:
            pdf_size = len(pdf_content)
            print(f"✅ PDF generated successfully: {pdf_size:,} bytes")
            
            # Save PDF for inspection
            with open('opera_test_resume.pdf', 'wb') as f:
                f.write(pdf_content)
            print(f"💾 PDF saved: opera_test_resume.pdf")
            
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation test failed: {e}")
        return False

def main():
    """Run complete R2 + Overleaf status check"""
    
    print("🎭 OPERA R2 + OVERLEAF INTEGRATION STATUS CHECK")
    print("=" * 60)
    
    # Test 1: R2 Configuration
    r2_config_ok = check_r2_configuration()
    
    # Test 2: LaTeX Generation
    latex_content = test_latex_generation()
    
    # Test 3: R2 Integration Readiness
    r2_ready = test_r2_integration_readiness() if r2_config_ok else False
    
    # Test 4: Expected URLs
    expected_urls = generate_expected_urls()
    
    # Test 5: PDF Generation
    pdf_ok = test_pdf_generation()
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 INTEGRATION STATUS SUMMARY")
    print(f"=" * 60)
    
    print(f"✅ R2 Configuration: {'✅ Complete' if r2_config_ok else '❌ Incomplete'}")
    print(f"✅ LaTeX Generation: {'✅ Working' if latex_content else '❌ Failed'}")
    print(f"✅ R2 Integration: {'✅ Ready' if r2_ready else '❌ Not Ready'}")
    print(f"✅ PDF Generation: {'✅ Working' if pdf_ok else '❌ Failed'}")
    
    if r2_config_ok and latex_content and r2_ready and pdf_ok:
        print(f"\n🎉 INTEGRATION FULLY READY!")
        print(f"✅ Opera application can be generated with R2 + Overleaf")
        print(f"✅ LaTeX files will be uploaded to R2 automatically")
        print(f"✅ Overleaf URLs will be generated for manual editing")
        print(f"✅ PDFs will be compiled locally as backup")
        
        print(f"\n🔗 OVERLEAF INTEGRATION READY:")
        print(f"   📄 Resume: Will be uploaded to R2 with Overleaf URL")
        print(f"   📝 Cover Letter: Will be uploaded to R2 with Overleaf URL")
        
        print(f"\n🚀 READY TO GENERATE OPERA APPLICATION!")
        
    else:
        print(f"\n⚠️ INTEGRATION ISSUES DETECTED:")
        
        if not r2_config_ok:
            print(f"❌ R2 Configuration: Add credentials to backend/.env")
        if not latex_content:
            print(f"❌ LaTeX Generation: Check template and generator")
        if not r2_ready:
            print(f"❌ R2 Integration: Install boto3 and check credentials")
        if not pdf_ok:
            print(f"❌ PDF Generation: Check LaTeX installation")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"1. Add R2 credentials to backend/.env")
        print(f"2. Install dependencies: pip install boto3 requests")
        print(f"3. Test R2 upload manually")
        print(f"4. Verify R2 bucket public access settings")

if __name__ == "__main__":
    main()