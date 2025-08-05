#!/usr/bin/env python3
"""
Simple Working Automation - Bypasses LaTeX issues
Generates basic text documents and sends emails immediately
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

class SimpleWorkingAutomation:
    """Simple automation that works without LaTeX complications"""
    
    def __init__(self):
        # Email configuration
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD', '')
        self.target_email = 'hongzhili01@gmail.com'
        
        logger.info("✅ Simple automation initialized")
    
    async def scan_and_process_jobs(self):
        """Main function - scan Gmail and process jobs"""
        try:
            logger.info("🚀 Starting simple job automation...")
            
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
            
            # Process each job
            successful_emails = 0
            
            for i, job in enumerate(jobs, 1):
                try:
                    logger.info(f"🎯 Processing job {i}/{len(jobs)}: {job['title']} at {job['company']}")
                    
                    # Generate simple text documents
                    cv_text = self._generate_simple_cv(job)
                    cl_text = self._generate_simple_cover_letter(job)
                    
                    # Send email with text documents
                    email_sent = await self._send_simple_job_email(job, cv_text, cl_text)
                    
                    if email_sent:
                        successful_emails += 1
                        logger.info(f"✅ Email sent for {job['company']}")
                    else:
                        logger.error(f"❌ Email failed for {job['company']}")
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {job.get('title', 'Unknown')}: {e}")
            
            logger.info(f"🎉 Automation completed: {successful_emails}/{len(jobs)} successful emails")
            logger.info(f"📧 Check {self.target_email} for job applications!")
            
        except Exception as e:
            logger.error(f"❌ Automation error: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_simple_cv(self, job: dict) -> str:
        """Generate simple CV text"""
        job_title = job.get('title', 'Software Developer')
        company = job.get('company', 'Target Company')
        keywords = job.get('keywords', [])
        
        # Determine role focus
        if 'backend' in job_title.lower() or any('backend' in kw for kw in keywords):
            role_focus = "Backend Developer"
            skills_focus = "Java/Spring Boot, Python, PostgreSQL, AWS, microservices architecture"
        elif 'devops' in job_title.lower() or any('devops' in kw or 'infrastructure' in kw for kw in keywords):
            role_focus = "DevOps Engineer"
            skills_focus = "Kubernetes, Docker, AWS/Azure, CI/CD, infrastructure automation"
        elif 'frontend' in job_title.lower() or any('frontend' in kw or 'react' in kw for kw in keywords):
            role_focus = "Frontend Developer"
            skills_focus = "React, Angular, JavaScript/TypeScript, HTML5/CSS3"
        else:
            role_focus = "Senior Fullstack Developer"
            skills_focus = "Java/Spring Boot, React, AWS, PostgreSQL, microservices"
        
        cv_text = f"""HONGZHI LI
{role_focus}

Contact Information:
Email: hongzhili01@gmail.com
Phone: 0728384299
LinkedIn: https://www.linkedin.com/in/hzl/
GitHub: https://github.com/bluehawana

PROFESSIONAL SUMMARY
Experienced {role_focus} with 5+ years of expertise in modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Specialized in {job_title.lower()} roles with strong focus on {skills_focus}.

CORE TECHNICAL SKILLS
• Programming Languages: Java/J2EE, JavaScript, C#/.NET Core, Python, TypeScript
• Frontend Technologies: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
• Backend Frameworks: Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI
• Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB
• Cloud Platforms: AWS, Azure, GCP
• DevOps: Docker, Kubernetes, Jenkins, GitHub Actions
• API Development: RESTful APIs, GraphQL, Microservices

PROFESSIONAL EXPERIENCE

ECARX | IT/Infrastructure Specialist
October 2024 - Present | Gothenburg, Sweden
• Leading infrastructure optimization and system integration projects for automotive technology solutions
• Implementing cost optimization by migrating from AKS to local Kubernetes cluster
• Managing complex network systems and providing technical solution design for enterprise applications
• Implementing monitoring solutions using Grafana and advanced scripting for system reliability

