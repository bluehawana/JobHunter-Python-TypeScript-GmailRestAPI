#!/usr/bin/env python3
"""
Test script to verify Heroku deployment is working correctly
"""
import requests
import json
import time

def test_heroku_app(app_url):
    """Test the deployed Heroku app"""
    print(f"🧪 Testing Heroku deployment: {app_url}")
    print("=" * 50)
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{app_url}/health", timeout=30)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   📊 Scheduler running: {health_data.get('scheduler_running')}")
            print(f"   📅 Next run: {health_data.get('next_run')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(app_url, timeout=30)
        if response.status_code == 200:
            root_data = response.json()
            print(f"   ✅ Root endpoint working")
            print(f"   📅 Schedule: {root_data.get('schedule')}")
            print(f"   🌍 Timezone: {root_data.get('timezone')}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test 3: Scheduled jobs status
        print("\n3. Testing scheduled jobs...")
        response = requests.get(f"{app_url}/status/next-jobs", timeout=30)
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"   ✅ Scheduled jobs endpoint working")
            print(f"   📋 Jobs scheduled: {len(jobs_data.get('scheduled_jobs', []))}")
            for job in jobs_data.get('scheduled_jobs', []):
                print(f"      - {job.get('name')}: {job.get('next_run')}")
        else:
            print(f"   ❌ Scheduled jobs failed: {response.status_code}")
            return False
        
        # Test 4: Manual trigger (optional - only if you want to test)
        print("\n4. Manual trigger test (skipped - would start automation)")
        print("   ℹ️  To test manual trigger: POST /trigger/manual-run")
        
        print("\n🎉 All tests passed! Heroku deployment is working correctly.")
        print(f"📅 Your automation will run automatically Monday-Friday at 6:00 AM Stockholm time")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main test function"""
    # Replace with your actual Heroku app URL
    app_url = input("Enter your Heroku app URL (e.g., https://jobhunter-lego-system.herokuapp.com): ").strip()
    
    if not app_url:
        print("❌ Please provide a valid Heroku app URL")
        return
    
    # Remove trailing slash if present
    app_url = app_url.rstrip('/')
    
    # Run tests
    success = test_heroku_app(app_url)
    
    if success:
        print(f"\n✅ Deployment test completed successfully!")
        print(f"🔗 Your app is live at: {app_url}")
        print(f"📊 Monitor at: https://dashboard.heroku.com/apps/{app_url.split('/')[-1].split('.')[0]}")
    else:
        print(f"\n❌ Deployment test failed. Check your Heroku logs:")
        print(f"   heroku logs --tail --app {app_url.split('/')[-1].split('.')[0]}")

if __name__ == "__main__":
    main()