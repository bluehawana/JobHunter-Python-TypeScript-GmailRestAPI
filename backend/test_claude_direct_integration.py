#!/usr/bin/env python3
"""
Direct test of Claude API with your configured environment
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables from .env file
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
        print("✅ Loaded .env file")
    except FileNotFoundError:
        print("❌ .env file not found")

load_env_file()

async def test_claude_direct():
    """Test Claude API directly with your configuration"""
    print("🔧 Testing Claude API with your configuration...")
    
    # Check environment variables
    token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    
    print(f"🔑 Token: {token[:20]}..." if token else "❌ No token found")
    print(f"🌐 Base URL: {base_url}")
    
    if not token:
        print("❌ ANTHROPIC_AUTH_TOKEN not found. Please set it:")
        print("export ANTHROPIC_AUTH_TOKEN=sk-...")
        return
    
    try:
        from app.services.claude_api_service import ClaudeAPIService
        claude = ClaudeAPIService()
        
        print(f"🤖 Claude API initialized: {claude.get_current_api_info()}")
        
        # Test simple prompt
        test_prompt = """
        Analyze this job and suggest 3 key skills to highlight:
        
        Job: Senior Backend Developer at Spotify
        Description: Java, Spring Boot, microservices, AWS, Kubernetes
        
        Return as JSON: {"skills": ["skill1", "skill2", "skill3"]}
        """
        
        print("📤 Sending test prompt to Claude...")
        response = await claude.generate_text(test_prompt)
        
        if response:
            print(f"✅ Claude responded ({len(response)} chars):")
            print(f"📝 Response: {response[:200]}...")
            
            # Test LEGO strategy
            print("\n🧠 Testing LEGO strategy generation...")
            lego_prompt = """
            Create a LEGO strategy for this job:
            Job: Backend Developer at Volvo
            Description: Java, Spring, microservices, automotive industry
            
            Return JSON with: primary_focus, skills_to_highlight, profile_angle
            """
            
            lego_response = await claude.generate_text(lego_prompt)
            print(f"🎯 LEGO Strategy: {lego_response[:300]}...")
            
            print("\n🎉 Claude API integration working perfectly!")
            
        else:
            print("❌ Claude API returned empty response")
            print("💡 Check your token and base URL configuration")
            
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_claude_direct())