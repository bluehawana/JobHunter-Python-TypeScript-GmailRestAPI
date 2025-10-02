#!/usr/bin/env python3
"""
Create Essity Cloud DevOps Application - Simple Version
Based on ECARX LEGO bricks pattern
"""
import os
from datetime import datetime
from pathlib import Path


def create_essity_cv() -> str:
    """Generate Essity-tailored CV LaTeX"""
    today = datetime.now().strftime('%Y.%m.%d')

    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{hyperref}

% Page setup
\geometry{margin=0.75in}
\pagestyle{empty}

% Color definitions
\definecolor{darkblue}{RGB}{0,51,102}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue
}

% ATS-friendly bullets
\setlist[itemize]{label=-, leftmargin=*}

\begin{document}
\pagestyle{empty}

% Name and contact
\begin{center}
{\LARGE \textbf{Hongzhi Li}}\\[10pt]
{\Large \textit{Cloud DevOps Engineer \& Site Reliability Specialist}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:+46728384299}{+46 728 384 299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\\[6pt]
Phone: +46 728 384 299 | Email: hongzhili01@gmail.com | Location: Gothenburg, Sweden
\end{center}

% Profile
\section*{Profile Summary}
Experienced Cloud DevOps Engineer with 4+ years of hands-on expertise in Azure, AWS, and GCP cloud platforms. Proven track record in site reliability engineering, DevOps, and DevSecOps practices within multinational organizations. Strong software development background in Python, C\#, and Go with high expertise in Docker, Terraform, Azure DevOps pipelines, Helm Charts, and multi-staging CI/CD deployments. AWS and Azure certified with a passion for sustainable technology solutions.

% Skills
\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Cloud Platforms (4+ years):} Microsoft Azure (primary), AWS, GCP; Multi-cloud architecture and migration
\item \textbf{DevOps Toolchains:} Docker, Terraform (IaC), Azure DevOps, Git, Helm Charts, Kubernetes (AKS/EKS/GKE)
\item \textbf{CI/CD Expertise:} Azure DevOps Pipelines (multi-staging), GitHub Actions, GitLab CI, Jenkins; Automated testing and deployment
\item \textbf{Programming Languages:} Python, C\#/.NET, Go, Bash/PowerShell; Infrastructure automation and tooling
\item \textbf{Site Reliability Engineering:} Prometheus, Grafana, System monitoring, Performance optimization, Incident response
\item \textbf{DevSecOps:} Security scanning, Vulnerability management, Compliance automation, Secret management
\item \textbf{Container Orchestration:} Kubernetes, Azure Kubernetes Service (AKS), Docker Swarm, Container security
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, Azure Cosmos DB, Database performance tuning
\item \textbf{Certifications:} AWS Solutions Architect Associate, AWS Developer Associate, Azure Fundamentals
\end{itemize}

% Experience
\section*{Professional Experience}

\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses by 40\%
\item Deployed comprehensive monitoring stack using Prometheus and Grafana to observe high-performance local cluster servers, tracking CPU usage, I/O performance, memory utilization, and network throughput
\item Conducted detailed performance analysis comparing on-premises GitLab runner environment with Azure Kubernetes Service (AKS), identifying 25\% performance improvement in CI/CD pipeline execution times
\item Implemented advanced Grafana dashboards for real-time infrastructure observability, enabling proactive issue detection and system optimization
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\end{itemize}

\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting both frontend and backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\item Built frontend features using Vue.js framework and integrated with backend APIs
\item Developed RESTful APIs and implemented comprehensive database integration
\item Participated in Agile development processes and collaborated with cross-functional teams
\end{itemize}

\section*{Hobby Projects}

\subsection*{AKS\_to\_OnPrem\_K8s\_Migration}
\textit{Oct 2024 -- Present} \\
\textbf{Azure Kubernetes Service, Terraform, Prometheus, Grafana, Docker}
\begin{itemize}
\item Led infrastructure optimization project migrating from AKS to on-premises Kubernetes, reducing operational costs by 40\%
\item Implemented comprehensive monitoring stack using Prometheus and Grafana for CPU, I/O, memory, and network metrics
\item Conducted detailed performance analysis comparing AKS vs on-prem, achieving 25\% improvement in CI/CD pipeline execution
\item Deployed advanced Grafana dashboards for real-time infrastructure observability and proactive issue detection
\end{itemize}

