#!/usr/bin/env python3
"""
Enhanced JobHunter processor with:
1. Proper 3-page CV maintaining all content
2. Job-specific experience tailoring (DevOps vs Backend vs Fullstack focus)
3. Enhanced hobby projects section
4. Send both PDF and LaTeX files for review
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EnhancedJobProcessor:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "bluehawanan@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = "leeharvad@gmail.com"
    
    def create_enhanced_cv(self, job_title, company, role_focus):
        """Create enhanced 3-page CV with job-specific tailoring"""
        
        # Role-specific profile summaries
        profile_summaries = {
            'devops': f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of hands-on experience in cloud platforms, containerization, and CI/CD automation. Proven expertise in Kubernetes, Docker, AWS/Azure, and infrastructure optimization. Strong background in system reliability, monitoring solutions, and cost optimization strategies. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure projects and implementing modern DevOps practices for {company}-type automotive technology solutions.",
            
            'backend': f"Experienced Backend Developer with over 5 years of specialized expertise in server-side technologies, microservices architecture, and database optimization. Proven track record in Java/Spring Boot, RESTful API development, and scalable backend systems. Strong background in PostgreSQL, MongoDB, and cloud-native application development. Currently serving as IT/Infrastructure Specialist at ECARX, focusing on backend infrastructure and system integration for {company}-style enterprise applications.",
            
            'frontend': f"Experienced Frontend Developer with strong fullstack capabilities and over 5 years of hands-on experience in modern web technologies and user interface development. Proven expertise in Angular, React, Vue.js, and responsive application design with seamless backend integration. Strong background in JavaScript/TypeScript, component-based architecture, and performance optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing frontend excellence and user experience focus ideal for {company} development initiatives.",
            
            'fullstack': f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} full-stack development requirements."
        }
        
        # Role-specific skills highlighting
        skills_sections = {
            'devops': """\\item \\textbf{DevOps \\& Infrastructure:} Kubernetes, Docker, Jenkins, GitHub Actions, Terraform, Infrastructure as Code
\\item \\textbf{Cloud Platforms:} AWS (EC2, RDS, S3, Lambda), Azure (AKS, Cosmos DB), GCP, Cloud Architecture
\\item \\textbf{Monitoring \\& Reliability:} Grafana, Prometheus, ELK Stack, System Monitoring, Performance Optimization
\\item \\textbf{Automation \\& Scripting:} Python, Bash, PowerShell, CI/CD Pipelines, Deployment Automation
\\item \\textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS), Container Orchestration
\\item \\textbf{Programming Languages:} Java/J2EE, Python, JavaScript, C\\#/.NET Core (for tooling and automation)
\\item \\textbf{Database Management:} PostgreSQL, MySQL, MongoDB, Database Optimization, Backup Strategies""",
            
            'backend': """\\item \\textbf{Backend Development:} Java/J2EE, Spring Boot, Spring MVC, Microservices Architecture
\\item \\textbf{API Development:} RESTful APIs, GraphQL, API Design, Documentation, Swagger/OpenAPI
\\item \\textbf{Database Expertise:} PostgreSQL, MySQL, MongoDB, Redis, Query Optimization, Schema Design
\\item \\textbf{Framework Proficiency:} Spring Framework, .NET Core, Node.js, Backend Architecture Patterns
\\item \\textbf{Performance \\& Scaling:} Application Optimization, Caching Strategies, Load Balancing
\\item \\textbf{Cloud \\& Infrastructure:} AWS, Azure, Docker, Kubernetes, Cloud-native Development
\\item \\textbf{Testing \\& Quality:} Unit Testing, Integration Testing, JUnit, Automated Testing, TDD""",
            
            'frontend': """\\item \\textbf{Frontend Frameworks:} Angular, ReactJS, Vue.js, React Native, Modern JavaScript/TypeScript
\\item \\textbf{UI/UX Development:} HTML5, CSS3, Responsive Design, Component Architecture, State Management
\\item \\textbf{Build Tools \\& Workflows:} Webpack, NPM, Yarn, Modern Build Pipelines, Performance Optimization
\\item \\textbf{Backend Integration:} RESTful API Consumption, GraphQL, Real-time Communication, WebSockets
\\item \\textbf{Mobile Development:} React Native, Cross-platform Applications, Mobile-first Design
\\item \\textbf{Programming Languages:} JavaScript, TypeScript, Java/J2EE, C\\# (for full-stack integration)
\\item \\textbf{Testing \\& Quality:} Jest, Cypress, Frontend Testing, Component Testing, E2E Testing""",
            
            'fullstack': """\\item \\textbf{Programming Languages:} Java/J2EE, JavaScript, TypeScript, C\\#/.NET Core, Python, Bash
