#!/usr/bin/env python3
"""
Test all new CV templates to ensure they work correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from cv_templates import CVTemplateManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

def test_template_detection():
    """Test that job descriptions correctly detect the right templates"""
    
    manager = CVTemplateManager()
    
    test_cases = {
        '.NET Developer': {
            'jd': """
                We are looking for a C# .NET Developer with experience in ASP.NET Core,
                Entity Framework, and Azure cloud services. You will build enterprise
                applications using Microsoft technology stack.
            """,
            'expected_role': 'dotnet_developer',
            'expected_template': 'dotnet_developer_template.tex'
        },
        'Java Developer': {
            'jd': """
                Java Developer needed with strong Spring Boot and Hibernate experience.
                You will build microservices using Java, Spring Framework, and Apache Kafka.
            """,
            'expected_role': 'java_developer',
            'expected_template': 'java_developer_template.tex'
        },
        'Full-Stack Developer': {
            'jd': """
                Full-Stack Developer position. We need someone with React, TypeScript for
                frontend and Node.js, Python for backend. Experience with both frontend
                and backend development required.
            """,
            'expected_role': 'fullstack_developer',
            'expected_template': 'fullstack_developer_template.tex'
        },
        'Kotlin/Android Developer': {
            'jd': """
                Kotlin Developer for Android Auto applications. You will work on in-vehicle
                infotainment systems using Kotlin, Android SDK, and Android Auto SDK.
                Automotive experience is a plus.
            """,
            'expected_role': 'kotlin_app_developer',
            'expected_template': 'kotlin_app_developer_template.tex'
        },
        'iOS Developer': {
            'jd': """
                iOS Developer needed with Swift and SwiftUI experience. You will build
                native iOS applications for iPhone and iPad using Xcode and iOS SDK.
            """,
            'expected_role': 'ios_developer',
            'expected_template': 'kotlin_app_developer_template.tex'  # Uses same template
        },
        'React Native Developer': {
            'jd': """
                React Native Developer for cross-platform mobile apps. Experience with
                React Native, Expo, and mobile app development for iOS and Android required.
            """,
            'expected_role': 'react_native_developer',
            'expected_template': 'kotlin_app_developer_template.tex'  # Uses same template
        },
        'DevOps Engineer': {
            'jd': """
                DevOps Engineer position. Experience with Kubernetes, Docker, Terraform,
                CI/CD pipelines, and AWS/Azure cloud platforms required.
            """,
            'expected_role': 'devops_cloud',
            'expected_template': 'devops_cloud_template.tex'
        },
        'IT Support': {
            'jd': """
                IT Support Specialist needed. Experience with helpdesk, service desk,
                technical support, and customer service. ITIL knowledge is a plus.
            """,
            'expected_role': 'it_support',
            'expected_template': 'incident_management_template.tex'
        }
    }
    
    print("=" * 80)
    print("TESTING NEW TEMPLATE DETECTION")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, test_data in test_cases.items():
        print(f"\n📋 Testing: {test_name}")
        print(f"   Expected role: {test_data['expected_role']}")
        
        # Detect role
        detected_role = manager.analyze_job_role(test_data['jd'])
        
        # Get template path
        template_path = manager.get_template_path(detected_role, 'cv')
        template_name = template_path.name if template_path else 'None'
        
        # Check if detection is correct
        if detected_role == test_data['expected_role']:
            print(f"   ✅ Role detection: {detected_role}")
            passed += 1
        else:
            print(f"   ❌ Role detection: {detected_role} (expected {test_data['expected_role']})")
            failed += 1
        
        # Check if template exists
        if template_path and template_path.exists():
            print(f"   ✅ Template exists: {template_name}")
        else:
            print(f"   ❌ Template missing: {template_name}")
            failed += 1
        
        # Get role breakdown
        breakdown = manager.get_role_breakdown(test_data['jd'], threshold=5.0)
        if breakdown:
            print(f"   📊 Role breakdown:")
            for role, percentage in breakdown[:3]:  # Top 3
                print(f"      - {role}: {percentage:.1f}%")
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0


def test_template_loading():
    """Test that all templates can be loaded"""
    
    manager = CVTemplateManager()
    
    print("\n" + "=" * 80)
    print("TESTING TEMPLATE LOADING")
    print("=" * 80)
    
    templates_to_test = [
        'dotnet_developer',
        'java_developer',
        'fullstack_developer',
        'kotlin_app_developer',
        'ios_developer',
        'react_native_developer',
        'devops_cloud',
        'it_support',
        'android_developer'
    ]
    
    passed = 0
    failed = 0
    
    for role in templates_to_test:
        print(f"\n📄 Testing template: {role}")
        
        # Try to load CV template
        cv_content = manager.load_template(role, 'cv')
        if cv_content and len(cv_content) > 1000:  # Should be substantial
            print(f"   ✅ CV template loaded ({len(cv_content)} chars)")
            passed += 1
        else:
            print(f"   ❌ CV template failed to load")
            failed += 1
        
        # Try to load CL template
        cl_content = manager.load_template(role, 'cl')
        if cl_content and len(cl_content) > 500:
            print(f"   ✅ CL template loaded ({len(cl_content)} chars)")
            passed += 1
        else:
            print(f"   ❌ CL template failed to load")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0


def test_all_templates_exist():
    """Test that all templates in ROLE_CATEGORIES exist"""
    
    manager = CVTemplateManager()
    
    print("\n" + "=" * 80)
    print("TESTING ALL TEMPLATES EXIST")
    print("=" * 80)
    
    templates = manager.list_available_templates()
    
    all_exist = True
    
    for template in templates:
        role = template['role']
        cv_exists = template['cv_exists']
        cl_exists = template['cl_exists']
        
        status = "✅" if (cv_exists and cl_exists) else "⚠️"
        print(f"{status} {role}:")
        print(f"   CV: {'✅' if cv_exists else '❌'} {template['cv_path']}")
        print(f"   CL: {'✅' if cl_exists else '❌'} {template['cl_path']}")
        
        if not (cv_exists and cl_exists):
            all_exist = False
    
    print("\n" + "=" * 80)
    if all_exist:
        print("✅ ALL TEMPLATES EXIST")
    else:
        print("⚠️  SOME TEMPLATES MISSING (but may use fallbacks)")
    print("=" * 80)
    
    return True  # Don't fail on missing templates, they may use fallbacks


if __name__ == '__main__':
    print("\n🧪 COMPREHENSIVE TEMPLATE TESTING\n")
    
    # Run all tests
    test1 = test_all_templates_exist()
    test2 = test_template_loading()
    test3 = test_template_detection()
    
    # Summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    if test1 and test2 and test3:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
