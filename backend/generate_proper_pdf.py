#!/usr/bin/env python3
"""
Generate proper PDF files that can actually be opened and viewed
"""
import subprocess
import tempfile
import os
from datetime import datetime

def create_proper_cv_pdf(job):
    """Create a real LaTeX CV PDF that can be opened"""
    
    latex_content = rf'''
\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=0.75in]{{geometry}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}

% Custom colors
\definecolor{{headingcolor}}{{RGB}}{{47, 79, 79}}
\definecolor{{accentcolor}}{{RGB}}{{70, 130, 180}}

% Custom section formatting
\titleformat{{\section}}{{\Large\bfseries\color{{headingcolor}}}}{{}}{{0em}}{{}}[\titlerule]
\titleformat{{\subsection}}{{\large\bfseries\color{{accentcolor}}}}{{}}{{0em}}{{}}

\begin{{document}}

% Header
\begin{{center}}
    {{\LARGE \textbf{{Hongzhi (Harvad) Li}}}} \\[0.3cm]
    {{\large Senior Software Engineer \& DevOps Specialist}} \\[0.2cm]
    \href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} $\bullet$ 
    +46 728 384 299 $\bullet$ 
    Gothenburg, Sweden \\
    \href{{https://linkedin.com/in/hongzhili}}{{linkedin.com/in/hongzhili}} $\bullet$
    \href{{https://github.com/bluehawana}}{{github.com/bluehawana}}
\end{{center}}

\section{{Professional Summary}}
Experienced Software Engineer with 5+ years in full-stack development, cloud infrastructure, and DevOps practices. 
Proven expertise in Java, Python, JavaScript, AWS, Docker, and Kubernetes. Strong background in microservices 
architecture and agile development methodologies.

\section{{Technical Skills}}
\begin{{itemize}}[leftmargin=*,itemsep=0pt]
    \item \textbf{{Languages:}} Java, Python, JavaScript, TypeScript, Go, C\#
    \item \textbf{{Frameworks:}} Spring Boot, React, Node.js, Django, .NET
    \item \textbf{{Cloud Platforms:}} AWS, Azure, Docker, Kubernetes
    \item \textbf{{DevOps Tools:}} Jenkins, GitLab CI, Terraform, Ansible
    \item \textbf{{Databases:}} PostgreSQL, MongoDB, Redis, MySQL
    \item \textbf{{Other:}} Microservices, REST APIs, GraphQL, Git, Agile
\end{{itemize}}

\section{{Professional Experience}}

\subsection{{Senior Software Engineer | ECARX Sweden AB | 2023 - Present}}
\begin{{itemize}}[leftmargin=*,itemsep=2pt]
    \item Developed cloud-native microservices using Java and Spring Boot
    \item Implemented Kubernetes deployment strategies and CI/CD pipelines
    \item Built monitoring and alerting systems using Prometheus and Grafana
    \item Led cross-functional teams in automotive software development
\end{{itemize}}

\subsection{{Software Engineer | Synteda AB | 2022 - 2023}}
\begin{{itemize}}[leftmargin=*,itemsep=2pt]
    \item Designed and implemented microservices architecture using C\# and .NET
    \item Developed cloud-native applications with Azure services
    \item Built REST APIs and integrated third-party services
    \item Collaborated in agile development environment
\end{{itemize}}

\subsection{{Junior Software Engineer | IT-Högskolan | 2021 - 2022}}
\begin{{itemize}}[leftmargin=*,itemsep=2pt]
    \item Developed Spring Boot applications with MySQL integration
    \item Created RESTful APIs for web applications
    \item Participated in code reviews and testing procedures
    \item Gained experience in full-stack development
\end{{itemize}}

\section{{Key Projects}}

\subsection{{JobHunter AI System}}
Python/TypeScript automation platform with Claude AI integration for job application optimization.
Technologies: Python, React, PostgreSQL, Docker

\subsection{{AndroidAuto AI Bot}}
AI-powered voice assistant for Android Auto systems with real-time processing.
Technologies: Python, Kotlin, Machine Learning, Voice Recognition

\subsection{{SmrtMart.com E-commerce Platform}}
Full-stack e-commerce solution with microservices architecture.
Technologies: Go, Next.js, PostgreSQL, Docker, Kubernetes

\section{{Education}}
\textbf{{Master's in Computer Science}} | University of Gothenburg \\
\textbf{{Bachelor's in Software Engineering}} | IT-Högskolan

\section{{Certifications}}
\begin{{itemize}}[leftmargin=*,itemsep=0pt]
    \item AWS Certified Solutions Architect - Associate
    \item Kubernetes Administrator (CKA)
    \item Azure DevOps Engineer Expert
\end{{itemize}}

\vspace{{0.3cm}}
\begin{{center}}
    \textit{{Generated for: {job.get('company', 'Target Company')} - {job.get('title', 'Software Position')}}} \\
    \textit{{Date: {datetime.now().strftime('%Y-%m-%d')}}}
\end{{center}}

\end{{document}}
'''
    
    return compile_latex_to_pdf(latex_content, 'cv')

