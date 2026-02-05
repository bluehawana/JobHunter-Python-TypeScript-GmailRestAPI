#!/usr/bin/env python3
"""
Diagnostic script to identify the 500 error cause
Run this on the VPS to diagnose the issue
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking Dependencies")
    print("=" * 30)
    
    # Check Python modules
    modules = ['flask', 'pathlib', 'datetime', 'subprocess']
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - MISSING")
    
    # Check pdflatex
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ pdflatex - OK")
        else:
            print("❌ pdflatex - ERROR")
    except Exception as e:
        print(f"❌ pdflatex - MISSING: {e}")

def check_file_permissions():
    """Check file permissions"""
    print("\n📁 Checking File Permissions")
    print("=" * 35)
    
    paths_to_check = [
        '/var/www/lego-job-generator',
        '/var/www/lego-job-generator/backend',
        '/var/www/lego-job-generator/backend/latex_sources',
        '/var/www/lego-job-generator/backend/generated_applications'
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            stat = os.stat(path)
            permissions = oct(stat.st_mode)[-3:]
            print(f"✅ {path} - {permissions}")
        else:
            print(f"❌ {path} - NOT FOUND")

def check_template_files():
    """Check if template files exist and are readable"""
    print("\n📄 Checking Template Files")
    print("=" * 30)
    
    template_files = [
        '/var/www/lego-job-generator/backend/latex_sources/cv_hongzhi_li_modern.tex',
        '/var/www/lego-job-generator/backend/latex_sources/cover_letter_hongzhi_li_template.tex'
    ]
    
    for file_path in template_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read(100)  # Read first 100 chars
                print(f"✅ {os.path.basename(file_path)} - OK ({len(content)} chars)")
            except Exception as e:
                print(f"❌ {os.path.basename(file_path)} - READ ERROR: {e}")
        else:
            print(f"❌ {os.path.basename(file_path)} - NOT FOUND")

def check_output_directory():
    """Check if output directory can be created"""
    print("\n📂 Checking Output Directory")
    print("=" * 30)
    
    try:
        output_dir = Path('/var/www/lego-job-generator/backend/generated_applications')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to create a test file
        test_file = output_dir / 'test.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        
        # Clean up
        test_file.unlink()
        print("✅ Output directory - OK")
        
    except Exception as e:
        print(f"❌ Output directory - ERROR: {e}")

def test_basic_imports():
    """Test basic imports that the API uses"""
    print("\n🐍 Testing Basic Imports")
    print("=" * 25)
    
    try:
        sys.path.append('/var/www/lego-job-generator/backend')
        from cv_templates import CVTemplateManager
        print("✅ CVTemplateManager import - OK")
        
        manager = CVTemplateManager()
        print("✅ CVTemplateManager init - OK")
        
        # Test template path resolution
        path = manager.get_template_path('kamstrup', 'cv')
        if path and path.exists():
            print("✅ Template path resolution - OK")
        else:
            print(f"❌ Template path resolution - FAILED: {path}")
            
    except Exception as e:
        print(f"❌ Import test - ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all diagnostic checks"""
    print("🩺 Diagnosing 500 Internal Server Error")
    print("=" * 50)
    
    check_dependencies()
    check_file_permissions()
    check_template_files()
    check_output_directory()
    test_basic_imports()
    
    print("\n💡 Next Steps:")
    print("1. Check service logs: sudo journalctl -u lego-backend.service -f")
    print("2. Check application logs in /var/www/lego-job-generator/")
    print("3. Test API endpoint manually with curl")

if __name__ == '__main__':
    main()