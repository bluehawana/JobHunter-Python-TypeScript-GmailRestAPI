#!/usr/bin/env python3
"""
Test Claude API integration with LEGO system
"""
import asyncio
import sys
import os
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

async def test_claude_lego_system():
    """Test Claude API integration with LEGO system"""
    print("🧪 Testing Claude API integration with LEGO system...")
    
    # Test job data
    test_job = {
        'title': 'Senior Backend Developer',
        'company': 'Spotify',
        'description': 'We are looking for a Senior Backend Developer with expertise in Java, Spring Boot, microservices architecture, and cloud platforms. Experience with Kubernetes, Docker, and AWS is highly valued. The role involves building scalable APIs and working with international teams.',
        'url': 'https://jobs.spotify.com/test',
        'location': 'Stockholm, Sweden'
    }
    
    try:
        # Test Claude LEGO strategy
        from improved_working_automation import ImprovedWorkingAutomation
        automation = ImprovedWorkingAutomation()
        
        print("🧠 Testing Claude LEGO strategy analysis...")
        strategy = await automation._get_claude_lego_strategy(test_job)
        print(f"✅ LEGO Strategy: {strategy}")
        
        print("\n🤖 Testing Claude LEGO resume building...")
        resume_content = await automation._build_claude_lego_resume(test_job, strategy)
        print(f"✅ Resume built: {len(resume_content)} characters")
        
        print("\n💌 Testing Claude cover letter creation...")
        cover_letter = await automation._build_claude_cover_letter(test_job)
        print(f"✅ Cover letter created: {len(cover_letter)} characters")
        
        # Save test outputs
        with open('test_claude_strategy.json', 'w') as f:
            import json
            json.dump(strategy, f, indent=2)
        
        with open('test_claude_resume.tex', 'w') as f:
            f.write(resume_content)
        
        with open('test_claude_cover_letter.txt', 'w') as f:
            f.write(cover_letter)
        
        print("\n🎉 Claude integration test completed successfully!")
        print("📁 Check test_claude_*.* files for outputs")
        
    except Exception as e:
        print(f"❌ Claude integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_claude_lego_system())