\subsection*{Azure\_DevOps\_Multi\_Stage\_Pipeline}
\textit{2024} \\
\textbf{Azure DevOps, Terraform, Helm Charts, Docker, C\#}
\begin{itemize}
\item Designed and implemented multi-staging CI/CD pipeline with dev, staging, and production environments
\item Automated infrastructure provisioning using Terraform modules and Helm Charts for Kubernetes deployments
\item Integrated security scanning, automated testing, and compliance checks into deployment pipeline
\item Achieved zero-downtime deployments with blue-green deployment strategy
\end{itemize}

\subsection*{Jobhunter\_Python\_Cloud\_Automation}
\textit{July 2024 -- Present} \\
\textbf{Python, Azure, AWS, Docker, GitHub Actions, REST APIs}
\begin{itemize}
\item Built automated job hunting pipeline with Gmail API integration and NLP-based resume customization
\item Deployed on Azure with CI/CD automation using GitHub Actions and Docker containers
\item Implemented monitoring and alerting for system reliability and performance optimization
\item Demo: https://jobs.bluehawana.com
\end{itemize}

\subsection*{Weather\_Anywhere\_Multi\_Cloud}
\textit{Feb 2024 -- Present} \\
\textbf{Spring Boot, Alibaba Cloud ECS, Azure, MySQL, Terraform}
\begin{itemize}
\item Weather tracking application deployed across multiple cloud providers for high availability
\item Infrastructure as Code using Terraform for automated provisioning and disaster recovery
\item Integrated with OpenCageData and Open-Meteo APIs for real-time weather data
\item Demo: https://weather.bluehawana.com
\end{itemize}

\section*{Education}
\textbf{IT Högskolan}\\
\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\
\textbf{Mölndal Campus}\\
\textit{Bachelor's Degree in Java Integration} | 2019-2021\\
\textbf{University of Gothenburg}\\
\textit{Master's Degree in International Business and Trade} | 2016-2019\\

\section*{Certifications}
\begin{itemize}
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\end{itemize}

\section*{Additional Information}
\begin{itemize}
\item \textbf{Languages:} Fluent in English and Mandarin
\item \textbf{Interests:} Sustainable technology, cloud infrastructure, energy efficiency, climate-neutral solutions
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\end{itemize}

\end{document}
"""
    return latex


def create_essity_cl() -> str:
    """Generate Essity cover letter LaTeX"""
    today = datetime.now().strftime('%Y.%m.%d')

    latex = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{xcolor}\definecolor{darkblue}{rgb}{0.0,0.2,0.6}
\setlength{\parindent}{0pt}
\begin{document}\pagestyle{empty}
\begin{letter}{Essity\\Munich, Germany}
\opening{Dear Hiring Manager,}

I am writing to express my strong interest in the Cloud DevOps Engineer position at Essity. With over 4 years of hands-on experience in cloud technologies, DevOps practices, and site reliability engineering across multinational organizations, I am excited about the opportunity to contribute to Essity's mission of improving quality of life through sustainable hygiene and health solutions.

My expertise spans Microsoft Azure (primary), AWS, and GCP, with proven experience in designing and managing multi-cloud architectures. Currently serving as IT/Infrastructure Specialist at ECARX, I recently led a significant infrastructure optimization project migrating from Azure Kubernetes Service to on-premises Kubernetes, achieving a 40\% reduction in operational costs. I deployed comprehensive monitoring using Prometheus and Grafana, and conducted detailed performance analysis that resulted in 25\% improvement in CI/CD pipeline execution times.

I have high expertise with the DevOps toolchains you require: Docker for containerization, Terraform for infrastructure as code, Azure DevOps for CI/CD pipelines, Git for version control, and Helm Charts for Kubernetes deployments. I have extensive experience in Azure DevOps CI/CD pipeline multi-staging code deployment administration, implementing dev, staging, and production environments with automated testing, security scanning, and zero-downtime deployments using blue-green strategies.

My software development background includes Python, C\#/.NET, and Go, which enables me to bridge the gap between development and operations effectively. I hold AWS Certified Solutions Architect Associate and AWS Certified Developer Associate certifications, demonstrating my commitment to professional excellence in cloud technologies.

What particularly resonates with me about Essity is your commitment to sustainability and the ``Business Ambition for 1.5 Degrees'' initiative. I am passionate about leveraging technology to create positive environmental impact, and I would be honored to contribute my DevOps and cloud expertise to help Essity achieve climate neutrality by 2050 while delivering high-quality hygiene and health solutions with maximum resource efficiency.

I am eager to bring my DevOps expertise, cloud architecture knowledge, and passion for sustainable technology to Essity's team in Munich. Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to Essity's continued success.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg, Sweden\\hongzhili01@gmail.com\\+46 728 384 299\\""" + today + r"""}
\end{letter}\end{document}
"""
    return latex


def main():
    print("🚀 Generating Essity Cloud DevOps Application (LEGO Bricks Style)...")

    # Create essity folder if it doesn't exist
    essity_folder = Path("job_applications/essity")
    essity_folder.mkdir(parents=True, exist_ok=True)

    # Generate CV
    cv_latex = create_essity_cv()
    cv_tex = essity_folder / \
        f"Essity_Cloud_DevOps_CV_{datetime.now().strftime('%Y%m%d')}.tex"
    cv_tex.write_text(cv_latex, encoding='utf-8')
    print(f"✅ CV LaTeX: {cv_tex}")

    # Generate Cover Letter
    cl_latex = create_essity_cl()
    cl_tex = essity_folder / \
        f"Essity_Cloud_DevOps_CL_{datetime.now().strftime('%Y%m%d')}.tex"
    cl_tex.write_text(cl_latex, encoding='utf-8')
    print(f"✅ Cover Letter LaTeX: {cl_tex}")

    print("\n🎯 ESSITY APPLICATION READY!")
    print("=" * 60)
    print("📱 KEY HIGHLIGHTS:")
    print("✅ 4+ years Azure/AWS/GCP experience")
    print("✅ DevOps & SRE expertise (Docker, Terraform, K8s)")
    print("✅ Azure DevOps CI/CD multi-staging pipelines")
    print("✅ Software development (Python, C#, Go)")
    print("✅ AWS & Azure certified")
    print("✅ 40% cost reduction through AKS migration")
    print("✅ 25% CI/CD performance improvement")
    print("✅ Passion for sustainable technology")
    print("\n📄 FILES GENERATED:")
    print(f"   • {cv_tex}")
    print(f"   • {cl_tex}")
    print("\n💡 NEXT STEPS:")
    print("   1. Compile LaTeX files to PDF using Overleaf or local LaTeX")
    print("   2. Review and customize if needed")
    print("   3. Submit to Essity!")


if __name__ == '__main__':
    main()
