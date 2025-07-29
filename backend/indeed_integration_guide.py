#!/usr/bin/env python3
"""
Indeed Integration Guide and Helper
Multiple approaches to integrate your Indeed saved jobs with the Smart CV system
"""
import json
import asyncio
from datetime import datetime
from typing import List, Dict

class IndeedIntegrationGuide:
    """Guide for integrating Indeed saved jobs with Smart CV system"""
    
    def __init__(self):
        self.integration_methods = {
            'method_1': 'Manual Copy-Paste from Browser',
            'method_2': 'Browser Extension/Bookmarklet',
            'method_3': 'CSV Upload Method',
            'method_4': 'API Integration (if available)'
        }
    
    def print_integration_options(self):
        """Print all available integration methods"""
        
        print("🔗 INDEED SAVED JOBS INTEGRATION GUIDE")
        print("="*50)
        print("\nSince Indeed requires authentication, here are your options:\n")
        
        print("📋 METHOD 1: MANUAL COPY-PASTE (Recommended)")
        print("-" * 40)
        print("1. Go to: https://myjobs.indeed.com/saved")
        print("2. Copy job details (title, company, description)")
        print("3. Use the manual_job_input() function below")
        print("4. Our system will process with AI optimization")
        
        print("\n🌐 METHOD 2: BROWSER BOOKMARKLET")
        print("-" * 40)
        print("1. Add bookmarklet to extract job data")
        print("2. Click bookmarklet on Indeed saved jobs page")
        print("3. Copy generated JSON")
        print("4. Import into our system")
        
        print("\n📊 METHOD 3: CSV/JSON EXPORT")
        print("-" * 40)
        print("1. Manually create CSV with job details")
        print("2. Use csv_import() function")
        print("3. Batch process all jobs")
        
        print("\n🔧 METHOD 4: BROWSER AUTOMATION")
        print("-" * 40)
        print("1. Use selenium to automate browser")
        print("2. Login to Indeed automatically")
        print("3. Scrape saved jobs data")
        print("4. Process with Smart CV system")
        
        print("\n" + "="*50)
        print("💡 RECOMMENDATION: Start with Method 1 (Manual) for immediate results")
        print("="*50)
    
    def manual_job_input(self):
        """Interactive manual job input"""
        
        print("\n🖊️  MANUAL JOB INPUT")
        print("-" * 30)
        print("Enter your Indeed saved jobs one by one:")
        print("(Press Enter with empty title to finish)\n")
        
        jobs = []
        job_count = 1
        
        while True:
            print(f"📋 JOB #{job_count}")
            title = input("Job Title: ").strip()
            
            if not title:
                break
                
            company = input("Company: ").strip()
            location = input("Location: ").strip()
            url = input("Job URL (optional): ").strip()
            
            print("Job Description (paste full description, then press Enter twice):")
            description_lines = []
            while True:
                line = input()
                if line == "":
                    break
                description_lines.append(line)
            
            description = "\n".join(description_lines)
            
            job = {
                'id': f'manual_indeed_{job_count}',
                'title': title,
                'company': company,
                'location': location,
                'url': url if url else f'https://indeed.com/manual_job_{job_count}',
                'description': description,
                'source': 'indeed_saved_manual',
                'job_type': 'fulltime',
                'remote_option': 'remote' in description.lower(),
                'posting_date': datetime.now(),
                'priority': 'high' if any(city in location.lower() for city in ['gothenburg', 'göteborg', 'stockholm']) else 'medium',
                'keywords': self._extract_basic_keywords(f"{title} {description}")
            }
            
            jobs.append(job)
            job_count += 1
            
            print(f"✅ Added: {title} at {company}")
            print("-" * 30)
        
        print(f"\n🎯 Total Jobs Added: {len(jobs)}")
        
        # Save to JSON file for processing
        filename = f"indeed_jobs_manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(jobs, f, indent=2, default=str)
        
        print(f"💾 Jobs saved to: {filename}")
        print("🚀 Run: python process_indeed_devops_jobs.py to process with Smart CV system")
        
        return jobs
    
    def _extract_basic_keywords(self, text: str) -> List[str]:
        """Extract basic keywords from job text"""
        
        text_lower = text.lower()
        
        # Common DevOps/Tech keywords
        keywords = []
        common_terms = [
            'python', 'java', 'javascript', 'go', 'bash',
            'kubernetes', 'docker', 'aws', 'azure', 'gcp',
            'terraform', 'ansible', 'jenkins', 'gitlab',
            'microservices', 'api', 'rest', 'graphql',
            'monitoring', 'grafana', 'prometheus',
            'ci/cd', 'devops', 'agile', 'scrum'
        ]
        
        for term in common_terms:
            if term in text_lower:
                keywords.append(term)
        
        return keywords[:10]  # Return top 10
    
    def create_bookmarklet_code(self) -> str:
        """Generate bookmarklet code for extracting Indeed job data"""
        
        bookmarklet = """
javascript:(function(){
    var jobs = [];
    var jobCards = document.querySelectorAll('[data-jk], .job_seen_beacon, .slider_container .slider_item');
    
    jobCards.forEach(function(card) {
        try {
            var titleEl = card.querySelector('h2 a, .jobTitle a, [data-testid="job-title"]');
            var companyEl = card.querySelector('.companyName, [data-testid="company-name"]');
            var locationEl = card.querySelector('.companyLocation, [data-testid="job-location"]');
            var linkEl = card.querySelector('h2 a, .jobTitle a');
            
            if (titleEl && companyEl) {
                jobs.push({
                    title: titleEl.innerText.trim(),
                    company: companyEl.innerText.trim(),
                    location: locationEl ? locationEl.innerText.trim() : 'Location not specified',
                    url: linkEl ? 'https://indeed.com' + linkEl.getAttribute('href') : '',
                    source: 'indeed_saved_bookmarklet',
                    extracted_at: new Date().toISOString()
                });
            }
        } catch(e) {
            console.log('Error extracting job:', e);
        }
    });
    
    if (jobs.length > 0) {
        var jsonData = JSON.stringify(jobs, null, 2);
        var newWindow = window.open();
        newWindow.document.write('<h3>Indeed Jobs Data</h3><pre>' + jsonData + '</pre>');
        newWindow.document.write('<br><button onclick="navigator.clipboard.writeText(\\'' + jsonData.replace(/'/g, "\\\\'") + '\\')">Copy JSON</button>');
        console.log('Extracted ' + jobs.length + ' jobs');
    } else {
        alert('No jobs found. Make sure you are on Indeed saved jobs page.');
    }
})();
        """
        
        return bookmarklet.strip()
    
    def csv_import_template(self):
        """Generate CSV template for manual job entry"""
        
        csv_template = """title,company,location,url,description,priority
Senior DevOps Engineer,Spotify,Stockholm Sweden,https://jobs.spotify.com/job/123,"Looking for DevOps engineer with Kubernetes experience...",high
Cloud Engineer,Volvo Cars,Gothenburg Sweden,https://careers.volvocars.com/job/456,"Join our cloud transformation team...",high
Platform Engineer,Klarna,Stockholm Sweden,https://jobs.klarna.com/job/789,"Build scalable platform infrastructure...",medium"""
        
        filename = f"indeed_jobs_template_{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(filename, 'w') as f:
            f.write(csv_template)
        
        print(f"📊 CSV Template created: {filename}")
        print("1. Fill in your Indeed saved jobs")
        print("2. Save the file")
        print("3. Use csv_to_jobs() to import")
        
        return filename
    
    def csv_to_jobs(self, csv_filename: str) -> List[Dict]:
        """Convert CSV file to jobs format"""
        
        import csv
        
        jobs = []
        
        try:
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    job = {
                        'id': f'csv_indeed_{i}',
                        'title': row.get('title', '').strip(),
                        'company': row.get('company', '').strip(),
                        'location': row.get('location', '').strip(),
                        'url': row.get('url', '').strip(),
                        'description': row.get('description', '').strip(),
                        'source': 'indeed_saved_csv',
                        'job_type': 'fulltime',
                        'remote_option': 'remote' in row.get('description', '').lower(),
                        'posting_date': datetime.now(),
                        'priority': row.get('priority', 'medium').strip(),
                        'keywords': self._extract_basic_keywords(f"{row.get('title', '')} {row.get('description', '')}")
                    }
                    
                    if job['title'] and job['company']:  # Valid job
                        jobs.append(job)
            
            print(f"✅ Imported {len(jobs)} jobs from {csv_filename}")
            
            # Save as JSON for processing
            json_filename = csv_filename.replace('.csv', '.json')
            with open(json_filename, 'w') as f:
                json.dump(jobs, f, indent=2, default=str)
            
            print(f"💾 Jobs converted to: {json_filename}")
            
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
        
        return jobs
    
    async def process_imported_jobs(self, jobs_filename: str):
        """Process imported jobs with Smart CV system"""
        
        try:
            with open(jobs_filename, 'r') as f:
                jobs = json.load(f)
            
            print(f"🚀 Processing {len(jobs)} imported jobs...")
            
            # Import and use the processor
            from process_indeed_devops_jobs import IndeedDevOpsProcessor
            
            processor = IndeedDevOpsProcessor()
            
            # Process with smart system
            results = await processor.process_devops_jobs_with_smart_system(jobs)
            
            # Generate report
            keyword_analysis = await processor.analyze_devops_market_keywords(jobs)
            report = processor.generate_processing_report(results, keyword_analysis)
            
            # Display summary
            processor.print_processing_summary(report)
            
            return report
            
        except Exception as e:
            print(f"❌ Error processing jobs: {e}")
            return None

