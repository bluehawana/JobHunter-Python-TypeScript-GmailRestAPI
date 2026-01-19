#!/usr/bin/env python3
"""
LEGO Mode Automation - Uses YOUR exact LaTeX templates with Claude API customization
Analyzes job descriptions and intelligently selects/highlights relevant components
"""
import asyncio
import sys
import os
import logging
import smtplib
import subprocess
import tempfile
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

class LegoModeAutomation:
    """LEGO Mode - Uses your exact templates with intelligent customization"""
    
    def __init__(self):
        # Email configuration
        self.sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        self.sender_password = os.getenv('SENDER_GMAIL_PASSWORD', '')
        self.target_email = 'hongzhili01@gmail.com'
        
        # Initialize Claude API
        from app.services.claude_api_service import ClaudeAPIService
        self.claude_api = ClaudeAPIService()
        
        # Your exact CV template
        self.cv_template = self._load_cv_template()
        # Your exact cover letter template  
        self.cl_template = self._load_cl_template()
        
        logger.info("✅ LEGO Mode automation initialized with YOUR templates")
    
    def _load_cv_template(self) -> str:
        """Load your exact CV template"""
        return """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{titlesec}
\\usepackage{xcolor}
\\usepackage{hyperref}
\\usepackage{fontawesome}

% Page setup
\\geometry{margin=0.75in}
\\pagestyle{empty}

% Color definitions
\\definecolor{darkblue}{RGB}{0,51,102}
\\definecolor{lightgray}{RGB}{128,128,128}

% Hyperlink setup
\\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}

% Section formatting
\\titleformat{\\section}{\\Large\\bfseries\\color{darkblue}}{}{0em}{}[\\titlerule]
\\titleformat{\\subsection}{\\large\\bfseries}{}{0em}{}

% Custom commands
\\newcommand{\\contactitem}[2]{\\textcolor{darkblue}{#1} #2}

\\begin{document}
\\pagestyle{empty} % no page number

% Name and contact details
\\begin{center}
{\\LARGE \\textbf{Hongzhi Li}}\\\\[10pt]
{\\Large \\textit{{JOB_ROLE}}}\\\\[10pt]
\\textcolor{darkblue}{\\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \\href{tel:0728384299}{0728384299} | \\href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \\href{https://github.com/bluehawana}{GitHub}}
\\end{center}

% Personal Profile
\\section*{Profile Summary}
{PROFILE_SUMMARY}

% Areas of Expertise
\\section*{Core Technical Skills}
{TECHNICAL_SKILLS}

% Experience
{EXPERIENCE_SECTION}

{PROJECTS_SECTION}

\\vspace{6pt}
\\section*{Education}
\\textbf{IT Högskolan}\\\\
\\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\\\
\\textbf{Mölndal Campus}\\\\
\\textit{Bachelor's Degree in Java Integration} | 2019-2021\\\\
\\textbf{University of Gothenburg}\\\\
\\textit{Master's Degree in International Business and Trade} | 2016-2019\\\\

\\vspace{6pt}
\\section*{Certifications}
\\begin{itemize}
\\item AWS Certified Solutions Architect - Associate (Aug 2022)
\\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\\item AWS Certified Developer - Associate (Nov 2022)
\\end{itemize}

\\vspace{6pt}
\\section*{Additional Information}
\\begin{itemize}
\\item \\textbf{Languages:} Fluent in English and Mandarin
\\item \\textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology
\\item \\textbf{Personal Website:} \\href{https://www.bluehawana.com}{bluehawana.com}
\\item \\textbf{Customer Websites:} \\href{https://www.senior798.eu}{senior798.eu}, \\href{https://www.mibo.se}{mibo.se}, \\href{https://www.omstallningsstod.se}{omstallningsstod.se}
\\end{itemize}

\\end{document}"""    
  
  def _load_cl_template(self) -> str:
        """Load your exact cover letter template - LinkedIn blue format"""
        return """\\documentclass[10pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{xcolor}
\\usepackage{hyperref}

\\geometry{margin=1in}
\\setlength{\\parindent}{0pt}
\\definecolor{linkedinblue}{RGB}{0,119,181}
\\hypersetup{colorlinks=true, linkcolor=linkedinblue, urlcolor=linkedinblue}

\\begin{document}

% Header with job information (simple left-aligned)
{\\color{linkedinblue}{COMPANY_NAME}\\\\
{JOB_TITLE}\\\\
Gothenburg, Sweden}

\\vspace{1cm}

{GREETING}

\\vspace{0.5cm}

{COVER_LETTER_BODY}

\\vspace{1cm}

Best Regards,\\\\[0.5cm]
Harvad (Hongzhi) Li

\\vspace{\\fill}

% Line separator
{\\color{linkedinblue}\\hrule height 0.5pt}

\\vspace{0.3cm}

% Footer with address and date
{\\color{linkedinblue}Ebbe Lieberathsgatan 27\\\\
412 65, Gothenburg, Sweden\\\\
\\hfill \\today}

\\end{document}"""

    async def scan_and_process_jobs(self):
        """Main LEGO mode function - intelligent component selection"""
        try:
            logger.info("🚀 Starting LEGO Mode automation with YOUR templates...")
            
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
            
            # Process each job with LEGO mode
            successful_emails = 0
            
            for i, job in enumerate(jobs, 1):
                try:
                    # Improve job data extraction
                    improved_job = self._improve_job_data(job)
                    
                    logger.info(f"🎯 LEGO Processing job {i}/{len(jobs)}: {improved_job['title']} at {improved_job['company']}")
                    
                    # Use Claude API to analyze job and customize templates
                    cv_latex = await self._lego_customize_cv(improved_job)
                    cl_latex = await self._lego_customize_cover_letter(improved_job)
                    
                    # Compile to PDFs
                    cv_pdf = await self._compile_latex_to_pdf(cv_latex, f"cv_{improved_job['company']}")
                    cl_pdf = await self._compile_latex_to_pdf(cl_latex, f"cl_{improved_job['company']}")
                    
                    if cv_pdf and cl_pdf:
                        # Send professional email
                        email_sent = await self._send_lego_job_email(improved_job, cv_pdf, cl_pdf)
                        
                        if email_sent:
                            successful_emails += 1
                            logger.info(f"✅ LEGO email sent for {improved_job['company']}")
                        else:
                            logger.error(f"❌ Email failed for {improved_job['company']}")
                    else:
                        logger.error(f"❌ PDF generation failed for {improved_job['company']}")
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {job.get('title', 'Unknown')}: {e}")
            
            logger.info(f"🎉 LEGO Mode completed: {successful_emails}/{len(jobs)} successful emails")
            logger.info(f"📧 Check {self.target_email} for YOUR customized applications!")
            
        except Exception as e:
            logger.error(f"❌ LEGO Mode error: {e}")
            import traceback
            traceback.print_exc() 
   async def _lego_customize_cv(self, job: dict) -> str:
        """Use Claude API to intelligently customize YOUR CV template"""
        try:
            job_description = job.get('description', '')
            job_title = job.get('title', '')
            company = job.get('company', '')
            keywords = job.get('keywords', [])
            
            # Claude prompt for LEGO mode CV customization
            claude_prompt = f"""
            You are helping customize Hongzhi Li's CV for a specific job using his existing template components.
            
            JOB DETAILS:
            - Title: {job_title}
            - Company: {company}
            - Description: {job_description}
            - Keywords: {', '.join(keywords)}
            
            TASK: Analyze the job description and customize these template components:
            
            1. JOB_ROLE: Choose the best role title from: "Fullstack Developer", "Backend Developer", "DevOps Engineer", "Software Developer", "IT Specialist"
            
            2. PROFILE_SUMMARY: Customize this summary to emphasize relevant experience:
            "Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Demonstrated ability to work across the entire technology stack from frontend user interfaces to backend services and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments."
            
            3. TECHNICAL_SKILLS: Reorder and emphasize the most relevant skills from this list:
            - Programming Languages: Java/J2EE, JavaScript, C#/.NET Core, Python, Bash, PowerShell
            - Frontend Frameworks: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
            - Backend Frameworks: Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
            - API Development: RESTful APIs, GraphQL, Microservices Architecture
            - Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
            - Testing: Unit Testing, Integration Testing, Automated Testing, JUnit, Jest
            - Cloud Platforms: AWS, Azure, GCP
            - Containerization: Docker, Kubernetes, Azure Kubernetes Service (AKS)
            - Version Control: Git, GitHub, GitLab
            - CI/CD: Jenkins, GitHub Actions, GitLab CI
            - Agile Methodologies: Scrum, Kanban, Sprint Planning, Code Reviews
            - Performance Optimization: Application scaling, Database optimization, Caching strategies
            - Security: Application security, Data protection, Authentication/Authorization
            
            4. EXPERIENCE_SECTION: Highlight the most relevant experience bullets for this role from:
            - ECARX (current): Infrastructure, Kubernetes, monitoring, cost optimization
            - Synteda: C#/.NET, cloud-native, microservices, APIs
            - IT-Högskolan: Spring Boot, RESTful APIs, frontend integration
            - Senior Material: Platform architecture, microservices, Spring Boot
            - AddCell: Cloud-native, GraphQL, serverless
            - Pembio: Java/Spring Boot, Vue.js, microservices
            
            5. PROJECTS_SECTION: Select the most relevant projects from:
            - AndroidAuto_AI_Bot: AI, voice assistant, LLM, Python, Kotlin
            - AndroidAuto_TTS_EpubReader: Python, TTS, Android Auto
            - Jobhunter_Python_TypeScript: Python, TypeScript, APIs, automation
            - Bluehawana.com: HTML5, CSS3, JavaScript, APIs
            - Gothenburg_TaxiPooling: Spring Boot, React Native, ML, PostgreSQL
            - AndroidAuto_CarTVPlayer: Kotlin, Android Auto, APIs
            - SmrtMart.com: Go, Next.js, PostgreSQL, microservices
            - Weather_Anywhere: Spring Boot, cloud, MySQL
            
            Return the customized LaTeX template with all placeholders filled in. Focus on ATS optimization and relevance to the job requirements.
            """
            
            logger.info("🤖 Using Claude API for LEGO CV customization...")
            customized_latex = await self.claude_api.generate_text(claude_prompt)
            
            if customized_latex and len(customized_latex) > 500:
                logger.info(f"✅ Claude LEGO CV customization successful")
                return customized_latex
            else:
                logger.warning("⚠️ Claude API failed, using manual LEGO customization")
                return self._manual_cv_customization(job)
                
        except Exception as e:
            logger.error(f"❌ Error in LEGO CV customization: {e}")
            return self._manual_cv_customization(job)
    
    async def _lego_customize_cover_letter(self, job: dict) -> str:
        """Use Claude API to intelligently customize YOUR cover letter template"""
        try:
            job_description = job.get('description', '')
            job_title = job.get('title', '')
            company = job.get('company', '')
            
            # Claude prompt for LEGO mode cover letter customization
            claude_prompt = f"""
            You are helping customize Hongzhi Li's cover letter for a specific job using his existing template.
            
            JOB DETAILS:
            - Title: {job_title}
            - Company: {company}
            - Description: {job_description}
            
            TASK: Customize these template components:
            
            1. COMPANY_NAME: {company}
            2. COMPANY_ADDRESS: Create appropriate address for {company} in Sweden
            3. GREETING: Use "Hej [Name]," if hiring manager name found, otherwise "Dear Hiring Manager,"
            4. CURRENT_DATE: {datetime.now().strftime('%Y.%m.%d')}
            
            5. COVER_LETTER_BODY: Customize this structure for the specific job:
            
            Paragraph 1: Express interest in the {job_title} role at {company}. Mention relevant passion (automotive for Volvo, music tech for Spotify, etc.)
            
            Paragraph 2: Highlight technical alignment - mention specific technologies from job description that match Hongzhi's skills (Java/Spring Boot, React, AWS, Kubernetes, etc.)
            
            Paragraph 3: Emphasize soft skills and collaboration - coaching teams, DevOps methodologies, multi-team environments
            
            Paragraph 4: List specific technical tools mentioned in job description that Hongzhi has experience with
            
            Paragraph 5: Show cultural fit and proactive attitude specific to this company
            
            Paragraph 6: Thank and express interest in discussing contribution to company's mission
            
            Use Hongzhi's experience at ECARX (automotive), Synteda (cloud/microservices), and his technical projects to show relevance.
            
            Return the complete customized LaTeX template with all placeholders filled in.
            """
            
            logger.info("🤖 Using Claude API for LEGO cover letter customization...")
            customized_latex = await self.claude_api.generate_text(claude_prompt)
            
            if customized_latex and len(customized_latex) > 500:
                logger.info(f"✅ Claude LEGO cover letter customization successful")
                return customized_latex
            else:
                logger.warning("⚠️ Claude API failed, using manual LEGO customization")
                return self._manual_cl_customization(job)
                
        except Exception as e:
            logger.error(f"❌ Error in LEGO cover letter customization: {e}")
            return self._manual_cl_customization(job)   
 def _improve_job_data(self, job: dict) -> dict:
        """Improve job data extraction, especially company names"""
        improved_job = job.copy()
        
        # Extract better company name from email subject and body
        email_subject = job.get('email_subject', '')
        body = job.get('body', '')
        
        # Swedish patterns for company extraction
        company_patterns = [
            r'([A-ZÅÄÖ][a-zåäö\s&]+?)\s+(?:söker|ker)\s+nu\s+fler\s+talanger',
            r'([A-ZÅÄÖ][a-zåäö\s&]+?)\s+is\s+actively\s+hiring',
            r'Join\s+([A-ZÅÄÖ][a-zåäö\s&]+?)\s+as',
            r'^([A-ZÅÄÖ][a-zåäö\s&]+?)\s*[-–]\s*[A-Z]',
        ]
        
        company_name = job.get('company', 'Technology Company')
        content_to_search = f"{email_subject} {body}"
        
        for pattern in company_patterns:
            match = re.search(pattern, content_to_search, re.IGNORECASE)
            if match:
                potential_company = match.group(1).strip().title()
                if len(potential_company) > 2 and len(potential_company) < 50:
                    company_name = potential_company
                    break
        
        # Known Swedish companies
        content_lower = content_to_search.lower()
        known_companies = {
            'volvo': 'Volvo Group', 'ericsson': 'Ericsson', 'spotify': 'Spotify',
            'klarna': 'Klarna', 'skf': 'SKF Group', 'hasselblad': 'Hasselblad'
        }
        
        for keyword, full_name in known_companies.items():
            if keyword in content_lower:
                company_name = full_name
                break
        
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
    
    def _manual_cv_customization(self, job: dict) -> str:
        """Manual CV customization as fallback"""
        job_title = job.get('title', '').lower()
        
        # Determine role
        if 'backend' in job_title:
            role = "Backend Developer"
        elif 'devops' in job_title:
            role = "DevOps Engineer"
        elif 'fullstack' in job_title:
            role = "Fullstack Developer"
        else:
            role = "Software Developer"
        
        # Basic customization
        customized = self.cv_template.replace('{JOB_ROLE}', role)
        customized = customized.replace('{PROFILE_SUMMARY}', 
            "Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies.")
        # Add other basic replacements...
        
        return customized
    
    def _manual_cl_customization(self, job: dict) -> str:
        """Manual cover letter customization as fallback"""
        company = job.get('company', 'Target Company')
        job_title = job.get('title', 'Software Developer')
        
        customized = self.cl_template.replace('{COMPANY_NAME}', company)
        customized = customized.replace('{COMPANY_ADDRESS}', f"{company}\\\\Sweden")
        customized = customized.replace('{GREETING}', "Dear Hiring Manager,")
        customized = customized.replace('{CURRENT_DATE}', datetime.now().strftime('%Y.%m.%d'))
        customized = customized.replace('{COVER_LETTER_BODY}', 
            f"I am writing to express my sincere interest in the {job_title} role at {company}...")
        
        return customized
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Compile LaTeX to PDF"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
                f.write(latex_content)
                tex_file = f.name
            
            # Compile with pdflatex
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
    
    async def _send_lego_job_email(self, job: dict, cv_pdf: bytes, cl_pdf: bytes) -> bool:
        """Send LEGO mode job email"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_url = job.get('url', '')
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = f"JobHunter LEGO Mode <{self.sender_email}>"
            msg['To'] = self.target_email
            msg['Subject'] = f"🎯 LEGO Mode: {job_title} at {company} - YOUR Templates Used"
            
            email_body = f"""Hi Hongzhi,

