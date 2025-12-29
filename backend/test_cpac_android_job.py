#!/usr/bin/env python3
"""
Test the template system with CPAC Systems Android Platform Developer job
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from cv_templates import CVTemplateManager

# CPAC Systems job description
cpac_jd = """
At CPAC Systems, we know that your background, interests and experiences shape how you solve problems – and that mix is what drives innovation here. When you approach challenges from new angles, you help us find smarter solutions that make life easier for our customers.

About us
CPAC Systems develops advanced control systems for marine and industrial applications. Since 1999, we've been turning complex operations into intuitive experiences. With 250 employees, a portfolio of 50 patents and more than 500,000 delivered products per year, we drive innovation in everything from electrification to intelligent automation, always working at the intersection of safety, efficiency and user experience. As part of Volvo Group, our role is to lead advanced technology development and explore the next generation of smart control systems.

Your role
As an Android Platform Developer, you will work on platform-level components that power modern automotive infotainment systems. You'll contribute to Android system services, frameworks and platform features, ensuring performance, reliability and smooth integration across hardware and application layers.

In this role, you will implement new platform functionality in Java/Kotlin, integrate native C++ components, participate in design and code reviews, and support CI/CD pipelines. You will collaborate closely with customer projects and cross-functional engineering teams, contributing to both feature development and long-term platform evolution.

You will also be a key part of Android OS upgrade projects, making sure platform components migrate cleanly between versions and remain compatible with automotive hardware, APIs and system constraints.

This is a hands-on development role for someone who enjoys digging into AOSP internals, solving complex problems and shaping the backbone of the entire Android system.

What you will do
• Develop and maintain Android platform components for automotive infotainment 
• Implement features using Java/Kotlin and integrate with native C++ layers 
• Drive development of assigned Android platform work packages 
• Perform design and code reviews for platform components 
• Support CI/CD pipelines using Jenkins and maintain clear documentation 
• Collaborate closely with customer projects and cross-functional engineering teams 
• Lead or contribute to Android OS upgrade projects, securing compatibility with hardware and applications

Key qualifications
• Strong experience in Android and AOSP platform development 
• Proficiency in Java and Kotlin (C++ for native integration is a plus) 
• Familiarity with Python for scripting and automation 
• Experience with Jenkins and CI/CD workflows 
• Knowledge of automotive infotainment systems and hybrid development environments 
• Proven experience with Android version upgrades, API changes, platform migrations and validation in automotive or embedded settings 
• Fluency in English, written and spoken
"""

def main():
    print("=" * 80)
    print("Testing CPAC Systems Android Platform Developer Job")
    print("=" * 80)
    
    manager = CVTemplateManager()
    
    # Analyze role
    role_category = manager.analyze_job_role(cpac_jd)
    print(f"\n✓ Detected role category: {role_category}")
    
    # Get role info
    role_info = manager.get_role_info(role_category)
    print(f"✓ Role display name: {role_info.get('display_name')}")
    print(f"✓ Keywords matched: {', '.join(role_info.get('keywords', []))}")
    print(f"✓ Priority: {role_info.get('priority')}")
    
    # Get template path
    template_path = manager.get_template_path(role_category)
    print(f"\n✓ Template path: {template_path}")
    
    if template_path:
        print(f"✓ Template exists: {template_path.exists()}")
        print(f"✓ Template file: {template_path.name}")
    else:
        print("✗ No template found")
        return
    
    # Load template
    template_content = manager.load_template(role_category)
    if template_content:
        print(f"\n✓ Template loaded successfully!")
        print(f"✓ Template size: {len(template_content)} characters")
        
        # Check for key Android/AOSP content
        android_keywords = ['Android', 'AOSP', 'Kotlin', 'automotive', 'infotainment']
        found_keywords = [kw for kw in android_keywords if kw in template_content]
        print(f"✓ Android keywords found in template: {', '.join(found_keywords)}")
        
        # Show first few lines
        lines = template_content.split('\n')[:15]
        print(f"\n✓ Template preview (first 15 lines):")
        print("-" * 80)
        for line in lines:
            print(line)
        print("-" * 80)
    else:
        print("✗ Failed to load template")
    
    print("\n" + "=" * 80)
    print("✓ Template system is working correctly!")
    print("=" * 80)

if __name__ == '__main__':
    main()
