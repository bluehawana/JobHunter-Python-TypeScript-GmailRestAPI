#!/usr/bin/env python3
"""
Test Claude API using command line approach
"""
import os
import subprocess
import asyncio

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

async def test_claude_cli():
    """Test Claude API using CLI approach"""
    
    token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")
    
    print(f"🔧 Testing Claude CLI Configuration:")
    print(f"   Token: {token[:20]}..." if token else "   Token: None")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print()
    
    if not token or not base_url:
        print("❌ Missing ANTHROPIC_AUTH_TOKEN or ANTHROPIC_BASE_URL")
        return False
    
    # Set environment variables for CLI
    env = os.environ.copy()
    env["ANTHROPIC_AUTH_TOKEN"] = token
    env["ANTHROPIC_BASE_URL"] = base_url
    
    # Test prompt
    test_prompt = "Hello! Please respond with 'Claude API test successful' if you can read this message."
    
    try:
        print("🤖 Testing Claude CLI...")
        
        # Try the claude command
        cmd = ["claude", "--model", model, "--print"]
        
        result = subprocess.run(
            cmd,
            input=test_prompt,
            text=True,
            capture_output=True,
            env=env,
            timeout=30
        )
        
        print(f"📊 Return code: {result.returncode}")
        print(f"📤 Stdout: {result.stdout}")
        print(f"📥 Stderr: {result.stderr}")
        
        if result.returncode == 0 and result.stdout:
            print("✅ Claude CLI test successful!")
            return True
        else:
            print("❌ Claude CLI test failed")
            return False
            
    except FileNotFoundError:
        print("❌ 'claude' command not found. You may need to install the Claude CLI.")
        print("💡 Try: pip install claude-cli")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_claude_cli())