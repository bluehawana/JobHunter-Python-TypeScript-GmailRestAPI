#!/usr/bin/env python3
"""
Simple Claude API test using direct HTTP instead of CLI
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

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

async def test_claude_http():
    """Test Claude API using HTTP instead of CLI"""
    print("🌐 Testing Claude API with HTTP approach...")
    
    try:
        import aiohttp
        
        token = os.getenv("ANTHROPIC_AUTH_TOKEN")
        base_url = os.getenv("ANTHROPIC_BASE_URL", "https://anyrouter.top")
        model = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")
        
        print(f"🔑 Token: {token[:20]}...")
        print(f"🌐 Base URL: {base_url}")
        print(f"🤖 Model: {model}")
        
        # Test simple HTTP request
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": token
        }
        
        request_data = {
            "model": model,
            "max_tokens": 1000,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": "Analyze this job and suggest 3 key skills to highlight for a resume: Job: Senior Backend Developer at Volvo. Requirements: Java, Spring Boot, microservices, AWS. Return as JSON: {\"skills\": [\"skill1\", \"skill2\", \"skill3\"]}"
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            url = f"{base_url}/v1/messages"
            print(f"📤 Sending request to: {url}")
            
            async with session.post(
                url,
                headers=headers,
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                print(f"📥 Response status: {response.status}")
                
                if response.status == 200:
                    response_data = await response.json()
                    print(f"✅ Success! Response: {response_data}")
                    
                    if "content" in response_data and response_data["content"]:
                        content = response_data["content"][0]["text"]
                        print(f"🎯 Claude's response: {content}")
                        return True
                else:
                    error_text = await response.text()
                    print(f"❌ Error {response.status}: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_claude_http())
    if success:
        print("🎉 Claude HTTP API is working!")
    else:
        print("💡 Consider using CLI fallback or checking API configuration")