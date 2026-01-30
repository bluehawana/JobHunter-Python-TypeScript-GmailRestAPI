#!/usr/bin/env python3
"""
Quick launcher for processing DevOps jobs with enhanced AI system
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

async def main():
    """Quick launcher"""
    
    print("🚀 LAUNCHING DEVOPS JOB PROCESSOR")
    print("🤖 Enhanced AI-Powered CV/CL System")
    print("=" * 50)
    
    try:
        # Import the processor
        from process_indeed_devops_jobs import IndeedDevOpsProcessor
        
        processor = IndeedDevOpsProcessor()
        
        # Get DevOps jobs (will use examples if no saved jobs found)
        jobs = await processor.get_saved_indeed_jobs()
        
        print(f"📋 Found {len(jobs)} DevOps positions:")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['title']} at {job['company']} ({job['location']})")
        
        # Ask user if they want to proceed
        proceed = input(f"\n🤖 Process these {len(jobs)} jobs with AI system? (y/n): ").lower()
        
        if proceed != 'y':
            print("👋 Processing cancelled")
            return
        
        # Process with smart system
        print("\n🚀 Processing jobs with Smart CV System...")
        results = await processor.process_devops_jobs_with_smart_system(jobs)
        
        # Analyze keywords
        keyword_analysis = await processor.analyze_devops_market_keywords(jobs)
        
        # Generate and display report
        report = processor.generate_processing_report(results, keyword_analysis)
        processor.print_processing_summary(report)
        
        # Save results
        await processor.save_results_to_database(report)
        
        print("\n✅ PROCESSING COMPLETE!")
        print("📧 Check leeharvad@gmail.com for optimized CV/CL documents")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Make sure Supabase credentials are set")
        print("2. Install required packages: pip install -r requirements.txt")
        print("3. Check that all service files are present")

if __name__ == "__main__":
    asyncio.run(main())