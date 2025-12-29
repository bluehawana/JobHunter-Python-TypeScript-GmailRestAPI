#!/usr/bin/env python3
"""
Nasdaq Software Developer - DevOps & Cloud Application Generator
Using LEGO Bricks Methodology with FinTech + FinOps focus
Company: Nasdaq (Eqlipse CSD)
Location: Stockholm, Sweden
"""

import subprocess
import os
from datetime import datetime

# ============================================================================
# LEGO BRICKS: Modular CV Components
# ============================================================================

def profile_brick_fintech_devops():
    """Profile brick optimized for FinTech DevOps role"""
    return r"""
\section*{Professional Summary}

DevOps \& Cloud Engineer with 5+ years of technical experience and 8+ years as Corporate Finance Specialist in banking sector, uniquely combining financial domain expertise with cloud infrastructure skills. Proven track record in cloud cost optimization (reduced Azure costs from \$65K to \$35.7K/month = \$350K+ annual savings through FinOps practices, HPC migration, and service optimization), Kubernetes orchestration, and real-world payment systems integration (Stripe API, PayPal/iZettle for e-commerce platforms). Expert in AWS, Terraform, GitLab CI/CD automation, and building scalable infrastructure. Strong background in financial analysis (Excel, Python), distributed systems, and infrastructure automation. Eager to deepen Kafka expertise and mentor teams on cloud-native best practices. Passionate about hyper-automation, developer experience, and delivering reliable solutions for mission-critical financial systems.
"""

def skills_brick_fintech_cloud():
    """Skills brick highlighting FinTech, Cloud, and DevOps"""
    return r"""
\section*{Core Technical Competencies}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item \textbf{FinTech \& Finance Domain:} 8+ years as Corporate Finance Specialist in banking, Financial evaluation \& modeling (Excel, Python), Payment systems integration (Stripe API on ichiban.biz \& smrtmart.com, PayPal/iZettle POS integration), Client evaluation \& presentations, Business analysis
\item \textbf{Cloud Platforms \& FinOps:} AWS (5+ years - EC2, S3, Lambda, CloudFormation, CloudWatch, IAM, VPC), Azure, FinOps practices, Cost optimization (\$65K to \$35.7K/month = 45\% reduction, \$350K+ annual savings), HPC migration \& tuning, Multi-account management
\item \textbf{Infrastructure as Code:} Terraform (expert), CloudFormation, Ansible, Infrastructure automation, Environment provisioning (Dev/QA/UAT/Prod)
\item \textbf{Container Orchestration:} Kubernetes (production experience), Docker, Helm Charts, Container security, AKS migration experience
\item \textbf{CI/CD \& Automation:} GitLab CI, GitHub Actions, Jenkins, Pipeline development, Build automation, Deployment automation, Hyper-automation mindset
\item \textbf{Messaging \& Streaming:} Kafka (production experience - Gothenburg taxi pooling \& car fleet rental systems), Event-driven architecture, Distributed systems, Message queue systems
\item \textbf{Programming:} Python (expert), Bash, Java (familiar), Go (familiar), Scripting automation
\item \textbf{Monitoring \& Observability:} Prometheus, Grafana, CloudWatch, ELK Stack, Performance optimization, Cost monitoring
\item \textbf{DevOps Practices:} Agile/Scrum, Sprint planning, Peer reviews, Documentation, Knowledge sharing, Mentoring
\item \textbf{Database Systems:} PostgreSQL, MySQL, MongoDB, Redis, Database optimization
\end{itemize}
"""

