#!/usr/bin/env python3
"""
Test official Claude Pro API directly
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

async def test_official_claude():
    """Test official Claude Pro API"""
    print("🔑 Testing Official Claude Pro API...")
    
    try:
        from app.services.claude_api_service import ClaudeAPIService
        claude = ClaudeAPIService()
        
        print(f"🔧 API info: {claude.get_current_api_info()}")
        
        # Test LEGO strategy generation
        test_prompt = """
        Analyze this job and create a LEGO strategy for Hongzhi Li:
        
        Job: Senior Backend Developer at Spotify
        Description: Java, Spring Boot, microservices, Kubernetes, AWS, international team
        
        Return JSON format:
        {
            "primary_focus": "backend",
            "skills_to_highlight": ["Java", "Spring Boot", "AWS"],
            "role_title": "Backend Developer & API Specialist",
            "profile_angle": "Experienced backend developer with international perspective"
        }
        
        Keep response concise and focused.
        """
        
        print("📤 Testing LEGO strategy generation...")
        response = await claude.generate_text(test_prompt)
        
        if response:
            print(f"✅ Official Claude Pro API success!")
            print(f"📝 Response ({len(response)} chars):")
            print(f"{response}")
            
            # Test cover letter generation
            print("\n💌 Testing cover letter generation...")
            cover_prompt = """
            Write a brief cover letter opening for Hongzhi Li:
            Job: Backend Developer at Spotify
            Focus: Cross-cultural bridge building, business-IT translation
            Length: 2-3 sentences maximum
            """
            
            cover_response = await claude.generate_text(cover_prompt)
            if cover_response:
                print(f"✅ Cover letter success!")
                print(f"📝 Response: {cover_response}")
                return True
            else:
                print("❌ Cover letter generation failed")
                return False
        else:
            print("❌ Official Claude Pro API failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_official_claude())
    if success:
        print("\n🎉 Official Claude Pro API is working perfectly!")
        print("💰 Using cost-efficient Sonnet 3.5 model")
        print("🧠 Ready for true LEGO intelligence!")
    else:
        print("\n⚠️ Official API needs debugging.")