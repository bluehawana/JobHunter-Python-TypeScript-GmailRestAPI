#!/usr/bin/env python3
"""Test Gemini API"""
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

api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key: {api_key[:20]}..." if api_key else "API Key: NOT FOUND")

if not api_key:
    print("❌ No API key found!")
    exit(1)

url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}'

data = {
    'contents': [{
        'parts': [{'text': 'Say hello in one word'}]
    }]
}

print(f"\n🔍 Testing Gemini API...")

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"✅ Success! Response: {text}")
    else:
        print(f"❌ Error: {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
