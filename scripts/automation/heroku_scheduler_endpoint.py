#!/usr/bin/env python3
"""
Heroku Scheduler Endpoint - Simple HTTP trigger for job automation
Use this with external cron services or Heroku Scheduler
"""
import sys
import os
sys.path.append('backend')

import asyncio
from run_06_00_automation import JobAutomationRunner

async def run_scheduled_automation():
    """Run the automation via HTTP endpoint"""
    print("🚀 HEROKU SCHEDULER: Starting job automation...")
    
    try:
        runner = JobAutomationRunner()
        await runner.run_automation()
        print("✅ HEROKU SCHEDULER: Automation completed successfully")
        return True
    except Exception as e:
        print(f"❌ HEROKU SCHEDULER: Automation failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_scheduled_automation())
    sys.exit(0 if success else 1)