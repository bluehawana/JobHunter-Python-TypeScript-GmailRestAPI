#!/usr/bin/env python3
"""
Generate Volvo Job Applications using LEGO Bricks Logic and Overleaf Styling
"""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from cv_lego_bricks import CVLegoBricks

class VolvoLegoGenerator:
    def __init__(self):
        self.lego = CVLegoBricks()
        self.base_dir = Path("/Users/harvadlee/Projects/JobHunter-Python-TypeScript-GmailRestAPI")
        self.output_base = self.base_dir / "job_applications"
        
    def get_overleaf_template(self, name, title, email, phone, linkedin, github, profile, skills, experience, projects):
        """Standard 'Overleaf' template based on Essity CV - Simplified to avoid missing packages"""
        return rf"""\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}

% Page setup
\geometry{{margin=0.75in}}
\pagestyle{{empty}}

% Color definitions
\definecolor{{darkblue}}{{RGB}}{{0,51,102}}
\definecolor{{lightgray}}{{RGB}}{{128,128,128}}

% Hyperlink setup
\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}}

% Section formatting (Hand-coded to avoid titlesec)
\newcommand{{\mysection}}[1]{{
    \vspace{{10pt}}
    {{\Large\bfseries\color{{darkblue}} #1}}
    \kern 2pt \hrule height 1pt \kern 5pt
}}
\newcommand{{\mysubsection}}[1]{{
    \vspace{{5pt}}
    {{\large\bfseries #1}}
    \vspace{{2pt}}
}}

\begin{{document}}
\pagestyle{{empty}}

% Name and contact details
\begin{{center}}
{{\LARGE \textbf{{{name}}}}}\\[10pt]
{{\Large \textit{{{title}}}}}\\[10pt]
\textcolor{{darkblue}}{{\href{{mailto:{email}}}{{{email}}} | \href{{tel:{phone}}}{{{phone}}} | \href{{{linkedin}}}{{LinkedIn}} | \href{{{github}}}{{GitHub}}}}
\end{{center}}

% Personal Profile
\mysection{{Profile Summary}}
{profile}

% Areas of Expertise
\mysection{{Core Technical Skills}}
{skills}

% Experience
\mysection{{Professional Experience}}
{experience}

{projects}

\mysection{{Education}}
\textbf{{IT Högskolan}} - Bachelor's Degree in .NET Cloud Development | 2021-2023\\
\textbf{{Mölndal Campus}} - Bachelor's Degree in Java Integration | 2019-2021\\
\textbf{{University of Göteborg}} - Master's Degree in International Business | 2016-2019

\mysection{{Cloud Certifications}}
\begin{{itemize}}[noitemsep]
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\end{{itemize}}

\vspace{{6pt}}
\mysection{{Additional Qualifications}}
\begin{{itemize}}[noitemsep]
\item \textbf{{Languages:}} Fluent in English and Mandarin Chinese; Swedish (B2 level)
\item \textbf{{Sustainability Focus:}} Passionate about leveraging technology for environmental impact and climate-neutral solutions (e.g., Volvo Energy initiatives)
\item \textbf{{Automotive Experience:}} Currently at ECARX with deep expertise in automotive infrastructure and DevOps pipelines
\end{{itemize}}

\end{{document}}
"""

    def get_cover_letter_template(self, name, recipient, company, date, subject, body):
        """Clean modern cover letter template"""
        return rf"""\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{geometry}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}

\geometry{{margin=1in}}
\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

\begin{{document}}

\noindent \textbf{{{name}}} \\
Gothenburg, Sweden \\
hongzhili01@gmail.com \\
0728 384 299

\vspace{{1cm}}

\noindent \textbf{{{recipient}}} \\
{company} \\
Sweden

\vspace{{0.5cm}}

\noindent {date}

\vspace{{1cm}}

\noindent \textbf{{Subject: {subject}}}

\vspace{{0.5cm}}

Dear {recipient.split()[0] if recipient else 'Hiring Manager'},

{body}

\vspace{{1cm}}

\noindent Sincerely, \\
\vspace{{0.5cm}}
\noindent {name}

\end{{document}}
"""

    def tex_escape(self, text):
        """Escape LaTeX special characters"""
        if not text:
            return ""
        import re # For tex_escape
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)

    def compile_pdf(self, tex_content, output_name, output_dir):
        """Compile LaTeX to PDF locally"""
        # Ensure only \n line endings
        tex_content = tex_content.replace('\r\n', '\n').replace('\r', '\n')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            # Run pdflatex twice for proper references
            try:
                for i in range(2):
                    result = subprocess.run(['pdflatex', '-interaction=nonstopmode', f"{output_name}.tex"], 
                                cwd=temp_dir, capture_output=True, check=True)
                
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    dest_pdf = output_dir / f"{output_name}.pdf"
                    dest_tex = output_dir / f"{output_name}.tex"
                    shutil.copy2(pdf_file, dest_pdf)
                    shutil.copy2(tex_file, dest_tex)
                    print(f"  ✅ Compiled and saved: {dest_pdf.name}")
                    return True
                else:
                    print(f"  ❌ PDF file missing after compilation: {output_name}")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Error compiling {output_name}:")
                log_file = temp_path / f"{output_name}.log"
                if log_file.exists():
                    with open(log_file, 'r') as log:
                        lines = log.readlines()
                        # Show some lines around the error
                        for line in lines:
                            if "!" in line:
                                print(f"    {line.strip()}")
                return False
        return False

    def generate_all(self):
        jobs = [
            {
                'id': 'volvo_energy',
                'title': 'Cloud Developer / Fullstack (Volvo Energy Integration)',
                'company': 'Volvo Energy',
                'recipient': 'Volvo Energy Recruitment Team',
                'subject': 'Application for Cloud Developer - Energy Integration Systems',
                'focus': 'fullstack',
                'requirements': ['cloud', 'azure', '.net', 'react', 'sustainability', 'energy'],
                'cl_body': """I am writing to express my strong interest in the Cloud Developer position at Volvo Energy, specifically focused on Energy Integration. With my background as an IT/Infrastructure Specialist at ECARX and my deep commitment to sustainable technology, I am excited about the prospect of contributing to Volvo's mission of electrification and climate-neutral transport solutions.

In my current role at ECARX, I have led infrastructure optimization projects, including complex migrations from Azure Kubernetes Service (AKS) to on-premise solutions, achieving significant cost savings and performance gains. My technical stack centered on C# .NET and React, combined with robust DevOps practices, aligns perfectly with the requirements of building scalable energy management platforms.

I have recently developed a Fleet Management Dashboard that leverages US DOT data to optimize fuel efficiency and track CO2 emissions—a project that directly mirrors the challenges Volvo Energy addresses in the transition to electric fleets. Furthermore, my experience with AI-driven pedagogical systems (AI Math Grader) demonstrates my ability to integrate advanced LLM capabilities into full-stack ecosystems.

I am particularly drawn to Volvo Energy because it sits at the intersection of my technical expertise and my passion for environmental impact. I am confident that my experience in building resilient, cloud-native architectures will be a significant asset to your team as you shape the future of energy integration at Volvo Group."""
            },
            {
                'id': 'volvo_architecture',
                'title': '.NET Solution Architect / Lead Developer',
                'company': 'Volvo Group IT',
                'recipient': 'Hiring Manager, Solutions Architecture',
                'subject': 'Application for .NET Solution Architect',
                'focus': 'infrastructure',
                'requirements': ['architecture', '.net', 'lead', 'infrastructure', 'strategy'],
                'cl_body': """I am writing to apply for the Solution Architect position at Volvo Group IT. With over 5 years of experience in architecting scalable full-stack applications and leading complex infrastructure transformations, I am eager to bring my strategic technical vision to your architectural team.

Currently at ECARX, I serve as an IT/Infrastructure Specialist where I design and implement the foundation for automotive infotainment systems. My achievement in migrating mission-critical workloads from AKS to high-performance on-premise Kubernetes clusters resulted in a 259% performance improvement and a 65% cost reduction—a testament to my ability to balance technical excellence with business value.

My architectural approach is defined by the 'LEGO bricks' logic: building modular, reusable systems that can scale and adapt rapidly. This is evidenced in my latest project, a Fleet Management System built with .NET 8 and React, designed to handle large-scale telemetrics and provide actionable insights for sustainable logistics.

Volvo's reputation for engineering excellence and its proactive stance on digital transformation resonate deeply with my professional goals. I am convinced that my blend of system-level infrastructure knowledge and high-level application architecture expertise will allow me to make immediate and meaningful contributions to Volvo's technical strategy."""
            },
            {
                'id': 'volvo_lina_infrastructure',
                'title': 'Fullstack C#/.NET Consultant (Infrastructure Focus)',
                'company': 'Volvo Group (via Lina Redgård)',
                'recipient': 'Lina Redgård',
                'subject': 'Application for C#/.NET Developer - Infrastructure & DevOps Focus',
                'focus': 'infrastructure',
                'requirements': ['infrastructure', 'devops', 'azure', 'c#', '.net'],
                'cl_body': """It was a pleasure following the opportunities you manage at Volvo Group. I am formally submitting my application for the Fullstack C#/.NET Consultant position, with a specific focus on the Infrastructure and DevOps aspects of the role.

My current experience as an IT/Infrastructure Specialist at ECARX has provided me with a unique perspective on the intersection of software development and system reliability. I don't just write code; I build the pipelines and platforms that ensure code runs flawlessly at scale. My expertise in Azure, Kubernetes, and Terraform has been instrumental in managing globally distributed automotive services and providing 24/7 production support.

I am particularly proud of my work on a Fleet Management Dashboard and an AI-driven Math Grader, both of which I architected from the ground up using .NET 8 and modern frontend frameworks. These projects showcase my ability to deliver end-to-end solutions while maintaining a rigorous focus on infrastructure stability and CI/CD automation.

I believe my background in the automotive sector, combined with my certifications in AWS and Azure, makes me a strong fit for the consultant roles you are handling. I am ready to bring my proactive, problem-solving mindset to the teams at Volvo Group."""
            },
            {
                'id': 'volvo_lina_quality',
                'title': 'Fullstack C#/.NET Consultant (Quality & Testing Focus)',
                'company': 'Volvo Group (via Lina Redgård)',
                'recipient': 'Lina Redgård',
                'subject': 'Application for C#/.NET Developer - Software Quality & Testing Focus',
                'focus': 'fullstack',
                'requirements': ['testing', 'quality', 'tdd', 'xunit', 'monitoring', 'grafana'],
                'cl_body': """I am writing to express my interest in the C#/.NET Consultant role focused on Software Quality and Testing at Volvo Group. As we discussed, I understand the critical importance of reliability and observability in large-scale enterprise systems, and I have dedicated my career to mastering these domains.

In my current role at ECARX, I have been instrumental in implementing advanced observability stacks using Grafana, Prometheus, and the ELK stack. This data-driven approach has allowed us to move from reactive troubleshooting to proactive site reliability engineering. My development process is rooted in TDD and automated testing paradigms, ensuring that quality is baked into the product from the first line of code.

My recent projects, including an AI Math Grader and a sustainable Fleet Management System, were built with a 'quality-first' mindset. For the AI Math Grader, I implemented complex feedback loops and validation layers to ensure the accuracy of pedagogical responses—a challenge that required rigorous testing of non-deterministic AI outputs.

I am excited about the possibility of bringing this focus on quality and monitoring to Volvo Group. I am confident that my experience in building robust, observable systems will help your teams maintain the high standards of performance and reliability that Volvo is known for."""
            }
        ]
        
        for job in jobs:
            print(f"🧱 Building application for: {job['title']}")
            
            # Use LEGO logic for CV content
            cv_bricks = self.lego.build_cv_for_job(job, application_type=job['focus'])
            
            # Construct CV LaTeX
            cv_tex = self.get_overleaf_template(
                name="Harvad (Hongzhi) Li",
                title=self.tex_escape(job['title']),
                email="hongzhili01@gmail.com",
                phone="0728 384 299",
                linkedin="https://linkedin.com/in/hongzhili",
                github="https://github.com/bluehawana",
                profile=cv_bricks['profile'],
                skills=cv_bricks['skills'],
                experience=cv_bricks['experience'],
                projects=cv_bricks['projects']
            )
            
            # Construct CL LaTeX
            cl_tex = self.get_cover_letter_template(
                name="Harvad (Hongzhi) Li",
                recipient=self.tex_escape(job['recipient']),
                company=self.tex_escape(job['company'].split('(')[0].strip()),
                date="January 9, 2026",
                subject=self.tex_escape(job['subject']),
                body=self.tex_escape(job['cl_body'])
            )
            
            # Create output directory
            job_dir = self.output_base / job['id']
            job_dir.mkdir(parents=True, exist_ok=True)
            
            # Compile PDFs
            cv_ok = self.compile_pdf(cv_tex, f"Harvad_Li_CV_{job['id']}", job_dir)
            cl_ok = self.compile_pdf(cl_tex, f"Harvad_Li_CL_{job['id']}", job_dir)
            
            if cv_ok and cl_ok:
                print(f"  ✨ All documents ready in: {job_dir}")
            else:
                print(f"  ⚠️  Some documents failed for: {job['id']}")

if __name__ == "__main__":
    generator = VolvoLegoGenerator()
    generator.generate_all()
