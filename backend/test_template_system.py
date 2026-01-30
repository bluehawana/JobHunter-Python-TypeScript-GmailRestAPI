#!/usr/bin/env python3
"""
Test the template-based LEGO system
"""

from cv_templates import CVTemplateManager

def test_android_job():
    """Test with Android Platform Developer job"""
    
    manager = CVTemplateManager()
    
    # Android job description
    android_jd = """
    Android Platform Developer
    
    We are looking for an Android Platform Developer to work on automotive infotainment systems.
    You will work with Kotlin, Java, and AOSP to build cutting-edge mobile experiences.
    
    Requirements:
    - Strong experience with Android SDK and Android Studio
    - Proficiency in Kotlin and Java
    - Experience with AOSP (Android Open Source Project)
    - Knowledge of automotive infotainment systems
    - Experience with Android Auto
    """
    
    print("=" * 80)
    print("Testing Android Job Detection")
    print("=" * 80)
    
    # Analyze role
    role_category = manager.analyze_job_role(android_jd)
    print(f"\n✓ Detected role category: {role_category}")
    
    # Get role info
    role_info = manager.get_role_info(role_category)
    print(f"✓ Role display name: {role_info.get('display_name')}")
    print(f"✓ Keywords: {', '.join(role_info.get('keywords', []))}")
    
    # Get template path
    template_path = manager.get_template_path(role_category)
    print(f"✓ Template path: {template_path}")
    print(f"✓ Template exists: {template_path.exists() if template_path else False}")
    
    # Load template
    template_content = manager.load_template(role_category)
    if template_content:
        print(f"✓ Template loaded successfully ({len(template_content)} characters)")
        print(f"✓ First 200 characters:\n{template_content[:200]}...")
    else:
        print("✗ Failed to load template")
    
    print("\n" + "=" * 80)


def test_devops_job():
    """Test with DevOps job"""
    
    manager = CVTemplateManager()
    
    devops_jd = """
    DevOps Engineer - Cloud Infrastructure
    
    We're looking for a DevOps Engineer to manage our AWS infrastructure.
    
    Requirements:
    - AWS, Azure, or GCP experience
    - Kubernetes and Docker
    - Terraform and Infrastructure as Code
    - CI/CD pipelines (Jenkins, GitHub Actions)
    - Python and Bash scripting
    """
    
    print("=" * 80)
    print("Testing DevOps Job Detection")
    print("=" * 80)
    
    role_category = manager.analyze_job_role(devops_jd)
    print(f"\n✓ Detected role category: {role_category}")
    
    role_info = manager.get_role_info(role_category)
    print(f"✓ Role display name: {role_info.get('display_name')}")
    
    template_path = manager.get_template_path(role_category)
    print(f"✓ Template path: {template_path}")
    print(f"✓ Template exists: {template_path.exists() if template_path else False}")
    
    print("\n" + "=" * 80)


def test_all_templates():
    """List all available templates"""
    
    manager = CVTemplateManager()
    
    print("=" * 80)
    print("All Available Templates")
    print("=" * 80)
    
    templates = manager.list_available_templates()
    
    for template in templates:
        status = "✓" if template['template_exists'] else "✗"
        print(f"\n{status} {template['display_name']}")
        print(f"   Role: {template['role']}")
        print(f"   Path: {template['template_path']}")
        print(f"   Keywords: {', '.join(template['keywords'][:5])}...")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    test_android_job()
    print("\n")
    test_devops_job()
    print("\n")
    test_all_templates()
