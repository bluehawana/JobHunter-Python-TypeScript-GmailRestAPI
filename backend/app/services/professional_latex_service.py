#!/usr/bin/env python3
"""
Professional LaTeX Service - Uses Hongzhi Li's actual professional templates
with Claude API enhancement for job-specific customization
"""
import os
import subprocess
import tempfile
import logging
from typing import Dict, Optional
from datetime import datetime
import re
from .claude_api_service import ClaudeAPIService

logger = logging.getLogger(__name__)

class ProfessionalLaTeXService:
    """Professional LaTeX service using Hongzhi Li's actual templates with Claude API enhancement"""
    
    def __init__(self):
        # Initialize Claude API service
        self.claude_api = ClaudeAPIService()
        
        # Load actual professional templates from latex_sources
        self.template_dir = os.path.join(os.path.dirname(__file__), '../../latex_sources')
        # Ensure absolute path
        self.template_dir = os.path.abspath(self.template_dir)
        
        # Load your professional CV template
        self.cv_template_path = os.path.join(self.template_dir, 'cv_hongzhi_li_modern.tex')
        self.cover_letter_template_path = os.path.join(self.template_dir, 'cover_letter_hongzhi_li_template.tex')
        
        # Load templates into memory
        self.cv_template = self._load_template(self.cv_template_path)
        self.cover_letter_template = self._load_template(self.cover_letter_template_path)
        
        logger.info("✅ Professional LaTeX service initialized with actual templates")
    
    def _load_template(self, template_path: str) -> str:
        """Load LaTeX template from file"""
        try:
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                logger.info(f"✅ Loaded template: {os.path.basename(template_path)}")
                return template_content
            else:
                logger.error(f"❌ Template not found: {template_path}")
                return ""
        except Exception as e:
            logger.error(f"❌ Error loading template {template_path}: {e}")
            return ""
    
    async def generate_customized_cv(self, job: Dict) -> bytes:
        """Generate customized CV using professional template and Claude API"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_description = job.get('description', '')
            job_keywords = job.get('keywords', [])
            
            logger.info(f"🎯 Generating PROFESSIONAL CV for {company} - {job_title}")
            logger.info(f"📋 Using Claude API for job-specific customization")
            
            if not self.cv_template:
                logger.error("❌ CV template not loaded")
                return b""
            
            # Use Claude API to customize the entire CV for this specific job
            customization_prompt = f"""
            You are helping Hongzhi Li customize his professional CV for a specific job application.
            
            TARGET JOB:
            - Title: {job_title}
            - Company: {company}
            - Description: {job_description[:800]}
            - Key Requirements: {', '.join(job_keywords[:10])}
            
            CURRENT CV TEMPLATE:
            {self.cv_template}
            
            Please customize this CV specifically for this job by:
            
            1. **Job Role in Header**: Change "Senior Fullstack Developer" to the most appropriate title for this role (e.g., "Backend Developer", "DevOps Engineer", "Fullstack Developer", etc.)
            
            2. **Professional Summary**: Rewrite the professional summary to emphasize the most relevant experience for this specific role. Highlight technologies and experience that match the job requirements.
            
            3. **Technical Skills**: Reorder and emphasize the technical skills most relevant to this job. Put the most important skills first in each category.
            
            4. **Experience Descriptions**: Modify the bullet points under each job to highlight the most relevant achievements and technologies for this specific role. Use keywords from the job description naturally.
            
            5. **Projects Section**: Select and customize the most relevant projects that demonstrate skills needed for this role.
            
            6. **ATS Optimization**: Naturally integrate relevant keywords from the job description throughout the CV.
            
            IMPORTANT: 
            - Keep the exact same LaTeX structure and formatting
            - Maintain all the professional styling (colors, fonts, sections)
            - Ensure the content is truthful but optimally presented
            - Keep it to appropriate length (1-2 pages)
            - Use proper LaTeX escaping for special characters
            
            Return ONLY the complete customized LaTeX code, ready to compile.
            """
            
            logger.info("🤖 Requesting CV customization from Claude API...")
            customized_cv_latex = await self.claude_api.generate_text(customization_prompt)
            
            if customized_cv_latex and len(customized_cv_latex) > 500:
                logger.info(f"✅ Claude API customization successful ({len(customized_cv_latex)} chars)")
                final_cv_content = customized_cv_latex
            else:
                logger.warning("⚠️ Claude API customization failed, using base template with manual customization")
                final_cv_content = self._manual_cv_customization(job)
                
            # Debug: Log template path and content length
            logger.info(f"📂 Template directory: {self.template_dir}")
            logger.info(f"📄 Final CV content length: {len(final_cv_content)} chars")
            
            # Compile to PDF
            pdf_content = await self._compile_latex_to_pdf(final_cv_content, f"cv_{company}_{job_title}")
            
            if pdf_content:
                logger.info(f"🎉 Successfully generated professional CV PDF ({len(pdf_content)} bytes)")
            else:
                logger.error("❌ Failed to generate CV PDF")
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"❌ Error generating customized CV: {e}")
            import traceback
            traceback.print_exc()
            return b""
    
    async def generate_customized_cover_letter(self, job: Dict) -> bytes:
        """Generate customized cover letter using professional template and Claude API"""
        try:
            job_title = job.get('title', 'Software Developer')
            company = job.get('company', 'Target Company')
            job_description = job.get('description', '')
            hiring_manager = job.get('hiring_manager', '')
            
            logger.info(f"📝 Generating PROFESSIONAL Cover Letter for {company} - {job_title}")
            
            if not self.cover_letter_template:
                logger.error("❌ Cover letter template not loaded")
                return b""
            
            # Use Claude API to customize the cover letter
            customization_prompt = f"""
            You are helping Hongzhi Li write a customized cover letter for a specific job application.
            
            TARGET JOB:
            - Title: {job_title}
            - Company: {company}
            - Description: {job_description[:800]}
            - Hiring Manager: {hiring_manager if hiring_manager else 'Unknown'}
            
            CURRENT COVER LETTER TEMPLATE:
            {self.cover_letter_template}
            
            Please customize this cover letter specifically for this job by:
            
            1. **Personalized Greeting**: Use the hiring manager's name if provided, otherwise use "Dear Hiring Manager"
            
            2. **Company-Specific Opening**: Research what you can infer about the company from the job description and customize the opening to show genuine interest in their specific work/mission
            
            3. **Technical Alignment**: Modify the technical skills section to emphasize the technologies and experience most relevant to this specific role
            
            4. **Experience Relevance**: Adjust the experience descriptions to highlight the most relevant projects and achievements for this role
            
            5. **Company Culture Fit**: Customize the culture fit paragraph based on what you can infer about the company from the job description
            
            6. **Specific Reasons**: Replace "[SPECIFIC REASON - customize per company]" with actual reasons why Hongzhi would want to work at this company based on the job description
            
            IMPORTANT:
            - Keep the exact same LaTeX structure and professional formatting
            - Maintain the professional tone and style
            - Ensure it fits on one page
            - Use proper LaTeX escaping for special characters
            - Make it sound genuine and enthusiastic
            - Include specific details from the job description
            
            Return ONLY the complete customized LaTeX code, ready to compile.
            """
            
            logger.info("🤖 Requesting cover letter customization from Claude API...")
            customized_cl_latex = await self.claude_api.generate_text(customization_prompt)
            
            if customized_cl_latex and len(customized_cl_latex) > 500:
                logger.info(f"✅ Claude API customization successful ({len(customized_cl_latex)} chars)")
                final_cl_content = customized_cl_latex
            else:
                logger.warning("⚠️ Claude API customization failed, using base template with manual customization")
                final_cl_content = self._manual_cover_letter_customization(job)
            
            # Compile to PDF
            pdf_content = await self._compile_latex_to_pdf(final_cl_content, f"cover_letter_{company}_{job_title}")
            
            if pdf_content:
                logger.info(f"🎉 Successfully generated professional cover letter PDF ({len(pdf_content)} bytes)")
            else:
                logger.error("❌ Failed to generate cover letter PDF")
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"❌ Error generating customized cover letter: {e}")
            import traceback
            traceback.print_exc()
            return b""
    
    def _manual_cv_customization(self, job: Dict) -> str:
        """Manual CV customization as fallback when Claude API fails"""
        job_title = job.get('title', 'Software Developer').lower()
        job_keywords = [kw.lower() for kw in job.get('keywords', [])]
        company = job.get('company', 'Target Company')
        
        # If template loading failed, use a simple working template
        if not self.cv_template:
            logger.warning("Using simple fallback CV template")
            return self._get_simple_cv_template(job)
        
        # Determine appropriate job role for header
        if 'backend' in job_title or any('backend' in kw for kw in job_keywords):
            role = "Backend Developer"
        elif 'devops' in job_title or any('devops' in kw or 'infrastructure' in kw for kw in job_keywords):
            role = "DevOps Engineer"
        elif 'frontend' in job_title or any('frontend' in kw or 'react' in kw for kw in job_keywords):
            role = "Frontend Developer"
        else:
            role = "Senior Fullstack Developer"
        
        # Basic template customization
        customized_template = self.cv_template.replace(
            "Senior Fullstack Developer", 
            role
        )
        
        logger.info(f"📝 Customized CV for {company} with role: {role}")
        return customized_template
    
    def _get_simple_cv_template(self, job: Dict) -> str:
        """Simple working CV template as ultimate fallback"""
        job_title = job.get('title', 'Software Developer')
        company = job.get('company', 'Target Company')
        
        return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=0.75in]{{geometry}}
\\usepackage{{hyperref}}

\\pagestyle{{empty}}

\\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}}

\\begin{{document}}

\\begin{{center}}
{{\\LARGE \\textbf{{Hongzhi Li}}}}\\\\[10pt]
{{\\Large \\textit{{Senior Fullstack Developer}}}}\\\\[10pt]
\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} | 0728384299 | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}
\\end{{center}}

\\vspace{{15pt}}

\\noindent\\textbf{{\\large Professional Summary}}\\\\
\\rule{{\\textwidth}}{{0.5pt}}\\\\[5pt]
Senior Fullstack Developer with 5+ years of expertise in Java/J2EE and modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications using Spring Boot, React, and comprehensive database management. Specialized in {job_title.lower()} roles at companies like {company}.

\\vspace{{15pt}}

\\noindent\\textbf{{\\large Core Technical Skills}}\\\\
\\rule{{\\textwidth}}{{0.5pt}}\\\\[5pt]
$\\bullet$ \\textbf{{Programming Languages:}} Java/J2EE, JavaScript, C\\#/.NET Core, Python, TypeScript\\\\[3pt]
$\\bullet$ \\textbf{{Frontend Frameworks:}} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3\\\\[3pt]
$\\bullet$ \\textbf{{Backend Frameworks:}} Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI\\\\[3pt]
$\\bullet$ \\textbf{{Databases:}} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB\\\\[3pt]
$\\bullet$ \\textbf{{Cloud Platforms:}} AWS, Azure, GCP\\\\[3pt]
$\\bullet$ \\textbf{{DevOps:}} Docker, Kubernetes, Jenkins, GitHub Actions

\\vspace{{15pt}}

\\noindent\\textbf{{\\large Professional Experience}}\\\\
\\rule{{\\textwidth}}{{0.5pt}}\\\\[5pt]

\\noindent\\textbf{{ECARX | IT/Infrastructure Specialist}}\\\\
\\textit{{October 2024 - Present | Gothenburg, Sweden}}\\\\[5pt]
$\\bullet$ Leading infrastructure optimization and system integration projects for automotive technology solutions\\\\[3pt]
$\\bullet$ Implementing cost optimization by migrating from AKS to local Kubernetes cluster\\\\[3pt]
$\\bullet$ Managing complex network systems and providing technical solution design\\\\[10pt]

\\noindent\\textbf{{Synteda | Azure Fullstack Developer}}\\\\
\\textit{{August 2023 - September 2024 | Gothenburg, Sweden}}\\\\[5pt]
$\\bullet$ Developed comprehensive talent management system using C\\# and .NET Core\\\\[3pt]
$\\bullet$ Built complete office management platform with scalable microservices design\\\\[3pt]
$\\bullet$ Implemented RESTful APIs and microservices for scalable application architecture\\\\[10pt]

\\vspace{{15pt}}

\\noindent\\textbf{{\\large Education}}\\\\
\\rule{{\\textwidth}}{{0.5pt}}\\\\[5pt]
\\textbf{{IT Högskolan}} | \\textit{{Bachelor's Degree in .NET Cloud Development}} | 2021-2023\\\\[5pt]
\\textbf{{University of Gothenburg}} | \\textit{{Master's in International Business and Trade}} | 2016-2019

\\vspace{{10pt}}

\\noindent\\textbf{{\\large Certifications}}\\\\
\\rule{{\\textwidth}}{{0.5pt}}\\\\[5pt]
$\\bullet$ AWS Certified Solutions Architect - Associate (Aug 2022)\\\\[3pt]
$\\bullet$ Microsoft Certified: Azure Fundamentals (Jun 2022)\\\\[3pt]
$\\bullet$ AWS Certified Developer - Associate (Nov 2022)

\\end{{document}}"""
    
    def _manual_cover_letter_customization(self, job: Dict) -> str:
        """Manual cover letter customization as fallback when Claude API fails"""
        job_title = job.get('title', 'Software Developer')
        company = job.get('company', 'Target Company')
        hiring_manager = job.get('hiring_manager', '')
        
        # Basic template customization
        customized_template = self.cover_letter_template
        
        # Replace placeholders
        customized_template = customized_template.replace('[JOB TITLE]', job_title)
        customized_template = customized_template.replace('[COMPANY NAME]', company)
        customized_template = customized_template.replace('[HIRING MANAGER NAME]', hiring_manager if hiring_manager else 'Hiring Manager')
        customized_template = customized_template.replace('[COMPANY ADDRESS]', f"{company}\\\\Sweden")
        customized_template = customized_template.replace('[CITY, POSTAL CODE]', "Sweden")
        
        # Replace specific reason placeholder
        if 'volvo' in company.lower():
            reason = "your leadership in automotive innovation and sustainable transportation solutions"
        elif 'spotify' in company.lower():
            reason = "your revolutionary impact on music streaming and audio technology"
        else:
            reason = "your innovative approach to technology and commitment to excellence"
        
        customized_template = customized_template.replace(
            '[SPECIFIC REASON - customize per company]', 
            reason
        )
        
        return customized_template
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Compile LaTeX content to PDF using pdflatex"""
        try:
            # Create safe filename
            safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)
            tex_file = f"{safe_filename}.tex"
            pdf_file = f"{safe_filename}.pdf"
            
            # Write LaTeX source file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            logger.info(f"📄 Saved LaTeX source: {tex_file}")
            
            # Compile LaTeX to PDF using pdflatex
            try:
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory=.',
                    tex_file
                ], 
                capture_output=True, 
                text=True, 
                timeout=30
                )
                
                # Check if compilation succeeded
                if result.returncode == 0 and os.path.exists(pdf_file):
                    # Read the generated PDF
                    with open(pdf_file, 'rb') as f:
                        pdf_content = f.read()
                    
                    # Validate PDF content
                    if self._validate_pdf(pdf_content):
                        logger.info(f"✅ Successfully compiled {pdf_file} ({len(pdf_content)} bytes)")
                        
                        # Clean up auxiliary files
                        for ext in ['.aux', '.log', '.out', '.tex']:
                            aux_file = f"{safe_filename}{ext}"
                            if os.path.exists(aux_file):
                                os.remove(aux_file)
                        
                        # Remove PDF file after reading
                        if os.path.exists(pdf_file):
                            os.remove(pdf_file)
                        
                        return pdf_content
                    else:
                        logger.error("❌ Generated PDF failed validation")
                        return b""
                else:
                    logger.error(f"❌ LaTeX compilation failed: {result.stderr}")
                    return b""
                    
            except subprocess.TimeoutExpired:
                logger.error("❌ LaTeX compilation timeout")
                return b""
                
        except Exception as e:
            logger.error(f"❌ Error compiling LaTeX to PDF: {e}")
            return b""
        
        finally:
            # Clean up any remaining files
            for ext in ['.aux', '.log', '.out', '.tex', '.pdf']:
                cleanup_file = f"{safe_filename}{ext}"
                if os.path.exists(cleanup_file):
                    try:
                        os.remove(cleanup_file)
                    except:
                        pass
    
    def _validate_pdf(self, pdf_content: bytes) -> bool:
        """Validate that the content is a proper PDF"""
        if not pdf_content:
            return False
        
        # Check PDF header
        if not pdf_content.startswith(b'%PDF-'):
            return False
        
        # Check minimum size
        if len(pdf_content) < 1000:
            return False
        
        # Check for PDF trailer
        if b'%%EOF' not in pdf_content[-100:]:
            return False
        
        return True