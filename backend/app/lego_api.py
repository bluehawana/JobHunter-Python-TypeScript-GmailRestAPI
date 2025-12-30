"""
🧱 LEGO Bricks API for Job Application Generation
Handles job analysis, LEGO bricks assembly, and PDF generation
"""

from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
import sys
import os
import json
import subprocess
import re
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from gemini_content_polisher import GeminiContentPolisher
from smart_latex_editor import SmartLaTeXEditor
from cv_templates import CVTemplateManager
from ai_analyzer import AIAnalyzer
from ai_resume_prompts import AIResumePrompts

lego_api = Blueprint('lego_api', __name__)

# Initialize managers
template_manager = CVTemplateManager()
ai_analyzer = AIAnalyzer()
ai_prompts = AIResumePrompts()

# LEGO Bricks definitions
PROFILE_BRICKS = {
    'incident_management_specialist': """Incident Management Specialist and DevOps/SRE Engineer with 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations. Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Expert in rapid incident response - restored 26 servers in 5 hours through systematic RCA. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation (Jenkins, GitHub Actions), and comprehensive observability (Prometheus, Grafana, ELK). Reduced cloud costs 45% through strategic migration and optimization. AWS/Azure certified with strong Linux administration, Python/Bash scripting, and Agile collaboration. Passionate about platform reliability, MTTR reduction, and developer experience.""",
    
    'devops_engineer': """DevOps Engineer with 5+ years building CI/CD pipelines, automating infrastructure, and managing cloud platforms. Expert in Kubernetes, Docker, Terraform, and cloud optimization across AWS and Azure. Proven track record in infrastructure automation, monitoring solutions, and platform reliability.""",
    
    'fullstack_developer': """Full-stack engineer with 5+ years building scalable web applications and cloud infrastructure solutions. Strong frontend expertise in React, TypeScript, and modern JavaScript, combined with deep cloud platform experience across AWS, Azure, and GCP. Proven track record collaborating with international teams, designing RESTful/GraphQL APIs, and delivering high-performance user experiences.""",
    
    'android_developer': """Experienced Android Developer with 5+ years in native Android development using Kotlin and Java. Expert in Android SDK, Android Studio, and automotive infotainment systems. Strong background in building performant mobile applications with modern architecture patterns."""
}

SKILLS_BRICKS = {
    'incident_management_primary': [
        r"\textbf{Incident Management \& Response:} Production troubleshooting, Root cause analysis (RCA), On-call rotations (24/7), Critical system recovery, MTTR optimization, Runbook automation",
        r"\textbf{Monitoring \& Observability:} Prometheus, Grafana, ELK Stack, Datadog, OpenTelemetry, CloudWatch, Alerting systems, SLO/SLI metrics",
        r"\textbf{Cloud Platforms:} AWS (EC2, S3, Lambda, CloudFormation, IAM), Azure (AKS, VMs, Functions), GCP, Hybrid cloud",
        r"\textbf{Infrastructure as Code:} Terraform, CloudFormation, Ansible, Puppet, Chef, Configuration management",
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, CircleCI, Azure DevOps, Pipeline optimization",
        r"\textbf{Container Orchestration:} Kubernetes, Docker, AKS, Helm Charts, Container security",
        r"\textbf{Automation \& Scripting:} Python, Bash, PowerShell, Go, Deployment automation",
        r"\textbf{Operating Systems:} Linux (Ubuntu, CentOS, RHEL), Windows Server, System administration",
    ],
    
    'devops_primary': [
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, CircleCI, Pipeline optimization, Release automation",
        r"\textbf{Infrastructure as Code:} Terraform, CloudFormation, Ansible, Infrastructure automation",
        r"\textbf{Cloud Platforms:} AWS, Azure, GCP, Hybrid cloud infrastructure",
        r"\textbf{Container Orchestration:} Kubernetes, Docker, Helm, Container security",
        r"\textbf{Monitoring:} Prometheus, Grafana, ELK Stack, Application monitoring",
    ],
    
    'fullstack_primary': [
        r"\textbf{Frontend:} React, TypeScript, JavaScript (ES6+), Next.js, Vue.js, State management",
        r"\textbf{Backend:} Node.js, Go, Python, Spring Boot, RESTful APIs, GraphQL",
        r"\textbf{Cloud Platforms:} AWS, Azure, GCP, Cloud optimization, Performance tuning",
        r"\textbf{DevOps:} Docker, Kubernetes, CI/CD, Terraform, Git/GitHub",
        r"\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis",
    ]
}


