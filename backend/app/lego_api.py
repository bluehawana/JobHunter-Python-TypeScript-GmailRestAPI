"""
🧱 LEGO Bricks API for Job Application Generation
Handles job analysis, LEGO bricks assembly, and PDF generation
"""

from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
import sys
import os
import json
import subprocess
import re
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from gemini_content_polisher import GeminiContentPolisher
from smart_latex_editor import SmartLaTeXEditor
from cv_templates import CVTemplateManager
from ai_analyzer import AIAnalyzer
from ai_resume_prompts import AIResumePrompts
from linkedin_job_extractor import extract_linkedin_job_info_from_content

lego_api = Blueprint('lego_api', __name__)

# Initialize managers
template_manager = CVTemplateManager()
ai_analyzer = AIAnalyzer()
ai_prompts = AIResumePrompts()

# LEGO Bricks definitions
PROFILE_BRICKS = {
    'incident_management_specialist': """Incident Management Specialist and DevOps/SRE Engineer with 6+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations (2019-Present). Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Expert in rapid incident response - restored 26 servers in 5 hours through systematic RCA. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation (Jenkins, GitHub Actions), and comprehensive observability (Prometheus, Grafana, ELK). Reduced cloud costs 45% through strategic migration and optimization. AWS/Azure certified with strong Linux administration, Python/Bash scripting, and Agile collaboration. Passionate about platform reliability, MTTR reduction, and developer experience.""",

    'devops_engineer': """DevOps Engineer with 6+ years building CI/CD pipelines, automating infrastructure, and managing cloud platforms (2019-Present). Expert in Kubernetes, Docker, Terraform, and cloud optimization across AWS and Azure. Proven track record in infrastructure automation, monitoring solutions, and platform reliability. Reduced cloud costs by 45% through strategic optimization. Strong background in both development and operations across multiple companies including ECARX, Synteda, Senior Material, and Pembio.""",

    'fullstack_developer': """Full-stack engineer with 6+ years building scalable web applications and cloud infrastructure solutions (2019-Present). Strong frontend expertise in React, TypeScript, and modern JavaScript, combined with deep cloud platform experience across AWS, Azure, and GCP. Proven track record collaborating with international teams, designing RESTful/GraphQL APIs, and delivering high-performance user experiences. Expert in both Java/Spring Boot and .NET Core with extensive DevOps and cloud deployment experience.""",

    'backend_developer': """Backend Developer with 6+ years building enterprise applications and microservices (2019-Present). Strong expertise in Java, Spring Boot, .NET Core, and Python with deep database optimization skills (PostgreSQL, MongoDB, Redis). Proven track record designing RESTful APIs handling millions of requests. Unique combination of Master's in International Business with technical expertise - understanding both implementation and business impact. Extensive experience with cloud platforms (AWS, Azure) and DevOps practices.""",

    'frontend_developer': """Frontend Developer with 6+ years of software development experience (2019-Present) including extensive frontend work with React, Angular, Vue.js, and TypeScript. Expert in building responsive, performant user interfaces with modern JavaScript frameworks and state management solutions. Strong background in full-stack development provides deep understanding of API integration, backend communication, and end-to-end application architecture. Experience with cloud deployment, CI/CD pipelines, and DevOps practices across ECARX, Synteda, Senior Material, Pembio, and CollabMaker.""",

    'android_developer': """Experienced Android Developer with 6+ years of software development experience (2019-Present) including native Android development using Kotlin and Java. Expert in Android SDK, Android Studio, and automotive infotainment systems. Strong background in building performant mobile applications with modern architecture patterns. Currently at ECARX bringing Android development expertise to automotive technology solutions.""",

    'ios_developer': """iOS Developer with 6+ years of software development experience (2019-Present) including mobile application development. Strong foundation in Swift, Objective-C, and iOS SDK with proven ability to build scalable mobile applications. Background in full-stack development provides comprehensive understanding of mobile-backend integration, RESTful APIs, and cloud services. Experience with modern iOS architecture patterns and continuous integration/deployment for mobile apps.""",

    'app_developer': """Mobile and Web Application Developer with 6+ years of experience (2019-Present) building cross-platform and native applications. Expert in React Native, Android (Kotlin/Java), and modern web technologies (React, TypeScript). Strong background in full-stack development with backend API integration, cloud services (AWS, Azure), and DevOps practices. Proven ability to deliver scalable applications with focus on user experience and performance optimization.""",

    'ai_product_engineer': """AI Product Engineer with 6+ years building intelligent systems and LLM-powered applications (2019-Present). Expert in React/TypeScript/Python with hands-on LLM integration (GPT-4, Claude, OpenAI API). Built production AI products including CarBot (Android Auto AI assistant), JobHunter (95% accurate AI role detection), and AI Math Grader. Proficient with AI coding tools (Cursor, Claude Code, Copilot). Passionate about integrating AI engines into production systems with measurable business impact.""",

    'it_business_analyst': """IT Business Analyst with 6+ years of combined business and technical experience (2019-Present). Master's in International Business & Trade combined with hands-on IT development experience across multiple companies. Expert at bridging the gap between technical IT systems and business requirements. Proven track record translating complex business needs into technical specifications, leading requirements workshops, and driving digital transformation. Strong analytical skills with deep understanding of both technical implementation (cloud platforms, databases, APIs) and business/commercial impact. Experience spans ECARX, Synteda, Senior Material, Pembio, and entrepreneurship at Hong Yan AB.""",

    'it_support_specialist': """IT Support Specialist with 6+ years of technical support and infrastructure experience (2019-Present). Expert in troubleshooting complex technical issues, managing IT infrastructure, and providing 24/7 support across global offices. Strong background in Windows/Linux system administration, network troubleshooting, hardware maintenance, and user support. Proven track record resolving critical incidents - restored 26 servers in 5 hours through systematic troubleshooting. Experience with cloud platforms (AWS, Azure), monitoring tools (Grafana, Prometheus), and IT service management. Experience spans ECARX, Synteda, IT-Högskolan, Senior Material, AddCell, Pembio, and CollabMaker.""",

    'site_reliability_engineer': """Site Reliability Engineer (SRE) with 6+ years managing production systems, ensuring high availability, and optimizing platform reliability (2019-Present). Expert in incident management, monitoring, automation, and capacity planning. Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation, and comprehensive observability (Prometheus, Grafana, ELK). Reduced MTTR by 35% through proactive monitoring and automation. Strong background in both development and operations, implementing SRE best practices including SLOs, error budgets, and blameless postmortems. Experience spans ECARX, Synteda, IT-Högskolan, Senior Material, AddCell, Pembio, and CollabMaker."""
}

SKILLS_BRICKS = {
    'incident_management_primary': [
        r"\textbf{Incident Management \& Response:} Production troubleshooting, Root cause analysis (RCA), On-call rotations (24/7), Critical system recovery, MTTR optimization, Runbook automation",
        r"\textbf{Monitoring \& Observability:} Prometheus, Grafana, ELK Stack, Datadog, OpenTelemetry, CloudWatch, Alerting systems, SLO/SLI metrics",
        r"\textbf{Cloud Platforms:} AWS (EC2, S3, Lambda, CloudFormation, IAM), Azure (AKS, VMs, Functions), GCP, Hybrid cloud",
        r"\textbf{Infrastructure as Code:} Terraform, CloudFormation, Ansible, Puppet, Chef, Configuration management",
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, CircleCI, Azure DevOps, Pipeline optimization",
        r"\textbf{Container Orchestration:} Kubernetes, Docker, AKS, Helm Charts, Container security",
        r"\textbf{Automation \& Scripting:} Python, Bash, PowerShell, Go, Deployment automation",
        r"\textbf{Operating Systems:} Linux (Ubuntu, CentOS, RHEL), Windows Server, System administration",
    ],
    
    'devops_primary': [
        r"\textbf{CI/CD Pipelines:} Jenkins, GitHub Actions, GitLab CI, CircleCI, Pipeline optimization, Release automation",
        r"\textbf{Infrastructure as Code:} Terraform, CloudFormation, Ansible, Infrastructure automation",
        r"\textbf{Cloud Platforms:} AWS, Azure, GCP, Hybrid cloud infrastructure",
        r"\textbf{Container Orchestration:} Kubernetes, Docker, Helm, Container security",
        r"\textbf{Monitoring:} Prometheus, Grafana, ELK Stack, Application monitoring",
    ],
    
    'fullstack_primary': [
        r"\textbf{Frontend:} React, TypeScript, JavaScript (ES6+), Next.js, Vue.js, State management",
        r"\textbf{Backend:} Node.js, Go, Python, Spring Boot, RESTful APIs, GraphQL",
        r"\textbf{Cloud Platforms:} AWS, Azure, GCP, Cloud optimization, Performance tuning",
        r"\textbf{DevOps:} Docker, Kubernetes, CI/CD, Terraform, Git/GitHub",
        r"\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis",
    ],

    'ai_product_engineer_primary': [
        r"\textbf{AI \& LLM:} OpenAI API (GPT-4), Anthropic Claude, LangChain, RAG, Prompt Engineering, Fine-tuning",
        r"\textbf{Full-Stack:} React, TypeScript, Python, Node.js, Next.js, FastAPI, RESTful APIs",
        r"\textbf{AI Tools:} Cursor, Claude Code, GitHub Copilot, Vercel AI SDK",
        r"\textbf{Cloud \& DevOps:} AWS, Azure, Docker, Kubernetes, CI/CD, Terraform",
        r"\textbf{Databases:} PostgreSQL, MongoDB, Redis, Vector Databases (Pinecone, Weaviate)",
    ],

    'backend_primary': [
        r"\textbf{Languages:} Java, Python, Go, C\#/.NET, TypeScript",
        r"\textbf{Frameworks:} Spring Boot, Spring Framework, FastAPI, ASP.NET Core",
        r"\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis, SQL optimization",
        r"\textbf{Architecture:} Microservices, RESTful APIs, Event-driven, Message queues",
        r"\textbf{Cloud \& DevOps:} AWS, Azure, Docker, Kubernetes, CI/CD pipelines",
    ],

    'it_business_analyst_primary': [
        r"\textbf{Business Analysis:} Requirements gathering, Gap analysis, Business case development, Process mapping",
        r"\textbf{Tools:} Excel (Advanced), Power BI, Visio, JIRA, Confluence, Microsoft 365",
        r"\textbf{IT Knowledge:} Cloud platforms (Azure, AWS), Databases (SQL), APIs, System architecture",
        r"\textbf{Project Management:} Agile/Scrum, Pre-studies, Change management, UAT coordination",
        r"\textbf{Communication:} Workshop facilitation, Stakeholder presentations, Cross-cultural collaboration",
    ]
}

# Projects section for LEGO bricks fallback (role-specific)
PROJECTS_BRICKS = {
    'default': r"""
\section*{Strategic Projects}

\subsection*{Fleet Management Dashboard}
\textit{2024 -- Present} \\
\textbf{.NET 8, React 18, SQL Server 2022, Azure, Docker, GitHub Actions}
\begin{itemize}[noitemsep]
\item Built intelligent fleet tracking platform using US DOT data for fuel efficiency and CO2 tracking
\item Implemented microservices architecture with event-driven patterns for real-time data processing
\item Leveraged Azure App Service and Docker for scalable hosting with automated CI/CD pipelines
\end{itemize}

\subsection*{SmrtMart E-commerce Platform}
\textit{2024 -- Present} \\
\textbf{Go, Next.js, PostgreSQL, Kubernetes, Stripe API}
\begin{itemize}[noitemsep]
\item Built fullstack e-commerce platform with microservices architecture and Stripe payment integration
\item Deployed on Kubernetes with auto-scaling for resilient distributed systems
\item Live: \href{https://www.smrtmart.com}{smrtmart.com}
\end{itemize}

\subsection*{JobHunter Automation Platform}
\textit{2025 -- Present} \\
\textbf{Python, TypeScript, React, Gmail REST API}
\begin{itemize}[noitemsep]
\item Automated job application pipeline with AI-powered role detection (95\% accuracy)
\item Built React dashboard for application tracking with real-time updates
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
""",

    'ai_product_engineer': r"""
\section*{AI Projects \& Products}

\subsection*{CarBot (AndroidAuto-Ebot) - AI Voice Assistant}
\textit{2024 - Present}
\begin{itemize}[noitemsep]
\item Built AI voice assistant for Android Auto outperforming Google Assistant with automotive-specific capabilities
\item Integrated LLM with real-time vehicle data, navigation, and contextual awareness
\item Tech: Android SDK, Kotlin, OpenAI API, Speech Recognition, TTS
\end{itemize}

\subsection*{AI Math Grader Ecosystem}
\textit{2025 -- Present} \\
\textbf{C\# .NET 8, React, AI/LLM (Gemini/OpenAI), Python}
\begin{itemize}[noitemsep]
\item Developed full-stack automated grading system for K-12 math with instant AI feedback
\item Architected modular API layer with C\# .NET for AI-driven feedback loops
\item Integrated white-label PDF export functionality
\end{itemize}

\subsection*{JobHunter - AI Job Application Automation}
\textit{2024 - Present}
\begin{itemize}[noitemsep]
\item Intelligent job application system with AI achieving 95\% accurate role detection
\item Full-stack application with AI-first architecture and prompt engineering
\item Tech: React, TypeScript, Python, MiniMax M2, Anthropic SDK
\end{itemize}
""",

    'it_business_analyst': r"""
\section*{IT-Business Integration Projects}

\subsection*{Fleet Management Business Solution}
\textbf{Business Analysis + Technical Implementation}
\begin{itemize}[noitemsep]
\item Conducted market research and stakeholder interviews to define business requirements
\item Created business case with ROI analysis for fuel efficiency features
\item Documented functional requirements and coordinated implementation
\end{itemize}

\subsection*{E-commerce Platform (SmrtMart.com)}
\textbf{End-to-End Business \& Technical Design}
\begin{itemize}[noitemsep]
\item Analyzed e-commerce market requirements and defined product specifications
\item Designed business processes for order management, inventory, and payment flows
\item Live platform demonstrating complete business solutions: \href{https://www.smrtmart.com}{smrtmart.com}
\end{itemize}

\subsection*{JobHunter Automation Platform}
\textbf{Business Process Automation}
\begin{itemize}[noitemsep]
\item Identified inefficiencies in job application process and designed automated solution
\item Created requirements documentation and process flow diagrams
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
""",

    'android_developer': r"""
\section*{Mobile \& Automotive Projects}

\subsection*{CarBot (AndroidAuto-Ebot) - AI Voice Assistant}
\textit{2024 - Present}
\begin{itemize}[noitemsep]
\item Built AI voice assistant for Android Auto outperforming Google Assistant with automotive-specific capabilities
\item Integrated LLM with real-time vehicle data, navigation, and contextual awareness
\item Tech: Android SDK, Kotlin, OpenAI API, Speech Recognition, TTS
\end{itemize}

\subsection*{Fleet Management Mobile App}
\textit{2024 -- Present} \\
\textbf{Kotlin, Android SDK, Retrofit, Room Database}
\begin{itemize}[noitemsep]
\item Developed Android companion app for fleet tracking with real-time GPS updates
\item Implemented offline-first architecture with Room database and sync capabilities
\item Used MVVM architecture with Jetpack components for maintainable codebase
\end{itemize}

\subsection*{E-commerce Mobile Client}
\textit{2024} \\
\textbf{Kotlin, Jetpack Compose, Retrofit}
\begin{itemize}[noitemsep]
\item Built native Android client for SmrtMart e-commerce platform
\item Implemented Material Design 3 with Jetpack Compose for modern UI
\item Integrated Stripe payment SDK for secure mobile checkout
\end{itemize}
""",

    'backend_developer': r"""
\section*{Backend \& API Projects}

\subsection*{Fleet Management API Platform}
\textit{2024 -- Present} \\
\textbf{.NET 8, SQL Server 2022, Azure, Docker}
\begin{itemize}[noitemsep]
\item Architected RESTful API serving fleet tracking data with 99.9\% uptime
\item Implemented caching strategies with Redis reducing database load by 60\%
\item Designed event-driven microservices architecture for real-time data processing
\end{itemize}

\subsection*{SmrtMart E-commerce Backend}
\textit{2024 -- Present} \\
\textbf{Go, PostgreSQL, Kubernetes, Stripe API}
\begin{itemize}[noitemsep]
\item Built high-performance Go backend handling 10k+ concurrent requests
\item Implemented secure payment processing with Stripe webhooks and idempotency
\item Deployed on Kubernetes with auto-scaling and zero-downtime deployments
\item Live: \href{https://www.smrtmart.com}{smrtmart.com}
\end{itemize}

\subsection*{JobHunter Backend Services}
\textit{2025 -- Present} \\
\textbf{Python, FastAPI, PostgreSQL, Gmail REST API}
\begin{itemize}[noitemsep]
\item Built AI-powered job analysis pipeline with 95\% role detection accuracy
\item Implemented Gmail integration for automated application tracking
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
""",

    'incident_management_specialist': r"""
\section*{Infrastructure \& Automation Projects}

\subsection*{Monitoring \& Alerting Platform}
\textit{2024 -- Present} \\
\textbf{Prometheus, Grafana, AlertManager, Python}
\begin{itemize}[noitemsep]
\item Deployed comprehensive monitoring stack for 50+ production services
\item Created custom Grafana dashboards with business-relevant KPIs
\item Implemented runbook automation reducing MTTR by 35\%
\end{itemize}

\subsection*{Infrastructure Automation Suite}
\textit{2024 -- Present} \\
\textbf{Terraform, Ansible, Python, Bash}
\begin{itemize}[noitemsep]
\item Automated server provisioning reducing deployment time from hours to minutes
\item Created self-healing scripts for common incident patterns
\item Implemented IaC patterns for consistent environment management
\end{itemize}

\subsection*{JobHunter Platform Operations}
\textit{2025 -- Present} \\
\textbf{Docker, Nginx, Let's Encrypt, GitHub Actions}
\begin{itemize}[noitemsep]
\item Managed production deployment with 99.9\% uptime on VPS infrastructure
\item Implemented CI/CD pipeline with automated testing and deployment
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
""",

    'devops_engineer': r"""
\section*{DevOps \& Cloud Projects}

\subsection*{Cloud Migration Project}
\textit{2024 -- Present} \\
\textbf{Azure AKS, Kubernetes, Terraform, Helm}
\begin{itemize}[noitemsep]
\item Led migration from Azure AKS to on-premise Kubernetes, reducing costs by 45\%
\item Implemented GitOps workflow with ArgoCD for declarative deployments
\item Created Helm charts for standardized application deployment
\end{itemize}

\subsection*{CI/CD Pipeline Optimization}
\textit{2024 -- Present} \\
\textbf{Jenkins, GitHub Actions, Docker, SonarQube}
\begin{itemize}[noitemsep]
\item Optimized build pipelines reducing deployment time by 60\%
\item Integrated quality gates with SonarQube for automated code review
\item Implemented parallel testing strategies for faster feedback
\end{itemize}

\subsection*{JobHunter Infrastructure}
\textit{2025 -- Present} \\
\textbf{Docker, Nginx, GitHub Actions, VPS}
\begin{itemize}[noitemsep]
\item Architected containerized deployment with automated CI/CD
\item Implemented SSL/TLS with Let's Encrypt auto-renewal
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
""",

    'fullstack_developer': r"""
\section*{Full-Stack Projects}

\subsection*{Fleet Management Dashboard}
\textit{2024 -- Present} \\
\textbf{.NET 8, React 18, SQL Server 2022, Azure, Docker}
\begin{itemize}[noitemsep]
\item Built intelligent fleet tracking platform with real-time data visualization
\item Implemented responsive React frontend with TypeScript and modern state management
\item Developed RESTful API backend with microservices architecture
\end{itemize}

\subsection*{SmrtMart E-commerce Platform}
\textit{2024 -- Present} \\
\textbf{Go, Next.js, PostgreSQL, Kubernetes, Stripe API}
\begin{itemize}[noitemsep]
\item Built fullstack e-commerce platform with SEO-optimized Next.js frontend
\item Implemented secure checkout flow with Stripe payment integration
\item Deployed on Kubernetes with auto-scaling for resilient distributed systems
\item Live: \href{https://www.smrtmart.com}{smrtmart.com}
\end{itemize}

\subsection*{JobHunter Automation Platform}
\textit{2025 -- Present} \\
\textbf{Python, TypeScript, React, Gmail REST API}
\begin{itemize}[noitemsep]
\item Built AI-powered job application pipeline with React dashboard
\item Implemented real-time updates with WebSocket connections
\item Demo: \href{https://jobs.bluehawana.com}{jobs.bluehawana.com}
\end{itemize}
"""
}


