#!/usr/bin/env python3
"""
Test MiniMax M2.1 API directly using official documentation format
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

def test_minimax_official():
    """Test MiniMax M2.1 using official documentation format"""
    try:
        import anthropic
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
        
        print(f"🔑 API Key: {api_key[:20]}..." if api_key else "❌ No API key found")
        print(f"🌐 Base URL: {base_url}")
        
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return False
        
        # Set environment variables as per official docs
        os.environ['ANTHROPIC_BASE_URL'] = base_url
        os.environ['ANTHROPIC_API_KEY'] = api_key
        
        # Initialize client using official format
        client = anthropic.Anthropic()
        
        print("🚀 Testing MiniMax M2.1 connection...")
        
        # Test with job analysis prompt using official format
        message = client.messages.create(
            model="MiniMax-M2.1",  # Official model name
            max_tokens=1000,
            system="You are a helpful AI assistant that analyzes job descriptions and extracts key information.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this job description and extract key information:

JOB DESCRIPTION:
Customer Support Engineer at Kamstrup
We are looking for a Customer Support Engineer to join our team. You will be responsible for providing technical support to customers, troubleshooting issues, and ensuring customer satisfaction.

Requirements:
- Technical support experience
- Strong communication skills
- Problem-solving abilities
- Knowledge of networking and troubleshooting

Please respond with JSON format:
{
  "company": "company name",
  "title": "job title", 
  "roleCategory": "role category",
  "keySkills": ["skill1", "skill2", "skill3"]
}"""
                        }
                    ]
                }
            ]
        )
        
        print("✅ MiniMax M2.1 API call successful!")
        
        # Process response using official format
        for block in message.content:
            if block.type == "thinking":
                print(f"🧠 Thinking:\n{block.thinking}\n")
            elif block.type == "text":
                print(f"📝 Text Response:\n{block.text}\n")
                
                # Try to parse JSON from the text response
                import json
                import re
                
                response_text = block.text
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                
                if json_match:
                    try:
                        parsed_json = json.loads(json_match.group())
                        print("✅ JSON parsing successful!")
                        print(f"📊 Extracted data:")
                        for key, value in parsed_json.items():
                            print(f"   {key}: {value}")
                        return True
                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON parsing failed: {e}")
                        return False
        
        return True
            
    except Exception as e:
        print(f"❌ Error testing MiniMax M2.1: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_greeting():
    """Test with simple greeting like in the official docs"""
    try:
        import anthropic
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
        
        # Set environment variables
        os.environ['ANTHROPIC_BASE_URL'] = base_url
        os.environ['ANTHROPIC_API_KEY'] = api_key
        
        client = anthropic.Anthropic()
        
        print("🚀 Testing simple greeting (official docs example)...")
        
        message = client.messages.create(
            model="MiniMax-M2.1",
            max_tokens=1000,
            system="You are a helpful assistant.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Hi, how are you?"
                        }
                    ]
                }
            ]
        )
        
        print("✅ Simple greeting test successful!")
        
        for block in message.content:
            if block.type == "thinking":
                print(f"🧠 Thinking:\n{block.thinking}\n")
            elif block.type == "text":
                print(f"📝 Text:\n{block.text}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with simple greeting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing MiniMax M2.1 Direct API Call (Official Format)")
    print("=" * 60)
    
    # Test simple greeting first
    print("1️⃣ Testing simple greeting...")
    success1 = test_simple_greeting()
    
    print("\n" + "=" * 60)
    
    # Test job analysis
    print("2️⃣ Testing job analysis...")
    success2 = test_minimax_official()
    
    print("=" * 60)
    if success1 and success2:
        print("🎉 MiniMax M2.1 test completed successfully!")
        print("💡 Both simple greeting and job analysis work!")
    elif success1:
        print("✅ Simple greeting works, job analysis needs adjustment")
    elif success2:
        print("✅ Job analysis works, simple greeting needs adjustment")
    else:
        print("❌ MiniMax M2.1 tests failed")
        print("💡 Check your API credentials and network connection")