#!/usr/bin/env python3
"""
Create Kollmorgen Application - Complete and Polished
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
        "title": "Junior Software Engineer - Operation & Visualization",
        "company": "Kollmorgen",
        "location": "Gothenburg, Sweden",
        "url": "https://career-agv.kollmorgen.com/jobs/5973951",
    }


def build_complete_cv_latex(polisher):
    """Build complete CV with all projects and experience"""

    print("   🤖 Polishing ECARX experience with Gemini...")
    ecarx_bullets = polisher.polish_ecarx_experience()
    ecarx_items = "\n".join([f"\\item {bullet}" for bullet in ecarx_bullets])

    print("   🤖 Polishing Synteda experience with Gemini...")
    synteda_bullets = polisher.polish_synteda_experience()
    synteda_items = "\n".join(
        [f"\\item {bullet}" for bullet in synteda_bullets])

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
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[10pt]
{\Large \textit{Software Engineer - Visualization \& UI/UX}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\section*{Profile Summary}
Software engineer with 5+ years building visualization systems and user interfaces for complex technical environments. Currently specializing in real-time monitoring dashboards and automotive UI at ECARX. Strong track record bridging technical and business teams, facilitating communication across international and Swedish colleagues. Experienced in full-stack development from mobile (Android/Xamarin) to cloud-native infrastructure. Passionate about cloud technologies, Linux, Raspberry Pi development, and AI integration. Proven ability to deliver complete solutions from business requirements to production deployment.

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Visualization \& UI:} Grafana, Prometheus, React, Next.js, Vue.js, Chart.js, real-time dashboards
\item \textbf{Mobile Development:} Android (Kotlin/Java), Android Auto, React Native, Xamarin (C\#), cross-platform
\item \textbf{Backend \& APIs:} Spring Boot, .NET/C\#, Node.js, RESTful APIs, WebSockets, microservices
\item \textbf{Cloud \& DevOps:} AWS, Azure, Docker, Kubernetes, CI/CD, cloud-native architecture
\item \textbf{Programming:} Kotlin, Java, C\#, JavaScript/TypeScript, Python, Go, Bash
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, SQLite, ApsaraDB RDS
\item \textbf{Systems:} Linux administration, Raspberry Pi development, embedded systems
\item \textbf{AI \& Innovation:} AI integration, LLM applications, Edge TTS, automation
\item \textbf{Soft Skills:} IT-business communication, international team collaboration, technical translation
\item \textbf{Languages:} Fluent English and Mandarin, Swedish B2 level
\end{itemize}

\section*{Working Experience}

\subsection*{ECARX | Senior Infrastructure \& Performance Engineering Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + ecarx_items + r"""
\end{itemize}

