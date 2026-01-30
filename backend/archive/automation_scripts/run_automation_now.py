#!/usr/bin/env python3
"""
Manual run script for daily job automation
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(project_dir / ".env")

from daily_job_automation import DailyJobAutomation

async def main():
    """Run automation manually"""
    
    print("🚀 MANUAL AUTOMATION RUN")
    print("=" * 30)
    
    automation = DailyJobAutomation()
    result = await automation.run_daily_automation()
    
    if result['success']:
        print("\n🎉 SUCCESS!")
        print(f"📊 Jobs found: {result.get('jobs_found', 0)}")
        print(f"📧 Applications generated: {result.get('applications_generated', 0)}")
        print(f"⏱️ Processing time: {result.get('processing_time_seconds', 0):.1f} seconds")
    else:
        print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())
