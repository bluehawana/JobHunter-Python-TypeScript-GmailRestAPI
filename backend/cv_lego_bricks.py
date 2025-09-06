#!/usr/bin/env python3
"""
CV LEGO Bricks System
Dynamically builds CV sections based on job requirements
"""

class CVLegoBricks:
    """LEGO bricks approach to CV building - modular, reusable components"""
    
    def __init__(self):
        self.profile_bricks = {
            'android_developer': """Experienced Android Developer with over 5 years of hands-on experience in native Android development using Kotlin and Java. Proven expertise in building scalable mobile applications with Android Studio, deep understanding of Android SDK and platform architecture. Strong background in system-level Android components including Activities, Services, Content Providers, and Broadcast Receivers. Demonstrated ability to work with automotive infotainment systems and in-car applications. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep Android development knowledge to automotive technology solutions.""",
            
            'fullstack_developer': """Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development.""",
            
            'mobile_developer': """Experienced Mobile Developer with expertise in cross-platform and native mobile development. Strong background in Android development using Kotlin and Java, with additional experience in React Native for cross-platform solutions. Proven ability to build scalable mobile applications with focus on user experience and performance optimization."""
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
            'ecarx_android_focused': """\\subsection*{ECARX | IT/Infrastructure Specialist (Android Development Focus)}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading Android-based automotive technology solutions and system integration projects
\\item Developing and maintaining Android applications for automotive infotainment systems
\\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\\item Providing technical expertise in Android development to cross-functional teams
\\item Managing complex network systems with focus on mobile and automotive connectivity
\\end{itemize}""",
            
            'ecarx_fullstack': """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\\item Providing IT support and infrastructure support to development teams for enhanced productivity
\\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\\item Managing complex network systems and providing technical solution design for enterprise-level applications
\\end{itemize}""",
            
            'synteda_android_focused': """\\subsection*{Synteda | Mobile Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed comprehensive mobile applications using Android development with Kotlin and Java
\\item Built complete mobile platform from scratch, architecting both Android frontend and backend components
\\item Implemented RESTful APIs for mobile applications with focus on real-time data processing
\\item Integrated SQLite and cloud databases with optimized query performance for mobile applications
\\end{itemize}""",
            
            'synteda_fullstack': """\\subsection*{Synteda | Azure Fullstack Developer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed comprehensive talent management system using C\\# and .NET Core with cloud-native architecture
\\item Built complete office management platform from scratch, architecting both frontend and backend components
\\item Implemented RESTful APIs and microservices for scalable application architecture
\\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\\end{itemize}"""
        }
        
        self.projects_bricks = {
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
\\end{itemize}

\\subsection{Bluehawana.com\\_Web.HTML}
\\textit{Jan 2025 -- Present} \\\\
\\textbf{HTML5, CSS3, JavaScript, GitHubAPI, LinkedIn API}
\\begin{itemize}
\\item Redesigned and upgraded personal portfolio website from static GitHub Pages to dynamic, professional-grade tech site
\\item Integrated GitHub API for real-time repository feed and LinkedIn API for automated blog synchronization
\\item Implemented responsive UI/UX with mobile-first design principles and performance-optimized layout
\\item Deployed on Netlify with custom domain and automated CI/CD via Git
\\item Added professional services module with booking system and contact form integration
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
                'automotive', 'car', 'vehicle', 'infotainment', 'ecarx'
            ]),
            'is_fullstack': any(keyword in full_text for keyword in [
                'fullstack', 'full stack', 'web', 'react', 'angular', 'spring'
            ]),
            'requires_mobile': any(keyword in full_text for keyword in [
                'mobile', 'app', 'android', 'ios'
            ]),
            'company': job_details.get('company', ''),
            'seniority': 'senior' if 'senior' in full_text else 'mid'
        }
        
        return analysis
    
    def _select_profile_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate profile summary brick"""
        
        if application_type == 'android_focused' or analysis['is_android']:
            return self.profile_bricks['android_developer']
        elif analysis['requires_mobile']:
            return self.profile_bricks['mobile_developer']
        else:
            return self.profile_bricks['fullstack_developer']
    
    def _select_skills_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate skills brick"""
        
        if application_type == 'android_focused' or analysis['is_android']:
            return self.skills_bricks['android_primary']
        else:
            return self.skills_bricks['fullstack_primary']
    
    def _select_experience_bricks(self, analysis: dict, application_type: str) -> str:
        """Select and combine appropriate experience bricks"""
        
        experience_sections = []
        
        # ECARX experience - tailor based on job type
        if application_type == 'android_focused' or analysis['is_android'] or analysis['is_automotive']:
            experience_sections.append(self.experience_bricks['ecarx_android_focused'])
            experience_sections.append(self.experience_bricks['synteda_android_focused'])
        else:
            experience_sections.append(self.experience_bricks['ecarx_fullstack'])
            experience_sections.append(self.experience_bricks['synteda_fullstack'])
        
        # Add remaining standard experience
        remaining_experience = """\\subsection*{IT-Högskolan | Backend Developer (Part-time)}
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

\\subsection*{Pembio AB | Fullstack Developer}
\\textit{October 2020 - September 2021 | Lund, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\\item Built frontend features using Vue.js framework and integrated with backend APIs
\\item Developed RESTful APIs and implemented comprehensive database integration
\\item Participated in Agile development processes and collaborated with cross-functional teams
\\item Implemented automated testing strategies and ensured application security
\\end{itemize}"""
        
        experience_sections.append(remaining_experience)
        
        return '\n\n'.join(experience_sections)
    
    def _select_projects_brick(self, analysis: dict, application_type: str) -> str:
        """Select appropriate projects brick"""
        
        if application_type == 'android_focused' or analysis['is_android'] or analysis['is_automotive']:
            return self.projects_bricks['android_automotive_projects']
        else:
            return self.projects_bricks['fullstack_projects']