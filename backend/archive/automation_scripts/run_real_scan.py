#!/usr/bin/env python3
"""
Run Real Email Scanning for Job Opportunities

This script will scan your actual Gmail account for job opportunities
and process them with customized documents.

Usage: python run_real_scan.py
"""

import os
import sys
import asyncio

def main():
    """Main function to run real email scanning"""
    print("🚀 REAL JOB OPPORTUNITY SCANNER")
    print("=" * 50)
    print("📧 Scanning bluehawana@gmail.com for actual job emails")
    print("🎯 Looking for IT support at Volvo Energy and other opportunities")
    print("📤 Will send processed applications to leeharvad@gmail.com")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('app'):
        print("❌ Please run this script from the backend directory")
        print("💡 Try: cd backend && python run_real_scan.py")
        return
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("💡 Make sure your email credentials are configured in .env")
        return
    
    try:
        # Import and run the real scanner
        from real_email_scan_and_process import main as scan_main
        
        print("🏃 Starting real email scan...")
        print()
        
        # Run the async scanner
        asyncio.run(scan_main())
        
    except KeyboardInterrupt:
        print("\\n⏹️  Scan interrupted by user")
    except Exception as e:
        print(f"❌ Error running scanner: {e}")
        print("💡 Check your email credentials and internet connection")

if __name__ == "__main__":
    main()