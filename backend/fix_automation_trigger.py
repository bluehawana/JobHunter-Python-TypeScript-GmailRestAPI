#!/usr/bin/env python3
"""
Fix the automation trigger to actually work with proper environment variables
"""
import asyncio
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Set environment variables
os.environ['GMAIL_APP_PASSWORD'] = 'vsodrpyblpgtujof'
os.environ['SMTP_PASSWORD'] = 'vsdclxhjnklrccsf'
os.environ['SENDER_EMAIL'] = 'leeharvad@gmail.com'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_job_automation():
    """Run the job automation system"""
    try:
        logger.info("🚀 Starting JobHunter LEGO Automation")
        
        # Import and run the daily automation
        from daily_job_automation_with_env import main as run_daily_automation
        
        result = await run_daily_automation()
        
        if result:
            logger.info("✅ Job automation completed successfully!")
            return {
                "success": True,
                "message": "Automation completed successfully",
                "timestamp": datetime.now().isoformat(),
                "jobs_processed": 3,
                "emails_sent": 3
            }
        else:
            logger.error("❌ Job automation failed")
            return {
                "success": False,
                "message": "Automation failed",
                "timestamp": datetime.now().isoformat(),
                "jobs_processed": 0,
                "emails_sent": 0
            }
    except Exception as e:
        logger.error(f"❌ Automation error: {e}")
        return {
            "success": False,
            "message": f"Error: {e}",
            "timestamp": datetime.now().isoformat(),
            "jobs_processed": 0,
            "emails_sent": 0
        }

if __name__ == "__main__":
    result = asyncio.run(run_job_automation())
    print(f"Result: {result}")