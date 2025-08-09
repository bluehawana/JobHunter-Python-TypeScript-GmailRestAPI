#!/usr/bin/env python3
"""
Test the Claude API load balancer with retry logic
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

async def test_load_balancer():
    """Test the Claude API load balancer"""
    print("🔄 Testing Claude API Load Balancer...")
    
    try:
        from app.services.claude_api_service import ClaudeAPIService
        claude = ClaudeAPIService()
        
        print(f"🔧 Load balancer info: {claude.get_current_api_info()}")
        
        # Test simple LEGO strategy prompt
        test_prompt = """
        Analyze this job and create a LEGO strategy:
        
        Job: Senior Backend Developer at Spotify
        Description: Java, Spring Boot, microservices, Kubernetes, AWS
        
        Return JSON format:
        {
            "primary_focus": "backend",
            "skills_to_highlight": ["Java", "Spring Boot", "AWS"],
            "role_title": "Backend Developer & API Specialist"
        }
        """
        
        print("📤 Testing LEGO strategy generation...")
        response = await claude.generate_text(test_prompt)
        
        if response:
            print(f"✅ Load balancer success!")
            print(f"📝 Response ({len(response)} chars): {response[:200]}...")
            
            # Test cover letter prompt
            print("\n💌 Testing cover letter generation...")
            cover_letter_prompt = """
            Create a personalized cover letter opening paragraph for:
            Job: Backend Developer at Spotify
            Focus on cross-cultural skills and business-IT translation abilities.
            Keep it under 100 words.
            """
            
            cover_response = await claude.generate_text(cover_letter_prompt)
            if cover_response:
                print(f"✅ Cover letter success!")
                print(f"📝 Response: {cover_response[:150]}...")
            else:
                print("❌ Cover letter generation failed")
            
            return True
        else:
            print("❌ Load balancer failed to get response")
            return False
            
    except Exception as e:
        print(f"❌ Load balancer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_load_balancer())
    if success:
        print("\n🎉 Load balancer is working! LEGO system can now use Claude intelligence.")
    else:
        print("\n⚠️ Load balancer needs debugging.")