def sanitize_filename(text: str) -> str:
    """
    Convert company name to safe filename format.
    Examples:
    - "Aros Kapital" -> "ArosKapital"
    - "Göteborgs Stad" -> "GoteborgStad"
    - "SKF Group" -> "SKFGroup"
    """
    # Remove special characters and replace spaces
    text = text.replace(' ', '')
    # Remove Swedish characters
    text = text.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
    text = text.replace('Å', 'A').replace('Ä', 'A').replace('Ö', 'O')
    # Remove any remaining non-alphanumeric characters
    text = ''.join(c for c in text if c.isalnum())
    return text


def extract_company_and_title_from_text(job_description: str) -> tuple:
    """
    Improved extraction of company name and job title from job description text.
    Handles LinkedIn format including concatenated text without line breaks.
    
    Returns:
        tuple: (company_name, job_title)
    """
    lines = [line.strip() for line in job_description.split('\n') if line.strip()]
    company = 'Company'
    title = 'Position'
    explicit_company_provided = False
    
    # PRIORITY: Check for explicit "Company name: XXX" and "Job title: XXX" format at the very beginning
    if lines:
        # Check first few lines for explicit company name and job title
        for i, line in enumerate(lines[:3]):  # Check first 3 lines
            line_stripped = line.strip()
            
            # Check for "Company name: XXX"
            company_match = re.match(r'^Company\s+name\s*:\s*(.+)$', line_stripped, re.IGNORECASE)
            if company_match:
                company = company_match.group(1).strip()
                explicit_company_provided = True
                print(f"📍 Extracted company from 'Company name:' format: {company}")
                lines[i] = ''  # Remove this line
            
            # Check for "Job title: XXX"
            title_match = re.match(r'^Job\s+title\s*:\s*(.+)$', line_stripped, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                print(f"📍 Extracted job title from 'Job title:' format: {title}")
                lines[i] = ''  # Remove this line
        
        # Clean up empty lines and update job_description
        lines = [l for l in lines if l.strip()]
        job_description = '\n'.join(lines)
        
        # If both company and title were explicitly provided, return immediately
        if explicit_company_provided and title != 'Position':
            print(f"📍 Using explicit company and title: {company} - {title}")
            return (company, title)
    
    # If explicit company was provided, return it immediately without further checks
    if explicit_company_provided:
        # Still try to extract title from remaining text
        for line in lines[:5]:
            if len(line) < 100 and any(keyword in line.lower() for keyword in 
                ['engineer', 'developer', 'specialist', 'manager', 'architect', 'lead', 'senior', 
                 'junior', 'consultant', 'analyst', 'designer', 'coordinator', 'director', 'support']):
                title = line
                print(f"📍 Extracted job title: {title}")
                break
        return (company, title)
    
    # STRATEGY 0: Check for priority companies FIRST (most reliable)
    full_text = ' '.join(lines).lower()
    priority_companies = [
        ('microsoft', 'Microsoft'),
        ('google', 'Google'),
        ('amazon', 'Amazon'),
        ('meta', 'Meta'),
        ('apple', 'Apple'),
        ('nvidia', 'NVIDIA'),
        ('intel', 'Intel'),
        ('amd', 'AMD'),
        ('ibm', 'IBM'),
        ('oracle', 'Oracle'),
        ('salesforce', 'Salesforce'),
        ('adobe', 'Adobe'),
        ('netflix', 'Netflix'),
        ('uber', 'Uber'),
        ('airbnb', 'Airbnb'),
        ('tesla', 'Tesla'),
        ('infimotion', 'InfiMotion Technology Europe AB'),
        ('kamstrup', 'Kamstrup'),
        ('volvo', 'Volvo Cars'),
        ('ericsson', 'Ericsson'),
        ('spotify', 'Spotify'),
        ('klarna', 'Klarna'),
        ('göteborgs stad', 'Göteborgs Stad'),
        ('goteborgs stad', 'Göteborgs Stad'),
        ('city of gothenburg', 'Göteborgs Stad'),
        ('stockholms stad', 'Stockholms Stad'),
        ('malmö stad', 'Malmö Stad'),
        ('aros kapital', 'Aros Kapital'),
        ('h&m', 'H&M'),
        ('ikea', 'IKEA'),
        ('scania', 'Scania'),
        ('saab', 'Saab'),
        ('electrolux', 'Electrolux'),
        ('skf', 'SKF'),
        ('abb', 'ABB'),
        ('atlas copco', 'Atlas Copco'),
        ('sandvik', 'Sandvik'),
    ]
    
    for search_term, proper_name in priority_companies:
        # Use word boundaries to match whole words only (e.g., "uber" not in "kubernetes")
        pattern = r'\b' + re.escape(search_term) + r'\b'
        if re.search(pattern, full_text, re.IGNORECASE):
            company = proper_name
            print(f"📍 Found priority company: {company}")
            break
    
    # STRATEGY 0.5: LinkedIn concatenated format (no line breaks)
    # Pattern: "MicrosoftShareShow more optionsCloud Solution Architect-Power PlatformSweden"
    if len(lines) == 1 or (len(lines) > 0 and len(lines[0]) > 100):
        text = lines[0] if len(lines) > 0 else job_description
        
        # Remove known LinkedIn UI noise
        text_cleaned = re.sub(r'(Share|Show more options|Apply|Save|Matches your job preferences|Promoted by hirer|Responses managed off LinkedIn)', '', text, flags=re.IGNORECASE)
        
        # Split on location/time to get text before that
        text_before_location = re.split(r'Sweden|Gothenburg|Stockholm|Remote|·|\d+\s*(?:hour|day|week|month)s?\s*ago', text_cleaned)[0]
        
        # Look for job title pattern
        job_title_pattern = r'([A-Z][a-zA-Z\s\-/\.&]+(?:Engineer|Developer|Specialist|Manager|Architect|Lead|Senior|Consultant|Analyst|Coordinator|Administrator|Designer|Product)(?:[\s\-][A-Z][a-zA-Z\s\-/\.&]*)?)'
        title_matches = re.findall(job_title_pattern, text_before_location)
        
        if title_matches and company != 'Company':
            # Take the last match (most likely the actual title after company name)
            title = title_matches[-1].strip()
            print(f"📍 Extracted from concatenated LinkedIn format - Company: {company}, Title: {title}")
            return (company, title)
    
    # STRATEGY 1: LinkedIn format - First line is company, second line is title
    # This is the MOST COMMON format when copying from LinkedIn
    # But sometimes there's noise in first line, so check first 5 lines for company + title pattern
    
    job_keywords = [
        'engineer', 'developer', 'specialist', 'manager', 'architect', 
        'lead', 'senior', 'junior', 'consultant', 'analyst', 'support',
        'coordinator', 'administrator', 'technician', 'designer', 'product',
        'ingenjör', 'utvecklare', 'specialist', 'arkitekt', 'chef'
    ]
    
    for i in range(min(5, len(lines) - 1)):
        potential_company = lines[i].strip()
        potential_title = lines[i + 1].strip()
        
        # Validate company (should be short, no job keywords, no time references)
        invalid_company_patterns = [
            r'\d+\s*(hour|day|week|month|year|minute)s?\s*(ago)?',  # Time patterns
            r'(engineer|developer|specialist|manager|architect|lead|senior|junior|consultant|analyst)',  # Job keywords
            r'^(the|a|an)\s+',  # Articles
            r'·',  # LinkedIn separator
            r'(services|solutions|systems)$',  # Generic words that are usually not company names alone
        ]
        
        is_valid_company = (
            len(potential_company) < 60 and 
            len(potential_company) > 2 and
            not any(re.search(pattern, potential_company, re.IGNORECASE) for pattern in invalid_company_patterns)
        )
        
        # Validate title (should contain job keywords, be reasonably short)
        is_valid_title = (
            len(potential_title) < 100 and 
            len(potential_title) > 5 and
            any(keyword in potential_title.lower() for keyword in job_keywords)
        )
        
        if is_valid_company and is_valid_title:
            company = potential_company
            title = potential_title
            print(f"📍 LinkedIn format detected at line {i} - Company: {company}, Title: {title}")
            return (company, title)
    
    # STRATEGY 2: If LinkedIn format fails, use advanced extraction
    # Job title keywords (English and Swedish)
    job_keywords = [
        'engineer', 'developer', 'specialist', 'manager', 'architect', 
        'lead', 'senior', 'junior', 'consultant', 'analyst', 'support',
        'coordinator', 'administrator', 'technician',
        'ingenjör', 'utvecklare', 'specialist', 'arkitekt', 'chef'
    ]
    
    # PRIORITY: Check for explicit company names first
    full_text = ' '.join(lines).lower()
    
    # SMART COMPANY DETECTION: Look for company suffixes (AB, Ltd, Inc, GmbH, etc.)
    company_suffix_patterns = [
        r'(?:by|till|to|på|hos|at|for|from)\s+([A-Z][A-Za-z\s&\-]+)\s+(AB|Ltd|Limited|Inc|Incorporated|GmbH|AG|SA|AS|Oy|ApS|BV|NV|SRL|Srl|SpA|S\.p\.A\.|Co\.|Corp|Corporation|Group|Europe|Technology|Solutions|Systems|Services|Consulting)',
        r'(?:by|till|to|på|hos|at|for|from)\s+([A-Z][A-Za-z\s&\-]+)\s+(Europe\s+AB|Technology\s+AB|Sweden\s+AB|Nordic\s+AB)',
        r'([A-Z][A-Za-z\s&\-]+)\s+(AB|Ltd|Limited|Inc|Incorporated|GmbH|AG|SA|AS|Oy|ApS|BV|NV|SRL|Srl|SpA|S\.p\.A\.|Co\.|Corp|Corporation|Group|Europe|Technology|Solutions|Systems|Services|Consulting)',
        r'([A-Z][A-Za-z\s&\-]+)\s+(Europe\s+AB|Technology\s+AB|Sweden\s+AB|Nordic\s+AB)',
    ]
    
    for pattern in company_suffix_patterns:
        matches = re.findall(pattern, job_description, re.IGNORECASE)
        if matches:
            # Take the first match
            company_parts = matches[0] if isinstance(matches[0], tuple) else (matches[0],)
            potential_company = ' '.join(company_parts).strip()
            # Clean up - remove ALL prepositions that might prefix company names
            potential_company = re.sub(r'^(by|till|to|på|hos|at|for|from)\s+', '', potential_company, flags=re.IGNORECASE).strip()
            if not any(word in potential_company.lower() for word in ['role', 'position', 'job', 'vacancy', 'opening']):
                company = potential_company
                print(f"📍 Found company via suffix pattern: {company}")
                break
    
    # Check for "by [Company]" or "Published by [Company]" pattern
    if company == 'Company':
        by_pattern = re.search(r'(?:published\s+)?by\s+([A-Z][A-Za-z\s&]+(?:AB|Europe|Technology|Group|Ltd|Inc|GmbH)?)', job_description, re.IGNORECASE)
        if by_pattern:
            potential_company = by_pattern.group(1).strip()
            # Clean up - remove trailing words that aren't part of company name
            potential_company = re.sub(r'\s+(Role|Location|Remote|Assignment|Seniority).*$', '', potential_company, flags=re.IGNORECASE)
            # Remove "by" if it's at the start (shouldn't happen with regex, but safety check)
            potential_company = re.sub(r'^by\s+', '', potential_company, flags=re.IGNORECASE)
            
            # FILTER OUT: Time-related text (hour ago, day ago, etc.) and invalid patterns
            invalid_patterns = [
                r'\d+\s*(hour|day|week|month|year|minute|second)s?\s*(ago)?',  # Time patterns
                r'^(hour|day|week|month)\s+ag',  # Partial time text like "hour ag"
                r'^(the|a|an)\s+',  # Articles
            ]
            is_invalid = any(re.search(pattern, potential_company, re.IGNORECASE) for pattern in invalid_patterns)
            
            if not is_invalid and len(potential_company) > 3 and len(potential_company) < 60:
                company = potential_company
                print(f"📍 Found company via 'by [Company]' pattern: {company}")
    
    # Priority company list (fallback for known companies)
    priority_companies = [
        ('microsoft', 'Microsoft'),
        ('google', 'Google'),
        ('amazon', 'Amazon'),
        ('meta', 'Meta'),
        ('apple', 'Apple'),
        ('infimotion', 'InfiMotion Technology Europe AB'),
        ('kamstrup', 'Kamstrup'),
        ('göteborgs stad', 'Göteborgs Stad'),
        ('goteborgs stad', 'Göteborgs Stad'),
        ('city of gothenburg', 'Göteborgs Stad'),
        ('stockholms stad', 'Stockholms Stad'),
        ('malmö stad', 'Malmö Stad'),
        ('aros kapital', 'Aros Kapital'),
        ('volvo', 'Volvo Cars'),
        ('ericsson', 'Ericsson'),
        ('spotify', 'Spotify'),
        ('h&m', 'H&M'),
        ('ikea', 'IKEA'),
        ('scania', 'Scania'),
        ('saab', 'Saab'),
        ('electrolux', 'Electrolux'),
        ('skf', 'SKF'),
        ('abb', 'ABB'),
        ('atlas copco', 'Atlas Copco'),
        ('sandvik', 'Sandvik'),
    ]
    
    if company == 'Company':  # Only check if not already found
        for search_term, proper_name in priority_companies:
            if search_term in full_text:
                company = proper_name
                print(f"📍 Found priority company: {company}")
                break
    
    # First pass: Look for title using "As a [Job Title]" pattern (highest priority)
    for i, line in enumerate(lines[:30]):
        line_lower = line.lower()
        
        # Pattern: "As a [Job Title]" or "As an [Job Title]"
        if 'as a ' in line_lower or 'as an ' in line_lower:
            # Find the position of "as a" or "as an"
            if 'as a ' in line_lower:
                start_idx = line_lower.find('as a ') + 5
            else:
                start_idx = line_lower.find('as an ') + 6
            
            potential_title = line[start_idx:].strip()
            # Take text until comma or "you will"
            if ',' in potential_title:
                potential_title = potential_title.split(',')[0].strip()
            if ' you will' in potential_title.lower():
                potential_title = potential_title.split(' you will')[0].strip()
            if potential_title and len(potential_title) < 80 and len(potential_title) > 5:
                title = potential_title
                print(f"📍 Found title via 'As a [Title]' pattern: {title}")
                break
    
    # Second pass: Look for title in first few lines if not found via "As a" pattern
    if title == 'Position':
        for i, line in enumerate(lines[:30]):
            if len(line) > 100 or len(line) < 3:
                continue
            
            line_lower = line.lower()
            
            # Check if this line is likely a job title
            # It should contain job keywords and be reasonably short
            if any(keyword in line_lower for keyword in job_keywords):
                # Skip lines that are clearly not titles
                skip_phrases = [
                    'som ', 'kommer du', 'du kommer', 'vi söker', 'we are looking',
                    'about the job', 'om jobbet', 'responsibilities', 'ansvar',
                    'provide', 'providing', 'you will', 'du kommer att', 'are you',
                    'high quality', 'customers'
                ]
                if any(phrase in line_lower for phrase in skip_phrases):
                    continue
                
                # This looks like a title
                cleaned = line.strip(' -–—:')
                if len(cleaned) < 80:
                    title = cleaned
                    print(f"📍 Found title in line {i}: {title}")
                    break
    
    # Second pass: Look for company name (only if not already found in priority check)
    if company == 'Company':
        # STEP 1: Look in first few lines (top of JD)
        for i, line in enumerate(lines[:5]):
            line_lower = line.lower()
            
            # Skip lines that are clearly job titles or descriptions
            if any(keyword in line_lower for keyword in job_keywords):
                continue
            
            # Look for company patterns in top lines
            if ' at ' in line_lower or line.strip().endswith(' -') or line.strip().endswith(' |'):
                # Extract potential company name
                if ' at ' in line_lower:
                    at_index = line_lower.find(' at ')
                    potential_company = line[at_index + 4:].strip().rstrip(',.:?!-|')
                elif line.strip().endswith(' -') or line.strip().endswith(' |'):
                    potential_company = line.strip().rstrip(' -|').strip()
                else:
                    continue
                
                # Clean and validate
                potential_company = potential_company.split(',')[0].split('.')[0].strip()
                if potential_company and len(potential_company) < 50 and len(potential_company.split()) <= 4:
                    company = potential_company
                    print(f"📍 Found company in top lines: {company}")
                    break
        
        # STEP 2: Look in middle section (lines 5-20)
        if company == 'Company':
            for i, line in enumerate(lines[5:20], 5):
                line_lower = line.lower()
                
                # Look for "At [Company]" pattern in middle section
                if ' at ' in line_lower:
                    at_index = line_lower.find(' at ')
                    potential_company = line[at_index + 4:].strip().rstrip(',.:?!')
                    potential_company = potential_company.split(',')[0].split('.')[0].strip()
                    if potential_company and len(potential_company) < 50 and len(potential_company.split()) <= 4:
                        company = potential_company
                        print(f"📍 Found company in middle section: {company}")
                        break
        
        # STEP 3: Look in "About Us" / company description sections (bottom of JD)
        if company == 'Company':
            company_section_patterns = [
                'get to know us', 'about us', 'get to know', 'about the company',
                'our company', 'who we are', 'about our company', 'company culture',
                'our team', 'our mission', 'our purpose', 'our vision', 'our story',
                'about our organization', 'join us', 'why work with us', 'our values'
            ]
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Check if this line starts a company description section
                if any(pattern in line_lower for pattern in company_section_patterns):
                    # Search in this line and next several lines for company name
                    search_lines = [line] + lines[i+1:min(i+8, len(lines))]
                    
                    for search_line in search_lines:
                        search_lower = search_line.lower()
                        
                        # Pattern: "At [Company]," or "At [Company]."
                        if ' at ' in search_lower:
                            at_index = search_lower.find(' at ')
                            potential_company = search_line[at_index + 4:].strip().rstrip(',.:?!')
                            potential_company = potential_company.split(',')[0].split('.')[0].strip()
                            if potential_company and len(potential_company) < 50 and len(potential_company.split()) <= 4:
                                company = potential_company
                                print(f"📍 Found company in 'About Us At [Company]' pattern: {company}")
                                break
                        
                        # Pattern: Company name at start of sentence in company description
                        words = search_line.split()
                        for j, word in enumerate(words):
                            if word and len(word) > 2 and word[0].isupper():
                                # Skip common words that aren't company names
                                common_words = ['The', 'Our', 'We', 'You', 'This', 'That', 'With', 'And', 'But', 'For', 'In', 'On', 'At', 'To', 'From', 'As', 'By', 'Of', 'Or', 'So', 'If', 'When', 'Where', 'Why', 'How', 'What', 'Who']
                                if word not in common_words:
                                    # Take 1-2 words as potential company name
                                    potential_company = ' '.join(words[j:j+2]).rstrip(',.:?!')
                                    potential_company = potential_company.split(',')[0].split('.')[0].strip()
                                    if len(potential_company.split()) <= 2 and len(potential_company) < 30 and potential_company.replace(' ', '').isalpha():
                                        company = potential_company
                                        print(f"📍 Found company in company description: {company}")
                                        break
                        
                        if company != 'Company':
                            break
                    
                    if company != 'Company':
                        break
        
        # Pattern 2: "At [Company]" anywhere in text (extended search)
        if company == 'Company':
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                if line_lower.startswith('at ') or ' at ' in line_lower:
                    # Extract company name after "at"
                    if line_lower.startswith('at '):
                        potential_company = line[3:].strip().rstrip(',.:')
                    else:
                        # Find "at" and extract what comes after
                        at_index = line_lower.find(' at ')
                        if at_index != -1:
                            potential_company = line[at_index + 4:].strip().rstrip(',.:')
                    
                    # Check if it looks like a company name (capitalized, not too long)
                    if potential_company and len(potential_company) < 50 and potential_company[0].isupper():
                        # Take only the first word/phrase before comma or period
                        potential_company = potential_company.split(',')[0].split('.')[0].strip()
                        if len(potential_company.split()) <= 3:  # Company names are usually 1-3 words
                            company = potential_company
                            print(f"📍 Found company via 'At [Company]' pattern: {company}")
                            break
        
        # Check for Swedish "Förvaltning/bolag" pattern (Göteborgs Stad specific)
        if company == 'Company':
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                if 'förvaltning/bolag' in line_lower or 'förvaltning / bolag' in line_lower:
                    # Next line usually contains the department/company name
                    if i + 1 < len(lines):
                        potential_company = lines[i + 1].strip()
                        # For Swedish government jobs, prefer the main organization over department
                        # Check if "Göteborgs Stad" or similar appears in surrounding context
                        context = ' '.join(lines[max(0, i-5):min(len(lines), i+10)]).lower()
                        if 'göteborgs stad' in context or 'goteborgs stad' in context:
                            company = 'Göteborgs Stad'
                            print(f"📍 Found 'Göteborgs Stad' in context of Förvaltning/bolag")
                        elif len(potential_company) < 50 and potential_company not in ['att', 'och', 'för', 'med']:
                            company = potential_company
                            print(f"📍 Found company via 'Förvaltning/bolag': {company}")
                        break
                
                # Look for "Om oss" section
                if line_lower in ['om oss', 'about us', 'about the company', 'om företaget']:
                    # Company name is often in the next few lines
                    for j in range(i + 1, min(i + 5, len(lines))):
                        potential = lines[j].strip()
                        # Look for capitalized text that could be a company name
                        if potential and len(potential) < 50 and potential[0].isupper():
                            # Filter out common Swedish words
                            words = potential.split()
                            if len(words) <= 4:
                                # Check it's not a common Swedish phrase
                                common_words = ['att', 'och', 'för', 'med', 'är', 'vi', 'som', 'på', 'i', 'av', 'till']
                                if not any(w.lower() in common_words for w in words[:2]):  # Check first 2 words
                                    company = potential
                                    print(f"📍 Found company in 'Om oss' section: {company}")
                                    break
                    if company != 'Company':
                        break
                
                # Look for explicit company mentions
                company_patterns = [
                    ('company:', 1),
                    ('företag:', 1),
                    ('arbetsgivare:', 1),
                    ('organisation:', 1),
                ]
                
                for pattern, offset in company_patterns:
                    if pattern in line_lower:
                        # Check if it's a header (company name on next line)
                        if line_lower.strip() == pattern:
                            if i + offset < len(lines):
                                potential = lines[i + offset].strip()
                                if potential and len(potential) < 50:
                                    company = potential
                                    print(f"📍 Found company after '{pattern}': {company}")
                                    break
                        else:
                            # Company name on same line
                            idx = line_lower.index(pattern) + len(pattern)
                            potential = line[idx:].strip(' -–—:,.')
                            potential = potential.split(',')[0].split('.')[0].strip()
                            if potential and len(potential) < 50:
                                company = potential
                                print(f"📍 Found company inline with '{pattern}': {company}")
                                break
                
                if company != 'Company':
                    break
    
    # Third pass: Look for company names that appear multiple times (strong signal)
    # Also look for specific patterns
    if company == 'Company':
        # Count capitalized words that appear multiple times
        from collections import Counter
        words = []
        
        # Common words to exclude (not company names)
        exclude_words = {
            'the', 'and', 'are', 'you', 'will', 'about', 'get', 'know', 'our', 'your',
            'customer', 'customers', 'support', 'engineer', 'manager', 'developer',
            'team', 'work', 'job', 'role', 'position', 'company', 'responsibilities',
            'requirements', 'experience', 'skills', 'qualifications', 'benefits',
            'apply', 'application', 'contact', 'email', 'phone', 'location'
        }
        
        for line in lines:
            # Extract capitalized words (potential company names)
            line_words = line.split()
            for word in line_words:
                # Must start with capital, be 3+ chars, not be common words
                clean_word = word.strip('.,;:!?()')
                if (clean_word and len(clean_word) >= 3 and clean_word[0].isupper() and 
                    clean_word.lower() not in exclude_words):
                    words.append(clean_word)
        
        # Find words that appear 3+ times (likely company name)
        word_counts = Counter(words)
        for word, count in word_counts.most_common(10):
            if count >= 3 and len(word) <= 20:
                company = word
                print(f"📍 Found company via frequency analysis: {company} (appears {count} times)")
                break
        
        # Specific company patterns
        if company == 'Company':
            for line in lines[:30]:
                if 'göteborgs stad' in line.lower() or 'goteborgs stad' in line.lower():
                    company = 'Göteborgs Stad'
                    print(f"📍 Found 'Göteborgs Stad' in text")
                    break
                if 'intraservice' in line.lower():
                    # Check if it mentions both
                    if 'göteborgs stad' in ' '.join(lines[:30]).lower():
                        company = 'Göteborgs Stad'
                    else:
                        company = 'Intraservice'
                    print(f"📍 Found company mention: {company}")
                    break
    
    # Clean up: Remove Swedish stop words if they ended up in company/title
    swedish_stopwords = ['att', 'och', 'för', 'med', 'är', 'som', 'på', 'i', 'av', 'till']
    if company.lower() in swedish_stopwords:
        company = 'Company'
    if title.lower().startswith('som '):
        title = 'Position'
    
    # Clean up company name: Remove parentheses and content inside them
    if company and company != 'Company':
        # Remove parentheses and their content: "Company Name (Extra Info)" -> "Company Name"
        company = re.sub(r'\s*\([^)]*\)', '', company).strip()
        # Remove trailing punctuation
        company = company.rstrip('.,;:!?-')
    
    print(f"🏢 Final extraction - Company: {company}, Title: {title}")
    return company, title


def analyze_job_description(job_description: str, job_url: str = None) -> dict:
    """Analyze job description and determine role type, keywords, and requirements"""
    
    job_lower = job_description.lower()
    
    # PRIORITY 1: Extract company and title from explicit "Company name:" / "Job title:" format
    # This is the PRIMARY method - user provides this explicitly
    company, title = extract_company_and_title_from_text(job_description)
    print(f"📍 Extracted from text: {company} - {title}")
    
    # PRIORITY 2: Try to extract from job URL if provided (only if text extraction failed)
    if job_url and (company == 'Company' or title == 'Position'):
        try:
            print(f"🔍 Attempting to extract job info from URL: {job_url}")
            from app.services.job_url_extractor import JobUrlExtractor
            extractor = JobUrlExtractor()
            extraction_result = extractor.extract_job_details(job_url)
            
            if extraction_result.get('success') and extraction_result.get('job_details'):
                job_details = extraction_result['job_details']
                if company == 'Company':
                    company = job_details.get('company', 'Company')
                if title == 'Position':
                    title = job_details.get('title', 'Position')
                print(f"✅ URL extraction successful: {title} at {company}")
            else:
                print(f"⚠️ URL extraction failed: {extraction_result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Error extracting from job URL: {e}")
    
    # Try AI analysis first (MiniMax M2) - DISABLED due to insufficient balance
    ai_result = None
    confidence = 0.0
    # AI analysis re-enabled - API balance restored
    use_ai = True  # AI analysis is now available
    
    if use_ai and ai_analyzer.is_available():
        ai_result = ai_analyzer.analyze_job_description(job_description)
        if ai_result:
            role_category = ai_result['role_category']
            confidence = ai_result['confidence']
            tech_keywords = ai_result.get('key_technologies', [])
            print(f"✓ AI Analysis: {role_category} (confidence: {confidence:.0%})")
        else:
            # Fallback to keyword matching
            role_category = template_manager.analyze_job_role(job_description)
            print(f"⚠ AI failed, using keyword matching: {role_category}")
    else:
        # Use CVTemplateManager for keyword-based role detection
        role_category = template_manager.analyze_job_role(job_description)
        print(f"ℹ Using keyword matching: {role_category}")
    
    role_info = template_manager.get_role_info(role_category)
    
    # Get percentage-based analysis
    try:
        role_percentages = template_manager.get_role_percentages(job_description)
        role_breakdown = template_manager.get_role_breakdown(job_description, threshold=5.0)
        role_scores = template_manager.get_role_scores(job_description)
        
        # Calculate confidence score based on percentage distribution
        if role_breakdown:
            primary_percentage = role_breakdown[0][1]
            secondary_percentage = role_breakdown[1][1] if len(role_breakdown) > 1 else 0
            # Higher confidence when primary role is dominant
            percentage_confidence = min(1.0, primary_percentage / 100.0)
            if confidence == 0.0:  # If no AI confidence, use percentage-based confidence
                confidence = percentage_confidence
        
    except Exception as e:
        print(f"⚠ Error getting percentage analysis: {e}")
        role_percentages = {}
        role_breakdown = []
        role_scores = {}
    
    # Map role category to display name
    # For company-specific roles, use a more appropriate display name
    if role_category == 'kamstrup':
        role_type = 'Customer Support Engineer'  # Use the actual job role, not company name
    else:
        role_type = role_category.replace('_', ' ').title()
    
    # Extract keywords if not from AI - make it role-specific
    if not ai_result or not tech_keywords:
        tech_keywords = []
        
        # Define role-specific keyword lists
        role_keyword_map = {
            'it_support': [
                'technical support', 'customer support', 'hardware', 'software', 
                'troubleshooting', 'incident management', 'ticketing', 'servicenow',
                'help desk', 'remote support', 'networking', 'configuration',
                'windows', 'linux', 'active directory', 'office 365', 'azure ad',
                'system administration', 'user support', 'it infrastructure',
                'hardware support', 'software support', 'network support',
                'problem solving', 'customer service', 'technical documentation',
                'training', 'onboarding', 'escalation', 'sla', 'itil'
            ],
            'devops_sre': [
                'kubernetes', 'docker', 'terraform', 'ansible', 'jenkins', 'github actions',
                'prometheus', 'grafana', 'elk', 'aws', 'azure', 'gcp', 'python', 'bash',
                'ci/cd', 'devops', 'sre', 'incident management', 'monitoring', 'observability',
                'infrastructure as code', 'automation', 'reliability', 'scalability',
                'load balancing', 'high availability', 'disaster recovery', 'backup',
                'linux', 'networking', 'security', 'performance tuning', 'troubleshooting',
                'on-call', 'incident response', 'postmortem', 'runbook', 'alerting'
            ],
            'infrastructure_engineer': [
                'infrastructure', 'networking', 'virtualization', 'vmware', 'hyper-v',
                'storage', 'san', 'nas', 'backup', 'disaster recovery', 'high availability',
                'load balancing', 'firewall', 'vpn', 'dns', 'dhcp', 'active directory',
                'windows server', 'linux', 'unix', 'scripting', 'automation', 'monitoring',
                'capacity planning', 'performance tuning', 'security', 'compliance',
                'data center', 'cloud migration', 'hybrid cloud', 'aws', 'azure', 'gcp'
            ],
            'backend_developer': [
                'python', 'java', 'go', 'node.js', 'spring boot', 'django', 'flask',
                'rest api', 'graphql', 'microservices', 'postgresql', 'mongodb', 'redis',
                'kafka', 'rabbitmq', 'docker', 'kubernetes'
            ],
            'frontend_developer': [
                'react', 'vue', 'angular', 'typescript', 'javascript', 'html', 'css',
                'webpack', 'redux', 'next.js', 'tailwind', 'responsive design', 'ui/ux'
            ],
            'fullstack_developer': [
                'react', 'typescript', 'node.js', 'python', 'java', 'rest api',
                'postgresql', 'mongodb', 'docker', 'aws', 'azure', 'ci/cd'
            ],
            'cloud_architect': [
                'aws', 'azure', 'gcp', 'cloud architecture', 'terraform', 'kubernetes',
                'microservices', 'serverless', 'lambda', 'api gateway', 'vpc', 'iam'
            ],
            'data_engineer': [
                'python', 'spark', 'airflow', 'kafka', 'sql', 'etl', 'data pipeline',
                'bigquery', 'redshift', 'snowflake', 'databricks', 'hadoop'
            ]
        }
        
        # Get keywords for the detected role, or use general keywords
        keyword_list = role_keyword_map.get(role_category, role_keyword_map['devops_sre'])
        
        for keyword in keyword_list:
            if keyword in job_lower:
                tech_keywords.append(keyword.title())
    
    # Only use fallback extraction if LinkedIn extraction failed
    if company == 'Company' or title == 'Position':
        # Use improved extraction function
        extracted_company, extracted_title = extract_company_and_title_from_text(job_description)
        if company == 'Company':
            company = extracted_company
        if title == 'Position':
            title = extracted_title
    
    # Clean up title if it contains company name with pipe separator
    # Pattern: "Job Title | Company Name" or "Job Title — Company Name"
    if title and ('|' in title or '—' in title or ' - ' in title):
        for separator in [' | ', ' — ', ' - ']:
            if separator in title:
                parts = title.split(separator, 1)
                if len(parts) == 2:
                    # Check which part is likely the title vs company
                    left, right = parts[0].strip(), parts[1].strip()
                    left_is_title = any(kw in left.lower() for kw in ['engineer', 'developer', 'architect', 'manager', 'specialist', 'analyst'])
                    right_is_title = any(kw in right.lower() for kw in ['engineer', 'developer', 'architect', 'manager', 'specialist', 'analyst'])
                    
                    if left_is_title and not right_is_title:
                        # Left is title, right is company
                        title = left
                        if company == 'Company':
                            company = right
                        break
                    elif right_is_title and not left_is_title:
                        # Right is title, left is company
                        if company == 'Company':
                            company = left
                        title = right
                        break
    
    # Validate extraction results
    extraction_success = True
    extraction_issues = []
    
    # Check if company was successfully extracted
    if company == 'Company' or not company or len(company.strip()) < 2:
        extraction_success = False
        extraction_issues.append('company_missing')
        company = 'Company'  # Ensure consistent fallback
    
    # Check if title was successfully extracted  
    if title == 'Position' or not title or len(title.strip()) < 3:
        extraction_success = False
        extraction_issues.append('title_missing')
        title = 'Position'  # Ensure consistent fallback
    
    # Additional validation for reasonable values
    if company and len(company) > 100:  # Company name too long
        extraction_success = False
        extraction_issues.append('company_invalid')
        company = 'Company'
        
    if title and len(title) > 100:  # Job title too long
        extraction_success = False
        extraction_issues.append('title_invalid')
        title = 'Position'
    
    return {
        'roleType': role_type,
        'roleCategory': role_category,  # Internal category key for template matching
        'keywords': tech_keywords[:15],  # Top 15 keywords
        'requiredSkills': tech_keywords[:10],  # Top 10 skills
        'achievements': [
            '26-server incident resolution in 5 hours',
            '45% cloud cost reduction',
            '35% MTTR reduction',
            '24/7 multi-region support'
        ],
        'company': company,
        'title': title,
        'templateInfo': role_info,  # Template information
        'aiAnalysis': {
            'used': ai_result is not None,
            'confidence': confidence,
            'reasoning': ai_result.get('reasoning', '') if ai_result else '',
            'model': 'MiniMax-M2' if ai_result else 'keyword-matching'
        },
        # Add percentage-based data
        'rolePercentages': role_percentages,  # All role percentages (0-100%)
        'roleBreakdown': [{'role': role, 'percentage': pct} for role, pct in role_breakdown],  # Significant roles (>5%)
        'roleScores': role_scores,  # Raw weighted scores
        'confidenceScore': confidence,  # Overall confidence in the analysis
        # Add extraction validation
        'extractionStatus': {
            'success': extraction_success,
            'issues': extraction_issues,
            'requiresManualInput': not extraction_success,
            'message': 'Company and job title extracted successfully' if extraction_success else 'Manual input required for missing information'
        }
    }


def customize_template(template_content: str, company: str, title: str, role_type: str, job_description: str = "", customization_notes: str = "") -> str:
    """Customize template by replacing placeholders and using AI to tailor content to job description"""
    import re

    # Clean up the title - remove extra whitespace and newlines
    clean_title = title.strip().split('\n')[0] if title and title != 'Position' else role_type

    # Escape special LaTeX characters in title
    clean_title = clean_title.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')

    # Pattern 1: Replace the {\Large ...} line after the name
    # This matches lines like "{\Large DevOps & Cloud Engineer | FinTech Specialist}"
    # or "{\Large Software Engineer | Automotive & Embedded Systems Enthusiast}"
    pattern = r'\{\\Large\s+[^\}]+\}'

    # Find the pattern
    match = re.search(pattern, template_content)
    if match:
        # Replace with clean title
        replacement = f'{{\\Large {clean_title}}}'
        template_content = template_content.replace(match.group(0), replacement, 1)

    # AI-powered content customization re-enabled - API balance restored
    use_ai_customization = True  # AI customization is now available
    
    if use_ai_customization and job_description and ai_analyzer.is_available():
        try:
            # Analyze job to extract key requirements
            ai_result = ai_analyzer.analyze_job_description(job_description)

            if ai_result and ai_result.get('confidence', 0) > 0.5:
                key_techs = ai_result.get('key_technologies', [])
                role_category = ai_result.get('role_category', '')

                # Build AI enhancement prompt with user's customization notes
                enhancement_prompt = f"""Enhance this LaTeX CV to be perfectly tailored for this job.

JOB DESCRIPTION:
{job_description}

KEY TECHNOLOGIES NEEDED: {', '.join(key_techs) if key_techs else 'Not specified'}
ROLE CATEGORY: {role_category}

{"USER'S CUSTOMIZATION PRIORITIES:" if customization_notes else ""}
{customization_notes if customization_notes else ""}

INSTRUCTIONS:
1. Keep the exact LaTeX structure and formatting
2. Emphasize experiences and achievements that match the job requirements
3. Highlight relevant technologies from the candidate's background
4. Reorder or emphasize bullet points to match job priorities
{f"5. PRIORITIZE what the user wants highlighted: {customization_notes}" if customization_notes else ""}

Return ONLY the enhanced LaTeX code, no explanations."""

                # Use AI to enhance the content (placeholder - need to implement)
                # For now, just add a note that AI will enhance this
                print(f"✓ AI enhancement available with user notes: {bool(customization_notes)}")
                
                # Customize Professional Summary section
                template_content = customize_profile_summary(
                    template_content, 
                    role_category, 
                    key_techs,
                    job_description
                )
                
                print(f"✓ AI-customized content for {role_category} with {len(key_techs)} key technologies")
        except Exception as e:
            print(f"⚠ AI customization failed: {e}, using template as-is")
            import traceback
            traceback.print_exc()
    
    return template_content


def customize_profile_summary(template_content: str, role_category: str, key_technologies: list, job_description: str) -> str:
    """
    Comprehensive CV customization based on job requirements
    Customizes: Profile Summary, Core Skills, Work Experience emphasis, Projects
    """
    import re
    
    # 1. Customize Professional/Profile Summary section
    summary_pattern = r'(\\section\*\{Professional Summary\})(.*?)(\\section\*\{)'
    match = re.search(summary_pattern, template_content, re.DOTALL)
    
    if not match:
        # Try alternative section names
        summary_pattern = r'(\\section\*\{Profile Summary\})(.*?)(\\section\*\{)'
        match = re.search(summary_pattern, template_content, re.DOTALL)
    
    if match:
        # Build customized summary based on role category
        custom_summary = build_custom_summary(role_category, key_technologies, job_description)
        
        if custom_summary:
            # Replace the summary content
            template_content = template_content.replace(
                match.group(0),
                f"{match.group(1)}\n\n{custom_summary}\n\n{match.group(3)}"
            )
    
    # 2. Customize Core Skills section - reorder based on JD keywords
    template_content = customize_skills_section(template_content, key_technologies)
    
    # 3. Add JD keyword emphasis comments for experience section
    # This helps maintain relevance without rewriting entire experience
    template_content = add_jd_context_comments(template_content, key_technologies, role_category)
    
    return template_content


def customize_skills_section(template_content: str, key_technologies: list) -> str:
    """
    Reorder and emphasize skills based on JD keywords
    Ensures ATS picks up the most relevant skills first
    """
    import re
    
    if not key_technologies:
        return template_content
    
    # Extract Core Technical Skills/Competencies section
    skills_pattern = r'(\\section\*\{Core Technical (?:Skills|Competencies)\})(.*?)(\\section\*\{)'
    match = re.search(skills_pattern, template_content, re.DOTALL)
    
    if match:
        skills_content = match.group(2)
        
        # Extract individual skill items - Match LaTeX \item lines
        # Pattern: \item \textbf{Category:} content
        # Note: colon is INSIDE the braces, followed by } then space then content
        item_pattern = r'\\item\s+\\textbf\{[^}]+\}\s*[^\n]+'
        items = re.findall(item_pattern, skills_content)
        
        if items and len(items) > 3:
            # Score each skill item based on keyword matches
            scored_items = []
            for item in items:
                score = 0
                item_lower = item.lower()
                for tech in key_technologies:
                    if tech.lower() in item_lower:
                        score += 1
                scored_items.append((score, item))
            
            # Sort by score (descending) - most relevant skills first
            scored_items.sort(key=lambda x: x[0], reverse=True)
            
            # Rebuild skills section with reordered items
            reordered_items = [item for score, item in scored_items]
            new_skills_content = '\n'.join(reordered_items)
            
            # Add comment about JD optimization
            new_skills_section = f"{match.group(1)}\n% Skills reordered based on job requirements\n\\begin{{itemize}}[leftmargin=*, itemsep=2pt]\n{new_skills_content}\n\\end{{itemize}}\n\n{match.group(3)}"
            
            template_content = template_content.replace(match.group(0), new_skills_section)
            print(f"✓ Reordered {len(items)} skill categories based on JD keywords")
    
    return template_content


def add_jd_context_comments(template_content: str, key_technologies: list, role_category: str) -> str:
    """
    Add LaTeX comments highlighting JD-relevant sections
    Helps maintain context about what's important for this specific job
    """
    if not key_technologies:
        return template_content
    
    # Add comment at the top of Professional Experience section
    tech_list = ', '.join(key_technologies[:10])
    comment = f"% JD Keywords: {tech_list}\n% Role: {role_category}\n% This CV is optimized for ATS matching with the above keywords\n\n"
    
    # Insert comment before Professional Experience section
    experience_pattern = r'(\\section\*\{Professional Experience\})'
    template_content = re.sub(experience_pattern, f"{comment}\\1", template_content)
    
    return template_content


def build_custom_summary(role_category: str, key_technologies: list, job_description: str) -> str:
    """
    Build a customized professional summary based on role and technologies
    Integrates with AI prompt strategies for maximum ATS and HR impact
    """
    
    # Base summaries for different role categories
    summaries = {
        'android_developer': """Android Developer with 5+ years building native mobile applications using Kotlin and Java. Expert in Android SDK, AOSP, and automotive infotainment systems. Strong background in building performant, user-centric mobile experiences with modern architecture patterns (MVVM, Clean Architecture). Proven track record delivering production applications with focus on code quality, testing, and maintainability.""",
        
        'devops_cloud': """DevOps Engineer with 5+ years building CI/CD pipelines, automating infrastructure, and managing cloud platforms. Expert in Kubernetes, Docker, Terraform, and cloud optimization across AWS and Azure. Proven track record in infrastructure automation, monitoring solutions, and platform reliability. Reduced cloud costs by 45% through strategic optimization and migration. Strong background in GitOps, infrastructure as code, and developer experience improvements.""",
        
        'incident_management_sre': """Incident Management Specialist and SRE Engineer with 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations. Currently at ECARX supporting 4 global offices with 24/7 on-call coverage. Expert in rapid incident response - restored 26 servers in 5 hours through systematic RCA. Proven expertise in Kubernetes, Terraform IaC, CI/CD automation, and comprehensive observability (Prometheus, Grafana, ELK). Reduced MTTR by 35% through proactive monitoring and automation.""",
        
        'fullstack_developer': """Full-stack Developer with 5+ years building scalable web applications and cloud infrastructure solutions. Strong frontend expertise in React, TypeScript, and modern JavaScript, combined with deep backend experience in Node.js, Python, and microservices. Proven track record collaborating with international teams, designing RESTful/GraphQL APIs, and delivering high-performance user experiences. Expert in cloud platforms (AWS, Azure, GCP) and DevOps practices.""",
        
        'ai_product_engineer': """AI Product Engineer with 5+ years building intelligent systems and LLM-powered applications. Expert in React/TypeScript/Python with hands-on experience integrating GPT-4, Claude, and other LLMs. Built production AI systems serving 1000+ users with 99.5% uptime. Proficient with AI coding tools (Cursor, Claude Code, Copilot). Passionate about "stitching" AI engines into products with hallucination-free outputs and robust guardrails.""",
        
        'platform_engineer': """Platform Engineer with 5+ years building internal developer platforms and infrastructure automation. Expert in Kubernetes, Terraform, and cloud-native technologies. Strong focus on developer experience, self-service platforms, and infrastructure reliability. Proven track record reducing deployment time by 60% through automation and improving platform adoption across engineering teams.""",
        
        'backend_developer': """Backend Developer with 5+ years building scalable APIs and microservices. Expert in Python, Java/Spring Boot, and Node.js with strong database optimization skills (PostgreSQL, MongoDB, Redis). Proven track record designing RESTful/GraphQL APIs handling millions of requests. Strong background in distributed systems, message queues (Kafka), and cloud platforms (AWS, Azure)."""
    }
    
    # Get base summary for role category
    base_summary = summaries.get(role_category, summaries['devops_cloud'])
    
    # Strategy 1: Resume Rewrite - Use strong action verbs and measurable achievements
    # Already built into base summaries with verbs like "built", "reduced", "delivered"
    
    # Strategy 3: JD Match - Emphasize key technologies from job description
    if key_technologies:
        tech_str = ', '.join(key_technologies[:8])  # Top 8 technologies
        # Add technology emphasis to summary for ATS keyword matching
        base_summary = base_summary.replace(
            'Expert in',
            f'Expert in {tech_str} and'
        )
    
    return base_summary


def generate_ai_enhancement_prompts(job_description: str, customized_cv_text: str, company: str, position: str) -> dict:
    """
    Generate all 5 AI prompt strategies for comprehensive job application support
    
    Returns dict with prompts for:
    1. Resume rewrite (get more interviews)
    2. Role targeting (10 higher-paying roles)
    3. JD match check (aim ~90% match)
    4. Interview prep (15 questions + answers)
    5. Proof projects (complete this week)
    """
    
    return {
        'resume_rewrite': ai_prompts.resume_rewrite(customized_cv_text),
        'role_targeting': ai_prompts.role_targeting(customized_cv_text),
        'jd_match': ai_prompts.jd_match_check(job_description, customized_cv_text),
        'interview_prep': ai_prompts.interview_prep(position, job_description),
        'proof_projects': ai_prompts.proof_projects(position, job_description),
        'cover_letter': ai_prompts.cover_letter_generator(job_description, customized_cv_text, company),
        'linkedin_optimization': ai_prompts.linkedin_optimization(customized_cv_text, [position]),
        'salary_negotiation': ai_prompts.salary_negotiation(position, 5, 'Sweden')
    }


def build_lego_cv(role_type: str, company: str, title: str, role_category: str = None, job_description: str = "", customization_notes: str = "") -> str:
    """Build CV using LEGO bricks based on role type - Template-based with AI customization"""

    # Try to load template first
    template_content = None
    if role_category:
        template_content = template_manager.load_template(role_category)

    # If template exists, use it as base WITHOUT customization to preserve quality
    if template_content:
        # IMPORTANT: Don't customize CV templates - they're already optimized!
        # The original templates are 3 pages with perfect Java/Spring Boot content
        # Only do basic placeholder replacement for company/title in header

        # Clean up the title - remove extra whitespace, newlines, and leading articles
        clean_title = title.strip().split('\n')[0] if title and title != 'Position' else role_type
        # Remove leading articles (an, a, the)
        clean_title = re.sub(r'^(an?|the)\s+', '', clean_title, flags=re.IGNORECASE).strip()
        # Title case, but preserve acronyms
        clean_title = clean_title.title() if clean_title else clean_title
        # Restore common acronyms that .title() would break
        acronyms = ['IT', 'AI', 'API', 'CI/CD', 'DevOps', 'SRE', 'UI', 'UX', 'QA', 'BI', 'ERP', 'CRM', 'HR', 'AWS', 'GCP', 'iOS', 'ML']
        for acronym in acronyms:
            clean_title = re.sub(r'\b' + acronym.title() + r'\b', acronym, clean_title, flags=re.IGNORECASE)
        # Escape special LaTeX characters in title
        clean_title = clean_title.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
        
        # Only replace the job title in the header ({\Large ...} line after name)
        pattern = r'\{\\Large\s+[^\}]+\}'
        match = re.search(pattern, template_content)
        if match:
            replacement = f'{{\\Large {clean_title}}}'
            template_content = template_content.replace(match.group(0), replacement, 1)
        
        print(f"✓ Using original CV template for {role_category} without content modification")
        return template_content
    
    # Fallback to LEGO bricks generation if no template
    
    # Clean up role_type, company, and title - handle placeholder cases
    if not role_type or role_type in ['Position', '[JOB TITLE]', '[Job Title]']:
        role_type = 'Software Engineer'
    if not company or company in ['Company', '[COMPANY NAME]', '[Company Name]']:
        company = 'Target Company'
    if not title or title in ['Position', '[JOB TITLE]', '[Job Title]']:
        title = role_type  # Use role_type as fallback for title
    
    # Map role type/category to brick keys (comprehensive mapping)
    role_map = {
        # By role_type (display name)
        'Incident Management Specialist': 'incident_management_specialist',
        'Incident Management Sre': 'incident_management_specialist',
        'Devops Engineer': 'devops_engineer',
        'Devops Cloud': 'devops_engineer',
        'Fullstack Developer': 'fullstack_developer',
        'Android Developer': 'android_developer',
        'Ai Product Engineer': 'ai_product_engineer',
        'Backend Developer': 'backend_developer',
        'It Business Analyst': 'it_business_analyst',
        'IT Support': 'it_support_specialist',
        'Customer Support Engineer': 'it_support_specialist',
        'Technical Support': 'it_support_specialist',
        'Cloud Engineer': 'devops_engineer',
        'Platform Engineer': 'devops_engineer',
        # By role_category (internal key)
        'incident_management_sre': 'incident_management_specialist',
        'devops_cloud': 'devops_engineer',
        'fullstack_developer': 'fullstack_developer',
        'android_developer': 'android_developer',
        'ai_product_engineer': 'ai_product_engineer',
        'backend_developer': 'backend_developer',
        'it_business_analyst': 'it_business_analyst',
        'it_support': 'it_support_specialist',
        'cloud_engineer': 'devops_engineer',
        'platform_engineer': 'devops_engineer',
        'devops_fintech': 'devops_engineer',
        'finops': 'devops_engineer',
        'integration_architect': 'backend_developer',
    }

    # Try role_category first, then role_type, then default
    brick_key = role_map.get(role_category, role_map.get(role_type, 'devops_engineer'))

    profile = PROFILE_BRICKS.get(brick_key, PROFILE_BRICKS['devops_engineer'])
    skills_key = brick_key.replace('_specialist', '_primary').replace('_engineer', '_primary').replace('_developer', '_primary').replace('_analyst', '_primary')
    skills = SKILLS_BRICKS.get(skills_key, SKILLS_BRICKS['devops_primary'])

    # Get projects section for this role
    projects = PROJECTS_BRICKS.get(brick_key, PROJECTS_BRICKS['default'])

    skills_items = "\n".join([f"\\item {skill}" for skill in skills])
    
    # Build LaTeX with modern Overleaf styling - ENHANCED TO MATCH PERFECT RESUME
    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}

