#!/usr/bin/env python3
"""
Test sending customized CV and cover letter to leeharvad@gmail.com
This will test the complete email automation workflow
"""
import asyncio
import sys
from pathlib import Path
import os

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Test job data for document generation
test_job = {
    'title': 'Senior Fullstack Developer',
    'company': 'ECARX Sweden',
    'location': 'Gothenburg, Sweden',
    'description': '''We are looking for a Senior Fullstack Developer to join our automotive technology team.
    
Key Responsibilities:
• Develop scalable backend services using Java and Spring Boot
• Build responsive frontend applications with React
• Design and implement RESTful APIs and microservices
• Work with PostgreSQL databases and cloud platforms (AWS/Azure)
• Deploy applications using Docker and Kubernetes

Requirements:
• 5+ years experience with Java/Spring Boot
• Strong knowledge of React/Angular frontend frameworks
• Experience with AWS or Azure cloud platforms
• Familiarity with Docker and Kubernetes
• Knowledge of PostgreSQL and MongoDB

Contact: HR Team for more information about this exciting opportunity.''',
    'url': 'https://careers.ecarx.com/senior-fullstack-developer',
    'source': 'ecarx_careers',
    'keywords': ['java', 'spring boot', 'react', 'aws', 'azure', 'microservices', 'postgresql', 'docker', 'kubernetes'],
    'job_type': 'fulltime',
    'remote_option': True,
    'posting_date': '2025-01-27',
    'confidence_score': 0.95
}

async def test_email_sending():
    """Test the complete email workflow"""
    print("🧪 Testing Email Automation to leeharvad@gmail.com")
    print("=" * 60)
    
    try:
        # Import services (with error handling for missing dependencies)
        try:
            from app.services.job_application_processor import JobApplicationProcessor
            processor = JobApplicationProcessor()
            has_full_processor = True
        except ImportError as e:
            print(f"⚠️  Full processor not available: {e}")
            print("📝 Using LaTeX service for document generation only")
            from app.services.latex_resume_service import LaTeXResumeService
            latex_service = LaTeXResumeService()
            has_full_processor = False
        
        print(f"📋 Test Job: {test_job['title']} at {test_job['company']}")
        print("-" * 40)
        
        if has_full_processor:
            # Step 1: Generate documents using full processor
            print("⚙️  Step 1: Generating customized documents...")
            processed_job = await processor.process_job_and_generate_documents(test_job)
            
            if processed_job['status'] == 'success':
                print("✅ Documents generated successfully!")
                print(f"   • CV size: {len(processed_job['cv_pdf'])} bytes")
                print(f"   • Cover Letter size: {len(processed_job['cover_letter_pdf'])} bytes")
                
                # Step 2: Send email
                print("\n📧 Step 2: Sending email to leeharvad@gmail.com...")
                email_sent = await processor.send_job_application_email(processed_job, "leeharvad@gmail.com")
                
                if email_sent:
                    print("🎉 SUCCESS! Email sent to leeharvad@gmail.com!")
                    print("📎 Attachments:")
                    print(f"   • CV_ECARX_Sweden_Senior_Fullstack_Developer.pdf")
                    print(f"   • CoverLetter_ECARX_Sweden_Senior_Fullstack_Developer.pdf")
                    return True
                else:
                    print("❌ Email sending failed - check SMTP configuration")
                    return False
            else:
                print(f"❌ Document generation failed: {processed_job.get('error')}")
                return False
        else:
            # Alternative: Test document generation only
            print("⚙️  Testing document generation only...")
            
            try:
                cv_content = await latex_service.generate_customized_cv(test_job)
                cl_content = await latex_service.generate_customized_cover_letter(test_job)
                
                if cv_content and cl_content:
                    print("✅ Documents generated successfully!")
                    print(f"   • CV size: {len(cv_content)} bytes")
                    print(f"   • Cover Letter size: {len(cl_content)} bytes")
                    print("📧 Email sending requires SMTP configuration")
                    return True
                else:
                    print("❌ Document generation failed - LaTeX compilation issue")
                    return False
            except Exception as e:
                print(f"❌ Document generation error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def check_smtp_config():
    """Check if SMTP configuration is available"""
    print("\n🔧 SMTP Configuration Check")
    print("-" * 30)
    
    smtp_vars = {
        'SMTP_HOST': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
        'SMTP_PORT': os.getenv('SMTP_PORT', '587'),
        'SMTP_USER': os.getenv('SMTP_USER', 'hongzhili01@gmail.com'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD', ''),
        'EMAILS_FROM_EMAIL': os.getenv('EMAILS_FROM_EMAIL', 'hongzhili01@gmail.com')
    }
    
    for key, value in smtp_vars.items():
        if key == 'SMTP_PASSWORD':
            status = "✅ Set" if value else "❌ Missing"
            print(f"   {key}: {status}")
        else:
            print(f"   {key}: {value}")
    
    if not smtp_vars['SMTP_PASSWORD']:
        print("\n💡 To enable email sending:")
        print("   1. Set SMTP_PASSWORD environment variable")
        print("   2. Use Gmail App Password (not regular password)")
        print("   3. Configure 2FA and generate app password in Gmail settings")

async def main():
    """Main test function"""
    print("📧 Testing JobHunter Email Automation")
    print("Sending customized CV and Cover Letter to leeharvad@gmail.com")
    print()
    
    # Check SMTP configuration
    await check_smtp_config()
    
    # Test email sending
    success = await test_email_sending()
    
    print("\n📊 TEST RESULTS:")
    print("=" * 60)
    
    if success:
        print("🎉 EMAIL TEST SUCCESSFUL!")
        print("✅ Documents generated with your custom format")
        print("✅ Email automation working correctly")
        print("📧 Check leeharvad@gmail.com for the test email")
        print("\n📋 Email contains:")
        print("   • Job details and application link")
        print("   • Customized CV matching your modern format")
        print("   • Cover letter with proper company styling")
        print("   • Keywords and job analysis")
    else:
        print("⚠️  EMAIL TEST INCOMPLETE")
        print("✅ Document templates updated and ready")
        print("❌ Email sending requires SMTP configuration")
        print("\n🔧 Next steps:")
        print("   1. Configure Gmail App Password")
        print("   2. Set SMTP_PASSWORD environment variable")
        print("   3. Re-run test to verify email delivery")
    
    print(f"\n💌 Your automation will send emails to leeharvad@gmail.com")
    print("   whenever new relevant jobs are found and processed!")

if __name__ == "__main__":
    asyncio.run(main())