Synteda | Azure Fullstack Developer (Freelance)
August 2023 - September 2024 | Gothenburg, Sweden
• Developed comprehensive talent management system using C# and .NET Core with cloud-native architecture
• Built complete office management platform from scratch with both frontend and backend components
• Implemented RESTful APIs and microservices for scalable application architecture
• Integrated SQL and NoSQL databases with optimized query performance

IT-Högskolan | Backend Developer
January 2023 - May 2023 | Gothenburg, Sweden
• Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
• Developed RESTful APIs for frontend integration and implemented secure data handling
• Collaborated with UI/UX designers for seamless frontend-backend integration
• Implemented automated tests as part of delivery process

KEY PROJECTS

JobHunter Automation Platform (2024 - Present)
• Built comprehensive job search automation using Python, FastAPI, and PostgreSQL
• Implemented automated document generation and integrated multiple job boards
• Technologies: Python, FastAPI, PostgreSQL, Supabase, React

Hong Yan AB - E-commerce Platform (smrtmart.com)
• Fullstack e-commerce platform with Spring Boot backend and React frontend
• Implemented microservices architecture with PostgreSQL and MongoDB integration
• Built order management, inventory tracking, and payment processing systems

EDUCATION
IT Högskolan | Bachelor's Degree in .NET Cloud Development | 2021-2023
Mölndal Campus | Bachelor's Degree in Java Integration | 2019-2021
University of Gothenburg | Master's in International Business and Trade | 2016-2019

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (Aug 2022)
• Microsoft Certified: Azure Fundamentals (Jun 2022)
• AWS Certified Developer - Associate (Nov 2022)

ADDITIONAL INFORMATION
• Languages: Fluent in English and Mandarin
• Personal Website: https://www.bluehawana.com
• Portfolio Sites: https://www.senior798.eu, https://www.mibo.se