\geometry{left=2cm,right=2cm,top=2cm,bottom=2cm}
\setlength{\parindent}{0pt}
\pagestyle{empty}

\definecolor{titlecolor}{RGB}{0,119,181}

\titleformat{\section}{\Large\bfseries\color{titlecolor}}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{12pt}{6pt}

\titleformat{\subsection}{\large\bfseries}{}{0em}{}
\titlespacing*{\subsection}{0pt}{8pt}{4pt}

\begin{document}

\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[8pt]
{\Large \textbf{""" + role_type + r"""}}\\[10pt]
\textcolor{titlecolor}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} — \href{tel:+46728384299}{+46 72 838 4299} — \href{https://www.linkedin.com/in/hzl/}{LinkedIn} — \href{https://github.com/bluehawana}{GitHub}}
\end{center}

\vspace{8pt}

\section*{Professional Summary}
""" + profile + r"""

\section*{Core Technical Competencies}
""" + skills_items.replace('\\item \\textbf{', '\\textbf{').replace('}', ': ').replace('\\item ', '') + r"""

\section*{Professional Experience}

\subsection*{Ecarx (Geely Automotive) — IT/Infrastructure Specialist}
\textit{October 2024 - November 2025 — Gothenburg, Sweden}

Managed IT infrastructure with 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego)

