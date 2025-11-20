#!/usr/bin/env python3
"""Simple test to verify Claude API works"""
import os
import requests
from pathlib import Path

# Load .env
env_path = Path('.env')
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val

api_key = os.getenv('ANTHROPIC_API_KEY')
base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com')
version = os.getenv('ANTHROPIC_VERSION', '2023-06-01')

print(f"API Key: {api_key[:20]}..." if api_key else "API Key: NOT FOUND")
print(f"Base URL: {base_url}")
print(f"Version: {version}")

if not api_key:
    print("❌ No API key found!")
    exit(1)

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
    'anthropic-version': version
}

data = {
    'model': 'claude-3-5-sonnet-20241022',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Say hello in one word'}]
}

print(f"\n🔍 Testing Claude API at {base_url}/v1/messages...")

try:
    response = requests.post(
        f'{base_url}/v1/messages',
        headers=headers,
        json=data,
        timeout=30
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:500]}")

    if response.status_code == 200:
        try:
            result = response.json()
            print(f"✅ Success! Response: {result['content'][0]['text']}")
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Raw response: {response.text}")
    else:
        print(f"❌ Error: {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
