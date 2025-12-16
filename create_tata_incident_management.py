#!/usr/bin/env python3
"""
🧱 LEGO BRICKS: Tata Technologies Incident Management Specialist Application
Dynamic CV building with role-specific content assembly
"""

from datetime import datetime
import sys
import os
from pathlib import Path

# Add backend to path for Gemini polishing
sys.path.append('backend')

def load_env():
    """Load environment variables from .env file"""
    env_path = Path('.env')
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


# 🧱 LEGO BRICK: Profile Summaries
PROFILE_BRICKS = {
    'incident_management_specialist': """Incident Management Specialist and DevOps/SRE Engineer with 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations. Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Expert in rapid incident response - restored 26 servers in 5 hours through systematic RCA. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation (Jenkins, GitHub Actions), and comprehensive observability (Prometheus, Grafana, ELK). Reduced cloud costs 45% through strategic migration and optimization. AWS/Azure certified with strong Linux administration, Python/Bash scripting, and Agile collaboration. Passionate about platform reliability, MTTR reduction, and developer experience.""",
    
    'devops_engineer': """DevOps Engineer with 5+ years building CI/CD pipelines, automating infrastructure, and managing cloud platforms. Expert in Kubernetes, Docker, Terraform, and cloud optimization across AWS and Azure.""",
    
    'sre_specialist': """Site Reliability Engineer with 5+ years ensuring high availability, implementing monitoring solutions, and optimizing system performance. Expert in incident response, capacity planning, and platform reliability."""
}

# 🧱 LEGO BRICK: Skills (ordered by role priority)
SKILLS_BRICKS = {
    'incident_management_primary': [
        r"\textbf{Incident Management \& Response:} Production troubleshooting, Root cause analysis (RCA), On-call rotations (24/7), Critical system recovery, MTTR optimization, Runbook automation, Post-incident reviews, Escalation management",
        r"\textbf{Monitoring \& Observability:} Prometheus, Grafana, ELK Stack (Elasticsearch, Logstash, Kibana), Datadog, OpenTelemetry, CloudWatch, Alerting systems, SLO/SLI metrics, Distributed tracing",
        r"\textbf{Cloud Platforms (5+ years):} AWS (EC2, S3, Lambda, CloudFormation, CloudWatch, IAM), Azure (AKS, VMs, Functions, ARM templates, Monitor), GCP familiarity, Hybrid cloud",
        r"\textbf{Infrastructure as Code:} Terraform (expert), CloudFormation, Ansible, Puppet, Chef, Configuration management, Infrastructure automation",
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, CircleCI, Azure DevOps, Pipeline optimization, Release automation, Feature flags, Rollback strategies",
        r"\textbf{Container Orchestration:} Kubernetes (production experience), Docker, Azure Kubernetes Service (AKS), Helm Charts, Container security, Pod troubleshooting",
        r"\textbf{Automation \& Scripting:} Python (expert), Bash, PowerShell, Go, Deployment automation, Self-service tooling",
        r"\textbf{Operating Systems:} Linux (Ubuntu, CentOS, RHEL) - expert, Windows Server, System administration, Performance tuning, Networking fundamentals",
        r"\textbf{Security \& Compliance:} IAM policies, Secrets management (Vault, AWS Secrets Manager), Network segmentation, Vulnerability scanning, Security audits, Access controls",
        r"\textbf{Database Operations:} PostgreSQL, MySQL, MongoDB, Redis, Backup/recovery strategies, Performance optimization, Replication",
        r"\textbf{Agile \& Collaboration:} Scrum, Kanban, Sprint planning, Cross-functional teams, Documentation, Remote work (3+ years)"
    ],
    
    'devops_primary': [
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, Pipeline optimization",
        r"\textbf{Infrastructure as Code:} Terraform, CloudFormation, Ansible",
        r"\textbf{Cloud Platforms:} AWS, Azure, Hybrid cloud infrastructure"
    ]
}

