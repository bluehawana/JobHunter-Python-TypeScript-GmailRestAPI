#!/usr/bin/env python3
"""
Create SKF Full‑Stack Application (Azure/OCI focus)

Generates a tailored CV (LaTeX + PDF) and Cover Letter (LaTeX + PDF)
for SKF full‑stack role using LEGO logic, then emails results if configured.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append('backend')

from backend.overleaf_pdf_generator import OverleafPDFGenerator
from backend.smart_latex_editor import SmartLaTeXEditor


def load_env():
    env = Path('.env')
    if env.exists():
        for raw in env.read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip(); v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def build_skf_job() -> dict:
    desc = "\n".join([
        "Design, develop, and maintain cloud-based applications with Azure and OCI",
        "Work across full stack: front-end (React/Angular) + back-end (microservices, REST)",
        "Optimize cloud solutions for global markets and regulatory requirements",
        "Collaborate cross-functionally; provide technical leadership and mentorship",
        "Support infrastructure transformation in line with architectural guidelines",
        "Set domain/sub-domain policies and guardrails; cyber security collaboration",
        "Explore new technologies for innovation, efficiency, and compliance",
        "Maintain architectural knowledge and manage dependencies across landscape",
        "Stack: Azure App Services, Functions, SQL Database, Azure DevOps; OCI; AWS (general)",
        "Docker, Kubernetes, CI/CD, multi/hybrid cloud networking",
    ])
    return {
        'title': 'Senior Fullstack Engineer',
        'company': 'SKF',
        'location': 'Gothenburg, Sweden',
        'url': 'https://www.skf.com',
        'description': desc,
    }


def tailor_skills_fullstack(latex: str) -> str:
    import re
    items = "\n".join([
        r"\item \textbf{Cloud (Azure/OCI/AWS):} Azure App Services, Functions, SQL Database, Azure DevOps; OCI Compute/Object Storage; AWS EC2/S3/CloudFront",
        r"\item \textbf{Frontend:} React, Angular, TypeScript, responsive UI, accessibility",
        r"\item \textbf{Backend/Microservices:} Java, C\#, Python; RESTful APIs, domain-driven design",
        r"\item \textbf{CI/CD & DevOps:} Azure DevOps, GitHub Actions/Jenkins; Docker, Kubernetes; blue/green & canary; quality gates",
        r"\item \textbf{Testing/QA:} Unit, integration, e2e; build verification, contract testing; test pyramids",
        r"\item \textbf{Security/Compliance:} Identity, secrets, policy-as-code; collaboration with Cyber Security",
        r"\item \textbf{Networking:} Hybrid/multi-cloud connectivity, ingress, CDN, TLS, guardrails",
        r"\item \textbf{Automotive:} Android Auto, AOSP, in-vehicle UX; HW collaboration; performance tuning",
        r"\item \textbf{Leadership:} Mentorship, code review standards, architectural guidelines & sub-domain policies",
    ])
    latex = latex.replace('SKILLS_PLACEHOLDER', items)
    # Profile summary
    summary = (
        "Experienced full‑stack engineer (5+ years) for automotive and industrial software, delivering React/Angular frontends "
        "and Java/C#/Python microservices at global scale. Deep Azure (App Services, Functions, SQL DB, Azure DevOps) with practical OCI/AWS; "
        "strong CI/CD (Docker/Kubernetes), testing (unit/integration/e2e), and hybrid/multi‑cloud networking. Led Azure cost optimization via hybrid patterns, "
        "and collaborated with Cyber Security to meet regulatory requirements. Mentor/tech lead who sets guardrails and architectural guidelines for diverse teams."
    )
    latex = latex.replace('PROFILE_SUMMARY_PLACEHOLDER', summary)
    # Role title
    latex = latex.replace('ROLE_TITLE_PLACEHOLDER', 'Senior Fullstack Engineer')
    return latex


def replace_projects_fullstack(latex: str) -> str:
    import re
    projects = r"""
\section*{Hobby Projects}

\subsection{AndroidAuto\_Fullstack\_Suite}
\textit{2025} \\
\textbf{Android (AOSP), Kotlin/Java, React/TypeScript, Fastlane, GitHub Actions}
\begin{itemize}
\item Designed Android Auto features end\-to\-end with backend APIs and CI/CD; signed builds and release channels
\item Achieved 7 min 47 s AOSP 15 clean build on on\-prem server through HW collaboration and pipeline optimization
\item Implemented testing (unit, integration, e2e) and log\-based triage for stable releases
\end{itemize}

\subsection{Azure\_Cost\_Optimization\_Hybrid}
\textit{2024 -- Present} \\
\textbf{Azure App Services/Functions/SQL, Kubernetes, Terraform, SLOs}
\begin{itemize}
\item Reduced spend by moving latency/cost\-sensitive workloads to hybrid/on\-prem while keeping elastic services in Azure
\item Instrumented services (SLOs, dashboards) and enforced CI/CD quality gates to maintain reliability during transformations
\end{itemize}

\subsection{SmrtMart\_E\-commerce\_Platform}
\textit{2024 -- Present} \\
\textbf{React, TypeScript, Spring Boot/.NET, Azure DevOps, Docker/Kubernetes}
\begin{itemize}
\item Fullstack microservices with React frontends and backend services; domain boundaries and REST APIs
\item CI/CD in Azure DevOps with quality gates (build/test/scan), blue/green & canary; IaC for repeatable environments
\end{itemize}

