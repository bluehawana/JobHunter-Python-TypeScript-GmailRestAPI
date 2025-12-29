#!/usr/bin/env python3
"""
ALTEN Senior Cloud Engineer Application Generator
Using LEGO Bricks Methodology for AWS/Cloud-focused role
Company: ALTEN Sweden (Automotive sector client in Gothenburg)
"""

import subprocess
import os
from datetime import datetime

# ============================================================================
# LEGO BRICKS: Modular CV Components
# ============================================================================

def profile_brick_cloud_aws():
    """Profile brick optimized for Senior Cloud Engineer role"""
    return r"""
\section*{Professional Summary}

DevOps Engineer with 5+ years of experience in cloud infrastructure automation, CI/CD optimization, and incident management. Proven track record managing multi-region infrastructure with 24/7 on-call support across 4 global offices. Expert in resolving critical production incidents - restored 26 servers within 5 hours through systematic root cause analysis. Demonstrated expertise in Kubernetes migration (45\% cost reduction), Terraform automation, Prometheus/Grafana monitoring, and Azure/AWS cloud platforms. Strong background in Python/Bash scripting, Infrastructure as Code, and building scalable cloud solutions.
"""

def skills_brick_aws_cloud():
    """Skills brick highlighting AWS and cloud technologies"""
    return r"""
\section*{Core Technical Competencies}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item \textbf{Cloud Platforms:} AWS (5+ years), Azure, Google Cloud Platform
\item \textbf{AWS Services:} Lambda, API Gateway, Step Functions, CloudFormation, CDK, ECS, EKS, S3, DynamoDB, RDS, CloudWatch, EventBridge, SNS, SQS
\item \textbf{Infrastructure as Code:} AWS CloudFormation, AWS CDK, Terraform, Pulumi
\item \textbf{Programming:} Python, TypeScript, Bash, Node.js, Go
\item \textbf{CI/CD:} AWS CodePipeline, CodeBuild, CodeDeploy, GitHub Actions, GitLab CI, Jenkins
\item \textbf{Security \& IAM:} AWS IAM, SSO, Organizations, Control Tower, StackSets, Service Catalog, Security Hub
\item \textbf{Containers:} Docker, Kubernetes, ECS, EKS, Fargate
\item \textbf{Monitoring:} CloudWatch, X-Ray, Prometheus, Grafana, ELK Stack
\item \textbf{DevOps:} Git, Agile, Scrum, Platform Engineering, SRE practices
\end{itemize}
"""

def experience_brick_ecarx_cloud():
    """ECARX experience highlighting cloud and AWS work"""
    return r"""
\section*{Professional Experience}

\subsection*{Ecarx (Geely Automotive) | IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Managed IT infrastructure with 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
\item Led Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45\% and improving CI/CD efficiency by 25\%
\item Optimized HPC cluster achieving world top 10\% performance, outperforming Azure servers by 259\%
\item Deployed Prometheus/Grafana monitoring for proactive incident detection and capacity planning
\item Resolved critical server boot failures through system diagnostics and configuration corrections
\item Implemented Infrastructure as Code using Terraform for automated infrastructure provisioning
\item Built and maintained CI/CD pipelines using GitHub Actions and GitLab CI
\end{itemize}
"""

def experience_brick_h3c():
    """H3C Technologies experience"""
    return r"""
\subsection*{H3C Technologies | Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Resolved critical incident affecting 26 servers through root cause analysis within 5 hours
\item Performed on-site hardware maintenance and component replacement
\item Delivered technical training and created documentation in Swedish and English
\end{itemize}
"""

def experience_brick_synteda():
    """Synteda AB experience"""
    return r"""
\subsection*{Synteda AB | Azure Developer \& Application Support (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Provided technical support for Azure cloud applications
\item Developed platforms using C\#/.NET Core with microservices architecture
\item Managed Azure configurations, database connectivity, and API integrations
\end{itemize}
"""

def experience_brick_pembio():
    """Pembio AB experience"""
    return r"""
\subsection*{Pembio AB | Full-Stack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Developed backend using Java/Spring Boot with microservices
\item Built frontend with Vue.js and RESTful API integration
\item Participated in Agile/Scrum development processes
\end{itemize}
"""

def education_brick():
    """Education section"""
    return r"""
\section*{Education}

\textbf{IT-Hogskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg

\textbf{Molndal Campus} | Bachelor's in Java Integration | 2019-2021 | Molndal

\textbf{University of Gothenburg} | Master's in International Business | 2016-2019 | Gothenburg
"""

def certifications_brick_aws():
    """Real certifications only"""
    return r"""
\section*{Certifications}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item AWS Certified Solutions Architect - Associate (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
\item AWS Certified Data Analytics - Specialty (2022)
\item CNCF Scholarship Recipient - CKAD Training \& Exam Voucher
\end{itemize}

\section*{Community Involvement}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Active member of AWS User Group Gothenburg
\item Participant in CNCF Gothenburg community events
\item Engaged with Cloud Native Computing Foundation initiatives
\item Member of Kubernetes Community Gothenburg
\end{itemize}

\section*{Additional Information}

\textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native)

\textbf{Work Authorization:} Swedish Permanent Residence

\textbf{Availability:} Immediate
"""

# ============================================================================
# LaTeX Document Assembly
# ============================================================================