\\item \\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
\\item \\textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
\\item \\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture
\\item \\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
\\item \\textbf{Cloud Platforms:} AWS, Azure, GCP, Docker, Kubernetes, Cloud-native Development
\\item \\textbf{DevOps \\& CI/CD:} Jenkins, GitHub Actions, GitLab CI, Infrastructure Automation"""
        }
        
        # Get role-specific content
        profile = profile_summaries.get(role_focus, profile_summaries['fullstack'])
        skills = skills_sections.get(role_focus, skills_sections['fullstack'])
        
        # Enhanced hobby projects section
        hobby_projects = """\\section*{Hobby Projects}

\\subsection*{Gothenburg TaxiCarPooling Web Application}
\\textit{May 2025 - Present | Full-Stack Development}
\\begin{itemize}[noitemsep]
\\item Developing intelligent carpooling platform using \\textbf{Spring Boot} backend with microservices architecture
\\item Cross-platform mobile application built with \\textbf{React Native}, integrating payment and geolocation services
\\item Backend API development with \\textbf{Node.js} microservices for real-time order matching and communication
\\item Database design and optimization using \\textbf{MySQL} with complex relational data modeling
\\item Cloud deployment on \\textbf{Heroku} with automated CI/CD pipelines and environment management
\\item Implemented automated order matching algorithm with real-time notifications and GPS tracking
\\item RESTful API design for mobile app integration with comprehensive authentication and authorization
\\item Built comprehensive automated testing suite ensuring data protection and GDPR compliance
\\item Real-time chat integration, payment processing, and advanced route optimization algorithms
\\end{itemize}

\\subsection*{Kotlin Car IPTV Player Application}
\\textit{March 2025 - Present | Android Development}
\\begin{itemize}[noitemsep]
\\item Developing Android Auto-compatible IPTV streaming application using \\textbf{Kotlin} and Android SDK
\\item Advanced media streaming with support for multiple video formats and adaptive bitrate streaming
\\item Integration with vehicle's infotainment system following Android Auto development guidelines
\\item Real-time data processing for voice command integration and hands-free operation
\\item Backend services built with \\textbf{Java} for content management and streaming optimization
\\item Secure API integrations with SQL database optimization for media content and user preferences
\\item Comprehensive testing framework covering both mobile and automotive use cases
\\item UI/UX designed specifically for automotive environment with safety and usability focus
\\end{itemize}

\\subsection*{JobHunter - AI-Powered Job Application Automation}
\\textit{Current Project | Full-Stack \\& DevOps}
\\begin{itemize}[noitemsep]
\\item Comprehensive job application automation system with intelligent job matching and application generation
\\item Backend API built with \\textbf{Python FastAPI}, integrating LinkedIn, Indeed, and Arbetsförmedlingen APIs
\\item Frontend dashboard developed with \\textbf{React} and \\textbf{TypeScript} for job management and analytics
\\item Database architecture using \\textbf{Supabase (PostgreSQL)} with complex job matching algorithms
\\item Email automation system with Gmail API integration for job alerts and application tracking
\\item LaTeX document generation system creating tailored CVs and cover letters for each application
\\item Multi-source job aggregation with intelligent filtering and priority-based application processing
\\item Complete DevOps pipeline with automated testing, deployment, and monitoring
\\end{itemize}

\\subsection*{EPUB to Voice Book Reader for Android Auto}
\\textit{February 2025 - Present | Mobile \\& AI Development}
\\begin{itemize}[noitemsep]
\\item Android Auto application converting EPUB books to audio using advanced text-to-speech technology
\\item Intelligent content parsing and natural voice synthesis with multiple language support
\\item Voice command integration for hands-free book navigation and playbook control
\\item Background processing capabilities allowing continuous audio playback during driving
\\item Integration with vehicle's audio system and steering wheel controls
\\item Advanced bookmark and progress tracking with cloud synchronization
\\item Offline functionality with local storage optimization for long journeys
\\item Custom audio processing algorithms for optimal listening experience in vehicle environment
\\end{itemize}

