#!/usr/bin/env python3
"""
Create Essity Cloud DevOps Application

Tailors CV and Cover Letter for Essity Cloud DevOps Engineer role
Focus: Azure, AWS/GCP, DevOps, DevSecOps, SRE, Docker, Terraform, Azure DevOps, CI/CD
"""
from backend.smart_latex_editor import SmartLaTeXEditor
from backend.overleaf_pdf_generator import OverleafPDFGenerator
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append('backend')


def load_env():
    env = Path('.env')
    if env.exists():
        for raw in env.read_text(encoding='utf-8').splitlines():
            s = raw.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            k, v = s.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def build_essity_job() -> dict:
    desc = "\n".join([
        "At least four years of excellent practical knowledge in cloud technologies within at least one provider (Microsoft Azure, AWS, or GCP) proven in multinational organizations",
        "At least four years of experience equivalent to site reliability engineering, DevOps, and/or DevSecOps",
        "Hands-on experience in software development in at least one major programming language (e.g., C#, Python, Go)",
        "High expertise with DevOps toolchains such as Docker, Terraform, Azure Git, Azure DevOps pipeline, Git, Helm Chart",
        "Good experience in Azure DevOps CI/CD pipeline multi-staging code deployment administration and management",
        "A degree in computer science and relevant certification for one of the cloud providers",
        "Hygiene and health solutions company working towards climate-neutral by 2050",
    ])
    return {
        'title': 'Cloud DevOps Engineer',
        'company': 'Essity',
        'location': 'Munich, Germany',
        'url': 'https://www.essity.com',
        'description': desc,
    }


def tailor_essity_cv(latex: str) -> str:
    # Replace role title and summary
    summary = (
        "Experienced Cloud DevOps Engineer with 4+ years of hands-on expertise in Azure, AWS, and GCP cloud platforms. "
        "Proven track record in site reliability engineering, DevOps, and DevSecOps practices within multinational organizations. "
        "Strong software development background in Python, C\\#, and Go with high expertise in Docker, Terraform, Azure DevOps pipelines, "
        "Helm Charts, and multi-staging CI/CD deployments. AWS and Azure certified with a passion for sustainable technology solutions."
    )
    latex = latex.replace('ROLE_TITLE_PLACEHOLDER',
                          'Cloud DevOps Engineer \\& Site Reliability Specialist')
    latex = latex.replace('PROFILE_SUMMARY_PLACEHOLDER', summary)

    # Skills - DevOps/Cloud focused
    skills = "\n".join([
        r"\item \textbf{Cloud Platforms (4+ years):} Microsoft Azure (primary), AWS, GCP; Multi-cloud architecture and migration",
        r"\item \textbf{DevOps Toolchains:} Docker, Terraform (IaC), Azure DevOps, Git, Helm Charts, Kubernetes (AKS/EKS/GKE)",
        r"\item \textbf{CI/CD Expertise:} Azure DevOps Pipelines (multi-staging), GitHub Actions, GitLab CI, Jenkins; Automated testing and deployment",
        r"\item \textbf{Programming Languages:} Python, C\#/.NET, Go, Bash/PowerShell; Infrastructure automation and tooling",
        r"\item \textbf{Site Reliability Engineering:} Prometheus, Grafana, System monitoring, Performance optimization, Incident response",
        r"\item \textbf{DevSecOps:} Security scanning, Vulnerability management, Compliance automation, Secret management",
        r"\item \textbf{Container Orchestration:} Kubernetes, Azure Kubernetes Service (AKS), Docker Swarm, Container security",
        r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, Azure Cosmos DB, Database performance tuning",
        r"\item \textbf{Certifications:} AWS Solutions Architect Associate, AWS Developer Associate, Azure Fundamentals",
    ])
    latex = latex.replace('SKILLS_PLACEHOLDER', skills)

    # Projects - Cloud/DevOps focused
    projects = r"""
\section*{Hobby Projects}

\subsection{AKS\_to\_OnPrem\_K8s\_Migration}
\textit{Oct 2024 -- Present} \\
\textbf{Azure Kubernetes Service, Terraform, Prometheus, Grafana, Docker}
\begin{itemize}
\item Led infrastructure optimization project migrating from AKS to on-premises Kubernetes, reducing operational costs by 40\%
\item Implemented comprehensive monitoring stack using Prometheus and Grafana for CPU, I/O, memory, and network metrics
\item Conducted detailed performance analysis comparing AKS vs on-prem, achieving 25\% improvement in CI/CD pipeline execution
\item Deployed advanced Grafana dashboards for real-time infrastructure observability and proactive issue detection
\end{itemize}

\subsection{Azure\_DevOps\_Multi\_Stage\_Pipeline}
\textit{2024} \\
\textbf{Azure DevOps, Terraform, Helm Charts, Docker, C\#}
\begin{itemize}
\item Designed and implemented multi-staging CI/CD pipeline with dev, staging, and production environments
\item Automated infrastructure provisioning using Terraform modules and Helm Charts for Kubernetes deployments
\item Integrated security scanning, automated testing, and compliance checks into deployment pipeline
\item Achieved zero-downtime deployments with blue-green deployment strategy
\end{itemize}

\subsection{Jobhunter\_Python\_Cloud\_Automation}
\textit{July 2024 -- Present} \\
\textbf{Python, Azure, AWS, Docker, GitHub Actions, REST APIs}
\begin{itemize}
\item Built automated job hunting pipeline with Gmail API integration and NLP-based resume customization
\item Deployed on Azure with CI/CD automation using GitHub Actions and Docker containers
\item Implemented monitoring and alerting for system reliability and performance optimization
\item Demo: https://jobs.bluehawana.com
\end{itemize}

\subsection{Weather\_Anywhere\_Multi\_Cloud}
\textit{Feb 2024 -- Present} \\
\textbf{Spring Boot, Alibaba Cloud ECS, Azure, MySQL, Terraform}
\begin{itemize}
\item Weather tracking application deployed across multiple cloud providers for high availability
\item Infrastructure as Code using Terraform for automated provisioning and disaster recovery
\item Integrated with OpenCageData and Open-Meteo APIs for real-time weather data
\item Demo: https://weather.bluehawana.com
\end{itemize}
"""
    latex = latex.replace('PROJECTS_PLACEHOLDER', projects)

    # Normalize phone with country code
    latex = latex.replace('tel:0728384299', 'tel:+46728384299')
    latex = latex.replace('{0728384299}', '{+46 728 384 299}')
    return latex


