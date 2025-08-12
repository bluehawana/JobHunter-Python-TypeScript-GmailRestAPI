#!/usr/bin/env python3
"""
LaTeX PDF Generator - Uses your EXACT LaTeX template for perfect quality
No more ReportLab approximations - this is the real deal!
"""
import os
import subprocess
import tempfile
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def create_latex_pdf(job: Dict[str, Any], latex_template: str = "") -> bytes:
    """Generate PDF using your EXACT LaTeX template - Overleaf quality guaranteed!"""
    try:
        # Your exact LaTeX template
        latex_content = r"""
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
{\Large \textit{ROLE_TITLE_PLACEHOLDER}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

% Personal Profile
\section*{Profile Summary}
PROFILE_SUMMARY_PLACEHOLDER

% Areas of Expertise
\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
SKILLS_PLACEHOLDER
\end{itemize}

% Experience
\section*{Professional Experience}

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

ADDITIONAL_EXPERIENCE_PLACEHOLDER

\section*{Hobby Projects}
PROJECTS_PLACEHOLDER

\section*{Education}
\textbf{IT Högskolan}\\
\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\
\textbf{Mölndal Campus}\\
\textit{Bachelor's Degree in Java Integration} | 2019-2021\\
\textbf{University of Gothenburg}\\
\textit{Master's Degree in International Business and Trade} | 2016-2019\\

\section*{Certifications}
\begin{itemize}
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\end{itemize}

\section*{Additional Information}
\begin{itemize}
\item \textbf{Languages:} Fluent in English and Mandarin
\item \textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\item \textbf{Customer Websites:} \href{https://www.senior798.eu}{senior798.eu}, \href{https://www.mibo.se}{mibo.se}, \href{https://www.omstallningsstod.se}{omstallningsstod.se}
\end{itemize}

\end{document}
"""
        
        # LEGO intelligence - tailor content based on job
        job_title = job.get('title', '').lower()
        job_description = job.get('description', '').lower()
        company = job.get('company', 'Company')
        
        # Determine role focus
        is_devops = any(keyword in job_title + job_description for keyword in 
                       ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
        is_backend = any(keyword in job_title + job_description for keyword in 
                        ['backend', 'api', 'microservices', 'spring', 'java', 'database']) and not is_devops
        is_frontend = any(keyword in job_title + job_description for keyword in 
                         ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui']) and not is_devops and not is_backend
        
        # LEGO role positioning
        if is_devops:
            role_title = "DevOps Engineer \\& Cloud Infrastructure Specialist"
            profile_summary = f"""Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, AWS, Docker, and infrastructure automation. Strong background in migrating from AKS to local Kubernetes clusters, implementing monitoring solutions using Grafana, and managing complex network systems. Demonstrated ability to work across the entire infrastructure stack from cloud platforms to system reliability and enterprise-level technical solution design. Specialized in infrastructure optimization roles for companies like {company}."""
            
            skills = [
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud ECS, Infrastructure as Code",
                r"\item \textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS), Container Orchestration",
                r"\item \textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI, Automated Testing, Deployment Pipelines",
                r"\item \textbf{Infrastructure:} System Integration, Network Management, Cost Optimization, Performance Monitoring",
                r"\item \textbf{Monitoring:} Grafana, Advanced Scripting, System Reliability, Application Performance",
                r"\item \textbf{Programming:} Python, Bash, PowerShell, Java, JavaScript, Go, Infrastructure Automation",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, Database Optimization",
                r"\item \textbf{Security:} Application security, Data protection, Authentication/Authorization, Network Security"
            ]
        elif is_backend:
            role_title = "Backend Developer \\& API Specialist"
            profile_summary = f"""Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, RESTful APIs, and scalable backend systems. Strong background in building comprehensive talent management systems using C\\# and .NET Core, implementing microservices for scalable application architecture, and integrating SQL and NoSQL databases with optimized query performance. Specialized in backend development roles for companies like {company}."""
            
            skills = [
                r"\item \textbf{Programming Languages:} Java/J2EE, C\#/.NET Core, Python, JavaScript, TypeScript, Go",
                r"\item \textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI, Express.js",
                r"\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture, API Gateway",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, Database Design",
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud, Serverless Computing",
                r"\item \textbf{Performance:} Database optimization, Caching strategies, Application scaling, Load Balancing",
                r"\item \textbf{Security:} Application security, Data protection, Authentication/Authorization, OAuth",
                r"\item \textbf{DevOps:} Docker, Kubernetes, Jenkins, GitHub Actions, CI/CD Pipelines"
            ]
        else:
            role_title = "Senior Fullstack Developer"
            profile_summary = f"""Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Strong background in both frontend and backend development, from React and Angular to Spring Boot and .NET Core, with expertise in cloud platforms and DevOps practices. Specialized in end-to-end development roles for companies like {company}."""
            
            skills = [
                r"\item \textbf{Programming Languages:} Java/J2EE, JavaScript, C\#/.NET Core, Python, TypeScript, Bash",
                r"\item \textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                r"\item \textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js, ASP.NET",
                r"\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3",
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud",
                r"\item \textbf{DevOps:} Docker, Kubernetes, Jenkins, GitHub Actions, GitLab CI",
                r"\item \textbf{Methodologies:} Agile, Scrum, Kanban, Sprint Planning, Code Reviews"
            ]
        
        # Additional experience based on role focus
        if is_devops:
            additional_experience = r"""
\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Implemented infrastructure automation and deployment pipelines for enhanced system reliability
\item Collaborated with DevOps teams to optimize application deployment and monitoring strategies
\item Implemented automated testing and continuous integration as part of delivery process
\end{itemize}

\subsection*{AddCell (CTH Startup) | DevOps Engineer}
\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed cloud-native applications using serverless computing architecture
\item Implemented infrastructure as code and automated deployment pipelines
\item Worked with containerization technologies and Kubernetes orchestration
\item Optimized cloud resource usage and implemented cost-effective scaling strategies
\end{itemize}
"""
        else:
            additional_experience = r"""
\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\item Built frontend features using Vue.js framework and integrated with backend APIs
\item Developed RESTful APIs and implemented comprehensive database integration
\item Participated in Agile development processes and collaborated with cross-functional teams
\end{itemize}
"""
        
        # Projects section
        projects = r"""
\subsection{Weather\_Anywhere.CLOUD\_API\_Encoding}
\textit{Feb 2024 -- Present} \\
\textbf{SpringBoot, AlibabaCloudECS, ApsaraDBRDS(MySQL), Heroku}
\begin{itemize}
\item Weather tracking app for Swedish and global cities using OpenCageData and Open-Meteo APIs
\item Deployed on Alibaba Cloud ECS with city coordinates and weather data stored in ApsaraDB MySQL
\item Dynamic city lookup and caching mechanism for optimized API usage and response speed
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection{Jobhunter\_Python\_TypeScript\_RESTAPI}
\textit{July 2024 -- Present} \\
\textbf{Python, TypeScript, GmailRESTAPI, LinkedinAPI}
\begin{itemize}
\item Automated job hunting pipeline integrating Gmail search, job scraping, and resume customization
\item Generated resumes and cover letters based on job descriptions using NLP techniques
\item Auto-sent job application drafts to user with a fully functional end-to-end workflow
\item Demo: https://jobs.bluehawana.com
\end{itemize}

\subsection{Gothenburg\_TaxiPooling\_Java\_ReactNative\_PythonALGO}
\textit{May 2024 -- Present} \\
\textbf{SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL}
\begin{itemize}
\item Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking
\item Developed cross-platform mobile application using React Native and Spring Boot microservices
\item Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling
\item Engineered for performance optimization and GDPR-compliant data privacy
\end{itemize}
"""
        
        # Replace placeholders with LEGO-tailored content
        latex_content = latex_content.replace("ROLE_TITLE_PLACEHOLDER", role_title)
        latex_content = latex_content.replace("PROFILE_SUMMARY_PLACEHOLDER", profile_summary)
        latex_content = latex_content.replace("SKILLS_PLACEHOLDER", "\n".join(skills))
        latex_content = latex_content.replace("ADDITIONAL_EXPERIENCE_PLACEHOLDER", additional_experience)
        latex_content = latex_content.replace("PROJECTS_PLACEHOLDER", projects)
        
        # Create temporary directory for LaTeX compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, "resume.tex")
            pdf_file = os.path.join(temp_dir, "resume.pdf")
            
            # Write LaTeX content to file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF (run twice for proper references)
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                    capture_output=True, text=True
                )
                
                if result.returncode != 0:
                    logger.error(f"LaTeX compilation failed: {result.stderr}")
                    return b""
            
            # Read the generated PDF
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as f:
                    pdf_content = f.read()
                
                logger.info(f"🎉 PERFECT LaTeX PDF: Generated {role_title} resume for {company} ({len(pdf_content)} bytes)")
                logger.info(f"✅ OVERLEAF QUALITY - This is your exact LaTeX template!")
                return pdf_content
            else:
                logger.error("PDF file was not generated")
                return b""
                
    except Exception as e:
        logger.error(f"❌ Error creating LaTeX PDF: {e}")
        return b""

if __name__ == "__main__":
    # Test the LaTeX PDF generator
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'Volvo Group',
        'description': 'Kubernetes, AWS, Docker, infrastructure automation, CI/CD pipelines'
    }
    
    pdf_content = create_latex_pdf(test_job)
    
    if pdf_content:
        with open('test_latex_resume.pdf', 'wb') as f:
            f.write(pdf_content)
        print(f"✅ Generated LaTeX resume: {len(pdf_content)} bytes")
    else:
        print("❌ Failed to generate PDF")