\subsection{Content\_Automation\_Pipeline}
\textit{2024 -- Present} \\
\textbf{GitHub Actions, APIs, Static Site CI}
\begin{itemize}
\item Automated syncing of bluehawana.com posts with LinkedIn and GitHub repositories
\item Event-driven jobs with audit trails to ensure compliant publishing across markets
\end{itemize}

\subsection{Multi\-Cloud\_Platform}
\textit{2024 -- Present} \\
\textbf{Azure, OCI, AWS, Cloudflare}
\begin{itemize}
\item Built cross-cloud delivery using Azure App Services/Functions & OCI; AWS/CDN where beneficial
\item Policy guardrails and security collaboration for global/regulatory compatibility
\end{itemize}

\subsection{Weather\_Anywhere\_Infra}
\textit{2024 -- Present} \\
\textbf{SpringBoot, Alibaba Cloud ECS, ApsaraDB RDS (MySQL)}
\begin{itemize}
\item Operated city/weather data service with cost-aware scaling and observability
\end{itemize}
"""
    # Replace placeholder directly if present
    return latex.replace('PROJECTS_PLACEHOLDER', projects)


def generate_cv(job: dict):
    gen = OverleafPDFGenerator()
    base = gen._generate_latex_content(job)
    cv = tailor_skills_fullstack(base)
    cv = replace_projects_fullstack(cv)
    pdf_bytes = gen._compile_latex_locally(cv)
    ts = datetime.now().strftime('%Y%m%d')
    tex = f"SKF_Fullstack_Tailored_CV_{ts}.tex"
    pdf = f"SKF_Fullstack_Tailored_CV_{ts}.pdf"
    Path(tex).write_text(cv, encoding='utf-8')
    if pdf_bytes:
        Path(pdf).write_bytes(pdf_bytes)
    return tex, (pdf if pdf_bytes else '')


def build_cover_letter(job: dict) -> str:
    today = datetime.now().strftime('%Y.%m.%d')
    content = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{xcolor}\definecolor{darkblue}{rgb}{0.0,0.2,0.6}
\setlength{\parindent}{0pt}
\begin{document}\pagestyle{empty}
\begin{letter}{SKF Sweden AB\\von Utfallsgatan 2\\415 05 G\"{o}teborg}
\opening{Dear Hiring Manager,}

I am a full\-stack engineer with 5+ years building cloud applications across React/Angular frontends and Java/C\#/Python microservices backends. In the automotive domain, I work hands\-on with Android Auto and in\-vehicle experiences, while partnering across product, platform, and security to deliver compliant, high\-quality solutions.

My recent work centers on Azure and hybrid/multi\-cloud designs. I build with Azure App Services, Functions, Azure SQL and Azure DevOps, and I bring practical OCI and AWS experience for cross\-cloud interoperability. I set domain and sub\-domain policies, introduce CI/CD quality gates (build/test/scan), and collaborate with Cyber Security on identity, secrets, and policy\-as\-code so teams can move fast while meeting regulatory needs in multiple markets.

As a bridge between product, platform, and application teams in a multi\-national environment, I translate business outcomes into roadmaps and engineering constraints into business decisions. This reduces friction, improves alignment, and raises delivery quality. In Android Auto work, I deliver full\-stack features with reliable pipelines and testing (unit/integration/e2e) and use performance baselines to maintain a high bar.

I would be excited to bring this mix of full\-stack delivery, Azure/OCI pragmatism, and technical leadership to SKF in Gothenburg.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\%s}
\end{letter}\end{document}
""" % (today)
    return content


def compile_cl(latex: str, name: str) -> str:
    ed = SmartLaTeXEditor()
    return ed.compile_latex(latex, name)


def main():
    load_env()
    job = build_skf_job()
    print("🎯 Generating SKF full‑stack CV…")
    cv_tex, cv_pdf = generate_cv(job)
    print(f"CV: {cv_tex} | {cv_pdf}")

    print("💌 Generating SKF full‑stack Cover Letter…")
    cl_tex = f"SKF_Fullstack_Tailored_CL_{datetime.now().strftime('%Y%m%d')}.tex"
    cl_pdf_name = f"SKF_Fullstack_Tailored_CL_{datetime.now().strftime('%Y%m%d')}"
    cl_latex = build_cover_letter(job)
    Path(cl_tex).write_text(cl_latex, encoding='utf-8')
    cl_pdf = compile_cl(cl_latex, cl_pdf_name) or ''
    print(f"CL: {cl_tex} | {cl_pdf}")

    # Optional: email via existing sender pattern
    try:
        from send_opera_devops_email import try_send_with_files
        if cv_pdf and cl_pdf:
            subject = "SKF Senior Fullstack Engineer — Tailored CV & Cover Letter"
            body = (
                "Hi,\n\nAttached are the tailored SKF full‑stack documents (Azure/OCI focus).\n\nBest,\nJobHunter Automation"
            )
            sent = try_send_with_files(
                'leeharvad@gmail.com',
                'vsdclxhjnklrccsf',
                'hongzhili01@gmail.com',
                [
                    (cv_pdf, "SKF_Fullstack_CV_Hongzhi_Li.pdf"),
                    (cl_pdf, "SKF_Fullstack_Cover_Letter_Hongzhi_Li.pdf"),
                ],
                subject=subject,
                body=body,
            )
            print("📧 Email sent" if sent else "📧 Email not sent")
    except Exception as e:
        print(f"⚠️ Email step skipped: {e}")


if __name__ == '__main__':
    main()
