#!/usr/bin/env python3
"""
Direct test of Claude API configuration
"""
import os
import asyncio
import aiohttp

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

async def test_claude_api():
    """Test Claude API directly"""
    
    token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL", "https://anyrouter.top")
    model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    print(f"🔧 Testing Claude API Configuration:")
    print(f"   Token: {token[:20]}..." if token else "   Token: None")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print()
    
    if not token:
        print("❌ No ANTHROPIC_AUTH_TOKEN found")
        return
    
    # Test request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "anthropic-version": "2023-06-01"
    }
    
    request_data = {
        "model": model,
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with 'API test successful' if you can read this."
            }
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{base_url}/v1/messages"
            print(f"🌐 Making request to: {url}")
            
            async with session.post(
                url,
                headers=headers,
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                print(f"📊 Response Status: {response.status}")
                print(f"📋 Response Headers: {dict(response.headers)}")
                
                content_type = response.headers.get('content-type', '')
                print(f"📄 Content Type: {content_type}")
                
                if 'application/json' in content_type:
                    response_data = await response.json()
                    print(f"✅ JSON Response: {response_data}")
                    
                    if "content" in response_data:
                        content = response_data["content"][0]["text"]
                        print(f"🎉 Claude Response: {content}")
                        return True
                else:
                    text_content = await response.text()
                    print(f"❌ HTML/Text Response: {text_content[:300]}...")
                    return False
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_claude_api())