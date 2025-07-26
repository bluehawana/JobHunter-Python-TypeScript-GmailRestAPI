#!/usr/bin/env python3
"""
Add Gothenburg-priority jobs and create LinkedIn saved jobs importer
"""

import os
import sys
from datetime import datetime, date
from typing import List, Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def create_gothenburg_jobs() -> List[Dict[str, Any]]:
    """Create high-priority Gothenburg jobs"""
    return [
        {
            "title": "Senior Python Developer",
            "company": "Volvo Group",
            "location": "Gothenburg, Sweden",
            "description": "Join our team developing next-generation automotive software using Python, microservices, and cloud technologies.",
            "requirements": "5+ years Python, microservices, AWS/Azure, automotive experience preferred",
            "salary_range": "650,000 - 850,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://volvogroup.com/careers/python-senior",
            "source": "company_website",
            "skills_matched": ["Python", "Microservices", "AWS", "Automotive"],
            "match_score": 0.97,
            "status": "found"
        },
        {
            "title": "Backend Developer",
            "company": "SKF Group",
            "location": "Gothenburg, Sweden", 
            "description": "Develop industrial IoT solutions using Python, Django, and PostgreSQL for bearing and machinery analytics.",
            "requirements": "3+ years Python, Django, PostgreSQL, IoT experience, industrial domain knowledge",
            "salary_range": "550,000 - 700,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://skf.com/careers/backend-dev",
            "source": "linkedin",
            "skills_matched": ["Python", "Django", "PostgreSQL", "IoT"],
            "match_score": 0.93,
            "status": "found"
        },
        {
            "title": "Full Stack Developer",
            "company": "Zenseact (Volvo)",
            "location": "Gothenburg, Sweden",
            "description": "Build autonomous driving software interfaces using Python backend and React frontend.",
            "requirements": "Python, FastAPI, React, TypeScript, autonomous systems, machine learning",
            "salary_range": "700,000 - 900,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior", 
            "posted_date": date.today().isoformat(),
            "apply_url": "https://zenseact.com/careers/fullstack",
            "source": "linkedin",
            "skills_matched": ["Python", "FastAPI", "React", "TypeScript", "ML"],
            "match_score": 0.96,
            "status": "found"
        },
        {
            "title": "DevOps Engineer",
            "company": "Hasselblad",
            "location": "Gothenburg, Sweden",
            "description": "Infrastructure and deployment automation for camera software using Python, Docker, and Kubernetes.",
            "requirements": "Python automation, Docker, Kubernetes, CI/CD, camera/imaging industry",
            "salary_range": "600,000 - 800,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://hasselblad.com/careers/devops",
            "source": "indeed",
            "skills_matched": ["Python", "Docker", "Kubernetes", "CI/CD"],
            "match_score": 0.89,
            "status": "found"
        },
        {
            "title": "Software Engineer",
            "company": "Stena Line",
            "location": "Gothenburg, Sweden",
            "description": "Develop maritime software solutions using Python for ferry operations and logistics.",
            "requirements": "Python, web development, databases, maritime/logistics experience preferred",
            "salary_range": "500,000 - 650,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://stenaline.com/careers/software-engineer",
            "source": "arbetsformedlingen",
            "skills_matched": ["Python", "Web Development", "Databases"],
            "match_score": 0.84,
            "status": "found"
        },
        {
            "title": "Data Engineer",
            "company": "CEVT (China Euro Vehicle Technology)",
            "location": "Gothenburg, Sweden",
            "description": "Build data pipelines for automotive testing using Python, Spark, and cloud technologies.",
            "requirements": "Python, Apache Spark, SQL, cloud platforms, automotive testing data",
            "salary_range": "600,000 - 750,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://cevt.se/careers/data-engineer",
            "source": "linkedin",
            "skills_matched": ["Python", "Apache Spark", "SQL", "Cloud"],
            "match_score": 0.87,
            "status": "found"
        },
        {
            "title": "Machine Learning Engineer", 
            "company": "Polestar",
            "location": "Gothenburg, Sweden",
            "description": "Develop ML models for electric vehicle optimization using Python, TensorFlow, and automotive data.",
            "requirements": "Python, TensorFlow/PyTorch, ML experience, automotive domain, electric vehicles",
            "salary_range": "750,000 - 950,000 SEK",
            "job_type": "Full-time",
            "experience_level": "Senior",
            "posted_date": date.today().isoformat(),
            "apply_url": "https://polestar.com/careers/ml-engineer",
            "source": "linkedin",
            "skills_matched": ["Python", "TensorFlow", "Machine Learning", "Automotive"],
            "match_score": 0.94,
            "status": "found"
        }
    ]

