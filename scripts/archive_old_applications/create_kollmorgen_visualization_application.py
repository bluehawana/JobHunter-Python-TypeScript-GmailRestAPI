#!/usr/bin/env python3
"""
Create Kollmorgen Junior Software Engineer Application

Generates a fully tailored CV (LaTeX + PDF) and Cover Letter (LaTeX + PDF)
for Kollmorgen's Junior Software Engineer - Operation & Visualization role.
Focuses on REAL visualization, UI/UX, and real-time systems experience.
NO FAKE AGV PROJECTS - only actual work and hobby projects.
"""
from backend.smart_latex_editor import SmartLaTeXEditor
from backend.company_info_extractor import CompanyInfoExtractor
from backend.overleaf_pdf_generator import OverleafPDFGenerator
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure backend module path is available
sys.path.append('backend')

# Local imports from backend


def ensure_claude_env():
    """Ensure CompanyInfoExtractor can read Claude API key from env."""
    if not os.getenv("ANTHROPIC_AUTH_TOKEN") and os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_AUTH_TOKEN"] = os.getenv("ANTHROPIC_API_KEY")


def load_env_from_dotenv():
    """Lightweight loader for .env into process env."""
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


def build_kollmorgen_job() -> dict:
    """Build job dict for Kollmorgen Junior Software Engineer role."""
    description_lines = [
        # Key responsibilities
        "Develop and maintain visualization software for AGV operations and fleet management",
        "Create intuitive user interfaces for real-time monitoring and control systems",
        "Work with robotics and autonomous vehicle systems",
        "Implement data visualization and dashboard solutions",
        "Collaborate with cross-functional teams on operation software",
        "Participate in full software development lifecycle",
        # Requirements
        "Bachelor's degree in Computer Science or related field",
        "Experience with modern UI frameworks and visualization libraries",
        "Knowledge of real-time systems and data visualization",
        "Strong programming skills in modern languages",
        "Understanding of software architecture and design patterns",
        "Team player with good communication skills",
        "Interest in robotics, automation, and AGV systems",
    ]
    return {
        "title": "Junior Software Engineer - Operation & Visualization",
        "company": "Kollmorgen",
        "location": "Gothenburg, Sweden",
        "url": "https://career-agv.kollmorgen.com/jobs/5973951-junior-software-engineer-operation-visualization",
        "description": "\n".join(description_lines),
    }


def customize_visualization_skills(latex: str) -> str:
    """Replace skills with visualization and UI-focused expertise."""
    import re
    skills_re = re.compile(
        r"(\\section\*\{Core Technical Skills\}\s*\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\s*\\end\{itemize\})")
    custom_items = "\n".join([
        r"\item \textbf{UI/Visualization:} React, Next.js, Vue.js, Chart.js, real-time dashboards, responsive design",
        r"\item \textbf{Mobile/Native UI:} Android (Kotlin/Java), React Native, Xamarin, automotive UI/UX, Android Auto",
        r"\item \textbf{Backend/APIs:} Spring Boot, Node.js, RESTful APIs, WebSockets, real-time data streaming",
        r"\item \textbf{Programming:} Kotlin, Java, JavaScript/TypeScript, Python, C\#, Go, Bash",
        r"\item \textbf{Real-time Systems:} Event-driven architecture, pub/sub patterns, live data visualization",
        r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, SQLite, time-series data handling",
        r"\item \textbf{Cloud/DevOps:} AWS, Azure, Docker, Kubernetes, CI/CD, GitHub Actions, Grafana, Prometheus",
        r"\item \textbf{Data Visualization:} Grafana dashboards, Prometheus metrics, custom charts, geolocation mapping",
        r"\item \textbf{Automotive:} Android Auto, automotive infotainment, AOSP, in-vehicle testing, Polestar platforms",
        r"\item \textbf{Testing:} Unit testing, integration testing, UI testing, automated testing frameworks",
    ])

    def repl(m):
        return m.group(1) + custom_items + m.group(3)
    return skills_re.sub(repl, latex)


