#!/usr/bin/env python3
"""
Test Z.AI GLM-4.7 API as alternative to MiniMax
"""

import os
from dotenv import load_dotenv

def test_zai_with_anthropic_client():
    """Test Z.AI using anthropic client"""
    try:
        from anthropic import Anthropic
        
        load_dotenv()
        
        # Use the same environment variables as the main system
        zai_api_key = os.environ.get('ANTHROPIC_API_KEY')  # Using ANTHROPIC_API_KEY as configured
        zai_base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        print(f"🔑 Z.AI API Key: {zai_api_key[:20]}..." if zai_api_key else "❌ No Z.AI API key configured")
        print(f"🌐 Z.AI Base URL: {zai_base_url}")
        
        if not zai_api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return False
        
        client = Anthropic(
            api_key=zai_api_key,
            base_url=zai_base_url
        )
        
        print("🚀 Testing Z.AI GLM-4.7 connection...")
        
        # Test 1: Simple greeting
        print("\n1️⃣ Testing simple greeting...")
        response = client.messages.create(
            model="glm-4.7",
            max_tokens=1000,
            messages=[{"role": "user", "content": "Hello! How are you?"}]
        )
        
        print("✅ Simple greeting successful!")
        print(f"📝 Response: {response.content[0].text}")
        
        # Test 2: Job analysis
        print("\n2️⃣ Testing job analysis...")
        job_analysis_response = client.messages.create(
            model="glm-4.7",
            max_tokens=2000,
            messages=[{
                "role": "user", 
                "content": """Analyze this job description and extract key information:

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
            }]
        )
        
        print("✅ Job analysis successful!")
        print(f"📝 Response: {job_analysis_response.content[0].text}")
        
        # Try to parse JSON from response
        import json
        import re
        
        response_text = job_analysis_response.content[0].text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            try:
                parsed_json = json.loads(json_match.group())
                print("✅ JSON parsing successful!")
                print(f"📊 Extracted data:")
                for key, value in parsed_json.items():
                    print(f"   {key}: {value}")
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Z.AI: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_zai_with_http():
    """Test Z.AI using direct HTTP requests"""
    try:
        import requests
        import json
        
        load_dotenv()
        
        zai_api_key = os.environ.get('ANTHROPIC_API_KEY')  # Using ANTHROPIC_API_KEY as configured
        zai_base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not zai_api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return False
        
        print("🌐 Testing Z.AI with HTTP requests...")
        
        url = f"{zai_base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {zai_api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "glm-4.7",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": "Hello! How are you?"}]
        }
        
        print("🚀 Making HTTP request to Z.AI...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Z.AI HTTP request successful!")
            print(f"🤖 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Z.AI HTTP request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error with Z.AI HTTP request: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Z.AI GLM-4.7 API")
    print("=" * 50)
    
    print("📝 Configuration found in .env:")
    print("ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic")
    print("ANTHROPIC_API_KEY=your-zai-api-key")
    print("=" * 50)
    
    # Try anthropic client first
    print("🔄 Testing with Anthropic client...")
    success1 = test_zai_with_anthropic_client()
    
    if not success1:
        print("\n" + "=" * 50)
        print("🔄 Testing with HTTP requests...")
        success2 = test_zai_with_http()
    else:
        success2 = True
    
    print("=" * 50)
    if success1 or success2:
        print("🎉 Z.AI GLM-4.7 test completed successfully!")
        print("💡 Z.AI can be used as alternative to MiniMax")
    else:
        print("❌ Z.AI GLM-4.7 test failed")
        print("💡 Check your Z.AI API credentials")