def main():
    """Main function - provides interactive menu"""
    
    guide = IndeedIntegrationGuide()
    
    while True:
        print("\n🔗 INDEED INTEGRATION MENU")
        print("=" * 30)
        print("1. View Integration Options")
        print("2. Manual Job Input")
        print("3. Generate Bookmarklet")
        print("4. Create CSV Template") 
        print("5. Import from CSV")
        print("6. Process DevOps Jobs (Demo)")
        print("0. Exit")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            guide.print_integration_options()
        elif choice == '2':
            jobs = guide.manual_job_input()
            if jobs:
                process = input("\nProcess jobs now? (y/n): ").lower()
                if process == 'y':
                    # Would call async processing here
                    print("🚀 Processing jobs... (Run process_indeed_devops_jobs.py)")
        elif choice == '3':
            bookmarklet = guide.create_bookmarklet_code()
            print("\n📱 BOOKMARKLET CODE:")
            print("-" * 40)
            print(bookmarklet)
            print("-" * 40)
            print("📋 Copy this code and save as bookmark")
            print("🌐 Use on Indeed saved jobs page")
        elif choice == '4':
            template_file = guide.csv_import_template()
            print(f"✅ Template created: {template_file}")
        elif choice == '5':
            csv_file = input("Enter CSV filename: ").strip()
            if csv_file:
                jobs = guide.csv_to_jobs(csv_file)
                if jobs:
                    print(f"✅ Ready to process {len(jobs)} jobs")
        elif choice == '6':
            print("🚀 Running demo with sample DevOps jobs...")
            # Import and run the processor
            import subprocess
            subprocess.run(['python', 'process_indeed_devops_jobs.py'])
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()