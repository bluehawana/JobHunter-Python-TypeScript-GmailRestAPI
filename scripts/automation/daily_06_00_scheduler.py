#!/usr/bin/env python3
"""
Daily 06:00 Job Automation Scheduler
Runs the job automation every weekday at 06:00 (6:00 AM)
"""
import schedule
import time
import subprocess
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_06_00_automation():
    """Execute the 06:00 automation"""
    logger.info("🎯 Starting 06:00 job automation...")
    
    try:
        # Activate virtual environment and run automation
        result = subprocess.run([
            'bash', '-c', 
            'source venv/bin/activate && python3 run_06_00_automation.py'
        ], capture_output=True, text=True, timeout=1800)  # 30 minute timeout
        
        if result.returncode == 0:
            logger.info("✅ 06:00 automation completed successfully")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error("❌ 06:00 automation failed")
            logger.error(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("❌ 06:00 automation timed out after 30 minutes")
    except Exception as e:
        logger.error(f"❌ 06:00 automation error: {e}")

def main():
    """Main scheduler loop"""
    logger.info("🕐 Daily 06:00 Job Automation Scheduler Started")
    logger.info("📅 Will run weekdays at 06:00 (6:00 AM)")
    
    # Schedule the job for 06:00 on weekdays only
    schedule.every().monday.at("06:00").do(run_06_00_automation)
    schedule.every().tuesday.at("06:00").do(run_06_00_automation)
    schedule.every().wednesday.at("06:00").do(run_06_00_automation)
    schedule.every().thursday.at("06:00").do(run_06_00_automation)
    schedule.every().friday.at("06:00").do(run_06_00_automation)
    
    # Also allow manual trigger for testing
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--test":
        logger.info("🧪 Running test automation now...")
        run_06_00_automation()
        return
    
    logger.info("⏰ Scheduler is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")

if __name__ == "__main__":
    main()