def add_visualization_experience(latex: str) -> str:
    """Augment ECARX experience to highlight REAL visualization and UI work."""
    import re
    ecarx_re = re.compile(
        r"(\\subsection\*\{ECARX \| Senior Infrastructure.*?\}[\s\S]*?\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\\end\{itemize\})")
    tailored_items = "\n".join([
        r"\item Designed and implemented real-time performance monitoring dashboards using Grafana and Prometheus for Android AOSP build systems",
        r"\item Created visualization tools for infrastructure metrics, achieving 3.5x performance improvement visibility through custom dashboards",
        r"\item Built web-based monitoring interfaces for automotive testing platforms including Polestar 4/5 emulator status visualization",
        r"\item Developed data visualization solutions for build time analytics, resource utilization, and system performance metrics",
        r"\item Collaborated with hardware engineers and testing teams to create intuitive UI for complex automotive validation workflows",
        r"\item Implemented real-time alerting and notification systems with visual feedback for infrastructure health monitoring",
        r"\item Designed user-friendly interfaces for managing hybrid cloud resources and on-premise HPC infrastructure",
        r"\item Created automated reporting dashboards for cross-functional teams to track Android development platform performance",
    ])

    def repl2(m):
        return m.group(1) + tailored_items + m.group(3)
    return ecarx_re.sub(repl2, latex)


def keep_real_projects_emphasize_visualization(latex: str) -> str:
    """Keep REAL projects but emphasize visualization and UI aspects - NO FAKE AGV PROJECTS."""
    import re
    # We'll keep the original projects but reorder and emphasize visualization aspects
    # No fake AGV dashboard or fake automotive monitoring suite
    return latex  # Keep original projects as they are real


def generate_cv(job: dict) -> dict:
    """Generate tailored CV LaTeX and PDF for Kollmorgen."""
    generator = OverleafPDFGenerator()
    base_latex = generator._generate_latex_content(job)

    # Customize for Kollmorgen visualization focus - using REAL experience only
    tailored_latex = customize_visualization_skills(base_latex)
    tailored_latex = add_visualization_experience(tailored_latex)
    # Keep real projects as-is, no fake AGV projects
    tailored_latex = keep_real_projects_emphasize_visualization(tailored_latex)

    # Compile PDF locally
    pdf_bytes = generator._compile_latex_locally(tailored_latex)

    # Save LaTeX and PDF
    ts = datetime.now().strftime("%Y%m%d")
    cv_tex = f"Kollmorgen_Visualization_Tailored_CV_{ts}.tex"
    cv_pdf = f"Kollmorgen_Visualization_Tailored_CV_{ts}.pdf"
    with open(cv_tex, 'w', encoding='utf-8') as f:
        f.write(tailored_latex)
    if pdf_bytes:
        with open(cv_pdf, 'wb') as f:
            f.write(pdf_bytes)

    # Upload LaTeX to R2 for Overleaf link (if configured)
    overleaf_url = ''
    try:
        from backend.r2_latex_storage import R2LaTeXStorage
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
    """Create Kollmorgen-specific cover letter focusing on REAL visualization and UI expertise."""
    company = company_info.get('company_name', job.get('company', 'Company'))
    address_block = company_info.get(
        'formatted_address', job.get('location', ''))
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

I am writing to express my strong interest in the Junior Software Engineer -- Operation \& Visualization position at %s. With hands\-on experience in visualization systems, real\-time monitoring dashboards, and automotive UI development, I am excited about the opportunity to contribute to your AGV operation software.

At ECARX, I have been deeply involved in creating visualization and monitoring solutions for complex automotive systems. I designed and implemented real\-time performance dashboards using Grafana and Prometheus for Android AOSP build infrastructure, providing intuitive visual feedback that enabled our team to achieve a 3.5x performance improvement. These dashboards process and visualize terabytes of build data daily, with our Android 15 AOSP clean build time reaching 7 minutes 47 seconds -- among the fastest publicly reported times.

