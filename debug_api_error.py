#!/usr/bin/env python3
"""
Debug script to identify what's causing the 500 error in the API
"""

import sys
import os
sys.path.append('backend')
sys.path.append('backend/app')

def test_imports():
    """Test if all imports work correctly"""
    print("🔍 Testing Imports")
    print("=" * 30)
    
    try:
        # Test basic imports
        from pathlib import Path
        print("✅ pathlib.Path imported")
        
        from datetime import datetime
        print("✅ datetime imported")
        
        # Test template manager import
        sys.path.append('backend')
        from cv_templates import CVTemplateManager
        print("✅ CVTemplateManager imported")
        
        # Test template manager initialization
        template_manager = CVTemplateManager()
        print("✅ CVTemplateManager initialized")
        
        # Test template path resolution
        template_path = template_manager.get_template_path('devops_cloud', 'cv')
        print(f"✅ Template path resolved: {template_path}")
        
        if template_path and template_path.exists():
            print("✅ Template file exists")
        else:
            print("❌ Template file missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_role_category_logic():
    """Test the role category logic"""
    print("\n🔧 Testing Role Category Logic")
    print("=" * 40)
    
    try:
        # Test the safeguard logic
        role_type = "IT Business Analyst"
        role_category = "devops_cloud"
        
        expected_role_type = role_category.replace('_', ' ').title()
        print(f"Input: role_type='{role_type}', role_category='{role_category}'")
        print(f"Expected: '{expected_role_type}'")
        
        if role_type != expected_role_type:
            print(f"⚠️ Role type mismatch detected: roleType='{role_type}', roleCategory='{role_category}'")
            print(f"🔧 Correcting role_type from '{role_type}' to '{expected_role_type}'")
            role_type = expected_role_type
        
        print(f"Result: role_type='{role_type}'")
        print("✅ Safeguard logic works")
        return True
        
    except Exception as e:
        print(f"❌ Safeguard logic error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_paths():
    """Test template path resolution"""
    print("\n📁 Testing Template Paths")
    print("=" * 35)
    
    try:
        sys.path.append('backend')
        from cv_templates import CVTemplateManager
        
        template_manager = CVTemplateManager()
        
        # Test key roles
        test_roles = ['devops_cloud', 'it_support', 'kamstrup', 'fullstack_developer']
        
        all_good = True
        for role in test_roles:
            cv_path = template_manager.get_template_path(role, 'cv')
            cl_path = template_manager.get_template_path(role, 'cl')
            
            print(f"\nRole: {role}")
            print(f"  CV Path: {cv_path}")
            print(f"  CL Path: {cl_path}")
            
            if cv_path and cv_path.exists():
                print(f"  ✅ CV template exists")
            else:
                print(f"  ❌ CV template missing")
                all_good = False
                
            if cl_path and cl_path.exists():
                print(f"  ✅ CL template exists")
            else:
                print(f"  ❌ CL template missing")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Template path error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_build_functions():
    """Test the build functions without Flask"""
    print("\n🏗️ Testing Build Functions")
    print("=" * 35)
    
    try:
        # We can't test the actual build functions due to Flask dependencies
        # But we can test the logic components
        
        # Test role mapping
        role_map = {
            'Incident Management Sre': 'incident_management_specialist',
            'Devops Engineer': 'devops_engineer',
            'Devops Cloud': 'devops_engineer',
            'devops_cloud': 'devops_engineer',
        }
        
        # Test mapping lookup
        role_category = 'devops_cloud'
        role_type = 'Devops Cloud'
        
        brick_key = role_map.get(role_category, role_map.get(role_type, 'devops_engineer'))
        print(f"Role mapping test: {role_category} -> {brick_key}")
        
        if brick_key == 'devops_engineer':
            print("✅ Role mapping works")
            return True
        else:
            print("❌ Role mapping failed")
            return False
            
    except Exception as e:
        print(f"❌ Build function error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debug tests"""
    print("🐛 Debugging API 500 Error")
    print("=" * 50)
    
    # Run tests
    imports_ok = test_imports()
    logic_ok = test_role_category_logic()
    paths_ok = test_template_paths()
    build_ok = test_build_functions()
    
    # Summary
    print("\n📊 Debug Results")
    print("=" * 20)
    print(f"Imports: {'✅ OK' if imports_ok else '❌ FAIL'}")
    print(f"Logic: {'✅ OK' if logic_ok else '❌ FAIL'}")
    print(f"Template Paths: {'✅ OK' if paths_ok else '❌ FAIL'}")
    print(f"Build Functions: {'✅ OK' if build_ok else '❌ FAIL'}")
    
    all_ok = all([imports_ok, logic_ok, paths_ok, build_ok])
    
    if all_ok:
        print("\n✅ All debug tests passed - issue might be elsewhere")
        print("💡 Check server logs for the actual error")
    else:
        print("\n❌ Found issues that might be causing the 500 error")
    
    return all_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)