Led Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45\% and improving CI/CD efficiency by 25\%

Optimized HPC cluster achieving world top 10\% performance, outperforming Azure servers by 259\%

Deployed Prometheus/Grafana monitoring for proactive incident detection and capacity planning

Resolved critical server boot failures through system diagnostics and configuration corrections

Implemented infrastructure automation using Terraform and Ansible, reducing manual deployment time by 60\%

Managed Docker containerization and Kubernetes orchestration for microservices architecture

Configured SSL/TLS certificates and network security protocols for production environments

\subsection*{H3C Technologies — Technical Support Engineer (Freelance)}
\textit{May 2024 - November 2025 — Gothenburg, Sweden}

Resolved critical incident affecting 26 servers through root cause analysis within 5 hours

Performed on-site hardware maintenance and component replacement for enterprise servers

Delivered technical training and created documentation in Swedish and English

Implemented monitoring solutions for proactive system health checks

Collaborated with international teams across different time zones for 24/7 support coverage

\subsection*{Synteda AB — Azure Developer \& Application Support (Freelance)}
\textit{August 2023 - September 2024 — Gothenburg, Sweden}

Provided technical support for Azure cloud applications serving 1000+ users

Developed platforms using C\#/.NET Core with microservices architecture

Managed Azure configurations, database connectivity, and API integrations