def experience_brick_ecarx_finops():
    """ECARX experience highlighting FinOps and cloud optimization"""
    return r"""
\section*{Professional Experience}

\subsection*{Ecarx (Geely Automotive) | IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Led Azure cost optimization initiative reducing monthly costs from \$65,000 to \$35,750 (45\% reduction, \$350K+ annual savings) through strategic migration of expensive Azure services to local HPC, HPC performance tuning, Azure service optimization, and AKS to on-premise Kubernetes migration
\item Designed and implemented Infrastructure as Code using Terraform for automated provisioning of Dev/QA/UAT/Production environments across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
\item Built and maintained CI/CD pipelines using GitHub Actions and GitLab CI, reducing deployment time by 25\% and improving developer experience through automation
\item Deployed comprehensive monitoring stack (Prometheus/Grafana) for proactive incident detection, capacity planning, and cost tracking across hybrid cloud infrastructure
\item Managed multi-region infrastructure with 24/7 on-call support, resolving critical incidents including 26-server recovery in 5 hours through systematic troubleshooting
\item Automated infrastructure provisioning and deployment processes, reducing manual intervention by 60\% and accelerating release cycles
\item Created comprehensive documentation and runbooks for infrastructure setup, deployment procedures, and troubleshooting guides
\item Mentored team members on Kubernetes, Terraform, and cloud-native best practices, improving team capability and knowledge sharing
\end{itemize}
"""

def experience_brick_h3c():
    """H3C experience"""
    return r"""
\subsection*{H3C Technologies | Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Resolved critical production incident affecting 26 servers through systematic root cause analysis and remediation within 5 hours
\item Provided 24/7 on-call support for mission-critical infrastructure, coordinating with engineering teams for complex problem resolution
\item Created technical documentation and operational guides in Swedish and English for knowledge sharing and team enablement
\end{itemize}
"""

def experience_brick_synteda_fintech():
    """Synteda experience with FinTech angle"""
    return r"""
\subsection*{Synteda AB | Azure Developer \& Application Support (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Developed and maintained cloud applications on Azure platform using C\#/.NET Core with microservices architecture
\item Integrated Stripe API for payment processing on ichiban.biz and smrtmart.com e-commerce platforms, handling secure financial transactions
\item Implemented PayPal (iZettle) POS integration enabling customers to order online and pay at physical shop location, bridging online-to-offline payment flow
\item Managed Azure cloud configurations, database connectivity, and API integrations for financial services applications
\item Implemented monitoring and cost optimization strategies for Azure resources, reducing operational expenses
\end{itemize}
"""

def experience_brick_pembio():
    """Pembio experience"""
    return r"""
\subsection*{Pembio AB | Full-Stack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Developed backend services using Java/Spring Boot with microservices architecture for e-commerce platform
\item Built RESTful APIs and implemented CI/CD pipelines for automated testing and deployment
\item Participated in Agile/Scrum development processes with sprint planning, peer reviews, and retrospectives
\end{itemize}
"""

def experience_brick_finance():
    """Finance/Banking experience brick"""
    return r"""
\subsection*{Banking \& Finance Sector | Corporate Finance Specialist}
\textit{2012 - 2019 | China \& Sweden}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item Performed financial evaluation and modeling using Excel and Python for client candidate assessment in corporate finance division
\item Conducted business analysis and presented evaluation results to supervisors, supporting investment and lending decisions
\item Gained deep understanding of financial operations, regulatory requirements, post-trade processes, and settlement systems
\item Worked with payment systems, transaction processing, and financial data management in international banking environment
\item Developed expertise in financial services technology, compliance requirements, and operational risk management
\item Collaborated with cross-functional teams on financial system implementations and process improvements
\end{itemize}
"""

def projects_brick_kafka():
    """Kafka projects section"""
    return r"""
\section*{Key Technical Projects}

\subsection*{Gothenburg Taxi Pooling System}
\textbf{Technologies:} Kafka, Java, Distributed Systems, Event-driven Architecture
\begin{itemize}[leftmargin=*, itemsep=1pt]
\item Built event-driven taxi pooling system using Kafka for real-time ride matching and coordination
\item Implemented Kafka producers/consumers for handling ride requests, driver availability, and location updates
\item Designed distributed system architecture for scalable, fault-tolerant ride-sharing operations
\item Available on GitHub: github.com/bluehawana
\end{itemize}

\subsection*{Car Fleet Rental Management System}
\textbf{Technologies:} Kafka, Microservices, Event Streaming, Java
\begin{itemize}[leftmargin=*, itemsep=1pt]
\item Developed car fleet rental system with Kafka-based event streaming for booking, availability, and fleet management
\item Implemented event-driven architecture for real-time inventory updates and reservation processing
\item Built microservices communicating via Kafka topics for scalable, decoupled system design
\end{itemize}
"""

