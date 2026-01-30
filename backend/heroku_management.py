#!/usr/bin/env python3
"""
Heroku JobHunter Management Scripts
Monitor and control your automated job hunting system
"""
import requests
import json
from datetime import datetime

class HerokuJobHunterManager:
    """Manage your Heroku JobHunter LEGO System"""
    
    def __init__(self, app_url="https://jobhunter-lego-system.herokuapp.com"):
        self.app_url = app_url
    
    def check_status(self):
        """Check system status"""
        try:
            response = requests.get(f"{self.app_url}/health")
            if response.status_code == 200:
                data = response.json()
                print("🟢 JobHunter LEGO System Status: HEALTHY")
                print(f"📅 Next scheduled run: {data.get('next_run', 'Not scheduled')}")
                print(f"⏰ Stockholm time: {data.get('stockholm_time', 'Unknown')}")
                print(f"🔧 Scheduler running: {data.get('scheduler_running', False)}")
                return True
            else:
                print(f"🔴 System Status: ERROR ({response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to system: {e}")
            return False
    
    def trigger_manual_run(self):
        """Trigger manual job hunting run"""
        try:
            response = requests.post(f"{self.app_url}/trigger/manual-run")
            if response.status_code == 200:
                print("🚀 Manual job hunting triggered successfully!")
                print("📧 Check hongzhili01@gmail.com for results in a few minutes")
                return True
            else:
                print(f"❌ Failed to trigger manual run: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error triggering manual run: {e}")
            return False
    
    def get_scheduled_jobs(self):
        """Get information about scheduled jobs"""
        try:
            response = requests.get(f"{self.app_url}/status/next-jobs")
            if response.status_code == 200:
                data = response.json()
                print("📅 Scheduled Jobs:")
                for job in data.get('scheduled_jobs', []):
                    print(f"   • {job['name']}: {job.get('next_run', 'Not scheduled')}")
                return data
            else:
                print(f"❌ Failed to get scheduled jobs: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting scheduled jobs: {e}")
            return None

def main():
    """Main management interface"""
    print("🧩 JobHunter LEGO System - Heroku Management")
    print("=" * 50)
    
    manager = HerokuJobHunterManager()
    
    while True:
        print("\n📋 Available Commands:")
        print("1. Check system status")
        print("2. Trigger manual job hunt")
        print("3. View scheduled jobs")
        print("4. Exit")
        
        choice = input("\n🔧 Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🔍 Checking system status...")
            manager.check_status()
        
        elif choice == "2":
            print("\n🚀 Triggering manual job hunt...")
            manager.trigger_manual_run()
        
        elif choice == "3":
            print("\n📅 Getting scheduled jobs...")
            manager.get_scheduled_jobs()
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()