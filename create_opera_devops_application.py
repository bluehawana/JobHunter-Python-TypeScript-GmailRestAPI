#!/usr/bin/env python3
"""
Create Opera DevOps Application (LEGO + Claude + Overleaf)

Generates a fully tailored CV (LaTeX + PDF) and Cover Letter (LaTeX + PDF)
for Opera's DevOps Engineer role, using the repo's LEGO bricks logic and
Claude-powered company info extraction. Also supports Overleaf URL generation
via Cloudflare R2 and optional email delivery.
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure backend module path is available for relative imports inside backend modules
sys.path.append('backend')

# Local imports from backend
from backend.overleaf_pdf_generator import OverleafPDFGenerator
from backend.company_info_extractor import CompanyInfoExtractor
from backend.smart_latex_editor import SmartLaTeXEditor


def ensure_claude_env():
    """Ensure CompanyInfoExtractor can read Claude API key from env.
    CompanyInfoExtractor expects ANTHROPIC_AUTH_TOKEN; fall back to ANTHROPIC_API_KEY if needed.
    """
    if not os.getenv("ANTHROPIC_AUTH_TOKEN") and os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_AUTH_TOKEN"] = os.getenv("ANTHROPIC_API_KEY")


def load_env_from_dotenv():
    """Lightweight loader for .env into process env (no external deps)."""
    env_path = Path('.env')
    if not env_path.exists():
        return
    try:
        for raw in env_path.read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception:
        pass


def build_opera_job() -> dict:
    """Build job dict from Opera DevOps JD LEGO bricks."""
    description_lines = [
        # Responsibilities
        "Support the engineering team when it comes to tools, CI and CD",
        "Build monitoring and reporting for the project",
        "Set up the framework for incident management and recovery",
        "Cooperate with the development team to build the SDLC framework for the project",
        "Create a release plan with the management team and developers",
        "Maintain existing infrastructure and create new solutions",
        "Advocate DevOps best practices in the organization",
        # Requirements
        "BS or MS in Computer Science or equivalent degree",
        "At least 2 years recent enterprise DevOps experience",
        "Solid knowledge of AWS is a must",
        "Experience with deployment and delivery of web and server apps",
        "Ability to build infrastructure from scratch",
        "Familiar: Docker, Jenkins, Terraform",
        "Experience: load balancing, CDN, Linux admin",
        "Fluent in English",
        # Ideal
        "Monitoring: Grafana, Loki, Prometheus",
        "Close-to-expert Git; Python and shell scripting; high availability systems",
        "Currently in Gothenburg or willing to relocate",
    ]
    return {
        "title": "DevOps Engineer",
        "company": "Opera",
        "location": "Gothenburg, Sweden",
        "url": "https://jobs.opera.com/",
        "description": "\n".join(description_lines),
    }


def customize_devops_skills_block(latex: str) -> str:
    """Replace the default DevOps skills with AWS-first, Opera-aligned details."""
    # We replace the skills itemize content by locating the Core Technical Skills block.
    # This is tolerant: we only replace the list content between \section*{Core Technical Skills} and next \section* or \subsection*.
    import re
    skills_re = re.compile(r"(\\section\*\{Core Technical Skills\}\s*\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\s*\\end\{itemize\})")
    custom_items = "\n".join([
        r"\item \textbf{Cloud (AWS-first):} EC2, VPC, IAM, RDS, S3, CloudFront (CDN), Route53, ALB/NLB, CloudWatch",
        r"\item \textbf{IaC \& Config:} Terraform (modules, workspaces), CloudFormation, Ansible; GitOps",
        r"\item \textbf{Containers/Orchestration:} Docker, Kubernetes (AKS/EKS/on-prem), Helm, Kustomize",
        r"\item \textbf{CI/CD:} Jenkins (multibranch, shared libs), GitHub Actions, GitLab CI; blue/green, canary",
        r"\item \textbf{Monitoring/Logging:} Prometheus, Grafana, Loki, Alertmanager; SLOs, dashboards, alerting",
        r"\item \textbf{Networking/HA:} Nginx/HAProxy, load balancing, TLS, CDN, autoscaling, high availability",
        r"\item \textbf{Systems:} Linux admin (Ubuntu/CentOS), systemd, shell scripting, performance tuning",
        r"\item \textbf{Programming:} Python, Bash, PowerShell; internal tooling and automation",
        r"\item \textbf{Git Expertise:} Rebase/merge workflows, GitFlow/trunk-based, reviews, submodules",
    ])
    def repl(m):
        return m.group(1) + custom_items + m.group(3)
    return skills_re.sub(repl, latex)


def add_opera_specific_experience(latex: str) -> str:
    """Augment ECARX bullets to mirror Opera responsibilities explicitly."""
    import re
    ecarx_re = re.compile(r"(\\subsection\*\{ECARX \| IT/Infrastructure Specialist\}[\s\S]*?\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\\end\{itemize\})")
    tailored_items = "\n".join([
        r"\item Built and maintained CI/CD pipelines (Jenkins/GitHub Actions) for microservices; standardized templates and secrets",
        r"\item Implemented Prometheus, Grafana, and Loki with Alertmanager; SLO dashboards and weekly reliability reporting",
        r"\item Established incident management: on-call rotation, runbooks, recovery playbooks, and postmortems",
        r"\item Co-defined SDLC with dev teams: GitFlow/trunk-based, code review gates, semantic versioning",
        r"\item Led release planning with PM/engineering; automated release notes and change approvals",
        r"\item Provisioned infra from scratch via Terraform modules; migrated AKS to on-prem Kubernetes (cost reduction)",
        r"\item Administered Linux servers; configured Nginx/HAProxy, ALB, and CloudFront for load balancing/CDN",
        r"\item Advocated DevOps best practices across the org; trained engineers on Git and incident readiness",
    ])
    def repl2(m):
        return m.group(1) + tailored_items + m.group(3)
    return ecarx_re.sub(repl2, latex)


def replace_projects_with_devops(latex: str) -> str:
    """Replace the Hobby Projects section with DevOps-focused projects."""
    import re
    new_projects = r"""
