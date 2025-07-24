#!/usr/bin/env python3
"""
Demo: Process sample jobs and generate application materials

This demo creates sample job data, generates PDFs, and shows you the complete workflow.
Since the LinkedIn API has limits and Gmail requires OAuth setup, this demo uses 
sample data to demonstrate the PDF generation and email system.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.latex_resume_service import LaTeXResumeService
from app.services.supabase_service import supabase_service

async def demo_job_processing():
    """Demo the complete job processing workflow"""
    
    print("🚀 JobHunter Demo - Application Generation System")
    print("=" * 60)
    print("Processing jobs for Hongzhi Li")
    print("Target: Generate customized PDFs and demonstrate email system")
    print()
    
    # Set up environment
    setup_environment()
    
    # Create sample jobs based on your URLs
    sample_jobs = [
        {
            'company_name': 'TechCorp Sweden',
            'job_title': 'Senior Fullstack Developer',
            'job_description': '''We are looking for a Senior Fullstack Developer to join our innovative team in Stockholm.

Key Requirements:
• 5+ years of experience with JavaScript, React, and Node.js
• Strong background in Java/Spring Boot development
• Experience with cloud platforms (AWS/Azure)
• Knowledge of microservices architecture
• Database experience with PostgreSQL and MongoDB
• CI/CD experience with Jenkins or GitHub Actions
• Agile/Scrum methodology experience

What we offer:
• Competitive salary (600,000 - 800,000 SEK)
• Flexible working hours and remote work options
• Professional development opportunities
• Modern tech stack and innovative projects
• Great team culture in Stockholm

This is an excellent opportunity for an experienced developer looking to work with cutting-edge technologies in a collaborative environment.''',
            'location': 'Stockholm, Sweden',
            'application_link': 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4266325638',
            'work_type': 'hybrid',
            'application_status': 'found',
            'final_result': 'pending',
            'salary_range': '600,000 - 800,000 SEK',
            'memo': 'Found via LinkedIn job search - matches fullstack developer profile perfectly'
        },
        {
            'company_name': 'Growing Startup',
            'job_title': 'Backend Developer',
            'job_description': '''Join our fast-growing startup as a Backend Developer! We\'re building the next generation of fintech solutions.

Requirements:
• 3+ years of Python/Django or Java/Spring Boot experience  
• RESTful API design and development
• Database design and optimization (PostgreSQL preferred)
• Experience with Docker and Kubernetes
• Cloud experience (preferably AWS)
• Understanding of microservices architecture
• Experience with automated testing

Nice to have:
• Fintech or financial services experience
• DevOps skills and CI/CD pipeline setup
• Frontend skills (React/Angular)
• Machine learning experience

We offer:
• Equity participation in a growing company
• Flexible work arrangements
• Learning and development budget
• Modern development tools and practices

This role was shared via LinkedIn Jobs email notification. Great opportunity to join early-stage startup with high growth potential.''',
            'location': 'Gothenburg, Sweden',
            'application_link': 'https://mail.google.com/mail/u/0/#search/linkedin+jobs/FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx',
            'work_type': 'remote',
            'application_status': 'found',
            'final_result': 'pending',
            'memo': 'Received via Gmail LinkedIn Jobs notification - startup environment with equity'
        }
    ]
    
    try:
        # Process each job
        latex_service = LaTeXResumeService()
        processed_jobs = []
        
        for i, job_data in enumerate(sample_jobs, 1):
            print(f"\n📋 Processing Job {i}: {job_data['job_title']} at {job_data['company_name']}")
            
            try:
                # Save job to database
                print("💾 Saving job to database...")
                saved_job = await supabase_service.create_job_application(job_data)
                processed_jobs.append(saved_job)
                print(f"✅ Job saved with ID: {saved_job.get('id')}")
                
                # Generate application materials
                print("📄 Generating customized CV and cover letter...")
                
                # Generate CV
                cv_pdf = await latex_service.generate_customized_cv(job_data)
                print(f"✅ CV generated: {len(cv_pdf) if cv_pdf else 0} bytes")
                
                # Generate cover letter
                cover_letter_pdf = await latex_service.generate_customized_cover_letter(job_data)
                print(f"✅ Cover letter generated: {len(cover_letter_pdf) if cover_letter_pdf else 0} bytes")
                
                # Save PDFs to files for demonstration
                if cv_pdf:
                    cv_filename = f"cv_{job_data['company_name'].replace(' ', '_')}_Hongzhi_Li.pdf"
                    with open(cv_filename, 'wb') as f:
                        f.write(cv_pdf)
                    print(f"💾 CV saved as: {cv_filename}")
                
                if cover_letter_pdf:
                    cl_filename = f"cover_letter_{job_data['company_name'].replace(' ', '_')}_Hongzhi_Li.pdf"
                    with open(cl_filename, 'wb') as f:
                        f.write(cover_letter_pdf)
                    print(f"💾 Cover letter saved as: {cl_filename}")
                
                # Update job status
                await supabase_service.update_application_status(
                    saved_job.get('id'),
                    'applied',
                    f'Generated customized application materials - CV: {len(cv_pdf) if cv_pdf else 0} bytes, Cover Letter: {len(cover_letter_pdf) if cover_letter_pdf else 0} bytes'
                )
                
                # Add communication log
                await supabase_service.add_communication_log(
                    saved_job.get('id'),
                    {
                        "date": datetime.now().isoformat(),
                        "type": "system",
                        "direction": "internal",
                        "subject": "Application Materials Generated",
                        "summary": f"Generated customized CV and cover letter PDFs for {job_data['company_name']} position"
                    }
                )
                
                print(f"✅ Job {i} processing completed successfully!")
                
            except Exception as e:
                print(f"❌ Error processing job {i}: {e}")
                continue
        
        # Display final summary
        print(f"\n📊 Processing Summary")
        print("=" * 40)
        print(f"Jobs processed: {len(processed_jobs)}")
        print(f"PDFs generated: {len(processed_jobs) * 2} (CV + Cover Letter for each)")
        
        for job in processed_jobs:
            print(f"\n📋 {job.get('job_title')} at {job.get('company_name')}")
            print(f"   Status: {job.get('application_status')}")
            print(f"   Location: {job.get('location')}")
            print(f"   Work Type: {job.get('work_type')}")
            print(f"   Link: {job.get('application_link')}")
        
        # Get final statistics
        print(f"\n📈 Database Statistics")
        stats = await supabase_service.get_application_statistics()
        print(f"Total applications in database: {stats.get('total_applications', 0)}")
        print(f"Applications by status: {stats.get('by_status', {})}")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"\n📧 Email System Demo")
        print("=" * 25)
        print("The email system is ready but requires Gmail App Password setup:")
        print("1. Go to Google Account → Security → 2-Step Verification")
        print("2. Generate an 'App Password' for 'Mail'")
        print("3. Set: export GMAIL_APP_PASSWORD='your-16-char-password'")
        print("4. Run the script again to send emails to leeharvad@gmail.com")
        
        print(f"\n📄 Generated Files:")
        print("Check the current directory for:")
        for job in sample_jobs:
            company = job['company_name'].replace(' ', '_')
            print(f"• cv_{company}_Hongzhi_Li.pdf")
            print(f"• cover_letter_{company}_Hongzhi_Li.pdf")
        
    except Exception as e:
        print(f"\n❌ Critical error during demo: {e}")
        import traceback
        traceback.print_exc()

def setup_environment():
    """Set up environment variables"""
    
    # Supabase credentials
    os.environ["SUPABASE_URL"] = "https://chcdebpjwallysedcfsq.supabase.co"
    os.environ["SUPABASE_ANON_KEY"] = "REMOVED_SECRET"
    
    print("✅ Environment configured")

async def test_latex_system():
    """Test the LaTeX PDF generation system"""
    
    print("\n🔧 Testing LaTeX PDF Generation System")
    print("=" * 45)
    
    try:
        latex_service = LaTeXResumeService()
        
        # Test job
        test_job = {
            'title': 'Fullstack Developer',
            'company': 'Test Company AB',
            'description': 'Looking for experienced fullstack developer with React, Node.js, and cloud experience.',
            'keywords': ['react', 'nodejs', 'aws', 'fullstack', 'javascript'],
            'location': 'Stockholm, Sweden'
        }
        
        print("📄 Testing CV generation...")
        cv_pdf = await latex_service.generate_customized_cv(test_job)
        
        if cv_pdf and len(cv_pdf) > 0:
            print(f"✅ CV generated successfully: {len(cv_pdf)} bytes")
            with open("test_cv.pdf", 'wb') as f:
                f.write(cv_pdf)
            print("💾 Test CV saved as: test_cv.pdf")
        else:
            print("❌ CV generation failed")
        
        print("📄 Testing cover letter generation...")
        cl_pdf = await latex_service.generate_customized_cover_letter(test_job)
        
        if cl_pdf and len(cl_pdf) > 0:
            print(f"✅ Cover letter generated successfully: {len(cl_pdf)} bytes")
            with open("test_cover_letter.pdf", 'wb') as f:
                f.write(cl_pdf)
            print("💾 Test cover letter saved as: test_cover_letter.pdf")
        else:
            print("❌ Cover letter generation failed")
        
        print("\n✅ LaTeX system test completed!")
        
    except Exception as e:
        print(f"❌ LaTeX test failed: {e}")
        print("\n💡 Make sure LaTeX is installed:")
        print("macOS: brew install --cask mactex")
        print("Ubuntu: sudo apt-get install texlive-latex-base texlive-latex-extra")

if __name__ == "__main__":
    print("JobHunter Demo - Automated Job Application System")
    print("Demonstrating PDF generation and database integration")
    print()
    
    # Run the demo
    asyncio.run(demo_job_processing())
    
    # Test LaTeX system
    print("\n" + "="*60)
    test_latex = input("Test LaTeX PDF generation? (y/n): ").lower().strip()
    if test_latex == 'y':
        asyncio.run(test_latex_system())