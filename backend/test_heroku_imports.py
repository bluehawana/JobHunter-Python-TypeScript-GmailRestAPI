#!/usr/bin/env python3
"""
Test script to check if all imports work correctly for Heroku deployment
"""
import sys
import os
from pathlib import Path

print("🔍 Testing Heroku app imports...")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    print("✅ Testing FastAPI import...")
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    print("✅ Testing uvicorn import...")
    import uvicorn
    print("✅ uvicorn imported successfully")
    
    print("✅ Testing scheduler imports...")
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz
    print("✅ Scheduler imports successful")
    
    print("✅ Testing master orchestrator import...")
    from master_automation_orchestrator import MasterAutomationOrchestrator
    print("✅ Master orchestrator imported successfully")
    
    print("✅ Testing orchestrator initialization...")
    orchestrator = MasterAutomationOrchestrator()
    print("✅ Orchestrator initialized successfully")
    
    print("🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)