# 🧱 LEGO BRICK: ECARX Experience (role-specific versions)
ECARX_BRICKS = {
    'incident_management_focused': [
        "Provided 24/7 on-call support for multi-region infrastructure across 4 global offices (Gothenburg, London, Stuttgart, San Diego), managing incident response, system monitoring, and rapid troubleshooting for distributed teams",
        "Resolved critical production incident affecting 26 servers experiencing cyclic crashes at H3C's largest Swedish customer (Zeekr) - performed systematic root cause analysis, identified outdated Ansys Fluent configurations, and completed remediation within 5 hours, restoring full production capacity",
        "Deployed comprehensive Prometheus and Grafana monitoring stack tracking real-time HPC metrics (CPU, I/O, memory, network), enabling proactive incident detection, capacity planning, and 40% reduction in MTTR through automated alerting",
        "Led strategic migration from Azure AKS to on-premise Kubernetes cluster, reducing annual cloud costs by 45% while improving CI/CD pipeline execution efficiency by 25% through infrastructure optimization and automation",
        "Coordinated with Huawei support engineers to resolve critical server boot failures following power outages - performed system diagnostics, BIOS configuration corrections, and service restoration with minimal downtime",
        "Optimized on-premise HPC cluster for Android AOSP 15 compilation through systematic performance analysis and tuning, achieving world top 10% performance (outperforming Microsoft Azure flagship servers by 259%)",
        "Automated infrastructure provisioning and deployment processes using Terraform and Ansible, reducing manual intervention by 60%, improving deployment reliability, and accelerating release cycles",
        "Implemented security best practices including IAM policies, secrets management (Vault), and network segmentation across hybrid cloud environment, passing security audits with zero critical findings",
        "Created comprehensive runbooks and incident response documentation, reducing mean time to resolution (MTTR) by 35% and enabling faster onboarding of new team members"
    ],
    
    'devops_focused': [
        "Built and optimized CI/CD pipelines for Android AOSP development, reducing build times and improving deployment reliability",
        "Managed hybrid cloud infrastructure across Azure and on-premise environments",
        "Automated infrastructure provisioning using Terraform and configuration management tools"
    ]
}

# 🧱 LEGO BRICK: H3C Experience
H3C_BRICKS = {
    'incident_management_focused': [
        "Resolved high-severity production incident affecting 26 servers at H3C's largest Swedish customer (Zeekr) - performed systematic root cause analysis under time pressure, identified outdated configuration files causing cyclic crashes, and completed configuration upgrades within 5 hours to restore full production capacity",
        "Participated in on-call rotations providing 24/7 support for critical infrastructure issues, coordinating with engineering teams for complex problem resolution and escalation management",
        "Conducted multiple on-site visits for hardware troubleshooting and component replacement (motherboards, hard drives, data cables), performing diagnostics, minimizing downtime, and ensuring business continuity",
        "Delivered comprehensive technical training for H3C servers and network equipment, covering installation, configuration, troubleshooting procedures, and incident response best practices",
        "Created technical documentation and runbooks translated into Swedish and English, improving knowledge sharing, reducing incident response times, and enabling self-service troubleshooting",
        "Performed capacity planning and performance tuning for customer server infrastructure, optimizing resource utilization, preventing future incidents, and supporting growth planning"
    ]
}

# 🧱 LEGO BRICK: Synteda Experience
SYNTEDA_BRICKS = {
    'incident_management_focused': [
        "Provided technical support and incident response for customer applications on Azure cloud platform, performing remote diagnostics, debugging, and on-site problem resolution with SLA compliance",
        "Managed Azure cloud service configurations, database connectivity issues, API integration problems, and performance optimization for customer workloads",
        "Implemented monitoring and alerting solutions for production applications using Azure Monitor and Application Insights, enabling proactive incident detection and faster resolution",
        "Participated in on-call rotations for production support, troubleshooting critical issues, and coordinating with development teams for bug fixes and patches",
        "Conducted system deployments, training sessions, and troubleshooting at customer sites to ensure stable operations, knowledge transfer, and customer satisfaction"
    ]
}

def build_tata_cv_latex():
    """🧱 Build CV using LEGO bricks - Incident Management Specialist focus"""
    
    print("   🧱 Assembling LEGO bricks for Incident Management Specialist role...")
    
    # Select appropriate bricks
    profile = PROFILE_BRICKS['incident_management_specialist']
    skills = SKILLS_BRICKS['incident_management_primary']
    ecarx_bullets = ECARX_BRICKS['incident_management_focused']
    h3c_bullets = H3C_BRICKS['incident_management_focused']
    synteda_bullets = SYNTEDA_BRICKS['incident_management_focused']
    
    # Format bullets
    skills_items = "\n".join([f"\\item {skill}" for skill in skills])
    ecarx_items = "\n".join([f"\\item {bullet}" for bullet in ecarx_bullets])
    h3c_items = "\n".join([f"\\item {bullet}" for bullet in h3c_bullets])
    synteda_items = "\n".join([f"\\item {bullet}" for bullet in synteda_bullets])
    
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
{\Large \textit{Incident Management Specialist | DevOps/SRE Engineer}}\\[10pt]
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
""" + ecarx_items + r"""
\end{itemize}

