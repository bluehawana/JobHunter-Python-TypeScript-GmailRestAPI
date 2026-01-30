#!/usr/bin/env python3
"""
Generate Android Developer CV and Cover Letter
Focuses on Android/React Native projects and soft skills
"""

import sys
from pathlib import Path
import subprocess
from datetime import datetime

def generate_android_cv():
    """Generate Android Developer CV with project focus"""
    
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
Senior Android Developer with 6+ years of software development experience (2019-Present) specializing in native Android and React Native applications. Expert in Kotlin, Java, and cross-platform mobile development with proven track record building automotive infotainment systems and consumer mobile apps. Strong background in bridging technical and business requirements, with unique ability to communicate across cultures (Chinese-Swedish-English). Currently at ECARX developing Android-based automotive solutions. All projects tested on physical devices including Polestar 4 emulator and Google Firebase Test Lab.

\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
\item \textbf{Mobile Development:} Android (Kotlin, Java), React Native, Expo, Native Android SDK
\item \textbf{Android Framework:} Activities, Services, Content Providers, Broadcast Receivers, MVVM, Clean Architecture
\item \textbf{Cross-Platform:} React Native, Expo, JavaScript/TypeScript, Redux, React Navigation
\item \textbf{Automotive:} Android Auto, Polestar 4 testing, In-car applications, Voice integration
\item \textbf{Testing:} Physical device testing (Polestar 4), Firebase Test Lab, JUnit, Espresso, Jest
\item \textbf{Backend Integration:} RESTful APIs, GraphQL, Spring Boot, PostgreSQL, MongoDB
\item \textbf{Cloud \& DevOps:} AWS, Azure, Docker, CI/CD (GitHub Actions, GitLab CI)
\item \textbf{Tools:} Android Studio, VS Code, Git, Gradle, npm, Expo CLI
\item \textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native) - Bridge communication gaps
\end{itemize}

\section*{Professional Experience}

\subsection*{ECARX (Geely Automotive) | Android Developer / IT Specialist}
\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed Android-based automotive infotainment systems for Geely/Volvo vehicles
\item Built and tested Android Auto applications on Polestar 4 physical emulator
\item Collaborated with international teams across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
\item Bridged communication between Chinese headquarters and Swedish development team
\item Implemented CI/CD pipelines for Android app deployment using GitHub Actions
\item Managed technical requirements gathering and stakeholder communication
\end{itemize}

