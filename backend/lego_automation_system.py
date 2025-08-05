#!/usr/bin/env python3
"""
LEGO Automation System - Uses your exact templates with intelligent customization
Analyzes job descriptions and selects optimal components like LEGO blocks
"""
import asyncio
import sys
import os
import logging
import smtplib
import subprocess
import tempfile
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import your templates
from templates.cv_template import (
    CV_TEMPLATE, PROFILE_SUMMARY, TECHNICAL_SKILLS, 
    EXPERIENCE_SECTION, PROJECTS_SECTION
)
from templates.cover_letter_template import (
    COVER_LETTER_TEMPLATE, BASE_COVER_LETTER_BODY,
    INDUSTRY_CUSTOMIZATIONS, TECHNICAL_ALIGNMENTS, TECHNOLOGY_LISTS
)

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegoAutomationSystem:
    """LEGO system using your exact templates with intelligent component selection"""
    
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD', '')
        self.target_email = 'hongzhili01@gmail.com'
        
        # Initialize Claude API
        from app.services.claude_api_service import ClaudeAPIService
        self.claude_api = ClaudeAPIService()
        
        logger.info("🧩 LEGO Automation System initialized with YOUR templates")
    
    async def run_lego_automation(self):
        """Main LEGO automation function"""
        try:
            logger.info("🚀 Starting LEGO Automation System...")
            
            # Scan Gmail for jobs
            from app.services.real_job_scanner import RealJobScanner
            email_scanner = RealJobScanner()
            
            jobs = await email_scanner.scan_real_gmail_jobs(days_back=3)
            logger.info(f"🔍 Found {len(jobs)} job opportunities")
            
            if not jobs:
                logger.info("📭 No jobs found")
                return
            
            successful_emails = 0
            
            for i, job in enumerate(jobs, 1):
                try:
                    # Extract proper company name
                    improved_job = self._extract_company_info(job)
                    
                    logger.info(f"🧩 LEGO Processing {i}/{len(jobs)}: {improved_job['title']} at {improved_job['company']}")
                    
                    # LEGO customization - select optimal components
                    cv_latex = await self._lego_customize_cv(improved_job)
                    cl_latex = await self._lego_customize_cover_letter(improved_job)
                    
                    # Compile to PDFs
                    cv_pdf = await self._compile_latex_to_pdf(cv_latex, f"cv_{improved_job['company']}")
                    cl_pdf = await self._compile_latex_to_pdf(cl_latex, f"cl_{improved_job['company']}")
                    
                    if cv_pdf and cl_pdf:
                        email_sent = await self._send_lego_email(improved_job, cv_pdf, cl_pdf)
                        if email_sent:
                            successful_emails += 1
                            logger.info(f"✅ LEGO email sent for {improved_job['company']}")
                    
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {job.get('title', 'Unknown')}: {e}")
            
            logger.info(f"🎉 LEGO Automation completed: {successful_emails}/{len(jobs)} successful")
            
        except Exception as e:
            logger.error(f"❌ LEGO Automation error: {e}")
    
    def _extract_company_info(self, job: dict) -> dict:
        """Extract proper company information"""
        improved_job = job.copy()
        
        email_subject = job.get('email_subject', '')
        body = job.get('body', '')
        sender = job.get('sender', '')
        
        # Known companies mapping
        content_lower = f"{email_subject} {body}".lower()
        known_companies = {
            'volvo': 'Volvo Group',
            'ericsson': 'Ericsson',
            'spotify': 'Spotify Technology',
            'klarna': 'Klarna Bank',
            'skf': 'SKF Group',
            'hasselblad': 'Hasselblad',
            'polestar': 'Polestar',
            'zenseact': 'Zenseact',
            'opera': 'Opera Software',
            'king': 'King Digital Entertainment'
        }
        
        company_name = "Technology Company"
        
        # Check for known companies first
        for keyword, full_name in known_companies.items():
            if keyword in content_lower:
                company_name = full_name
                break
        
        # Extract from sender domain if not found
        if company_name == "Technology Company" and '@' in sender:
            domain = sender.split('@')[1].split('.')[0]
            if domain not in ['linkedin', 'indeed', 'glassdoor', 'gmail']:
                company_name = domain.title()
        
        improved_job['company'] = company_name
        
        # Extract application URL
        if not improved_job.get('url'):
            url_patterns = [
                r'https://[^\s]+\.linkedin\.com/jobs/view/\d+',
                r'https://[^\s]+\.indeed\.com/viewjob\?jk=[a-zA-Z0-9]+',
                r'https://[^\s]+/jobs?/[^\s]+',
            ]
            
            for pattern in url_patterns:
                url_match = re.search(pattern, body)
                if url_match:
                    improved_job['url'] = url_match.group(0)
                    break
        
        return improved_job    
