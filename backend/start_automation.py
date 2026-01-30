#!/usr/bin/env python3
"""
JobHunter Fully Automated System Startup
Completely hands-off job hunting with webhooks and notifications
"""
import os
import sys
import subprocess
import asyncio
from pathlib import Path

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    # Load .env file
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print("✅ Environment file found")
        return True
    else:
        print("❌ .env file not found")
        return False

def start_api_server():
    """Start the FastAPI server with webhooks"""
    print("🚀 Starting API server with webhook endpoints...")
    
    try:
        # Start FastAPI server in background
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], cwd=Path(__file__).parent)
        
        print("✅ API server started on http://localhost:8000")
        print("📡 Webhook endpoints available:")
        print("   • POST /api/v1/webhooks/trigger/daily-job-scan")
        print("   • POST /api/v1/webhooks/trigger/process-job")
        print("   • POST /api/v1/webhooks/trigger/gmail-scan")
        print("   • POST /api/v1/webhooks/trigger/emergency-job-alert")
        print("   • GET  /api/v1/webhooks/status/automation")
        
        return api_process
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def start_scheduler():
    """Start the automated scheduler"""
    print("⏰ Starting automated scheduler...")
    
    try:
        scheduler_process = subprocess.Popen([
            sys.executable, "automation/automated_scheduler.py"
        ], cwd=Path(__file__).parent)
        
        print("✅ Automated scheduler started")
        print("📅 Schedule:")
        print("   • Daily job scan: 06:00 Stockholm time")
        print("   • Hourly urgent checks")
        print("   • Weekly summary: Sunday 18:00")
        
        return scheduler_process
        
    except Exception as e:
        print(f"❌ Failed to start scheduler: {e}")
        return None

def display_automation_info():
    """Display automation setup information"""
    print("\n" + "="*60)
    print("🤖 JOBHUNTER FULLY AUTOMATED SYSTEM")
    print("="*60)
    print("✅ COMPLETELY HANDS-OFF OPERATION")
    print()
    print("📧 Email Scanning:")
    print("   • Monitors bluehawana@gmail.com automatically")
    print("   • Detects LinkedIn, Indeed, Glassdoor job alerts")
    print("   • Processes Volvo Energy positions with priority")
    print()
    print("📄 Document Generation:")
    print("   • AI-powered CV customization (when Claude API available)")
    print("   • Tailored cover letters for each position")
    print("   • Professional LaTeX templates")
    print("   • ATS-optimized content")
    print()
    print("📤 Application Delivery:")
    print("   • Automatic email to leeharvad@gmail.com")
    print("   • PDF attachments (CV + Cover Letter)")
    print("   • Job details and application links")
    print("   • Professional email formatting")
    print()
    print("📱 Notifications:")
    print("   • SMS alerts for urgent jobs (if Twilio configured)")
    print("   • Daily scan completion notifications")
    print("   • Weekly summary reports")
    print()
    print("🔗 Integration Options:")
    print("   • n8n workflows (see automation/n8n_workflows.json)")
    print("   • Zapier webhooks")
    print("   • Twilio SMS notifications")
    print("   • Custom webhook triggers")
    print()
    print("🎯 ZERO MANUAL INTERVENTION REQUIRED")
    print("="*60)

def main():
    """Main startup function"""
    display_automation_info()
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return
    
    print("\n🚀 Starting JobHunter Automation System...")
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server")
        return
    
    # Start scheduler
    scheduler_process = start_scheduler()
    if not scheduler_process:
        print("❌ Failed to start scheduler")
        api_process.terminate()
        return
    
    print("\n✅ AUTOMATION SYSTEM FULLY OPERATIONAL")
    print("🎯 Your job applications will be processed automatically")
    print("📧 Check leeharvad@gmail.com for tailored applications")
    print("📱 SMS notifications will keep you informed")
    print()
    print("🔧 Integration URLs:")
    print("   • n8n: http://localhost:8000/api/v1/webhooks/trigger/daily-job-scan")
    print("   • Zapier: http://localhost:8000/api/v1/webhooks/trigger/process-job")
    print("   • Status: http://localhost:8000/api/v1/webhooks/status/automation")
    print()
    print("Press Ctrl+C to stop the automation system")
    
    try:
        # Keep running until interrupted
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping automation system...")
        
        if api_process:
            api_process.terminate()
            print("✅ API server stopped")
        
        if scheduler_process:
            scheduler_process.terminate()
            print("✅ Scheduler stopped")
        
        print("👋 JobHunter automation system stopped")

if __name__ == "__main__":
    main()