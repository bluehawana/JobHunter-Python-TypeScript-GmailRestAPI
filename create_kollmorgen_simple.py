#!/usr/bin/env python3
"""
Simple Kollmorgen Application Generator
No Claude API, no email - just generate CV and Cover Letter PDFs
"""
from backend.smart_latex_editor import SmartLaTeXEditor
from backend.overleaf_pdf_generator import OverleafPDFGenerator
import sys
from datetime import datetime
from pathlib import Path

sys.path.append('backend')


def build_kollmorgen_job() -> dict:
    """Build job dict for Kollmorgen."""
    return {
        "title": "Junior Software Engineer - Operation & Visualization",
        "company": "Kollmorgen",
        "location": "Gothenburg, Sweden",
        "url": "https://career-agv.kollmorgen.com/jobs/5973951",
        "description": "Visualization and operation software for AGV systems",
    }


def customize_cv_for_visualization(latex: str) -> str:
    """Customize CV to emphasize visualization skills."""
    import re

    # Update skills section
    skills_pattern = re.compile(
        r"(\\section\*\{Core Technical Skills\}\s*\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\s*\\end\{itemize\})"
    )

    new_skills = "\n".join([
        r"\item \textbf{UI/Visualization:} React, Next.js, Vue.js, Chart.js, real-time dashboards, responsive design",
        r"\item \textbf{Mobile/Native UI:} Android (Kotlin/Java), React Native, Xamarin, automotive UI/UX, Android Auto",
        r"\item \textbf{Backend/APIs:} Spring Boot, Node.js, RESTful APIs, WebSockets, real-time data streaming",
        r"\item \textbf{Programming:} Kotlin, Java, JavaScript/TypeScript, Python, C\#, Go, Bash",
        r"\item \textbf{Real-time Systems:} Event-driven architecture, pub/sub patterns, live data visualization",
        r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, SQLite, time-series data",
        r"\item \textbf{Cloud/DevOps:} AWS, Azure, Docker, Kubernetes, CI/CD, Grafana, Prometheus",
        r"\item \textbf{Data Visualization:} Grafana dashboards, Prometheus metrics, custom charts, geolocation",
        r"\item \textbf{Automotive:} Android Auto, AOSP, in-vehicle testing, Polestar platforms",
        r"\item \textbf{Testing:} Unit testing, integration testing, UI testing, automated frameworks",
    ])

    latex = skills_pattern.sub(lambda m: m.group(
        1) + new_skills + m.group(3), latex)

    # Update ECARX experience to highlight visualization
    ecarx_pattern = re.compile(
        r"(\\subsection\*\{ECARX \| Senior Infrastructure.*?\}[\s\S]*?\\begin\{itemize\}\[noitemsep\]\s*)([\s\S]*?)(\\end\{itemize\})"
    )

    new_ecarx = "\n".join([
        r"\item Designed real-time performance monitoring dashboards using Grafana and Prometheus for Android AOSP build systems",
        r"\item Created visualization tools for infrastructure metrics, achieving 3.5x performance improvement visibility",
        r"\item Built web-based monitoring interfaces for automotive testing platforms including Polestar 4/5 emulator visualization",
        r"\item Developed data visualization solutions for build time analytics, resource utilization, and performance metrics",
        r"\item Collaborated with hardware engineers and testing teams to create intuitive UI for automotive validation workflows",
        r"\item Implemented real-time alerting systems with visual feedback for infrastructure health monitoring",
        r"\item Designed user-friendly interfaces for managing hybrid cloud resources and on-premise HPC infrastructure",
        r"\item Created automated reporting dashboards for cross-functional teams to track development platform performance",
    ])

    latex = ecarx_pattern.sub(lambda m: m.group(
        1) + new_ecarx + m.group(3), latex)

    return latex


def build_cover_letter_latex() -> str:
    """Create Kollmorgen cover letter."""
    today = datetime.now().strftime('%Y.%m.%d')

    return r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}