def analyze_job_description(job_description: str, job_url: str = None) -> dict:
    """Analyze job description and determine role type, keywords, and requirements"""
    
    job_lower = job_description.lower()
    
    # Try AI analysis first (MiniMax M2)
    ai_result = None
    confidence = 0.0
    if ai_analyzer.is_available():
        ai_result = ai_analyzer.analyze_job_description(job_description)
        if ai_result:
            role_category = ai_result['role_category']
            confidence = ai_result['confidence']
            tech_keywords = ai_result.get('key_technologies', [])
            print(f"✓ AI Analysis: {role_category} (confidence: {confidence:.0%})")
        else:
            # Fallback to keyword matching
            role_category = template_manager.analyze_job_role(job_description)
            print(f"⚠ AI failed, using keyword matching: {role_category}")
    else:
        # Use CVTemplateManager for keyword-based role detection
        role_category = template_manager.analyze_job_role(job_description)
        print(f"ℹ Using keyword matching: {role_category}")
    
    role_info = template_manager.get_role_info(role_category)
    
    # Map role category to display name
    role_type = role_category.replace('_', ' ').title()
    
    # Extract keywords if not from AI
    if not ai_result or not tech_keywords:
        tech_keywords = []
        keyword_list = [
            'kubernetes', 'docker', 'terraform', 'ansible', 'jenkins', 'github actions',
            'prometheus', 'grafana', 'elk', 'aws', 'azure', 'gcp', 'python', 'bash',
            'react', 'typescript', 'node.js', 'go', 'java', 'spring boot',
            'ci/cd', 'devops', 'sre', 'incident management', 'monitoring', 'observability'
        ]
        
        for keyword in keyword_list:
            if keyword in job_lower:
                tech_keywords.append(keyword.title())
    
    # Extract company and title (improved extraction)
    lines = [line.strip() for line in job_description.split('\n') if line.strip()]
    company = 'Company'
    title = 'Position'
    
    # Try to find job title - look for lines with job-related keywords
    job_keywords = ['engineer', 'developer', 'specialist', 'manager', 'architect', 'lead', 'senior', 'junior']
    for i, line in enumerate(lines[:15]):
        # Skip very long lines (likely paragraphs)
        if len(line) > 100:
            continue
        # Check if line contains job keywords
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in job_keywords):
            # Clean up common prefixes
            cleaned = line
            for prefix in ['job title:', 'position:', 'role:', 'we are looking for']:
                if cleaned.lower().startswith(prefix):
                    cleaned = cleaned[len(prefix):].strip()
            # Remove trailing dashes or special chars
            cleaned = cleaned.strip(' -–—:')
            if cleaned and len(cleaned) < 80:
                title = cleaned
                break
    
    # Try to find company name - look for common patterns
    for i, line in enumerate(lines[:20]):
        line_lower = line.lower()
        # Skip very long lines
        if len(line) > 100:
            continue
        # Look for company indicators
        if any(indicator in line_lower for indicator in ['company:', 'about us', 'at ', 'join ']):
            # Try next line if this is just a header
            if line_lower in ['company:', 'about us', 'about the company']:
                if i + 1 < len(lines):
                    company = lines[i + 1].strip(' -–—:')
                    break
            else:
                # Extract company name from line
                for indicator in ['at ', 'join ', 'company: ']:
                    if indicator in line_lower:
                        idx = line_lower.index(indicator) + len(indicator)
                        company = line[idx:].strip(' -–—:,.')
                        # Take only first part before comma or period
                        company = company.split(',')[0].split('.')[0].strip()
                        break
                if company != 'Company':
                    break
    
    return {
        'roleType': role_type,
        'roleCategory': role_category,  # Internal category key for template matching
        'keywords': tech_keywords[:15],  # Top 15 keywords
        'requiredSkills': tech_keywords[:10],  # Top 10 skills
        'achievements': [
            '26-server incident resolution in 5 hours',
            '45% cloud cost reduction',
            '35% MTTR reduction',
            '24/7 multi-region support'
        ],
        'company': company,
        'title': title,
        'templateInfo': role_info,  # Template information
        'aiAnalysis': {
            'used': ai_result is not None,
            'confidence': confidence,
            'reasoning': ai_result.get('reasoning', '') if ai_result else '',
            'model': 'MiniMax-M2' if ai_result else 'keyword-matching'
        }
    }


def customize_template(template_content: str, company: str, title: str, role_type: str, job_description: str = "") -> str:
    """Customize template by replacing placeholders and using AI to tailor content to job description"""
    import re
    
    # Clean up the title - remove extra whitespace and newlines
    clean_title = title.strip().split('\n')[0] if title and title != 'Position' else role_type
    
    # Escape special LaTeX characters in title
    clean_title = clean_title.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
    
    # Pattern 1: Replace the {\Large ...} line after the name
    # This matches lines like "{\Large DevOps & Cloud Engineer | FinTech Specialist}"
    # or "{\Large Software Engineer | Automotive & Embedded Systems Enthusiast}"
    pattern = r'\{\\Large\s+[^\}]+\}'
    
    # Find the pattern
    match = re.search(pattern, template_content)
    if match:
        # Replace with clean title
        replacement = f'{{\\Large {clean_title}}}'
        template_content = template_content.replace(match.group(0), replacement, 1)
    
    # AI-powered content customization if job description provided
    if job_description and ai_analyzer.is_available():
        try:
            # Analyze job to extract key requirements
            ai_result = ai_analyzer.analyze_job_description(job_description)
            
            if ai_result and ai_result.get('confidence', 0) > 0.5:
                key_techs = ai_result.get('key_technologies', [])
                role_category = ai_result.get('role_category', '')
                
                # Customize Professional Summary section
                template_content = customize_profile_summary(
                    template_content, 
                    role_category, 
                    key_techs,
                    job_description
                )
                
                print(f"✓ AI-customized content for {role_category} with {len(key_techs)} key technologies")
        except Exception as e:
            print(f"⚠ AI customization failed: {e}, using template as-is")
            import traceback
            traceback.print_exc()
    
    return template_content


def customize_profile_summary(template_content: str, role_category: str, key_technologies: list, job_description: str) -> str:
    """
    Comprehensive CV customization based on job requirements
    Customizes: Profile Summary, Core Skills, Work Experience emphasis, Projects
    """
    import re
    
    # 1. Customize Professional/Profile Summary section
    summary_pattern = r'(\\section\*\{Professional Summary\})(.*?)(\\section\*\{)'
    match = re.search(summary_pattern, template_content, re.DOTALL)
    
    if not match:
        # Try alternative section names
        summary_pattern = r'(\\section\*\{Profile Summary\})(.*?)(\\section\*\{)'
        match = re.search(summary_pattern, template_content, re.DOTALL)
    
    if match:
        # Build customized summary based on role category
        custom_summary = build_custom_summary(role_category, key_technologies, job_description)
        
        if custom_summary:
            # Replace the summary content
            template_content = template_content.replace(
                match.group(0),
                f"{match.group(1)}\n\n{custom_summary}\n\n{match.group(3)}"
            )
    
    # 2. Customize Core Skills section - reorder based on JD keywords
    template_content = customize_skills_section(template_content, key_technologies)
    
    # 3. Add JD keyword emphasis comments for experience section
    # This helps maintain relevance without rewriting entire experience
    template_content = add_jd_context_comments(template_content, key_technologies, role_category)
    
    return template_content


