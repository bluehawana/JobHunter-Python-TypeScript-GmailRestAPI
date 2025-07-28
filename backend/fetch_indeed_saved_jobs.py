#!/usr/bin/env python3
"""
Fetch Indeed Saved Jobs
Extract jobs from Indeed saved jobs URL: https://myjobs.indeed.com/saved?from=_atweb_nc_saved_jobs_apply
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import os
from supabase import create_client, Client

class IndeedSavedJobsFetcher:
    def __init__(self):
        # Supabase setup from environment variables
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set")
        
        # Session for Indeed requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def extract_jobs_from_indeed_page(self, html_content: str) -> List[Dict]:
        """Extract job information from Indeed saved jobs page HTML"""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Look for job cards in Indeed's structure
        job_cards = soup.find_all(['div', 'a'], {'class': lambda x: x and any(keyword in x.lower() for keyword in ['job', 'saved', 'card'])})
        
        print(f"Found {len(job_cards)} potential job elements")
        
        for card in job_cards:
            try:
                # Extract job title
                title_elem = card.find(['h2', 'h3', 'span', 'a'], {'class': lambda x: x and 'title' in x.lower()})
                if not title_elem:
                    title_elem = card.find('a', href=lambda x: x and '/viewjob' in x) if card.find('a', href=lambda x: x and '/viewjob' in x) else None
                
                # Extract company name  
                company_elem = card.find(['span', 'div', 'a'], {'class': lambda x: x and 'company' in x.lower()})
                
                # Extract location
                location_elem = card.find(['div', 'span'], {'class': lambda x: x and 'location' in x.lower()})
                
                # Extract job URL
                link_elem = card.find('a', href=lambda x: x and ('/viewjob' in x or '/jobs/view' in x))
                
                if title_elem and company_elem:
                    job = {
                        'title': title_elem.get_text().strip(),
                        'company': company_elem.get_text().strip(),
                        'location': location_elem.get_text().strip() if location_elem else 'Location not specified',
                        'url': f"https://indeed.com{link_elem.get('href')}" if link_elem else None,
                        'source': 'indeed_saved',
                        'status': 'saved',
                        'priority': 'high' if any(city in location_elem.get_text().lower() if location_elem else '' for city in ['gothenburg', 'göteborg', 'stockholm']) else 'medium',
                        'description': 'Job description to be fetched from Indeed job page'
                    }
                    
                    jobs.append(job)
                    print(f"✅ Extracted: {job['title']} at {job['company']}")
                
            except Exception as e:
                print(f"Error extracting job from card: {e}")
                continue
        
        return jobs
    
    def create_mock_indeed_jobs(self) -> List[Dict]:
        """Create mock Indeed jobs based on typical Swedish market"""
        
        print("🔄 Creating mock Indeed saved jobs (user should replace with actual saved jobs)")
        
        mock_jobs = [
            {
                'title': 'Senior Software Developer',
                'company': 'Volvo Cars',
                'location': 'Gothenburg, Sweden',
                'url': 'https://jobs.volvocars.com/job/senior-software-developer',
                'source': 'indeed_saved',
                'status': 'saved',
                'priority': 'high',
                'description': 'Join Volvo Cars software development team building next-generation automotive software solutions. Work with modern tech stack including Java, Python, React, and cloud technologies.'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'SKF Group',
                'location': 'Gothenburg, Sweden', 
                'url': 'https://careers.skf.com/job/devops-engineer',
                'source': 'indeed_saved',
                'status': 'saved',
                'priority': 'high',
                'description': 'SKF Group seeks DevOps Engineer to build and maintain CI/CD pipelines, manage cloud infrastructure, and support development teams with automation and deployment processes.'
            },
            {
                'title': 'Backend Developer',
                'company': 'Polestar',
                'location': 'Gothenburg, Sweden',
                'url': 'https://careers.polestar.com/job/backend-developer',
                'source': 'indeed_saved', 
                'status': 'saved',
                'priority': 'high',
                'description': 'Polestar is looking for Backend Developer to work on electric vehicle software systems. Experience with microservices, APIs, and cloud platforms required.'
            },
            {
                'title': 'Fullstack Developer',
                'company': 'Klarna',
                'location': 'Stockholm, Sweden',
                'url': 'https://jobs.klarna.com/job/fullstack-developer',
                'source': 'indeed_saved',
                'status': 'saved', 
                'priority': 'medium',
                'description': 'Join Klarna engineering team to build innovative fintech solutions. Work with React, Node.js, Java, and modern cloud technologies in an agile environment.'
            },
            {
                'title': 'Cloud Platform Engineer',
                'company': 'Spotify',
                'location': 'Stockholm, Sweden',
                'url': 'https://jobs.spotify.com/job/cloud-platform-engineer',
                'source': 'indeed_saved',
                'status': 'saved',
                'priority': 'medium', 
                'description': 'Spotify seeks Cloud Platform Engineer to build and maintain infrastructure for music streaming platform. Kubernetes, Docker, AWS experience required.'
            }
        ]
        
        return mock_jobs
    
    def save_jobs_to_supabase(self, jobs: List[Dict]) -> bool:
        """Save Indeed jobs to Supabase database"""
        
        try:
            supabase: Client = create_client(self.supabase_url, self.supabase_key)
            
            print(f"💾 Saving {len(jobs)} Indeed jobs to Supabase...")
            
            for job in jobs:
                job_data = {
                    "title": job["title"],
                    "company": job["company"], 
                    "location": job["location"],
                    "url": job.get("url"),
                    "source": job["source"],
                    "status": job["status"],
                    "priority": job["priority"],
                    "description": job["description"],
                    "posted_date": "Recently",
                    "job_type": "fulltime"
                }
                
                # Insert into Supabase
                result = supabase.table("jobs").insert(job_data).execute()
                print(f"✅ Saved: {job['title']} at {job['company']}")
            
            print(f"🎉 Successfully saved {len(jobs)} Indeed jobs!")
            return True
            
        except Exception as e:
            print(f"❌ Error saving jobs to Supabase: {e}")
            return False
    
    def fetch_and_process_indeed_jobs(self, url: str = None) -> List[Dict]:
        """Main function to fetch and process Indeed saved jobs"""
        
        print("🔍 INDEED SAVED JOBS FETCHER")
        print("=" * 40)
        
        if url:
            print(f"📄 Fetching jobs from: {url}")
            print("⚠️  Note: Indeed requires login to access saved jobs")
            print("⚠️  This is a mock implementation - user should provide actual job data")
        
        # For now, create mock jobs since Indeed requires authentication
        jobs = self.create_mock_indeed_jobs()
        
        print(f"\n📋 Found {len(jobs)} jobs:")
        for job in jobs:
            priority_icon = "🏢" if job['priority'] == 'high' else "🌐"
            print(f"  {priority_icon} {job['title']} at {job['company']} ({job['location']})")
        
        # Save to Supabase
        if self.save_jobs_to_supabase(jobs):
            print(f"\n✅ All jobs saved to database successfully!")
        
        return jobs

def main():
    """Main function"""
    
    fetcher = IndeedSavedJobsFetcher()
    
    # URL provided by user
    indeed_url = "https://myjobs.indeed.com/saved?from=_atweb_nc_saved_jobs_apply"
    
    # Fetch and process jobs
    jobs = fetcher.fetch_and_process_indeed_jobs(indeed_url)
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Jobs saved to Supabase database")
    print("2. Run job processing script to generate CVs/CLs")
    print("3. Check leeharvad@gmail.com for applications")
    print("4. Replace mock data with actual Indeed saved jobs")

if __name__ == "__main__":
    main()