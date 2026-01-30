#!/usr/bin/env python3
"""
Generate Android Developer CV and Cover Letter - Updated Version
Focuses on AOSP, Software Factory DevOps, .NET Xamarin, and accurate work history
"""

import sys
from pathlib import Path
import subprocess
from datetime import datetime

def generate_android_cv():
    """Generate Android Developer CV with AOSP/DevOps focus"""
    
    latex_cv = r"""\documentclass[11pt,a4paper]{article}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}

\geometry{left=2cm,right=2cm,top=2cm,bottom=2cm}
\setlength{\parindent}{0pt}
\pagestyle{empty}

\definecolor{titlecolor}{RGB}{0,102,204}
\definecolor{linkcolor}{RGB}{0,102,204}

\titleformat{\section}{\Large\bfseries\color{titlecolor}}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{12pt}{6pt}

\titleformat{\subsection}{\large\bfseries}{}{0em}{}
\titlespacing*{\subsection}{0pt}{8pt}{4pt}

\hypersetup{
    colorlinks=true,
    linkcolor=linkcolor,
    urlcolor=linkcolor,
    citecolor=linkcolor
}

\begin{document}

\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[10pt]
{\Large \textit{Senior Android Developer}}\\[10pt]
\textcolor{titlecolor}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:+46728384299}{+46 72 838 4299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\vspace{8pt}

\section*{Professional Summary}
Senior Android Developer with 6+ years of software development experience (2019-Present) specializing in native Android (Kotlin/Java), AOSP customization, and cross-platform mobile development (.NET Xamarin, React Native). Proven expertise building automotive infotainment systems with hands-on AOSP 15, QNS integration, and Software Factory DevOps workflows. Strong background in system-level Android development, CI/CD automation, and bridging technical-business requirements. Unique trilingual capability (Chinese, English, Swedish) facilitating international team collaboration. All projects rigorously tested on physical devices including Polestar 4 emulator and Google Firebase Test Lab.

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Native Android:} Kotlin, Java, Android SDK, Android Studio, MVVM/MVP/Clean Architecture
\item \textbf{AOSP \& System-Level:} AOSP 15 customization, QNS (Qualified Networks Service), System Services, HAL integration
\item \textbf{Android Framework:} Activities, Services, Content Providers, Broadcast Receivers, Binder IPC
\item \textbf{Cross-Platform:} .NET Xamarin (Graduate Project), React Native, Expo, Hybrid apps
\item \textbf{Automotive:} Android Auto, Android Automotive OS, in-car infotainment systems, Polestar 4 testing
\item \textbf{DevOps \& Software Factory:} CI/CD pipelines, Jenkins, GitLab CI, GitHub Actions, Docker, Kubernetes
\item \textbf{Backend Integration:} RESTful APIs, Spring Boot, .NET Core, PostgreSQL, MongoDB, Redis
\item \textbf{Cloud Platforms:} AWS, Azure, GCP - Cloud-native mobile backend architecture
\item \textbf{Testing:} JUnit, Espresso, Firebase Test Lab, Physical device testing, Automated UI testing
\item \textbf{AI Integration:} LLM APIs (GPT-4, Claude), Voice processing (TTS, STT, wake-word detection)
\item \textbf{Languages:} Chinese (Native), English (Fluent), Swedish (B2) - Trilingual technical communication
\end{itemize}

\section*{Professional Experience}

\subsection*{ECARX (Geely Automotive) | IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}

\textbf{Android Automotive \& Software Factory DevOps:}
\begin{itemize}[noitemsep]
\item Worked extensively with AOSP 15 customization and QNS (Qualified Networks Service) integration for automotive systems
\item Participated in Software Factory DevOps workflows: CI/CD pipeline automation, build systems, release management
\item Tested Android Automotive applications on Polestar 4 physical emulator ensuring production-grade quality
\item Collaborated with international teams across 4 global offices (China, Sweden, UK, Germany)
\item Bridged technical communication between Chinese headquarters and Swedish development team
\item Implemented monitoring solutions (Prometheus/Grafana) and automation scripts for system reliability
\item Managed hybrid cloud infrastructure (AWS, Azure, AKS) supporting Android development and testing pipelines
\item Hands-on experience with automotive-specific Android components and system-level integration
\end{itemize}

\subsection*{Synteda AB | .NET Azure Developer (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}

\textbf{Mobile \& Cloud Development:}
\begin{itemize}[noitemsep]
\item Developed cross-platform mobile applications using .NET Xamarin and React Native (iOS/Android)
\item Built backend APIs using .NET Core and Azure cloud services (App Services, Functions, Cosmos DB)
\item Integrated mobile apps with Azure services and implemented real-time features using SignalR
\item Deployed applications on Azure with CI/CD automation (Azure DevOps, GitHub Actions)
\item Implemented push notifications and offline-first mobile architecture patterns
\end{itemize}

\subsection*{IT-Högskolan | .NET Cloud Developer (LIA 2 Internship)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}

\textbf{Graduate Project - .NET Xamarin Mobile App:}
\begin{itemize}[noitemsep]
\item Developed cross-platform mobile application using .NET Xamarin.Forms (iOS/Android)
\item Built backend services with .NET Core, Entity Framework Core, and Azure SQL Database
\item Integrated Azure cloud services (App Services, Blob Storage) for scalable deployment
\item Implemented MVVM architecture pattern and data binding for maintainable mobile code
\item Automated testing and CI/CD pipelines using Azure DevOps
\item Collaborated in Agile team environment with sprint planning and code reviews
\end{itemize}

\subsection*{Senior Material (Europe) AB | Platform Architect}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}

\textbf{Mobile \& Platform Development:}
\begin{itemize}[noitemsep]
\item Developed mobile-responsive web applications and React Native prototypes
\item Bridged communication between business stakeholders and technical team
\item Translated business requirements into technical specifications
\item Demonstrated strong interpersonal skills working with diverse international team
\item Proved ability to deliver results independently and as team player
\end{itemize}

\subsection*{AddCell | Cloud Developer (LIA 1 - Intensive Training)}
\textit{September 2022 - November 2022 | Gothenburg, Sweden}

\textbf{Mobile \& Cloud Development:}
\begin{itemize}[noitemsep]
\item Developed mobile applications with focus on cross-platform development
\item Built applications using .NET and Azure cloud services
\item Integrated mobile apps with cloud backends (Azure, AWS)
\item Practiced mobile testing on physical devices and emulators
\end{itemize}

\subsection*{Pembio AB | Full Stack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}

\textbf{Mobile \& Backend Development:}
\begin{itemize}[noitemsep]
\item Developed React Native mobile application for productivity SaaS platform
\item Built cross-platform mobile app with shared codebase for iOS and Android
\item Integrated mobile frontend with Spring Boot backend APIs
\item Implemented real-time features and push notifications
\item Worked remotely during COVID-19, demonstrating strong self-management skills
\end{itemize}

\subsection*{CollabMaker | Mobile Developer}
\textit{July 2020 - October 2020 | Gothenburg, Sweden}

\textbf{React Native Development:}
\begin{itemize}[noitemsep]
\item Developed React Native mobile application for career guidance platform
\item Built responsive mobile UI with React Native components
\item Integrated mobile app with backend APIs
\item Collaborated with cross-functional team in Agile environment
\item Demonstrated strong communication skills bridging frontend and backend teams
\end{itemize}

\section*{Android \& Mobile Projects}

\subsection*{CarAI Assistant (AndroidAuto-Ebot)}
\textit{2024 - Present} | \href{https://github.com/bluehawana/AndroidAuto-Ebot}{GitHub}
\begin{itemize}[noitemsep]
\item Built AI voice assistant for Android Auto with custom wake-word detection ("Hi Car")
\item System-level Android development with AOSP customization for automotive integration
\item Integrated GPT-4 LLM for natural language understanding and conversational responses
\item Implemented Text-to-Speech (TTS) and Speech-to-Text (STT) pipeline for hands-free experience
\item Tested extensively on Polestar 4 physical emulator and Firebase Test Lab
\item Technologies: Kotlin, Android Auto SDK, AOSP, OpenAI API, Edge TTS, Voice Recognition
\end{itemize}

\subsection*{CarTV Player (AndroidAuto-CarTVPlayer)}
\textit{2024 - Present} | \href{https://github.com/bluehawana/AndroidAuto-CarTVPlayer}{GitHub}
\begin{itemize}[noitemsep]
\item Designed customized Android Auto media player with enhanced audio controls
\item Built intuitive UI optimized for in-vehicle use with distraction-free design
\item Integrated voice command processing and secure data access via SQL backend
\item Tested on Polestar 4 emulator ensuring automotive compliance
\item Technologies: Kotlin, Android Auto, ExoPlayer, VLC Player, RESTful APIs
\end{itemize}

\subsection*{EPUB Reader for Android Auto}
\textit{2024 - Present} | \href{https://github.com/bluehawana/AndroidAuto-TTS-EpubReader}{GitHub}
\begin{itemize}[noitemsep]
\item Built EPUB-to-MP3 audiobook generator using Microsoft Edge TTS
\item Designed offline media synchronization for Android Auto playback
\item Created distraction-free in-car UI for audio playback while commuting
\item Tested on Polestar 4 and Firebase Test Lab
\item Technologies: Python, Edge TTS, EPUB parsing, Android Auto, Telegram Bot Integration
\end{itemize}

\subsection*{Gothenburg Taxi Pooling}
\textit{2024 - Present} | \href{https://github.com/bluehawana/GothenburgTaxiPooling-Java-ReactNative}{GitHub}
\begin{itemize}[noitemsep]
\item Hybrid mobile app: Native Android (Kotlin) for core features, React Native for cross-platform UI
\item Spring Boot backend with PostgreSQL database and RESTful API architecture
\item Neural network-powered matching algorithm for optimal ride pairing
\item Real-time geolocation tracking using Android Location Services and WebSocket
\item Tested on physical Android/iOS devices and Firebase Test Lab
\item Technologies: Kotlin, React Native, Spring Boot, PostgreSQL, Python ML, Google Maps API
\end{itemize}

\subsection*{Enterprise Info App}
\textit{2023 - Present} | \href{https://github.com/bluehawana/ReactNative-EntInfo}{GitHub}
\begin{itemize}[noitemsep]
\item Cross-platform enterprise mobile solution built with React Native and Expo
\item Offline-first architecture with AsyncStorage and SQLite for local data persistence
\item Real-time data synchronization with RESTful backend API
\item TypeScript for type safety and maintainable codebase
\item Tested on physical devices (Android/iOS) and Firebase Test Lab
\item Technologies: React Native, Expo, TypeScript, Redux, AsyncStorage, SQLite
\end{itemize}

\section*{Education}

\textbf{IT-Högskolan} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg

\textbf{Molndal Campus} | Bachelor's in Java Integration | 2019-2021 | Molndal

\textbf{University of Gothenburg} | Master's in International Business | 2016-2019 | Gothenburg

\section*{Certifications \& Testing}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item AWS Certified Solutions Architect - Associate (2022)
\item Microsoft Certified: Azure Fundamentals (2022)
\item Extensive testing experience: Polestar 4 physical emulator, Firebase Test Lab, physical devices
\item Active contributor to Android and React Native open-source communities
\end{itemize}

\section*{Soft Skills \& Cultural Bridge}

\begin{itemize}[leftmargin=*, itemsep=2pt]
\item \textbf{Cross-Cultural Communication:} Native Chinese, Fluent English, Swedish B2 - Bridge gaps between Asian and European teams
\item \textbf{Business-IT Bridge:} Master's in International Business + Technical expertise - Translate business needs to technical solutions
\item \textbf{Proven Track Record:} Successfully delivered projects at ECARX and Senior Material with international teams
\item \textbf{Strong Work Ethic:} Demonstrated ability to work independently and deliver results under pressure
\item \textbf{Team Player:} Excellent collaboration skills, positive attitude, and charisma in team environments
\item \textbf{Problem Solver:} Creative solutions to complex technical and communication challenges
\end{itemize}

\section*{Additional Information}

\textbf{Languages:} Chinese (Native), English (Fluent), Swedish (B2) - Unique trilingual advantage

\textbf{Work Authorization:} Swedish Permanent Residence

\textbf{Availability:} Immediate

\textbf{GitHub:} \href{https://github.com/bluehawana}{github.com/bluehawana} - Active portfolio with 20+ Android/React Native projects

\end{document}
"""
    
    return latex_cv