def customize_skills_section(template_content: str, key_technologies: list) -> str:
    """
    Reorder and emphasize skills based on JD keywords
    Ensures ATS picks up the most relevant skills first
    """
    import re
    
    if not key_technologies:
        return template_content
    
    # Extract Core Technical Skills/Competencies section
    skills_pattern = r'(\\section\*\{Core Technical (?:Skills|Competencies)\})(.*?)(\\section\*\{)'
    match = re.search(skills_pattern, template_content, re.DOTALL)
    
    if match:
        skills_content = match.group(2)
        
        # Extract individual skill items - Match LaTeX \item lines
        # Pattern: \item \textbf{Category:} content
        # Note: colon is INSIDE the braces, followed by } then space then content
        item_pattern = r'\\item\s+\\textbf\{[^}]+\}\s*[^\n]+'
        items = re.findall(item_pattern, skills_content)
        
        if items and len(items) > 3:
            # Score each skill item based on keyword matches
            scored_items = []
            for item in items:
                score = 0
                item_lower = item.lower()
                for tech in key_technologies:
                    if tech.lower() in item_lower:
                        score += 1
                scored_items.append((score, item))
            
            # Sort by score (descending) - most relevant skills first
            scored_items.sort(key=lambda x: x[0], reverse=True)
            
            # Rebuild skills section with reordered items
            reordered_items = [item for score, item in scored_items]
            new_skills_content = '\n'.join(reordered_items)
            
            # Add comment about JD optimization
            new_skills_section = f"{match.group(1)}\n% Skills reordered based on job requirements\n\\begin{{itemize}}[leftmargin=*, itemsep=2pt]\n{new_skills_content}\n\\end{{itemize}}\n\n{match.group(3)}"
            
            template_content = template_content.replace(match.group(0), new_skills_section)
            print(f"✓ Reordered {len(items)} skill categories based on JD keywords")
    
    return template_content


def add_jd_context_comments(template_content: str, key_technologies: list, role_category: str) -> str:
    """
    Add LaTeX comments highlighting JD-relevant sections
    Helps maintain context about what's important for this specific job
    """
    if not key_technologies:
        return template_content
    
    # Add comment at the top of Professional Experience section
    tech_list = ', '.join(key_technologies[:10])
    comment = f"% JD Keywords: {tech_list}\n% Role: {role_category}\n% This CV is optimized for ATS matching with the above keywords\n\n"
    
    # Insert comment before Professional Experience section
    experience_pattern = r'(\\section\*\{Professional Experience\})'
    template_content = re.sub(experience_pattern, f"{comment}\\1", template_content)
    
    return template_content


def build_custom_summary(role_category: str, key_technologies: list, job_description: str) -> str:
    """
    Build a customized professional summary based on role and technologies
    Integrates with AI prompt strategies for maximum ATS and HR impact
    """
    
    # Base summaries for different role categories
    summaries = {
        'android_developer': """Android Developer with 5+ years building native mobile applications using Kotlin and Java. Expert in Android SDK, AOSP, and automotive infotainment systems. Strong background in building performant, user-centric mobile experiences with modern architecture patterns (MVVM, Clean Architecture). Proven track record delivering production applications with focus on code quality, testing, and maintainability.""",
        
        'devops_cloud': """DevOps Engineer with 5+ years building CI/CD pipelines, automating infrastructure, and managing cloud platforms. Expert in Kubernetes, Docker, Terraform, and cloud optimization across AWS and Azure. Proven track record in infrastructure automation, monitoring solutions, and platform reliability. Reduced cloud costs by 45% through strategic optimization and migration. Strong background in GitOps, infrastructure as code, and developer experience improvements.""",
        
        'incident_management_sre': """Incident Management Specialist and SRE Engineer with 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations. Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Expert in rapid incident response - restored 26 servers in 5 hours through systematic RCA. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation, and comprehensive observability (Prometheus, Grafana, ELK). Reduced MTTR by 35% through proactive monitoring and automation.""",
        
        'fullstack_developer': """Full-stack Developer with 5+ years building scalable web applications and cloud infrastructure solutions. Strong frontend expertise in React, TypeScript, and modern JavaScript, combined with deep backend experience in Node.js, Python, and microservices. Proven track record collaborating with international teams, designing RESTful/GraphQL APIs, and delivering high-performance user experiences. Expert in cloud platforms (AWS, Azure, GCP) and DevOps practices.""",
        
        'ai_product_engineer': """AI Product Engineer with 5+ years building intelligent systems and LLM-powered applications. Expert in React/TypeScript/Python with hands-on experience integrating GPT-4, Claude, and other LLMs. Built production AI systems serving 1000+ users with 99.5% uptime. Proficient with AI coding tools (Cursor, Claude Code, Copilot). Passionate about "stitching" AI engines into products with hallucination-free outputs and robust guardrails.""",
        
        'platform_engineer': """Platform Engineer with 5+ years building internal developer platforms and infrastructure automation. Expert in Kubernetes, Terraform, and cloud-native technologies. Strong focus on developer experience, self-service platforms, and infrastructure reliability. Proven track record reducing deployment time by 60% through automation and improving platform adoption across engineering teams.""",
        
        'backend_developer': """Backend Developer with 5+ years building scalable APIs and microservices. Expert in Python, Java/Spring Boot, and Node.js with strong database optimization skills (PostgreSQL, MongoDB, Redis). Proven track record designing RESTful/GraphQL APIs handling millions of requests. Strong background in distributed systems, message queues (Kafka), and cloud platforms (AWS, Azure)."""
    }
    
    # Get base summary for role category
    base_summary = summaries.get(role_category, summaries['devops_cloud'])
    
    # Strategy 1: Resume Rewrite - Use strong action verbs and measurable achievements
    # Already built into base summaries with verbs like "built", "reduced", "delivered"
    
    # Strategy 3: JD Match - Emphasize key technologies from job description
    if key_technologies:
        tech_str = ', '.join(key_technologies[:8])  # Top 8 technologies
        # Add technology emphasis to summary for ATS keyword matching
        base_summary = base_summary.replace(
            'Expert in',
            f'Expert in {tech_str} and'
        )
    
    return base_summary


