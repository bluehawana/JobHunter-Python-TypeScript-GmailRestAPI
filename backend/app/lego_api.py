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
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from gemini_content_polisher import GeminiContentPolisher
from smart_latex_editor import SmartLaTeXEditor
from cv_templates import CVTemplateManager
from ai_analyzer import AIAnalyzer

lego_api = Blueprint('lego_api', __name__)

# Initialize managers
template_manager = CVTemplateManager()
ai_analyzer = AIAnalyzer()

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


def customize_template(template_content: str, company: str, title: str, role_type: str) -> str:
    """Customize template by replacing placeholders and dynamic content"""
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
    
    return template_content


def build_lego_cv(role_type: str, company: str, title: str, role_category: str = None) -> str:
    """Build CV using LEGO bricks based on role type - Template-based with customization"""
    
    # Try to load template first
    template_content = None
    if role_category:
        template_content = template_manager.load_template(role_category)
    
    # If template exists, use it as base and customize
    if template_content:
        # Customize template with job-specific information
        template_content = customize_template(template_content, company, title, role_type)
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
    
    # Build LaTeX with Tata/ALTEN styling
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
{\Huge\bfseries Harvad Lee}\\[6pt]
{\Large """ + role_type + r"""}\\[10pt]
hongzhili01@gmail.com | +46 72 838 4299 | Gothenburg, Sweden\\
linkedin.com/in/hzl | github.com/bluehawana
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
    """Fetch job description from URL"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
        
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
                return jsonify({'error': 'Could not fetch job description from URL'}), 400
        
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
        
        # Build LaTeX documents
        cv_latex = build_lego_cv(role_type, company, title, role_category)
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
