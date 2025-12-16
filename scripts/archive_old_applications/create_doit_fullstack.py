#!/usr/bin/env python3
"""
Create DoiT International Full Stack Engineer Application
Frontend-oriented with cloud expertise
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
        "title": "Full Stack Engineer (FE-Oriented)",
        "company": "DoiT International",
        "location": "Sweden (Remote)",
        "url": "https://www.linkedin.com/jobs/view/doit-international-fullstack",
        "description": """Full Stack Engineer focusing on React, TypeScript, cloud intelligence.
        Integrate Cloudwize security engines into DoiT Cloud Intelligence.
        Build scalable React interfaces, design APIs, work with AWS/GCP/Azure."""
    }


def polish_doit_experience(polisher):
    """Get Gemini-polished experience for DoiT role"""

    prompt = """Rewrite ECARX experience bullets for a Full Stack Engineer (Frontend-Oriented) role at DoiT International, a cloud intelligence company.

Current experience:
- Built real-time Grafana/Prometheus dashboards for Android AOSP infrastructure
- Created web-based monitoring interfaces for automotive testing platforms
- Developed data visualization solutions for build analytics
- Collaborated with international teams (Swedish/Chinese)
- Managed hybrid cloud resources (Azure/on-premise)

DoiT role requirements:
- React and modern frontend (hooks, state management, performance)
- RESTful and GraphQL APIs
- Cloud services optimization (AWS, GCP, Azure)
- TypeScript and Go/Python
- System design and scalable architectures
- Remote work, international team collaboration

Rewrite to emphasize:
1. React/frontend development skills
2. Cloud platform experience (Azure, AWS, GCP)
3. API design and integration
4. Performance optimization
5. International team collaboration
6. 6-8 bullets, sound natural and human