---
Customized for: {job_title} at {company}
Keywords optimized: {', '.join(keywords[:8])}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        return cv_text
    
    def _generate_simple_cover_letter(self, job: dict) -> str:
        """Generate simple cover letter text"""
        job_title = job.get('title', 'Software Developer')
        company = job.get('company', 'Target Company')
        description = job.get('description', '')
        
        # Determine company focus
        if 'volvo' in company.lower():
            company_focus = "your leadership in automotive innovation and sustainable transportation solutions"
        elif 'spotify' in company.lower():
            company_focus = "your revolutionary impact on music streaming and audio technology"
        elif 'ericsson' in company.lower():
            company_focus = "your pioneering work in telecommunications and 5G technology"
        else:
            company_focus = "your innovative approach to technology and commitment to excellence"
        
        # Extract key requirements
        tech_requirements = []
        if 'java' in description.lower() or 'spring' in description.lower():
            tech_requirements.append('Java/Spring Boot development')
        if 'react' in description.lower() or 'frontend' in description.lower():
            tech_requirements.append('React frontend development')
        if 'aws' in description.lower() or 'cloud' in description.lower():
            tech_requirements.append('cloud platform expertise')
        if 'kubernetes' in description.lower() or 'docker' in description.lower():
            tech_requirements.append('containerization and orchestration')
        
        tech_alignment = ', '.join(tech_requirements[:3]) if tech_requirements else 'full-stack development and modern DevOps practices'
        
        cover_letter_text = f"""HONGZHI LI
Senior Fullstack Developer

{datetime.now().strftime('%Y-%m-%d')}

{company}
Sweden

Re: Application for {job_title} Position

Dear Hiring Manager,

I am writing to express my sincere interest in the {job_title} role at {company}. As a seasoned software professional with a profound passion for innovative technology solutions, I am excited by the prospect of contributing to the development of cutting-edge solutions for your platform.

What draws me to {company} is {company_focus}. With my proven experience in {tech_alignment}, I am confident in my ability to streamline software delivery processes for your mission-critical applications. Furthermore, my expertise in full-stack development, cloud infrastructure, and automation practices aligns perfectly with your need for a developer who can leverage their experiences to improve workflows for other developers.

Throughout my career, I have consistently demonstrated a strong commitment to coaching cross-functional teams on modern development methodologies and fostering a culture of collaboration and continuous improvement. I thrive in multi-team environments, where I can leverage my overall understanding of complex systems and intricate integration processes to drive efficiency and innovation.

At {company}, I am eager to contribute my skills and knowledge in tools such as Python, Java, Spring Boot, React, Cloud/Azure/AWS, Kubernetes, Docker, PostgreSQL, and modern CI/CD practices. My hands-on experience with these technologies, combined with my passion for the industry, makes me an ideal candidate for this role.

I am impressed by {company}'s accountable culture that enables teams to influence and make quick decisions. As a proactive and results-driven professional, I welcome the opportunity to shape the development of this role while contributing to the company's success.

Thank you for considering my application. I look forward to discussing how my expertise and passion can contribute to {company}'s exciting mission in developing cutting-edge solutions.

Sincerely,

Hongzhi Li

Contact Information:
Email: hongzhili01@gmail.com
Phone: 0728384299
LinkedIn: https://www.linkedin.com/in/hzl/
GitHub: https://github.com/bluehawana
Portfolio: https://www.bluehawana.com

---
Customized for: {job_title} at {company}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        return cover_letter_text
    
    async def _send_simple_job_email(self, job: dict, cv_text: str, cl_text: str) -> bool:
        """Send job application email with text documents"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_url = job.get('url', '')
            keywords = job.get('keywords', [])
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"JobHunter Automation <{self.sender_email}>"
            msg['To'] = self.target_email
            msg['Subject'] = f"🎯 Job Application Ready: {job_title} at {company}"
            
            # Create email body
            email_body = f"""Hi Hongzhi,

🎯 NEW JOB APPLICATION PROCESSED

Your JobHunter automation system has found and processed a new job opportunity:

📋 JOB DETAILS:
• Position: {job_title}
• Company: {company}
• Location: {job.get('location', 'Sweden')}
• Source: {job.get('source', 'Gmail')}
• Keywords: {', '.join(keywords[:8])}

🔗 APPLICATION LINK:
{job_url}

📄 CUSTOMIZED DOCUMENTS:
I've generated tailored CV and Cover Letter documents specifically for this position. Both documents are attached as text files and optimized for this role.

📝 JOB DESCRIPTION PREVIEW:
{job.get('description', 'No description available')[:300]}{'...' if len(job.get('description', '')) > 300 else ''}

🎯 NEXT STEPS:
1. Review the attached customized CV and Cover Letter
2. Apply directly using the job URL above
3. The documents are tailored specifically for this role and company

✨ DOCUMENT FEATURES:
• Role-specific customization for {job_title}
• Company-focused cover letter content
• ATS-optimized keywords: {', '.join(keywords[:5])}
• Professional formatting ready for submission

Status: Successfully processed
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Good luck with your application! 🚀

Best regards,
JobHunter Automation System
"""
            
            # Attach email body
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Attach CV as text file
            cv_attachment = MIMEApplication(cv_text.encode('utf-8'), _subtype='plain')
            cv_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=f"CV_{company}_{job_title.replace(' ', '_')}_Customized.txt"
            )
            msg.attach(cv_attachment)
            
            # Attach Cover Letter as text file
            cl_attachment = MIMEApplication(cl_text.encode('utf-8'), _subtype='plain')
            cl_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=f"CoverLetter_{company}_{job_title.replace(' ', '_')}_Customized.txt"
            )
            msg.attach(cl_attachment)
            
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent successfully to {self.target_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
            return False

async def main():
    """Main function"""
    print("🚀 Simple Working JobHunter Automation")
    print("=" * 50)
    print("✅ Bypasses LaTeX compilation issues")
    print("📧 Generates text-based CV and Cover Letters")
    print("📤 Sends applications via email")
    print("🎯 Fully functional automation")
    print("=" * 50)
    
    # Initialize and run automation
    automation = SimpleWorkingAutomation()
    await automation.scan_and_process_jobs()

if __name__ == "__main__":
    asyncio.run(main())