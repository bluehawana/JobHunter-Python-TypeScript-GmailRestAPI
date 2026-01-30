#!/usr/bin/env python3
"""
Simple launcher for the complete job hunting automation
Single command to run everything: python run_complete_automation.py
"""
import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def main():
    """Simple main function to launch the master orchestrator"""
    print("🚀 Starting Complete Job Hunting Automation...")
    print("📧 This will scan Gmail, process jobs, generate PDFs, and send applications")
    print()
    
    try:
        # Import and run the master orchestrator
        from master_automation_orchestrator import main as run_orchestrator
        asyncio.run(run_orchestrator())
        
    except KeyboardInterrupt:
        print("\n⏹️  Automation stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()