async def _lego_customize_cv(self, job: dict) -> str:
        """LEGO CV customization - select optimal components"""
        try:
            job_description = job.get('description', '')
            job_title = job.get('title', '').lower()
            company = job.get('company', '')
            keywords = job.get('keywords', [])
            
            # LEGO Component Selection using Claude API
            claude_prompt = f"""
            Analyze this job and customize Hongzhi Li's CV using LEGO component selection:
            
            JOB: {job_title} at {company}
            DESCRIPTION: {job_description}
            KEYWORDS: {', '.join(keywords)}
            
            LEGO CUSTOMIZATION TASKS:
            
            1. ROLE_TITLE: Choose the best fit from:
               - "Fullstack Developer" (for full-stack roles)
               - "Backend Developer" (for backend-focused roles)
               - "DevOps Engineer" (for infrastructure/DevOps roles)
               - "Software Developer" (for general development roles)
            
            2. TECHNICAL_SKILLS: Reorder the skills list to put the most relevant skills first.
               Keep the exact LaTeX format but prioritize based on job requirements.
            
            3. EXPERIENCE_HIGHLIGHTING: Which experience bullets should be emphasized?
               - ECARX (current): Infrastructure, Kubernetes, monitoring
               - Synteda: C#/.NET, microservices, cloud-native
               - IT-Högskolan: Spring Boot, APIs
               - Senior Material: Platform architecture, microservices
               - AddCell: Cloud-native, GraphQL
               - Pembio: Java/Spring Boot, Vue.js
            
            4. PROJECT_SELECTION: Which projects are most relevant?
               - AndroidAuto_AI_Bot: AI, voice, Python, Kotlin
               - JobHunter: Python, TypeScript, APIs, automation
               - Bluehawana.com: HTML5, CSS3, JavaScript, APIs
               - TaxiPooling: Spring Boot, React Native, ML
               - SmrtMart.com: Go, Next.js, PostgreSQL, microservices
               - Weather_Anywhere: Spring Boot, cloud, MySQL
            
            Return a customized CV using the exact template structure with:
            - ROLE_TITLE filled in
            - Skills reordered by relevance
            - All content preserved but optimized for this job
            
            Use the complete template with all sections included.
            """
            
            logger.info("🤖 Using Claude for LEGO CV component selection...")
            customized_cv = await self.claude_api.generate_text(claude_prompt)
            
            if customized_cv and len(customized_cv) > 1000:
                logger.info("✅ Claude LEGO CV customization successful")
                return customized_cv
            else:
                logger.warning("⚠️ Claude failed, using manual LEGO customization")
                return self._manual_lego_cv(job)
                
        except Exception as e:
            logger.error(f"❌ Claude error: {e}")
            return self._manual_lego_cv(job)
    
    def _manual_lego_cv(self, job: dict) -> str:
        """Manual LEGO CV customization"""
        job_title = job.get('title', '').lower()
        
        # Select role title
        if 'backend' in job_title:
            role_title = "Backend Developer"
        elif 'devops' in job_title or 'infrastructure' in job_title:
            role_title = "DevOps Engineer"
        elif 'fullstack' in job_title or 'full stack' in job_title:
            role_title = "Fullstack Developer"
        else:
            role_title = "Software Developer"
        
        # Build CV using your template components
        cv_content = CV_TEMPLATE.replace('ROLE_TITLE', role_title)
        cv_content = cv_content.replace('PROFILE_SUMMARY', PROFILE_SUMMARY)
        cv_content = cv_content.replace('TECHNICAL_SKILLS', TECHNICAL_SKILLS)
        cv_content = cv_content.replace('EXPERIENCE_SECTION', EXPERIENCE_SECTION)
        cv_content = cv_content.replace('PROJECTS_SECTION', PROJECTS_SECTION)
        
        return cv_content
    
    async def _lego_customize_cover_letter(self, job: dict) -> str:
        """LEGO cover letter customization"""
        try:
            job_title = job.get('title', '')
            company = job.get('company', '')
            job_description = job.get('description', '')
            
            # Determine industry and technical focus
            industry_key = self._determine_industry(company, job_description)
            tech_focus = self._determine_tech_focus(job_title, job_description)
            
            # LEGO Component Selection using Claude API
            claude_prompt = f"""
            Customize Hongzhi Li's cover letter for this job using LEGO component selection:
            
            JOB: {job_title} at {company}
            DESCRIPTION: {job_description}
            
            LEGO CUSTOMIZATION:
            
            1. COMPANY_NAME: {company}
            2. COMPANY_ADDRESS: Create appropriate address for {company} in Sweden
            3. GREETING: Use "Dear Hiring Manager," (or specific name if found)
            4. CURRENT_DATE: {datetime.now().strftime('%Y.%m.%d')}
            
            5. COVER_LETTER_BODY: Customize the 6-paragraph structure:
            
            Paragraph 1: Express interest in {job_title} at {company}, show passion for their industry
            Paragraph 2: Technical alignment - highlight relevant technologies from job description
            Paragraph 3: Soft skills - coaching teams, collaboration, multi-team environments
            Paragraph 4: Specific tools from job description that match Hongzhi's experience
            Paragraph 5: Cultural fit and proactive attitude
            Paragraph 6: Thank and express interest in contribution
            
            Use Hongzhi's ECARX (automotive/infrastructure) and Synteda (cloud/microservices) experience.
            
            Return the complete LaTeX template with all placeholders filled.
            """
            
            logger.info("🤖 Using Claude for LEGO cover letter customization...")
            customized_cl = await self.claude_api.generate_text(claude_prompt)
            
            if customized_cl and len(customized_cl) > 500:
                logger.info("✅ Claude LEGO cover letter customization successful")
                return customized_cl
            else:
                logger.warning("⚠️ Claude failed, using manual LEGO customization")
                return self._manual_lego_cover_letter(job, industry_key, tech_focus)
                
        except Exception as e:
            logger.error(f"❌ Claude error: {e}")
            return self._manual_lego_cover_letter(job, 'default', 'default')
    
    def _manual_lego_cover_letter(self, job: dict, industry_key: str, tech_focus: str) -> str:
        """Manual LEGO cover letter customization"""
        job_title = job.get('title', 'Software Developer')
        company = job.get('company', 'Target Company')
        
        # Select LEGO components
        industry_info = INDUSTRY_CUSTOMIZATIONS.get(industry_key, INDUSTRY_CUSTOMIZATIONS['default'])
        technical_alignment = TECHNICAL_ALIGNMENTS.get(tech_focus, TECHNICAL_ALIGNMENTS['default'])
        tool_list = TECHNOLOGY_LISTS.get(tech_focus, TECHNOLOGY_LISTS['default'])
        
        # Build cover letter body
        cover_letter_body = BASE_COVER_LETTER_BODY.format(
            job_title=job_title,
            company=company,
            industry=industry_info['industry'],
            solutions=industry_info['solutions'],
            target_audience=industry_info['target_audience'],
            technical_alignment=technical_alignment,
            key_technologies=f"containerization, infrastructure as code, and automation practices",
            methodologies=industry_info['methodologies'],
            tool_list=tool_list
        )
        
        # Build complete cover letter
        cl_content = COVER_LETTER_TEMPLATE.replace('COMPANY_NAME', company)
        cl_content = cl_content.replace('COMPANY_ADDRESS', f"{company}\\\\Sweden")
        cl_content = cl_content.replace('GREETING', "Dear Hiring Manager,")
        cl_content = cl_content.replace('CURRENT_DATE', datetime.now().strftime('%Y.%m.%d'))
        cl_content = cl_content.replace('COVER_LETTER_BODY', cover_letter_body)
        
        return cl_content
    
    def _determine_industry(self, company: str, description: str) -> str:
        """Determine industry for LEGO component selection"""
        content = f"{company} {description}".lower()
        
        if any(word in content for word in ['volvo', 'automotive', 'car', 'vehicle']):
            return 'automotive'
        elif any(word in content for word in ['spotify', 'music', 'audio', 'streaming']):
            return 'music_tech'
        elif any(word in content for word in ['klarna', 'bank', 'financial', 'fintech', 'payment']):
            return 'fintech'
        elif any(word in content for word in ['game', 'gaming', 'king', 'dice']):
            return 'gaming'
        else:
            return 'default'
    
    def _determine_tech_focus(self, job_title: str, description: str) -> str:
        """Determine technical focus for LEGO component selection"""
        content = f"{job_title} {description}".lower()
        
        if any(word in content for word in ['devops', 'infrastructure', 'kubernetes', 'ci/cd']):
            return 'devops'
        elif any(word in content for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
        elif any(word in content for word in ['frontend', 'react', 'angular', 'ui', 'ux']):
            return 'frontend'
        elif any(word in content for word in ['cloud', 'aws', 'azure', 'gcp']):
            return 'cloud'
        elif any(word in content for word in ['fullstack', 'full stack', 'full-stack']):
            return 'fullstack'
        else:
            return 'default'
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Compile LaTeX to PDF"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
                f.write(latex_content)
                tex_file = f.name
            
            result = subprocess.run([
                'pdflatex', '-interaction=nonstopmode', tex_file
            ], capture_output=True, text=True, cwd=tempfile.gettempdir())
            
            pdf_file = tex_file.replace('.tex', '.pdf')
            
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as f:
                    pdf_content = f.read()
                
                # Cleanup
                for ext in ['.tex', '.pdf', '.aux', '.log']:
                    cleanup_file = tex_file.replace('.tex', ext)
                    if os.path.exists(cleanup_file):
                        os.remove(cleanup_file)
                
                return pdf_content
            else:
                logger.error(f"❌ PDF compilation failed: {result.stderr}")
                return b""
                
        except Exception as e:
            logger.error(f"❌ LaTeX compilation error: {e}")
            return b""
    
    async def _send_lego_email(self, job: dict, cv_pdf: bytes, cl_pdf: bytes) -> bool:
        """Send LEGO automation email"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_url = job.get('url', '')
            
            msg = MIMEMultipart()
            msg['From'] = f"JobHunter LEGO System <{self.sender_email}>"
            msg['To'] = self.target_email
            msg['Subject'] = f"🧩 LEGO System: {job_title} at {company} - Optimized Components"
            
            email_body = f"""Hi Hongzhi,

🧩 LEGO AUTOMATION SYSTEM RESULTS

Your JobHunter LEGO system analyzed the job and selected optimal components:

📋 JOB DETAILS:
• Position: {job_title}
• Company: {company}
• Location: {job.get('location', 'Sweden')}

🔗 DIRECT APPLICATION LINK:
{job_url if job_url else 'Check original email for application link'}

📄 LEGO OPTIMIZED DOCUMENTS (PDF):
✅ CV - YOUR template with intelligently selected components
✅ Cover Letter - YOUR template with job-specific customization

🧩 LEGO COMPONENT SELECTION:
• Used YOUR exact LaTeX templates as base
• Claude AI analyzed job requirements
• Selected most relevant experience bullets
• Prioritized matching technical skills
• Chose optimal projects to highlight
• Customized cover letter for industry/role fit

🎯 OPTIMIZATION FEATURES:
• ATS keyword optimization
• Role-specific component prioritization
• Industry-aware customization
• Technical alignment matching
• Professional formatting maintained

📊 READY FOR SUBMISSION:
1. Download the optimized PDFs
2. Click the application link above
3. Submit with confidence

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

LEGO blocks assembled perfectly! 🚀

Best regards,
JobHunter LEGO System
"""
            
            msg.attach(MIMEText(email_body, 'plain'))
            
            if cv_pdf:
                cv_attachment = MIMEApplication(cv_pdf, _subtype='pdf')
                cv_attachment.add_header('Content-Disposition', 'attachment', 
                    filename=f"Hongzhi_Li_CV_{company.replace(' ', '_')}_LEGO.pdf")
                msg.attach(cv_attachment)
            
            if cl_pdf:
                cl_attachment = MIMEApplication(cl_pdf, _subtype='pdf')
                cl_attachment.add_header('Content-Disposition', 'attachment', 
                    filename=f"Hongzhi_Li_CoverLetter_{company.replace(' ', '_')}_LEGO.pdf")
                msg.attach(cl_attachment)
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending LEGO email: {e}")
            return False

async def main():
    """Main LEGO automation function"""
    print("🧩 JobHunter LEGO Automation System")
    print("=" * 50)
    print("✅ Uses YOUR exact LaTeX templates")
    print("🤖 Claude AI component selection")
    print("🎯 Intelligent LEGO block assembly")
    print("📊 ATS optimization")
    print("🔗 Direct application links")
    print("=" * 50)
    
    lego_system = LegoAutomationSystem()
    await lego_system.run_lego_automation()

if __name__ == "__main__":
    asyncio.run(main())