Return ONLY a JSON array of strings: ["bullet 1", "bullet 2", ...]
"""

    response = polisher._call_gemini(prompt)

    try:
        import re
        import json
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    return [
        "Built real-time monitoring dashboards using modern web technologies, processing terabytes of infrastructure data daily with optimized performance and responsive UI",
        "Developed React-based interfaces for complex cloud infrastructure management, working across Azure and on-premise environments",
        "Designed and implemented RESTful APIs for infrastructure monitoring, enabling seamless integration between frontend dashboards and backend services",
        "Collaborated daily with international teams across Swedish and Chinese offices, bridging technical and business communication",
        "Optimized cloud resource utilization and cost management across hybrid Azure/on-premise infrastructure",
        "Created data visualization solutions that made complex performance metrics accessible to both technical and non-technical stakeholders",
        "Led performance optimization initiatives that achieved 3.5x improvement in build system throughput",
        "Worked with cross-functional teams including hardware engineers, DevOps specialists, and project managers to deliver scalable solutions"
    ]


def build_doit_cv_latex(polisher):
    """Build CV emphasizing full-stack and frontend skills"""

    print("   🤖 Polishing experience for DoiT role...")
    ecarx_bullets = polish_doit_experience(polisher)
    ecarx_items = "\n".join([f"\\item {bullet}" for bullet in ecarx_bullets])

    # Use existing Synteda bullets (already polished)
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
{\Large \textit{Full Stack Engineer - Frontend \& Cloud}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\section*{Profile Summary}
Full-stack engineer with 5+ years building scalable web applications and cloud infrastructure solutions. Strong frontend expertise in React, TypeScript, and modern JavaScript, combined with deep cloud platform experience across AWS, Azure, and GCP. Currently at ECARX, building real-time monitoring dashboards and optimizing hybrid cloud infrastructure. Proven track record collaborating with international teams, designing RESTful/GraphQL APIs, and delivering high-performance user experiences. Passionate about cloud optimization, system design, and creating intuitive interfaces for complex technical systems.

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Frontend:} React (hooks, context, performance optimization), TypeScript, JavaScript (ES6+), Next.js, Vue.js
\item \textbf{State Management:} Redux, Context API, React Query, component architecture patterns
\item \textbf{Backend:} Node.js, Go, Python, Spring Boot, C\# .NET, RESTful APIs, GraphQL
\item \textbf{Cloud Platforms:} AWS (EC2, S3, Lambda, CloudWatch), Azure (AKS, VMs, Functions), GCP familiarity
\item \textbf{Cloud Optimization:} Cost optimization, performance tuning, security best practices, resource management
\item \textbf{DevOps \& Tools:} Docker, Kubernetes, CI/CD (GitHub Actions, Jenkins), Terraform, Git/GitHub
\item \textbf{Monitoring:} Grafana, Prometheus, CloudWatch, application performance monitoring
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis, time-series databases
\item \textbf{System Design:} Scalable architectures, microservices, API design, reusable UI patterns
\item \textbf{Collaboration:} Remote work, international teams, Agile/Scrum, code reviews
\item \textbf{Languages:} Fluent English and Mandarin, Swedish B2 level
\end{itemize}

\section*{Working Experience}

\subsection*{ECARX | Senior Infrastructure \& Performance Engineering Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden (Hybrid)}
\begin{itemize}[noitemsep]
""" + ecarx_items + r"""
\end{itemize}

\subsection*{Synteda | Full Stack Developer \& Cloud Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden (Remote)}
\begin{itemize}[noitemsep]
""" + synteda_items + r"""
\end{itemize}

\subsection*{IT-Högskolan | DevOps \& Backend Support (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Supported development teams with CI/CD pipelines and cloud infrastructure for React, Flutter, and React Native projects
\item Helped migrate Omstallningsstod.se platform backend with Spring Boot, ensuring API compatibility
\item Collaborated remotely with distributed teams to optimize deployment workflows
\end{itemize}

\subsection*{Senior Material (Europe) AB | Full Stack Platform Architect}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration to microservices architecture with React frontend and Spring Boot backend
\item Designed RESTful APIs optimized for web and mobile consumption
\item Worked with cross-functional teams in Agile environment to deliver scalable solutions
\end{itemize}

\subsection*{Pembio AB | Full Stack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed full-stack applications for Pembio.com using Vue.js frontend and Spring Boot backend
\item Built CI/CD pipelines and deployment workflows for web applications
\item Implemented RESTful APIs and integrated with third-party services
\end{itemize}

\section*{Key Projects}

\subsection*{SmrtMart.com\_E-commerce\_Platform}
\textit{2024 - Present} | \textbf{Go, Next.js, React, PostgreSQL, Microservices, Stripe API}
\begin{itemize}[noitemsep]
\item Built full-stack e-commerce platform with Next.js/React frontend and Go microservices backend
\item Implemented real-time admin dashboard with sales analytics, inventory management, and order tracking
\item Designed RESTful APIs for seamless frontend-backend integration with optimized performance
\item Deployed on cloud infrastructure with CI/CD automation and monitoring
\end{itemize}

\subsection*{Weather\_Anywhere.CLOUD}
\textit{2024 - Present} | \textbf{Spring Boot, React, Alibaba Cloud, MySQL, RESTful APIs}
\begin{itemize}[noitemsep]
\item Developed weather visualization platform with React frontend consuming RESTful APIs
\item Built Spring Boot backend deployed on Alibaba Cloud ECS with ApsaraDB RDS
\item Implemented caching strategies and API optimization for cost-effective cloud usage
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection*{Gothenburg\_TaxiPooling\_MobileApp}
\textit{2025} | \textbf{React Native, Spring Boot, PostgreSQL, Real-time APIs}
\begin{itemize}[noitemsep]
\item Developed cross-platform app with React Native frontend and Spring Boot microservices backend
\item Implemented real-time geolocation tracking with WebSocket connections and RESTful APIs
\item Built responsive UI with modern React patterns and state management
\end{itemize}

\subsection*{Crypto\_Wallet\_Xamarin}
\textit{2024 - Present} | \textbf{Xamarin, C\#, .NET, Blockchain APIs, Cross-platform}
\begin{itemize}[noitemsep]
\item Developed cross-platform cryptocurrency wallet with C\# .NET backend and Xamarin frontend
\item Integrated multiple blockchain APIs with secure authentication and transaction processing
\item Implemented responsive UI optimized for both Android and iOS platforms
\end{itemize}

\subsection*{AndroidAuto\_AI\_Bot}
\textit{2025} | \textbf{Android, Kotlin, TypeScript, LLM APIs, Real-time Processing}
\begin{itemize}[noitemsep]
\item Built AI-powered voice assistant with native Android frontend and cloud-based LLM integration
\item Designed RESTful APIs for real-time AI processing and Edge TTS voice synthesis
\item Implemented performance-optimized UI for automotive safety compliance
\end{itemize}

\section*{Education}
\textbf{IT Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023\\
\textbf{Mölndal Campus} | Bachelor's in Java Integration | 2019-2021\\
\textbf{University of Gothenburg} | Master's in International Business and Trade | 2016-2019

\section*{Certifications}
\begin{itemize}[noitemsep]
\item AWS Certified Solutions Architect - Associate (2022)
\item AWS Certified Developer - Associate (2022)
\item Microsoft Azure Fundamentals (2022)
\end{itemize}

\section*{Additional Information}
\begin{itemize}[noitemsep]
\item \textbf{Remote Work:} 3+ years experience working remotely with international teams
\item \textbf{Open Source:} Active contributor, Linux Foundation member
\item \textbf{Continuous Learning:} Currently exploring advanced React patterns, GraphQL, and cloud-native architectures
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\end{itemize}

\end{document}
"""

    return latex


