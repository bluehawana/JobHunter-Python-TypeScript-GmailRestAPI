#!/usr/bin/env python3
"""
Test Z.AI GLM-4.7 connection on VPS
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_zai_on_vps():
    """Test Z.AI connection on VPS"""
    try:
        # Load environment variables
        load_dotenv()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        print("🧪 Testing Z.AI GLM-4.7 on VPS")
        print("=" * 40)
        print(f"🔑 API Key: {api_key[:20]}..." if api_key else "❌ No API key found")
        print(f"🌐 Base URL: {base_url}")
        
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            print("💡 Check your .env file")
            return False
        
        # Test Z.AI connection
        url = f"{base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "glm-4.7",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": "Hello! Please respond with 'Z.AI GLM-4.7 is working on VPS!'"}]
        }
        
        print("🚀 Making test request to Z.AI...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Z.AI connection successful!")
            
            # Extract response text
            if 'content' in result:
                for block in result['content']:
                    if block.get('type') == 'text':
                        print(f"🤖 Response: {block.get('text', '')}")
            
            return True
        else:
            print(f"❌ Z.AI connection failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Z.AI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_zai_on_vps()
    
    print("=" * 40)
    if success:
        print("🎉 Z.AI GLM-4.7 is working on VPS!")
    else:
        print("❌ Z.AI GLM-4.7 test failed on VPS")
        print("💡 Check API credentials and network connection")