#!/usr/bin/env python3
"""Test Project Manager role detection"""
import sys
sys.path.insert(0, 'backend')

from cv_templates import CVTemplateManager

job_description = """
Senior Project Manager
JR-49184
Published on 03 Feb 2026 by InfiMotion Technology Europe AB

Role: Engineering Project Management
Seniority level: Senior
Location: Gothenburg (SE)
Remote: 0%
Assignment period: 02 Mar 2026 - 31 Dec 2026
Application deadline: 15 Feb 2026 23:59 (10 days left)

Assignment description:
For our client we are looking for a Senior Project Manager.

As a Senior Project Manager you will be responsibility for overseeing the delivery of project content 
for specific vehicle applications, Advanced Engineering projects, and sales campaigns. Your role will 
involve ensuring that sales and program activities are closely aligned with customer requirements in 
terms of quality, timing, and cost. You will lead customer projects, take the lead in coordinating 
project work across engineering teams located in both Sweden and China. Moreover, you will be 
responsible for effectively managing decision points and mitigating risks to ensure that project 
objectives are successfully achieved.

Responsibilities/Tasks:
- Carry out and execute projects for their customers mainly found within the automotive industry.
- Ensure projects are managed successfully against the targets of timing, quality and cost.
- Subject matter expert in project execution and technical matters in discussions with their commercial and sales teams.
- Coordinate and lead internal expertise in RFI and RFQ responses.
- Ensure project issues are managed with agreed solutions between China and Sweden teams

Requirements to succeed in this role:
- A university degree within a technical field or equivalent working experience
- Project management experience within Electric Drive systems
- Experience within the European automotive culture
- Strong background in technical sales support
- Fluency in both spoken and written English
- Intercultural experience from China/Asia is highly valued

About you:
We are seeking an individual with strong leadership abilities, capable of inspiring, driving, and 
motivating teams. Additionally, excellent communication, negotiation, and influencing skills are essential.
"""

print("🧪 Testing Project Manager Role Detection")
print("=" * 60)

template_manager = CVTemplateManager()
role_category = template_manager.analyze_job_role(job_description)

print(f"✅ Detected Role: {role_category}")
print(f"📋 Template: {template_manager.get_template_path(role_category, 'cv')}")
print(f"📄 CL Template: {template_manager.get_template_path(role_category, 'cl')}")

# Check if it matches project_manager
if role_category == 'project_manager':
    print("✅ SUCCESS: Correctly detected as Project Manager!")
else:
    print(f"❌ FAILED: Detected as '{role_category}' instead of 'project_manager'")
    print("\nKeywords found in job description:")
    job_lower = job_description.lower()
    pm_keywords = ['project manager', 'technical project manager', 'pm', 'project lead', 
                   'program manager', 'project coordinator', 'agile project', 'scrum master', 
                   'project management', 'pmp', 'stakeholder management', 'budget management', 
                   'risk management', 'project delivery', 'cross-functional teams']
    for keyword in pm_keywords:
        if keyword in job_lower:
            print(f"  - '{keyword}' ✓")

print("=" * 60)
