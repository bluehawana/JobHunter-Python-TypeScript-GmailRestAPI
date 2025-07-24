import os
import subprocess
import tempfile
import logging
from typing import Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class SimpleLaTeXService:
    """Simplified LaTeX service with proper template formatting"""
    
    def __init__(self):
        # Simplified CV template with proper escaping
        self.cv_template = """\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}

% Page setup
\\geometry{{margin=0.75in}}
\\pagestyle{{empty}}

% Color definitions
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

% Hyperlink setup
\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}}

% Section formatting
\\titleformat{{\\section}}{{\\Large\\bfseries\\color{{darkblue}}}}{{}}{{0em}}{{}}[\\titlerule]

\\begin{{document}}
\\pagestyle{{empty}}

% Name and contact details
\\begin{{center}}
{{\\LARGE \\textbf{{Hongzhi Li}}}}\\\\[10pt]
{{\\Large \\textit{{{job_role}}}}}\\\\[10pt]
\\textcolor{{darkblue}}{{\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} | \\href{{tel:0728384299}}{{0728384299}} | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

% Personal Profile
\\section*{{Profile Summary}}
{customized_profile}

% Areas of Expertise
\\section*{{Core Technical Skills}}
\\begin{{itemize}}[noitemsep]
{skills_content}
\\end{{itemize}}

% Experience
\\section*{{Professional Experience}}

\\subsection*{{ECARX | IT/Infrastructure Specialist}}
\\textit{{October 2024 - Present | Gothenburg, Sweden}}
\\begin{{itemize}}[noitemsep]
\\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\\item Providing IT support and infrastructure support to development teams for enhanced productivity
\\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster
\\item Implementing modern monitoring solutions using Grafana and advanced scripting
\\item Managing complex network systems and providing technical solution design
\\end{{itemize}}

\\subsection*{{Synteda | Azure Fullstack Developer \\& Integration Specialist}}
\\textit{{August 2023 - September 2024 | Gothenburg, Sweden}}
\\begin{{itemize}}[noitemsep]
\\item Developed comprehensive talent management system using C\\# and .NET Core
\\item Built complete office management platform with scalable microservices design
\\item Participated in business negotiations and requirement gathering sessions
\\item Provided Azure cloud consulting services to cross-functional teams
\\item Implemented RESTful APIs and microservices for scalable application architecture
\\end{{itemize}}

\\section*{{Education}}
\\textbf{{IT Högskolan}}\\\\
\\textit{{Bachelor's Degree in .NET Cloud Development}} | 2021-2023\\\\
\\textbf{{University of Gothenburg}}\\\\
\\textit{{Master's Degree in International Business and Trade}} | 2016-2019\\\\

\\section*{{Certifications}}
\\begin{{itemize}}
\\item AWS Certified Solutions Architect - Associate (Aug 2022)
\\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\\item AWS Certified Developer - Associate (Nov 2022)
\\end{{itemize}}

\\end{{document}}"""

        # Simplified cover letter template
        self.cover_letter_template = """\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}

% Define colors
\\definecolor{{darkblue}}{{rgb}}{{0.0, 0.2, 0.6}}

% Remove paragraph indentation
\\setlength{{\\parindent}}{{0pt}}

\\begin{{document}}
\\pagestyle{{empty}}

\\begin{{letter}}{{\\textcolor{{darkblue}}{{\\\\
{company_name}\\\\
{company_address}
}}}}\\\\

\\vspace{{40pt}}

\\opening{{Dear {hiring_manager},}}
\\vspace{{10pt}}

{cover_letter_body}

\\vspace{{20pt}}
Sincerely,

Hongzhi Li\\\\

{current_date}

\\vspace{{40pt}}
{{\\color{{darkblue}}\\rule{{\\linewidth}}{{0.6pt}}}}
\\vspace{{4pt}}

\\closing{{\\color{{darkblue}} Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299}}\\\\

\\end{{letter}}
\\end{{document}}"""
    
    async def generate_customized_cv(self, job: Dict) -> bytes:
        """Generate customized CV based on job requirements"""
        try:
            # Extract job information
            job_title = job.get('title', 'Software Developer')
            job_description = job.get('description', '')
            job_keywords = job.get('keywords', [])
            company = job.get('company', '')
            
            # Customize job role in header
            job_role = self._determine_job_role(job_title, job_keywords)
            
            # Generate customized profile summary
            customized_profile = self._generate_customized_profile(job, job_description, job_keywords)
            
            # Generate relevant skills section
            skills_content = self._generate_relevant_skills(job_keywords, job_description)
            
            # Fill in the template
            cv_content = self.cv_template.format(
                job_role=job_role,
                customized_profile=customized_profile,
                skills_content=skills_content
            )
            
            # Compile LaTeX to PDF
            pdf_content = await self._compile_latex_to_pdf(cv_content, f"cv_{company}")
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating customized CV: {e}")
            return b""
    
    async def generate_customized_cover_letter(self, job: Dict) -> bytes:
        """Generate customized cover letter based on job"""
        try:
            company_name = job.get('company', 'Your Company')
            job_title = job.get('title', 'the position')
            job_description = job.get('description', '')
            
            # Generate cover letter body
            cover_letter_body = self._generate_cover_letter_body(job, job_description)
            
            # Determine hiring manager greeting
            hiring_manager = "Hiring Manager"
            
            # Fill in template
            cover_letter_content = self.cover_letter_template.format(
                company_name=company_name,
                company_address=f"{company_name}\\\\\\\\Sweden",
                hiring_manager=hiring_manager,
                cover_letter_body=cover_letter_body,
                current_date=datetime.now().strftime("%Y.%m.%d")
            )
            
            # Compile to PDF
            pdf_content = await self._compile_latex_to_pdf(
                cover_letter_content, 
                f"cover_letter_{company_name}"
            )
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            return b""
    
    def _determine_job_role(self, job_title: str, keywords: list) -> str:
        """Determine the most appropriate job role for CV header"""
        title_lower = job_title.lower()
        
        if 'fullstack' in title_lower or 'full stack' in title_lower:
            return "Fullstack Developer"
        elif 'devops' in title_lower:
            return "DevOps Engineer"
        elif 'cloud' in title_lower:
            return "Cloud Developer"
        elif 'backend' in title_lower:
            return "Backend Developer"
        elif 'frontend' in title_lower:
            return "Frontend Developer"
        else:
            return "Software Developer"
    
    def _generate_customized_profile(self, job: Dict, description: str, keywords: list) -> str:
        """Generate customized profile summary based on job"""
        # Extract key technologies
        all_content = f"{description} {' '.join(keywords)}".lower()
        
        tech_mentions = []
        if 'java' in all_content:
            tech_mentions.append('Java/Spring Boot')
        if 'react' in all_content:
            tech_mentions.append('React')
        if 'aws' in all_content or 'azure' in all_content:
            tech_mentions.append('cloud services')
        if 'microservices' in all_content:
            tech_mentions.append('microservices architecture')
        
        if tech_mentions:
            tech_list = ', '.join(tech_mentions[:3])
            return f"Experienced Fullstack Developer with over 5 years of hands-on experience specializing in {tech_list}. Proven expertise in building scalable full-stack applications with comprehensive database management. Strong background in RESTful API development and end-to-end application development."
        else:
            return "Experienced Fullstack Developer with over 5 years of hands-on experience in modern web technologies. Proven expertise in building scalable full-stack applications and comprehensive database management. Strong background in RESTful API development and end-to-end application development."
    
    def _generate_relevant_skills(self, keywords: list, description: str) -> str:
        """Generate skills section emphasizing job-relevant technologies"""
        # Base skills organized by relevance
        base_skills = [
            "\\\\item \\\\textbf{{Programming Languages:}} Java/J2EE, JavaScript, C\\\\#/.NET Core, Python",
            "\\\\item \\\\textbf{{Frontend Frameworks:}} React, Angular, Vue.js, HTML5, CSS3",
            "\\\\item \\\\textbf{{Backend Frameworks:}} Spring Boot, .NET Core, Node.js",
            "\\\\item \\\\textbf{{Databases:}} PostgreSQL, MySQL, MongoDB",
            "\\\\item \\\\textbf{{Cloud Platforms:}} AWS, Azure, GCP",
            "\\\\item \\\\textbf{{DevOps:}} Docker, Kubernetes, CI/CD, Jenkins"
        ]
        
        return "\\n".join(base_skills)
    
    def _generate_cover_letter_body(self, job: Dict, description: str) -> str:
        """Generate customized cover letter body"""
        job_title = job.get('title', 'the position')
        company_name = job.get('company', 'your company')
        
        intro = f"I am writing to express my sincere interest in the {job_title} role at {company_name}."
        
        experience_para = "As an experienced Fullstack Developer with over 5 years of expertise in both frontend and backend technologies, I am excited about the opportunity to contribute to your development team with my comprehensive technical skill set."
        
        tech_para = "Throughout my career at companies like ECARX, Synteda, and Senior Material, I have consistently demonstrated expertise in building scalable applications, implementing cloud solutions, and working in collaborative agile environments."
        
        closing_para = f"I am impressed by {company_name}'s commitment to innovation and would welcome the opportunity to contribute to your team's success. Thank you for considering my application."
        
        return f"{intro}\\n\\n{experience_para}\\n\\n{tech_para}\\n\\n{closing_para}"
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Compile LaTeX content to PDF - Mock version for testing"""
        try:
            # Create mock PDF content for testing
            pdf_header = b'%PDF-1.4\\n'
            pdf_content = f"""
Mock PDF: {filename}
Generated: {datetime.now()}

LaTeX Content (first 300 chars):
{latex_content[:300]}...

This is a mock PDF for testing purposes.
""".encode('utf-8')
            
            return pdf_header + pdf_content
            
        except Exception as e:
            logger.error(f"Error creating mock PDF: {e}")
            return b"Mock PDF Generation Failed"