\section*{Hobby Projects}

\subsection{ECARX\_Cost\_Optimization\_\&\_HPC\_Migration}
\textit{2024 -- Present} \\
\textbf{Terraform, Kubernetes, On-prem HPC, Prometheus/Grafana/Loki}
\begin{itemize}
\item Led Azure cost optimization by migrating AKS workloads to on-prem HPC Kubernetes cluster using Terraform modules
\item Achieved significant cost savings and up to 259\% CI throughput improvement vs Azure flagship VM in pipeline workloads
\item Implemented observability with Prometheus, Grafana, Loki, and Alertmanager; SLO dashboards and actionable alerting
\item Established incident framework (on-call, runbooks, recovery playbooks, postmortems) and SDLC guardrails
\end{itemize}

\subsection{Multi-Cloud\_DevOps\_Platform}
\textit{2024 -- Present} \\
\textbf{Cloudflare R2/WAF/CDN, AWS, Azure, GCP, Heroku}
\begin{itemize}
\item Built resilient delivery across Cloudflare, AWS, Azure, GCP, and Heroku for apps and internal tooling
\item Automated LaTeX/Overleaf integration via Cloudflare R2; artifact backups and shareable edit links
\item Implemented GitOps workflows, secrets management, and environment promotion with policy gates
\end{itemize}

\subsection{SmrtMart\_E-commerce\_CI/CD}
\textit{2024 -- Present} \\
\textbf{GitHub Actions/Jenkins, Terraform, Docker, Kubernetes}
\begin{itemize}
\item Implemented build/test/deploy pipelines with blue/green and canary strategies and infrastructure as code
\item Added end-to-end observability, performance baselines, and automated rollbacks on SLO violations
\end{itemize}

\subsection{Content\_Automation\_Pipeline}
\textit{2024 -- Present} \\
\textbf{GitHub Actions, APIs, Static Site CI}
\begin{itemize}
\item Automated syncing of bluehawana.com posts with LinkedIn and GitHub repositories for unified publishing
\item Event-driven jobs ensure changes propagate across platforms with audit trails and status reporting
\end{itemize}

\subsection{Android\_Auto\_CI\_\&\_Release}
\textit{2025} \\
\textbf{Gradle, GitHub Actions, Fastlane (signing)}
\begin{itemize}
\item Standardized Android Auto project pipelines; signed builds, release channels, and artifact retention
\item Integrated crash/log capture and log-based triage into release process
\end{itemize}