\subsection*{H3C Technologies | Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + h3c_items + r"""
\end{itemize}

\subsection*{Synteda AB | Azure Developer \& Application Support (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + synteda_items + r"""
\end{itemize}

\subsection*{Pembio AB | Backend Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed backend services for Pembio.com platform using Java and Spring Boot with microservices architecture
\item Implemented CI/CD pipelines for automated testing and deployment, improving release velocity and code quality
\item Participated in Agile development processes (Scrum), collaborating with cross-functional teams on sprint planning and delivery
\end{itemize}

\section*{Education}
\textbf{IT-Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg, Sweden

\textbf{Mölndal Campus} | Bachelor's in Java Integration | 2019-2021 | Mölndal, Sweden

\textbf{University of Gothenburg} | Master's in International Business and Trade | 2016-2019 | Gothenburg, Sweden

\section*{Certifications}
\begin{itemize}[noitemsep]
\item AWS Certified Solutions Architect - Associate (2022)
\item AWS Certified Data Analytics - Specialty (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
\item H3C Server and Network Equipment Technical Training
\end{itemize}

\section*{Additional Information}
\begin{itemize}[noitemsep]
\item \textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native)
\item \textbf{Work Authorization:} Swedish Permanent Residence
\item \textbf{Availability:} Immediate | Based in Gothenburg, Sweden
\item \textbf{On-call Experience:} 3+ years with 24/7 multi-region support
\end{itemize}

\end{document}
"""
    
    return latex


def build_tata_cover_letter_latex():
    """🧱 Build cover letter using LEGO bricks - professional Overleaf style"""
    
    today = datetime.now().strftime("%B %d, %Y")
    
    latex = r"""\documentclass[a4paper,10pt]{article}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}

% Define colors
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}

% Remove paragraph indentation
\setlength{\parindent}{0pt}

\begin{document}
\pagestyle{empty}

{\color{darkblue}Tata Technologies\\
Digital Enterprise Solutions Department\\
Gothenburg, Sweden}

\vspace{40pt}

Dear Hiring Manager,

\vspace{10pt}

I'm excited to apply for the Incident Management Specialist position at Tata Technologies. With 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations, I'm confident I can contribute immediately to your Cloud \& Connectivity team.

\textbf{Incident Management Expertise:} At ECARX, I provide 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego). My most significant achievement was resolving a critical incident affecting 26 servers at H3C's largest Swedish customer (Zeekr) - I performed systematic root cause analysis under pressure, identified outdated configuration files causing cyclic crashes, and completed remediation within 5 hours. This experience demonstrates my ability to work under pressure, perform thorough RCA, and restore production systems rapidly.

\textbf{Infrastructure \& Automation:} I led the migration from Azure AKS to on-premise Kubernetes, reducing cloud costs by 45\% while improving CI/CD efficiency by 25\%. I deployed comprehensive Prometheus/Grafana monitoring stacks that reduced MTTR by 35\% through proactive alerting. I automate infrastructure using Terraform and Ansible, reducing manual intervention by 60\% and accelerating release cycles.

\textbf{Technical Alignment:} My skills directly match your requirements - AWS/Azure certified with hands-on experience in EC2, S3, Lambda, AKS; expert in Terraform and CloudFormation for IaC; proficient with Jenkins, GitHub Actions, and GitLab CI for CI/CD; deep expertise in Prometheus, Grafana, and ELK for observability; strong Python and Bash scripting for automation; production Kubernetes experience including troubleshooting and optimization.

\textbf{Why Tata Technologies:} I'm drawn to your focus on digital transformation for world-leading manufacturers. As a Gothenburg resident with Swedish permanent residence, I'm immediately available and excited about working on-site. My experience with international teams (English/Swedish/Chinese fluency) and Agile methodologies positions me well for your global environment.