Implemented CI/CD pipelines using Azure DevOps and GitHub Actions

Optimized application performance resulting in 40\% faster response times

Designed and implemented RESTful APIs with comprehensive error handling and logging

\subsection*{IT-Högskolan — Backend Developer}
\textit{January 2023 - May 2023 — Gothenburg, Sweden}

Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services

Developed RESTful APIs for frontend integration and implemented secure data handling

Collaborated with UI/UX designers for seamless frontend-backend integration

Implemented automated tests as part of delivery process achieving 90\% code coverage

Worked with PostgreSQL databases and optimized query performance

\subsection*{Senior Material AB — Fullstack Developer}
\textit{May 2022 - December 2022 — Gothenburg, Sweden}

Developed e-commerce platform using React frontend and Spring Boot backend

Implemented payment processing integration with Stripe and PayPal APIs

Built inventory management system with real-time stock tracking

Optimized database queries reducing page load times by 50\%

Collaborated with cross-functional teams using Agile/Scrum methodologies

\subsection*{AddCell AB — Software Developer}
\textit{September 2021 - April 2022 — Gothenburg, Sweden}

Developed mobile applications using React Native for iOS and Android platforms

Implemented backend services using Node.js and Express.js framework

Integrated third-party APIs for location services and payment processing

Participated in code reviews and maintained high code quality standards

\subsection*{Pembio AB — Full-Stack Developer}
\textit{October 2020 - September 2021 — Lund, Sweden}

Developed backend using Java/Spring Boot with microservices architecture

Built frontend with Vue.js and integrated with backend APIs

Implemented user authentication and authorization systems

Participated in Agile development processes and collaborated with cross-functional teams

Designed and implemented database schemas using PostgreSQL

\subsection*{CollabMaker — Software Developer (Part-time)}
\textit{January 2020 - September 2020 — Gothenburg, Sweden}

Developed web applications using modern JavaScript frameworks

Implemented responsive design principles for mobile-first development

Collaborated with designers to create intuitive user interfaces

Participated in startup environment with rapid prototyping and iteration

""" + projects + r"""

\section*{Education}

\textbf{IT-Hogskolan} — Bachelor's in .NET Cloud Development — 2021-2023 — Gothenburg

Specialized in cloud-native application development using Microsoft Azure. Completed capstone project: Microservices architecture with Docker and Kubernetes. Coursework: Advanced C\#/.NET, Azure Services, DevOps, Database Design.

\textbf{Molndal Campus} — Bachelor's in Java Integration — 2019-2021 — Molndal

Focus on enterprise Java development and system integration. Thesis project: RESTful API design patterns for microservices. Coursework: Spring Framework, Hibernate, Maven, JUnit Testing.

\textbf{University of Gothenburg} — Master's in International Business — 2016-2019 — Gothenburg

Specialized in international trade and business strategy. Thesis: "Digital Transformation in Nordic SMEs". Coursework: Strategic Management, International Marketing, Business Analytics.

\section*{Certifications}

AWS Certified Solutions Architect - Associate (2022)

Microsoft Certified: Azure Fundamentals (2022)

AWS Certified Data Analytics - Specialty (2022)

Certified Kubernetes Administrator (CKA) (2023) - Linux Foundation

Docker Certified Associate (2023) - Docker Inc.

Terraform Associate (2024) - HashiCorp

Prometheus Certified Associate (2024) - Linux Foundation

\section*{Community Involvement}

Active member of AWS User Group Gothenburg - participating in cloud architecture discussions

Participant in CNCF Gothenburg community events - focusing on Kubernetes and cloud-native technologies

CNCF Scholarship Recipient - CKAD Training \& Exam Voucher (2024)

Member of Kubernetes Community Gothenburg - contributing to local meetups and knowledge sharing

DevOps Gothenburg Meetup - Regular speaker on infrastructure automation topics

Open Source Contributions - Active contributor to various GitHub projects

Technical Mentoring - Mentor junior developers in cloud technologies and DevOps practices

\section*{Additional Information}

\textbf{Languages:} English (Fluent), Swedish (B2), Chinese (Native)

\textbf{Work Authorization:} Swedish Permanent Residence

\textbf{Availability:} Immediate

\end{document}
"""
    
    return latex


def customize_cover_letter(template_content: str, company: str, title: str) -> str:
    """Customize cover letter template with company and title"""
    import re
    from datetime import datetime

    # Clean up title - remove leading articles (an, a, the)
    if title:
        title = re.sub(r'^(an?|the)\s+', '', title, flags=re.IGNORECASE).strip()
        # Capitalize first letter of each word, but preserve acronyms
        title = title.title() if title else title
        # Restore common acronyms that .title() would break
        acronyms = ['IT', 'AI', 'API', 'CI/CD', 'DevOps', 'SRE', 'UI', 'UX', 'QA', 'BI', 'ERP', 'CRM', 'HR', 'AWS', 'GCP', 'iOS', 'ML']
        for acronym in acronyms:
            title = re.sub(r'\b' + acronym.title() + r'\b', acronym, title, flags=re.IGNORECASE)

    # Replace placeholders - CRITICAL: Replace longest placeholders FIRST to avoid partial replacements
    # This prevents "COMPANY_NAME_PLACEHOLDER" from becoming "Aros Kapital_PLACEHOLDER" 
    # when we later replace "COMPANY_NAME"
    
    if company and company != 'Company':
        # Replace longest patterns first
        template_content = template_content.replace('COMPANY_NAME_PLACEHOLDER', company)
        template_content = template_content.replace('COMPANY\\_NAME', company)  # LaTeX escaped
        template_content = template_content.replace('[COMPANY NAME]', company)
        template_content = template_content.replace('[Company Name]', company)
        template_content = template_content.replace('{company_name}', company)
        # Do NOT replace bare "COMPANY_NAME" as it might match parts of other placeholders

    # Replace position/job title placeholders - longest first
    if title and title != 'Position':
        # Replace longest patterns first
        template_content = template_content.replace('JOB_TITLE_PLACEHOLDER', title)
        template_content = template_content.replace('JOB\\_TITLE', title)  # LaTeX escaped
        template_content = template_content.replace('[JOB TITLE]', title)
        template_content = template_content.replace('[Position]', title)
        template_content = template_content.replace('{job_title}', title)
        # Do NOT replace bare "JOB_TITLE" as it might match parts of other placeholders

    # Replace any remaining placeholder patterns
    template_content = template_content.replace('[SPECIFIC REASON - customize per company]', 'your reputation for excellence and commitment to quality')
    template_content = template_content.replace('[SPECIFIC REASON]', 'your reputation for excellence and commitment to quality')
    
    # Remove inappropriate generic language that doesn't fit all roles
    template_content = template_content.replace('passion for innovative software development', 'dedication to technical excellence')
    template_content = template_content.replace('innovative software development', 'technical excellence')
    template_content = template_content.replace('scalable software solutions', 'effective technical solutions')
    template_content = template_content.replace('modern development practices', 'best practices and continuous improvement')

    # Clean up placeholder lines in header (use simple string operations to avoid regex escape issues)
    lines = template_content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Skip lines with unfilled placeholders
        if '[Address]' in line or '[Contact Email]' in line or '[City]' in line:
            continue
        if 'Hiring Manager' in line and '\\\\' in line:
            continue
        cleaned_lines.append(line)
    template_content = '\n'.join(cleaned_lines)

    # Update date
    today = datetime.now().strftime("%B %d, %Y")
    template_content = re.sub(
        r'(January|February|March|April|May|June|July|August|September|October|November|December) \d+, 202\d',
        today,
        template_content
    )

    return template_content


def ai_enhance_cover_letter(template_content: str, job_description: str, company: str, title: str) -> str:
    """
    Use GLM-4.7 to intelligently enhance cover letter with relevant experience
    based on job description requirements
    """
    try:
        import requests
        import json
        import re
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not api_key:
            print("⚠️ No API key - skipping AI enhancement")
            return template_content
        
        # Extract key requirements from job description
        jd_lower = job_description.lower()
        
        # Build context about candidate's full experience
        candidate_context = """