def generate_android_cover_letter(company: str, position: str):
    """Generate Android Developer Cover Letter with correct Overleaf template"""
    
    latex_cl = rf"""\documentclass[a4paper,10pt]{{article}}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{{geometry}}
\usepackage{{enumitem}}
\usepackage{{titlesec}}
\usepackage{{hyperref}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}

% Define colors
\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

% Section formatting
\titleformat{{\section}}{{\large\bfseries\raggedright\color{{black}}}}{{}}{{0em}}{{}}[\titlerule]
\titleformat{{\subsection}}[runin]{{\bfseries}}{{}}{{0em}}{{}}[:]

% Remove paragraph indentation
\setlength{{\parindent}}{{0pt}}

\begin{{document}}
\pagestyle{{empty}} % no page number

% Header
{{\color{{darkblue}}
{company}\\
{position}\\
Gothenburg, Sweden}}

\vspace{{14pt}}

\today

\vspace{{16pt}}

% Opening
\textbf{{Dear Hiring Manager,}}

\vspace{{8pt}}

I am writing to express my strong interest in the {position} position at {company}. With 6+ years of software development experience specializing in Android (Kotlin/Java), AOSP customization, and cross-platform mobile development, combined with my unique ability to bridge cultural and business-technical gaps, I am confident I would be a valuable addition to your team.

\textbf{{Technical Excellence with Real-World Impact}}

My Android development expertise spans native Kotlin/Java applications, AOSP 15 customization, and cross-platform solutions (.NET Xamarin, React Native). At ECARX (Geely Automotive), I worked extensively with AOSP 15, QNS integration, and Software Factory DevOps workflows, testing Android Automotive applications on Polestar 4 physical emulators. My GitHub portfolio includes CarAI Assistant (AI voice assistant for Android Auto with AOSP customization), CarTV Player (customized media player), Gothenburg Taxi Pooling (hybrid native Android + React Native), and Enterprise Info App (offline-first architecture). All projects have been rigorously tested on physical devices, Polestar 4 emulator, and Firebase Test Lab.

\textbf{{Bridging Gaps: My Unique Value Proposition}}

What sets me apart is my ability to bridge multiple gaps:

\textbf{{Cultural Bridge (Chinese-Swedish-English):}} As a native Chinese speaker with fluent English and Swedish B2, I excel at facilitating communication between Asian headquarters and European teams. At ECARX, I successfully bridged communication between Chinese management and Swedish developers across 4 global offices.

\textbf{{Business-IT Bridge:}} With a Master's in International Business combined with deep technical expertise, I translate complex business requirements into technical solutions. At Senior Material Europe AB, I worked directly with business stakeholders to deliver technical solutions that drove business value.

\textbf{{Technical Bridge (Frontend-Backend-Mobile):}} My full-stack background enables me to understand the entire application ecosystem, ensuring smooth API integration and optimal user experience.

\textbf{{Proven Soft Skills}}

My colleagues consistently highlight my communication excellence, problem-solving mindset, team collaboration, self-management, adaptability, and results-driven approach. At Senior Material Europe AB, I demonstrated exceptional ability to work with international teams while delivering technical solutions. My entrepreneurial background (Hong Yan AB, 8+ years) further proves my self-motivation and ability to see projects through from concept to completion.

I am particularly drawn to {company} because of the opportunity to contribute my unique combination of technical expertise and cross-cultural communication skills. I am confident that my trilingual capabilities, AOSP/DevOps experience, and proven track record would make me an asset to your team.

Thank you for considering my application. I look forward to the possibility of contributing to {company}'s success.

\vspace{{10pt}}

% Closing
Sincerely,

\vspace{{15pt}}

Harvad (Hongzhi) Li

\vspace{{20pt}}

{{\color{{darkblue}}\rule{{\linewidth}}{{0.6pt}}}}

\vspace{{4pt}}

{{\color{{darkblue}}
Ebbe Lieberathsgatan 27\\
412 65 Göteborg, Sweden\\
hongzhili01@gmail.com | 0728 384 299\\
LinkedIn: \href{{https://www.linkedin.com/in/hzl/}}{{linkedin.com/in/hzl}} | GitHub: \href{{https://github.com/bluehawana}}{{github.com/bluehawana}}}}

\end{{document}}
"""
    
    return latex_cl