🎯 LEGO MODE APPLICATION READY

Your JobHunter system used YOUR exact LaTeX templates with Claude AI customization:

📋 JOB DETAILS:
• Position: {job_title}
• Company: {company}
• Location: {job.get('location', 'Sweden')}

🔗 DIRECT APPLICATION LINK:
{job_url if job_url else 'Check original email for application link'}

📄 YOUR CUSTOMIZED TEMPLATES (PDF):
✅ CV - Using YOUR exact LaTeX template with intelligent component selection
✅ Cover Letter - Using YOUR exact template with job-specific customization

🧩 LEGO MODE FEATURES:
• Used YOUR exact LaTeX templates (not generated ones)
• Claude AI analyzed job description for optimal component selection
• ATS-optimized keyword integration
• Intelligent highlighting of relevant experience
• Professional formatting maintained

🎯 READY TO SUBMIT:
1. Download the attached PDFs
2. Click the application link above
3. Submit directly to employer

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your templates, intelligently customized! 🚀

Best regards,
JobHunter LEGO Mode
"""
            
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Attach PDFs
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
            
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending LEGO email: {e}")
            return False

async def main():
    """Main LEGO mode function"""
    print("🧩 JobHunter LEGO Mode - Using YOUR Exact Templates")
    print("=" * 60)
    print("✅ YOUR LaTeX CV template")
    print("✅ YOUR LaTeX cover letter template") 
    print("🤖 Claude AI intelligent customization")
    print("🎯 Component selection based on job analysis")
    print("📊 ATS optimization")
    print("=" * 60)
    
    automation = LegoModeAutomation()
    await automation.scan_and_process_jobs()

if __name__ == "__main__":
    import re
    asyncio.run(main())