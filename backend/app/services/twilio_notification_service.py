#!/usr/bin/env python3
"""
Twilio SMS Notification Service for JobHunter Automation
Sends SMS alerts for job processing status
"""
import os
import logging
from typing import Optional
from twilio.rest import Client
from datetime import datetime

logger = logging.getLogger(__name__)

class TwilioNotificationService:
    """SMS notification service using Twilio"""
    
    def __init__(self):
        # Twilio configuration
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.to_number = os.getenv('USER_PHONE_NUMBER', '+46728384299')
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
            logger.info("✅ Twilio SMS service initialized")
        else:
            self.client = None
            self.enabled = False
            logger.warning("⚠️ Twilio credentials not found, SMS notifications disabled")
    
    async def send_daily_scan_complete(self, jobs_found: int, applications_sent: int) -> bool:
        """Send notification when daily scan completes"""
        message = f"✅ JobHunter Daily Scan Complete!\n📧 Found: {jobs_found} jobs\n📤 Sent: {applications_sent} applications\nCheck leeharvad@gmail.com for details."
        return await self._send_sms(message)
    
    async def send_urgent_job_alert(self, job_title: str, company: str) -> bool:
        """Send urgent job alert"""
        message = f"🚨 URGENT JOB ALERT!\n🏢 {company}\n💼 {job_title}\n📄 Customized application generated and sent!\nTime: {datetime.now().strftime('%H:%M')}"
        return await self._send_sms(message)
    
    async def send_volvo_energy_alert(self) -> bool:
        """Send specific alert for Volvo Energy positions"""
        message = f"🚗⚡ VOLVO ENERGY ALERT!\n🎯 IT Support position detected\n📄 Tailored resume & cover letter sent\n⏰ {datetime.now().strftime('%H:%M')}\nCheck email immediately!"
        return await self._send_sms(message)
    
    async def send_system_error(self, error_type: str) -> bool:
        """Send system error notification"""
        message = f"❌ JobHunter System Error\n🔧 Type: {error_type}\n⏰ {datetime.now().strftime('%H:%M')}\nCheck logs for details."
        return await self._send_sms(message)
    
    async def send_claude_api_success(self, jobs_processed: int) -> bool:
        """Send notification when Claude API is working"""
        message = f"🤖 Claude AI Active!\n✨ {jobs_processed} jobs processed with AI customization\n📄 Premium tailored applications sent"
        return await self._send_sms(message)
    
    async def send_weekly_summary(self, total_jobs: int, total_applications: int) -> bool:
        """Send weekly summary"""
        message = f"📊 Weekly JobHunter Summary\n🔍 Jobs found: {total_jobs}\n📤 Applications sent: {total_applications}\n🎯 Keep hunting!"
        return await self._send_sms(message)
    
    async def _send_sms(self, message: str) -> bool:
        """Internal method to send SMS"""
        if not self.enabled:
            logger.warning("📱 SMS disabled - would send: " + message[:50] + "...")
            return False
        
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            logger.info(f"📱 SMS sent successfully: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ SMS send failed: {e}")
            return False
    
    def is_enabled(self) -> bool:
        """Check if SMS service is enabled"""
        return self.enabled