#!/usr/bin/env python3
"""
Hongzhi Li's CV Template - LEGO Component Tailoring System
Intelligently customizes your excellent LaTeX template based on job requirements
"""
from typing import Dict, Any

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
clas
s LegoResumeBuilder:
    """LEGO Component Resume Builder - Intelligently tailors resume based on job requirements"""
    
    def __init__(self):
        self.base_template = CV_TEMPLATE
        self.profile_summary = PROFILE_SUMMARY
        self.technical_skills = TECHNICAL_SKILLS
        self.experience_section = EXPERIENCE_SECTION
        self.projects_section = PROJECTS_SECTION
    
    def generate_tailored_resume(self, job_data: Dict[str, Any]) -> str:
        """Generate LEGO-tailored resume based on job requirements"""
        
        # Analyze job requirements
        job_title = job_data.get('title', '').lower()
        job_description = job_data.get('description', '').lower()
        company = job_data.get('company', 'Company')
        
        # Determine job focus areas
        is_devops = self._is_devops_role(job_title, job_description)
        is_backend = self._is_backend_role(job_title, job_description)
        is_frontend = self._is_frontend_role(job_title, job_description)
        is_fullstack = self._is_fullstack_role(job_title, job_description)
        
        # Build LEGO components
        role_title = self._get_role_title(is_devops, is_backend, is_frontend, is_fullstack)
        tailored_summary = self._get_tailored_summary(company, is_devops, is_backend, is_frontend, is_fullstack)
        tailored_skills = self._get_tailored_skills(is_devops, is_backend, is_frontend, is_fullstack)
        tailored_experience = self._get_tailored_experience(is_devops, is_backend, is_frontend, is_fullstack)
        tailored_projects = self._get_tailored_projects(is_devops, is_backend, is_frontend, is_fullstack)
        
        # Assemble LEGO components into final resume
        return self.base_template.replace("ROLE_TITLE", role_title) \
                                .replace("PROFILE_SUMMARY", tailored_summary) \
                                .replace("TECHNICAL_SKILLS", tailored_skills) \
                                .replace("EXPERIENCE_SECTION", tailored_experience) \
                                .replace("PROJECTS_SECTION", tailored_projects)
    
    def _is_devops_role(self, job_title: str, job_description: str) -> bool:
        """Detect if this is a DevOps/Infrastructure role"""
        devops_keywords = ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd', 
                          'deployment', 'monitoring', 'grafana', 'jenkins', 'terraform', 'ansible']
        return any(keyword in job_title + job_description for keyword in devops_keywords)
    
    def _is_backend_role(self, job_title: str, job_description: str) -> bool:
        """Detect if this is a Backend role"""
        backend_keywords = ['backend', 'api', 'microservices', 'spring', 'java', 'database', 'server',
                           'rest', 'graphql', 'sql', 'postgresql', 'mysql', 'mongodb']
        return any(keyword in job_title + job_description for keyword in backend_keywords)
    
    def _is_frontend_role(self, job_title: str, job_description: str) -> bool:
        """Detect if this is a Frontend role"""
        frontend_keywords = ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui', 'ux', 
                            'typescript', 'css', 'html', 'responsive', 'mobile']
        return any(keyword in job_title + job_description for keyword in frontend_keywords)
    
    def _is_fullstack_role(self, job_title: str, job_description: str) -> bool:
        """Detect if this is a Fullstack role"""
        fullstack_keywords = ['fullstack', 'full-stack', 'full stack']
        return any(keyword in job_title + job_description for keyword in fullstack_keywords)
    
    def _get_role_title(self, is_devops: bool, is_backend: bool, is_frontend: bool, is_fullstack: bool) -> str:
        """Get tailored professional title"""
        if is_devops:
            return "DevOps Engineer & Cloud Infrastructure Specialist"
        elif is_backend and not is_frontend:
            return "Backend Developer & API Specialist"
        elif is_frontend and not is_backend:
            return "Frontend Developer & UI Specialist"
        else:
            return "Fullstack Developer"
    
    def _get_tailored_summary(self, company: str, is_devops: bool, is_backend: bool, is_frontend: bool, is_fullstack: bool) -> str:
        """Get tailored professional summary"""
        if is_devops:
            return f"""Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, AWS, Docker, and infrastructure automation. Strong background in migrating from AKS to local Kubernetes clusters, implementing monitoring solutions using Grafana, and managing complex network systems. Demonstrated ability to work across the entire infrastructure stack from cloud platforms to system reliability and enterprise-level technical solution design. Specialized in infrastructure optimization roles for companies like {company}."""
        elif is_backend:
            return f"""Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, RESTful APIs, and scalable backend systems. Strong background in Java/J2EE development, comprehensive database management across SQL and NoSQL platforms, and end-to-end backend application development. Demonstrated ability to work across the entire backend technology stack from API design to database optimization and microservices architecture. Specialized in backend development roles for companies like {company}."""
        elif is_frontend:
            return f"""Experienced Frontend Developer with over 5 years of expertise in modern web technologies, user interface development, and responsive design. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in React, Angular, Vue.js, and mobile-first development. Strong background in JavaScript/TypeScript development, comprehensive frontend framework integration, and end-to-end user experience optimization. Demonstrated ability to work across the entire frontend technology stack from UI/UX design to performance optimization and cross-platform development. Specialized in frontend development roles for companies like {company}."""
        else:
            return f"""Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Demonstrated ability to work across the entire technology stack from frontend user interfaces to backend services and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions for companies like {company}."""
    
    def _get_tailored_skills(self, is_devops: bool, is_backend: bool, is_frontend: bool, is_fullstack: bool) -> str:
        """Get tailored technical skills section"""
        if is_devops:
            return r"""
\begin{itemize}[noitemsep]
\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud ECS
\item \textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)
\item \textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI, Automated Testing, Deployment Pipelines
\item \textbf{Infrastructure:} Infrastructure as Code, System Integration, Network Management, Cost Optimization
\item \textbf{Monitoring:} Grafana, Advanced Scripting, System Reliability, Performance Monitoring
\item \textbf{Programming Languages:} Python, Bash, PowerShell, Java, JavaScript, Go
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, ApsaraDB
\item \textbf{Backend Frameworks:} Spring Boot, .NET Core, Node.js, FastAPI
\item \textbf{Version Control:} Git, GitHub, GitLab
\item \textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews
\item \textbf{Security:} Application security, Data protection, Authentication/Authorization
\end{itemize}
"""
        elif is_backend:
            return r"""
\begin{itemize}[noitemsep]
\item \textbf{Programming Languages:} Java/J2EE, C\#/.NET Core, Python, JavaScript, TypeScript
\item \textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI
\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture
\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud
\item \textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest
\item \textbf{Performance Optimization:} Database optimization, Caching strategies, Application scaling
\item \textbf{Security:} Application security, Data protection, Authentication/Authorization
\item \textbf{Version Control:} Git, GitHub, GitLab
\item \textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI
\item \textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews
\end{itemize}
"""
        elif is_frontend:
            return r"""
\begin{itemize}[noitemsep]
\item \textbf{Frontend Frameworks:} React, Angular, Vue.js, React Native
\item \textbf{Programming Languages:} JavaScript, TypeScript, HTML5, CSS3
\item \textbf{UI/UX:} Responsive Design, Mobile-First Design, User Experience Optimization
\item \textbf{State Management:} Redux, Context API, Vuex, State Management Patterns
\item \textbf{Build Tools:} Webpack, Vite, npm, yarn, Modern Build Pipelines
\item \textbf{Testing:} Jest, Cypress, Unit Testing, Integration Testing, E2E Testing
\item \textbf{API Integration:} RESTful APIs, GraphQL, Axios, Fetch API
\item \textbf{Version Control:} Git, GitHub, GitLab
\item \textbf{Performance:} Code Splitting, Lazy Loading, Performance Optimization
\item \textbf{Cross-Platform:} Progressive Web Apps, Mobile Development, Responsive Design
\item \textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews
\end{itemize}
"""
        else:
            return TECHNICAL_SKILLS
    
    def _get_tailored_experience(self, is_devops: bool, is_backend: bool, is_frontend: bool, is_fullstack: bool) -> str:
        """Get tailored professional experience section"""
        if is_devops:
            return r"""
\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\end{itemize}

\subsection*{AddCell (CTH Startup) | DevOps Engineer}
\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed cloud-native applications using serverless computing architecture
\item Implemented GraphQL APIs for efficient data fetching and frontend integration
\item Worked with SQL and NoSQL databases for optimal data storage and retrieval
\end{itemize}

\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

\subsection*{Senior Material (Europe) AB | Platform Architect \& Project Coordinator}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration of business-critical applications with microservices architecture
\item Collaborated with development teams to optimize applications for maximum speed and scalability
\item Participated in Agile ceremonies including sprint planning, reviews, and retrospectives
\end{itemize}
"""
        elif is_backend:
            return r"""
\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection*{Senior Material (Europe) AB | Platform Architect \& Project Coordinator}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration of business-critical applications with microservices architecture
\item Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption
\item Collaborated with development teams to optimize applications for maximum speed and scalability
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\item Developed RESTful APIs and implemented comprehensive database integration
\item Implemented automated testing strategies and ensured application security
\end{itemize}

\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\end{itemize}
"""
        elif is_frontend:
            return r"""
\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Built complete office management platform from scratch, architecting frontend components
\item Developed comprehensive user interfaces using modern frontend frameworks
\item Collaborated with backend teams for seamless API integration
\end{itemize}

\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Developed responsive user interfaces for "Omstallningsstod.se" adult education platform
\item Implemented secure data handling and user authentication flows
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Built frontend features using Vue.js framework and integrated with backend APIs
\item Developed responsive user interfaces for Pembio.com platform
\item Participated in Agile development processes and collaborated with cross-functional teams
\end{itemize}

\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\end{itemize}
"""
        else:
            return EXPERIENCE_SECTION
    
    def _get_tailored_projects(self, is_devops: bool, is_backend: bool, is_frontend: bool, is_fullstack: bool) -> str:
        """Get tailored hobby projects section"""
        if is_devops:
            return r"""
\section*{Hobby Projects}

\subsection{Weather\_Anywhere.CLOUD\_API\_Encoding}
\textit{Feb 2024 -- Present} \\
\textbf{SpringBoot, AlibabaCloudECS, ApsaraDBRDS(MySQL), Heroku}
\begin{itemize}
\item Weather tracking app for Swedish and global cities using OpenCageData and Open-Meteo APIs
\item Deployed on Alibaba Cloud ECS with city coordinates and weather data stored in ApsaraDB MySQL
\item Dynamic city lookup and caching mechanism for optimized API usage and response speed
\item Demo: https://weather.bluehawana.com
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

\subsection{SmrtMart.com\_COMMERCE.WEB}
\textit{April 2024 -- Present} \\
\textbf{Go, Next, PostgreSQL, Microservices, StripeAPI}
\begin{itemize}
\item Fullstack e-commerce platform with microservices-based architecture for seamless scalability
\item Implemented comprehensive order management, inventory tracking, and payment systems
\item Optimized backend API performance and integrated PostgreSQL and MongoDB for hybrid data storage
\end{itemize}
"""
        elif is_backend:
            return r"""
\section*{Hobby Projects}

\subsection{Jobhunter\_Python\_TypeScript\_RESTAPI}
\textit{July 2025 -- Present} \\
\textbf{Python, TypeScript, GmailRESTAPI, LinkedinAPI}
\begin{itemize}
\item Automated job hunting pipeline integrating Gmail search, job scraping, and resume customization
\item Generated resumes and cover letters based on job descriptions using NLP techniques
\item Auto-sent job application drafts to user with a fully functional end-to-end workflow
\item Demo: https://jobs.bluehawana.com
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
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection{Gothenburg\_TaxiPooling\_Java\_ReacNative\_PythonALGO}
\textit{May 2025 -- Present} \\
\textbf{SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL}
\begin{itemize}
\item Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking
\item Developed cross-platform mobile application using React Native and Spring Boot microservices
\item Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling
\end{itemize}
"""
        elif is_frontend:
            return r"""
\section*{Hobby Projects}

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

\subsection{AndroidAuto\_CarTVPlayer\_KOTLIN}
\textit{March 2025 -- Present} \\
\textbf{Kotlin, AndroidAuto, RESTfulAPIs, EXOPlaer, VLCPlayer}
\begin{itemize}
\item Designed and built a customized Android Auto media player with enhanced audio controls and intuitive UI
\item Integrated voice command processing and secure data access via SQL backend
\item Developed and tested robust frontend and backend modules for smooth in-vehicle experience
\end{itemize}

\subsection{Gothenburg\_TaxiPooling\_Java\_ReacNative\_PythonALGO}
\textit{May 2025 -- Present} \\
\textbf{SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL}
\begin{itemize}
\item Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking
\item Developed cross-platform mobile application using React Native and Spring Boot microservices
\item Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling
\end{itemize}

\subsection{AndroidAuto\_TTS\_EpubReader}
\textit{June 2025 -- Present} \\
\textbf{Python, EdgeTTS, EPUB, AndroidAuto, TelegramBotIntegration, CloudFlare}
\begin{itemize}
\item Built an EPUB-to-MP3 audiobook generator using Microsoft Edge TTS for Android Auto playback
\item Designed offline media synchronization for customized reading-on-the-road experience
\item Created distraction-free in-car UI for audio playbook of personalized content while commuting
\end{itemize}
"""
        else:
            return PROJECTS_SECTION


# Create global instance for easy access
lego_builder = LegoResumeBuilder()

def generate_tailored_cv(job_data: Dict[str, Any]) -> str:
    """Main function to generate LEGO-tailored CV"""
    return lego_builder.generate_tailored_resume(job_data)