\\subsection*{Personal Website Transformation (bluehawana.com)}
\\textit{January 2025 - Present | Full-Stack Web Development}
\\begin{itemize}[noitemsep]
\\item Complete website transformation from static HTML to dynamic full-stack application
\\item Frontend rebuilt with modern \\textbf{React} and \\textbf{TypeScript} with responsive design
\\item Backend API development using \\textbf{Node.js} and \\textbf{Express} with RESTful architecture
\\item Database integration with \\textbf{MongoDB} for dynamic content management and blog functionality
\\item Advanced SEO optimization and performance enhancements achieving 95+ Lighthouse scores
\\item Integration with multiple APIs for portfolio showcase, blog management, and contact functionality
\\item CI/CD pipeline setup with automated testing and deployment to cloud hosting
\\item Progressive Web App (PWA) features with offline capabilities and mobile optimization
\\item Custom CMS development for easy content management and blog posting
\\end{itemize}

\\subsection*{E-commerce Platform (smrtmart.com)}
\\textit{April 2024 - Present | Enterprise Development}
\\begin{itemize}[noitemsep]
\\item Full-scale e-commerce platform with \\textbf{Spring Boot} backend and \\textbf{React} frontend
\\item Microservices architecture with \\textbf{PostgreSQL} and \\textbf{MongoDB} database integration
\\item Comprehensive order management system with inventory tracking and automated workflows
\\item Payment processing integration with multiple providers and fraud detection systems
\\item RESTful API development for frontend-backend communication and third-party integrations
\\item Advanced search functionality with Elasticsearch integration and recommendation algorithms
\\item Real-time analytics dashboard with sales reporting and business intelligence features
\\item Mobile-responsive design with PWA capabilities for enhanced user experience
\\end{itemize}"""
        
        # Role-specific experience tailoring
        experience_sections = self.get_role_specific_experience(role_focus)
        
        cv_template = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}

% Page setup
\\geometry{{margin=0.75in}}
\\pagestyle{{empty}}

% Color definitions
\\definecolor{{linkedinblue}}{{RGB}}{{0,119,181}}
\\definecolor{{lightgray}}{{RGB}}{{128,128,128}}

% Hyperlink setup
\\hypersetup{{
    colorlinks=true,
    linkcolor=linkedinblue,
    urlcolor=linkedinblue,
    citecolor=linkedinblue
}}

% Section formatting
\\titleformat{{\\section}}{{\\Large\\bfseries\\color{{linkedinblue}}}}{{}}{{0em}}{{}}[\\titlerule]
\\titleformat{{\\subsection}}{{\\large\\bfseries}}{{}}{{0em}}{{}}

\\begin{{document}}

% Name and contact details
\\begin{{center}}
{{\\LARGE \\textbf{{Hongzhi Li}}}}\\\\[10pt]
{{\\Large \\textit{{{job_title}}}}}\\\\[10pt]
\\textcolor{{linkedinblue}}{{\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} | \\href{{tel:0728384299}}{{0728384299}} | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

% Personal Profile
\\section*{{Profile Summary}}
{profile}

% Areas of Expertise
\\section*{{Core Technical Skills}}
\\begin{{itemize}}[noitemsep]
{skills}
\\item \\textbf{{Testing:}} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest
\\item \\textbf{{Version Control:}} Git, GitHub, GitLab
\\item \\textbf{{Agile Methodologies:}} Scrum, Kanban, Sprint Planning, Code Reviews
\\item \\textbf{{Performance Optimization:}} Application scaling, Database optimization, Caching strategies
\\item \\textbf{{Security:}} Application security, Data protection, Authentication/Authorization
\\end{{itemize}}

% Experience
\\section*{{Professional Experience}}
{experience_sections}

{hobby_projects}

\\section*{{Education}}
\\textbf{{IT Högskolan}}\\\\
\\textit{{Bachelor's Degree in .NET Cloud Development}} | 2021-2023\\\\
\\textbf{{Mölndal Campus}}\\\\
\\textit{{Bachelor's Degree in Java Integration}} | 2019-2021\\\\
\\textbf{{University of Gothenburg}}\\\\
\\textit{{Master's Degree in International Business and Trade}} | 2016-2019\\\\

\\section*{{Certifications}}
\\begin{{itemize}}[noitemsep]
\\item AWS Certified Solutions Architect - Associate (Aug 2022)
\\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\\item AWS Certified Developer - Associate (Nov 2022)
\\end{{itemize}}

\\section*{{Additional Information}}
\\begin{{itemize}}[noitemsep]
\\item \\textbf{{Languages:}} Fluent in English and Mandarin
\\item \\textbf{{Interests:}} Vehicle technology, energy sector, electrical charging systems, and battery technology
\\item \\textbf{{Personal Website:}} \\href{{https://www.bluehawana.com}}{{bluehawana.com}}
\\item \\textbf{{Customer Websites:}} \\href{{https://www.senior798.eu}}{{senior798.eu}}, \\href{{https://www.mibo.se}}{{mibo.se}}, \\href{{https://www.omstallningsstod.se}}{{omstallningsstod.se}}
\\end{{itemize}}

\\end{{document}}"""
        
        return cv_template
    
    def get_role_specific_experience(self, role_focus):
        """Get work experience tailored to specific role focus"""
        
        if role_focus == 'devops':
            return """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\\item Implementing cost optimization by migrating from AKS to local Kubernetes cluster, reducing operational expenses by 40\\%
\\item Implementing modern monitoring solutions using Grafana, Prometheus, and advanced scripting for system reliability
\\item Managing complex network systems and providing DevOps solution design for enterprise-level applications
\\item Automating deployment pipelines and implementing Infrastructure as Code practices
\\end{itemize}

\\subsection*{Synteda | Azure Cloud DevOps Engineer \\& Infrastructure Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native talent management system with comprehensive Azure infrastructure automation
\\item Implemented containerized microservices architecture with Docker and Kubernetes deployment strategies
\\item Built automated CI/CD pipelines using Azure DevOps and GitHub Actions for continuous deployment
\\item Designed and implemented infrastructure monitoring, logging, and alerting systems
\\end{itemize}

\\subsection*{IT-Högskolan | DevOps \\& Backend Developer (Part-time)}
\\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Migrated "Omstallningsstod.se" platform with focus on deployment automation and infrastructure optimization
\\item Implemented automated testing and deployment pipelines as part of DevOps transformation
\\item Collaborated with infrastructure teams to ensure seamless CI/CD integration and system reliability
\\item Designed monitoring and logging solutions for production environment stability
\\end{itemize}

\\subsection*{Senior Material (Europe) AB | Platform Infrastructure Architect \\& DevOps Coordinator}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Led migration of business-critical applications with focus on containerization and orchestration
\\item Designed and implemented scalable infrastructure architecture using modern DevOps practices
\\item Optimized deployment processes and implemented automated scaling solutions for maximum efficiency
\\item Established monitoring, alerting, and incident response procedures for production systems
\\end{itemize}

\\subsection*{AddCell (CTH Startup) | DevOps Engineer}
\\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native applications using serverless computing architecture and infrastructure automation
\\item Implemented comprehensive monitoring, logging, and deployment automation for startup infrastructure
\\item Designed scalable cloud infrastructure with cost optimization and performance monitoring
\\end{itemize}

\\subsection*{Pembio AB | DevOps \\& Fullstack Developer}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed Pembio.com platform with emphasis on deployment automation and infrastructure management
\\item Implemented comprehensive testing frameworks and automated deployment pipelines
\\item Designed monitoring and alerting systems for production environment reliability and performance
\\item Collaborated with development teams to implement DevOps best practices and CI/CD workflows
\\end{itemize}"""
        
        elif role_focus == 'backend':
            return """\\subsection*{ECARX | Backend Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading backend system optimization and integration projects for automotive technology solutions
\\item Developing scalable microservices architecture and API design for enterprise-level applications
\\item Implementing database optimization strategies and performance tuning for high-traffic backend systems
\\item Managing complex data processing systems and backend service reliability for mission-critical applications
\\end{itemize}

\\subsection*{Synteda | Senior Backend Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed comprehensive talent management system using C\\# and .NET Core with microservices architecture
\\item Built scalable backend APIs handling complex business logic for office management platform
\\item Implemented RESTful APIs and GraphQL services for high-performance application architecture
\\item Integrated SQL and NoSQL databases with advanced query optimization and data protection measures
\\end{itemize}

\\subsection*{IT-Högskolan | Senior Backend Developer (Part-time)}
\\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Migrated "Omstallningsstod.se" adult education platform using advanced Spring Boot backend architecture
\\item Developed complex RESTful APIs for frontend integration with secure data handling and authentication
\\item Implemented comprehensive database design and optimization for educational content management
\\item Designed scalable backend architecture supporting thousands of concurrent users
\\end{itemize}

\\subsection*{Senior Material (Europe) AB | Backend Platform Architect \\& API Coordinator}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Led migration of business-critical applications with focus on backend microservices architecture
\\item Developed high-performance backend services with Spring Boot and designed RESTful APIs for frontend consumption
\\item Implemented advanced database optimization and caching strategies for maximum performance and scalability
\\item Architected API gateway solutions and service mesh infrastructure for complex enterprise applications
\\end{itemize}

\\subsection*{AddCell (CTH Startup) | Backend \\& API Developer}
\\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native backend applications using serverless computing and microservices architecture
\\item Implemented advanced GraphQL APIs for efficient data fetching and optimized database interactions
\\item Designed scalable database schemas and implemented complex query optimization for SQL and NoSQL systems
\\end{itemize}

\\subsection*{Pembio AB | Senior Backend Developer}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed Pembio.com platform backend with Java and Spring Boot in advanced microservices architecture
\\item Designed and implemented complex RESTful APIs with comprehensive authentication and authorization systems
\\item Built scalable database integration with PostgreSQL and MongoDB, including advanced query optimization
\\item Implemented comprehensive testing strategies including unit, integration, and performance testing
\\end{itemize}"""
        
        else:  # fullstack or default
            return """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\\item Providing IT support and infrastructure support to development teams for enhanced productivity
\\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\\item Managing complex network systems and providing technical solution design for enterprise-level applications
\\end{itemize}

\\subsection*{Synteda | Azure Fullstack Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed comprehensive talent management system using C\\# and .NET Core with cloud-native architecture
\\item Built complete office management platform from scratch, architecting both frontend and backend components
\\item Implemented RESTful APIs and microservices for scalable application architecture
\\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\\end{itemize}

\\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\\item Developed RESTful APIs for frontend integration and implemented secure data handling
\\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\\item Implemented automated tests as part of delivery process
\\end{itemize}

\\subsection*{Senior Material (Europe) AB | Platform Architect \\& Project Coordinator}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Led migration of business-critical applications with microservices architecture
\\item Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption
\\item Collaborated with development teams to optimize applications for maximum speed and scalability
\\item Participated in Agile ceremonies including sprint planning, reviews, and retrospectives
\\end{itemize}

\\subsection*{AddCell (CTH Startup) | DevOps Engineer}
\\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native applications using serverless computing architecture
\\item Implemented GraphQL APIs for efficient data fetching and frontend integration
\\item Worked with SQL and NoSQL databases for optimal data storage and retrieval
\\end{itemize}

\\subsection*{Pembio AB | Fullstack Developer}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\\item Built frontend features using Vue.js framework and integrated with backend APIs
\\item Developed RESTful APIs and implemented comprehensive database integration
\\item Participated in Agile development processes and collaborated with cross-functional teams
\\item Implemented automated testing strategies and ensured application security
\\end{itemize}"""
    
    def create_enhanced_cover_letter(self, job_title, company, role_focus):
        """Create enhanced cover letter with role-specific focus"""
        
        # Role-specific introductions
        intro_paragraphs = {
            'devops': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in DevOps engineering and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in infrastructure automation, cloud platforms, and cost optimization strategies to your team. My recent achievement of reducing operational expenses by 40% through AKS to Kubernetes migration demonstrates my ability to deliver tangible results in infrastructure optimization.",
            
            'backend': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of specialized experience in backend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Java/Spring Boot, microservices architecture, and scalable backend systems to your team. My experience developing high-performance APIs and database optimization strategies aligns perfectly with your backend development requirements.",
            
            'frontend': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in frontend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Angular, React, and modern web technologies to your team. My experience building responsive applications and seamless user experiences makes me an ideal candidate for your frontend development initiatives.",
            
            'fullstack': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for end-to-end software solutions to your team."
        }
        
        # Role-specific project highlights
        project_highlights = {
            'devops': "My recent projects demonstrate strong DevOps capabilities: implementing cost-effective Kubernetes migrations, building comprehensive monitoring solutions with Grafana, and developing automated CI/CD pipelines. The Gothenburg TaxiCarPooling project showcases my ability to design cloud infrastructure on Heroku with automated deployment, while the JobHunter automation platform demonstrates my skills in building scalable DevOps workflows and infrastructure management.",
            
            'backend': "My recent projects demonstrate strong backend development capabilities: building microservices architecture for the Gothenburg TaxiCarPooling platform using Spring Boot and Node.js, developing RESTful APIs with MySQL optimization, and creating scalable backend systems. The JobHunter project showcases my ability to design complex API integrations and database architectures, while my e-commerce platform demonstrates enterprise-level backend development skills.",
            
            'frontend': "My recent projects demonstrate strong frontend development capabilities: building cross-platform mobile applications with React Native for the Gothenburg TaxiCarPooling project, developing responsive web interfaces with React and TypeScript, and creating intuitive user experiences. My personal website transformation from static to dynamic showcases modern frontend development skills, while the Android Auto applications demonstrate my ability to create specialized user interfaces for different platforms.",
            
            'fullstack': "My recent projects demonstrate comprehensive fullstack capabilities: developing the Gothenburg TaxiCarPooling platform with Spring Boot backend and React Native frontend, building the JobHunter automation system with Python FastAPI and React, and transforming my personal website into a dynamic full-stack application. These projects showcase my ability to work across the entire technology stack from database design to user interface development."
        }
        
        intro = intro_paragraphs.get(role_focus, intro_paragraphs['fullstack'])
        projects = project_highlights.get(role_focus, project_highlights['fullstack'])
        
        cl_template = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}

