#!/usr/bin/env python3
"""
CV LEGO Bricks System
Dynamically builds CV sections based on job requirements
"""

class CVLegoBricks:
    """LEGO bricks approach to CV building - modular, reusable components"""
    
    def __init__(self):
        self.profile_bricks = {
            'android_developer': """Experienced Android Developer with 6+ years of hands-on experience (2019-Present) in native Android development using Kotlin and Java. Proven expertise in building scalable mobile applications with Android Studio, deep understanding of Android SDK and platform architecture. Strong background in system-level Android components including Activities, Services, Content Providers, and Broadcast Receivers. Demonstrated ability to work with automotive infotainment systems and in-car applications. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep Android development knowledge to automotive technology solutions. Experience spans across ECARX, Synteda, CollabMaker, and Pembio.""",
            
            'ios_developer': """Experienced iOS Developer with 6+ years of software development experience (2019-Present) including mobile application development. Strong foundation in Swift, Objective-C, and iOS SDK with proven ability to build scalable mobile applications. Background in full-stack development provides comprehensive understanding of mobile-backend integration, RESTful APIs, and cloud services. Experience with modern iOS architecture patterns (MVVM, Clean Architecture) and continuous integration/deployment for mobile apps.""",
            
            'fullstack_developer': """Experienced Fullstack Developer with 6+ years of hands-on experience (2019-Present) in Java/J2EE and .NET development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, .NET Core, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, cloud deployment (AWS, Azure), and DevOps practices including CI/CD pipelines, Docker, and Kubernetes. Experience spans across ECARX, Synteda, IT-Högskolan, Senior Material, AddCell, Pembio, and CollabMaker.""",
            
            'backend_developer': """Backend Developer with 6+ years of hands-on experience (2019-Present) building enterprise applications and microservices. Strong expertise in Java/Spring Boot and .NET Core with deep database optimization skills (PostgreSQL, MongoDB, Redis, SQL Server). Proven track record designing RESTful APIs handling millions of requests with focus on performance, scalability, and security. Extensive experience with cloud platforms (AWS, Azure), Docker, Kubernetes, and CI/CD pipelines. Experience spans across ECARX, Synteda, IT-Högskolan, Senior Material, AddCell, and Pembio.""",
            
            'frontend_developer': """Frontend Developer with 6+ years of software development experience (2019-Present) including extensive frontend work with React, Angular, Vue.js, and TypeScript. Expert in building responsive, performant user interfaces with modern JavaScript frameworks and state management solutions. Strong background in full-stack development provides deep understanding of API integration, backend communication, and end-to-end application architecture. Experience with cloud deployment, CI/CD pipelines, and DevOps practices. Experience spans across ECARX, Synteda, Senior Material, Pembio, and CollabMaker.""",
            
            'app_developer': """Mobile and Web Application Developer with 6+ years of experience (2019-Present) building cross-platform and native applications. Expert in React Native, Android (Kotlin/Java), and modern web technologies (React, TypeScript). Strong background in full-stack development with backend API integration, cloud services (AWS, Azure), and DevOps practices. Proven ability to deliver scalable applications with focus on user experience, performance optimization, and continuous deployment. Experience spans across ECARX, Synteda, Senior Material, Pembio, and CollabMaker.""",
            
            'devops_cloud_engineer': """DevOps and Cloud Engineer with 6+ years of experience (2019-Present) building cloud-native infrastructure, CI/CD pipelines, and automated deployment systems. Expert in AWS, Azure, Kubernetes, Docker, Terraform, and Infrastructure as Code. Proven track record managing production systems with 24/7 on-call support, reducing cloud costs by 45%, and implementing comprehensive monitoring solutions. Strong background in both development and operations, bridging the gap between software engineering and infrastructure management. Experience spans across ECARX, Synteda, IT-Högskolan, Senior Material, AddCell, Pembio, and CollabMaker.""",
            
            'it_business_analyst': """IT Business Analyst with 6+ years of combined business and technical experience (2019-Present). Master's in International Business & Trade combined with hands-on IT development experience across multiple companies. Expert at bridging the gap between technical IT systems and business requirements. Proven track record translating complex business needs into technical specifications, leading requirements workshops, and driving digital transformation. Strong analytical skills with deep understanding of both technical implementation (cloud platforms, databases, APIs) and business/commercial impact. Experience spans across ECARX, Synteda, Senior Material, Pembio, and entrepreneurship at Hong Yan AB.""",
            
            'mobile_developer': """Mobile Developer with 6+ years of software development experience (2019-Present) including native and cross-platform mobile development. Strong background in Android development using Kotlin and Java, with additional experience in React Native for cross-platform solutions. Proven ability to build scalable mobile applications with focus on user experience, performance optimization, and cloud integration. Experience with CI/CD pipelines, DevOps practices, and modern mobile architecture patterns. Experience spans across ECARX, Synteda, Pembio, and CollabMaker."""
        }
        
        self.skills_bricks = {
            'android_primary': """\\begin{itemize}[noitemsep]
\\item \\textbf{Mobile Development:} Android (5+ years), Kotlin, Java, Android Studio
\\item \\textbf{Android Framework:} Activities, Services, Content Providers, Broadcast Receivers, Intents
\\item \\textbf{Android SDK:} Platform Architecture, System-level Components, UI/UX Design
\\item \\textbf{Mobile Architecture:} MVVM, MVP, Clean Architecture, Dependency Injection
\\item \\textbf{Database Integration:} SQLite, Room, PostgreSQL, MongoDB integration
\\item \\textbf{API Integration:} RESTful APIs, Real-time data processing, JSON/XML parsing
\\item \\textbf{Voice Processing:} Text-to-Speech (TTS), Wake-word detection, Voice commands
\\item \\textbf{Real-time Systems:} Geolocation tracking, Live data updates, Push notifications
\\item \\textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit
\\item \\textbf{Version Control:} Git, GitHub, GitLab
\\item \\textbf{Learning Areas:} Native AOSP development, C/C++, Android Runtime Resource Overlays (RRO)
\\item \\textbf{Cross-Cultural:} Mandarin Chinese proficiency, Eastern-Western communication bridge
\\end{itemize}""",
            
            'fullstack_primary': """\\begin{itemize}[noitemsep]
\\item \\textbf{Programming Languages:} Java/J2EE, JavaScript, C\\#/.NET Core, Python, Bash, PowerShell
\\item \\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
\\item \\textbf{Backend Frameworks:} Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
\\item \\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture
\\item \\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
\\item \\textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest
\\item \\textbf{Cloud Platforms:} AWS, Azure, GCP
\\item \\textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)
\\item \\textbf{Version Control:} Git, GitHub, GitLab
\\item \\textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI
\\item \\textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews
\\item \\textbf{Performance Optimization:} Application scaling, Database optimization, Caching strategies
\\item \\textbf{Security:} Application security, Data protection, Authentication/Authorization
\\end{itemize}"""
        }
        
        self.experience_bricks = {
            'ecarx_infrastructure': """\\subsection*{ECARX (Geely Automotive) | IT/Infrastructure Specialist}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Managed multi-cloud infrastructure across AWS and Azure with 24/7 on-call support for 4 global offices
\\item Led Azure AKS to on-premise Kubernetes migration, reducing operational costs by 45\% and improving CI/CD efficiency by 25\%
\\item Implemented Infrastructure as Code using Terraform for AWS and Azure resource provisioning
\\item Deployed Prometheus/Grafana monitoring stack for proactive incident detection and capacity planning
\\item Built CI/CD pipelines with GitHub Actions and GitLab CI for automated deployments
\\item Worked extensively with Software Factory, DevOps practices, and container orchestration (AKS, AWS EKS)
\\end{itemize}""",
            
            'ecarx_android_focused': """\\subsection*{ECARX | IT/Infrastructure Specialist (Android Development Focus)}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading Android-based automotive technology solutions and system integration projects
\\item Developing and maintaining Android applications for automotive infotainment systems
\\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\\item Providing technical expertise in Android development to cross-functional teams
\\item Managing complex network systems with focus on mobile and automotive connectivity
\\end{itemize}""",
            
            'ecarx_fullstack': """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Led full-stack infrastructure optimization and cloud deployment projects for automotive technology
\\item Developed and maintained internal platforms using C\# .NET and React with cloud-native architecture
\\item Implemented cost-optimization strategies via Kubernetes cluster migration and CI/CD automation
\\item Managed AWS and Azure cloud resources with Infrastructure as Code (Terraform)
\\item Provided 24/7 production support for globally distributed automotive services with comprehensive monitoring
\\end{itemize}""",
            
            'synteda_devops_cloud': """\\subsection*{Synteda | .NET and Azure Integration Developer (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native applications on Azure with microservices architecture using .NET Core
\\item Implemented CI/CD pipelines using Azure DevOps and GitHub Actions for automated deployments
\\item Managed Azure Kubernetes Service (AKS) for container orchestration and scaling
\\item Built Infrastructure as Code with Terraform for Azure resource provisioning
\\item Integrated Azure Functions, App Services, and Azure Databricks for serverless computing
\\item Implemented monitoring and logging with Azure Monitor and Application Insights
\\end{itemize}""",
            
            'synteda_android_focused': """\\subsection*{Synteda | Mobile Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed comprehensive mobile applications using Android development with Kotlin and Java
\\item Built complete mobile platform from scratch, architecting both Android frontend and backend components
\\item Implemented RESTful APIs for mobile applications with focus on real-time data processing
\\item Integrated SQLite and cloud databases with optimized query performance for mobile applications
\\end{itemize}""",
            
            'synteda_fullstack': """\\subsection*{Synteda | C\# .NET Fullstack Developer \\& Integration Specialist}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed scalable talent management microservices using C\# .NET Core and Azure cloud-native architecture
\\item Built and optimized RESTful APIs and integrated SQL/NoSQL databases with high performance and security
\\item Managed automated CI/CD pipelines via Azure DevOps, ensuring reliable high-frequency releases
\\item Implemented Docker containerization and Azure Kubernetes Service (AKS) for scalable deployments
\\end{itemize}""",
            
            'iths_lia2_devops_cloud': """\\subsection*{IT-Högskolan | .NET Cloud Developer (LIA 2 - Intensive Training)}
\\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Intensive cloud development training with Azure platform (40+ hours/week, 5 months)
\\item Built and deployed applications on Azure App Services, Azure Functions, and Azure Kubernetes Service
\\item Implemented CI/CD pipelines with Azure DevOps for automated testing and deployment
\\item Worked with Infrastructure as Code using Terraform and ARM templates for Azure resources
\\item Gained hands-on experience with Azure monitoring, security, and cloud-native architecture patterns
\\item Migrated applications from on-premises to Azure cloud with zero-downtime deployment strategies
\\end{itemize}""",
            
            'senior_material_devops_cloud': """\\subsection*{Senior Material (Europe) AB | Platform Architect \\& Project Coordinator}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Architected full-stack web platform with cloud deployment on Azure for manufacturing sector
\\item Implemented CI/CD pipelines for automated testing and deployment using Azure DevOps
\\item Managed Azure cloud resources and optimized infrastructure costs through resource right-sizing
\\item Built microservices architecture with Docker containers and Azure Kubernetes Service
\\item Integrated Azure DevOps for project management, version control, and deployment automation
\\item Implemented monitoring and logging solutions using Azure Monitor for production systems
\\end{itemize}""",
            
            'addcell_devops_cloud': """\\subsection*{AddCell | Cloud Developer (LIA 1 - Intensive Training)}
\\textit{September 2022 - November 2022 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native applications deployed on both Azure and AWS (intensive 40+ hrs/week, 3 months)
\\item Built .NET Blazor application with backend APIs deployed on Azure App Services
\\item Implemented AWS Lambda functions and EC2 instances for multi-cloud deployment strategy
\\item Worked with Docker and Kubernetes for container orchestration across cloud platforms
\\item Set up CI/CD pipelines using Azure DevOps and GitLab for automated deployments
\\item Gained hands-on experience with multi-cloud architecture, Infrastructure as Code, and DevOps practices
\\end{itemize}""",
            
            'pembio_devops_cloud': """\\subsection*{Pembio AB | Full Stack Engineer (Internship)}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed full-stack SaaS application with cloud deployment on AWS/Azure
\\item Built backend microservices with Spring Boot and deployed on cloud platforms using Docker
\\item Implemented CI/CD pipelines for automated testing and deployment using GitHub Actions
\\item Worked with Docker containers and Kubernetes orchestration for scalable cloud infrastructure
\\item Set up monitoring and logging for production applications using CloudWatch and Azure Monitor
\\item Participated in Agile/Scrum development with DevOps practices and continuous delivery
\\end{itemize}""",
            
            'collabmaker_devops_cloud': """\\subsection*{CollabMaker | Frontend Developer (Internship)}
\\textit{July 2020 - October 2020 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed React.js frontend with backend API integration and cloud deployment
\\item Worked with CI/CD pipelines for automated deployments using GitHub Actions
\\item Participated in Agile/Scrum development processes with DevOps practices
\\item Gained experience with Git version control, collaborative development, and cloud collaboration tools
\\item Worked remotely during COVID-19, using cloud-based development and deployment workflows
\\end{itemize}""",
            
            # Backend Developer focused experience bricks
            'ecarx_backend': """\\subsection*{ECARX (Geely Automotive) | IT/Infrastructure Specialist}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed and maintained backend services for automotive technology platforms using .NET Core
\\item Built RESTful APIs and microservices architecture for distributed systems
\\item Optimized database performance (SQL Server, PostgreSQL) and implemented caching strategies with Redis
\\item Managed cloud infrastructure on AWS and Azure with Infrastructure as Code (Terraform)
\\item Implemented comprehensive monitoring and logging for backend services using Prometheus and Grafana
\\end{itemize}""",
            
            'synteda_backend': """\\subsection*{Synteda | .NET Backend Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed scalable backend microservices using C\# .NET Core and ASP.NET Core
\\item Built and optimized RESTful APIs with focus on performance, security, and scalability
\\item Integrated SQL Server and Azure Cosmos DB with Entity Framework Core
\\item Implemented message queues and event-driven architecture for asynchronous processing
\\item Managed database migrations, stored procedures, and query optimization
\\end{itemize}""",
            
            'pembio_backend': """\\subsection*{Pembio AB | Backend Engineer (Internship)}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed backend microservices using Java and Spring Boot framework
\\item Built RESTful APIs for SaaS platform with focus on scalability and performance
\\item Implemented database integration with PostgreSQL and MongoDB
\\item Worked with message queues (RabbitMQ) for asynchronous task processing
\\item Participated in code reviews, unit testing, and continuous integration practices
\\end{itemize}""",
            
            # Frontend Developer focused experience bricks
            'ecarx_frontend': """\\subsection*{ECARX (Geely Automotive) | IT/Infrastructure Specialist}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed and maintained internal web applications using React and TypeScript
\\item Built responsive user interfaces with modern JavaScript frameworks and state management
\\item Integrated frontend applications with backend APIs and cloud services
\\item Implemented CI/CD pipelines for automated frontend deployments
\\item Optimized web application performance and implemented comprehensive testing strategies
\\end{itemize}""",
            
            'synteda_frontend': """\\subsection*{Synteda | Frontend Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed modern web applications using React, TypeScript, and Angular
\\item Built responsive, accessible user interfaces with focus on user experience
\\item Integrated frontend applications with RESTful APIs and Azure cloud services
\\item Implemented state management solutions (Redux, Context API) for complex applications
\\item Worked with modern build tools (Webpack, Vite) and testing frameworks (Jest, React Testing Library)
\\end{itemize}""",
            
            'collabmaker_frontend': """\\subsection*{CollabMaker | Frontend Developer (Internship)}
\\textit{July 2020 - October 2020 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed React.js frontend for career guidance and matchmaking platform
\\item Built reusable UI components with modern JavaScript (ES6+) and React hooks
\\item Integrated frontend with backend APIs using Axios and RESTful services
\\item Participated in UI/UX design discussions and implemented responsive designs
\\item Worked in Agile/Scrum environment with daily standups and sprint planning
\\end{itemize}""",
            
            # IT Business Analyst focused experience bricks
            'ecarx_business_analyst': """\\subsection*{ECARX (Geely Automotive) | IT/Infrastructure Specialist}
\\textit{October 2024 - November 2025 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Analyzed business requirements and translated them into technical specifications for automotive IT systems
\\item Conducted stakeholder workshops across 4 global offices to gather requirements and align on solutions
\\item Led cost-benefit analysis for cloud migration project, achieving 45\% cost reduction
\\item Created technical documentation, process flows, and system architecture diagrams
\\item Coordinated between business stakeholders and technical teams to ensure successful project delivery
\\end{itemize}""",
            
            'synteda_business_analyst': """\\subsection*{Synteda | IT Business Analyst \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Gathered and documented business requirements for talent management platform
\\item Conducted gap analysis between current state and desired business outcomes
\\item Created functional specifications and user stories for development teams
\\item Facilitated workshops with stakeholders to define business processes and system requirements
\\item Analyzed data flows and integration points between systems
\\end{itemize}""",
            
            'senior_material_business_analyst': """\\subsection*{Senior Material (Europe) AB | Business Analyst \\& Project Coordinator}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Led business analysis for digital transformation of manufacturing platforms
\\item Conducted stakeholder interviews and requirements gathering sessions
\\item Created business cases with ROI analysis for technology investments
\\item Documented business processes and created process flow diagrams
\\item Coordinated between business units and IT teams to ensure alignment on project goals
\\end{itemize}""",
            
            'hongyan_business_analyst': """\\subsection*{Hong Yan AB | Entrepreneur \\& Business Analyst}
\\textit{April 2017 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Analyzed market trends and customer data to drive business decisions
\\item Implemented technology solutions (Wix, Zettle, Stripe) to optimize business operations
\\item Conducted financial analysis and forecasting, achieving 25\% annual revenue growth
\\item Integrated online ordering, table reservation, and delivery services through technology platforms
\\item Analyzed partnership opportunities with Uber Eats and Foodora, optimizing delivery operations
\\end{itemize}"""
        }
        }
        
        self.projects_bricks = {
            'volvo_focused_projects': """\\section*{Strategic Projects}
\\subsection{Fleet Management Dashboard}
\\textit{2024 -- Present} \\\\
\\textbf{.NET 8, React 18, SQL Server 2022, Azure, Docker, GitHub Actions}
\\begin{itemize}
\\item Built an intelligent fleet tracking platform using US DOT data to optimize fuel efficiency and CO2 tracking for sustainable transport operations.
\\item Implemented predictive maintenance analytics and route optimization features, aligning with Volvo's mission for eco-friendly and cost-effective logistics.
\\item Leveraged Azure App Service and Docker for scalable hosting, with fully automated CI/CD pipelines via GitHub Actions.
\\end{itemize}

\\subsection{AI Math Grader Ecosystem}
\\textit{2025 -- Present} \\\\
\\textbf{C\# .NET 8, React, AI/LLM (Gemini/OpenAI), Python, PDF Export}
\\begin{itemize}
\\item Developed a full-stack automated grading system for K-12 math, providing instant, pedagogical feedback using advanced LLM integration.
\\item Architected a modular API layer for AI-driven feedback loops, ensuring low-latency processing and high accuracy in mathematical evaluation.
\\item Integrated white-label PDF export functionality for accessible, cost-effective result sharing.
\\end{itemize}""",
            
            'android_automotive_projects': """\\section*{Android \\& Automotive Projects}
\\subsection{AndroidAuto\\_AI\\_Bot}
\\textit{June 2025 -- Present} \\\\
\\textbf{AndroidAuto, EdgeTTS, TwitterAPI, LLM, Python, Kotlin}
\\begin{itemize}
\\item Designed an in-car AI voice assistant for Android Auto, activated via a custom wake-word \\texttt{"Hi Car"}, as a smarter alternative to Google Assistant
\\item Integrated Large Language Models (LLMs) for natural language understanding and real-time conversational responses
\\item Enabled real-time querying of public Twitter/X content via Twitter API, with responses converted to speech using Edge TTS
\\item Built a text-to-speech (TTS) pipeline to vocalize responses from the LLM and external APIs for hands-free, eyes-free user experience
\\item Designed for Android Auto with a distraction-free, voice-only interface and on-device wake-word detection
\\item Supports conversational queries, personalized information access, and live updates while commuting
\\end{itemize}

\\subsection{AndroidAuto\\_TTS\\_EpubReader}
\\textit{June 2025 -- Present} \\\\
\\textbf{Python, EdgeTTS, EPUB, AndroidAuto, TelegramBotIntegration, CloudFlare}
\\begin{itemize}
\\item Built an EPUB-to-MP3 audiobook generator using Microsoft Edge TTS for Android Auto playback
\\item Designed offline media synchronization for customized reading-on-the-road experience
\\item Created distraction-free in-car UI for audio playback of personalized content while commuting
\\end{itemize}

\\subsection{AndroidAuto\\_CarTVPlayer}
\\textit{March 2025 -- Present} \\\\
\\textbf{Kotlin, AndroidAuto, RESTfulAPIs, EXOPlayer, VLCPlayer}
\\begin{itemize}
\\item Designed and built a customized Android Auto media player with enhanced audio controls and intuitive UI
\\item Integrated voice command processing and secure data access via SQL backend
\\item Developed and tested robust frontend and backend modules for smooth in-vehicle experience
\\end{itemize}

\\subsection{Gothenburg\\_TaxiPooling}
\\textit{May 2025 -- Present} \\\\
\\textbf{SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL}
\\begin{itemize}
\\item Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking
\\item Developed cross-platform mobile application using React Native and Spring Boot microservices
\\item Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling
\\item Engineered for performance optimization and GDPR-compliant data privacy
\\end{itemize}""",
            
            'fullstack_projects': """\\section*{Hobby Projects}
\\subsection{JobHunter\\_Python\\_TypeScript\\_RESTAPI}
\\textit{July 2025 -- Present} \\\\
\\textbf{Python, TypeScript, GmailRESTAPI, LinkedinAPI}
\\begin{itemize}
\\item Automated job hunting pipeline integrating Gmail search, job scraping, and resume customization
\\item Generated resumes and cover letters based on job descriptions using NLP techniques
\\item Auto-sent job application drafts to user with a fully functional end-to-end workflow
\\item Demo: https://jobs.bluehawana.com
\\end{itemize}

\\subsection{Bluehawana.com\\_Web.HTML}
\\textit{Jan 2025 -- Present} \\\\
\\textbf{HTML5, CSS3, JavaScript, GitHubAPI, LinkedIn API}
\\begin{itemize}
\\item Redesigned and upgraded personal portfolio website from static GitHub Pages to dynamic, professional-grade tech site
\\item Integrated GitHub API for real-time repository feed and LinkedIn API for automated blog synchronization
\\item Implemented responsive UI/UX with mobile-first design principles and performance-optimized layout
\\item Deployed on Netlify with custom domain and automated CI/CD via Git
\\end{itemize}

\\subsection{SmrtMart.com\\_COMMERCE.WEB}
\\textit{April 2024 -- Present} \\\\
\\textbf{Go, Next, PostgreSQL, Microservices, StripeAPI}
\\begin{itemize}
\\item Fullstack e-commerce platform with microservices-based architecture for seamless scalability
\\item Implemented comprehensive order management, inventory tracking, and payment systems
\\item Optimized backend API performance and integrated PostgreSQL and MongoDB for hybrid data storage
\\end{itemize}"""
        }
    
    def build_cv_for_job(self, job_details: dict, application_type: str = 'android_focused') -> dict:
        """Build CV using LEGO bricks based on job requirements"""
        
        # Analyze job requirements
        job_analysis = self._analyze_job_requirements(job_details)
        
        # Select appropriate bricks
        cv_components = {
            'profile': self._select_profile_brick(job_analysis, application_type),
            'skills': self._select_skills_brick(job_analysis, application_type),
            'experience': self._select_experience_bricks(job_analysis, application_type),
            'projects': self._select_projects_brick(job_analysis, application_type)
        }
        
        return cv_components
    
    def _analyze_job_requirements(self, job_details: dict) -> dict:
        """Analyze job requirements to determine focus areas"""
        
        title = job_details.get('title', '').lower()
        description = job_details.get('description', '').lower()
        requirements = ' '.join(job_details.get('requirements', [])).lower()
        
        full_text = f"{title} {description} {requirements}"
        
        analysis = {
            'is_android': any(keyword in full_text for keyword in [
                'android', 'kotlin', 'java', 'mobile', 'aosp', 'infotainment'
            ]),
            'is_automotive': any(keyword in full_text for keyword in [
                'automotive', 'car', 'vehicle', 'infotainment', 'volvo', 'ecarx'
            ]),
            'is_fullstack': any(keyword in full_text for keyword in [
                'fullstack', 'full-stack', 'full stack', 'react', '.net', 'c\#'
            ]),
            'requires_infrastructure': any(keyword in full_text for keyword in [
                'infrastructure', 'devops', 'azure', 'docker', 'kubernetes', 'terraform'
            ]),
            'requires_mobile': any(keyword in full_text for keyword in [
                'mobile', 'app', 'android', 'ios'
            ]),
            'company': job_details.get('company', ''),
            'seniority': 'senior' if any(k in full_text for k in ['senior', 'architect', 'lead']) else 'mid'
        }
        
        return analysis
    
    def _select_profile_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate profile summary brick"""
        
        if application_type == 'android_focused' or analysis['is_android']:
            return self.profile_bricks['android_developer']
        elif analysis['requires_infrastructure']:
            return """Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, Azure, Docker, and infrastructure automation. Specialized in building resilient, scalable infrastructure for mission-critical automotive systems."""
        else:
            return self.profile_bricks['fullstack_developer']
    
    def _select_skills_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate skills brick"""
        
        if application_type == 'android_focused' or analysis['is_android']:
            return self.skills_bricks['android_primary']
        elif analysis['requires_infrastructure']:
            return """\\begin{itemize}[noitemsep]
\\item \\textbf{Infrastructure \& Cloud:} Azure (AKS, App Services, Functions), AWS, GCP, Terraform (IaC)
\\item \\textbf{DevOps \& CI/CD:} GitHub Actions, Azure DevOps, Jenkins, Docker, Kubernetes, Helm
\\item \\textbf{Programming:} C\# .NET 8, Python, Bash, PowerShell, Go, JavaScript, TypeScript
\\item \\textbf{Observability:} Grafana, Prometheus, ELK Stack, Performance Tuning, SLO-driven Alerting
\\item \\textbf{Backend \& APIs:} ASP.NET Core, RESTful/GraphQL APIs, Microservices, Kafka, Kafka Streams
\\item \\textbf{Databases:} SQL Server, PostgreSQL, MongoDB, Redis, Entity Framework Core
\\item \\textbf{Methodologies:} Agile/Scrum, DevSecOps, Site Reliability Engineering (SRE), Incident Management
\\end{itemize}"""
        else:
            return self.skills_bricks['fullstack_primary']
    
    def _select_experience_bricks(self, analysis: dict, application_type: str) -> str:
        """Select and combine appropriate experience bricks based on job requirements"""
        
        experience_sections = []
        
        # Determine the focus area
        is_devops_cloud = analysis['requires_infrastructure'] or 'devops' in application_type.lower() or 'cloud' in application_type.lower()
        is_backend = 'backend' in application_type.lower() or analysis.get('is_backend', False)
        is_frontend = 'frontend' in application_type.lower() or analysis.get('is_frontend', False)
        is_business_analyst = 'business' in application_type.lower() or 'analyst' in application_type.lower()
        is_android = analysis['is_android'] or 'android' in application_type.lower()
        
        # ECARX experience (Oct 2024 - Nov 2025)
        if is_business_analyst:
            experience_sections.append(self.experience_bricks['ecarx_business_analyst'])
        elif is_backend:
            experience_sections.append(self.experience_bricks['ecarx_backend'])
        elif is_frontend:
            experience_sections.append(self.experience_bricks['ecarx_frontend'])
        elif is_devops_cloud:
            experience_sections.append(self.experience_bricks['ecarx_infrastructure'])
        elif is_android:
            experience_sections.append(self.experience_bricks['ecarx_android_focused'])
        else:
            experience_sections.append(self.experience_bricks['ecarx_fullstack'])
            
        # Synteda experience (Aug 2023 - Sep 2024)
        if is_business_analyst:
            experience_sections.append(self.experience_bricks['synteda_business_analyst'])
        elif is_backend:
            experience_sections.append(self.experience_bricks['synteda_backend'])
        elif is_frontend:
            experience_sections.append(self.experience_bricks['synteda_frontend'])
        elif is_devops_cloud:
            experience_sections.append(self.experience_bricks['synteda_devops_cloud'])
        elif is_android:
            experience_sections.append(self.experience_bricks['synteda_android_focused'])
        else:
            experience_sections.append(self.experience_bricks['synteda_fullstack'])
        
        # IT-Högskolan LIA 2 (Jan 2023 - May 2023) - Intensive Azure/DevOps training
        if is_devops_cloud or is_backend or is_frontend:
            experience_sections.append(self.experience_bricks['iths_lia2_devops_cloud'])
        
        # Senior Material (Jan 2022 - Dec 2022)
        if is_business_analyst:
            experience_sections.append(self.experience_bricks['senior_material_business_analyst'])
        elif is_devops_cloud:
            experience_sections.append(self.experience_bricks['senior_material_devops_cloud'])
        else:
            # Original version for non-DevOps roles
            experience_sections.append("""\\subsection*{Senior Material (Europe) AB | Fullstack Platform Architect}
\\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\\begin{itemize}[noitemsep]
\\item Led the digital transformation of manufacturing platforms in the lithium-ion battery sector, migrating monoliths to containerized microservices
\\item Architected scalable backend solutions with Spring Boot and integrated modern React frontends for real-time manufacturing data visualization
\\item Collaborated in high-stakes agile environments to optimize system performance and data integrity during critical technical transitions
\\end{itemize}""")
        
        # AddCell LIA 1 (Sep 2022 - Nov 2022) - Intensive multi-cloud training
        if is_devops_cloud or is_backend or is_frontend:
            experience_sections.append(self.experience_bricks['addcell_devops_cloud'])
        
        # Pembio (Oct 2020 - Sep 2021)
        if is_backend:
            experience_sections.append(self.experience_bricks['pembio_backend'])
        elif is_devops_cloud:
            experience_sections.append(self.experience_bricks['pembio_devops_cloud'])
        else:
            # Original version for non-DevOps roles
            experience_sections.append("""\\subsection*{Pembio AB | Fullstack Developer}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\\item Built frontend features using Vue.js framework and integrated with backend APIs
\\item Developed RESTful APIs and implemented comprehensive database integration
\\item Participated in Agile development processes and collaborated with cross-functional teams
\\end{itemize}""")
        
        # CollabMaker (Jul 2020 - Oct 2020)
        if is_frontend:
            experience_sections.append(self.experience_bricks['collabmaker_frontend'])
        elif is_devops_cloud:
            experience_sections.append(self.experience_bricks['collabmaker_devops_cloud'])
        
        # Hong Yan AB (Apr 2017 - Present) - Only for Business Analyst roles
        if is_business_analyst:
            experience_sections.append(self.experience_bricks['hongyan_business_analyst'])
        
        return '\n\n'.join(experience_sections)
    
    def _select_projects_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate projects brick"""

        if analysis['is_automotive'] or analysis['is_fullstack'] or analysis['requires_infrastructure']:
            # For Volvo/automotive roles, include BOTH Strategic Projects AND Hobby Projects
            return self.projects_bricks['volvo_focused_projects'] + '\n\n' + self.projects_bricks['fullstack_projects']
        elif analysis['is_android']:
            # For Android roles, include Android projects AND Hobby Projects
            return self.projects_bricks['android_automotive_projects'] + '\n\n' + self.projects_bricks['fullstack_projects']
        else:
            return self.projects_bricks['fullstack_projects']