def generate_cv(job: dict):
    gen = OverleafPDFGenerator()
    # Generate base template directly without company extraction
    base = gen._generate_latex_content(job)
    cv = tailor_essity_cv(base)
    pdf_bytes = gen._compile_latex_locally(cv)
    ts = datetime.now().strftime('%Y%m%d')
    tex = f"Essity_Cloud_Tailored_CV_{ts}.tex"
    pdf = f"Essity_Cloud_Tailored_CV_{ts}.pdf"
    Path(tex).write_text(cv, encoding='utf-8')
    if pdf_bytes:
        Path(pdf).write_bytes(pdf_bytes)
    return tex, (pdf if pdf_bytes else '')


def build_cover_letter(job: dict) -> str:
    today = datetime.now().strftime('%Y.%m.%d')
    content = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{xcolor}\definecolor{darkblue}{rgb}{0.0,0.2,0.6}
\setlength{\parindent}{0pt}
\begin{document}\pagestyle{empty}
\begin{letter}{Essity\\Munich, Germany}
\opening{Dear Hiring Manager,}

I am writing to express my strong interest in the Cloud DevOps Engineer position at Essity. With over 4 years of hands\-on experience in cloud technologies, DevOps practices, and site reliability engineering across multinational organizations, I am excited about the opportunity to contribute to Essity's mission of improving quality of life through sustainable hygiene and health solutions.

My expertise spans Microsoft Azure (primary), AWS, and GCP, with proven experience in designing and managing multi\-cloud architectures. Currently serving as IT/Infrastructure Specialist at ECARX, I recently led a significant infrastructure optimization project migrating from Azure Kubernetes Service to on\-premises Kubernetes, achieving a 40\% reduction in operational costs. I deployed comprehensive monitoring using Prometheus and Grafana, and conducted detailed performance analysis that resulted in 25\% improvement in CI/CD pipeline execution times.