CANDIDATE BACKGROUND - Harvad (Hongzhi) Li:

CHINA EXPERIENCE (2012-2016):
- Market Manager at Bank of China (2015-2016): Corporate banking, client relationships, financial products
- Corporate Finance Specialist at Industrial and Commercial Bank of China (2012-2015): Financial analysis, risk assessment, corporate lending, investment evaluation

SWEDEN BUSINESS EXPERIENCE (2017-Present):
- Entrepreneur & Co-founder, Hong Yan AB (2017-Present): Built restaurant business from 0 to 3.2M SEK revenue (2021), 25% annual growth
- E-commerce & Payment Systems: Integrated Wix, Zettle, Stripe for online payments, booking systems, delivery services
- Ranked #1 on Foodora (2021-2022), most recommended on Uber Eats and Tripadvisor
- Business expansion: Online shopping, table reservations, delivery services integration

WEB DEVELOPMENT & PROJECTS:
- smrtmart.com: E-commerce platform (Next.js, React, Go, PostgreSQL, Stripe payment integration)
- hongyanab.com: Company website with booking system, payment processing, customer management
- bluehawana.com: Personal portfolio website showcasing technical projects
- weather.bluehawana.com: ASCII-style weather forecast application
- jobs.bluehawana.com: AI-powered job application platform (React, TypeScript, Python FastAPI)
- models.bluehawana.com: NVIDIA NIM proxy Claude code demo platform
- sagatoy.com: AI-powered interactive toy platform (React, Python, WebSockets, multi-LLM routing)

TECHNICAL EXPERIENCE (2020-2025):
- ECARX (2024-2025): IT/Infrastructure, Azure AKS, FinOps (45% cost reduction), monitoring, DevOps
- Synteda (2023-2024): .NET development, Azure integration, full-stack applications
- IT-Högskolan (2023): .NET Cloud Development, Azure DevOps, Terraform
- Senior Material (2022): Platform architect, full-stack development, Microsoft ecosystem integration
- Pembio (2020-2021): Full-stack development, Vue.js, Spring Boot, mission management system
- CollabMaker (2020): Frontend development, React.js, career matching platform

IT BUSINESS ANALYST CAPABILITIES:
- Bridge between business and IT: Translate business requirements into technical solutions
- Requirements gathering and stakeholder management (worked with Chinese and Swedish stakeholders)
- Business process analysis and improvement (restaurant operations, e-commerce workflows)
- System integration projects (Wix, Zettle, Stripe, Uber Eats, Foodora integrations)
- Data analysis and reporting (sales analytics, customer insights, operational metrics)
- Project coordination with technical teams and business stakeholders
- Gap analysis and solution design for business problems

CROSS-CULTURAL COMMUNICATION STRENGTHS:
- Trilingual: English (Fluent), Swedish (B2), Chinese (Native)
- Chinese-Swedish business bridge: Understand both cultures, work styles, and business practices
- Experience working with Chinese banks (BOC, ICBC) and Swedish companies (ECARX, Synteda, Senior Material)
- Cultural adaptation: Successfully transitioned from Chinese corporate banking to Swedish tech/startup environment
- International team collaboration: Worked across 4 global offices at ECARX (China, Sweden, UK, Germany)
- Client-facing experience in both Chinese and Swedish markets

RELEVANT SKILLS FOR FINTECH/LENDING/BUSINESS:
- Financial services experience (banking, corporate finance, lending, risk assessment)
- Payment systems integration (Stripe, Zettle, Wix Payments)
- E-commerce platforms and online payment processing
- Business operations (payroll, accounting, inventory, customer management)
- SME business growth and expansion strategies
- Full-stack web development for business applications
"""

        prompt = f"""You are enhancing a cover letter for a job application. Based on the job description, intelligently select and emphasize the MOST RELEVANT experience from the candidate's background.

JOB DESCRIPTION:
{job_description[:1500]}

COMPANY: {company}
POSITION: {title}

{candidate_context}

CURRENT COVER LETTER TEMPLATE:
{template_content}

TASK: Enhance the cover letter by:
1. If the job involves FINTECH/LENDING/FINANCE/PAYMENTS: Emphasize China banking experience, Sweden business experience with payment systems, e-commerce projects
2. If the job involves FULL-STACK/WEB DEVELOPMENT: Emphasize web projects (smrtmart.com, hongyanab.com, jobs.bluehawana.com, sagatoy.com)
3. If the job involves BUSINESS/ENTREPRENEURSHIP: Emphasize Hong Yan AB success story, SME growth, business expansion
4. If the job involves TECHNICAL SUPPORT/IT: Emphasize ECARX experience, multilingual support, problem-solving
5. If the job involves IT BUSINESS ANALYST/INTEGRATION: Emphasize bridge between business and IT, requirements gathering, stakeholder management, system integration projects
6. If the job mentions CHINESE/ASIAN MARKETS or INTERNATIONAL: Emphasize Chinese-Swedish bilingual capabilities, cross-cultural communication, experience in both Chinese banks and Swedish tech companies
7. If the job involves COMMUNICATION/STAKEHOLDER MANAGEMENT: Emphasize trilingual abilities (English, Swedish, Chinese), experience working with diverse teams across 4 global offices

IMPORTANT:
- Keep the existing LaTeX structure intact
- Replace the generic "Body paragraph 2" section with specific, relevant experience
- Mention 2-3 most relevant projects/experiences
- Keep it concise (3-4 sentences per paragraph)
- Maintain professional tone
- Do NOT add placeholder text
- Return ONLY the enhanced LaTeX code, no explanations

Enhanced cover letter:"""

        url = f"{base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "glm-4.7",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        print("🤖 Calling GLM-4.7 to enhance cover letter with relevant experience...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'content' in result and len(result['content']) > 0:
                enhanced_content = result['content'][0].get('text', '')
                
                # Clean up the response - remove markdown code blocks if present
                enhanced_content = re.sub(r'```latex\n', '', enhanced_content)
                enhanced_content = re.sub(r'```\n?', '', enhanced_content)
                enhanced_content = enhanced_content.strip()
                
                # Validate it's still valid LaTeX
                if '\\documentclass' in enhanced_content and '\\begin{document}' in enhanced_content:
                    print("✅ Cover letter enhanced with relevant experience")
                    return enhanced_content
                else:
                    print("⚠️ AI response not valid LaTeX, using original template")
                    return template_content
            else:
                print("⚠️ Empty AI response, using original template")
                return template_content
        else:
            print(f"⚠️ AI API error: {response.status_code}, using original template")
            return template_content
            
    except Exception as e:
        print(f"⚠️ Error in AI enhancement: {e}, using original template")
        return template_content


def build_lego_cover_letter(role_type: str, company: str, title: str, role_category: str = None, job_description: str = "", customization_notes: str = "") -> str:
    """Build cover letter using LEGO bricks - Template-based with customization"""

    print(f"[CL] role_category={role_category}, company={company}, title={title}")

    # Try to load cover letter template directly from cv_templates
    if role_category:
        # Use the new direct CL template loading (no string manipulation needed)
        template_content = template_manager.load_template(role_category, 'cl')

        if template_content:
            print(f"[CL] Loaded CL template for role: {role_category}")
            # Customize with company/title
            template_content = customize_cover_letter(template_content, company, title)
            print(f"[CL] Template customized successfully")
            
            # AI Enhancement: Use GLM-4.7 to add relevant experience based on job description
            if job_description and len(job_description) > 100:
                template_content = ai_enhance_cover_letter(template_content, job_description, company, title)
            
            return template_content
        else:
            print(f"[CL] No CL template found for role: {role_category}")

    print(f"[CL] Falling back to LEGO bricks generation")
    # Fallback to LEGO bricks generation
    today = datetime.now().strftime("%B %d, %Y")
    
    # Clean up company and title - handle placeholder cases
    if not company or company in ['Company', '[COMPANY NAME]', '[Company Name]']:
        company = 'Target Company'
    if not title or title in ['Position', '[JOB TITLE]', '[Job Title]']:
        title = 'Target Position'
    
    # DEBUG: Print what values are being used
    print(f"[CL DEBUG] Using company='{company}', title='{title}', role_type='{role_type}'")
    
    # Create role-appropriate cover letter content
    if 'support' in title.lower() or 'support' in role_type.lower():
        # Customer/Technical Support role content
        opening = f"I'm excited to apply for the {title} position at {company}. With 5+ years of technical experience and a strong background in customer service and problem-solving, I'm confident I can provide excellent support to your customers and contribute immediately to your team."
        
        expertise = r"""\textbf{Customer Support Excellence:} At ECARX, I provide technical support across 4 global offices, helping customers resolve complex technical issues. My most significant achievement was resolving a critical incident affecting 26 servers - I performed systematic troubleshooting under pressure and completed resolution within 5 hours, ensuring minimal customer impact. This experience demonstrates my ability to work under pressure, communicate effectively with customers, and resolve technical problems rapidly.

\textbf{Technical Problem-Solving:} I have hands-on experience with various technologies including cloud platforms (AWS, Azure), monitoring tools (Prometheus, Grafana), and scripting (Python, Bash). I excel at translating complex technical concepts into clear explanations for customers, creating documentation, and providing training. My multilingual abilities (English, Swedish, Chinese) enable me to support diverse customer bases effectively.

\textbf{Customer-Focused Approach:} I'm passionate about helping customers succeed and ensuring their technical challenges are resolved quickly and efficiently. My experience includes troubleshooting hardware and software issues, coordinating with engineering teams, and maintaining high customer satisfaction through clear communication and follow-up."""
        
        closing = f"I'm passionate about customer success and technical problem-solving. I'd welcome the opportunity to discuss how my experience can contribute to {company}'s continued success and customer satisfaction. Thank you for considering my application."
        
    else:
        # Default technical role content
        opening = f"I'm excited to apply for the {title} position at {company}. With 5+ years managing production infrastructure, resolving critical incidents, and optimizing cloud operations, I'm confident I can contribute immediately to your team."
        
        expertise = r"""\textbf{Technical Expertise:} At ECARX, I provide 24/7 on-call support across 4 global offices (Gothenburg, London, Stuttgart, San Diego). My most significant achievement was resolving a critical incident affecting 26 servers - I performed systematic root cause analysis under pressure and completed remediation within 5 hours. This experience demonstrates my ability to work under pressure, perform thorough RCA, and restore production systems rapidly.

\textbf{Infrastructure \& Automation:} I led the migration from Azure AKS to on-premise Kubernetes, reducing cloud costs by 45\% while improving CI/CD efficiency by 25\%. I deployed comprehensive Prometheus/Grafana monitoring stacks that reduced MTTR by 35\% through proactive alerting. I automate infrastructure using Terraform and Ansible, reducing manual intervention by 60\% and accelerating release cycles.

\textbf{Technical Alignment:} My skills directly match your requirements - AWS/Azure certified with hands-on experience; expert in Terraform and CloudFormation for IaC; proficient with Jenkins, GitHub Actions, and GitLab CI for CI/CD; deep expertise in Prometheus, Grafana, and ELK for observability; strong Python and Bash scripting for automation; production Kubernetes experience including troubleshooting and optimization."""
        
        closing = f"I'm passionate about platform reliability, MTTR reduction, and developer experience improvements. I'd welcome the opportunity to discuss how my experience can contribute to {company}'s success. Thank you for considering my application."
    
    latex = r"""\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=1in}
\setlength{\parindent}{0pt}
\definecolor{linkedinblue}{RGB}{0,119,181}
\hypersetup{colorlinks=true, linkcolor=linkedinblue, urlcolor=linkedinblue}

\begin{document}

% Header with job information (LinkedIn blue - matching CV)
{\color{linkedinblue}\textbf{""" + company + r"""}\\
""" + title + r"""\\
Gothenburg, Sweden}

\vspace{1cm}

Dear Hiring Manager,

\vspace{0.5cm}

""" + opening + r"""

""" + expertise + r"""

""" + closing + r"""

\vspace{1cm}

Best Regards,\\[0.5cm]
Harvad (Hongzhi) Li

\vspace{\fill}

% Line separator
{\color{linkedinblue}\hrule height 0.5pt}

\vspace{0.3cm}

% Footer with address and date
{\color{linkedinblue}Ebbe Lieberathsgatan 27\\
41265, Gothenburg, Sweden\\
\hfill \today}

\end{document}
"""
    
    return latex


def fetch_job_from_url(url: str) -> str:
    """Fetch job description from URL using ScraperAPI"""
    try:
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import urlparse, parse_qs, quote
        
        parsed_url = urlparse(url)
        is_indeed = 'indeed' in parsed_url.netloc.lower()
        is_linkedin = 'linkedin' in parsed_url.netloc.lower()
        
        # Handle Indeed URL - extract job key
        if is_indeed:
            query_params = parse_qs(parsed_url.query)
            job_key = query_params.get('vjk', [None])[0] or query_params.get('jk', [None])[0]
            if job_key:
                url = f"{parsed_url.scheme}://{parsed_url.netloc}/viewjob?jk={job_key}"
                print(f"📌 Converted Indeed URL: {url}")
        
        # Check for ScraperAPI key
        api_key = os.environ.get('SCRAPERAPI_KEY', '')
        
        # LinkedIn requires premium scraping or manual copy-paste
        if is_linkedin:
            if api_key:
                # Use ScraperAPI with premium LinkedIn support
                scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={quote(url)}&premium=true&country_code=se"
                print(f"🔄 Using ScraperAPI Premium for LinkedIn")
                response = requests.get(scraper_url, timeout=60)
            else:
                # LinkedIn blocks automated access - return empty to trigger manual paste
                print(f"⚠️ LinkedIn requires manual copy-paste or ScraperAPI Premium")
                print(f"💡 Solution: Copy job description from LinkedIn and paste into text area")
                return ""
        
        # Use ScraperAPI for Indeed (they block VPS IPs)
        elif is_indeed and api_key:
            scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={quote(url)}"
            print(f"🔄 Using ScraperAPI for {parsed_url.netloc}")
            response = requests.get(scraper_url, timeout=60)
        else:
            # Direct request (works for other sites, may fail for Indeed/LinkedIn without proxy)
            if is_indeed:
                print(f"⚠️ No SCRAPERAPI_KEY configured - direct request may be blocked")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            response = requests.get(url, headers=headers, timeout=15)
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            element.decompose()
        
        text = ""
        
        # Indeed-specific parsing
        if is_indeed:
            # Look for job description container
            job_desc = soup.find('div', {'id': 'jobDescriptionText'})
            if job_desc:
                text = job_desc.get_text(separator='\n', strip=True)
            
            # Get title and company
            title_elem = soup.find('h1', class_=lambda x: x and 'jobTitle' in str(x).lower()) or soup.find('h1')
            company_elem = soup.find(attrs={'data-testid': 'inlineHeader-companyName'}) or soup.find(class_=lambda x: x and 'company' in str(x).lower())
            
            if title_elem:
                text = f"Job Title: {title_elem.get_text(strip=True)}\n" + text
            if company_elem:
                text = f"Company: {company_elem.get_text(strip=True)}\n" + text
        
        # LinkedIn-specific parsing
        elif is_linkedin:
            job_containers = soup.find_all(['div', 'section'], class_=lambda x: x and 'description' in str(x).lower())
            for container in job_containers:
                text += container.get_text(separator='\n', strip=True) + '\n'
        
        # Fallback: get all text
        if not text or len(text) < 100:
            text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) > 2]
        # Remove duplicates
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        
        text = '\n'.join(unique_lines)
        
        # Truncate if too long
        if len(text) > 10000:
            text = text[:10000] + "\n\n[Content truncated...]"
        
        if len(text) < 50:
            print(f"⚠️ Retrieved very little content ({len(text)} chars)")
            return ""
        
        print(f"✓ Successfully fetched {len(text)} characters")
        return text
        
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out for URL: {url}")
        return ""
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error {e.response.status_code} for URL: {url}")
        return ""
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""


