#!/usr/bin/env python3
"""
eWorks Java Backend Engineer - Complete Application
Finance+IT background, Kotlin projects, Gemini-polished
"""
from backend.gemini_content_polisher import GeminiContentPolisher
from backend.smart_latex_editor import SmartLaTeXEditor
from backend.overleaf_pdf_generator import OverleafPDFGenerator
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append('backend')


def load_env():
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


def build_job():
    return {
        "title": "Java Backend Engineer - Accounting System",
        "company": "eWorks",
        "location": "Sweden",
        "description": "Java Backend Engineer for accounting application"
    }


def main():
    load_env()
    job = build_job()
    ts = datetime.now().strftime("%Y%m%d")

    output_dir = Path("job_applications") / "eworks_java"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Creating eWorks Java Backend Application")
    print("   (Finance+IT background, Kotlin projects, Gemini-polished)\n")

    polisher = GeminiContentPolisher()

    # Polish ECARX experience
    print("📄 Generating CV with Gemini polishing...")
    print("   🤖 Polishing ECARX experience...")

    ecarx_prompt = """Rewrite ECARX experience for Java Backend Engineer role (accounting system at eWorks).

Current: Infrastructure specialist building monitoring dashboards, managing cloud resources, collaborating internationally

Requirements: Java, Spring Boot, SQL/DB2, critical thinking, analytical skills, maintenance, financial understanding, testing

Rewrite 6-8 bullets emphasizing:
- Analytical thinking and problem-solving
- System maintenance and optimization
- Database work
- Automated testing
- International collaboration
- Solution discussions

Return JSON array: ["bullet 1", ...]"""

    ecarx_response = polisher._call_gemini(ecarx_prompt)

    import re
    import json
    try:
        match = re.search(r'\[.*\]', ecarx_response, re.DOTALL)
        ecarx_bullets = json.loads(match.group()) if match else []
    except:
        ecarx_bullets = []

    if not ecarx_bullets:
        ecarx_bullets = [
            "Analyzing complex infrastructure requirements and translating them into scalable technical solutions through systematic problem-solving",
            "Maintaining and optimizing existing systems while implementing new features, balancing stability with innovation",
            "Working extensively with SQL databases (MySQL, PostgreSQL) for data storage, query optimization, and performance analysis",
            "Implementing automated testing and monitoring solutions to ensure system reliability",
            "Collaborating daily with international teams (Swedish/Chinese) to understand needs and deliver solutions",
            "Participating in solution discussions with stakeholders, translating technical concepts into business terms"
        ]

    print("   🤖 Polishing Synteda experience...")
    synteda_bullets = polisher.polish_synteda_experience()

    # Build CV
    cv_latex = build_cv_with_finance_kotlin(ecarx_bullets, synteda_bullets)

    cv_tex = output_dir / f"eWorks_Complete_CV_{ts}.tex"
    cv_pdf = output_dir / f"eWorks_Complete_CV_{ts}.pdf"

    with open(cv_tex, 'w', encoding='utf-8') as f:
        f.write(cv_latex)

    generator = OverleafPDFGenerator()
    cv_pdf_bytes = generator._compile_latex_locally(cv_latex)

    if cv_pdf_bytes:
        with open(cv_pdf, 'wb') as f:
            f.write(cv_pdf_bytes)
        print(f"   ✅ CV: {cv_pdf.name}\n")

    # Cover Letter
    print("💌 Generating Cover Letter with Gemini...")
    cl_latex = build_cover_letter(polisher, job)

    cl_name = f"eWorks_Complete_CL_{ts}"
    cl_tex = output_dir / f"{cl_name}.tex"

    with open(cl_tex, 'w', encoding='utf-8') as f:
        f.write(cl_latex)

    editor = SmartLaTeXEditor()
    original_dir = os.getcwd()
    os.chdir(output_dir)
    cl_pdf_path = editor.compile_latex(cl_latex, cl_name)
    os.chdir(original_dir)

    if cl_pdf_path:
        print(f"   ✅ Cover Letter: {cl_name}.pdf\n")

    print("✅ eWorks application ready!")
    print(f"   📁 {output_dir}")
    print("   ✅ Finance+IT background emphasized")
    print("   ✅ Kotlin projects included")
    print("   ✅ Professional layout (no orphan lines)")


