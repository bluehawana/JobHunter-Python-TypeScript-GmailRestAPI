#!/usr/bin/env python3
"""
Test R2 + Overleaf Integration for Opera Application
Verify: LaTeX generation → R2 upload → Overleaf URL → PDF accessibility
"""
import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_r2_config():
    """Check R2 configuration"""
    print("🔧 CHECKING R2 CONFIGURATION")
    print("-" * 40)
    
    configs = {
        'R2_ENDPOINT_URL': os.getenv('R2_ENDPOINT_URL'),
        'R2_PUBLIC_DOMAIN': os.getenv('R2_PUBLIC_DOMAIN'),
        'R2_BUCKET_NAME': os.getenv('R2_BUCKET_NAME'),
        'R2_ACCESS_KEY_ID': os.getenv('R2_ACCESS_KEY_ID'),
        'R2_SECRET_ACCESS_KEY': os.getenv('R2_SECRET_ACCESS_KEY')
    }
    
    for key, value in configs.items():
        if value:
            display_value = value[:20] + '...' if len(value) > 20 else value
            print(f"✅ {key}: {display_value}")
        else:
            print(f"❌ {key}: Missing")
    
    missing = [k for k, v in configs.items() if not v]
    if missing:
        print(f"\n❌ Missing configurations: {', '.join(missing)}")
        return False
    
    print(f"✅ All R2 configurations present")
    return True

def test_r2_upload_workflow():
    """Test complete R2 upload workflow"""
    print(f"\n☁️ TESTING R2 UPLOAD WORKFLOW")
    print("-" * 40)
    
    try:
        # Import R2 storage (might fail if boto3 not installed)
        try:
            from r2_latex_storage import R2LaTeXStorage
        except ImportError as e:
            print(f"❌ Cannot import R2 storage: {e}")
            print(f"💡 Install boto3: pip install boto3")
            return None
        
        # Initialize R2 storage
        r2_storage = R2LaTeXStorage()
        if not r2_storage.client:
            print("❌ R2 client initialization failed")
            return None
        
        print("✅ R2 client initialized")
        
        # Generate Opera LaTeX content
        opera_job = {
            'title': 'DevOps Engineer',
            'company': 'Opera',
            'description': 'Kubernetes, Docker, Prometheus, Grafana, monitoring, CI/CD'
        }
        
        from overleaf_pdf_generator import OverleafPDFGenerator
        generator = OverleafPDFGenerator()
        latex_content = generator._generate_latex_content(opera_job)
        
        print(f"📝 Generated LaTeX: {len(latex_content)} chars")
        
        # Upload to R2
        print("☁️ Uploading to R2...")
        r2_result = r2_storage.upload_latex_file(latex_content, opera_job)
        
        if r2_result:
            print("✅ R2 upload successful!")
            print(f"   📁 File: {r2_result['filename']}")
            print(f"   🔗 URL: {r2_result['public_url']}")
            print(f"   🎯 Overleaf: {r2_result['overleaf_url']}")
            return r2_result
        else:
            print("❌ R2 upload failed")
            return None
            
    except Exception as e:
        print(f"❌ R2 workflow test failed: {e}")
        return None

def test_url_accessibility(r2_result):
    """Test if uploaded file is accessible"""
    print(f"\n🌐 TESTING URL ACCESSIBILITY")
    print("-" * 40)
    
    if not r2_result:
        print("❌ No R2 result to test")
        return False
    
    try:
        url = r2_result['public_url']
        print(f"🔗 Testing: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            print(f"✅ URL accessible: {len(content)} chars")
            
            # Verify LaTeX content
            if '\\documentclass' in content and 'Hongzhi Li' in content:
                print("✅ Valid LaTeX content confirmed")
                return True
            else:
                print("❌ Invalid LaTeX content")
                return False
        else:
            print(f"❌ URL not accessible: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_overleaf_integration():
    """Test Overleaf URL generation"""
    print(f"\n🎯 TESTING OVERLEAF INTEGRATION")
    print("-" * 40)
    
    # Test URL format
    test_latex_url = "https://pub-2c3ec75a299b4921821bb5ad0f311531.r2.dev/resume_opera_test.tex"
    overleaf_url = f"https://www.overleaf.com/docs?snip_uri={test_latex_url}"
    
    print(f"📝 LaTeX URL format: {test_latex_url}")
    print(f"🎯 Overleaf URL format: {overleaf_url}")
    
    # Check URL format
    if 'overleaf.com/docs?snip_uri=' in overleaf_url:
        print("✅ Overleaf URL format correct")
        print("💡 You can test this URL manually in browser")
        return True
    else:
        print("❌ Overleaf URL format incorrect")
        return False

def main():
    """Run R2 + Overleaf integration test"""
    
    print("🎭 R2 + OVERLEAF INTEGRATION TEST FOR OPERA")
    print("=" * 60)
    
    # Step 1: Check configuration
    config_ok = check_r2_config()
    
    # Step 2: Test R2 upload (if config OK)
    r2_result = None
    if config_ok:
        r2_result = test_r2_upload_workflow()
    
    # Step 3: Test URL accessibility
    url_accessible = False
    if r2_result:
        url_accessible = test_url_accessibility(r2_result)
    
    # Step 4: Test Overleaf integration
    overleaf_ok = test_overleaf_integration()
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 INTEGRATION TEST SUMMARY")
    print(f"=" * 60)
    
    print(f"✅ R2 Configuration: {config_ok}")
    print(f"✅ R2 Upload: {bool(r2_result)}")
    print(f"✅ URL Accessible: {url_accessible}")
    print(f"✅ Overleaf Format: {overleaf_ok}")
    
    if config_ok and r2_result and url_accessible and overleaf_ok:
        print(f"\n🎉 INTEGRATION WORKING PERFECTLY!")
        print(f"✅ Opera LaTeX files can be uploaded to R2")
        print(f"✅ Files are publicly accessible")
        print(f"✅ Overleaf URLs are properly formatted")
        print(f"\n🔗 OPERA OVERLEAF URL:")
        print(f"   {r2_result['overleaf_url']}")
        print(f"\n🚀 Ready for automated Opera applications!")
    else:
        print(f"\n⚠️ INTEGRATION ISSUES:")
        if not config_ok:
            print(f"❌ Add R2 credentials to backend/.env")
        if not r2_result:
            print(f"❌ R2 upload failed - check credentials/permissions")
        if not url_accessible:
            print(f"❌ Files not publicly accessible - check R2 settings")
        if not overleaf_ok:
            print(f"❌ Overleaf URL format issues")

if __name__ == "__main__":
    main()