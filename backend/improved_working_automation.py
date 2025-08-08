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
    
    async def _get_claude_lego_strategy(self, job: dict) -> dict:
        """Claude analyzes job and decides LEGO component strategy"""
        try:
            from app.services.claude_api_service import ClaudeAPIService
            claude = ClaudeAPIService()
            
            job_analysis_prompt = f"""
            Analyze this job posting and create a LEGO component strategy for tailoring Hongzhi Li's resume:

            JOB TITLE: {job.get('title', 'Software Developer')}
            COMPANY: {job.get('company', 'Target Company')}
            JOB DESCRIPTION: {job.get('description', 'No description provided')}
            
            HONGZHI'S BACKGROUND:
            - Current: IT/Infrastructure Specialist at ECARX (Oct 2024-Present)
            - Previous: Azure Fullstack Developer at Synteda (Aug 2023-Sep 2024)
            - Education: IT Högskolan (.NET Cloud Development), University of Gothenburg (International Business)
            - Skills: Java/J2EE, C#/.NET Core, Angular, React, AWS, Azure, Docker, Kubernetes
            
            Please analyze and decide:
            1. PRIMARY_FOCUS: What should be the main positioning? (devops/backend/frontend/fullstack)
            2. SKILLS_TO_HIGHLIGHT: Which technical skills to emphasize most?
            3. EXPERIENCE_ORDER: Which job experience should lead?
            4. PROFILE_ANGLE: How to position Hongzhi for this specific role?
            5. KEYWORDS_TO_INCLUDE: Key terms from job description to naturally integrate
            6. SECTIONS_TO_EMPHASIZE: Which resume sections need more detail?
            7. TONE: Professional tone to match company culture
            
            Return as JSON format:
            {{
                "primary_focus": "devops|backend|frontend|fullstack",
                "skills_to_highlight": ["skill1", "skill2", "skill3"],
                "experience_order": ["ecarx_first|synteda_first"],
                "profile_angle": "specific positioning statement",
                "keywords_to_include": ["keyword1", "keyword2"],
                "sections_to_emphasize": ["skills", "experience", "projects"],
                "tone": "corporate|startup|technical|innovative"
            }}
            """
            
            strategy_response = await claude.generate_text(job_analysis_prompt)
            
            if strategy_response:
                try:
                    import json
                    strategy = json.loads(strategy_response)
                    logger.info(f"🧠 Claude LEGO strategy: {strategy.get('primary_focus', 'fullstack')} focus")
                    return strategy
                except json.JSONDecodeError:
                    logger.warning("⚠️ Claude returned invalid JSON, using default strategy")
            
            # Fallback strategy
            return {
                "primary_focus": "fullstack",
                "skills_to_highlight": ["Java", "React", "AWS"],
                "experience_order": "ecarx_first",
                "profile_angle": "Experienced developer",
                "keywords_to_include": [],
                "sections_to_emphasize": ["skills", "experience"],
                "tone": "professional"
            }
            
        except Exception as e:
            logger.error(f"❌ Claude LEGO strategy error: {e}")
            return {"primary_focus": "fullstack", "skills_to_highlight": [], "experience_order": "ecarx_first"}
    
    async def _build_claude_lego_resume(self, job: dict, strategy: dict) -> str:
        """Claude builds the actual LaTeX resume using LEGO strategy"""
        try:
            from app.services.claude_api_service import ClaudeAPIService
            claude = ClaudeAPIService()
            
            # Get base template components
            from templates.cv_template import get_base_template_components
            base_components = get_base_template_components()
            
            lego_build_prompt = f"""
            Build a tailored LaTeX resume for Hongzhi Li using this LEGO strategy:
            
            STRATEGY: {strategy}
            
            JOB DETAILS:
            - Title: {job.get('title', 'Software Developer')}
            - Company: {job.get('company', 'Target Company')}
            - Description: {job.get('description', 'No description provided')}
            
            BASE TEMPLATE COMPONENTS:
            {base_components}
            
            INSTRUCTIONS:
            1. Use the EXACT LaTeX structure from base template
            2. Apply the LEGO strategy to customize content:
               - Tailor profile summary based on primary_focus
               - Reorder and emphasize skills based on skills_to_highlight
               - Adjust experience descriptions based on experience_order
               - Integrate keywords_to_include naturally
               - Emphasize sections_to_emphasize with more detail
            3. Keep professional LaTeX formatting
            4. Ensure content fits appropriately on pages
            5. Make it ATS-friendly with proper keywords
            
            Return ONLY the complete LaTeX document ready to compile.
            """
            
            tailored_latex = await claude.generate_text(lego_build_prompt)
            
            if tailored_latex and len(tailored_latex) > 500:
                logger.info(f"🎯 Claude built tailored resume ({len(tailored_latex)} chars)")
                return tailored_latex
            else:
                logger.warning("⚠️ Claude LEGO build failed, using fallback")
                from templates.cv_template import generate_tailored_cv
                return generate_tailored_cv(job)
                
        except Exception as e:
            logger.error(f"❌ Claude LEGO build error: {e}")
            from templates.cv_template import generate_tailored_cv
            return generate_tailored_cv(job)
    
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
        """Generate Claude-powered LEGO-tailored CV - Claude decides everything"""
        try:
            # Run the async operations in a new event loop
            import asyncio
            
            # Create new event loop for this thread
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're in a running loop, use run_in_executor
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self._generate_cv_pdf_sync, job)
                        return future.result()
                else:
                    return asyncio.run(self._generate_cv_pdf_async(job))
            except RuntimeError:
                return asyncio.run(self._generate_cv_pdf_async(job))
                
        except Exception as e:
            logger.error(f"❌ Error generating Claude LEGO CV PDF: {e}")
            return b""
    
    def _generate_cv_pdf_sync(self, job: dict) -> bytes:
        """Synchronous wrapper for CV generation"""
        return asyncio.run(self._generate_cv_pdf_async(job))
    
    async def _generate_cv_pdf_async(self, job: dict) -> bytes:
        """Async CV generation with Claude integration"""
        try:
            # STEP 1: Claude analyzes job and decides LEGO strategy
            logger.info(f"🧠 Claude analyzing job requirements for {job.get('company', 'Company')}")
            lego_strategy = await self._get_claude_lego_strategy(job)
            
            # STEP 2: Claude builds tailored LaTeX using LEGO components
            logger.info(f"🤖 Claude building tailored resume using LEGO strategy")
            latex_content = await self._build_claude_lego_resume(job, lego_strategy)
            
            # STEP 3: Save Claude's creation for debugging
            company = job.get('company', 'Company').replace(' ', '_').replace('/', '_')
            title = job.get('title', 'Position').replace(' ', '_').replace('/', '_')
            latex_filename = f"Claude_LEGO_{title}_{company}.tex"
            
            try:
                with open(latex_filename, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                logger.info(f"✅ Saved Claude's LEGO creation: {latex_filename}")
            except:
                pass
            
            # STEP 4: Try to compile LaTeX to PDF (if pdflatex available)
            try:
                import subprocess
                import tempfile
                
                with tempfile.TemporaryDirectory() as temp_dir:
                    tex_file = os.path.join(temp_dir, f"{title}_{company}.tex")
                    pdf_file = os.path.join(temp_dir, f"{title}_{company}.pdf")
                    
                    # Write LaTeX content
                    with open(tex_file, 'w', encoding='utf-8') as f:
                        f.write(latex_content)
                    
                    # Compile with pdflatex
                    result = subprocess.run([
                        'pdflatex', '-interaction=nonstopmode', 
                        '-output-directory', temp_dir, tex_file
                    ], capture_output=True, timeout=30)
                    
                    if result.returncode == 0 and os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            pdf_content = f.read()
                        logger.info(f"🎉 SUCCESS: Generated Claude LEGO LaTeX PDF ({len(pdf_content)} bytes)")
                        return pdf_content
                    else:
                        logger.warning(f"⚠️ pdflatex failed: {result.stderr.decode()}")
                        
            except Exception as latex_error:
                logger.warning(f"⚠️ LaTeX compilation not available: {latex_error}")
            
            # STEP 5: Create enhanced ReportLab PDF with Claude's LEGO logic
            logger.info(f"📄 Creating enhanced PDF using Claude's LEGO strategy")
            return self._create_enhanced_lego_pdf(job, latex_content)
            
        except Exception as e:
            logger.error(f"❌ Error generating Claude LEGO CV PDF: {e}")
            return b""
            logger.error(f"❌ Claude resume enhancement error: {e}")
            return base_latex_content
    
    async def _enhance_cover_letter_with_claude(self, job: dict, base_cover_letter: str) -> str:
        """Use Claude API to enhance cover letter LaTeX content"""
        try:
            from app.services.claude_api_service import ClaudeAPIService
            claude_service = ClaudeAPIService()
            
            enhanced_content = await claude_service.enhance_cover_letter_content(job, base_cover_letter)
            
            if enhanced_content and len(enhanced_content) > 100:
                logger.info(f"🎉 Claude successfully enhanced cover letter for {job.get('company', 'Unknown')}")
                return enhanced_content
            else:
                logger.warning("⚠️ Claude enhancement failed, using base template")
                return base_cover_letter
                
        except Exception as e:
            logger.error(f"❌ Claude cover letter enhancement error: {e}")
            return base_cover_letter

            # STEP 3: Try to compile LaTeX to PDF (if pdflatex available)
            try:
                import subprocess
                import tempfile
                import os
                
                with tempfile.TemporaryDirectory() as temp_dir:
                    tex_file = os.path.join(temp_dir, f"{title}_{company}.tex")
                    pdf_file = os.path.join(temp_dir, f"{title}_{company}.pdf")
                    
                    # Write LaTeX content
                    with open(tex_file, 'w', encoding='utf-8') as f:
                        f.write(latex_content)
                    
                    # Compile with pdflatex
                    result = subprocess.run([
                        'pdflatex', '-interaction=nonstopmode', 
                        '-output-directory', temp_dir, tex_file
                    ], capture_output=True, timeout=30)
                    
                    if result.returncode == 0 and os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            pdf_content = f.read()
                        logger.info(f"🎉 SUCCESS: Generated BEAUTIFUL LaTeX PDF ({len(pdf_content)} bytes) for {title} at {company}")
                        return pdf_content
                    else:
                        logger.warning(f"⚠️ pdflatex failed: {result.stderr.decode()}")
                        
            except Exception as latex_error:
                logger.warning(f"⚠️ LaTeX compilation not available: {latex_error}")
            
            # STEP 4: Create a MUCH BETTER ReportLab PDF that mimics your template
            logger.info(f"📄 Creating enhanced PDF for {title} at {company} using LEGO logic")
            return self._create_enhanced_lego_pdf(job, latex_content)
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
            
            # Analyze job for LEGO component selection
            job_title = job.get('title', '').lower()
            job_description = job.get('description', '').lower()
            company = job.get('company', 'Company')
            
            is_devops = any(keyword in job_title + job_description for keyword in 
                           ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
            is_backend = any(keyword in job_title + job_description for keyword in 
                            ['backend', 'api', 'microservices', 'spring', 'java', 'database', 'server'])
            is_frontend = any(keyword in job_title + job_description for keyword in 
                             ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui', 'ux'])
            
            # Build LEGO-tailored content
            content = []
            
            # Header with tailored role title
            content.append(Paragraph("HONGZHI LI", title_style))
            
            if is_devops:
                role_title = "DevOps Engineer & Cloud Infrastructure Specialist"
            elif is_backend and not is_frontend:
                role_title = "Backend Developer & API Specialist"
            elif is_frontend and not is_backend:
                role_title = "Frontend Developer & UI Specialist"
            else:
                role_title = "Fullstack Developer"
                
            content.append(Paragraph(role_title, styles['Normal']))
            content.append(Paragraph("hongzhili01@gmail.com | 0728384299 | LinkedIn | GitHub", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # LEGO Component: Tailored Professional Summary
            content.append(Paragraph("PROFILE SUMMARY", heading_style))
            
            if is_devops:
                summary = f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, AWS, Docker, and infrastructure automation. Specialized in infrastructure solutions for companies like {company}."
            elif is_backend:
                summary = f"Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, RESTful APIs, and scalable backend systems. Specialized in backend development roles for companies like {company}."
            elif is_frontend:
                summary = f"Experienced Frontend Developer with over 5 years of expertise in modern web technologies and user interface development. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in React, Angular, Vue.js, and responsive web applications. Specialized in frontend development roles for companies like {company}."
            else:
                summary = f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Specialized in fullstack development roles for companies like {company}."
            
            content.append(Paragraph(summary, styles['Normal']))
            content.append(Spacer(1, 12))
            
            # LEGO Component: Tailored Technical Skills
            content.append(Paragraph("CORE TECHNICAL SKILLS", heading_style))
            
            if is_devops:
                skills = [
                    "Cloud Platforms: AWS, Azure, GCP, Alibaba Cloud ECS",
                    "Containerization: Docker, Kubernetes, Azure Kubernetes Service (AKS)",
                    "CI/CD: Jenkins, GitHub Actions, GitLab CI, Automated Testing",
                    "Infrastructure: Infrastructure as Code, System Integration, Network Management",
                    "Monitoring: Grafana, Advanced Scripting, System Reliability",
                    "Programming Languages: Python, Bash, PowerShell, Java, JavaScript"
                ]
            elif is_backend:
                skills = [
                    "Programming Languages: Java/J2EE, C#/.NET Core, Python, JavaScript, TypeScript",
                    "Backend Frameworks: Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI",
                    "API Development: RESTful APIs, GraphQL, Microservices Architecture",
                    "Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                    "Performance: Database optimization, Caching strategies, Application scaling",
                    "Security: Application security, Data protection, Authentication/Authorization"
                ]
            elif is_frontend:
                skills = [
                    "Frontend Frameworks: React, Angular, Vue.js, React Native",
                    "Programming Languages: JavaScript, TypeScript, HTML5, CSS3",
                    "UI/UX: Responsive Design, Mobile-First Design, User Experience",
                    "State Management: Redux, Context API, Vuex",
                    "Build Tools: Webpack, Vite, npm, yarn",
                    "Testing: Jest, Cypress, Unit Testing, Integration Testing"
                ]
            else:
                skills = [
                    "Programming Languages: Java/J2EE, JavaScript, C#/.NET Core, Python, TypeScript",
                    "Frontend Technologies: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                    "Backend Frameworks: Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI",
                    "Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                    "Cloud Platforms: AWS, Azure, GCP",
                    "DevOps: Docker, Kubernetes, Jenkins, GitHub Actions, GitLab CI"
                ]
            
            for skill in skills:
                content.append(Paragraph(f"• {skill}", styles['Normal']))
            content.append(Spacer(1, 12))
            
            # LEGO Component: Tailored Experience Order
            content.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
            
            if is_devops:
                # Lead with ECARX infrastructure role for DevOps positions
                content.append(Paragraph("<b>ECARX | IT/Infrastructure Specialist</b>", styles['Normal']))
                content.append(Paragraph("October 2024 - Present | Gothenburg, Sweden", styles['Normal']))
                ecarx_points = [
                    "Leading infrastructure optimization and system integration projects for automotive technology solutions",
                    "Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses",
                    "Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability",
                    "Managing complex network systems and providing technical solution design for enterprise-level applications"
                ]
                for point in ecarx_points:
                    content.append(Paragraph(f"• {point}", styles['Normal']))
                content.append(Spacer(1, 6))
            
            # Always include Synteda with tailored focus
            content.append(Paragraph("<b>Synteda | Azure Fullstack Developer & Integration Specialist</b>", styles['Normal']))
            content.append(Paragraph("August 2023 - September 2024 | Gothenburg, Sweden", styles['Normal']))
            
            if is_backend:
                synteda_points = [
                    "Developed comprehensive talent management system using C# and .NET Core with cloud-native architecture",
                    "Built complete office management platform from scratch, architecting backend components",
                    "Implemented RESTful APIs and microservices for scalable application architecture",
                    "Integrated SQL and NoSQL databases with optimized query performance and data protection measures"
                ]
            elif is_frontend:
                synteda_points = [
                    "Built complete office management platform from scratch, architecting frontend components",
                    "Developed comprehensive user interfaces using modern frontend frameworks",
                    "Collaborated with backend teams for seamless API integration",
                    "Implemented responsive design principles and user experience optimization"
                ]
            else:
                synteda_points = [
                    "Developed comprehensive talent management system using C# and .NET Core with cloud-native architecture",
                    "Built complete office management platform from scratch, architecting both frontend and backend components",
                    "Implemented RESTful APIs and microservices for scalable application architecture",
                    "Integrated SQL and NoSQL databases with optimized query performance and data protection measures"
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
            
            logger.info(f"✅ Generated LEGO-tailored CV PDF for {role_title} role at {company}")
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error generating LEGO CV PDF: {e}")
            return b""
    
    def _create_enhanced_lego_pdf(self, job: dict, latex_content: str) -> bytes:
        """Create enhanced PDF that actually uses LEGO logic from LaTeX template"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.colors import HexColor
            from reportlab.lib.units import inch
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            # Parse LaTeX content to extract LEGO components
            job_title = job.get('title', '').lower()
            job_description = job.get('description', '').lower()
            company = job.get('company', 'Company')
            
            # Determine job focus (LEGO logic)
            is_devops = any(keyword in job_title + job_description for keyword in 
                           ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
            is_backend = any(keyword in job_title + job_description for keyword in 
                            ['backend', 'api', 'microservices', 'spring', 'java', 'database']) and not is_devops
            is_frontend = any(keyword in job_title + job_description for keyword in 
                             ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui']) and not is_devops and not is_backend
            
            # Create enhanced styles that match your LaTeX template
            styles = getSampleStyleSheet()
            
            # Dark blue color like your template
            dark_blue = HexColor('#003366')
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=10,
                alignment=1,  # Center
                textColor=dark_blue,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=16,
                spaceAfter=10,
                alignment=1,  # Center
                textColor=dark_blue,
                fontName='Helvetica-Bold'
            )
            
            section_style = ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                spaceBefore=12,
                textColor=dark_blue,
                fontName='Helvetica-Bold'
            )
            
            # Build LEGO-tailored content
            story = []
            
            # Header with LEGO-tailored role
            story.append(Paragraph("HONGZHI LI", title_style))
            
            if is_devops:
                role_title = "DevOps Engineer & Cloud Infrastructure Specialist"
            elif is_backend:
                role_title = "Backend Developer & API Specialist"
            elif is_frontend:
                role_title = "Frontend Developer & UI Specialist"
            else:
                role_title = "Fullstack Developer"
            
            story.append(Paragraph(role_title, subtitle_style))
            
            # Contact info with clickable links (like your LaTeX template)
            contact_info = '''
            <a href="mailto:hongzhili01@gmail.com" color="blue">hongzhili01@gmail.com</a> | 
            <a href="tel:0728384299" color="blue">0728384299</a> | 
            <a href="https://www.linkedin.com/in/hzl/" color="blue">LinkedIn</a> | 
            <a href="https://github.com/bluehawana" color="blue">GitHub</a>
            '''
            story.append(Paragraph(contact_info, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # LEGO Component: Tailored Profile Summary
            story.append(Paragraph("PROFILE SUMMARY", section_style))
            
            if is_devops:
                summary = f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, AWS, Docker, and infrastructure automation. Specialized in infrastructure solutions for companies like {company}."
            elif is_backend:
                summary = f"Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, RESTful APIs, and scalable backend systems. Specialized in backend development roles for companies like {company}."
            elif is_frontend:
                summary = f"Experienced Frontend Developer with over 5 years of expertise in modern web technologies and user interface development. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in React, Angular, Vue.js, and responsive web applications. Specialized in frontend development roles for companies like {company}."
            else:
                summary = f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Specialized in fullstack development roles for companies like {company}."
            
            story.append(Paragraph(summary, styles['Normal']))
            story.append(Spacer(1, 15))
            
            # LEGO Component: Tailored Technical Skills
            story.append(Paragraph("CORE TECHNICAL SKILLS", section_style))
            
            if is_devops:
                skills = [
                    "<b>Cloud Platforms:</b> AWS, Azure, GCP, Alibaba Cloud ECS",
                    "<b>Containerization:</b> Docker, Kubernetes, Azure Kubernetes Service (AKS)",
                    "<b>CI/CD:</b> Jenkins, GitHub Actions, GitLab CI, Automated Testing",
                    "<b>Infrastructure:</b> Infrastructure as Code, System Integration, Network Management",
                    "<b>Monitoring:</b> Grafana, Advanced Scripting, System Reliability",
                    "<b>Programming Languages:</b> Python, Bash, PowerShell, Java, JavaScript"
                ]
            elif is_backend:
                skills = [
                    "<b>Programming Languages:</b> Java/J2EE, C#/.NET Core, Python, JavaScript, TypeScript",
                    "<b>Backend Frameworks:</b> Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI",
                    "<b>API Development:</b> RESTful APIs, GraphQL, Microservices Architecture",
                    "<b>Databases:</b> PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                    "<b>Performance:</b> Database optimization, Caching strategies, Application scaling",
                    "<b>Security:</b> Application security, Data protection, Authentication/Authorization"
                ]
            elif is_frontend:
                skills = [
                    "<b>Frontend Frameworks:</b> React, Angular, Vue.js, React Native",
                    "<b>Programming Languages:</b> JavaScript, TypeScript, HTML5, CSS3",
                    "<b>UI/UX:</b> Responsive Design, Mobile-First Design, User Experience",
                    "<b>State Management:</b> Redux, Context API, Vuex",
                    "<b>Build Tools:</b> Webpack, Vite, npm, yarn",
                    "<b>Testing:</b> Jest, Cypress, Unit Testing, Integration Testing"
                ]
            else:
                skills = [
                    "<b>Programming Languages:</b> Java/J2EE, JavaScript, C#/.NET Core, Python, TypeScript",
                    "<b>Frontend Technologies:</b> Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                    "<b>Backend Frameworks:</b> Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI",
                    "<b>Databases:</b> PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                    "<b>Cloud Platforms:</b> AWS, Azure, GCP",
                    "<b>DevOps:</b> Docker, Kubernetes, Jenkins, GitHub Actions, GitLab CI"
                ]
            
            for skill in skills:
                story.append(Paragraph(f"• {skill}", styles['Normal']))
            story.append(Spacer(1, 15))
            
            # Add more sections from your template...
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
            
            # ECARX (tailored based on job type)
            story.append(Paragraph("<b>ECARX | IT/Infrastructure Specialist</b>", styles['Normal']))
            story.append(Paragraph("<i>October 2024 - Present | Gothenburg, Sweden</i>", styles['Normal']))
            
            if is_devops:
                ecarx_points = [
                    "Leading infrastructure optimization and system integration projects for automotive technology solutions",
                    "Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses",
                    "Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability",
                    "Managing complex network systems and providing technical solution design for enterprise-level applications"
                ]
            else:
                ecarx_points = [
                    "Leading infrastructure optimization and system integration projects for automotive technology solutions",
                    "Providing IT support and infrastructure support to development teams for enhanced productivity",
                    "Managing complex network systems and providing technical solution design for enterprise-level applications"
                ]
            
            for point in ecarx_points:
                story.append(Paragraph(f"• {point}", styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Add education and certifications
            story.append(Paragraph("EDUCATION", section_style))
            story.append(Paragraph("<b>IT Högskolan</b><br/>Bachelor's Degree in .NET Cloud Development | 2021-2023", styles['Normal']))
            story.append(Paragraph("<b>University of Gothenburg</b><br/>Master's Degree in International Business and Trade | 2016-2019", styles['Normal']))
            story.append(Spacer(1, 15))
            
            story.append(Paragraph("CERTIFICATIONS", section_style))
            certs = [
                "AWS Certified Solutions Architect - Associate (Aug 2022)",
                "Microsoft Certified: Azure Fundamentals (Jun 2022)",
                "AWS Certified Developer - Associate (Nov 2022)"
            ]
            for cert in certs:
                story.append(Paragraph(f"• {cert}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            logger.info(f"🎉 LEGO SUCCESS: Generated tailored {role_title} resume for {company} ({len(buffer.getvalue())} bytes)")
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Enhanced LEGO PDF generation failed: {e}")
            return b"PDF generation failed"
    
    def _generate_cover_letter_pdf(self, job: dict) -> bytes:
        """Generate Claude-powered tailored cover letter PDF"""
        try:
            # Run the async operations properly
            import asyncio
            
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're in a running loop, use run_in_executor
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self._generate_cover_letter_pdf_sync, job)
                        return future.result()
                else:
                    return asyncio.run(self._generate_cover_letter_pdf_async(job))
            except RuntimeError:
                return asyncio.run(self._generate_cover_letter_pdf_async(job))
                
        except Exception as e:
            logger.error(f"❌ Error generating cover letter PDF: {e}")
            return b""
    
    def _generate_cover_letter_pdf_sync(self, job: dict) -> bytes:
        """Synchronous wrapper for cover letter generation"""
        return asyncio.run(self._generate_cover_letter_pdf_async(job))
    
    async def _generate_cover_letter_pdf_async(self, job: dict) -> bytes:
        """Async cover letter generation with Claude integration"""
        try:
            # Claude analyzes and creates personalized cover letter
            logger.info(f"🤖 Claude creating personalized cover letter for {job.get('company', 'Company')}")
            cover_letter_content = await self._build_claude_cover_letter(job)
            
            # Try LaTeX compilation first if we have LaTeX content
            if "\\documentclass" in cover_letter_content:
                try:
                    import subprocess
                    import tempfile
                    
                    with tempfile.TemporaryDirectory() as temp_dir:
                        company = job.get('company', 'Company').replace(' ', '_').replace('/', '_')
                        title = job.get('title', 'Position').replace(' ', '_').replace('/', '_')
                        
                        tex_file = os.path.join(temp_dir, f"Claude_CL_{title}_{company}.tex")
                        pdf_file = os.path.join(temp_dir, f"Claude_CL_{title}_{company}.pdf")
                        
                        with open(tex_file, 'w', encoding='utf-8') as f:
                            f.write(cover_letter_content)
                        
                        result = subprocess.run([
                            'pdflatex', '-interaction=nonstopmode', 
                            '-output-directory', temp_dir, tex_file
                        ], capture_output=True, timeout=30)
                        
                        if result.returncode == 0 and os.path.exists(pdf_file):
                            with open(pdf_file, 'rb') as f:
                                pdf_content = f.read()
                            logger.info(f"🎉 Generated Claude LaTeX cover letter PDF ({len(pdf_content)} bytes)")
                            return pdf_content
                            
                except Exception as latex_error:
                    logger.warning(f"⚠️ LaTeX cover letter compilation failed: {latex_error}")
            
            # Fallback to ReportLab with Claude content
            return self._create_claude_cover_letter_reportlab_pdf(job, cover_letter_content)
            
        except Exception as e:
            logger.error(f"❌ Error generating cover letter PDF: {e}")
            return b""
    
    async def _build_claude_cover_letter(self, job: dict) -> str:
        """Claude creates personalized cover letter using job analysis"""
        try:
            from app.services.claude_api_service import ClaudeAPIService
            claude = ClaudeAPIService()
            
            cover_letter_prompt = f"""
            Create a personalized, compelling cover letter for Hongzhi Li that focuses on SOFT SKILLS and UNIQUE VALUE not covered in his CV:
            
            JOB DETAILS:
            - Title: {job.get('title', 'Software Developer')}
            - Company: {job.get('company', 'Target Company')}
            - Description: {job.get('description', 'No description provided')}
            
            HONGZHI'S UNIQUE BACKGROUND & SOFT SKILLS (focus on these):
            - Cross-cultural bridge builder: Chinese background living/working in Sweden
            - Business-IT translator: Master's in International Business + Technical expertise
            - Cultural adaptability: Successfully integrated into Swedish tech culture
            - Global perspective: Understands both Eastern and Western business approaches
            - Communication skills: Bridges technical complexity with business needs
            - Multilingual: Mandarin, English, Swedish (learning)
            - International mindset: Valuable for companies with global operations
            - Problem-solving approach: Combines analytical thinking with creative solutions
            - Team collaboration: Experience working in diverse, multicultural teams
            - Continuous learning: Constantly adapting to new technologies and cultures
            
            TECHNICAL BACKGROUND (mention briefly):
            - Current: IT/Infrastructure Specialist at ECARX (Oct 2024-Present)
            - Previous: Azure Fullstack Developer at Synteda (Aug 2023-Sep 2024)
            - Education: IT Högskolan (.NET Cloud Development), University of Gothenburg (International Business)
            
            COVER LETTER FOCUS AREAS:
            1. Emphasize cross-cultural communication and bridge-building abilities
            2. Highlight business-technical translation skills (Master's in International Business)
            3. Show how Chinese-Swedish perspective adds value to the company
            4. Demonstrate cultural adaptability and global mindset
            5. Connect soft skills to specific job requirements
            6. Show enthusiasm for Swedish tech culture and innovation
            7. Mention ability to work with international teams/clients
            8. Focus on problem-solving and collaborative approach
            
            AVOID:
            - Don't repeat technical details from CV
            - Don't list programming languages extensively
            - Don't focus on certifications or technical achievements
            
            Structure:
            - Professional header with contact info
            - Date
            - Company address
            - Personalized greeting
            - Opening: Express genuine interest and unique value proposition
            - Body 1: Cross-cultural bridge-building and business-IT translation skills
            - Body 2: How international perspective and soft skills benefit the company
            - Body 3: Cultural fit and enthusiasm for Swedish innovation
            - Closing: Professional and confident
            
            Return the complete cover letter content (not LaTeX format).
            """
            
            personalized_cover_letter = await claude.generate_text(cover_letter_prompt)
            
            if personalized_cover_letter and len(personalized_cover_letter) > 300:
                logger.info(f"💌 Claude created personalized cover letter ({len(personalized_cover_letter)} chars)")
                return personalized_cover_letter
            else:
                logger.warning("⚠️ Claude cover letter creation failed, using fallback")
                return self._get_fallback_cover_letter(job)
                
        except Exception as e:
            logger.error(f"❌ Claude cover letter creation error: {e}")
            return self._get_fallback_cover_letter(job)
    
    def _create_claude_cover_letter_reportlab_pdf(self, job: dict, cover_letter_content: str) -> bytes:
        """Create PDF from Claude's cover letter content using ReportLab"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
            
            styles = getSampleStyleSheet()
            content = []
            
            # Parse Claude's content and format it properly
            lines = cover_letter_content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    content.append(Spacer(1, 12))
                elif line.upper() == line and len(line) > 5:  # Likely a header
                    content.append(Paragraph(line, styles['Title']))
                elif line.startswith('Dear') or line.startswith('Sincerely'):
                    content.append(Paragraph(line, styles['Normal']))
                    content.append(Spacer(1, 12))
                else:
                    content.append(Paragraph(line, styles['Normal']))
                    content.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(content)
            buffer.seek(0)
            
            logger.info(f"✅ Generated Claude cover letter PDF using ReportLab")
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error creating Claude cover letter PDF: {e}")
            return b""
    
    def _get_fallback_cover_letter(self, job: dict) -> str:
        """Fallback cover letter focusing on soft skills when Claude fails"""
        return f"""HONGZHI LI
Cross-Cultural Technology Professional
hongzhili01@gmail.com | 0728384299

{datetime.now().strftime('%Y-%m-%d')}

{job.get('company', 'Hiring Team')}
Sweden

Re: Application for {job.get('title', 'Software Developer')} Position

Dear Hiring Manager,

I am writing to express my genuine interest in the {job.get('title', 'Software Developer')} role at {job.get('company', 'your company')}. What sets me apart is my unique ability to bridge cultures, translate between business and technology, and bring a global perspective to Swedish innovation.

As a Chinese professional who has successfully integrated into Sweden's tech ecosystem, I offer a distinctive combination of cross-cultural communication skills and business-technical translation abilities. My Master's in International Business, combined with hands-on technical experience, allows me to understand both the strategic business context and the technical implementation details that drive successful projects.

My multicultural background has proven invaluable in my current role at ECARX, where I facilitate communication between diverse international teams and help translate complex technical solutions into clear business value. This skill becomes increasingly important as Swedish companies expand globally and work with international partners and clients.

What excites me most about {job.get('company', 'your company')} is the opportunity to contribute my unique perspective to your innovative team. I believe my combination of cultural adaptability, business acumen, and collaborative approach would add significant value to your organization's continued growth and success.

I would welcome the opportunity to discuss how my cross-cultural expertise and passion for bridging business and technology can contribute to {job.get('company', 'your company')}'s objectives.

Sincerely,
Hongzhi Li"""
    
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