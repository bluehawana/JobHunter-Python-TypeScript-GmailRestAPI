#!/usr/bin/env python3
"""
Test MiniMax M2.1 API using direct HTTP requests
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_minimax_http():
    """Test MiniMax M2.1 using direct HTTP requests"""
    try:
        load_dotenv()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
        
        print(f"🔑 API Key: {api_key[:20]}..." if api_key else "❌ No API key found")
        print(f"🌐 Base URL: {base_url}")
        
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return False
        
        # Test 1: Simple greeting
        print("\n1️⃣ Testing simple greeting...")
        url = f"{base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "MiniMax-M2.1",
            "max_tokens": 1000,
            "system": "You are a helpful assistant.",
            "messages": [
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
        }
        
        print("🚀 Making HTTP request for greeting...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Simple greeting successful!")
            
            # Process response content
            if 'content' in result:
                for block in result['content']:
                    if block.get('type') == 'thinking':
                        print(f"🧠 Thinking: {block.get('thinking', '')}")
                    elif block.get('type') == 'text':
                        print(f"📝 Text: {block.get('text', '')}")
            else:
                print(f"🤖 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Simple greeting failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
        
        # Test 2: Job analysis
        print("\n2️⃣ Testing job analysis...")
        
        job_payload = {
            "model": "MiniMax-M2.1",
            "max_tokens": 1500,
            "system": "You are a helpful AI assistant that analyzes job descriptions and extracts key information.",
            "messages": [
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
        }
        
        print("🚀 Making HTTP request for job analysis...")
        response = requests.post(url, headers=headers, json=job_payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Job analysis successful!")
            
            # Process response content
            if 'content' in result:
                for block in result['content']:
                    if block.get('type') == 'thinking':
                        print(f"🧠 Thinking: {block.get('thinking', '')}")
                    elif block.get('type') == 'text':
                        text_content = block.get('text', '')
                        print(f"📝 Text: {text_content}")
                        
                        # Try to parse JSON from response
                        import re
                        json_match = re.search(r'\{.*\}', text_content, re.DOTALL)
                        
                        if json_match:
                            try:
                                parsed_json = json.loads(json_match.group())
                                print("✅ JSON parsing successful!")
                                print(f"📊 Extracted data:")
                                for key, value in parsed_json.items():
                                    print(f"   {key}: {value}")
                            except json.JSONDecodeError as e:
                                print(f"⚠️ JSON parsing failed: {e}")
            else:
                print(f"🤖 Response: {json.dumps(result, indent=2)}")
                
            return True
        else:
            print(f"❌ Job analysis failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error with HTTP request: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing MiniMax M2.1 via HTTP Requests")
    print("=" * 50)
    
    success = test_minimax_http()
    
    print("=" * 50)
    if success:
        print("🎉 MiniMax M2.1 HTTP test completed successfully!")
        print("💡 You can now use MiniMax M2.1 via HTTP requests")
    else:
        print("❌ MiniMax M2.1 HTTP test failed")
        print("💡 Check your API credentials and network connection")