\subsection*{Synteda AB | Mobile Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed mobile applications using React Native and native Android
\item Built cross-platform solutions with shared codebase for iOS and Android
\item Integrated mobile apps with Azure cloud services and RESTful APIs
\item Tested applications on physical devices and Firebase Test Lab
\item Collaborated with clients to translate business requirements into technical solutions
\end{itemize}

\subsection*{IT-Högskolan | Mobile Developer (LIA 2 - Intensive Training)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Intensive mobile development training (40+ hours/week, 5 months)
\item Built Android applications with Kotlin and Java
\item Developed React Native cross-platform applications
\item Practiced modern mobile architecture patterns (MVVM, Clean Architecture)
\item Gained hands-on experience with mobile CI/CD and testing strategies
\end{itemize}

\subsection*{Senior Material (Europe) AB | Mobile \& Platform Developer}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Developed mobile-responsive web applications and React Native prototypes
\item Bridged communication between business stakeholders and technical team
\item Translated business requirements into technical specifications
\item Demonstrated strong interpersonal skills working with diverse international team
\item Proved ability to deliver results independently and as team player
\end{itemize}

\subsection*{AddCell | Mobile Developer (LIA 1 - Intensive Training)}
\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed mobile applications with focus on cross-platform development
\item Built React Native applications with Expo framework
\item Integrated mobile apps with cloud backends (Azure, AWS)
\item Practiced mobile testing on physical devices and emulators
\end{itemize}

\subsection*{Pembio AB | Full Stack Developer (React Native Focus)}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed React Native mobile application for productivity SaaS platform
\item Built cross-platform mobile app with shared codebase for iOS and Android
\item Integrated mobile frontend with Spring Boot backend APIs
\item Implemented real-time features and push notifications
\item Worked remotely during COVID-19, demonstrating strong self-management skills
\end{itemize}

\subsection*{CollabMaker | Mobile Developer (React Native)}
\textit{July 2020 - October 2020 | Gothenburg, Sweden}
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
\item Built AI voice assistant for Android Auto with custom wake-word detection
\item Integrated LLM (GPT-4) for natural language understanding and conversational responses
\item Implemented Text-to-Speech (TTS) pipeline for hands-free, eyes-free user experience
\item Tested extensively on Polestar 4 physical emulator and Firebase Test Lab
\item Technologies: Kotlin, Android Auto SDK, OpenAI API, Edge TTS, Voice Recognition
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
\item Neural network-powered carpooling platform with React Native mobile app
\item Developed cross-platform mobile application with real-time geolocation tracking
\item Integrated Spring Boot backend with PostgreSQL for scalable data handling
\item Implemented secure payment processing and RESTful APIs
\item Tested on physical Android devices and Firebase Test Lab
\item Technologies: React Native, Spring Boot, PostgreSQL, Python ML, Google Maps API
\end{itemize}

\subsection*{Enterprise Info App (React Native + Expo)}
\textit{2023 - Present} | \href{https://github.com/bluehawana/ReactNative-EntInfo}{GitHub}
\begin{itemize}[noitemsep]
\item Built enterprise information management app using React Native and Expo
\item Developed cross-platform mobile solution with shared codebase
\item Implemented offline-first architecture with local data persistence
\item Integrated with backend APIs for real-time data synchronization
\item Tested on physical devices (Android/iOS) and Firebase Test Lab
\item Technologies: React Native, Expo, TypeScript, Redux, AsyncStorage
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
    """Generate Android Developer Cover Letter emphasizing soft skills"""
    
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

I am writing to express my strong interest in the {position} position at {company}. With 6+ years of software development experience specializing in Android and React Native applications, combined with my unique ability to bridge cultural and business-technical gaps, I am confident I would be a valuable addition to your team.

\textbf{{Technical Excellence with Real-World Impact}}

My Android development expertise spans native Kotlin/Java applications and cross-platform React Native solutions. At ECARX (Geely Automotive), I developed Android-based automotive infotainment systems tested on Polestar 4 physical emulators. My GitHub portfolio includes CarAI Assistant (AI voice assistant for Android Auto), CarTV Player (customized media player), Gothenburg Taxi Pooling (React Native with real-time geolocation), and Enterprise Info App (offline-first architecture). All projects have been rigorously tested on physical devices, Polestar 4 emulator, and Firebase Test Lab.

\textbf{{Bridging Gaps: My Unique Value Proposition}}

What sets me apart is my ability to bridge multiple gaps:

\textbf{{Cultural Bridge (Chinese-Swedish-English):}} As a native Chinese speaker with fluent English and Swedish B2, I excel at facilitating communication between Asian headquarters and European teams. At ECARX, I successfully bridged communication between Chinese management and Swedish developers across 4 global offices.

\textbf{{Business-IT Bridge:}} With a Master's in International Business combined with deep technical expertise, I translate complex business requirements into technical solutions. At Senior Material Europe AB, I worked directly with business stakeholders to deliver technical solutions that drove business value.

\textbf{{Technical Bridge (Frontend-Backend-Mobile):}} My full-stack background enables me to understand the entire application ecosystem, ensuring smooth API integration and optimal user experience.

\textbf{{Proven Soft Skills}}

My colleagues consistently highlight my communication excellence, problem-solving mindset, team collaboration, self-management, adaptability, and results-driven approach. At Senior Material Europe AB, I demonstrated exceptional ability to work with international teams while delivering technical solutions. My entrepreneurial background (Hong Yan AB, 8+ years) further proves my self-motivation and ability to see projects through from concept to completion.

I am particularly drawn to {company} because of the opportunity to contribute my unique combination of technical expertise and cross-cultural communication skills. I am confident that my trilingual capabilities, technical skills, and proven track record would make me an asset to your team.

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
    
    print(f"📝 Generated LaTeX: {tex_file}")
    
    # Compile to PDF
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        pdf_file = output_dir / f'{output_name}.pdf'
        if pdf_file.exists():
            print(f"✅ Generated PDF: {pdf_file}")
            return True
        else:
            print(f"❌ PDF generation failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Generate Android Developer CV and Cover Letter"""
    
    print("🚀 Generating Android Developer Application Package...\n")
    
    # Create output directory
    output_dir = Path('android_application_package')
    output_dir.mkdir(exist_ok=True)
    
    # Generate CV
    print("="*60)
    print("Generating Android Developer CV")
    print("="*60)
    cv_latex = generate_android_cv()
    cv_success = compile_latex(cv_latex, 'Android_Developer_CV_Harvad_Li', output_dir)
    
    # Generate Cover Letter
    print("\n" + "="*60)
    print("Generating Android Developer Cover Letter")
    print("="*60)
    company = input("Enter company name (or press Enter for 'Your Company'): ").strip() or "Your Company"
    position = input("Enter position title (or press Enter for 'Android Developer'): ").strip() or "Android Developer"
    
    cl_latex = generate_android_cover_letter(company, position)
    cl_success = compile_latex(cl_latex, f'Android_Developer_CL_{company.replace(" ", "_")}', output_dir)
    
    # Summary
    print("\n" + "="*60)
    print("📊 Generation Summary")
    print("="*60)
    print(f"CV: {'✅ Success' if cv_success else '❌ Failed'}")
    print(f"Cover Letter: {'✅ Success' if cl_success else '❌ Failed'}")
    
    if cv_success and cl_success:
        print(f"\n✅ Application package ready in: {output_dir}/")
        print("\nFiles generated:")
        print(f"  - Android_Developer_CV_Harvad_Li.pdf")
        print(f"  - Android_Developer_CL_{company.replace(' ', '_')}.pdf")
        print("\n🎯 Key Highlights:")
        print("  ✓ 6+ years experience (2019-Present)")
        print("  ✓ Android/React Native projects with GitHub links")
        print("  ✓ Polestar 4 + Firebase Test Lab testing mentioned")
        print("  ✓ Soft skills emphasized (cultural bridge, communication)")
        print("  ✓ ECARX and Senior Material experience highlighted")
        print("  ✓ Trilingual advantage (Chinese-English-Swedish)")


if __name__ == '__main__':
    main()