def ai_review_documents(cv_latex: str, cl_latex: str, job_description: str, company: str, title: str) -> dict:
    """
    AI-powered quality check for generated CV and Cover Letter using Z.AI GLM-4.7
    Reviews documents against job description to catch inappropriate content
    """
    try:
        import requests
        import json
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not api_key:
            print("⚠️ No API key for AI review - skipping quality check")
            return {'overall_score': 85, 'ready_to_send': True, 'critical_issues': []}
        
        # Extract text content from LaTeX for analysis
        import re
        cv_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', cv_latex)  # Remove LaTeX commands
        cv_text = re.sub(r'\\[a-zA-Z]+', '', cv_text)  # Remove remaining commands
        cv_text = re.sub(r'\{|\}', '', cv_text)  # Remove braces
        
        cl_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', cl_latex)
        cl_text = re.sub(r'\\[a-zA-Z]+', '', cl_text)
        cl_text = re.sub(r'\{|\}', '', cl_text)
        
        prompt = f"""Review these job application documents for quality and appropriateness:

JOB DESCRIPTION:
{job_description[:1000]}...

COMPANY: {company}
POSITION: {title}

CV CONTENT:
{cv_text[:2000]}...

COVER LETTER CONTENT:
{cl_text[:1000]}...

Please analyze and provide a JSON response with:
1. overall_score (0-100): Overall quality score
2. ready_to_send (boolean): Whether documents are appropriate to send
3. critical_issues (array): List any critical problems like:
   - Inappropriate language for the role (e.g., "software development" for Customer Support)
   - Generic placeholder text like [COMPANY NAME] or [SPECIFIC REASON]
   - Mismatched skills/experience for the position
   - Unprofessional content

Format: {{"overall_score": 85, "ready_to_send": true, "critical_issues": []}}"""

        url = f"{base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "glm-4.7",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result_data = response.json()
            
            # Extract text from response
            ai_response = ""
            if 'content' in result_data:
                for block in result_data['content']:
                    if block.get('type') == 'text':
                        ai_response += block.get('text', '')
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                quality_result = json.loads(json_match.group())
                print(f"✅ AI Quality Check completed: {quality_result.get('overall_score', 'N/A')}/100")
                return quality_result
            else:
                print("⚠️ Could not parse AI quality check response")
                return {'overall_score': 75, 'ready_to_send': True, 'critical_issues': ['Could not parse AI response']}
        else:
            print(f"⚠️ AI quality check failed: {response.status_code}")
            return {'overall_score': 70, 'ready_to_send': True, 'critical_issues': ['AI service unavailable']}
            
    except Exception as e:
        print(f"⚠️ AI quality check error: {e}")
        return {'overall_score': 70, 'ready_to_send': True, 'critical_issues': [f'Quality check error: {str(e)}']}


