#!/usr/bin/env python3
"""
Create Tata Cloud Developer Application

Tailors CV (LaTeX+PDF) and Cover Letter (LaTeX+PDF) to a Cloud Developer role
focused on .NET/C#, AWS, Kubernetes, MongoDB, Terraform, Grafana, Kafka,
IaC, cloud security, and event-driven architecture in the energy domain.
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
            s = raw.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            k, v = s.split('=', 1)
            k = k.strip(); v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def build_tata_job() -> dict:
    desc = "\n".join([
        ".NET/C# cloud development on AWS with Kubernetes/EKS",
        "IaC with Terraform; observability with Grafana; MongoDB for data",
        "Event-driven architecture with Kafka; secure distributed systems",
        "Energy systems domain; vehicle technology familiarity a plus",
        "DevOps practices, CI/CD, performance optimization",
        "Collaborative, diverse, fast-paced teams; analytical, structured, curious",
        "+4 years experience; Bachelor's degree or equivalent; B driver’s license optional",
    ])
    return {
        'title': 'Cloud Developer (.NET/AWS/Kubernetes)',
        'company': 'Tata',
        'location': 'Gothenburg, Sweden',
        'url': 'https://www.tatatechnologies.com',
        'description': desc,
    }


def tailor_tata_cv(latex: str) -> str:
    # Replace role title and summary
    summary = (
        "Cloud developer with 4+ years designing and integrating event-driven, secure distributed systems "
        "on AWS using .NET/C#, Kubernetes (EKS), Terraform (IaC), MongoDB, Grafana, and Kafka. Strong in DevOps, CI/CD, and "
        "performance optimization. Energy systems interest and familiarity with vehicle technology; sustainability-minded, analytical, and structured."
    )
    latex = latex.replace('ROLE_TITLE_PLACEHOLDER', 'Cloud Developer')
    latex = latex.replace('PROFILE_SUMMARY_PLACEHOLDER', summary)

    # Skills
    skills = "\n".join([
        r"\item \textbf{Languages/Frameworks:} .NET, C\#, Python, Java; ASP.NET/Core APIs",
        r"\item \textbf{Cloud (AWS):} EKS, EC2, S3, RDS, IAM, CloudFront, CloudWatch; basic Azure/GCP",
        r"\item \textbf{Datastores:} MongoDB, PostgreSQL/MySQL; schema design and performance",
        r"\item \textbf{Event-Driven:} Kafka (producers/consumers, topics, schemas), streaming pipelines",
        r"\item \textbf{IaC/Automation:} Terraform modules/workspaces; GitHub Actions/Jenkins; GitOps",
        r"\item \textbf{Containers/Orchestration:} Docker, Kubernetes (EKS/on-prem); Helm/Kustomize",
        r"\item \textbf{Observability/SRE:} Grafana/Prometheus/Alertmanager; SLOs, dashboards, alerting",
        r"\item \textbf{Security:} Secrets, identity, network policies; secure patterns in distributed systems",
        r"\item \textbf{Domain:} Energy systems, sustainability focus; vehicle technology familiarity",
    ])
    latex = latex.replace('SKILLS_PLACEHOLDER', skills)

    # Projects (replace placeholder block)
    projects = r"""
\section*{Hobby Projects}