\subsection{Weather\_Anywhere\_Infra}
\textit{2024 -- Present} \\
\textbf{SpringBoot, Alibaba Cloud ECS, ApsaraDB RDS (MySQL), Heroku}
\begin{itemize}
\item Operated city/weather data service with Alibaba Cloud ECS and ApsaraDB, focusing on reliability and cost
\item Demo: https://weather.bluehawana.com
\end{itemize}
"""
    # Replace content between Hobby Projects and Education
    pattern = re.compile(r"(\\section\*\{Hobby Projects\})([\s\S]*?)(?=\\section\*\{Education\})")
    if pattern.search(latex):
        def repl(_m):
            return new_projects + "\n\\section*{Education}"
        return pattern.sub(repl, latex)
    return latex


def generate_cv(job: dict) -> dict:
    """Generate tailored CV LaTeX and PDF for Opera DevOps."""
    generator = OverleafPDFGenerator()
    base_latex = generator._generate_latex_content(job)

    # Customize for Opera requirements
    tailored_latex = customize_devops_skills_block(base_latex)
    tailored_latex = add_opera_specific_experience(tailored_latex)
    tailored_latex = replace_projects_with_devops(tailored_latex)

    # Compile PDF locally
    pdf_bytes = generator._compile_latex_locally(tailored_latex)

    # Save LaTeX and PDF
    ts = datetime.now().strftime("%Y%m%d")
    cv_tex = f"OPERA_DevOps_Tailored_CV_{ts}.tex"
    cv_pdf = f"OPERA_DevOps_Tailored_CV_{ts}.pdf"
    with open(cv_tex, 'w', encoding='utf-8') as f:
        f.write(tailored_latex)
    if pdf_bytes:
        with open(cv_pdf, 'wb') as f:
            f.write(pdf_bytes)

    # Upload LaTeX to R2 for Overleaf link (if configured)
    overleaf_url = ''
    try:
        from backend.r2_latex_storage import R2LaTeXStorage  # optional dependency (boto3)
        r2 = R2LaTeXStorage()
        r2res = r2.upload_latex_file(tailored_latex, job)
        if r2res:
            overleaf_url = r2res.get('overleaf_url', '')
    except Exception:
        pass

    return {
        'latex_file': cv_tex,
        'pdf_file': cv_pdf if pdf_bytes else '',
        'overleaf_url': overleaf_url,
        'pdf_size': len(pdf_bytes) if pdf_bytes else 0,
        'latex_size': len(tailored_latex),
    }


def build_cover_letter_latex(job: dict, company_info: dict) -> str:
    """Create Opera-specific cover letter focusing on cultural bridging and hybrid cloud."""
    company = company_info.get('company_name', job.get('company', 'Company'))
    # Force Opera HQ address as requested
    if company.lower() == 'opera':
        address_block = 'V\\"{a}stra Hamngatan 8\\\\411 17 G\\"{o}teborg'
    else:
        address_block = company_info.get('formatted_address', job.get('location', ''))
    greeting = company_info.get('greeting', 'Dear Hiring Manager')
    today = datetime.now().strftime('%Y.%m.%d')

    content = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}
\setlength{\parindent}{0pt}
\begin{document}
\pagestyle{empty}
\begin{letter}{%s\\%s}
\opening{%s,}

I am writing to express my interest in the DevOps Engineer role. Beyond tooling and pipelines, my strongest value is operating as a cultural and cross\-functional bridge in a multi\-national enterprise. Working daily across Swedish and Chinese teams, I translate business goals into engineering roadmaps and turn engineering constraints into business\-ready decisions. This reduces friction, shortens feedback loops, and raises delivery quality through clearer expectations and shared vocabulary.

At ECARX, this bridge role shaped how we combined public cloud with private infrastructure. With a deep understanding of Azure Kubernetes Service, I helped design a pragmatic hybrid approach: AKS where it makes sense for elasticity and managed services; on\-prem HPC Kubernetes where cost/performance is critical. We balanced reliability and spend by instrumenting everything (Prometheus/Grafana/Loki/Alertmanager) and letting SLOs guide capacity choices. Around the edges, we used Cloudflare (CDN/WAF/R2) and selectively leveraged Heroku, Azure, AWS, and GCP to meet specific business demands while keeping operational complexity in check.

One concrete impact: together with our hardware engineer, visualization specialist, and DevOps team, we recorded a 7 minutes 47 seconds Android AOSP 15 clean build on our on\-prem server. That result, achieved through careful CPU/memory/I/O tuning, build cache strategy, and targeted parallelization, is competitive among the fastest publicly reported times and demonstrates both engineering depth and cross\-team coordination.

I am a lifelong learner (currently preparing the CNCF CKAD exam) and I enjoy bringing people together—product, platform, and application teams—to make complex systems feel simple and dependable. I would be excited to bring this mix of cultural fluency, hybrid\-cloud pragmatism, and delivery focus to %s in Gothenburg.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\%s}
\end{letter}
\end{document}
""" % (company, address_block, greeting, company, today)
    return content


