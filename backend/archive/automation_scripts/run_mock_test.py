#!/usr/bin/env python3
"""
Simple script to run the mock test for job application automation

This script will:
1. Set up the environment
2. Run the complete workflow mock test
3. Show results

Usage: python run_mock_test.py
"""

import os
import sys
import asyncio
import subprocess

def setup_environment():
    """Set up the environment for the mock test"""
    print("🔧 Setting up environment...")
    
    # Check if we're in the backend directory
    if not os.path.exists('app'):
        print("❌ Please run this script from the backend directory")
        return False
    
    # Check if required files exist
    required_files = [
        'app/services/email_scanner_service.py',
        'app/services/job_application_processor.py',
        'app/services/latex_resume_service.py'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file not found: {file_path}")
            return False
    
    print("✅ Environment setup complete")
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("🚀 JOB APPLICATION AUTOMATION - MOCK TEST")
    print("=" * 60)
    print()
    print("This test will simulate the complete workflow:")
    print("1. 📧 Scan bluehawana@gmail.com for LinkedIn job emails")
    print("2. 🔍 Find newest job spots with 'LinkedIn Jobs' title")
    print("3. 📄 Generate customized resume and cover letter in LaTeX")
    print("4. 📎 Convert to PDF files")
    print("5. 📤 Send to leeharvad@gmail.com with job details")
    print()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Run the mock test
    try:
        print("🏃 Running mock test...")
        print()
        
        # Import and run the mock test
        from mock_test_complete_workflow import mock_test_complete_workflow
        
        # Run the async function
        result = asyncio.run(mock_test_complete_workflow())
        
        if result:
            print()
            print("=" * 60)
            print("🎉 MOCK TEST COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print()
            print("📧 Check leeharvad@gmail.com for the job application emails")
            print("📎 Each email contains customized CV and cover letter PDFs")
            print("🔗 Application links are included for easy access")
            print()
            print("💡 You can now decide how to proceed with each application!")
        else:
            print()
            print("❌ Mock test failed. Check the logs above for details.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error running mock test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()