\setlength{\parindent}{0pt}
\begin{document}
\pagestyle{empty}
\begin{letter}{Kollmorgen\\Gothenburg, Sweden}
\opening{Dear Hiring Manager,}

I am writing to express my strong interest in the Junior Software Engineer -- Operation \& Visualization position at Kollmorgen. With hands\-on experience in visualization systems, real\-time monitoring dashboards, and automotive UI development, I am excited about the opportunity to contribute to your AGV operation software.

At ECARX, I have been deeply involved in creating visualization and monitoring solutions for complex automotive systems. I designed and implemented real\-time performance dashboards using Grafana and Prometheus for Android AOSP build infrastructure, providing intuitive visual feedback that enabled our team to achieve a 3.5x performance improvement. These dashboards process and visualize terabytes of build data daily, with our Android 15 AOSP clean build time reaching 7 minutes 47 seconds -- among the fastest publicly reported times.

Beyond infrastructure monitoring, I have extensive experience building user\-facing applications with modern frameworks. My hobby projects demonstrate this breadth: I developed Android Auto applications with automotive\-optimized UI/UX compliant with safety standards, created a cross\-platform carpooling mobile app with real\-time geolocation tracking and interactive maps using React Native, and built e\-commerce platforms with real\-time analytics dashboards. Each project required balancing technical complexity with user\-friendly design.

What excites me most about this role is applying my visualization skills to robotics and autonomous systems. Having worked with automotive testing platforms including Polestar 4/5 emulators, I understand the importance of reliable, intuitive interfaces for complex systems. I am eager to bring my real\-time data visualization experience, UI/UX skills, and passion for automation to help Kollmorgen deliver world\-class AGV operation software.

I am a collaborative team player who thrives in cross\-functional environments, fluent in English and Mandarin with Swedish B2 proficiency. I would be thrilled to contribute to your team in Gothenburg.

\closing{Sincerely,}
\signature{Hongzhi Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\%s}
\end{letter}
\end{document}
""" % today


def main():
    job = build_kollmorgen_job()
    ts = datetime.now().strftime("%Y%m%d")

    # Create output folder structure
    output_dir = Path("job_applications") / "kollmorgen"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Creating Kollmorgen application (simplified)...")
    print(f"   Output: {output_dir}\n")

    # Generate CV
    print("📄 Generating CV...")
    generator = OverleafPDFGenerator()
    base_latex = generator._generate_latex_content(job)
    cv_latex = customize_cv_for_visualization(base_latex)
    cv_pdf_bytes = generator._compile_latex_locally(cv_latex)

    cv_tex = output_dir / f"Kollmorgen_CV_{ts}.tex"
    cv_pdf = output_dir / f"Kollmorgen_CV_{ts}.pdf"

    with open(cv_tex, 'w', encoding='utf-8') as f:
        f.write(cv_latex)

    if cv_pdf_bytes:
        with open(cv_pdf, 'wb') as f:
            f.write(cv_pdf_bytes)
        print(f"✅ CV generated: {cv_pdf}")
    else:
        print("❌ CV PDF generation failed")

    # Generate Cover Letter
    print("💌 Generating Cover Letter...")
    cl_latex = build_cover_letter_latex()
    editor = SmartLaTeXEditor()
    cl_name = f"Kollmorgen_CL_{ts}"

    # Temporarily change to output directory for compilation
    import os
    original_dir = os.getcwd()
    os.chdir(output_dir)
    cl_pdf_path = editor.compile_latex(cl_latex, cl_name)
    os.chdir(original_dir)

    cl_tex = output_dir / f"{cl_name}.tex"
    with open(cl_tex, 'w', encoding='utf-8') as f:
        f.write(cl_latex)

    if cl_pdf_path:
        print(f"✅ Cover Letter generated: {cl_pdf_path}")
    else:
        print("❌ Cover Letter PDF generation failed")

    print("\n✅ Done! Files saved to:")
    print(f"   📁 {output_dir}")
    print(f"   📄 CV: {cv_pdf.name}")
    print(f"   💌 Cover Letter: {cl_name}.pdf")


if __name__ == "__main__":
    main()
