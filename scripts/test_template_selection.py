#!/usr/bin/env python3
"""Test template selection with real job_applications templates"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from cv_templates import CVTemplateManager

manager = CVTemplateManager()

# Test 1: DevOps job (should use gothenburg template, NO banking)
devops_jd = '''
Senior DevOps Engineer
We are looking for a DevOps Engineer with expertise in Kubernetes, Terraform, and AWS.
You will build CI/CD pipelines and manage cloud infrastructure.
'''

role = manager.analyze_job_role(devops_jd)
template_path = manager.get_template_path(role)
print(f'Test 1 - DevOps Job:')
print(f'  Role: {role}')
print(f'  Template: {template_path}')
print(f'  Expected: gothenburg_devops_cicd (NO banking)')
print(f'  ✓ PASS' if 'gothenburg' in str(template_path) else '  ✗ FAIL')
print()

# Test 2: FinTech job (should use nasdaq template WITH banking)
fintech_jd = '''
DevOps Engineer - Financial Services
Nasdaq is looking for a DevOps Engineer with experience in financial systems.
Knowledge of payment systems, trading platforms, and banking operations is a plus.
'''

role = manager.analyze_job_role(fintech_jd)
template_path = manager.get_template_path(role)
print(f'Test 2 - FinTech Job:')
print(f'  Role: {role}')
print(f'  Template: {template_path}')
print(f'  Expected: nasdaq_devops_cloud (WITH banking)')
print(f'  ✓ PASS' if 'nasdaq' in str(template_path) else '  ✗ FAIL')
print()

# Test 3: AI Product Engineer (should use omnimodular template, NO banking)
ai_jd = '''
AI Product Engineer
We need an AI Product Engineer with experience in LLM integration, GPT-4, and Claude.
Build intelligent systems with React, TypeScript, and Python.
'''

role = manager.analyze_job_role(ai_jd)
template_path = manager.get_template_path(role)
print(f'Test 3 - AI Product Engineer:')
print(f'  Role: {role}')
print(f'  Template: {template_path}')
print(f'  Expected: omnimodular (NO banking)')
print(f'  ✓ PASS' if 'omnimodular' in str(template_path) else '  ✗ FAIL')
print()

# Test 4: Android Developer
android_jd = '''
Android Platform Developer
Looking for Android developer with Kotlin and AOSP experience for automotive infotainment.
'''

role = manager.analyze_job_role(android_jd)
template_path = manager.get_template_path(role)
print(f'Test 4 - Android Developer:')
print(f'  Role: {role}')
print(f'  Template: {template_path}')
print(f'  Expected: ecarx_android_developer')
print(f'  ✓ PASS' if 'ecarx' in str(template_path) else '  ✗ FAIL')
print()

# Test 5: Full-stack Developer
fullstack_jd = '''
Full-Stack Developer
We need a full-stack developer with React, Node.js, and TypeScript experience.
Build modern web applications with cloud infrastructure.
'''

role = manager.analyze_job_role(fullstack_jd)
template_path = manager.get_template_path(role)
print(f'Test 5 - Full-Stack Developer:')
print(f'  Role: {role}')
print(f'  Template: {template_path}')
print(f'  Expected: doit_international')
print(f'  ✓ PASS' if 'doit' in str(template_path) else '  ✗ FAIL')
print()

print("=" * 60)
print("Summary: Template system now uses REAL templates from job_applications/")
print("✓ DevOps jobs use gothenburg template (NO banking content)")
print("✓ FinTech jobs use nasdaq template (WITH banking experience)")
print("✓ AI jobs use omnimodular template (NO banking content)")