I'm passionate about platform reliability, MTTR reduction, and developer experience improvements. I'd welcome the opportunity to discuss how my incident management expertise and infrastructure automation skills can contribute to Tata Technologies' success. Thank you for considering my application.

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


def compile_pdfs():
    """Compile LaTeX files to PDF"""
    import subprocess
    import os
    
    output_dir = "job_applications/tata_incident_management"
    
    print("\n📄 Compiling CV to PDF...")
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "Tata_Incident_Management_Harvad_CV.tex"],
            cwd=output_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            cv_size = os.path.getsize(f"{output_dir}/Tata_Incident_Management_Harvad_CV.pdf") / 1024
            print(f"   ✅ CV compiled: {cv_size:.1f} KB")
        else:
            print(f"   ⚠️ CV compilation had warnings (PDF may still be created)")
    except Exception as e:
        print(f"   ❌ CV compilation failed: {e}")
    
    print("\n📄 Compiling Cover Letter to PDF...")
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "Tata_Incident_Management_Harvad_CL.tex"],
            cwd=output_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            cl_size = os.path.getsize(f"{output_dir}/Tata_Incident_Management_Harvad_CL.pdf") / 1024
            print(f"   ✅ Cover Letter compiled: {cl_size:.1f} KB")
        else:
            print(f"   ⚠️ Cover Letter compilation had warnings (PDF may still be created)")
    except Exception as e:
        print(f"   ❌ Cover Letter compilation failed: {e}")
    
    # Clean up auxiliary files
    for ext in ['.aux', '.log', '.out']:
        for filename in ['Tata_Incident_Management_Harvad_CV', 'Tata_Incident_Management_Harvad_CL']:
            try:
                os.remove(f"{output_dir}/{filename}{ext}")
            except:
                pass


def main():
    load_env()
    
    print("🧱 LEGO BRICKS: Tata Technologies Incident Management Application")
    print("=" * 70)
    print("🎯 Role: Incident Management Specialist (DevOps/SRE)")
    print("🏢 Company: Tata Technologies")
    print("📍 Location: Gothenburg, Sweden")
    print("\n🧱 LEGO Bricks Strategy:")
    print("   ✅ Profile: Incident Management Specialist focus")
    print("   ✅ Skills: Incident response, monitoring, cloud platforms prioritized")
    print("   ✅ Experience: 26-server incident, 24/7 on-call, RCA expertise highlighted")
    print("   ✅ Achievements: 45% cost reduction, 35% MTTR reduction, 5-hour incident resolution")
    print("   ✅ Keywords: Terraform, Kubernetes, Prometheus, Grafana, Jenkins, AWS, Azure")
    print("=" * 70)
    
    # Create output directory
    output_dir = Path("job_applications/tata_incident_management")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build CV
    print("\n📄 Building CV with LEGO bricks...")
    cv_latex = build_tata_cv_latex()
    cv_path = output_dir / "Tata_Incident_Management_Harvad_CV.tex"
    with open(cv_path, "w", encoding="utf-8") as f:
        f.write(cv_latex)
    print("   ✅ CV LaTeX created")
    
    # Build Cover Letter
    print("\n📄 Building Cover Letter with LEGO bricks...")
    cl_latex = build_tata_cover_letter_latex()
    cl_path = output_dir / "Tata_Incident_Management_Harvad_CL.tex"
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_latex)
    print("   ✅ Cover Letter LaTeX created")
    
    # Compile PDFs
    compile_pdfs()
    
    print("\n" + "=" * 70)
    print("✅ LEGO BRICKS APPLICATION READY!")
    print("=" * 70)
    print(f"📁 Location: {output_dir}")
    print("\n🧱 LEGO Bricks Applied:")
    print("   • Incident Management Specialist identity (not generic DevOps)")
    print("   • 26-server incident resolution prominently featured")
    print("   • 24/7 on-call experience across 4 global offices")
    print("   • Quantified achievements: 45% cost reduction, 35% MTTR reduction")
    print("   • ATS-optimized keywords: Terraform, Kubernetes, Prometheus, Grafana")
    print("   • Role-specific skills ordering: Incident response first")
    print("\n📋 Next Steps:")
    print("   1. Review PDFs (should be opened automatically)")
    print("   2. Submit to Tata Technologies via LinkedIn/email")
    print("   3. Emphasize: 5-hour incident resolution, multi-region support, RCA expertise")


if __name__ == "__main__":
    main()