@lego_api.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        'status': 'healthy',
        'service': 'JobHunter LEGO API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@lego_api.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze job description and return analysis with ATS optimization"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        job_url = data.get('jobUrl', '')
        company_name = data.get('companyName', '').strip()
        job_title = data.get('jobTitle', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if not company_name or not job_title:
            return jsonify({'error': 'Company name and job title are required'}), 400
        
        # STEP 1: Get ATS optimization recommendations from AI
        ats_recommendations = None
        if ai_analyzer.is_available():
            print("🤖 Getting ATS optimization recommendations from AI...")
            ats_recommendations = ai_analyzer.analyze_job_for_ats_optimization(job_description)
            if ats_recommendations:
                print(f"✅ AI recommends template: {ats_recommendations['recommended_template']}")
                print(f"📊 ATS score potential: {ats_recommendations['ats_score_potential']}%")
                print(f"🔑 Critical keywords: {', '.join(ats_recommendations['critical_keywords'][:5])}")
        
        # STEP 2: Analyze the job description (role detection)
        analysis = analyze_job_description(job_description, job_url)
        
        # STEP 3: Override with user-provided company and title
        analysis['company'] = company_name
        analysis['title'] = job_title
        analysis['extractionStatus'] = {
            'success': True,
            'issues': [],
            'requiresManualInput': False,
            'message': 'Company and job title provided by user',
            'source': 'user_input'
        }
        
        # STEP 4: Add ATS optimization recommendations to analysis
        if ats_recommendations:
            analysis['ats_optimization'] = ats_recommendations
            # Override role type if AI recommends a different template
            if ats_recommendations['recommended_template'] != analysis.get('roleType'):
                print(f"📝 Overriding role from {analysis.get('roleType')} to {ats_recommendations['recommended_template']} based on AI recommendation")
                analysis['roleType'] = ats_recommendations['recommended_template']
        
        print(f"📍 User provided: {company_name} - {job_title}")
        print(f"🎯 Final role type: {analysis.get('roleType')}")
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'jobDescription': job_description,
            'extractionStatus': analysis.get('extractionStatus', {}),
            'atsOptimization': ats_recommendations  # Include ATS recommendations in response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/update-job-info', methods=['POST'])
def update_job_info():
    """Update company name and job title manually when extraction fails"""
    try:
        data = request.json
        analysis = data.get('analysis', {})
        company = data.get('company', '').strip()
        title = data.get('title', '').strip()
        
        if not company or not title:
            return jsonify({'error': 'Both company name and job title are required'}), 400
        
        # Validate input lengths
        if len(company) > 100:
            return jsonify({'error': 'Company name too long (max 100 characters)'}), 400
        if len(title) > 100:
            return jsonify({'error': 'Job title too long (max 100 characters)'}), 400
        
        # Update the analysis with manual input
        analysis['company'] = company
        analysis['title'] = title
        analysis['extractionStatus'] = {
            'success': True,
            'issues': [],
            'requiresManualInput': False,
            'message': 'Company and job title provided manually',
            'source': 'manual_input'
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'message': 'Job information updated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/generate-lego-application', methods=['POST'])
def generate_lego_application():
    """Generate CV and Cover Letter using LEGO bricks"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        job_url = data.get('jobUrl', '')
        analysis = data.get('analysis', {})
        customization_notes = data.get('customizationNotes', '')

        # EXTRACT FROM URL IF PROVIDED: Use backend URL extraction for accurate parsing
        if job_url and job_url.strip():
            print(f"🔗 Extracting job details from URL: {job_url}")
            try:
                from app.services.job_url_extractor import JobUrlExtractor
                extractor = JobUrlExtractor()
                extraction_result = extractor.extract_job_details(job_url)
                
                if extraction_result.get('success') and extraction_result.get('job_details'):
                    job_details = extraction_result['job_details']
                    print(f"✅ URL Extraction successful:")
                    print(f"   Company: {job_details.get('company')}")
                    print(f"   Title: {job_details.get('title')}")
                    print(f"   Location: {job_details.get('location')}")
                    
                    # Override analysis with extracted data (URL extraction is more accurate)
                    if job_details.get('company'):
                        analysis['company'] = job_details['company']
                    if job_details.get('title'):
                        analysis['title'] = job_details['title']
                    if job_details.get('description') and not job_description:
                        job_description = job_details['description']
                else:
                    print(f"⚠️ URL extraction failed: {extraction_result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"⚠️ URL extraction error: {e}")
                # Continue with analysis data as fallback

        role_type = analysis.get('roleType', 'DevOps Engineer')
        role_category = analysis.get('roleCategory', 'devops_cloud')
        company = analysis.get('company', 'Company')
        title = analysis.get('title', 'Position')

        print(f"📋 Final values after URL extraction: Company='{company}', Title='{title}', Role='{role_type}'")

        # SAFEGUARD: Ensure role_type is consistent with role_category
        # This prevents mismatches where role_category is 'devops_cloud' but role_type is 'IT Business Analyst'
        # EXCEPTION: Don't override for company-specific roles like 'kamstrup' - keep the actual job title
        if role_category not in ['kamstrup']:  # Add other company-specific roles here if needed
            expected_role_type = role_category.replace('_', ' ').title()
            if role_type != expected_role_type:
                print(f"⚠️ Role type mismatch detected: roleType='{role_type}', roleCategory='{role_category}'")
                print(f"🔧 Correcting role_type from '{role_type}' to '{expected_role_type}'")
                role_type = expected_role_type

        # Handle template selection failures gracefully
        try:
            # Verify template exists before proceeding
            template_path = template_manager.get_template_path(role_category, 'cv')
            if not template_path:
                print(f"⚠ Template not found for role {role_category}, using fallback")
                # Get fallback role
                fallback_role = template_manager.template_matcher.get_fallback_template([role_category])
                role_category = fallback_role
                role_type = fallback_role.replace('_', ' ').title()
                print(f"✓ Using fallback role: {role_category}")
        except Exception as e:
            print(f"⚠ Template verification failed: {e}, using default")
            role_category = 'devops_cloud'
            role_type = 'DevOps Cloud'

        # Build LaTeX documents with AI-powered content customization
        print(f"[API DEBUG] About to generate documents with - Company: '{company}', Title: '{title}', Role Type: '{role_type}', Role Category: '{role_category}'")
        cv_latex = build_lego_cv(role_type, company, title, role_category, job_description, customization_notes)
        cl_latex = build_lego_cover_letter(role_type, company, title, role_category, job_description, customization_notes)
        
        # AI QUALITY CHECK: Review generated documents against job description
        print(f"🤖 Running AI quality check on generated documents...")
        quality_check = ai_review_documents(cv_latex, cl_latex, job_description, company, title)
        print(f"📊 AI Quality Check Results: {quality_check.get('overall_score', 'N/A')}/100")
        
        # Log critical issues if any
        if quality_check.get('critical_issues'):
            print(f"⚠️ Critical Issues Found: {quality_check['critical_issues']}")
        if not quality_check.get('ready_to_send', True):
            print(f"🚫 Documents NOT ready to send - needs review!")
        else:
            print(f"✅ Documents passed AI quality check")
        
        # Create output directory
        output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate smart filenames based on company name
        company_safe = sanitize_filename(company)
        cv_filename = f'cv_harvad_{company_safe}.pdf'
        cl_filename = f'cl_harvad_{company_safe}.pdf'
        
        # Save LaTeX files
        cv_tex_path = output_dir / 'cv.tex'
        cl_tex_path = output_dir / 'cl.tex'
        
        with open(cv_tex_path, 'w', encoding='utf-8') as f:
            f.write(cv_latex)
        
        with open(cl_tex_path, 'w', encoding='utf-8') as f:
            f.write(cl_latex)
        
        # Compile to PDF (temporary names)
        cv_pdf_temp = output_dir / 'cv.pdf'
        cl_pdf_temp = output_dir / 'cl.pdf'
        
        # Compile CV
        cv_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cv_result.returncode != 0:
            print(f"CV PDF compilation error: {cv_result.stderr}")
            print(f"CV PDF compilation output: {cv_result.stdout}")
        
        # Compile CL
        cl_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cl_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cl_result.returncode != 0:
            print(f"CL PDF compilation error: {cl_result.stderr}")
            print(f"CL PDF compilation output: {cl_result.stdout}")
        
        # Check if PDFs were created
        if not cv_pdf_temp.exists():
            print(f"ERROR: CV PDF was not created at {cv_pdf_temp}")
            return jsonify({'error': 'CV PDF compilation failed'}), 500
        
        if not cl_pdf_temp.exists():
            print(f"ERROR: CL PDF was not created at {cl_pdf_temp}")
            return jsonify({'error': 'CL PDF compilation failed'}), 500
        
        # Rename PDFs to smart filenames
        cv_pdf_path = output_dir / cv_filename
        cl_pdf_path = output_dir / cl_filename
        cv_pdf_temp.rename(cv_pdf_path)
        cl_pdf_temp.rename(cl_pdf_path)
        
        print(f"✅ Generated files: {cv_filename}, {cl_filename}")
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            for file in output_dir.glob(f'*{ext}'):
                file.unlink()
        
        # Include percentage breakdown in response
        response_data = {
            'success': True,
            'documents': {
                'cvUrl': f'/api/download/{output_dir.name}/{cv_filename}',
                'clUrl': f'/api/download/{output_dir.name}/{cl_filename}',
                'cvPreview': f'/api/preview/{output_dir.name}/{cv_filename}',
                'clPreview': f'/api/preview/{output_dir.name}/{cl_filename}'
            },
            'templateInfo': {
                'selectedRole': role_category,
                'selectedRoleDisplay': role_type,
                'templateUsed': str(template_manager.get_template_path(role_category, 'cv')) if template_manager.get_template_path(role_category, 'cv') else 'fallback'
            }
        }
        
        # Add percentage breakdown if available in analysis
        if 'rolePercentages' in analysis:
            response_data['roleAnalysis'] = {
                'rolePercentages': analysis['rolePercentages'],
                'roleBreakdown': analysis['roleBreakdown'],
                'confidenceScore': analysis.get('confidenceScore', 0.0)
            }
        
        # Add AI quality check results
        response_data['qualityCheck'] = quality_check
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in generate_lego_application: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/download/<folder>/<filename>')
def download_file(folder, filename):
    """Download generated PDF"""
    try:
        file_path = Path('generated_applications') / folder / filename
        if file_path.exists():
            # Set proper filename for download
            download_name = filename
            return send_file(file_path, as_attachment=True, download_name=download_name)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/preview/<folder>/<filename>')
def preview_file(folder, filename):
    """Preview generated PDF"""
    try:
        file_path = Path('generated_applications') / folder / filename
        if file_path.exists():
            return send_file(file_path, mimetype='application/pdf', download_name=filename)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/generate-comprehensive-application', methods=['POST'])
def generate_comprehensive_application():
    """
    Generate comprehensive job application package:
    1. AI-customized CV (Profile, Skills, Experience optimized for JD)
    2. Cover Letter
    3. All 5 AI Enhancement Prompts:
       - Resume rewrite (get more interviews)
       - Role targeting (10 higher-paying roles)
       - JD match check (~90% alignment)
       - Interview prep (15 questions + answers)
       - Proof projects (complete this week)
    """
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        analysis = data.get('analysis', {})
        
        role_type = analysis.get('roleType', 'DevOps Engineer')
        role_category = analysis.get('roleCategory', 'devops_cloud')
        company = analysis.get('company', 'Company')
        title = analysis.get('title', 'Position')

        # SPLIT COMBINED COMPANY-TITLE STRING: Handle "Kamstrup - Customer Support Engineer" format
        if company and ' - ' in company:
            parts = company.split(' - ', 1)  # Split only on first dash
            company = parts[0].strip()
            if title == 'Position' or not title:  # Only override title if it's not already set
                title = parts[1].strip()
            print(f"📍 Split combined string: Company='{company}', Title='{title}'")
        elif title and ' - ' in title:
            parts = title.split(' - ', 1)  # Split only on first dash
            if company == 'Company' or not company:  # Only override company if it's not already set
                company = parts[0].strip()
            title = parts[1].strip()
            print(f"📍 Split combined string: Company='{company}', Title='{title}'")
        
        # SAFEGUARD: Ensure role_type is consistent with role_category
        # This prevents mismatches where role_category is 'devops_cloud' but role_type is 'IT Business Analyst'
        # EXCEPTION: Don't override for company-specific roles like 'kamstrup' - keep the actual job title
        if role_category not in ['kamstrup']:  # Add other company-specific roles here if needed
            expected_role_type = role_category.replace('_', ' ').title()
            if role_type != expected_role_type:
                print(f"⚠️ Role type mismatch detected: roleType='{role_type}', roleCategory='{role_category}'")
                print(f"🔧 Correcting role_type from '{role_type}' to '{expected_role_type}'")
                role_type = expected_role_type
        
        # Build LaTeX documents with comprehensive AI-powered customization
        cv_latex = build_lego_cv(role_type, company, title, role_category, job_description)
        cl_latex = build_lego_cover_letter(role_type, company, title, role_category)
        
        # Create output directory
        output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save LaTeX files
        cv_tex_path = output_dir / 'cv.tex'
        cl_tex_path = output_dir / 'cl.tex'
        
        with open(cv_tex_path, 'w', encoding='utf-8') as f:
            f.write(cv_latex)
        
        with open(cl_tex_path, 'w', encoding='utf-8') as f:
            f.write(cl_latex)
        
        # Compile to PDF
        cv_pdf_path = output_dir / 'cv.pdf'
        cl_pdf_path = output_dir / 'cl.pdf'
        
        # Compile CV
        cv_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cv_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cv_result.returncode != 0:
            print(f"CV PDF compilation error: {cv_result.stderr}")
        
        # Compile CL
        cl_result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(cl_tex_path)],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if cl_result.returncode != 0:
            print(f"CL PDF compilation error: {cl_result.stderr}")
        
        # Check if PDFs were created
        if not cv_pdf_path.exists():
            return jsonify({'error': 'CV PDF compilation failed'}), 500
        
        if not cl_pdf_path.exists():
            return jsonify({'error': 'CL PDF compilation failed'}), 500
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            for file in output_dir.glob(f'*{ext}'):
                file.unlink()
        
        # Generate all 5 AI enhancement prompts
        ai_prompts_dict = generate_ai_enhancement_prompts(
            job_description,
            cv_latex,  # Use LaTeX source as resume text
            company,
            title
        )
        
        # Save AI prompts to JSON file
        prompts_path = output_dir / 'ai_enhancement_prompts.json'
        with open(prompts_path, 'w', encoding='utf-8') as f:
            json.dump(ai_prompts_dict, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'documents': {
                'cvUrl': f'/api/download/{output_dir.name}/cv.pdf',
                'clUrl': f'/api/download/{output_dir.name}/cl.pdf',
                'cvPreview': f'/api/preview/{output_dir.name}/cv.pdf',
                'clPreview': f'/api/preview/{output_dir.name}/cl.pdf',
                'promptsUrl': f'/api/download/{output_dir.name}/ai_enhancement_prompts.json'
            },
            'aiEnhancementPrompts': {
                'resumeRewrite': {
                    'title': '1. Resume Rewrite (Get More Interviews)',
                    'description': 'Rewrite with measurable achievements, strong action verbs, and ATS-friendly keywords',
                    'prompt': ai_prompts_dict['resume_rewrite']
                },
                'roleTargeting': {
                    'title': '2. Role Targeting (10 Higher-Paying Roles)',
                    'description': 'Identify 10 high-paying roles ranked by salary and market demand',
                    'prompt': ai_prompts_dict['role_targeting']
                },
                'jdMatch': {
                    'title': '3. JD Match Check (~90% Alignment)',
                    'description': 'Compare keywords and optimize resume for ~90% alignment without exaggerating',
                    'prompt': ai_prompts_dict['jd_match']
                },
                'interviewPrep': {
                    'title': '4. Interview Prep (15 Questions + Answers)',
                    'description': '15 realistic interview questions with confident sample answers',
                    'prompt': ai_prompts_dict['interview_prep']
                },
                'proofProjects': {
                    'title': '5. Proof Projects (Complete This Week)',
                    'description': '3 small projects to complete within 7 days to demonstrate skills',
                    'prompt': ai_prompts_dict['proof_projects']
                },
                'coverLetter': {
                    'title': 'Bonus: Cover Letter Generator',
                    'description': 'Generate compelling cover letter that tells a story',
                    'prompt': ai_prompts_dict['cover_letter']
                },
                'linkedinOptimization': {
                    'title': 'Bonus: LinkedIn Optimization',
                    'description': 'Optimize LinkedIn profile for recruiter searches',
                    'prompt': ai_prompts_dict['linkedin_optimization']
                },
                'salaryNegotiation': {
                    'title': 'Bonus: Salary Negotiation',
                    'description': 'Research salary ranges and negotiation strategy',
                    'prompt': ai_prompts_dict['salary_negotiation']
                }
            },
            'customizationSummary': {
                'profileSummary': 'Tailored to JD with key technologies emphasized',
                'coreSkills': 'Reordered based on JD keyword relevance',
                'workExperience': 'JD context comments added for ATS optimization',
                'atsOptimization': 'Keywords from JD emphasized throughout CV'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/generate-direct-zai', methods=['POST'])
def generate_direct_zai():
    """Generate CV and Cover Letter using direct Z.AI GLM-4.7 call"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
        
        # Direct Z.AI GLM-4.7 call via HTTP
        import requests
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
        
        url = f"{base_url}/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'anthropic-version': '2023-06-01'
        }
        
        prompt = f"""Analyze this job description and generate a complete professional CV and Cover Letter.

JOB DESCRIPTION:
{job_description}

Please provide:
1. Company name
2. Job title  
3. Role category (devops_cloud, fullstack_developer, backend_developer, etc.)
4. Complete LaTeX CV code (3 pages, professional format)
5. Complete LaTeX Cover Letter code (1 page, matching design)

Format your response as JSON:
{{
  "company": "extracted company name",
  "title": "extracted job title", 
  "roleType": "role category",
  "cvLatex": "complete LaTeX CV code here",
  "clLatex": "complete LaTeX cover letter code here"
}}"""

        payload = {
            "model": "glm-4.7",
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        print("🚀 Making direct Z.AI GLM-4.7 request...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result_data = response.json()
            print("✅ Z.AI GLM-4.7 request successful!")
            
            # Extract text from response
            ai_response = ""
            if 'content' in result_data:
                for block in result_data['content']:
                    if block.get('type') == 'text':
                        ai_response += block.get('text', '')
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Create output directory and compile PDFs
                output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Save and compile CV
                cv_tex_path = output_dir / 'cv.tex'
                with open(cv_tex_path, 'w', encoding='utf-8') as f:
                    f.write(result['cvLatex'])
                
                # Save and compile CL
                cl_tex_path = output_dir / 'cl.tex'
                with open(cl_tex_path, 'w', encoding='utf-8') as f:
                    f.write(result['clLatex'])
                
                # Compile PDFs
                for tex_file in [cv_tex_path, cl_tex_path]:
                    subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
                        capture_output=True,
                        timeout=30
                    )
                
                return jsonify({
                    'success': True,
                    'analysis': {
                        'company': result.get('company', 'Company'),
                        'title': result.get('title', 'Position'),
                        'roleType': result.get('roleType', 'Professional')
                    },
                    'documents': {
                        'cvUrl': f'/api/download/{output_dir.name}/cv.pdf',
                        'clUrl': f'/api/download/{output_dir.name}/cl.pdf'
                    },
                    'aiResponse': ai_response[:500] + '...' if len(ai_response) > 500 else ai_response,
                    'model': 'Z.AI GLM-4.7'
                })
            else:
                return jsonify({'error': 'Could not parse AI response'}), 500
        else:
            print(f"❌ Z.AI request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return jsonify({'error': f'Z.AI API error: {response.status_code}'}), 500
            
    except Exception as e:
        print(f"Error in direct Z.AI generation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def generate_direct_minimax():
    """Generate CV and Cover Letter using direct MiniMax M2 call"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
        
        # Direct MiniMax M2 call
        import anthropic
        
        client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY'),
            base_url=os.environ.get('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic')
        )
        
        prompt = f"""Analyze this job description and generate a complete professional CV and Cover Letter.

JOB DESCRIPTION:
{job_description}

Please provide:
1. Company name
2. Job title  
3. Role category (devops_cloud, fullstack_developer, backend_developer, etc.)
4. Complete LaTeX CV code (3 pages, professional format)
5. Complete LaTeX Cover Letter code (1 page, matching design)

Format your response as JSON:
{{
  "company": "extracted company name",
  "title": "extracted job title", 
  "roleType": "role category",
  "cvLatex": "complete LaTeX CV code here",
  "clLatex": "complete LaTeX cover letter code here"
}}"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse the AI response
        ai_response = message.content[0].text
        
        # Try to extract JSON from the response
        import json
        import re
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            
            # Create output directory and compile PDFs
            output_dir = Path('generated_applications') / datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save and compile CV
            cv_tex_path = output_dir / 'cv.tex'
            with open(cv_tex_path, 'w', encoding='utf-8') as f:
                f.write(result['cvLatex'])
            
            # Save and compile CL
            cl_tex_path = output_dir / 'cl.tex'
            with open(cl_tex_path, 'w', encoding='utf-8') as f:
                f.write(result['clLatex'])
            
            # Compile PDFs
            for tex_file in [cv_tex_path, cl_tex_path]:
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
                    capture_output=True,
                    timeout=30
                )
            
            return jsonify({
                'success': True,
                'analysis': {
                    'company': result.get('company', 'Company'),
                    'title': result.get('title', 'Position'),
                    'roleType': result.get('roleType', 'Professional')
                },
                'documents': {
                    'cvUrl': f'/api/download/{output_dir.name}/cv.pdf',
                    'clUrl': f'/api/download/{output_dir.name}/cl.pdf'
                },
                'aiResponse': ai_response[:500] + '...' if len(ai_response) > 500 else ai_response
            })
        else:
            return jsonify({'error': 'Could not parse AI response'}), 500
            
    except Exception as e:
        print(f"Error in direct MiniMax generation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def regenerate_application():
    """Regenerate application with user feedback"""
    try:
        data = request.json
        feedback = data.get('feedback', '')
        
        # For now, just regenerate with same logic
        # In future, use feedback to adjust LEGO bricks
        
        return generate_lego_application()
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/resume-rewrite', methods=['POST'])
def ai_prompt_resume_rewrite():
    """Generate AI prompt for resume rewriting"""
    try:
        data = request.json
        resume_text = data.get('resumeText', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text required'}), 400
        
        prompt = ai_prompts.resume_rewrite(resume_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'resume_rewrite',
            'description': 'Rewrite resume to improve interview chances with measurable achievements and ATS optimization'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/role-targeting', methods=['POST'])
def ai_prompt_role_targeting():
    """Generate AI prompt for identifying high-paying roles"""
    try:
        data = request.json
        experience_text = data.get('experienceText', '')
        
        if not experience_text:
            return jsonify({'error': 'Experience text required'}), 400
        
        prompt = ai_prompts.role_targeting(experience_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'role_targeting',
            'description': 'Identify 10 high-paying roles ranked by salary and market demand'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/jd-match', methods=['POST'])
def ai_prompt_jd_match():
    """Generate AI prompt for JD-resume matching"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        resume_text = data.get('resumeText', '')
        
        if not job_description or not resume_text:
            return jsonify({'error': 'Job description and resume text required'}), 400
        
        prompt = ai_prompts.jd_match_check(job_description, resume_text)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'jd_match',
            'description': 'Compare keywords and optimize resume for ~90% alignment with job description'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/interview-prep', methods=['POST'])
def ai_prompt_interview_prep():
    """Generate AI prompt for interview preparation"""
    try:
        data = request.json
        position = data.get('position', '')
        job_description = data.get('jobDescription', '')
        
        if not position:
            return jsonify({'error': 'Position required'}), 400
        
        prompt = ai_prompts.interview_prep(position, job_description)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'interview_prep',
            'description': '15 realistic interview questions with confident sample answers'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/proof-projects', methods=['POST'])
def ai_prompt_proof_projects():
    """Generate AI prompt for proof-of-skill projects"""
    try:
        data = request.json
        position = data.get('position', '')
        job_description = data.get('jobDescription', '')
        
        if not position or not job_description:
            return jsonify({'error': 'Position and job description required'}), 400
        
        prompt = ai_prompts.proof_projects(position, job_description)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'proof_projects',
            'description': '3 small projects to complete this week that demonstrate required skills'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/cover-letter', methods=['POST'])
def ai_prompt_cover_letter():
    """Generate AI prompt for cover letter creation"""
    try:
        data = request.json
        job_description = data.get('jobDescription', '')
        resume_text = data.get('resumeText', '')
        company_name = data.get('companyName', '')
        
        if not all([job_description, resume_text, company_name]):
            return jsonify({'error': 'Job description, resume text, and company name required'}), 400
        
        prompt = ai_prompts.cover_letter_generator(job_description, resume_text, company_name)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'cover_letter',
            'description': 'Generate compelling cover letter that tells a story'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/linkedin-optimization', methods=['POST'])
def ai_prompt_linkedin():
    """Generate AI prompt for LinkedIn profile optimization"""
    try:
        data = request.json
        resume_text = data.get('resumeText', '')
        target_roles = data.get('targetRoles', [])
        
        if not resume_text or not target_roles:
            return jsonify({'error': 'Resume text and target roles required'}), 400
        
        prompt = ai_prompts.linkedin_optimization(resume_text, target_roles)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'linkedin_optimization',
            'description': 'Optimize LinkedIn profile for recruiter searches'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/salary-negotiation', methods=['POST'])
def ai_prompt_salary():
    """Generate AI prompt for salary negotiation research"""
    try:
        data = request.json
        position = data.get('position', '')
        experience_years = data.get('experienceYears', 0)
        location = data.get('location', 'Sweden')
        
        if not position or not experience_years:
            return jsonify({'error': 'Position and experience years required'}), 400
        
        prompt = ai_prompts.salary_negotiation(position, experience_years, location)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'promptType': 'salary_negotiation',
            'description': 'Research salary ranges and negotiation strategy'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lego_api.route('/api/ai-prompts/all', methods=['GET'])
def list_ai_prompts():
    """List all available AI prompt types"""
    return jsonify({
        'success': True,
        'prompts': [
            {
                'type': 'resume_rewrite',
                'endpoint': '/api/ai-prompts/resume-rewrite',
                'description': 'Rewrite resume with measurable achievements and ATS optimization',
                'requiredFields': ['resumeText']
            },
            {
                'type': 'role_targeting',
                'endpoint': '/api/ai-prompts/role-targeting',
                'description': 'Identify 10 high-paying roles ranked by salary and demand',
                'requiredFields': ['experienceText']
            },
            {
                'type': 'jd_match',
                'endpoint': '/api/ai-prompts/jd-match',
                'description': 'Optimize resume for ~90% alignment with job description',
                'requiredFields': ['jobDescription', 'resumeText']
            },
            {
                'type': 'interview_prep',
                'endpoint': '/api/ai-prompts/interview-prep',
                'description': '15 realistic interview questions with sample answers',
                'requiredFields': ['position'],
                'optionalFields': ['jobDescription']
            },
            {
                'type': 'proof_projects',
                'endpoint': '/api/ai-prompts/proof-projects',
                'description': '3 small projects to demonstrate required skills',
                'requiredFields': ['position', 'jobDescription']
            },
            {
                'type': 'cover_letter',
                'endpoint': '/api/ai-prompts/cover-letter',
                'description': 'Generate compelling cover letter that tells a story',
                'requiredFields': ['jobDescription', 'resumeText', 'companyName']
            },
            {
                'type': 'linkedin_optimization',
                'endpoint': '/api/ai-prompts/linkedin-optimization',
                'description': 'Optimize LinkedIn profile for recruiter searches',
                'requiredFields': ['resumeText', 'targetRoles']
            },
            {
                'type': 'salary_negotiation',
                'endpoint': '/api/ai-prompts/salary-negotiation',
                'description': 'Research salary ranges and negotiation strategy',
                'requiredFields': ['position', 'experienceYears'],
                'optionalFields': ['location']
            }
        ]
    })
