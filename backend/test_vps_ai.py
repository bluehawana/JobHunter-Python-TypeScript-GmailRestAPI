#!/usr/bin/env python3
"""
Quick test script to verify AI is working on VPS
Run this after deployment to ensure everything is set up correctly
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("🧪 Testing AI Integration on VPS")
print("="*80)

# Test 1: Check imports
print("\n1. Testing imports...")
try:
    from ai_analyzer import AIAnalyzer
    from cv_templates import CVTemplateManager
    from minimax_search.models import Document
    print("   ✅ All imports successful")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check environment
print("\n2. Checking environment variables...")
import os
if os.getenv('ANTHROPIC_API_KEY'):
    print("   ✅ ANTHROPIC_API_KEY is set")
else:
    print("   ❌ ANTHROPIC_API_KEY not found")

if os.getenv('ANTHROPIC_BASE_URL'):
    print(f"   ✅ ANTHROPIC_BASE_URL: {os.getenv('ANTHROPIC_BASE_URL')}")
else:
    print("   ⚠️  ANTHROPIC_BASE_URL not set (will use default)")

# Test 3: Check AI availability
print("\n3. Testing AI Analyzer...")
try:
    analyzer = AIAnalyzer()
    if analyzer.is_available():
        print("   ✅ AI Analyzer is available")
        print(f"   ✅ Model: {analyzer.model}")
    else:
        print("   ⚠️  AI Analyzer not available (will use keyword fallback)")
except Exception as e:
    print(f"   ❌ AI Analyzer error: {e}")

# Test 4: Test template manager
print("\n4. Testing Template Manager...")
try:
    manager = CVTemplateManager()
    templates = manager.list_available_templates()
    available = [t for t in templates if t['template_exists']]
    print(f"   ✅ Template Manager initialized")
    print(f"   ✅ {len(available)}/{len(templates)} templates available")
except Exception as e:
    print(f"   ❌ Template Manager error: {e}")

# Test 5: Quick AI analysis
print("\n5. Testing AI analysis...")
test_job = """
DevOps Engineer position requiring Kubernetes, Docker, AWS, and CI/CD experience.
Must have Python and Terraform skills.
"""

try:
    if analyzer.is_available():
        result = analyzer.analyze_job_description(test_job)
        if result:
            print(f"   ✅ AI Analysis successful")
            print(f"   ✅ Role: {result['role_category']}")
            print(f"   ✅ Confidence: {result['confidence']:.0%}")
        else:
            print("   ⚠️  AI Analysis returned no result")
    else:
        print("   ⚠️  Skipping AI test (not available)")
        # Test keyword fallback
        role = manager.analyze_job_role(test_job)
        print(f"   ✅ Keyword fallback: {role}")
except Exception as e:
    print(f"   ❌ Analysis error: {e}")

# Test 6: Test data models
print("\n6. Testing data models...")
try:
    from minimax_search.models import SearchFilters
    filters = SearchFilters(document_types=['cv'], max_results=10)
    filters.validate()
    print("   ✅ Data models working")
except Exception as e:
    print(f"   ❌ Data model error: {e}")

# Summary
print("\n" + "="*80)
print("📊 Test Summary")
print("="*80)

if analyzer.is_available():
    print("✅ AI Integration: WORKING")
    print("   Your VPS has full AI intelligence!")
else:
    print("⚠️  AI Integration: FALLBACK MODE")
    print("   Using keyword matching (still works, but no AI)")
    print("   Check:")
    print("   - ANTHROPIC_API_KEY in .env")
    print("   - anthropic package installed: pip3 install anthropic")

print("\n🎉 VPS is ready to use!")
print("="*80)
