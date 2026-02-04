#!/usr/bin/env python3
"""
Test Z.AI GLM-4.7 integration with our AI analyzer
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

def test_ai_analyzer_with_zai():
    """Test our AI analyzer with Z.AI GLM-4.7"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from ai_analyzer import AIAnalyzer
        
        print("🧪 Testing AI Analyzer with Z.AI GLM-4.7")
        print("=" * 50)
        
        analyzer = AIAnalyzer()
        
        print(f"🔧 AI Available: {analyzer.is_available()}")
        print(f"🤖 Model: {analyzer.model}")
        
        if not analyzer.is_available():
            print("❌ AI analyzer not available")
            return False
        
        # Test job description
        job_description = """
Customer Support Engineer at Kamstrup
We are looking for a Customer Support Engineer to join our team. You will be responsible for providing technical support to customers, troubleshooting issues, and ensuring customer satisfaction.

Requirements:
- Technical support experience
- Strong communication skills
- Problem-solving abilities
- Knowledge of networking and troubleshooting
- Experience with customer service
- Ability to work in a team environment

Responsibilities:
- Provide technical support to customers via phone, email, and chat
- Troubleshoot hardware and software issues
- Document customer interactions and solutions
- Collaborate with engineering teams to resolve complex issues
- Train customers on product usage
"""
        
        print("🚀 Analyzing job description...")
        result = analyzer.analyze_job_description(job_description)
        
        if result:
            print("✅ AI analysis successful!")
            print(f"📊 Results:")
            print(f"   Role Category: {result['role_category']}")
            print(f"   Confidence: {result['confidence']:.1%}")
            print(f"   Key Technologies: {result.get('key_technologies', [])}")
            print(f"   Reasoning: {result.get('reasoning', 'N/A')}")
            return True
        else:
            print("❌ AI analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AI analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_analyzer_with_zai()
    
    print("=" * 50)
    if success:
        print("🎉 Z.AI GLM-4.7 integration test successful!")
        print("💡 The system is ready to use Z.AI for job analysis")
    else:
        print("❌ Z.AI GLM-4.7 integration test failed")
        print("💡 Check your Z.AI API credentials and configuration")