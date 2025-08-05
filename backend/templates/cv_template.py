#!/usr/bin/env python3
"""
Hongzhi Li's CV Template - Python-friendly version
Converted from your exact LaTeX template with proper escaping
"""

CV_TEMPLATE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fontawesome}

% Page setup
\geometry{margin=0.75in}
\pagestyle{empty}

% Color definitions
\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{lightgray}{RGB}{128,128,128}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}

% Section formatting
\titleformat{\section}{\Large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\large\bfseries}{}{0em}{}

% Custom commands
\newcommand{\contactitem}[2]{\textcolor{darkblue}{#1} #2}

\begin{document}
\pagestyle{empty} % no page number

% Name and contact details
\begin{center}
{\LARGE \textbf{Hongzhi Li}}\\[10pt]
{\Large \textit{ROLE_TITLE}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

% Personal Profile
\section*{Profile Summary}
PROFILE_SUMMARY

% Areas of Expertise
\section*{Core Technical Skills}
TECHNICAL_SKILLS

% Experience
EXPERIENCE_SECTION

PROJECTS_SECTION

\vspace{6pt}
\section*{Education}
\textbf{IT Högskolan}\\
\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\
\textbf{Mölndal Campus}\\
\textit{Bachelor's Degree in Java Integration} | 2019-2021\\
\textbf{University of Gothenburg}\\
\textit{Master's Degree in International Business and Trade} | 2016-2019\\

\vspace{6pt}
\section*{Certifications}
\begin{itemize}
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\end{itemize}

\vspace{6pt}
\section*{Additional Information}
\begin{itemize}
\item \textbf{Languages:} Fluent in English and Mandarin
\item \textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\item \textbf{Customer Websites:} \href{https://www.senior798.eu}{senior798.eu}, \href{https://www.mibo.se}{mibo.se}, \href{https://www.omstallningsstod.se}{omstallningsstod.se}
\end{itemize}

\end{document}
"""

# Your complete profile summary
PROFILE_SUMMARY = """Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Demonstrated ability to work across the entire technology stack from frontend user interfaces to backend services and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments."""

# Your complete technical skills
TECHNICAL_SKILLS = r"""
\begin{itemize}[noitemsep]
\item \textbf{Programming Languages:} Java/J2EE, JavaScript, C\#/.NET Core, Python, Bash, PowerShell
\item \textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
\item \textbf{Backend Frameworks:} Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
\item \textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest
\item \textbf{Cloud Platforms:} AWS, Azure, GCP
\item \textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)
\item \textbf{Version Control:} Git, GitHub, GitLab
\item \textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI
\item \textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews
\item \textbf{Performance Optimization:} Application scaling, Database optimization, Caching strategies
\item \textbf{Security:} Application security, Data protection, Authentication/Authorization
\end{itemize}
"""

# Your complete experience section
EXPERIENCE_SECTION = r"""
\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\end{itemize}

\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting both frontend and backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection*{Senior Material (Europe) AB | Platform Architect \& Project Coordinator}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration of business-critical applications with microservices architecture
\item Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption
\item Collaborated with development teams to optimize applications for maximum speed and scalability
\item Participated in Agile ceremonies including sprint planning, reviews, and retrospectives
\end{itemize}

\subsection*{AddCell (CTH Startup) | DevOps Engineer}
\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed cloud-native applications using serverless computing architecture
\item Implemented GraphQL APIs for efficient data fetching and frontend integration
\item Worked with SQL and NoSQL databases for optimal data storage and retrieval
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\item Built frontend features using Vue.js framework and integrated with backend APIs
\item Developed RESTful APIs and implemented comprehensive database integration
\item Participated in Agile development processes and collaborated with cross-functional teams
\item Implemented automated testing strategies and ensured application security
\end{itemize}
"""

# Your complete projects section
PROJECTS_SECTION = r"""
\section*{Hobby Projects}
\subsection{AndroidAuto\_AI\_Bot}
\textit{June 2025 -- Present} \\
\textbf{AndroidAuto, EdgeTTS, TwitterAPI, LLM, Python, Kotelin}
\begin{itemize}
\item Designed an in-car AI voice assistant for Android Auto, activated via a custom wake-word \texttt{"Hi Car"}, as a smarter alternative to Google Assistant
\item Integrated Large Language Models (LLMs) for natural language understanding and real-time conversational responses
\item Enabled real-time querying of public Twitter/X content (e.g., Elon Musk, Donald Trump) via Twitter API, with responses converted to speech using Edge TTS
\item Built a text-to-speech (TTS) pipeline to vocalize responses from the LLM and external APIs for hands-free, eyes-free user experience
\item Designed for Android Auto with a distraction-free, voice-only interface and on-device wake-word detection
\item Supports conversational queries, personalized information access, and live updates while commuting
\end{itemize}

\subsection{AndroidAuto\_TTS\_EpubReader}
\textit{June 2025 -- Present} \\
\textbf{Python, EdgeTTS, EPUB, AndroidAuto, TelegramBotIntegration, CloudFlare}
\begin{itemize}
\item Built an EPUB-to-MP3 audiobook generator using Microsoft Edge TTS for Android Auto playback
\item Designed offline media synchronization for customized reading-on-the-road experience
\item Created distraction-free in-car UI for audio playbook of personalized content while commuting
\end{itemize}

\subsection{Jobhunter\_Python\_TypeScript\_RESTAPI}
\textit{July 2025 -- Present} \\
\textbf{Python, TypeScript, GmailRESTAPI, LinkedinAPI}
\begin{itemize}
\item Automated job hunting pipeline integrating Gmail search, job scraping, and resume customization
\item Generated resumes and cover letters based on job descriptions using NLP techniques
\item Auto-sent job application drafts to user with a fully functional end-to-end workflow
\end{itemize}

\subsection{Bluehawana.com\_Web.HTML}
\textit{Jan 2025 -- Present} \\
\textbf{HTML5, CSS3, JavaScript, GitHubAPI, LinkedIn API}
\begin{itemize}
\item Redesigned and upgraded personal portfolio website from static GitHub Pages to dynamic, professional-grade tech site
\item Integrated GitHub API for real-time repository feed and LinkedIn API for automated blog synchronization
\item Implemented responsive UI/UX with mobile-first design principles and performance-optimized layout
\item Deployed on Netlify with custom domain and automated CI/CD via Git
\item Added professional services module with booking system and contact form integration
\end{itemize}

\subsection{Gothenburg\_TaxiPooling\_Java\_ReacNative\_PythonALGO}
\textit{May 2025 -- Present} \\
\textbf{SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL}
\begin{itemize}
\item Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking
\item Developed cross-platform mobile application using React Native and Spring Boot microservices
\item Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling
\item Engineered for performance optimization and GDPR-compliant data privacy
\end{itemize}

\subsection{AndroidAuto\_CarTVPlayer\_KOTLIN}
\textit{March 2025 -- Present} \\
\textbf{Kotlin, AndroidAuto, RESTfulAPIs, EXOPlaer, VLCPlayer}
\begin{itemize}
\item Designed and built a customized Android Auto media player with enhanced audio controls and intuitive UI
\item Integrated voice command processing and secure data access via SQL backend
\item Developed and tested robust frontend and backend modules for smooth in-vehicle experience
\end{itemize}

\subsection{SmrtMart.com\_COMMERCE.WEB}
\textit{April 2024 -- Present} \\
\textbf{Go, Next, PostgreSQL, Microservices, StripeAPI}
\begin{itemize}
\item Fullstack e-commerce platform with microservices-based architecture for seamless scalability
\item Implemented comprehensive order management, inventory tracking, and payment systems
\item Optimized backend API performance and integrated PostgreSQL and MongoDB for hybrid data storage
\end{itemize}

\subsection{Weather\_Anywhere.CLOUD\_API\_Encoding}
\textit{Feb 2024 -- Present} \\
\textbf{SpringBoot, AlibabaCloudECS, ApsaraDBRDS(MySQL), Heroku}
\begin{itemize}
\item Weather tracking app for Swedish and global cities using OpenCageData and Open-Meteo APIs
\item Deployed on Alibaba Cloud ECS with city coordinates and weather data stored in ApsaraDB MySQL
\item Dynamic city lookup and caching mechanism for optimized API usage and response speed
\end{itemize}
"""