def create_proper_cover_letter_pdf(job):
    """Create a real LaTeX Cover Letter PDF that can be opened"""
    
    company = job.get('company', 'Technology Company')
    title = job.get('title', 'Software Developer Position')
    
    latex_content = rf'''
\documentclass[11pt,a4paper]{{letter}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}

\definecolor{{accentcolor}}{{RGB}}{{70, 130, 180}}

\signature{{Hongzhi (Harvad) Li}}
\address{{Hongzhi (Harvad) Li \\ Senior Software Engineer \\ 
          Gothenburg, Sweden \\ 
          +46 728 384 299 \\ 
          \href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}}}}

\begin{{document}}

\begin{{letter}}{{{company} \\ 
                 Sweden}}

\opening{{Dear Hiring Manager,}}

I am writing to express my strong interest in the \textbf{{{title}}} position at \textbf{{{company}}}. 
With my extensive experience in software development, cloud infrastructure, and DevOps practices, 
I am confident I would be a valuable addition to your team.

My background includes over 5 years of experience with modern development technologies and practices. 
At my current role with ECARX Sweden AB, I have been developing cloud-native microservices using 
Java and Spring Boot, implementing Kubernetes deployment strategies, and building comprehensive 
monitoring solutions. This experience has given me deep expertise in the technologies that are 
essential for today's software engineering challenges.

I am particularly excited about this opportunity at {company} because of your reputation for 
innovation and technical excellence. My experience with microservices architecture, cloud platforms 
(AWS/Azure), and DevOps practices aligns perfectly with the requirements outlined in your job posting. 
I have consistently delivered high-quality software solutions while working collaboratively in 
agile environments.

Some key achievements that demonstrate my capabilities:
\begin{{itemize}}
    \item Designed and implemented scalable microservices architectures
    \item Built and managed CI/CD pipelines using Jenkins and GitLab
    \item Developed full-stack applications using modern frameworks
    \item Led cross-functional teams in delivering complex projects
\end{{itemize}}

I am particularly drawn to roles that challenge me to work with cutting-edge technologies and 
contribute to meaningful projects. I believe my technical skills, combined with my passion for 
software engineering and collaborative approach, would make me a strong fit for your team.

I would welcome the opportunity to discuss how my experience and enthusiasm can contribute to 
{company}'s continued success. Thank you for your time and consideration.

\closing{{Best regards,}}

\vspace{{0.5cm}}
\begin{{center}}
    \textit{{Generated for: {company} - {title}}} \\
    \textit{{Date: {datetime.now().strftime('%Y-%m-%d')}}}
\end{{center}}

\end{{letter}}
\end{{document}}
'''
    
    return compile_latex_to_pdf(latex_content, 'cover_letter')

def compile_latex_to_pdf(latex_content, doc_type):
    """Compile LaTeX to proper PDF bytes"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(latex_content)
            tex_file = f.name
        
        # Compile with pdflatex
        result = subprocess.run([
            'pdflatex', '-interaction=nonstopmode', tex_file
        ], capture_output=True, text=True, cwd=tempfile.gettempdir())
        
        pdf_file = tex_file.replace('.tex', '.pdf')
        
        if os.path.exists(pdf_file):
            # Read PDF bytes
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            
            # Save test copy
            test_file = f"test_{doc_type}_{datetime.now().strftime('%H%M%S')}.pdf"
            with open(test_file, 'wb') as f:
                f.write(pdf_bytes)
            
            print(f"✅ {doc_type.upper()} PDF: {len(pdf_bytes)} bytes -> {test_file}")
            
            # Cleanup
            for ext in ['.tex', '.pdf', '.aux', '.log']:
                cleanup_file = tex_file.replace('.tex', ext)
                if os.path.exists(cleanup_file):
                    os.remove(cleanup_file)
            
            return pdf_bytes
        else:
            print(f"❌ PDF compilation failed: {result.stderr}")
            return b""
            
    except Exception as e:
        print(f"❌ LaTeX compilation error: {e}")
        return b""

if __name__ == "__main__":
    # Test with sample job
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'SKF Group',
        'description': 'Kubernetes, Docker, AWS, microservices',
        'keywords': ['kubernetes', 'docker', 'aws', 'python', 'devops']
    }
    
    print("🧪 Testing proper PDF generation...")
    
    cv_pdf = create_proper_cv_pdf(test_job)
    cl_pdf = create_proper_cover_letter_pdf(test_job)
    
    if cv_pdf and cl_pdf:
        print("🎉 Both PDFs generated successfully!")
        print(f"📄 CV: {len(cv_pdf)} bytes")
        print(f"📄 Cover Letter: {len(cl_pdf)} bytes")
    else:
        print("❌ PDF generation failed")