def generate_ai_enhancement_prompts(job_description: str, customized_cv_text: str, company: str, position: str) -> dict:
    """
    Generate all 5 AI prompt strategies for comprehensive job application support
    
    Returns dict with prompts for:
    1. Resume rewrite (get more interviews)
    2. Role targeting (10 higher-paying roles)
    3. JD match check (aim ~90% match)
    4. Interview prep (15 questions + answers)
    5. Proof projects (complete this week)
    """
    
    return {
        'resume_rewrite': ai_prompts.resume_rewrite(customized_cv_text),
        'role_targeting': ai_prompts.role_targeting(customized_cv_text),
        'jd_match': ai_prompts.jd_match_check(job_description, customized_cv_text),
        'interview_prep': ai_prompts.interview_prep(position, job_description),
        'proof_projects': ai_prompts.proof_projects(position, job_description),
        'cover_letter': ai_prompts.cover_letter_generator(job_description, customized_cv_text, company),
        'linkedin_optimization': ai_prompts.linkedin_optimization(customized_cv_text, [position]),
        'salary_negotiation': ai_prompts.salary_negotiation(position, 5, 'Sweden')
    }


def build_lego_cv(role_type: str, company: str, title: str, role_category: str = None, job_description: str = "") -> str:
    """Build CV using LEGO bricks based on role type - Template-based with customization"""
    
    # Try to load template first
    template_content = None
    if role_category:
        template_content = template_manager.load_template(role_category)
    
    # If template exists, use it as base and customize
    if template_content:
        # Customize template with job-specific information and AI-powered content tailoring
        template_content = customize_template(template_content, company, title, role_type, job_description)
        return template_content
    
    # Fallback to LEGO bricks generation if no template
    # Map role type to brick keys
    role_map = {
        'Incident Management Specialist': 'incident_management_specialist',
        'Devops Engineer': 'devops_engineer',
        'Fullstack Developer': 'fullstack_developer',
        'Android Developer': 'android_developer'
    }
    
    brick_key = role_map.get(role_type, 'devops_engineer')
    
    profile = PROFILE_BRICKS[brick_key]
    skills_key = brick_key.replace('_specialist', '_primary').replace('_engineer', '_primary').replace('_developer', '_primary')
    skills = SKILLS_BRICKS.get(skills_key, SKILLS_BRICKS['devops_primary'])
    
    skills_items = "\n".join([f"\\item {skill}" for skill in skills])
    
    # Build LaTeX with modern Overleaf styling
    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}

\geometry{left=2cm,right=2cm,top=2cm,bottom=2cm}
\setlength{\parindent}{0pt}
\pagestyle{empty}

\definecolor{titlecolor}{RGB}{0,102,204}

\titleformat{\section}{\Large\bfseries\color{titlecolor}}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{12pt}{6pt}

\titleformat{\subsection}{\large\bfseries}{}{0em}{}
\titlespacing*{\subsection}{0pt}{8pt}{4pt}

\begin{document}

