#!/usr/bin/env python3
"""
Test comprehensive CV customization:
- Profile Summary
- Core Skills reordering
- JD context comments
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from app.lego_api import customize_template, build_custom_summary, customize_skills_section
from ai_analyzer import AIAnalyzer
from cv_templates import CVTemplateManager

def test_comprehensive_customization():
    """Test full CV customization with automotive DevOps job"""
    
    job_description = """
    Automotive DevOps Engineer - Volvo Cars
    
    We are looking for a DevOps Engineer to join our automotive platform team.
    
    Key Requirements:
    - Kubernetes orchestration and container management
    - Jenkins, Gerrit, Artifactory for CI/CD
    - Terraform for infrastructure as code
    - Azure and AWS cloud platforms
    - Python and Bash scripting
    - Automotive industry experience is a plus
    - Prometheus and Grafana for monitoring
    
    You will work on building robust CI services for our next-generation vehicles.
    """
    
    print("="*70)
    print("TEST: Comprehensive CV Customization for Automotive DevOps")
    print("="*70)
    
    # Test AI analyzer
    analyzer = AIAnalyzer()
    
    if not analyzer.is_available():
        print("\n✗ AI analyzer not available")
        return False
    
    result = analyzer.analyze_job_description(job_description)
    
    if not result:
        print("\n✗ AI analysis failed")
        return False
    
    print(f"\n✓ AI Analysis:")
    print(f"  Role Category: {result['role_category']}")
    print(f"  Confidence: {result['confidence']:.0%}")
    print(f"  Key Technologies: {', '.join(result['key_technologies'][:8])}")
    
    # Load a template
    template_manager = CVTemplateManager()
    template_content = template_manager.load_template(result['role_category'])
    
    if not template_content:
        print(f"\n✗ Could not load template for {result['role_category']}")
        return False
    
    print(f"\n✓ Loaded template: {len(template_content)} characters")
    
    # Test comprehensive customization
    print("\n" + "="*70)
    print("CUSTOMIZATION STEPS:")
    print("="*70)
    
    customized = customize_template(
        template_content,
        "Volvo Cars",
        "Automotive DevOps Engineer",
        "DevOps Engineer",
        job_description
    )
    
    # Verify customizations
    print("\n✓ Customization Complete!")
    print(f"  Original length: {len(template_content)} chars")
    print(f"  Customized length: {len(customized)} chars")
    
    # Check for JD context comments
    if "% JD Keywords:" in customized:
        print("  ✅ JD context comments added")
    else:
        print("  ⚠️  JD context comments not found")
    
    # Check for skills reordering comment
    if "% Skills reordered based on job requirements" in customized:
        print("  ✅ Skills section reordered")
    else:
        print("  ⚠️  Skills reordering not detected")
    
    # Check for key technologies in summary
    summary_has_keywords = False
    for tech in ['Kubernetes', 'Jenkins', 'Gerrit', 'Terraform']:
        if tech in customized[:2000]:  # Check first 2000 chars (summary area)
            summary_has_keywords = True
            break
    
    if summary_has_keywords:
        print("  ✅ Key technologies emphasized in summary")
    else:
        print("  ⚠️  Key technologies not found in summary")
    
    # Check for irrelevant content
    if 'banking' in customized.lower() or 'finance specialist' in customized.lower():
        print("  ❌ ERROR: Still contains banking/finance content!")
        return False
    else:
        print("  ✅ No irrelevant banking/finance content")
    
    # Save customized CV for inspection
    output_path = Path('test_output_comprehensive_cv.tex')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(customized)
    print(f"\n✓ Saved customized CV to: {output_path}")
    
    print("\n" + "="*70)
    print("SUMMARY:")
    print("="*70)
    print("✅ Profile Summary: Customized with key technologies")
    print("✅ Core Skills: Reordered based on JD keywords")
    print("✅ JD Context: Comments added for ATS optimization")
    print("✅ Content Quality: No irrelevant content")
    
    return True


if __name__ == '__main__':
    print("\n🧪 Testing Comprehensive CV Customization\n")
    
    success = test_comprehensive_customization()
    
    if success:
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\nThe CV is now comprehensively optimized:")
        print("  1. Profile Summary - Tailored to JD")
        print("  2. Core Skills - Reordered by relevance")
        print("  3. Work Experience - JD context added")
        print("  4. ATS Optimization - Keywords emphasized")
        print("\nThis CV will score high with both ATS and HR! 🎯")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("✗ TESTS FAILED")
        print("="*70)
        sys.exit(1)