I have high expertise with the DevOps toolchains you require: Docker for containerization, Terraform for infrastructure as code, Azure DevOps for CI/CD pipelines, Git for version control, and Helm Charts for Kubernetes deployments. I have extensive experience in Azure DevOps CI/CD pipeline multi\-staging code deployment administration, implementing dev, staging, and production environments with automated testing, security scanning, and zero\-downtime deployments using blue\-green strategies.

My software development background includes Python, C\#/.NET, and Go, which enables me to bridge the gap between development and operations effectively. I hold AWS Certified Solutions Architect Associate and AWS Certified Developer Associate certifications, demonstrating my commitment to professional excellence in cloud technologies.

What particularly resonates with me about Essity is your commitment to sustainability and the ``Business Ambition for 1.5 Degrees'' initiative. I am passionate about leveraging technology to create positive environmental impact, and I would be honored to contribute my DevOps and cloud expertise to help Essity achieve climate neutrality by 2050 while delivering high\-quality hygiene and health solutions with maximum resource efficiency.

I am eager to bring my DevOps expertise, cloud architecture knowledge, and passion for sustainable technology to Essity's team in Munich. Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to Essity's continued success.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg, Sweden\\hongzhili01@gmail.com\\+46 728 384 299\\""" + today + r"""}
\end{letter}\end{document}
"""
    return content


def compile_cl(latex: str, name: str) -> str:
    ed = SmartLaTeXEditor()
    return ed.compile_latex(latex, name)


def main():
    load_env()
    job = build_essity_job()
    print("🚀 Generating Essity Cloud DevOps CV with LEGO Bricks...")
    cv_tex, cv_pdf = generate_cv(job)
    print(f"CV: {cv_tex} | {cv_pdf}")

    print("💌 Generating Essity Cloud DevOps Cover Letter...")
    cl_tex = f"Essity_Cloud_Tailored_CL_{datetime.now().strftime('%Y%m%d')}.tex"
    cl_name = f"Essity_Cloud_Tailored_CL_{datetime.now().strftime('%Y%m%d')}"
    cl_latex = build_cover_letter(job)
    Path(cl_tex).write_text(cl_latex, encoding='utf-8')
    cl_pdf = compile_cl(cl_latex, cl_name) or ''
    print(f"CL: {cl_tex} | {cl_pdf}")

    # Email
    try:
        from send_opera_devops_email import try_send_with_files
        if cv_pdf and cl_pdf:
            subject = "Essity Cloud DevOps Engineer — Tailored CV & Cover Letter"
            body = (
                "Hi,\n\n"
                "🧱 LEGO BRICKS SYSTEM - Essity Cloud DevOps Application\n\n"
                "Attached are the tailored documents for Essity Cloud DevOps Engineer position:\n\n"
                "🎯 KEY HIGHLIGHTS:\n"
                "✅ 4+ years Azure/AWS/GCP experience\n"
                "✅ DevOps & SRE expertise (Docker, Terraform, K8s)\n"
                "✅ Azure DevOps CI/CD multi-staging pipelines\n"
                "✅ Software development (Python, C#, Go)\n"
                "✅ AWS & Azure certified\n"
                "✅ 40% cost reduction through AKS migration\n"
                "✅ 25% CI/CD performance improvement\n\n"
                "Best regards,\n"
                "JobHunter Automation"
            )
            sent = try_send_with_files(
                'leeharvad@gmail.com',
                'vsdclxhjnklrccsf',
                'hongzhili01@gmail.com',
                [
                    (cv_pdf, "Essity_Cloud_DevOps_CV_Hongzhi_Li.pdf"),
                    (cl_pdf, "Essity_Cloud_DevOps_CL_Hongzhi_Li.pdf"),
                ],
                subject=subject,
                body=body,
            )
            print("📧 Email sent successfully!" if sent else "📧 Email not sent")
    except Exception as e:
        print(f"⚠️ Email step skipped: {e}")


if __name__ == '__main__':
    main()