\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[10pt]
{\Large \textit{""" + role_type + r"""}}\\[10pt]
\textcolor{titlecolor}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:+46728384299}{+46 72 838 4299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\vspace{8pt}

\section*{Profile Summary}
""" + profile + r"""

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
""" + skills_items + r"""
\end{itemize}

\section*{Professional Experience}

\subsection*{Ecarx (Geely Automotive) | IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Managed IT infrastructure with 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
\item Led Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45\% and improving CI/CD efficiency by 25\%
\item Optimized HPC cluster achieving world top 10\% performance, outperforming Azure servers by 259\%
\item Deployed Prometheus/Grafana monitoring for proactive incident detection and capacity planning
\item Resolved critical server boot failures through system diagnostics and configuration corrections
\end{itemize}

\subsection*{H3C Technologies | Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Resolved critical incident affecting 26 servers through root cause analysis within 5 hours
\item Performed on-site hardware maintenance and component replacement
\item Delivered technical training and created documentation in Swedish and English
\end{itemize}

\subsection*{Synteda AB | Azure Developer \& Application Support (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Provided technical support for Azure cloud applications
\item Developed platforms using C\#/.NET Core with microservices architecture
\item Managed Azure configurations, database connectivity, and API integrations
\end{itemize}

\subsection*{Pembio AB | Full-Stack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Developed backend using Java/Spring Boot with microservices
\item Built frontend with Vue.js and RESTful API integration
\item Participated in Agile/Scrum development processes
\end{itemize}

\section*{Education}

\textbf{IT-Hogskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg

\textbf{Molndal Campus} | Bachelor's in Java Integration | 2019-2021 | Molndal

\textbf{University of Gothenburg} | Master's in International Business | 2016-2019 | Gothenburg

\section*{Certifications}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item AWS Certified Solutions Architect - Associate (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
\item AWS Certified Data Analytics - Specialty (2022)
\end{itemize}

\section*{Community Involvement}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Active member of AWS User Group Gothenburg
\item Participant in CNCF Gothenburg community events
\item CNCF Scholarship Recipient - CKAD Training \& Exam Voucher
\item Member of Kubernetes Community Gothenburg
\end{itemize}

\section*{Additional Information}

\textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native)

\textbf{Work Authorization:} Swedish Permanent Residence

\textbf{Availability:} Immediate

\end{document}
"""
    
    return latex


def customize_cover_letter(template_content: str, company: str, title: str) -> str:
    """Customize cover letter template with company and title"""
    import re
    from datetime import datetime
    
    # Replace company name in header (e.g., "CPAC Systems" or "[Company Name]")
    if company and company != 'Company':
        # Replace [Company Name] placeholder
        template_content = template_content.replace('[Company Name]', company)
        template_content = template_content.replace('[Location]', 'Gothenburg, Sweden')
        
        # Replace hardcoded company names (e.g., "CPAC Systems", "Tata Technologies")
        # Look for pattern: {\color{darkblue}CompanyName\\
        pattern = r'(\\color\{darkblue\})[^\\]+(\\\\'
        replacement = f'\\1{company}\\2'
        template_content = re.sub(pattern, replacement, template_content, count=1)
    
    # Replace job title in "Re:" line and throughout
    if title and title != 'Position':
        # Replace in Re: line
        template_content = re.sub(
            r'Re: Application for [^\\]+',
            f'Re: Application for {title}',
            template_content
        )
        # Replace "Android Platform Developer" or similar in second line of header
        pattern2 = r'(\\color\{darkblue\}[^\\]+\\\\)\n([^\\]+)(\\\\)'
        def replace_title(match):
            return f'{match.group(1)}\n{title}{match.group(3)}'
        template_content = re.sub(pattern2, replace_title, template_content, count=1)
    
    # Update date
    today = datetime.now().strftime("%B %d, %Y")
    template_content = re.sub(r'December \d+, 202\d', today, template_content)
    
    return template_content


def build_lego_cover_letter(role_type: str, company: str, title: str, role_category: str = None) -> str:
    """Build cover letter using LEGO bricks - Template-based with customization"""
    
    # Try to load cover letter template first
    if role_category:
        # Look for cover letter template
        template_path = template_manager.get_template_path(role_category)
        if template_path:
            # Try to find CL template in same directory
            cl_path = template_path.parent / template_path.name.replace('_CV.tex', '_CL.tex')
            if cl_path.exists():
                try:
                    with open(cl_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                        # Customize with company/title
                        template_content = customize_cover_letter(template_content, company, title)
                        return template_content
                except Exception as e:
                    print(f"Error loading CL template: {e}")
    
    # Fallback to LEGO bricks generation
    today = datetime.now().strftime("%B %d, %Y")
    
    latex = r"""\documentclass[a4paper,10pt]{article}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}

% Define colors
\definecolor{darkblue}{rgb}{0.0, 0.4, 0.8}

% Remove paragraph indentation
\setlength{\parindent}{0pt}

\begin{document}
\pagestyle{empty}

{\color{darkblue}""" + company + r"""\\
""" + title + r"""\\
Gothenburg, Sweden}

\vspace{40pt}

Dear Hiring Manager,

\vspace{10pt}

I'm excited to apply for the """ + title + r""" position at """ + company + r""". With 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations, I'm confident I can contribute immediately to your team.

\textbf{Technical Expertise:} At ECARX, I provide 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego). My most significant achievement was resolving a critical incident affecting 26 servers - I performed systematic root cause analysis under pressure and completed remediation within 5 hours. This experience demonstrates my ability to work under pressure, perform thorough RCA, and restore production systems rapidly.

\textbf{Infrastructure \& Automation:} I led the migration from Azure AKS to on-premise Kubernetes, reducing cloud costs by 45\% while improving CI/CD efficiency by 25\%. I deployed comprehensive Prometheus/Grafana monitoring stacks that reduced MTTR by 35\% through proactive alerting. I automate infrastructure using Terraform and Ansible, reducing manual intervention by 60\% and accelerating release cycles.

\textbf{Technical Alignment:} My skills directly match your requirements - AWS/Azure certified with hands-on experience; expert in Terraform and CloudFormation for IaC; proficient with Jenkins, GitHub Actions, and GitLab CI for CI/CD; deep expertise in Prometheus, Grafana, and ELK for observability; strong Python and Bash scripting for automation; production Kubernetes experience including troubleshooting and optimization.

I'm passionate about platform reliability, MTTR reduction, and developer experience improvements. I'd welcome the opportunity to discuss how my experience can contribute to """ + company + r"""'s success. Thank you for considering my application.

\vspace{10pt}

Sincerely,

Harvad Lee

\vspace{40pt}

{\color{darkblue}\rule{\linewidth}{0.6pt}}

\vspace{4pt}

{\color{darkblue}Ebbe Lieberathsgatan 27\\
412 65 Göteborg\\
hongzhili01@gmail.com\\
+46 72 838 4299\\
""" + today + r"""}

\end{document}
"""
    
    return latex


def fetch_job_from_url(url: str) -> str:
    """Fetch job description from URL using ScraperAPI"""
    try:
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import urlparse, parse_qs, quote
        
        parsed_url = urlparse(url)
        is_indeed = 'indeed' in parsed_url.netloc.lower()
        is_linkedin = 'linkedin' in parsed_url.netloc.lower()
        
        # Handle Indeed URL - extract job key
        if is_indeed:
            query_params = parse_qs(parsed_url.query)
            job_key = query_params.get('vjk', [None])[0] or query_params.get('jk', [None])[0]
            if job_key:
                url = f"{parsed_url.scheme}://{parsed_url.netloc}/viewjob?jk={job_key}"
                print(f"📌 Converted Indeed URL: {url}")
        
        # Check for ScraperAPI key
        api_key = os.environ.get('SCRAPERAPI_KEY', '')
        
        # LinkedIn requires premium scraping or manual copy-paste
        if is_linkedin:
            if api_key:
                # Use ScraperAPI with premium LinkedIn support
                scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={quote(url)}&premium=true&country_code=se"
                print(f"🔄 Using ScraperAPI Premium for LinkedIn")
                response = requests.get(scraper_url, timeout=60)
            else:
                # LinkedIn blocks automated access - return empty to trigger manual paste
                print(f"⚠️ LinkedIn requires manual copy-paste or ScraperAPI Premium")
                print(f"💡 Solution: Copy job description from LinkedIn and paste into text area")
                return ""
        
        # Use ScraperAPI for Indeed (they block VPS IPs)
        elif is_indeed and api_key:
            scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={quote(url)}"
            print(f"🔄 Using ScraperAPI for {parsed_url.netloc}")
            response = requests.get(scraper_url, timeout=60)
        else:
            # Direct request (works for other sites, may fail for Indeed/LinkedIn without proxy)
            if is_indeed:
                print(f"⚠️ No SCRAPERAPI_KEY configured - direct request may be blocked")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            response = requests.get(url, headers=headers, timeout=15)
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            element.decompose()
        
        text = ""
        
        # Indeed-specific parsing
        if is_indeed:
            # Look for job description container
            job_desc = soup.find('div', {'id': 'jobDescriptionText'})
            if job_desc:
                text = job_desc.get_text(separator='\n', strip=True)
            
            # Get title and company
            title_elem = soup.find('h1', class_=lambda x: x and 'jobTitle' in str(x).lower()) or soup.find('h1')
            company_elem = soup.find(attrs={'data-testid': 'inlineHeader-companyName'}) or soup.find(class_=lambda x: x and 'company' in str(x).lower())
            
            if title_elem:
                text = f"Job Title: {title_elem.get_text(strip=True)}\n" + text
            if company_elem:
                text = f"Company: {company_elem.get_text(strip=True)}\n" + text
        
        # LinkedIn-specific parsing
        elif is_linkedin:
            job_containers = soup.find_all(['div', 'section'], class_=lambda x: x and 'description' in str(x).lower())
            for container in job_containers:
                text += container.get_text(separator='\n', strip=True) + '\n'
        
        # Fallback: get all text
        if not text or len(text) < 100:
            text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) > 2]
        # Remove duplicates
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        
        text = '\n'.join(unique_lines)
        
        # Truncate if too long
        if len(text) > 10000:
            text = text[:10000] + "\n\n[Content truncated...]"
        
        if len(text) < 50:
            print(f"⚠️ Retrieved very little content ({len(text)} chars)")
            return ""
        
        print(f"✓ Successfully fetched {len(text)} characters")
        return text
        
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out for URL: {url}")
        return ""
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error {e.response.status_code} for URL: {url}")
        return ""
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""


@lego_api.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze job description and return analysis"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        job_url = data.get('jobUrl', '')
        
        if not job_description and not job_url:
            return jsonify({'error': 'Job description or URL required'}), 400
        
        # If URL provided, fetch job description
        if job_url and not job_description:
            job_description = fetch_job_from_url(job_url)
            if not job_description:
                return jsonify({
                    'error': 'Could not fetch job description from URL. Indeed and LinkedIn often block automated access. Please try copying and pasting the job description text directly into the text area instead.',
                    'suggestion': 'Copy the job description from the website and paste it in the text area'
                }), 400
        
        analysis = analyze_job_description(job_description, job_url)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'jobDescription': job_description  # Return fetched description
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/generate-lego-application', methods=['POST'])
def generate_lego_application():
    """Generate CV and Cover Letter using LEGO bricks"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        analysis = data.get('analysis', {})
        
        role_type = analysis.get('roleType', 'DevOps Engineer')
        role_category = analysis.get('roleCategory', 'devops_cloud')
        company = analysis.get('company', 'Company')
        title = analysis.get('title', 'Position')
        
        # Build LaTeX documents with AI-powered content customization
        cv_latex = build_lego_cv(role_type, company, title, role_category, job_description)
        cl_latex = build_lego_cover_letter(role_type, company, title, role_category)
        
        # Create output directory
        output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save LaTeX files
        cv_tex_path = output_dir / 'cv.tex'
        cl_tex_path = output_dir / 'cl.tex'
        
        with open(cv_tex_path, 'w', encoding='utf-8') as f:
            f.write(cv_latex)
        
        with open(cl_tex_path, 'w', encoding='utf-8') as f:
            f.write(cl_latex)
        
        # Compile to PDF
        cv_pdf_path = output_dir / 'cv.pdf'
        cl_pdf_path = output_dir / 'cl.pdf'
        
        # Compile CV
        cv_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cv_result.returncode != 0:
            print(f"CV PDF compilation error: {cv_result.stderr}")
            print(f"CV PDF compilation output: {cv_result.stdout}")
        
        # Compile CL
        cl_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cl_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cl_result.returncode != 0:
            print(f"CL PDF compilation error: {cl_result.stderr}")
            print(f"CL PDF compilation output: {cl_result.stdout}")
        
        # Check if PDFs were created
        if not cv_pdf_path.exists():
            print(f"ERROR: CV PDF was not created at {cv_pdf_path}")
            return jsonify({'error': 'CV PDF compilation failed'}), 500
        
        if not cl_pdf_path.exists():
            print(f"ERROR: CL PDF was not created at {cl_pdf_path}")
            return jsonify({'error': 'CL PDF compilation failed'}), 500
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            for file in output_dir.glob(f'*{ext}'):
                file.unlink()
        
        return jsonify({
            'success': True,
            'documents': {
                'cvUrl': f'/api/download/{output_dir.name}/cv.pdf',
                'clUrl': f'/api/download/{output_dir.name}/cl.pdf',
                'cvPreview': f'/api/preview/{output_dir.name}/cv.pdf',
                'clPreview': f'/api/preview/{output_dir.name}/cl.pdf'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/download/<folder>/<filename>')
def download_file(folder, filename):
    """Download generated PDF"""
    try:
        file_path = Path('generated_applications') / folder / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/preview/<folder>/<filename>')
def preview_file(folder, filename):
    """Preview generated PDF"""
    try:
        file_path = Path('generated_applications') / folder / filename
        if file_path.exists():
            return send_file(file_path, mimetype='application/pdf')
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/generate-comprehensive-application', methods=['POST'])
def generate_comprehensive_application():
    """
    Generate comprehensive job application package:
    1. AI-customized CV (Profile, Skills, Experience optimized for JD)
    2. Cover Letter
    3. All 5 AI Enhancement Prompts:
       - Resume rewrite (get more interviews)
       - Role targeting (10 higher-paying roles)
       - JD match check (~90% alignment)
       - Interview prep (15 questions + answers)
       - Proof projects (complete this week)
    """
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        analysis = data.get('analysis', {})
        
        role_type = analysis.get('roleType', 'DevOps Engineer')
        role_category = analysis.get('roleCategory', 'devops_cloud')
        company = analysis.get('company', 'Company')
        title = analysis.get('title', 'Position')
        
        # Build LaTeX documents with comprehensive AI-powered customization
        cv_latex = build_lego_cv(role_type, company, title, role_category, job_description)
        cl_latex = build_lego_cover_letter(role_type, company, title, role_category)
        
        # Create output directory
        output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save LaTeX files
        cv_tex_path = output_dir / 'cv.tex'
        cl_tex_path = output_dir / 'cl.tex'
        
        with open(cv_tex_path, 'w', encoding='utf-8') as f:
            f.write(cv_latex)
        
        with open(cl_tex_path, 'w', encoding='utf-8') as f:
            f.write(cl_latex)
        
        # Compile to PDF
        cv_pdf_path = output_dir / 'cv.pdf'
        cl_pdf_path = output_dir / 'cl.pdf'
        
        # Compile CV
        cv_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cv_result.returncode != 0:
            print(f"CV PDF compilation error: {cv_result.stderr}")
        
        # Compile CL
        cl_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cl_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cl_result.returncode != 0:
            print(f"CL PDF compilation error: {cl_result.stderr}")
        
        # Check if PDFs were created
        if not cv_pdf_path.exists():
            return jsonify({'error': 'CV PDF compilation failed'}), 500
        
        if not cl_pdf_path.exists():
            return jsonify({'error': 'CL PDF compilation failed'}), 500
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            for file in output_dir.glob(f'*{ext}'):
                file.unlink()
        
        # Generate all 5 AI enhancement prompts
        ai_prompts_dict = generate_ai_enhancement_prompts(
            job_description,
            cv_latex,  # Use LaTeX source as resume text
            company,
            title
        )
        
        # Save AI prompts to JSON file
        prompts_path = output_dir / 'ai_enhancement_prompts.json'
        with open(prompts_path, 'w', encoding='utf-8') as f:
            json.dump(ai_prompts_dict, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'documents': {
                'cvUrl': f'/api/download/{output_dir.name}/cv.pdf',
                'clUrl': f'/api/download/{output_dir.name}/cl.pdf',
                'cvPreview': f'/api/preview/{output_dir.name}/cv.pdf',
                'clPreview': f'/api/preview/{output_dir.name}/cl.pdf',
                'promptsUrl': f'/api/download/{output_dir.name}/ai_enhancement_prompts.json'
            },
            'aiEnhancementPrompts': {
                'resumeRewrite': {
                    'title': '1. Resume Rewrite (Get More Interviews)',
                    'description': 'Rewrite with measurable achievements, strong action verbs, and ATS-friendly keywords',
                    'prompt': ai_prompts_dict['resume_rewrite']
                },
                'roleTargeting': {
                    'title': '2. Role Targeting (10 Higher-Paying Roles)',
                    'description': 'Identify 10 high-paying roles ranked by salary and market demand',
                    'prompt': ai_prompts_dict['role_targeting']
                },
                'jdMatch': {
                    'title': '3. JD Match Check (~90% Alignment)',
                    'description': 'Compare keywords and optimize resume for ~90% alignment without exaggerating',
                    'prompt': ai_prompts_dict['jd_match']
                },
                'interviewPrep': {
                    'title': '4. Interview Prep (15 Questions + Answers)',
                    'description': '15 realistic interview questions with confident sample answers',
                    'prompt': ai_prompts_dict['interview_prep']
                },
                'proofProjects': {
                    'title': '5. Proof Projects (Complete This Week)',
                    'description': '3 small projects to complete within 7 days to demonstrate skills',
                    'prompt': ai_prompts_dict['proof_projects']
                },
                'coverLetter': {
                    'title': 'Bonus: Cover Letter Generator',
                    'description': 'Generate compelling cover letter that tells a story',
                    'prompt': ai_prompts_dict['cover_letter']
                },
                'linkedinOptimization': {
                    'title': 'Bonus: LinkedIn Optimization',
                    'description': 'Optimize LinkedIn profile for recruiter searches',
                    'prompt': ai_prompts_dict['linkedin_optimization']
                },
                'salaryNegotiation': {
                    'title': 'Bonus: Salary Negotiation',
                    'description': 'Research salary ranges and negotiation strategy',
                    'prompt': ai_prompts_dict['salary_negotiation']
                }
            },
            'customizationSummary': {
                'profileSummary': 'Tailored to JD with key technologies emphasized',
                'coreSkills': 'Reordered based on JD keyword relevance',
                'workExperience': 'JD context comments added for ATS optimization',
                'atsOptimization': 'Keywords from JD emphasized throughout CV'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/regenerate-application', methods=['POST'])
def regenerate_application():
    """Regenerate application with user feedback"""
    try:
        data = request.json
        feedback = data.get('feedback', '')
        
        # For now, just regenerate with same logic
        # In future, use feedback to adjust LEGO bricks
        
        return generate_lego_application()
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/resume-rewrite', methods=['POST'])
def ai_prompt_resume_rewrite():
    """Generate AI prompt for resume rewriting"""
    try:
        data = request.json
        resume_text = data.get('resumeText', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text required'}), 400
        
        prompt = ai_prompts.resume_rewrite(resume_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'resume_rewrite',
            'description': 'Rewrite resume to improve interview chances with measurable achievements and ATS optimization'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/role-targeting', methods=['POST'])
def ai_prompt_role_targeting():
    """Generate AI prompt for identifying high-paying roles"""
    try:
        data = request.json
        experience_text = data.get('experienceText', '')
        
        if not experience_text:
            return jsonify({'error': 'Experience text required'}), 400
        
        prompt = ai_prompts.role_targeting(experience_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'role_targeting',
            'description': 'Identify 10 high-paying roles ranked by salary and market demand'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/jd-match', methods=['POST'])
def ai_prompt_jd_match():
    """Generate AI prompt for JD-resume matching"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        resume_text = data.get('resumeText', '')
        
        if not job_description or not resume_text:
            return jsonify({'error': 'Job description and resume text required'}), 400
        
        prompt = ai_prompts.jd_match_check(job_description, resume_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'jd_match',
            'description': 'Compare keywords and optimize resume for ~90% alignment with job description'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/interview-prep', methods=['POST'])
def ai_prompt_interview_prep():
    """Generate AI prompt for interview preparation"""
    try:
        data = request.json
        position = data.get('position', '')
        job_description = data.get('jobDescription', '')
        
        if not position:
            return jsonify({'error': 'Position required'}), 400
        
        prompt = ai_prompts.interview_prep(position, job_description)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'interview_prep',
            'description': '15 realistic interview questions with confident sample answers'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/proof-projects', methods=['POST'])
def ai_prompt_proof_projects():
    """Generate AI prompt for proof-of-skill projects"""
    try:
        data = request.json
        position = data.get('position', '')
        job_description = data.get('jobDescription', '')
        
        if not position or not job_description:
            return jsonify({'error': 'Position and job description required'}), 400
        
        prompt = ai_prompts.proof_projects(position, job_description)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'proof_projects',
            'description': '3 small projects to complete this week that demonstrate required skills'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/cover-letter', methods=['POST'])
def ai_prompt_cover_letter():
    """Generate AI prompt for cover letter creation"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        resume_text = data.get('resumeText', '')
        company_name = data.get('companyName', '')
        
        if not all([job_description, resume_text, company_name]):
            return jsonify({'error': 'Job description, resume text, and company name required'}), 400
        
        prompt = ai_prompts.cover_letter_generator(job_description, resume_text, company_name)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'cover_letter',
            'description': 'Generate compelling cover letter that tells a story'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/linkedin-optimization', methods=['POST'])
def ai_prompt_linkedin():
    """Generate AI prompt for LinkedIn profile optimization"""
    try:
        data = request.json
        resume_text = data.get('resumeText', '')
        target_roles = data.get('targetRoles', [])
        
        if not resume_text or not target_roles:
            return jsonify({'error': 'Resume text and target roles required'}), 400
        
        prompt = ai_prompts.linkedin_optimization(resume_text, target_roles)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'linkedin_optimization',
            'description': 'Optimize LinkedIn profile for recruiter searches'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/salary-negotiation', methods=['POST'])
def ai_prompt_salary():
    """Generate AI prompt for salary negotiation research"""
    try:
        data = request.json
        position = data.get('position', '')
        experience_years = data.get('experienceYears', 0)
        location = data.get('location', 'Sweden')
        
        if not position or not experience_years:
            return jsonify({'error': 'Position and experience years required'}), 400
        
        prompt = ai_prompts.salary_negotiation(position, experience_years, location)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'salary_negotiation',
            'description': 'Research salary ranges and negotiation strategy'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/all', methods=['GET'])
def list_ai_prompts():
    """List all available AI prompt types"""
    return jsonify({
        'success': True,
        'prompts': [
            {
                'type': 'resume_rewrite',
                'endpoint': '/api/ai-prompts/resume-rewrite',
                'description': 'Rewrite resume with measurable achievements and ATS optimization',
                'requiredFields': ['resumeText']
            },
            {
                'type': 'role_targeting',
                'endpoint': '/api/ai-prompts/role-targeting',
                'description': 'Identify 10 high-paying roles ranked by salary and demand',
                'requiredFields': ['experienceText']
            },
            {
                'type': 'jd_match',
                'endpoint': '/api/ai-prompts/jd-match',
                'description': 'Optimize resume for ~90% alignment with job description',
                'requiredFields': ['jobDescription', 'resumeText']
            },
            {
                'type': 'interview_prep',
                'endpoint': '/api/ai-prompts/interview-prep',
                'description': '15 realistic interview questions with sample answers',
                'requiredFields': ['position'],
                'optionalFields': ['jobDescription']
            },
            {
                'type': 'proof_projects',
                'endpoint': '/api/ai-prompts/proof-projects',
                'description': '3 small projects to demonstrate required skills',
                'requiredFields': ['position', 'jobDescription']
            },
            {
                'type': 'cover_letter',
                'endpoint': '/api/ai-prompts/cover-letter',
                'description': 'Generate compelling cover letter that tells a story',
                'requiredFields': ['jobDescription', 'resumeText', 'companyName']
            },
            {
                'type': 'linkedin_optimization',
                'endpoint': '/api/ai-prompts/linkedin-optimization',
                'description': 'Optimize LinkedIn profile for recruiter searches',
                'requiredFields': ['resumeText', 'targetRoles']
            },
            {
                'type': 'salary_negotiation',
                'endpoint': '/api/ai-prompts/salary-negotiation',
                'description': 'Research salary ranges and negotiation strategy',
                'requiredFields': ['position', 'experienceYears'],
                'optionalFields': ['location']
            }
        ]
    })