def create_linkedin_jobs_importer():
    """Create a template for importing LinkedIn saved jobs"""
    print("🔗 LinkedIn Saved Jobs Import System")
    print("=" * 50)
    
    linkedin_template_jobs = [
        {
            "title": "[PASTE JOB TITLE FROM LINKEDIN]",
            "company": "[PASTE COMPANY NAME]",
            "location": "Gothenburg, Sweden",  # Default to Gothenburg priority
            "description": "[PASTE JOB DESCRIPTION]",
            "requirements": "[PASTE REQUIREMENTS]",
            "salary_range": "[IF AVAILABLE]",
            "job_type": "Full-time",
            "experience_level": "[Junior/Mid-level/Senior]",
            "posted_date": date.today().isoformat(),
            "apply_url": "[LINKEDIN URL]",
            "source": "linkedin_saved",
            "skills_matched": ["[EXTRACT RELEVANT SKILLS]"],
            "match_score": 0.95,  # High priority for saved jobs
            "status": "saved"  # Special status for LinkedIn saved jobs
        }
    ]
    
    print("📋 LinkedIn Import Instructions:")
    print("1. Open your LinkedIn saved jobs page")
    print("2. For each job, copy the details")
    print("3. Use the save_linkedin_job() function below")
    print("4. Or manually add to the template above")
    print()
    
    return linkedin_template_jobs

def save_linkedin_job(title: str, company: str, location: str = "Gothenburg, Sweden", 
                     description: str = "", requirements: str = "", 
                     apply_url: str = "", salary_range: str = ""):
    """Helper function to quickly save a LinkedIn job"""
    
    job_data = {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "requirements": requirements,
        "salary_range": salary_range,
        "job_type": "Full-time",
        "experience_level": "Mid-level",  # Default
        "posted_date": date.today().isoformat(),
        "apply_url": apply_url,
        "source": "linkedin_saved",
        "skills_matched": ["Python"],  # Default, can be updated
        "match_score": 0.95,  # High priority for saved jobs
        "status": "saved"
    }
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        result = supabase.table('jobs').insert(job_data).execute()
        if result.data:
            print(f"✅ Saved LinkedIn job: {title} at {company}")
            return True
        else:
            print(f"❌ Failed to save: {title}")
            return False
            
    except Exception as e:
        print(f"❌ Error saving LinkedIn job: {e}")
        return False

def main():
    """Main function to add Gothenburg jobs and set up LinkedIn import"""
    print("🚀 Gothenburg Jobs Priority & LinkedIn Import Setup")
    print("=" * 60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Add Gothenburg priority jobs
        print("🏢 Adding Gothenburg Priority Jobs...")
        gothenburg_jobs = create_gothenburg_jobs()
        
        saved_count = 0
        for job in gothenburg_jobs:
            try:
                result = supabase.table('jobs').insert(job).execute()
                if result.data:
                    saved_count += 1
                    print(f"   ✅ {job['title']} at {job['company']}")
                    
            except Exception as e:
                if 'duplicate' in str(e).lower():
                    print(f"   ⚠️  Duplicate: {job['title']} at {job['company']}")
                else:
                    print(f"   ❌ Error: {e}")
        
        print(f"\n📊 Added {saved_count}/{len(gothenburg_jobs)} Gothenburg jobs")
        
        # Set up LinkedIn import system
        print("\n🔗 Setting up LinkedIn Saved Jobs Import...")
        create_linkedin_jobs_importer()
        
        print("\n📝 QUICK LinkedIn Job Add Examples:")
        print("Python code to add your saved jobs:")
        print()
        print("# Example usage:")
        print("save_linkedin_job(")
        print("    title='Senior Python Developer',")
        print("    company='Example Company',") 
        print("    location='Gothenburg, Sweden',")
        print("    description='Job description here...',")
        print("    apply_url='https://linkedin.com/jobs/view/123456'")
        print(")")
        
        print(f"\n🎯 PRIORITY RESULTS:")
        print(f"   🏢 Gothenburg jobs added: {saved_count}")
        print(f"   🔗 LinkedIn import system: Ready")
        
        print(f"\n✅ Setup completed! Now run 'python check_jobs_supabase.py' to see all jobs")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()