def education_brick():
    """Education section"""
    return r"""
\section*{Education}

\textbf{IT-Hogskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg

\textbf{Molndal Campus} | Bachelor's in Java Integration | 2019-2021 | Molndal

\textbf{University of Gothenburg} | Master's in International Business \& Trade | 2016-2019 | Gothenburg
\begin{itemize}[leftmargin=*, itemsep=1pt]
\item Focus: International Finance, Trade Operations, Business Analytics
\end{itemize}
"""

def certifications_brick():
    """Certifications"""
    return r"""
\section*{Certifications}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item AWS Certified Solutions Architect - Associate (2022)
\item AWS Certified Data Analytics - Specialty (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
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

\textbf{Availability:} Immediate - Ready to relocate to Stockholm

\textbf{Key Strengths:} FinTech domain knowledge, FinOps expertise, Hyper-automation mindset, Mentoring
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
{\Large DevOps \& Cloud Engineer | FinTech Specialist}\\[10pt]
hongzhili01@gmail.com | +46 72 838 4299 | Gothenburg, Sweden\\
linkedin.com/in/hzl | github.com/bluehawana
\end{center}

\vspace{8pt}
"""

    # Assemble CV with LEGO bricks
    cv_content = header
    cv_content += profile_brick_fintech_devops()
    cv_content += skills_brick_fintech_cloud()
    cv_content += experience_brick_ecarx_finops()
    cv_content += experience_brick_h3c()
    cv_content += experience_brick_synteda_fintech()
    cv_content += experience_brick_pembio()
    cv_content += experience_brick_finance()
    cv_content += projects_brick_kafka()
    cv_content += education_brick()
    cv_content += certifications_brick()
    
    cv_content += r"""
\end{document}
"""
    
    return cv_content

def create_cover_letter_latex():
    """Create cover letter for Nasdaq position"""
    
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

{\color{darkblue}Nasdaq\\
Eqlipse CSD - Cloud \& Platform Team Nexus\\
Stockholm, Sweden}

\vspace{40pt}

Dear Hiring Manager,

\vspace{10pt}

I am excited to apply for the Software Developer - DevOps and Cloud position at Nasdaq's Eqlipse CSD team. With 5+ years of DevOps/Cloud experience combined with 8+ years in banking and finance, I bring the unique combination of technical expertise and FinTech domain knowledge that makes me an ideal fit for your post-trade infrastructure team.

\textbf{FinTech Domain Expertise:} My 8+ years as Corporate Finance Specialist in banking gives me deep understanding of financial operations, post-trade processes, and settlement systems. I performed financial evaluation using Excel and Python, conducted business analysis, and presented client assessments to supervisors. I've implemented real payment systems: Stripe API integration on ichiban.biz and smrtmart.com, and PayPal (iZettle) POS integration enabling online-to-physical payment flow. This domain knowledge allows me to understand not just the "how" but the "why" behind financial infrastructure decisions - directly applicable to CSD operations.

\textbf{Cloud \& FinOps Excellence:} At ECARX, I led an Azure cost optimization initiative that reduced monthly costs from \$65,000 to \$35,750 (45\% reduction = \$350K+ annual savings). I achieved this by: (1) migrating expensive Azure services to local HPC infrastructure, (2) HPC performance tuning achieving world top 10\% performance, (3) optimizing Azure service configurations and product selections, and (4) strategic AKS to on-premise Kubernetes migration. I designed Infrastructure as Code using Terraform for automated provisioning of Dev/QA/UAT/Production environments across 4 global offices. This experience directly aligns with your need to "optimize Cloud footprint for lower costs and higher performance."

