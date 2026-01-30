#!/usr/bin/env python3
"""
Heroku Job Automation Entry Point
Runs the complete job hunting automation with beautiful multi-page PDFs
Scheduled to run at 20:00 Swedish time for optimal Claude API performance
"""
import asyncio
import os
import sys
import logging
from datetime import datetime
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
        print("✅ Environment variables loaded")
    except FileNotFoundError:
        print("⚠️ .env file not found, using Heroku environment variables")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_heroku_automation():
    """Main Heroku automation function"""
    try:
        print("🚀 HEROKU JOB AUTOMATION STARTED")
        print("=" * 60)
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"🌍 Timezone: {os.getenv('TZ', 'UTC')}")
        print(f"🎯 Mode: Automated Job Hunting with Beautiful PDFs")
        print(f"📧 Target: hongzhili01@gmail.com")
        print("=" * 60)
        
        # Import and run the improved automation
        from improved_working_automation import ImprovedWorkingAutomation
        
        automation = ImprovedWorkingAutomation()
        
        print("📧 Scanning Gmail for job opportunities...")
        await automation.scan_and_process_jobs()
        
        print("\n🎉 HEROKU AUTOMATION COMPLETED!")
        print("=" * 60)
        print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("📧 Check hongzhili01@gmail.com for professional job applications")
        print("🎯 Beautiful multi-page PDFs generated with LEGO intelligence")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Heroku automation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Entry point for Heroku"""
    print("🧩 JobHunter - Heroku Automation")
    print("🤖 Claude-powered LEGO system with beautiful PDFs")
    
    # Load environment variables
    load_env_file()
    
    # Run the automation
    asyncio.run(run_heroku_automation())

if __name__ == "__main__":
    main()