def create_cv_latex():
    """Assemble CV using LEGO bricks"""
    
    header = r"""\documentclass[11pt,a4paper]{article}
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
{\Large Senior Cloud Engineer | AWS Specialist | DevOps Expert}\\[10pt]
hongzhili01@gmail.com | +46 72 838 4299 | Gothenburg, Sweden\\
linkedin.com/in/hzl | github.com/bluehawana
\end{center}

\vspace{8pt}
"""

    # Assemble CV with LEGO bricks
    cv_content = header
    cv_content += profile_brick_cloud_aws()
    cv_content += skills_brick_aws_cloud()
    cv_content += experience_brick_ecarx_cloud()
    cv_content += experience_brick_h3c()
    cv_content += experience_brick_synteda()
    cv_content += experience_brick_pembio()
    cv_content += education_brick()
    cv_content += certifications_brick_aws()
    
    cv_content += r"""
\end{document}
"""
    
    return cv_content

def create_cover_letter_latex():
    """Create cover letter for ALTEN Cloud Engineer position"""
    
    cl_content = r"""\documentclass[a4paper,10pt]{article}
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

{\color{darkblue}ALTEN Sweden\\
Senior Cloud Engineer Position\\
Gothenburg, Sweden}

\vspace{40pt}

Dear Hiring Manager,

\vspace{10pt}

I am writing to express my strong interest in the Senior Cloud Engineer position at ALTEN. With over 5 years of hands-on AWS experience and a proven track record of designing and implementing enterprise-scale cloud-native platforms, I am excited about the opportunity to contribute to your automotive sector client in Gothenburg.

\textbf{Cloud Infrastructure Expertise:} At ECARX (Geely Automotive), I managed IT infrastructure supporting 4 international offices (Gothenburg, London, Stuttgart, San Diego). I led the Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45\% while improving CI/CD efficiency by 25\%. I have hands-on experience with AWS and Azure cloud platforms, implementing Infrastructure as Code using Terraform, and building CI/CD pipelines with GitHub Actions and GitLab CI.

\textbf{Programming \& Automation:} I bring strong programming skills in Python, Bash, C\#/.NET Core, and Java/Spring Boot. At Synteda AB, I developed cloud platforms using microservices architecture and managed Azure configurations. At Pembio AB, I built full-stack applications with Vue.js frontend and Java backend. I've implemented CI/CD pipelines using GitHub Actions and GitLab CI, improving deployment efficiency by 25\%.

\textbf{Monitoring \& Incident Management:} I deployed comprehensive Prometheus/Grafana monitoring stacks for proactive incident detection and capacity planning. My most significant achievement was resolving a critical incident at H3C Technologies affecting 26 servers - I performed systematic root cause analysis under pressure, identified outdated configuration files causing cyclic crashes, and completed remediation within 5 hours.

\textbf{Problem-Solving:} My experience resolving a critical 26-server incident in 5 hours demonstrates my systematic problem-solving approach and ability to perform under pressure. I've successfully worked with cross-functional teams, mentored junior engineers, and contributed to architectural decisions that balance technical excellence with business requirements.

\textbf{Why ALTEN:} I am particularly drawn to ALTEN's focus on engineering excellence and career development. The opportunity to work on cloud platforms for the automotive sector, combined with ALTEN's reputation as one of Sweden's most attractive employers, makes this role an ideal next step in my career.

I am based in Gothenburg with Swedish permanent residence and available for full-time on-site work. I am fluent in English and would welcome the opportunity to discuss how my AWS expertise and cloud engineering experience can contribute to your client's success.

Thank you for considering my application. I look forward to the opportunity to discuss this position further.

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
December 16, 2025}

\end{document}
"""
    
    return cl_content

# ============================================================================
# PDF Generation
# ============================================================================

def compile_latex_to_pdf(tex_content, output_name, output_dir):
    """Compile LaTeX to PDF using pdflatex"""
    
    tex_file = os.path.join(output_dir, f"{output_name}.tex")
    
    # Write LaTeX content
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)
    
    print(f"✅ Created {tex_file}")
    
    # Compile to PDF
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        pdf_file = os.path.join(output_dir, f"{output_name}.pdf")
        
        if os.path.exists(pdf_file):
            file_size = os.path.getsize(pdf_file) / 1024  # KB
            print(f"✅ Generated {pdf_file} ({file_size:.1f} KB)")
            return True
        else:
            print(f"❌ PDF generation failed for {output_name}")
            print(result.stdout[-500:] if result.stdout else "No output")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ PDF compilation timed out for {output_name}")
        return False
    except FileNotFoundError:
        print("❌ pdflatex not found. Please install TeX Live.")
        return False

def main():
    """Main execution"""
    
    print("=" * 70)
    print("🧱 ALTEN Senior Cloud Engineer Application Generator")
    print("=" * 70)
    print()
    
    output_dir = "job_applications/alten_cloud"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate CV
    print("📄 Generating CV...")
    cv_latex = create_cv_latex()
    cv_success = compile_latex_to_pdf(cv_latex, "ALTEN_Cloud_Engineer_Harvad_CV", output_dir)
    
    print()
    
    # Generate Cover Letter
    print("📄 Generating Cover Letter...")
    cl_latex = create_cover_letter_latex()
    cl_success = compile_latex_to_pdf(cl_latex, "ALTEN_Cloud_Engineer_Harvad_CL", output_dir)
    
    print()
    print("=" * 70)
    
    if cv_success and cl_success:
        print("✅ Application package generated successfully!")
        print(f"📁 Location: {output_dir}/")
        print("📄 Files:")
        print(f"   - ALTEN_Cloud_Engineer_Harvad_CV.pdf")
        print(f"   - ALTEN_Cloud_Engineer_Harvad_CL.pdf")
    else:
        print("⚠️  Some files failed to generate. Check errors above.")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