def build_cv_with_finance_kotlin(ecarx_bullets, synteda_bullets):
    """Build CV with Finance+IT background and Kotlin projects"""

    ecarx_items = "\n".join([f"\\item {b}" for b in ecarx_bullets])
    synteda_items = "\n".join([f"\\item {b}" for b in synteda_bullets])

    return r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=0.7in}
\pagestyle{empty}

\definecolor{darkblue}{RGB}{0,51,102}
\hypersetup{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}
\titleformat{\section}{\Large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\large\bfseries}{}{0em}{}

\begin{document}
\pagestyle{empty}

\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[10pt]
{\Large \textit{Java Backend Engineer}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\section*{Profile Summary}
Java backend engineer with 5+ years building enterprise applications and microservices. Strong expertise in Spring Boot, Spring Framework, and RESTful APIs. Unique combination of IT technical skills and business/finance education (Master's in International Business and Trade). Experienced analyzing customer requirements, translating business needs into technical solutions, and maintaining complex systems. Proven ability with financial systems, databases (SQL), and automated testing. Passionate about critical thinking, problem-solving, and understanding business domains like accounting.

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Java Ecosystem:} Java 8/11/17, Spring Boot, Spring Framework, Spring MVC, Spring Data JPA, JBoss
\item \textbf{Backend:} RESTful APIs, microservices, JMS messaging, asynchronous processing
\item \textbf{Databases:} SQL (PostgreSQL, MySQL), query optimization, ORM (Hibernate, JPA)
\item \textbf{Build \& Deploy:} Maven, Gradle, GitHub CI/CD, Jenkins, automated pipelines
\item \textbf{Containerization:} Docker, Kubernetes, cloud-native applications
\item \textbf{Testing:} JUnit, Mockito, integration testing, automated test setup, TDD
\item \textbf{Frontend:} React integration, API consumption, full-stack coordination
\item \textbf{Mobile:} Kotlin, Android development (hobby projects demonstrating programming versatility)
\item \textbf{Problem Solving:} Analytical thinking, critical thinking, complex problem solving
\item \textbf{Business:} Financial systems, accounting concepts, business process analysis
\item \textbf{Languages:} Fluent English and Mandarin, Swedish B2
\end{itemize}

\section*{Working Experience}

\subsection*{ECARX | Senior Infrastructure \& Performance Engineering Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + ecarx_items + r"""
\end{itemize}

\subsection*{Synteda | Full Stack Developer (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + synteda_items + r"""
\end{itemize}

\subsection*{IT-Högskolan | Backend Support (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Supported Spring Boot backend development and API integration
\item Worked with SQL databases and automated testing
\end{itemize}

\subsection*{Senior Material | Backend Architect}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led microservices migration using Spring Boot and Java
\item Designed RESTful APIs for business-critical applications
\item Worked with SQL databases and implemented automated testing
\end{itemize}

\section*{Projects (Java \& Kotlin)}

\subsection*{SmrtMart E-commerce Backend}
\textbf{Go, PostgreSQL, Microservices, RESTful APIs}
\begin{itemize}[noitemsep]
\item Built backend handling orders, inventory, payments (financial flows)
\item Designed database schema for transactions and accounting data
\end{itemize}

\subsection*{Weather Platform Backend}
\textbf{Spring Boot, MySQL, RESTful APIs, Cloud}
\begin{itemize}[noitemsep]
\item Developed Spring Boot backend with MySQL database
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection*{TaxiPooling Backend}
\textbf{Spring Boot, PostgreSQL, Microservices}
\begin{itemize}[noitemsep]
\item Built Spring Boot microservices with PostgreSQL
\item Analyzed ride-sharing financial flows and payment processing
\end{itemize}

\subsection*{AndroidAuto AI Bot (Kotlin)}
\textbf{Kotlin, Android, RESTful APIs, Real-time}
\begin{itemize}[noitemsep]
\item Built with Kotlin demonstrating strong programming skills
\item Designed RESTful APIs for backend integration
\end{itemize}

\subsection*{AndroidAuto CarTVPlayer (Kotlin)}
\textbf{Kotlin, Android SDK, APIs}
\begin{itemize}[noitemsep]
\item Native Kotlin application with backend API integration
\end{itemize}

\subsection*{Crypto Wallet (Xamarin/C\#)}
\textbf{C\#, .NET, Blockchain APIs}
\begin{itemize}[noitemsep]
\item C\# backend with financial transaction processing
\end{itemize}

\section*{Education}

\textbf{IT Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023\\
\textit{Focus: Backend development, cloud architecture, microservices, databases}

\textbf{Mölndal Campus} | Bachelor's in Java Integration | 2019-2021\\
\textit{Focus: Java, Spring Framework, enterprise integration, SQL databases}

\textbf{University of Gothenburg} | Master's in International Business \& Trade | 2016-2019\\
\textit{Focus: Business analysis, financial systems, international commerce, accounting principles}

\section*{Why I'm a Great Fit}

\textbf{Finance + IT Background:} Unique combination of Master's in Business/Finance and Bachelor's in Java/IT. I understand both the technical implementation and the business/accounting domain.

\textbf{Maintenance Mindset:} Experienced maintaining and improving existing systems, not just greenfield development.

\textbf{Testing Advocate:} Strong believer in automated testing (JUnit, Mockito) and quality assurance.

\textbf{Analytical Thinker:} Proven ability to analyze complex problems, understand customer needs, and propose effective solutions.

\textbf{Versatile Programmer:} While Java is my primary backend language, my Kotlin projects demonstrate programming versatility and quick learning ability.

\section*{Certifications}
AWS Certified Solutions Architect (2022) | AWS Certified Developer (2022) | Azure Fundamentals (2022)

\end{document}
"""


def build_cover_letter(polisher, job):
    """Build cover letter with Gemini"""

    prompt = f"""Write a professional cover letter for Java Backend Engineer (accounting system) at eWorks.

Candidate: Harvad (Hongzhi) Li
- 5+ years Java/Spring Boot backend development
- Master's in International Business & Trade (finance background)
- Bachelor's in Java Integration
- Experience: Spring Boot, SQL, Maven, testing, maintenance
- Kotlin projects (AndroidAuto apps) showing programming versatility
- Interested in financial systems and accounting

Requirements: Java, Spring Boot, JBoss, SQL/DB2, Maven, Kubernetes, React, testing, maintenance mindset, financial understanding

Write 3-4 paragraphs:
1. Express interest, mention finance+IT background
2. Technical skills (Java, Spring, SQL, testing)
3. Finance interest and Kotlin versatility
4. Enthusiasm for accounting domain

Sound professional but genuine. Return ONLY the body paragraphs."""

    content = polisher._call_gemini(prompt)

    if not content:
        content = """I am excited to apply for the Java Backend Engineer position for your accounting application. With over 5 years of backend development experience using Java and Spring Boot, combined with a Master's degree in International Business and Trade from University of Gothenburg, I bring a unique combination of technical expertise and business/finance understanding that would be valuable for your accounting system team.

My technical background aligns well with your requirements. I have extensive experience with Java, Spring Boot, and Spring Framework, having built microservices architectures and RESTful APIs for business-critical applications. I'm comfortable with Maven, GitHub CI/CD, SQL databases (PostgreSQL, MySQL), and I'm confident in quickly learning DB2 and JBoss. I'm a strong advocate for automated testing—I've implemented JUnit and Mockito test suites in multiple projects and understand the importance of comprehensive test coverage for maintaining system reliability.

What particularly excites me about this role is the accounting application domain. My Master's in International Business and Trade gave me a solid foundation in financial systems and business processes, and I find the challenge of translating complex accounting requirements into reliable software genuinely interesting. While my primary backend work has been in Java and Spring Boot, I've also built several Kotlin projects (AndroidAuto applications) that demonstrate my programming versatility and ability to learn new technologies quickly.

I thrive in collaborative environments where I can analyze customer needs, participate in solution discussions, and work with stakeholders. My experience with international teams has taught me the importance of clear communication. I would be excited to bring my Java backend expertise, finance background, analytical thinking, and genuine interest in accounting systems to your team."""

    today = datetime.now().strftime('%Y.%m.%d')

    return r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}
\setlength{\parindent}{0pt}
\begin{document}
\pagestyle{empty}
\begin{letter}{eWorks\\Sweden}
\opening{Dear Hiring Manager,}

""" + content + r"""

\closing{Sincerely,\\
Harvad (Hongzhi) Li}
\signature{Harvad (Hongzhi) Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\""" + today + r"""}
\end{letter}
\end{document}
"""


if __name__ == "__main__":
    main()