def compile_latex(latex_content: str, output_name: str, output_dir: Path):
    """Compile LaTeX to PDF"""
    
    # Write LaTeX file
    tex_file = output_dir / f'{output_name}.tex'
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✅ Generated: {tex_file}")
    
    # Compile to PDF
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            pdf_file = output_dir / f'{output_name}.pdf'
            print(f"✅ Compiled: {pdf_file}")
            return True
        else:
            print(f"❌ LaTeX compilation failed for {output_name}")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ LaTeX compilation timed out for {output_name}")
        return False
    except FileNotFoundError:
        print("❌ pdflatex not found. Please install LaTeX (e.g., sudo apt-get install texlive-latex-base)")
        return False


def main():
    """Main function"""
    
    # Get company and position
    if len(sys.argv) >= 3:
        company = sys.argv[1]
        position = sys.argv[2]
    else:
        company = input("Enter company name: ").strip() or "Tech Company"
        position = input("Enter position: ").strip() or "Senior Android Developer"
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'android_application_package'
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n🚀 Generating Android Developer Application Package")
    print(f"   Company: {company}")
    print(f"   Position: {position}")
    print(f"   Output: {output_dir}\n")
    
    # Generate CV
    print("📄 Generating CV...")
    cv_latex = generate_android_cv()
    cv_success = compile_latex(cv_latex, 'Android_Developer_CV_Harvad_Li', output_dir)
    
    # Generate Cover Letter
    print("\n📄 Generating Cover Letter...")
    cl_latex = generate_android_cover_letter(company, position)
    cl_success = compile_latex(cl_latex, f'Android_Developer_CL_{company.replace(" ", "_")}', output_dir)
    
    # Summary
    print("\n" + "="*60)
    if cv_success and cl_success:
        print("✅ SUCCESS! Android Developer Application Package Generated")
        print(f"\n📦 Files created in: {output_dir}")
        print(f"  - Android_Developer_CV_Harvad_Li.pdf")
        print(f"  - Android_Developer_CL_{company.replace(' ', '_')}.pdf")
        print("\n🎯 Key Highlights:")
        print("  ✓ 6+ years experience (2019-Present)")
        print("  ✓ AOSP 15, QNS, Software Factory DevOps")
        print("  ✓ .NET Xamarin graduate project + React Native")
        print("  ✓ Android/React Native projects with GitHub links")
        print("  ✓ Polestar 4 + Firebase Test Lab testing mentioned")
        print("  ✓ Soft skills and cultural bridge emphasized")
        print("  ✓ LinkedIn blue header/footer format")
    else:
        print("⚠️  Some files failed to compile. Check errors above.")
    print("="*60)


if __name__ == '__main__':
    main()
