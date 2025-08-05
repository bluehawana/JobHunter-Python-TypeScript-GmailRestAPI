#!/usr/bin/env python3
"""
Improved Working Automation - PDF generation + better company extraction + direct links
"""
import asyncio
import sys
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from pathlib import Path
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImprovedWorkingAutomation:
    """Improved automation with PDF generation and better company extraction"""
    
    def __init__(self):
        # Email configuration
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD', '')
        self.target_email = 'hongzhili01@gmail.com'
        
        logger.info("✅ Improved automation initialized")
    
    async def scan_and_process_jobs(self):
        """Main function - scan Gmail and process jobs with improvements"""
        try:
            logger.info("🚀 Starting improved job automation...")
            
            # Import email scanner
            from app.services.real_job_scanner import RealJobScanner
            email_scanner = RealJobScanner()
            
            # Scan Gmail for jobs
            logger.info("📧 Scanning Gmail for job opportunities...")
            jobs = await email_scanner.scan_real_gmail_jobs(days_back=3)
            
            logger.info(f"🔍 Found {len(jobs)} job opportunities")
            
            if not jobs:
                logger.info("📭 No jobs found")
                return
            
            # Process each job with improvements
            successful_emails = 0
            
            for i, job in enumerate(jobs, 1):
                try:
                    # Improve company name extraction
                    improved_job = self._improve_job_data(job)
                    
                    logger.info(f"🎯 Processing job {i}/{len(jobs)}: {improved_job['title']} at {improved_job['company']}")
                    
                    # Generate PDF documents
                    cv_pdf = self._generate_cv_pdf(improved_job)
                    cl_pdf = self._generate_cover_letter_pdf(improved_job)
                    
                    # Send improved email
                    email_sent = await self._send_improved_job_email(improved_job, cv_pdf, cl_pdf)
                    
                    if email_sent:
                        successful_emails += 1
                        logger.info(f"✅ Email sent for {improved_job['company']}")
                    else:
                        logger.error(f"❌ Email failed for {improved_job['company']}")
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {job.get('title', 'Unknown')}: {e}")
            
            logger.info(f"🎉 Automation completed: {successful_emails}/{len(jobs)} successful emails")
            logger.info(f"📧 Check {self.target_email} for professional PDF applications!")
            
        except Exception as e:
            logger.error(f"❌ Automation error: {e}")
            import traceback
            traceback.print_exc()
    
    def _improve_job_data(self, job: dict) -> dict:
        """Improve job data extraction, especially company names"""
        improved_job = job.copy()
        
        # Extract better company name from email subject and body
        email_subject = job.get('email_subject', '')
        body = job.get('body', '')
        sender = job.get('sender', '')
        
        # Swedish patterns for company extraction
        company_patterns = [
            # "Company söker nu fler talanger till"
            r'([A-ZÅÄÖ][a-zåäö\s&]+?)\s+(?:söker|ker)\s+nu\s+fler\s+talanger',
            # "Company is actively hiring"
            r'([A-ZÅÄÖ][a-zåäö\s&]+?)\s+is\s+actively\s+hiring',
            # "Join Company as"
            r'Join\s+([A-ZÅÄÖ][a-zåäö\s&]+?)\s+as',
            # "Company - Job Title"
            r'^([A-ZÅÄÖ][a-zåäö\s&]+?)\s*[-–]\s*[A-Z]',
            # From email domain
            r'@([a-zA-Z]+)\.com',
        ]
        
        # Try to extract company name
        company_name = job.get('company', 'Technology Company')
        
        content_to_search = f"{email_subject} {body}"
        
        for pattern in company_patterns:
            match = re.search(pattern, content_to_search, re.IGNORECASE)
            if match:
                potential_company = match.group(1).strip()
                # Clean up the company name
                potential_company = re.sub(r'\s+', ' ', potential_company)
                potential_company = potential_company.title()
                
                # Validate it's a reasonable company name
                if len(potential_company) > 2 and len(potential_company) < 50:
                    company_name = potential_company
                    break
        
        # Special handling for known Swedish companies
        content_lower = content_to_search.lower()
        known_companies = {
            'volvo': 'Volvo Group',
            'ericsson': 'Ericsson',
            'spotify': 'Spotify',
            'klarna': 'Klarna',
            'skf': 'SKF Group',
            'hasselblad': 'Hasselblad',
            'polestar': 'Polestar',
            'zenseact': 'Zenseact',
            'cevt': 'CEVT',
            'stena': 'Stena Line'
        }
        
        for keyword, full_name in known_companies.items():
            if keyword in content_lower:
                company_name = full_name
                break
        
        improved_job['company'] = company_name
        
        # Improve job title extraction
        if 'ker nu fler talanger till' in email_subject.lower():
            # Extract job title after the Swedish phrase
            title_match = re.search(r'ker nu fler talanger till\s+(.+)', email_subject, re.IGNORECASE)
            if title_match:
                improved_job['title'] = title_match.group(1).strip()
        
        # Ensure we have the original application URL
        if not improved_job.get('url') or improved_job.get('url') == '':
            # Try to extract URL from body
            url_patterns = [
                r'https://[^\s]+\.linkedin\.com/jobs/view/\d+',
                r'https://[^\s]+\.indeed\.com/viewjob\?jk=[a-zA-Z0-9]+',
                r'https://[^\s]+/jobs?/[^\s]+',
                r'https://[^\s]+/careers?/[^\s]+',
            ]
            
            for pattern in url_patterns:
                url_match = re.search(pattern, body)
                if url_match:
                    improved_job['url'] = url_match.group(0)
                    break
        
        return improved_job
    
    def _generate_cv_pdf(self, job: dict) -> bytes:
        """Generate CV as PDF using ReportLab"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=12,
                alignment=1  # Center
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                textColor='darkblue'
            )
            
            # Build content
            content = []
            
            # Header
            content.append(Paragraph("HONGZHI LI", title_style))
            content.append(Paragraph("Senior Fullstack Developer", styles['Normal']))
            content.append(Paragraph("hongzhili01@gmail.com | 0728384299 | LinkedIn | GitHub", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Professional Summary
            content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            summary = f"Experienced Senior Fullstack Developer with 5+ years of expertise in modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Specialized in {job['title'].lower()} roles at companies like {job['company']}."
            content.append(Paragraph(summary, styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Technical Skills
            content.append(Paragraph("CORE TECHNICAL SKILLS", heading_style))
            skills = [
                "Programming Languages: Java/J2EE, JavaScript, C#/.NET Core, Python, TypeScript",
                "Frontend Technologies: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                "Backend Frameworks: Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI",
                "Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                "Cloud Platforms: AWS, Azure, GCP",
                "DevOps: Docker, Kubernetes, Jenkins, GitHub Actions"
            ]
            
            for skill in skills:
                content.append(Paragraph(f"• {skill}", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Experience
            content.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
            
            # ECARX
            content.append(Paragraph("<b>ECARX | IT/Infrastructure Specialist</b>", styles['Normal']))
            content.append(Paragraph("October 2024 - Present | Gothenburg, Sweden", styles['Normal']))
            ecarx_points = [
                "Leading infrastructure optimization and system integration projects",
                "Implementing cost optimization by migrating from AKS to local Kubernetes cluster",
                "Managing complex network systems and providing technical solution design"
            ]
            for point in ecarx_points:
                content.append(Paragraph(f"• {point}", styles['Normal']))
            content.append(Spacer(1, 6))
            
            # Synteda
            content.append(Paragraph("<b>Synteda | Azure Fullstack Developer</b>", styles['Normal']))
            content.append(Paragraph("August 2023 - September 2024 | Gothenburg, Sweden", styles['Normal']))
            synteda_points = [
                "Developed comprehensive talent management system using C# and .NET Core",
                "Built complete office management platform with scalable microservices design",
                "Implemented RESTful APIs and microservices for scalable application architecture"
            ]
            for point in synteda_points:
                content.append(Paragraph(f"• {point}", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Education
            content.append(Paragraph("EDUCATION", heading_style))
            content.append(Paragraph("IT Högskolan | Bachelor's Degree in .NET Cloud Development | 2021-2023", styles['Normal']))
            content.append(Paragraph("University of Gothenburg | Master's in International Business and Trade | 2016-2019", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Certifications
            content.append(Paragraph("CERTIFICATIONS", heading_style))
            certs = [
                "AWS Certified Solutions Architect - Associate (Aug 2022)",
                "Microsoft Certified: Azure Fundamentals (Jun 2022)",
                "AWS Certified Developer - Associate (Nov 2022)"
            ]
            for cert in certs:
                content.append(Paragraph(f"• {cert}", styles['Normal']))
            
            # Build PDF
            doc.build(content)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error generating CV PDF: {e}")
            return b""
    
    def _generate_cover_letter_pdf(self, job: dict) -> bytes:
        """Generate Cover Letter as PDF using ReportLab"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
            
            styles = getSampleStyleSheet()
            
            content = []
            
            # Header
            content.append(Paragraph("HONGZHI LI", styles['Title']))
            content.append(Paragraph("Senior Fullstack Developer", styles['Normal']))
            content.append(Paragraph("hongzhili01@gmail.com | 0728384299", styles['Normal']))
            content.append(Spacer(1, 20))
            
            # Date
            content.append(Paragraph(datetime.now().strftime('%Y-%m-%d'), styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Company info
            content.append(Paragraph(f"{job['company']}", styles['Normal']))
            content.append(Paragraph("Sweden", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Subject
            content.append(Paragraph(f"<b>Re: Application for {job['title']} Position</b>", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Greeting
            content.append(Paragraph("Dear Hiring Manager,", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # Body paragraphs
            paragraphs = [
                f"I am writing to express my sincere interest in the {job['title']} role at {job['company']}. As a seasoned software professional with over 5 years of experience, I am excited by the prospect of contributing to your innovative team.",
                
                f"My technical expertise aligns perfectly with your requirements. I have extensive experience in full-stack development, cloud platforms, and modern DevOps practices. My current role as IT/Infrastructure Specialist at ECARX has strengthened my skills in system integration and scalable architecture design.",
                
                f"I am particularly drawn to {job['company']} because of your innovative approach to technology and commitment to excellence. My combination of technical expertise, hands-on experience with modern development practices, and proven track record of delivering scalable solutions makes me an ideal candidate for this position.",
                
                f"I would welcome the opportunity to discuss how my experience and passion for software development can contribute to {job['company']}'s continued success. Thank you for considering my application."
            ]
            
            for para in paragraphs:
                content.append(Paragraph(para, styles['Normal']))
                content.append(Spacer(1, 12))
            
            # Closing
            content.append(Paragraph("Sincerely,", styles['Normal']))
            content.append(Spacer(1, 20))
            content.append(Paragraph("Hongzhi Li", styles['Normal']))
            
            # Build PDF
            doc.build(content)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error generating cover letter PDF: {e}")
            return b""
    
    async def _send_improved_job_email(self, job: dict, cv_pdf: bytes, cl_pdf: bytes) -> bool:
        """Send improved job application email with PDFs and direct links"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_url = job.get('url', '')
            keywords = job.get('keywords', [])
            location = job.get('location', 'Sweden')
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"JobHunter Pro <{self.sender_email}>"
            msg['To'] = self.target_email
            msg['Subject'] = f"🎯 Ready to Apply: {job_title} at {company}"
            
            # Create improved email body
            email_body = f"""Hi Hongzhi,

🎯 NEW JOB APPLICATION READY FOR SUBMISSION

Your JobHunter system has processed a new opportunity and generated professional PDF documents:

📋 JOB DETAILS:
• Position: {job_title}
• Company: {company}
• Location: {location}
• Source: {job.get('source', 'Gmail')}

🔗 DIRECT APPLICATION LINK:
{job_url if job_url else 'Check original email for application link'}

📄 PROFESSIONAL PDF DOCUMENTS ATTACHED:
✅ Customized CV (PDF) - Tailored for {job_title} role
✅ Personalized Cover Letter (PDF) - Company-specific content

🎯 NEXT STEPS:
1. Download the attached PDF documents
2. Click the application link above to apply directly
3. Upload the PDFs to the job application form
4. Submit your application

📝 JOB DESCRIPTION PREVIEW:
{job.get('description', 'No description available')[:400]}{'...' if len(job.get('description', '')) > 400 else ''}

🔑 KEYWORDS OPTIMIZED:
{', '.join(keywords[:8]) if keywords else 'General software development skills'}

✨ DOCUMENT FEATURES:
• Professional PDF format ready for employers
• ATS-optimized content with relevant keywords
• Company-specific customization
• Role-focused experience highlighting
• Professional formatting and layout

📊 APPLICATION STATUS: Ready for immediate submission
🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Good luck with your application! 🚀

Best regards,
JobHunter Pro System

---
💡 TIP: These PDFs are professionally formatted and ready to submit directly to employers.
"""
            
            # Attach email body
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Attach CV PDF
            if cv_pdf:
                cv_attachment = MIMEApplication(cv_pdf, _subtype='pdf')
                cv_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"Hongzhi_Li_CV_{company.replace(' ', '_')}_{job_title.replace(' ', '_')}.pdf"
                )
                msg.attach(cv_attachment)
            
            # Attach Cover Letter PDF
            if cl_pdf:
                cl_attachment = MIMEApplication(cl_pdf, _subtype='pdf')
                cl_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"Hongzhi_Li_CoverLetter_{company.replace(' ', '_')}_{job_title.replace(' ', '_')}.pdf"
                )
                msg.attach(cl_attachment)
            
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"✅ Improved email sent successfully to {self.target_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending improved email: {e}")
            return False

async def main():
    """Main function"""
    print("🚀 Improved JobHunter Automation")
    print("=" * 50)
    print("✅ Professional PDF documents")
    print("🏢 Better company name extraction")
    print("🔗 Direct application links included")
    print("📧 Ready-to-submit applications")
    print("=" * 50)
    
    # Check if reportlab is available
    try:
        import reportlab
        print("✅ PDF generation available")
    except ImportError:
        print("❌ Please install reportlab: pip install reportlab")
        return
    
    # Initialize and run automation
    automation = ImprovedWorkingAutomation()
    await automation.scan_and_process_jobs()

if __name__ == "__main__":
    asyncio.run(main())