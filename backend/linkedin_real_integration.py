#!/usr/bin/env python3
"""
Real LinkedIn Integration for Saved Jobs
Uses your LinkedIn API credentials to fetch actual saved jobs
"""
import asyncio
import aiohttp
import json
import os
from typing import List, Dict, Optional
from claude_final_system import ClaudeFinalSystem

class LinkedInRealIntegration:
    def __init__(self):
        # LinkedIn API credentials - You need to set these environment variables
        self.client_id = "77duha47hcbh8o"  # Your LinkedIn Client ID from the code
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")  # You need to provide this
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")    # You need to provide this
        
        # Claude system for processing jobs
        self.claude_system = ClaudeFinalSystem()
        
        # LinkedIn API endpoints
        self.base_url = "https://api.linkedin.com/v2"
        
        if not self.client_secret or not self.access_token:
            print("⚠️  LinkedIn credentials missing!")
            print("Please set these environment variables:")
            print("export LINKEDIN_CLIENT_SECRET='your_linkedin_client_secret'")
            print("export LINKEDIN_ACCESS_TOKEN='your_linkedin_access_token'")
            print()
            print("🔗 How to get LinkedIn API credentials:")
            print("1. Go to https://www.linkedin.com/developers/")
            print("2. Create an app for job searching")
            print("3. Get your Client Secret and Access Token")
            print("4. Set the environment variables above")
            print()
    
    async def fetch_saved_jobs(self) -> List[Dict]:
        """Fetch saved jobs from LinkedIn API"""
        
        if not self.access_token:
            print("❌ LinkedIn access token not configured")
            return []
        
        print("🔗 Fetching saved jobs from LinkedIn API...")
        
        # LinkedIn API endpoint for saved jobs (this might need adjustment based on actual API)
        url = f"{self.base_url}/people/~/saved-jobs"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        jobs = self.parse_saved_jobs_response(data)
                        print(f"✅ Found {len(jobs)} saved jobs from LinkedIn")
                        return jobs
                    elif response.status == 401:
                        print("❌ LinkedIn authentication failed - check your access token")
                        return []
                    elif response.status == 403:
                        print("❌ LinkedIn API access forbidden - check permissions")
                        return []
                    else:
                        error_text = await response.text()
                        print(f"❌ LinkedIn API error {response.status}: {error_text}")
                        return []
                        
        except Exception as e:
            print(f"❌ Error fetching LinkedIn saved jobs: {e}")
            return []
    
    def parse_saved_jobs_response(self, data: Dict) -> List[Dict]:
        """Parse LinkedIn saved jobs API response"""
        
        jobs = []
        elements = data.get("elements", [])
        
        for element in elements:
            try:
                job_data = element.get("job", {})
                if not job_data:
                    continue
                
                job = {
                    "job_title": job_data.get("title", ""),
                    "company": self.extract_company_name(job_data),
                    "location": job_data.get("formattedLocation", ""),
                    "job_description": self.extract_job_description(job_data),
                    "job_link": self.extract_job_url(job_data),
                    "posted_date": job_data.get("listedAt"),
                    "saved_date": element.get("savedAt"),
                    "priority": self.determine_job_priority(job_data),
                    "source": "linkedin_saved"
                }
                
                if job["job_title"] and job["company"]:
                    jobs.append(job)
                    
            except Exception as e:
                print(f"⚠️ Error parsing saved job: {e}")
                continue
        
        return jobs
    
    def extract_company_name(self, job_data: Dict) -> str:
        """Extract company name from LinkedIn job data"""
        company_info = job_data.get("companyDetails", {})
        if isinstance(company_info, dict):
            company = company_info.get("company", {})
            if isinstance(company, dict):
                return company.get("name", "Unknown Company")
            elif isinstance(company, str):
                return company
        return "Unknown Company"
    
    def extract_job_description(self, job_data: Dict) -> str:
        """Extract job description from LinkedIn job data"""
        description = job_data.get("description", {})
        if isinstance(description, dict):
            return description.get("text", "No description available")
        elif isinstance(description, str):
            return description
        return "No description available"
    
    def extract_job_url(self, job_data: Dict) -> str:
        """Extract job URL from LinkedIn job data"""
        job_id = job_data.get("id") or job_data.get("jobPostingId")
        if job_id:
            return f"https://www.linkedin.com/jobs/view/{job_id}"
        return ""
    
    def determine_job_priority(self, job_data: Dict) -> str:
        """Determine job priority based on location and company"""
        location = job_data.get("formattedLocation", "").lower()
        company = self.extract_company_name(job_data).lower()
        
        # High priority: Gothenburg jobs
        if "gothenburg" in location or "göteborg" in location:
            return "high"
        
        # High priority: Famous remote companies
        famous_companies = [
            "spotify", "volvo", "ericsson", "king", "opera", "skype", 
            "google", "microsoft", "apple", "amazon", "meta", "netflix"
        ]
        
        if any(famous in company for famous in famous_companies):
            return "high"
        
        return "medium"
    
    async def process_saved_jobs(self) -> Dict:
        """Process all LinkedIn saved jobs with Claude system"""
        
        print("🚀 LinkedIn Saved Jobs Processing with Claude")
        print("=" * 60)
        
        # Fetch saved jobs from LinkedIn
        saved_jobs = await self.fetch_saved_jobs()
        
        if not saved_jobs:
            print("❌ No saved jobs found")
            return {"processed": 0, "successful": 0, "failed": 0}
        
        print(f"📋 Processing {len(saved_jobs)} saved jobs with improved Claude system")
        print()
        
        results = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "jobs": []
        }
        
        # Sort by priority (high priority first)
        saved_jobs.sort(key=lambda x: 0 if x["priority"] == "high" else 1)
        
        for i, job in enumerate(saved_jobs, 1):
            job_title = job["job_title"]
            company = job["company"]
            job_description = job["job_description"]
            job_link = job["job_link"]
            priority = job["priority"]
            
            print(f"📋 Processing {i}/{len(saved_jobs)}: {job_title} at {company}")
            print(f"🎯 Priority: {priority}")
            print(f"🔗 {job_link}")
            print("-" * 50)
            
            try:
                success = await self.claude_system.process_job_application(
                    job_title, company, job_description, job_link
                )
                
                results["processed"] += 1
                if success:
                    results["successful"] += 1
                    print(f"✅ SUCCESS: {job_title} at {company}")
                else:
                    results["failed"] += 1
                    print(f"❌ FAILED: {job_title} at {company}")
                
                results["jobs"].append({
                    "job_title": job_title,
                    "company": company,
                    "priority": priority,
                    "success": success
                })
                
            except Exception as e:
                print(f"❌ ERROR: {e}")
                results["failed"] += 1
                results["jobs"].append({
                    "job_title": job_title,
                    "company": company,
                    "priority": priority,
                    "success": False
                })
            
            print()
            await asyncio.sleep(3)  # Delay between jobs
        
        return results
    
    def print_results_summary(self, results: Dict):
        """Print processing results summary"""
        
        print("📊 LINKEDIN SAVED JOBS PROCESSING COMPLETE!")
        print("=" * 60)
        print(f"📋 Total Jobs: {results['processed']}")
        print(f"✅ Successful: {results['successful']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"📧 Check leeharvad@gmail.com for applications!")
        print()
        
        print("🎯 Jobs by Priority:")
        high_priority = [j for j in results["jobs"] if j["priority"] == "high"]
        medium_priority = [j for j in results["jobs"] if j["priority"] == "medium"]
        
        print(f"  🔥 High Priority: {len(high_priority)}")
        for job in high_priority:
            status = "✅" if job["success"] else "❌"
            print(f"    {status} {job['job_title']} at {job['company']}")
        
        print(f"  📋 Medium Priority: {len(medium_priority)}")
        for job in medium_priority:
            status = "✅" if job["success"] else "❌"
            print(f"    {status} {job['job_title']} at {job['company']}")
        
        print()
        print("🎯 Each application includes:")
        print("  ✅ Swedish B2 + driving licenses")
        print("  ✅ AKS migration (60% cost reduction) for DevOps roles")
        print("  ✅ Role-specific project highlights")
        print("  ✅ Powerful persuasive cover letters")
        print("  ✅ 90%+ ATS optimization")

async def main():
    """Main function to process LinkedIn saved jobs"""
    
    integration = LinkedInRealIntegration()
    
    if not integration.client_secret or not integration.access_token:
        print("❌ Cannot proceed without LinkedIn credentials")
        print()
        print("📋 What you need to do:")
        print("1. Get LinkedIn API credentials from https://www.linkedin.com/developers/")
        print("2. Set environment variables:")
        print("   export LINKEDIN_CLIENT_SECRET='your_secret'")
        print("   export LINKEDIN_ACCESS_TOKEN='your_token'")
        print("3. Run this script again")
        return
    
    # Process all saved jobs
    results = await integration.process_saved_jobs()
    
    # Print summary
    integration.print_results_summary(results)

if __name__ == "__main__":
    asyncio.run(main())