\subsection{EnergyTelemetry\_Kafka\_Streaming}
\textit{2024 -- Present} \\
\textbf{.NET/C\#, Kafka, EKS, Terraform, Grafana, MongoDB}
\begin{itemize}
\item Built event-driven pipeline for simulated energy telemetry; Kafka topics with schema evolution and validation
\item Deployed on EKS with IaC (Terraform); dashboards/alerts in Grafana/Prometheus for SLO-based operations
\item Persisted aggregates to MongoDB; exposed .NET APIs for analytics and visualization
\end{itemize}

\subsection{GreenFleet\_Optimization\_Service}
\textit{2025} \\
\textbf{.NET APIs, AWS (Lambda/API Gateway/S3), Python, Terraform}
\begin{itemize}
\item Service calculating energy/cost impact for route and charging decisions; sustainability metrics
\item IaC for environments; CI/CD with tests and security scans; results surfaced via REST endpoints
\end{itemize}

\subsection{AndroidAuto\_Companion\_Backends}
\textit{2025} \\
\textbf{ASP.NET Core, Kafka, MongoDB, GitHub Actions}
\begin{itemize}
\item Companion backend for Android Auto features; event-driven updates, caching, and robust CI/CD
\item Contract tests and e2e flows to ensure safe rollout of client features
\end{itemize}
"""
    latex = latex.replace('PROJECTS_PLACEHOLDER', projects)
    # Normalize phone with country code for ATS
    latex = latex.replace('tel:0728384299', 'tel:+46728384299')
    latex = latex.replace('{0728384299}', '{+46 728 384 299}')
    return latex


def generate_cv(job: dict):
    gen = OverleafPDFGenerator()
    base = gen._generate_latex_content(job)
    cv = tailor_tata_cv(base)
    pdf_bytes = gen._compile_latex_locally(cv)
    ts = datetime.now().strftime('%Y%m%d')
    tex = f"Tata_Cloud_Tailored_CV_{ts}.tex"
    pdf = f"Tata_Cloud_Tailored_CV_{ts}.pdf"
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
\begin{letter}{Tata Technologies\\Gustaf Larsons v 15\\418 78 G\"{o}teborg}
\opening{Dear Hiring Manager,}

I am a cloud developer with 4+ years building event\-driven, secure distributed systems on AWS using .NET/C\#, Kubernetes (EKS), Terraform, MongoDB, Grafana, and Kafka. I integrate complex systems with a DevOps mindset—automation first, IaC everywhere, observable by default—and I focus on performance and reliability in production.

I enjoy the energy/sustainability domain. My recent projects include a Kafka\-based energy telemetry pipeline on EKS (IaC with Terraform, Grafana/Prometheus SLOs), a green fleet optimization service (.NET APIs on AWS with CI/CD and security scans), and Android Auto companion backends using event\-driven patterns and contract tests. I collaborate closely with security and platform teams on secrets, identity, and network policy to keep distributed systems safe and compliant.

I hold a valid B driver's license and have participated in vehicle testing and verification activities in Gothenburg, including programs for Polestar 5, EX30, and Hongqi. This hands\-on exposure to on\-road validation and test workflows informs how I design telemetry, observability, and safety\-critical integrations across cloud backends and in\-vehicle clients.

What motivates me is continuous improvement: tuning services for lower latency and better resource efficiency, strengthening pipelines with tests and policy gates, and using analytics to guide cost/performance trade\-offs. I communicate clearly, mentor others, and thrive in diverse teams that move fast while staying organized and structured.

I would be excited to bring this blend of .NET/AWS engineering, Kubernetes/IaC automation, and event\-driven design to Tata. Thank you for your time and consideration.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\+46 728 384 299\\%s}
\end{letter}\end{document}
""" % (today)
    return content


def compile_cl(latex: str, name: str) -> str:
    ed = SmartLaTeXEditor()
    return ed.compile_latex(latex, name)


def main():
    load_env()
    job = build_tata_job()
    print("🚀 Generating Tata Cloud CV…")
    cv_tex, cv_pdf = generate_cv(job)
    print(f"CV: {cv_tex} | {cv_pdf}")

    print("💌 Generating Tata Cloud Cover Letter…")
    cl_tex = f"Tata_Cloud_Tailored_CL_{datetime.now().strftime('%Y%m%d')}.tex"
    cl_name = f"Tata_Cloud_Tailored_CL_{datetime.now().strftime('%Y%m%d')}"
    cl_latex = build_cover_letter(job)
    Path(cl_tex).write_text(cl_latex, encoding='utf-8')
    cl_pdf = compile_cl(cl_latex, cl_name) or ''
    print(f"CL: {cl_tex} | {cl_pdf}")

    # Email
    try:
        from send_opera_devops_email import try_send_with_files
        if cv_pdf and cl_pdf:
            subject = "Tata Cloud Developer — Tailored CV & Cover Letter"
            body = (
                "Hi,\n\nAttached are the tailored Tata Cloud Developer documents (.NET/AWS/Kubernetes).\n\nBest,\nJobHunter Automation"
            )
            sent = try_send_with_files(
                'leeharvad@gmail.com',
                'vsdclxhjnklrccsf',
                'hongzhili01@gmail.com',
                [
                    (cv_pdf, "Tata_Cloud_CV_Hongzhi_Li.pdf"),
                    (cl_pdf, "Tata_Cloud_Cover_Letter_Hongzhi_Li.pdf"),
                ],
                subject=subject,
                body=body,
            )
            print("📧 Email sent" if sent else "📧 Email not sent")
    except Exception as e:
        print(f"⚠️ Email step skipped: {e}")


if __name__ == '__main__':
    main()