def generate_cover_letter(job: dict) -> dict:
    """Generate Opera cover letter LaTeX and PDF, using Claude-backed company info when possible."""
    ensure_claude_env()
    extractor = CompanyInfoExtractor()
    info_res = extractor.extract_and_validate_company_info(job)
    company_info = info_res['company_info'] if info_res.get('success') else {
        'company_name': job.get('company', 'Company'),
        'formatted_address': job.get('location', ''),
        'greeting': 'Dear Hiring Manager',
    }

    cl_latex = build_cover_letter_latex(job, company_info)

    # Compile to PDF via SmartLaTeXEditor (robust local pdflatex wrapper)
    editor = SmartLaTeXEditor()
    ts = datetime.now().strftime("%Y%m%d")
    cl_name = f"OPERA_DevOps_Tailored_CL_{ts}"
    cl_pdf_path = editor.compile_latex(cl_latex, cl_name)

    cl_tex = f"{cl_name}.tex"
    with open(cl_tex, 'w', encoding='utf-8') as f:
        f.write(cl_latex)

    # Optional: Upload CL LaTeX to R2 for Overleaf editing
    overleaf_url = ''
    try:
        from backend.r2_latex_storage import R2LaTeXStorage  # optional dependency
        r2 = R2LaTeXStorage()
        r2res = r2.upload_latex_file(cl_latex, job)
        if r2res:
            overleaf_url = r2res.get('overleaf_url', '')
    except Exception:
        pass

    return {
        'latex_file': cl_tex,
        'pdf_file': cl_pdf_path or '',
        'overleaf_url': overleaf_url,
        'company_info_quality': info_res.get('quality_score', 0) if info_res.get('success') else 0,
        'extraction_method': info_res.get('extraction_method', 'fallback') if info_res.get('success') else 'none',
    }


def maybe_send_email(job: dict, cv_pdf: str, cl_pdf: str, cv_tex: str, cl_tex: str):
    """Send review email with PDFs and LaTeX sources if SMTP configured."""
    if not os.getenv('SMTP_PASSWORD'):
        print("⚠️ SMTP_PASSWORD not configured; skipping email send.")
        return False
    editor = SmartLaTeXEditor()
    role_focus = editor.determine_role_focus(job.get('title', ''))
    ok = editor.send_review_email(job.get('title',''), job.get('company',''), cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus)
    return ok


def main():
    # Load .env first so Claude/R2/SMTP can be picked up without manual exports
    load_env_from_dotenv()
    ensure_claude_env()
    job = build_opera_job()
    print("🎭 Creating Opera DevOps application using LEGO + Claude…")

    # CV
    print("\n📄 Generating tailored CV…")
    cv_res = generate_cv(job)
    print(json.dumps({k: v for k, v in cv_res.items() if k not in ['pdf_size','latex_size']}, indent=2))
    if cv_res['overleaf_url']:
        print(f"🔗 Overleaf (CV): {cv_res['overleaf_url']}")

    # Cover Letter
    print("\n💌 Generating tailored Cover Letter…")
    cl_res = generate_cover_letter(job)
    print(json.dumps({k: v for k, v in cl_res.items() if k not in []}, indent=2))
    if cl_res['overleaf_url']:
        print(f"🔗 Overleaf (CL): {cl_res['overleaf_url']}")

    # Optional email
    sent = maybe_send_email(job, cv_res.get('pdf_file',''), cl_res.get('pdf_file',''), cv_res.get('latex_file',''), cl_res.get('latex_file',''))
    if sent:
        print("📧 Email sent with PDFs + LaTeX sources")
    else:
        print("📧 Email not sent (missing SMTP config or opted out)")

    print("\n✅ Opera DevOps application artifacts ready.")


if __name__ == "__main__":
    main()