\textbf{DevOps \& Automation:} I built and maintained CI/CD pipelines using GitLab CI and GitHub Actions, reducing deployment time by 25\% and improving developer experience through hyper-automation. I automated infrastructure provisioning processes, reducing manual intervention by 60\%. My approach focuses on enabling teams through automation, comprehensive documentation, and knowledge sharing - exactly what you need for "better Developer Experience and higher efficiency."

\textbf{Kafka \& Distributed Systems:} I have hands-on Kafka experience from building event-driven systems for Gothenburg taxi pooling and car fleet rental projects (available on my GitHub). I implemented Kafka for real-time event streaming, message processing, and distributed system coordination. Combined with my production Kubernetes experience (AKS to on-premise migration), I understand how to build and operate scalable, distributed systems. I'm eager to deepen my Kafka expertise in a production FinTech environment and mentor team members on event-driven architecture best practices.

\textbf{Collaboration \& Mentoring:} I actively mentor team members on Kubernetes, Terraform, and cloud-native practices. I participate in peer reviews, sprint planning, and retrospectives. I'm an active member of AWS User Group Gothenburg and CNCF Gothenburg community, demonstrating my commitment to knowledge sharing and continuous learning.

\textbf{Why Nasdaq:} I'm genuinely passionate about FinTech and excited to work on infrastructure that powers global financial markets. The combination of cutting-edge cloud technology and mission-critical financial systems is exactly where I want to grow my career. I'm ready to relocate to Stockholm and embrace the hybrid work model (3+ days in office).

I would welcome the opportunity to discuss how my FinTech domain knowledge, FinOps expertise, and DevOps skills can contribute to Eqlipse CSD's success. Thank you for considering my application.

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
    print("🧱 Nasdaq DevOps & Cloud Application Generator")
    print("=" * 70)
    print("🎯 Role: Software Developer - DevOps & Cloud")
    print("🏢 Company: Nasdaq (Eqlipse CSD)")
    print("📍 Location: Stockholm, Sweden")
    print()
    print("🧱 LEGO Bricks Strategy:")
    print("   ✅ FinTech Domain: 8+ years banking/finance experience")
    print("   ✅ FinOps: 45% cost reduction through cloud optimization")
    print("   ✅ Payment Systems: Stripe/PayPal integration experience")
    print("   ✅ Cloud: AWS, Terraform, Kubernetes expertise")
    print("   ✅ Automation: CI/CD, hyper-automation mindset")
    print("   ✅ Mentoring: Community involvement, knowledge sharing")
    print("=" * 70)
    print()
    
    output_dir = "job_applications/nasdaq_devops_cloud"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate CV
    print("📄 Generating CV...")
    cv_latex = create_cv_latex()
    cv_success = compile_latex_to_pdf(cv_latex, "Nasdaq_DevOps_Cloud_Harvad_CV", output_dir)
    
    print()
    
    # Generate Cover Letter
    print("📄 Generating Cover Letter...")
    cl_latex = create_cover_letter_latex()
    cl_success = compile_latex_to_pdf(cl_latex, "Nasdaq_DevOps_Cloud_Harvad_CL", output_dir)
    
    print()
    print("=" * 70)
    
    if cv_success and cl_success:
        print("✅ Application package generated successfully!")
        print(f"📁 Location: {output_dir}/")
        print("📄 Files:")
        print(f"   - Nasdaq_DevOps_Cloud_Harvad_CV.pdf")
        print(f"   - Nasdaq_DevOps_Cloud_Harvad_CL.pdf")
        print()
        print("🎯 Key Differentiators:")
        print("   • 8+ years FinTech/banking domain knowledge")
        print("   • 45% cloud cost reduction (FinOps expertise)")
        print("   • Payment systems integration (Stripe/PayPal)")
        print("   • Terraform + Kubernetes production experience")
        print("   • Ready to relocate to Stockholm")
    else:
        print("⚠️  Some files failed to generate. Check errors above.")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
