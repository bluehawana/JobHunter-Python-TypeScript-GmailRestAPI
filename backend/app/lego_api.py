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

lego_api = Blueprint('lego_api', __name__)

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
    
    # Determine role type
    role_type = 'devops_engineer'  # default
    
    if any(keyword in job_lower for keyword in ['incident', 'sre', 'site reliability', 'on-call', 'monitoring']):
        role_type = 'incident_management_specialist'
    elif any(keyword in job_lower for keyword in ['fullstack', 'full stack', 'full-stack', 'react', 'frontend']):
        role_type = 'fullstack_developer'
    elif any(keyword in job_lower for keyword in ['android', 'mobile', 'kotlin', 'ios']):
        role_type = 'android_developer'
    
    # Extract keywords
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
    
    # Extract company and title (basic extraction)
    lines = job_description.split('\n')
    company = 'Company'
    title = 'Position'
    
    for line in lines[:10]:
        if 'company' in line.lower() or 'at ' in line.lower():
            company = line.strip()
            break
    
    for line in lines[:5]:
        if any(word in line.lower() for word in ['engineer', 'developer', 'specialist', 'manager']):
            title = line.strip()
            break
    
    return {
        'roleType': role_type.replace('_', ' ').title(),
        'keywords': tech_keywords[:15],  # Top 15 keywords
        'requiredSkills': tech_keywords[:10],  # Top 10 skills
        'achievements': [
            '26-server incident resolution in 5 hours',
            '45% cloud cost reduction',
            '35% MTTR reduction',
            '24/7 multi-region support'
        ],
        'company': company,
        'title': title
    }


def build_lego_cv(role_type: str, company: str, title: str) -> str:
    """Build CV using LEGO bricks based on role type"""
    
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
    
    # Build LaTeX
    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=0.75in}
\pagestyle{empty}

\definecolor{darkblue}{RGB}{0,51,102}

\hypersetup{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}

\titleformat{\section}{\Large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\large\bfseries}{}{0em}{}

\begin{document}
\pagestyle{empty}

\begin{center}
{\LARGE \textbf{Harvad Lee}}\\[10pt]
{\Large \textit{""" + role_type + r"""}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:+46728384299}{+46 72 838 4299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\section*{Profile Summary}
""" + profile + r"""

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
""" + skills_items + r"""
\end{itemize}

\section*{Professional Experience}

\subsection*{ECARX Sweden AB (Geely Automotive Group) | IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Provided 24/7 on-call support for multi-region infrastructure across 4 global offices
\item Resolved critical production incident affecting 26 servers within 5 hours through systematic RCA
\item Led Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45\%
\item Deployed comprehensive Prometheus/Grafana monitoring stack, reducing MTTR by 35\%
\item Automated infrastructure provisioning using Terraform and Ansible
\end{itemize}

\subsection*{H3C Technologies | Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Resolved high-severity production incident affecting 26 servers through root cause analysis
\item Participated in on-call rotations providing 24/7 support for critical infrastructure
\item Created technical documentation and runbooks in Swedish and English
\end{itemize}

\section*{Education}
\textbf{IT-Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg, Sweden

\textbf{Mölndal Campus} | Bachelor's in Java Integration | 2019-2021 | Mölndal, Sweden

\section*{Certifications}
\begin{itemize}[noitemsep]
\item AWS Certified Solutions Architect - Associate (2022)
\item AWS Certified Data Analytics - Specialty (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
\end{itemize}

\section*{Additional Information}
\begin{itemize}[noitemsep]
\item \textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native)
\item \textbf{Work Authorization:} Swedish Permanent Residence
\item \textbf{Availability:} Immediate | Based in Gothenburg, Sweden
\end{itemize}

\end{document}
"""
    
    return latex


def build_lego_cover_letter(role_type: str, company: str, title: str) -> str:
    """Build cover letter using LEGO bricks"""
    
    today = datetime.now().strftime("%B %d, %Y")
    
    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=1in}
\pagestyle{empty}

\definecolor{darkblue}{RGB}{0,51,102}

\hypersetup{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}

\begin{document}

\begin{flushright}
{\color{darkblue}\textbf{Harvad Lee}}\\
+46 72 838 4299\\
hongzhili01@gmail.com\\
Gothenburg, Sweden\\
""" + today + r"""
\end{flushright}

{\color{darkblue}\rule{\textwidth}{0.5pt}}

\vspace{12pt}

\textbf{Hiring Team}\\
""" + company + r"""\\
""" + title + r"""\\
Gothenburg, Sweden

\vspace{12pt}

Dear Hiring Manager,

I'm excited to apply for the """ + title + r""" position at """ + company + r""". With 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations, I'm confident I can contribute immediately to your team.

My experience at ECARX demonstrates my capability to manage complex infrastructure with 24/7 on-call support. I resolved a critical incident affecting 26 servers within 5 hours through systematic root cause analysis. I led the migration from Azure AKS to on-premise Kubernetes, reducing cloud costs by 45\% while improving CI/CD efficiency by 25\%.

My technical skills directly match your requirements, including expertise in cloud platforms (AWS/Azure certified), infrastructure as code (Terraform, CloudFormation), CI/CD pipelines (Jenkins, GitHub Actions), and comprehensive monitoring solutions (Prometheus, Grafana, ELK).

I'm passionate about platform reliability, automation, and developer experience improvements. I'd welcome the opportunity to discuss how my experience can contribute to """ + company + r"""'s success. Thank you for considering my application.

\vspace{12pt}

Sincerely,

\vspace{12pt}

Harvad Lee

\vspace{12pt}

{\color{darkblue}\rule{\textwidth}{0.5pt}}

\end{document}
"""
    
    return latex


@lego_api.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze job description and return analysis"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        job_url = data.get('jobUrl', '')
        
        if not job_description and not job_url:
            return jsonify({'error': 'Job description or URL required'}), 400
        
        # If URL provided, fetch job description (simplified for now)
        if job_url and not job_description:
            job_description = f"Job from {job_url}"
        
        analysis = analyze_job_description(job_description, job_url)
        
        return jsonify({
            'success': True,
            'analysis': analysis
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
        company = analysis.get('company', 'Company')
        title = analysis.get('title', 'Position')
        
        # Build LaTeX documents
        cv_latex = build_lego_cv(role_type, company, title)
        cl_latex = build_lego_cover_letter(role_type, company, title)
        
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
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_tex_path)],
            capture_output=True,
            timeout=30
        )
        
        # Compile CL
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cl_tex_path)],
            capture_output=True,
            timeout=30
        )
        
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