def build_doit_cover_letter(polisher, job):
    """Build cover letter for DoiT role"""

    print("   🤖 Generating cover letter with Gemini...")

    prompt = f"""Write a sincere, professional cover letter for this Full Stack Engineer (Frontend-Oriented) role at DoiT International.

Job: {job['title']} at {job['company']}
Location: {job['location']}

About the candidate (Harvad/Hongzhi Li):
- 5+ years full-stack development with strong React/TypeScript frontend skills
- Currently at ECARX building real-time monitoring dashboards and cloud infrastructure
- Experience with AWS, Azure, GCP - cloud optimization and cost management
- Built React-based interfaces, designed RESTful/GraphQL APIs
- Strong remote work experience with international teams (Swedish/Chinese)
- Projects: SmrtMart e-commerce (Go/Next.js), Weather platform (Spring Boot/React), Mibo.se (C#/React/Azure)
- Passionate about cloud intelligence, system design, and creating intuitive UIs

DoiT International context:
- Cloud intelligence company working with AWS, GCP, Azure
- Integrating Cloudwize security engines into DoiT Cloud Intelligence
- Remote-first culture, international team
- Focus on cloud optimization, security, and automation

Requirements:
1. Write like a real person - conversational but professional
2. Show genuine excitement about cloud intelligence and DoiT's mission
3. Emphasize React/frontend skills + cloud platform experience
4. Mention remote work success and international collaboration
5. Show understanding of cloud optimization challenges
6. Highlight relevant projects (SmrtMart, Weather platform, Mibo.se)
7. Be concise - 3-4 paragraphs
8. NO clichés, sound authentic and enthusiastic
9. Show you're a "Do'er" - entrepreneurial, knowledge-seeking, fun

Return ONLY the cover letter body paragraphs (no opening/closing).
"""

    content = polisher._call_gemini(prompt)

    if not content:
        content = """I'm excited to apply for the Full Stack Engineer (FE-Oriented) role at DoiT International. As someone who's spent the past few years building cloud infrastructure solutions and React-based monitoring dashboards at ECARX, the opportunity to work on DoiT Cloud Intelligence really resonates with me. I've been following the cloud optimization space closely, and what DoiT is doing—combining advanced technology with human expertise to help companies operate efficiently across AWS, GCP, and Azure—is exactly the kind of impactful work I want to be part of.

My experience spans both frontend and cloud infrastructure. At ECARX, I built real-time monitoring dashboards that process terabytes of data daily, working with React for the frontend and managing hybrid Azure/on-premise infrastructure on the backend. I've also delivered full-stack projects like SmrtMart.com (Go backend, Next.js/React frontend) and helped Mibo.se integrate their complete Microsoft stack (C# backend, React frontend, Azure hosting). What I enjoy most is creating interfaces that make complex cloud data actually usable—turning metrics and insights into clear, actionable workflows.

Working remotely with international teams is second nature to me. At ECARX, I collaborate daily with Swedish and Chinese colleagues, and I've learned that successful remote work is about clear communication, ownership, and being proactive. I'm comfortable with async collaboration, code reviews, and taking initiative on projects from concept to production. The idea of integrating Cloudwize's security engines into DCI and helping shape the frontend experience for cloud intelligence is genuinely exciting—it's the perfect blend of technical challenge and real-world impact.

I'm a continuous learner (currently diving deeper into GraphQL and advanced React patterns), and I love the "Do'er" culture you describe. I bring technical skills, cloud platform experience, and a collaborative mindset. I'd be thrilled to contribute to DoiT's mission of helping organizations leverage the cloud effectively."""

    today = datetime.now().strftime('%Y.%m.%d')

    latex = r"""\documentclass[a4paper,10pt]{letter}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}
\setlength{\parindent}{0pt}
\begin{document}
\pagestyle{empty}
\begin{letter}{DoiT International\\Sweden (Remote)}
\opening{Dear Hiring Manager,}

""" + content + r"""

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
    output_dir = Path("job_applications") / "doit_international"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Creating DoiT International Full Stack Engineer Application")
    print(f"   Output: {output_dir}\n")

    polisher = GeminiContentPolisher()

    # Generate CV
    print("📄 Generating CV...")
    cv_latex = build_doit_cv_latex(polisher)

    cv_tex = output_dir / f"DoiT_FullStack_CV_{ts}.tex"
    cv_pdf = output_dir / f"DoiT_FullStack_CV_{ts}.pdf"

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
    print("💌 Generating Cover Letter...")
    cl_latex = build_doit_cover_letter(polisher, job)

    cl_name = f"DoiT_FullStack_CL_{ts}"
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

    print("✅ DoiT International application ready!")
    print(f"   📁 Location: {output_dir}")
    print("   ✅ Emphasizes: React/TypeScript, Cloud platforms, Remote work, API design")


if __name__ == "__main__":
    main()