Beyond infrastructure monitoring, I have extensive experience building user\-facing applications with modern frameworks. My hobby projects demonstrate this breadth: I developed Android Auto applications with automotive\-optimized UI/UX compliant with safety standards, created a cross\-platform carpooling mobile app with real\-time geolocation tracking and interactive maps using React Native, and built e\-commerce platforms with real\-time analytics dashboards. Each project required balancing technical complexity with user\-friendly design.

What excites me most about this role is applying my visualization skills to robotics and autonomous systems. Having worked with automotive testing platforms including Polestar 4/5 emulators, I understand the importance of reliable, intuitive interfaces for complex systems. I am eager to bring my real\-time data visualization experience, UI/UX skills, and passion for automation to help %s deliver world\-class AGV operation software.

I am a collaborative team player who thrives in cross\-functional environments, fluent in English and Mandarin with Swedish B2 proficiency. I would be thrilled to contribute to your team in Gothenburg.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\%s}
\end{letter}
\end{document}
""" % (company, address_block, greeting, company, company, today)
    return content


def generate_cover_letter(job: dict) -> dict:
    """Generate Kollmorgen cover letter LaTeX and PDF."""
    ensure_claude_env()
    extractor = CompanyInfoExtractor()
    info_res = extractor.extract_and_validate_company_info(job)
    company_info = info_res['company_info'] if info_res.get('success') else {
        'company_name': job.get('company', 'Company'),
        'formatted_address': job.get('location', ''),
        'greeting': 'Dear Hiring Manager',
    }

    cl_latex = build_cover_letter_latex(job, company_info)

    # Compile to PDF
    editor = SmartLaTeXEditor()
    ts = datetime.now().strftime("%Y%m%d")
    cl_name = f"Kollmorgen_Visualization_Tailored_CL_{ts}"
    cl_pdf_path = editor.compile_latex(cl_latex, cl_name)

    cl_tex = f"{cl_name}.tex"
    with open(cl_tex, 'w', encoding='utf-8') as f:
        f.write(cl_latex)

    # Optional: Upload CL LaTeX to R2 for Overleaf editing
    overleaf_url = ''
    try:
        from backend.r2_latex_storage import R2LaTeXStorage
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
    ok = editor.send_review_email(job.get('title', ''), job.get(
        'company', ''), cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus)
    return ok


def main():
    # Load .env first
    load_env_from_dotenv()
    ensure_claude_env()
    job = build_kollmorgen_job()
    print("🎨 Creating Kollmorgen Visualization application (REAL experience only)…")

    # CV
    print("\n📄 Generating tailored CV…")
    cv_res = generate_cv(job)
    print(json.dumps({k: v for k, v in cv_res.items()
          if k not in ['pdf_size', 'latex_size']}, indent=2))
    if cv_res['overleaf_url']:
        print(f"🔗 Overleaf (CV): {cv_res['overleaf_url']}")

    # Cover Letter
    print("\n💌 Generating tailored Cover Letter…")
    cl_res = generate_cover_letter(job)
    print(json.dumps(
        {k: v for k, v in cl_res.items() if k not in []}, indent=2))
    if cl_res['overleaf_url']:
        print(f"🔗 Overleaf (CL): {cl_res['overleaf_url']}")

    # Optional email
    sent = maybe_send_email(job, cv_res.get('pdf_file', ''), cl_res.get(
        'pdf_file', ''), cv_res.get('latex_file', ''), cl_res.get('latex_file', ''))
    if sent:
        print("📧 Email sent with PDFs + LaTeX sources")
    else:
        print("📧 Email not sent (missing SMTP config or opted out)")

    print("\n✅ Kollmorgen Visualization application ready (NO FAKE PROJECTS).")


if __name__ == "__main__":
    main()
