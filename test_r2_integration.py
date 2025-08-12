#!/usr/bin/env python3
"""
Test Cloudflare R2 Integration for LaTeX Storage
This will test your R2 setup with the Opera DevOps resume
"""
import sys
import os
sys.path.append('backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

from r2_latex_storage import R2LaTeXStorage, create_resume_with_r2_overleaf

def test_r2_setup():
    """Test R2 configuration and upload"""
    
    print("🧪 TESTING CLOUDFLARE R2 INTEGRATION")
    print("=" * 60)
    
    # Check environment variables
    r2_endpoint = os.getenv('R2_ENDPOINT_URL')
    r2_public = os.getenv('R2_PUBLIC_DOMAIN')
    r2_bucket = os.getenv('R2_BUCKET_NAME')
    r2_access_key = os.getenv('R2_ACCESS_KEY_ID')
    r2_secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    print(f"📊 R2 Configuration:")
    print(f"   Endpoint: {r2_endpoint}")
    print(f"   Public Domain: {r2_public}")
    print(f"   Bucket: {r2_bucket}")
    print(f"   Access Key: {'✅ Set' if r2_access_key else '❌ Missing'}")
    print(f"   Secret Key: {'✅ Set' if r2_secret_key else '❌ Missing'}")
    
    if not all([r2_endpoint, r2_public, r2_bucket]):
        print("\n❌ R2 configuration incomplete!")
        print("💡 Please add your R2 access keys to backend/.env:")
        print("   R2_ACCESS_KEY_ID=your_access_key")
        print("   R2_SECRET_ACCESS_KEY=your_secret_key")
        return False
    
    # Test Opera DevOps job
    opera_job = {
        'title': 'DevOps Engineer',
        'company': 'Opera',
        'description': 'Kubernetes, AWS, Docker, infrastructure automation, CI/CD pipelines, monitoring'
    }
    
    print(f"\n🎭 Testing with Opera DevOps Engineer job...")
    
    # Test R2 storage
    try:
        r2_storage = R2LaTeXStorage()
        
        if not r2_storage.client:
            print("❌ R2 client initialization failed")
            print("💡 Please check your R2 access keys in backend/.env")
            return False
        
        print("✅ R2 client initialized successfully")
        
        # Generate LaTeX content
        from overleaf_pdf_generator import OverleafPDFGenerator
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(opera_job)
        
        print(f"📝 Generated LaTeX content: {len(latex_content)} characters")
        
        # Test upload to R2
        print("☁️ Uploading to R2...")
        r2_result = r2_storage.upload_latex_file(latex_content, opera_job)
        
        if r2_result:
            print("✅ R2 upload successful!")
            print(f"   📁 Filename: {r2_result['filename']}")
            print(f"   🔗 Public URL: {r2_result['public_url']}")
            print(f"   🎯 Overleaf URL: {r2_result['overleaf_url']}")
            
            # Test the complete integration
            print(f"\n🚀 Testing complete integration...")
            complete_result = create_resume_with_r2_overleaf(opera_job)
            
            if complete_result['success'] and complete_result['r2_upload_success']:
                print("🎉 COMPLETE SUCCESS!")
                print(f"   📄 PDF Size: {complete_result['pdf_size']:,} bytes")
                print(f"   📝 LaTeX Size: {complete_result['latex_size']:,} characters")
                print(f"   ☁️ R2 Upload: ✅")
                print(f"   🔗 Overleaf URL: {complete_result['overleaf_url']}")
                
                # Save PDF locally for comparison
                if complete_result['pdf_content']:
                    with open('test_r2_opera_resume.pdf', 'wb') as f:
                        f.write(complete_result['pdf_content'])
                    print(f"   💾 PDF saved: test_r2_opera_resume.pdf")
                
                return True
            else:
                print("❌ Complete integration failed")
                return False
        else:
            print("❌ R2 upload failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing R2: {e}")
        return False

def test_overleaf_url():
    """Test if the generated Overleaf URL works"""
    print(f"\n🔗 OVERLEAF URL TEST")
    print("=" * 40)
    
    # Use the public domain to create a test URL
    r2_public = os.getenv('R2_PUBLIC_DOMAIN')
    if r2_public:
        test_filename = "resume_opera_devops_engineer_test.tex"
        test_url = f"https://{r2_public}/{test_filename}"
        overleaf_url = f"https://www.overleaf.com/docs?snip_uri={test_url}"
        
        print(f"📝 Test LaTeX URL: {test_url}")
        print(f"🎯 Test Overleaf URL: {overleaf_url}")
        print(f"💡 Once you upload a file, you can test this URL in Overleaf")
    else:
        print("❌ R2_PUBLIC_DOMAIN not configured")

if __name__ == "__main__":
    print("🎯 CLOUDFLARE R2 + OVERLEAF INTEGRATION TEST")
    print("=" * 60)
    
    success = test_r2_setup()
    test_overleaf_url()
    
    if success:
        print(f"\n🎉 R2 INTEGRATION READY!")
        print(f"✅ Your job automation now has:")
        print(f"   • Perfect LaTeX PDF generation")
        print(f"   • Automatic R2 upload")
        print(f"   • Overleaf URLs for manual editing")
        print(f"   • Professional resume hosting")
        print(f"\n🚀 Ready for automated job applications!")
    else:
        print(f"\n❌ R2 SETUP INCOMPLETE")
        print(f"💡 Please add your R2 access keys to backend/.env")
        print(f"   R2_ACCESS_KEY_ID=your_access_key")
        print(f"   R2_SECRET_ACCESS_KEY=your_secret_key")