% Page setup
\\geometry{{margin=1in}}
\\pagestyle{{empty}}

% Color definitions
\\definecolor{{linkedinblue}}{{RGB}}{{0,119,181}}

\\hypersetup{{
    colorlinks=true,
    linkcolor=linkedinblue,
    urlcolor=linkedinblue,
    citecolor=linkedinblue
}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{10pt}}

\\begin{{document}}

% Header
\\begin{{center}}
{{\\LARGE \\textbf{{\\textcolor{{linkedinblue}}{{Hongzhi Li}}}}}}\\\\
\\vspace{{5pt}}
{{\\large \\textcolor{{linkedinblue}}{{Fullstack Developer}}}}\\\\
\\vspace{{10pt}}
\\textcolor{{linkedinblue}}{{\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} | \\href{{tel:0728384299}}{{0728384299}} | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

\\vspace{{20pt}}

\\today

{company} Hiring Team\\\\
{company}\\\\
Hiring Department

\\vspace{{20pt}}

\\textbf{{\\textcolor{{linkedinblue}}{{Subject: Application for {job_title} Position}}}}

Dear Hiring Manager,

{intro}

{projects}

What particularly excites me about {company} is your commitment to innovative technology solutions. My experience spans from automotive technology at ECARX to freelance cloud-native development at Synteda, giving me valuable insight into building scalable, enterprise-level applications across different industries. I have consistently delivered projects that improve system reliability, reduce operational costs, and enhance user experience.

\\textbf{{\\textcolor{{linkedinblue}}{{Key technical highlights include:}}}}
\\begin{{itemize}}[noitemsep]
\\item Comprehensive project portfolio demonstrating {role_focus} expertise with real-world applications
\\item Proven track record in building scalable systems serving thousands of users
\\item Strong experience with modern development practices, testing, and deployment automation
\\item Active GitHub portfolio showcasing continuous learning and innovative project development
\\item AWS and Azure certifications with practical cloud development and deployment experience
\\end{{itemize}}

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals, combined with my hands-on project experience, position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience and passion for {role_focus} development can contribute to {company}'s continued success. Thank you for considering my application.

\\vspace{{20pt}}

Best regards,

Hongzhi Li

\\end{{document}}"""
        
        return cl_template
    
    def determine_role_focus(self, title):
        """Determine role focus from job title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['devops', 'infrastructure', 'sre', 'platform', 'cloud engineer']):
            return 'devops'
        elif any(word in title_lower for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
        elif any(word in title_lower for word in ['frontend', 'react', 'angular', 'ui', 'ux']):
            return 'frontend'
        else:
            return 'fullstack'
    
    def compile_latex(self, tex_content, output_name):
        """Compile LaTeX to PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            try:
                # Run twice for proper references and page breaks
                for i in range(2):
                    result = subprocess.run([
                        'pdflatex', 
                        '-interaction=nonstopmode',
                        '-output-directory', str(temp_path),
                        str(tex_file)
                    ], capture_output=True, text=True, cwd=temp_path)
                    
                    if result.returncode != 0 and i == 1:
                        print(f"❌ LaTeX compilation failed for {output_name}")
                        return None
                
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    return final_path
                
            except Exception as e:
                print(f"❌ Error compiling {output_name}: {e}")
                return None
    
    def save_latex_files(self, cv_content, cl_content, job_title, company):
        """Save LaTeX source files for review"""
        company_safe = company.lower().replace(' ', '_').replace('.', '')
        title_safe = job_title.lower().replace(' ', '_')
        
        cv_tex_path = f"hongzhi_{title_safe}_{company_safe}_cv.tex"
        cl_tex_path = f"hongzhi_{title_safe}_{company_safe}_cl.tex"
        
        with open(cv_tex_path, 'w', encoding='utf-8') as f:
            f.write(cv_content)
        
        with open(cl_tex_path, 'w', encoding='utf-8') as f:
            f.write(cl_content)
        
        return cv_tex_path, cl_tex_path
    
    def send_enhanced_email(self, job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex):
        """Send email with both PDF and LaTeX files for review"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Review: {job_title} at {company} - PDF + LaTeX Files"
            
            body = f"""Hi,

New tailored job application ready for your review:

🏢 Company: {company}
💼 Position: {job_title}
📍 Priority: {'🏢 Gothenburg' if 'gothenburg' in company.lower() else '🌐 Remote/Other'}

📎 Files attached:
   • CV (PDF) - Ready to send
   • Cover Letter (PDF) - Ready to send  
   • CV (LaTeX source) - For your review/editing
   • Cover Letter (LaTeX source) - For your review/editing

🎯 This application has been tailored specifically for this {job_title.lower()} role with:
   ✅ Role-specific experience highlighting
   ✅ Enhanced 3-page format with complete hobby projects
   ✅ Dark blue (LinkedIn) colors
   ✅ ATS-optimized formatting

📝 Review Process:
   1. Check the PDF files for content and formatting
   2. Edit LaTeX source files if needed for final polish
   3. Recompile if you make changes
   4. Send final application manually or approve automation

Best regards,
JobHunter Automation System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach all files
            attachments = [
                (cv_pdf, f"CV_{company}_{job_title}.pdf"),
                (cl_pdf, f"CoverLetter_{company}_{job_title}.pdf"),
                (cv_tex, f"CV_{company}_{job_title}.tex"),
                (cl_tex, f"CoverLetter_{company}_{job_title}.tex")
            ]
            
            for file_path, filename in attachments:
                if Path(file_path).exists():
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            server.quit()
            
            print(f"✅ Enhanced email sent for {job_title} at {company}")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Test enhanced processor"""
    processor = EnhancedJobProcessor()
    
    # Test jobs
    test_jobs = [
        ("DevOps Engineer", "Volvo Cars"),
        ("Senior Backend Developer", "Spotify"),
        ("Fullstack Developer", "SKF Group")
    ]
    
    print("🚀 Enhanced JobHunter with 3-Page CVs and LaTeX Sources")
    print("=" * 60)
    
    for job_title, company in test_jobs:
        print(f"\\n📋 Processing: {job_title} at {company}")
        
        role_focus = processor.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        # Generate documents
        cv_content = processor.create_enhanced_cv(job_title, company, role_focus)
        cl_content = processor.create_enhanced_cover_letter(job_title, company, role_focus)
        
        # Save LaTeX files
        cv_tex, cl_tex = processor.save_latex_files(cv_content, cl_content, job_title, company)
        
        # Compile PDFs
        cv_pdf = processor.compile_latex(cv_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
        cl_pdf = processor.compile_latex(cl_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
        
        if cv_pdf and cl_pdf:
            # Send enhanced email with both PDF and LaTeX
            success = processor.send_enhanced_email(job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex)
            
            if success:
                print(f"🎉 SUCCESS: Both PDF and LaTeX files sent for review")
                
                # Clean up PDF files but keep LaTeX for review
                try:
                    os.remove(cv_pdf)
                    os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"❌ FAILED: Email not sent")
        else:
            print(f"❌ FAILED: PDF compilation failed")
        
        await asyncio.sleep(2)
    
    print(f"\\n📧 Check {processor.recipient_email} for enhanced applications!")

if __name__ == "__main__":
    asyncio.run(main())