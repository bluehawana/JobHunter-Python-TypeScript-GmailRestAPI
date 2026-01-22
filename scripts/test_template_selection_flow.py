#!/usr/bin/env python3
"""
Test to verify the complete template selection flow:
Job Analysis → Role Detection → Template Selection → LaTeX Loading
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import analyze_job_description, build_lego_cv, build_lego_cover_letter
from cv_templates import CVTemplateManager

def test_template_selection_flow():
    """Test that job analysis correctly selects the closest matching LaTeX templates"""
    
    print("=" * 80)
    print("TESTING TEMPLATE SELECTION FLOW")
    print("=" * 80)
    
    test_cases = [
        {
            'name': 'IT Business Analyst',
            'description': """
            We are looking for an IT Business Analyst to bridge business and technology.
            You will gather requirements, facilitate workshops, and work with stakeholders.
            Experience with Power BI, Visio, and business process improvement required.
            """,
            'expected_role': 'it_business_analyst',
            'expected_template': 'incluso_it_business_analyst'
        },
        {
            'name': 'Android Developer',
            'description': """
            Android Developer needed for mobile app development.
            Strong Kotlin and Android SDK experience required.
            You will build native Android applications using Jetpack components.
            """,
            'expected_role': 'android_developer',
            'expected_template': 'ecarx_android_developer'
        },
        {
            'name': 'DevOps Cloud Engineer',
            'description': """
            DevOps Engineer to manage our cloud infrastructure.
            Experience with Kubernetes, Docker, Terraform, and CI/CD pipelines.
            AWS and Azure knowledge required.
            """,
            'expected_role': 'devops_cloud',
            'expected_template': 'alten_cloud'
        },
        {
            'name': 'Fullstack Developer',
            'description': """
            Fullstack Developer for web application development.
            React, TypeScript, Node.js, and modern JavaScript frameworks.
            You will work on both frontend and backend systems.
            """,
            'expected_role': 'fullstack_developer',
            'expected_template': 'ahlsell_fullstack'
        },
        {
            'name': 'Backend Java Developer',
            'description': """
            Backend Developer with strong Java and Spring Boot experience.
            You will build microservices and RESTful APIs.
            Experience with distributed systems and databases required.
            """,
            'expected_role': 'backend_developer',
            'expected_template': 'eworks_java'
        },
        {
            'name': 'Incident Management / SRE',
            'description': """
            SRE Engineer for incident management and production support.
            24/7 on-call rotation, monitoring with Prometheus and Grafana.
            Focus on MTTR reduction and system reliability.
            """,
            'expected_role': 'incident_management_sre',
            'expected_template': 'tata_incident_management'
        }
    ]
    
    template_manager = CVTemplateManager()
    results = []
    
    for test_case in test_cases:
        print(f"\n{'=' * 80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'=' * 80}")
        
        # Step 1: Analyze job description
        analysis = analyze_job_description(test_case['description'])
        detected_role = analysis.get('roleCategory')
        
        print(f"\n1️⃣ Job Analysis:")
        print(f"   Expected Role: {test_case['expected_role']}")
        print(f"   Detected Role: {detected_role}")
        print(f"   Match: {'✅' if detected_role == test_case['expected_role'] else '❌'}")
        
        # Step 2: Get template path
        cv_template_path = template_manager.get_template_path(detected_role, 'cv')
        cl_template_path = template_manager.get_template_path(detected_role, 'cl')
        
        print(f"\n2️⃣ Template Selection:")
        print(f"   CV Template: {cv_template_path.name if cv_template_path else 'NOT FOUND'}")
        print(f"   CL Template: {cl_template_path.name if cl_template_path else 'NOT FOUND'}")
        
        # Step 3: Verify template contains expected content
        if cv_template_path and cv_template_path.exists():
            template_dir = cv_template_path.parent.name
            expected_in_path = test_case['expected_template']
            path_match = expected_in_path in str(cv_template_path).lower()
            print(f"   Template Directory: {template_dir}")
            print(f"   Expected in Path: {expected_in_path}")
            print(f"   Path Match: {'✅' if path_match else '❌'}")
        else:
            print(f"   ❌ Template file not found!")
            path_match = False
        
        # Step 4: Load template content
        cv_content = template_manager.load_template(detected_role, 'cv')
        cl_content = template_manager.load_template(detected_role, 'cl')
        
        print(f"\n3️⃣ Template Loading:")
        print(f"   CV Loaded: {'✅' if cv_content else '❌'} ({len(cv_content) if cv_content else 0} chars)")
        print(f"   CL Loaded: {'✅' if cl_content else '❌'} ({len(cl_content) if cl_content else 0} chars)")
        
        # Overall result
        success = (
            detected_role == test_case['expected_role'] and
            cv_template_path is not None and
            cl_template_path is not None and
            path_match and
            cv_content is not None and
            cl_content is not None
        )
        
        results.append({
            'name': test_case['name'],
            'success': success,
            'role_match': detected_role == test_case['expected_role'],
            'template_found': cv_template_path is not None,
            'content_loaded': cv_content is not None
        })
        
        print(f"\n{'✅ PASS' if success else '❌ FAIL'}")
    
    # Summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    print(f"\nDetailed Results:")
    for result in results:
        status = '✅' if result['success'] else '❌'
        print(f"  {status} {result['name']}")
        if not result['success']:
            if not result['role_match']:
                print(f"      - Role detection failed")
            if not result['template_found']:
                print(f"      - Template not found")
            if not result['content_loaded']:
                print(f"      - Content loading failed")
    
    print(f"\n{'=' * 80}")
    if passed == total:
        print("🎉 ALL TESTS PASSED! Template selection flow working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Review the issues above.")
    print(f"{'=' * 80}")
    
    return passed == total

if __name__ == '__main__':
    success = test_template_selection_flow()
    sys.exit(0 if success else 1)