\subsection*{Synteda | Mobile App Developer \& Azure Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
""" + synteda_items + r"""
\end{itemize}

\subsection*{IT-Högskolan | Mobile DevOps Support (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Supported mobile development teams with DevOps infrastructure for Kotlin, Flutter, and React Native projects
\item Helped migrate Omstallningsstod.se platform backend, ensuring smooth mobile app integration
\item Collaborated with developers to optimize API connectivity and deployment pipelines for mobile applications
\end{itemize}

\subsection*{Senior Material (Europe) AB | Mobile Platform Architect}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration to microservices architecture optimized for mobile consumption
\item Designed RESTful APIs with Android SDK compatibility and efficient mobile data serialization
\item Worked with cross-functional teams to optimize applications for Android performance and battery efficiency
\end{itemize}

\subsection*{Pembio AB | Mobile App Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed native Android and iOS applications for Pembio.com platform using Java, Kotlin, and Swift
\item Built mobile deployment pipelines and app store distribution workflows for both platforms
\item Implemented mobile-specific features including push notifications, offline sync, and biometric authentication
\end{itemize}

\section*{Key Projects}

\subsection*{Crypto\_Wallet\_Xamarin}
\textit{2024 - Present} | \textbf{Xamarin, C\#, Blockchain APIs, Mobile Security}
\begin{itemize}[noitemsep]
\item Developed secure cross-platform cryptocurrency wallet application using Xamarin and C\# stack
\item Implemented advanced mobile security features including biometric authentication and secure key storage
\item Integrated multiple blockchain APIs for real-time cryptocurrency transaction processing
\item Built responsive UI components optimized for both Android and iOS platforms with .NET MAUI
\end{itemize}

\subsection*{AndroidAuto\_AI\_Bot}
\textit{2025} | \textbf{Android Auto, Kotlin, EdgeTTS, LLM, AI Integration}
\begin{itemize}[noitemsep]
\item Designed distraction-free voice-first UI for in-car AI assistant with LLM integration
\item Built native Android Auto interface with real-time AI processing and Edge TTS voice synthesis
\item Implemented custom wake-word detection and natural language understanding for automotive safety
\end{itemize}

\subsection*{Gothenburg\_TaxiPooling\_MobileApp}
\textit{2025} | \textbf{React Native, Spring Boot, PostgreSQL, Geolocation}
\begin{itemize}[noitemsep]
\item Developed cross-platform carpooling app with real-time geolocation visualization and route mapping
\item Implemented interactive UI for passenger matching, ride tracking, and real-time status updates
\item Built Spring Boot microservices backend with RESTful APIs for mobile consumption
\end{itemize}

\subsection*{SmrtMart.com\_E-commerce}
\textit{2024 - Present} | \textbf{Go, Next.js, PostgreSQL, Microservices}
\begin{itemize}[noitemsep]
\item Built comprehensive admin dashboard with real-time sales analytics and inventory visualization
\item Implemented interactive charts and graphs for business metrics using modern UI frameworks
\item Created responsive design with intuitive navigation and real-time order tracking
\end{itemize}

\subsection*{Weather\_Anywhere.CLOUD}
\textit{2024 - Present} | \textbf{Spring Boot, Alibaba Cloud ECS, ApsaraDB RDS (MySQL)}
\begin{itemize}[noitemsep]
\item Developed weather visualization platform with interactive UI for Swedish and global cities
\item Deployed on Alibaba Cloud infrastructure with optimized API usage and caching mechanisms
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection*{AndroidAuto\_CarTVPlayer\_KOTLIN}
\textit{2025} | \textbf{Kotlin, Android Auto SDK, ExoPlayer, Automotive APIs}
\begin{itemize}[noitemsep]
\item Designed native Android Auto media player with automotive-optimized UI controls
\item Implemented intuitive interface compliant with Android Auto design guidelines and safety standards
\item Integrated voice command processing using Android Speech Recognition
\end{itemize}

\subsection*{Raspberry\_Pi\_Home\_Automation}
\textit{2023 - Present} | \textbf{Python, Linux, IoT, Raspberry Pi}
\begin{itemize}[noitemsep]
\item Built home automation system using Raspberry Pi with sensor integration and remote monitoring
\item Developed Python-based control interfaces and real-time data visualization dashboards
\item Implemented cloud connectivity for remote access and mobile app integration
\end{itemize}

\section*{Education}
\textbf{IT Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023\\
\textbf{Mölndal Campus} | Bachelor's in Java Integration | 2019-2021\\
\textbf{University of Gothenburg} | Master's in International Business and Trade | 2016-2019

\section*{Certifications \& Continuous Learning}
\begin{itemize}[noitemsep]
\item AWS Certified Solutions Architect - Associate (2022)
\item AWS Certified Developer - Associate (2022)
\item Microsoft Azure Fundamentals (2022)
\item Active in cloud-native development community and Linux Foundation
\item Continuous learning: AI/ML integration, Kubernetes, advanced Raspberry Pi projects
\end{itemize}

\section*{Additional Information}
\begin{itemize}[noitemsep]
\item \textbf{Technical Interests:} Cloud-native architecture, Linux systems, Raspberry Pi development, AI integration
\item \textbf{Community:} Linux Foundation member, open source contributor, tech blog author
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\item \textbf{Driver's License:} Valid Swedish license for in-vehicle testing
\end{itemize}

\end{document}
"""

    return latex


def build_complete_cover_letter_latex(polisher, job):
    """Build complete cover letter with Gemini polishing"""

    print("   🤖 Polishing cover letter with Gemini...")

    # Get Gemini-polished content
    cl_content = polisher.polish_cover_letter_content(job)

    today = datetime.now().strftime('%Y.%m.%d')

    latex = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}
\setlength{\parindent}{0pt}
\begin{document}
\pagestyle{empty}
\begin{letter}{Kollmorgen\\Gothenburg, Sweden}
\opening{Dear Hiring Manager,}

""" + cl_content + r"""

\closing{Sincerely,\\
Harvad (Hongzhi) Li}
\signature{Harvad (Hongzhi) Li\\Ebbe Lieberathsgatan 27\\412 65 G\"{o}teborg\\hongzhili01@gmail.com\\0728384299\\""" + today + r"""}
\end{letter}
\end{document}
"""

    return latex


def main():
    load_env()
    job = build_job()
    ts = datetime.now().strftime("%Y%m%d")

    # Create output folder
    output_dir = Path("job_applications") / "kollmorgen"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Creating Complete Kollmorgen Application with Gemini AI")
    print(f"   Output: {output_dir}\n")

    # Initialize polisher
    polisher = GeminiContentPolisher()

    # Generate CV
    print("📄 Generating Complete CV...")
    cv_latex = build_complete_cv_latex(polisher)

    cv_tex = output_dir / f"Kollmorgen_Complete_CV_{ts}.tex"
    cv_pdf = output_dir / f"Kollmorgen_Complete_CV_{ts}.pdf"

    with open(cv_tex, 'w', encoding='utf-8') as f:
        f.write(cv_latex)

    # Compile CV
    generator = OverleafPDFGenerator()
    cv_pdf_bytes = generator._compile_latex_locally(cv_latex)

    if cv_pdf_bytes:
        with open(cv_pdf, 'wb') as f:
            f.write(cv_pdf_bytes)
        print(f"   ✅ CV: {cv_pdf.name}\n")

    # Generate Cover Letter
    print("💌 Generating Complete Cover Letter...")
    cl_latex = build_complete_cover_letter_latex(polisher, job)

    cl_name = f"Kollmorgen_Complete_CL_{ts}"
    cl_tex = output_dir / f"{cl_name}.tex"

    with open(cl_tex, 'w', encoding='utf-8') as f:
        f.write(cl_latex)

    # Compile Cover Letter
    editor = SmartLaTeXEditor()
    import os
    original_dir = os.getcwd()
    os.chdir(output_dir)
    cl_pdf_path = editor.compile_latex(cl_latex, cl_name)
    os.chdir(original_dir)

    if cl_pdf_path:
        print(f"   ✅ Cover Letter: {cl_name}.pdf\n")

    print("✅ Complete application ready!")
    print(f"   📁 Location: {output_dir}")
    print("   ✅ Includes: Mibo.se C# project, Ingress talent management, Xamarin crypto wallet")
    print("   ✅ Mentions: Cloud-native, Linux, Raspberry Pi, AI integration")


if __name__ == "__main__":
    main()
