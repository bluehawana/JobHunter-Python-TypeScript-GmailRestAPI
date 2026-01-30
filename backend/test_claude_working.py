#!/usr/bin/env python3
"""
Test to get Claude API actually working for LEGO decisions
"""
import asyncio
import os
import sys
import subprocess
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

def test_claude_direct_cli():
    """Test Claude CLI directly with minimal prompt"""
    print("🔧 Testing Claude CLI directly...")
    
    token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("CLAUDE_MODEL")
    
    print(f"🔑 Token: {token[:20]}...")
    print(f"🌐 Base URL: {base_url}")
    print(f"🤖 Model: {model}")
    
    # Simple test prompt
    test_prompt = """Job: Senior Backend Developer at Volvo Group
Requirements: Java, Spring Boot, microservices, AWS, Kubernetes

Analyze this job and return ONLY this JSON format:
{"focus": "backend", "skills": ["Java", "Spring Boot", "AWS"], "role_title": "Backend Developer"}"""
    
    try:
        # Set environment
        env = os.environ.copy()
        env["ANTHROPIC_AUTH_TOKEN"] = token
        env["ANTHROPIC_BASE_URL"] = base_url
        
        # Run Claude CLI with shorter timeout
        print("📤 Running Claude CLI...")
        result = subprocess.run([
            "claude", "--model", model, "--print"
        ], input=test_prompt, text=True, capture_output=True, env=env, timeout=15)
        
        if result.returncode == 0 and result.stdout:
            response = result.stdout.strip()
            print(f"✅ Claude responded: {response}")
            return response
        else:
            print(f"❌ Claude CLI failed: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("⏰ Claude CLI timed out after 15 seconds")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_alternative_approach():
    """Test alternative approach using curl"""
    print("\n🌐 Testing alternative HTTP approach...")
    
    token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("CLAUDE_MODEL")
    
    # Try different endpoint patterns
    endpoints_to_try = [
        f"{base_url}/v1/messages",
        f"{base_url}/api/v1/messages", 
        f"{base_url}/v1/chat/completions",
        f"{base_url}/api/v1/chat/completions"
    ]
    
    for endpoint in endpoints_to_try:
        print(f"🔍 Trying endpoint: {endpoint}")
        
        curl_command = [
            "curl", "-s", "-X", "POST", endpoint,
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {token}",
            "-H", "anthropic-version: 2023-06-01",
            "-d", f'''{{
                "model": "{model}",
                "max_tokens": 100,
                "messages": [{{
                    "role": "user", 
                    "content": "Test: Return just the word SUCCESS"
                }}]
            }}'''
        ]
        
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                response = result.stdout
                print(f"📥 Response: {response[:200]}...")
                if "SUCCESS" in response or "content" in response:
                    print(f"✅ Working endpoint found: {endpoint}")
                    return endpoint
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    return None

if __name__ == "__main__":
    print("🧪 Testing Claude API to make LEGO system work properly...\n")
    
    # Test 1: Direct CLI
    claude_response = test_claude_direct_cli()
    
    # Test 2: Alternative HTTP
    if not claude_response:
        working_endpoint = test_alternative_approach()
        if working_endpoint:
            print(f"\n🎉 Found working endpoint: {working_endpoint}")
        else:
            print("\n❌ No working endpoints found")
    
    if claude_response:
        print(f"\n🎉 Claude is working! We can now implement true LEGO logic.")
    else:
        print(f"\n⚠️ Claude API issues confirmed. Need to fix this for true LEGO system.")