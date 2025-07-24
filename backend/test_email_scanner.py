#!/usr/bin/env python3
"""
Test script for email scanner service
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

# Set environment variables for testing
os.environ['SMTP_USER'] = 'bluehawana@gmail.com'
os.environ['SMTP_PASSWORD'] = 'irlgwloknosqdut'

from app.services.email_scanner_service import EmailScannerService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_email_scanner():
    """Test the email scanner service"""
    try:
        logger.info("Testing email scanner service...")
        
        # Initialize email scanner
        scanner = EmailScannerService()
        
        # Scan for job emails from the last 7 days (for testing)
        job_opportunities = await scanner.scan_job_emails(days_back=7)
        
        logger.info(f"Found {len(job_opportunities)} job opportunities")
        
        # Display results
        for i, job in enumerate(job_opportunities[:5], 1):  # Show first 5
            logger.info(f"\nJob {i}:")
            logger.info(f"  Title: {job.get('title', 'N/A')}")
            logger.info(f"  Company: {job.get('company', 'N/A')}")
            logger.info(f"  Source: {job.get('source', 'N/A')}")
            logger.info(f"  Location: {job.get('location', 'N/A')}")
            logger.info(f"  URL: {job.get('url', 'N/A')}")
            logger.info(f"  Remote: {job.get('remote_option', False)}")
        
        if len(job_opportunities) > 5:
            logger.info(f"\n... and {len(job_opportunities) - 5} more jobs")
        
        return job_opportunities
        
    except Exception as e:
        logger.error(f"Error testing email scanner: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    asyncio.run(test_email_scanner())