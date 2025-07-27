#!/usr/bin/env python3
"""
Complete JobHunter workflow:
1. Fetch all jobs from Supabase database
2. For each job: create tailored CV and cover letter
3. Generate PDFs with proper naming (hongzhi_[role]_[company].pdf)
4. Send individual emails for each job application
5. Update database with application status
"""
import asyncio
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class JobApplicationProcessor:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "bluehawanan@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = "leeharvad@gmail.com"
        
    def normalize_job_title(self, title: str) -> str:
        """Normalize job title for file naming"""
        # Remove special characters and normalize
        normalized = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        normalized = re.sub(r'\s+', '_', normalized.strip())
        return normalized.lower()
    
    def extract_key_skills_from_description(self, description: str, title: str) -> List[str]:
        """Extract key skills and technologies from job description"""
        description_lower = description.lower()
        title_lower = title.lower()
        
        # Define skill categories
        programming_langs = ['java', 'python', 'javascript', 'typescript', 'c#', '.net', 'node.js', 'spring boot', 'react', 'angular', 'vue.js']
        cloud_skills = ['aws', 'azure', 'gcp', 'kubernetes', 'docker', 'jenkins', 'ci/cd', 'devops', 'terraform']
        databases = ['postgresql', 'mysql', 'mongodb', 'redis', 'sql', 'nosql']
        methodologies = ['agile', 'scrum', 'microservices', 'restful api', 'graphql']
        
        found_skills = []
        
        # Check for skills in description
        for skill_list in [programming_langs, cloud_skills, databases, methodologies]:
            for skill in skill_list:
                if skill in description_lower or skill in title_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def determine_role_focus(self, title: str, skills: List[str]) -> str:
        """Determine the primary role focus for tailoring"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['devops', 'infrastructure', 'sre', 'platform']):
            return 'devops'
        elif any(word in title_lower for word in ['backend', 'api', 'microservices']):
            return 'backend'
        elif any(word in title_lower for word in ['frontend', 'react', 'angular', 'ui']):
            return 'frontend'
        elif any(word in title_lower for word in ['fullstack', 'full-stack', 'full stack']):
            return 'fullstack'
        elif any(word in title_lower for word in ['data', 'analytics', 'ml', 'machine learning']):
            return 'data'
        else:
            return 'fullstack'  # Default
    
    def create_tailored_cv_simple(self, job: Dict, role_focus: str, skills: List[str]) -> str:
        """Create job-specific CV with tailored content"""
        
        # Determine profile summary based on role
        profile_summaries = {
            'devops': "Experienced DevOps Engineer and Fullstack Developer with over 5 years of hands-on experience in infrastructure automation, cloud platforms, and CI/CD pipelines. Proven expertise in Kubernetes, Docker, AWS/Azure, and building scalable microservices architectures. Strong background in Java/Spring Boot backend development with modern frontend integration. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex infrastructure solutions and automated deployment environments.",
            
            'backend': "Experienced Backend Developer with over 5 years of hands-on experience in Java/J2EE development and modern server-side technologies. Proven expertise in building scalable backend services using Spring Boot, microservices architecture, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, system optimization, and cloud deployment. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex backend solutions and high-performance applications.",
            
            'frontend': "Experienced Frontend Developer with strong fullstack capabilities and over 5 years of hands-on experience in modern web technologies. Proven expertise in Angular, React, Vue.js, and responsive web application development with seamless backend integration. Strong background in JavaScript/TypeScript, HTML5/CSS3, and building user-centric interfaces with optimal performance. Currently serving as IT/Infrastructure Specialist at ECARX, bringing technical excellence to user experience and frontend architecture solutions.",
            
            'fullstack': "Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments.",
            
            'data': "Experienced Software Developer with strong data engineering capabilities and over 5 years of hands-on experience in backend systems and data processing. Proven expertise in building scalable data pipelines, database optimization, and analytics platforms using Java/Spring Boot with modern cloud technologies. Strong background in SQL/NoSQL databases, API development, and cloud-based data solutions. Currently serving as IT/Infrastructure Specialist at ECARX, bringing technical expertise to data-driven solutions and analytics platforms."
        }
        
        # Skills highlighting based on role and job requirements
        highlighted_skills = self.get_highlighted_skills(role_focus, skills)
        
        cv_template = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=0.8in]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

% Define dark blue color (LinkedIn blue)
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

% Hyperlink setup
\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue,
    pdfauthor={{Hongzhi Li}},
    pdftitle={{Hongzhi Li - {job.get('title', 'Developer')} CV}}
}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{8pt}}

\\newcommand{{\\sectiontitle}}[1]{{
    \\vspace{{10pt}}
    {{\\large\\textbf{{\\textcolor{{darkblue}}{{#1}}}}}}
    \\vspace{{5pt}}
    \\textcolor{{darkblue}}{{\\hrule}}
    \\vspace{{8pt}}
}}

\\newcommand{{\\jobtitle}}[4]{{
    \\textbf{{#1}} --- #2\\\\
    \\textit{{#3 --- #4}}\\\\
}}

\\begin{{document}}

% Header
\\begin{{center}}
{{\\huge \\textbf{{\\textcolor{{darkblue}}{{Hongzhi Li}}}}}}\\\\
\\vspace{{8pt}}
{{\\Large \\textcolor{{darkblue}}{{{job.get('title', 'Fullstack Developer')}}}}}\\\\
\\vspace{{12pt}}
\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} $\\bullet$ 0728384299 $\\bullet$ 
\\href{{https://linkedin.com/in/hongzhi-li}}{{LinkedIn}} $\\bullet$ 
\\href{{https://github.com/bluehawana}}{{GitHub}}
\\end{{center}}

\\vspace{{15pt}}

\\sectiontitle{{Profile Summary}}
{profile_summaries.get(role_focus, profile_summaries['fullstack'])}

\\sectiontitle{{Core Technical Skills}}
{highlighted_skills}

\\sectiontitle{{Professional Experience}}

\\jobtitle{{ECARX}}{{IT/Infrastructure Specialist}}{{October 2024 - Present}}{{Gothenburg, Sweden}}
{self.get_tailored_ecarx_experience(role_focus)}

\\jobtitle{{Synteda}}{{Azure Fullstack Developer \\& Integration Specialist (Freelance)}}{{August 2023 - September 2024}}{{Gothenburg, Sweden}}
{self.get_tailored_synteda_experience(role_focus)}

\\jobtitle{{IT-H\\"ogskolan}}{{Backend Developer (Part-time)}}{{January 2023 - May 2023}}{{Gothenburg, Sweden}}
{self.get_tailored_ithogskolan_experience(role_focus)}

\\jobtitle{{Senior Material (Europe) AB}}{{Platform Architect \\& Project Coordinator}}{{January 2022 - December 2022}}{{Eskilstuna, Sweden}}
{self.get_tailored_senior_material_experience(role_focus)}

\\jobtitle{{AddCell (CTH Startup)}}{{DevOps Engineer}}{{September 2022 - November 2022}}{{Gothenburg, Sweden}}
{self.get_tailored_addcell_experience(role_focus)}

\\jobtitle{{Pembio AB}}{{Fullstack Developer}}{{October 2020 - September 2021}}{{Lund, Sweden}}
{self.get_tailored_pembio_experience(role_focus)}

\\sectiontitle{{Hobby Projects}}

{self.get_tailored_projects(role_focus)}

\\sectiontitle{{Education}}
\\textbf{{IT H\\"ogskolan}}\\\\
Bachelor's Degree in .NET Cloud Development --- 2021-2023, M\\"olndal Campus\\\\
Bachelor's Degree in Java Integration --- 2019-2021

\\textbf{{University of Gothenburg}}\\\\
Master's Degree in International Business and Trade --- 2016-2019

\\sectiontitle{{Certifications}}
$\\bullet$ AWS Certified Solutions Architect - Associate (Aug 2022)\\\\
$\\bullet$ Microsoft Certified: Azure Fundamentals (Jun 2022)\\\\
$\\bullet$ AWS Certified Developer - Associate (Nov 2022)

\\sectiontitle{{Additional Information}}
\\textbf{{Languages:}} Fluent in English and Mandarin\\\\
\\textbf{{Interests:}} Vehicle technology, energy sector, electrical charging systems\\\\
\\textbf{{Website:}} \\href{{https://bluehawana.com}}{{bluehawana.com}}

\\end{{document}}"""
        
        return cv_template
    
    def get_highlighted_skills(self, role_focus: str, job_skills: List[str]) -> str:
        """Get skills section tailored to role focus"""
        
        base_skills = {
            'devops': [
                "\\textbf{Cloud Platforms:} AWS, Azure, GCP, Kubernetes, Docker, AKS",
                "\\textbf{DevOps Tools:} Jenkins, GitHub Actions, GitLab CI, Terraform, Ansible",
                "\\textbf{Programming Languages:} Java/J2EE, Python, Bash, PowerShell, JavaScript",
                "\\textbf{Backend Frameworks:} Spring Boot, .NET Core, Node.js, Microservices",
                "\\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis, SQL/NoSQL",
                "\\textbf{Monitoring:} Grafana, Prometheus, ELK Stack, Application Monitoring",
                "\\textbf{Infrastructure:} Kubernetes, Docker, Network Systems, System Integration"
            ],
            'backend': [
                "\\textbf{Programming Languages:} Java/J2EE, C\\#/.NET Core, Python, JavaScript, SQL",
                "\\textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js",
                "\\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture",
                "\\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis, Database Optimization",
                "\\textbf{Cloud Platforms:} AWS, Azure, Cloud-native Development",
                "\\textbf{Testing:} Unit Testing, Integration Testing, JUnit, Automated Testing",
                "\\textbf{Performance:} Application Scaling, Caching Strategies, Query Optimization"
            ],
            'frontend': [
                "\\textbf{Frontend Frameworks:} Angular, ReactJS, Vue.js, React Native, HTML5, CSS3",
                "\\textbf{Programming Languages:} JavaScript, TypeScript, Java/J2EE, C\\#",
                "\\textbf{Backend Integration:} RESTful APIs, GraphQL, State Management",
                "\\textbf{Development Tools:} Git, GitHub, Webpack, NPM, Modern Build Tools",
                "\\textbf{UI/UX:} Responsive Design, Cross-browser Compatibility, Performance Optimization",
                "\\textbf{Testing:} Jest, Frontend Testing, Component Testing",
                "\\textbf{Cloud Platforms:} AWS, Azure, Frontend Deployment"
            ],
            'fullstack': [
                "\\textbf{Programming Languages:} Java/J2EE, JavaScript, TypeScript, C\\#/.NET Core, Python",
                "\\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                "\\textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js",
                "\\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture",
                "\\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB",
                "\\textbf{Cloud Platforms:} AWS, Azure, GCP, Containerization with Docker/Kubernetes",
                "\\textbf{DevOps:} CI/CD Pipelines, Jenkins, GitHub Actions, Infrastructure as Code"
            ]
        }
        
        skills_list = base_skills.get(role_focus, base_skills['fullstack'])
        return "\\n\\n".join(skills_list)
    
    def get_tailored_ecarx_experience(self, role_focus: str) -> str:
        """Get ECARX experience tailored to role focus"""
        experiences = {
            'devops': "$\\bullet$ Leading infrastructure optimization and system integration projects for automotive technology solutions\\\\\n$\\bullet$ Implementing cost optimization by migrating from AKS to local Kubernetes cluster, reducing operational expenses\\\\\n$\\bullet$ Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability\\\\\n$\\bullet$ Managing complex network systems and providing technical solution design for enterprise-level applications\\\\\n$\\bullet$ Providing infrastructure automation and DevOps support to development teams",
            
            'backend': "$\\bullet$ Leading backend system optimization and integration projects for automotive technology solutions\\\\\n$\\bullet$ Developing scalable microservices architecture and API design for enterprise applications\\\\\n$\\bullet$ Implementing database optimization and performance tuning for high-traffic systems\\\\\n$\\bullet$ Providing technical solution design and backend architecture guidance\\\\\n$\\bullet$ Managing complex data processing systems and backend service reliability",
            
            'frontend': "$\\bullet$ Leading user interface optimization and frontend integration projects\\\\\n$\\bullet$ Implementing modern frontend monitoring and performance optimization solutions\\\\\n$\\bullet$ Providing technical solution design for user-facing applications and interfaces\\\\\n$\\bullet$ Supporting frontend development teams with infrastructure and deployment automation\\\\\n$\\bullet$ Managing complex frontend build systems and deployment pipelines",
            
            'fullstack': "$\\bullet$ Leading infrastructure optimization and system integration projects for automotive technology solutions\\\\\n$\\bullet$ Providing IT support and infrastructure support to development teams for enhanced productivity\\\\\n$\\bullet$ Implementing cost optimization project by migrating from AKS to local Kubernetes cluster\\\\\n$\\bullet$ Implementing modern monitoring solutions using Grafana and advanced scripting\\\\\n$\\bullet$ Managing complex network systems and providing technical solution design"
        }
        
        return experiences.get(role_focus, experiences['fullstack'])
    
    def get_tailored_synteda_experience(self, role_focus: str) -> str:
        """Get Synteda experience tailored to role focus"""
        experiences = {
            'devops': "$\\bullet$ Developed cloud-native talent management system with Azure infrastructure and CI/CD automation\\\\\n$\\bullet$ Implemented containerized microservices architecture with Docker and Kubernetes deployment\\\\\n$\\bullet$ Built automated deployment pipelines and infrastructure as code solutions\\\\\n$\\bullet$ Optimized database performance and implemented monitoring for production systems",
            
            'backend': "$\\bullet$ Developed comprehensive talent management system using C\\# and .NET Core with microservices architecture\\\\\n$\\bullet$ Built scalable backend APIs and implemented complex business logic for office management platform\\\\\n$\\bullet$ Implemented RESTful APIs and microservices for high-performance application architecture\\\\\n$\\bullet$ Integrated SQL and NoSQL databases with optimized query performance and data protection",
            
            'frontend': "$\\bullet$ Built complete office management platform frontend with modern UI frameworks and responsive design\\\\\n$\\bullet$ Developed user-centric interfaces with seamless backend API integration\\\\\n$\\bullet$ Implemented modern frontend architecture with component-based design patterns\\\\\n$\\bullet$ Optimized frontend performance and user experience across multiple platforms",
            
            'fullstack': "$\\bullet$ Developed comprehensive talent management system using C\\# and .NET Core with cloud-native architecture\\\\\n$\\bullet$ Built complete office management platform from scratch, architecting both frontend and backend components\\\\\n$\\bullet$ Implemented RESTful APIs and microservices for scalable application architecture\\\\\n$\\bullet$ Integrated SQL and NoSQL databases with optimized query performance and data protection measures"
        }
        
        return experiences.get(role_focus, experiences['fullstack'])
    
    def get_tailored_ithogskolan_experience(self, role_focus: str) -> str:
        """Get IT-Högskolan experience tailored to role focus"""
        return "$\\bullet$ Migrated \\\"Omstallningsstod.se\\\" adult education platform using Spring Boot backend services\\\\\n$\\bullet$ Developed RESTful APIs for frontend integration and implemented secure data handling\\\\\n$\\bullet$ Collaborated with UI/UX designers to ensure seamless frontend-backend integration\\\\\n$\\bullet$ Implemented automated tests as part of delivery process"
    
    def get_tailored_senior_material_experience(self, role_focus: str) -> str:
        """Get Senior Material experience tailored to role focus"""
        return "$\\bullet$ Led migration of business-critical applications with microservices architecture\\\\\n$\\bullet$ Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption\\\\\n$\\bullet$ Collaborated with development teams to optimize applications for maximum speed and scalability\\\\\n$\\bullet$ Participated in Agile ceremonies including sprint planning, reviews, and retrospectives"
    
    def get_tailored_addcell_experience(self, role_focus: str) -> str:
        """Get AddCell experience tailored to role focus"""
        return "$\\bullet$ Developed cloud-native applications using serverless computing architecture\\\\\n$\\bullet$ Implemented GraphQL APIs for efficient data fetching and frontend integration\\\\\n$\\bullet$ Worked with SQL and NoSQL databases for optimal data storage and retrieval"
    
    def get_tailored_pembio_experience(self, role_focus: str) -> str:
        """Get Pembio experience tailored to role focus"""
        return "$\\bullet$ Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture\\\\\n$\\bullet$ Built frontend features using Vue.js framework and integrated with backend APIs\\\\\n$\\bullet$ Developed RESTful APIs and implemented comprehensive database integration\\\\\n$\\bullet$ Participated in Agile development processes and collaborated with cross-functional teams\\\\\n$\\bullet$ Implemented automated testing strategies and ensured application security"
    
    def get_tailored_projects(self, role_focus: str) -> str:
        """Get hobby projects tailored to role focus"""
        
        projects = {
            'devops': """\\jobtitle{Gothenburg TaxiCarPooling Web Application}{Personal Project}{May 2025 - Present}{}
$\\bullet$ Architected intelligent carpooling platform with containerized Spring Boot backend and Node.js microservices\\\\
$\\bullet$ Implemented CI/CD pipelines and infrastructure automation for scalable deployment\\\\
$\\bullet$ Built comprehensive monitoring and logging systems with automated scaling capabilities\\\\
$\\bullet$ Designed PostgreSQL database with optimization for high availability and performance\\\\
$\\bullet$ Developed infrastructure as code and automated testing suites for production reliability

\\jobtitle{SmartTV \\& VoiceBot - Android Auto Applications}{Personal Project}{March 2025 - Present}{}
$\\bullet$ Deployed Android Auto applications with containerized Java backend services and automated deployment\\\\
$\\bullet$ Implemented monitoring and logging systems for real-time performance tracking\\\\
$\\bullet$ Built secure infrastructure with database optimization and automated backup systems\\\\
$\\bullet$ Developed comprehensive testing frameworks with CI/CD integration""",
            
            'backend': """\\jobtitle{Gothenburg TaxiCarPooling Web Application}{Personal Project}{May 2025 - Present}{}
$\\bullet$ Developing intelligent carpooling platform using Spring Boot backend with advanced microservices architecture\\\\
$\\bullet$ Implemented sophisticated order matching algorithm with RESTful APIs for real-time data processing\\\\
$\\bullet$ Designed high-performance PostgreSQL database integration with advanced query optimization\\\\
$\\bullet$ Built comprehensive automated testing suite and implemented robust data protection compliance\\\\
$\\bullet$ Developed scalable backend architecture supporting payment and geolocation service integrations

\\jobtitle{SmartTV \\& VoiceBot - Android Auto Applications}{Personal Project}{March 2025 - Present}{}
$\\bullet$ Developing Android Auto applications with sophisticated Java backend services and modern API architecture\\\\
$\\bullet$ Implemented high-performance RESTful APIs for real-time data processing and voice command integration\\\\
$\\bullet$ Built secure API integrations with advanced SQL database optimization for vehicle data access\\\\
$\\bullet$ Developed comprehensive backend testing framework with performance monitoring""",
            
            'frontend': """\\jobtitle{Gothenburg TaxiCarPooling Web Application}{Personal Project}{May 2025 - Present}{}
$\\bullet$ Developing intelligent carpooling platform with cross-platform React Native mobile application\\\\
$\\bullet$ Built responsive user interfaces with seamless payment and geolocation service integrations\\\\
$\\bullet$ Implemented modern frontend architecture with optimized user experience and performance\\\\
$\\bullet$ Developed comprehensive frontend testing suite with automated UI validation\\\\
$\\bullet$ Created intuitive user interfaces for real-time order matching and communication features

\\jobtitle{SmartTV \\& VoiceBot - Android Auto Applications}{Personal Project}{March 2025 - Present}{}
$\\bullet$ Developing Android Auto applications with modern frontend interfaces and intuitive user experience\\\\
$\\bullet$ Built responsive user interfaces with voice command integration and real-time feedback\\\\
$\\bullet$ Implemented modern frontend frameworks with seamless backend API integration\\\\
$\\bullet$ Developed comprehensive frontend testing framework with cross-platform compatibility""",
            
            'fullstack': """\\jobtitle{Gothenburg TaxiCarPooling Web Application}{Personal Project}{May 2025 - Present}{}
$\\bullet$ Developing intelligent carpooling platform using Spring Boot backend and Node.js microservices\\\\
$\\bullet$ Cross-platform mobile application with React Native, integrating payment and geolocation services\\\\
$\\bullet$ Implemented automated order matching algorithm and RESTful APIs for real-time data processing\\\\
$\\bullet$ Designed system with PostgreSQL database integration and optimized for scalability and performance\\\\
$\\bullet$ Built comprehensive automated testing suite and ensured data protection compliance

\\jobtitle{SmartTV \\& VoiceBot - Android Auto Applications}{Personal Project}{March 2025 - Present}{}
$\\bullet$ Developing Android Auto apps with Java backend services and modern frontend interfaces\\\\
$\\bullet$ Implemented RESTful APIs for real-time data processing and voice command integration\\\\
$\\bullet$ Built secure API integrations with SQL database optimization for vehicle data access\\\\
$\\bullet$ Developed comprehensive testing framework for both frontend and backend components"""
        }
        
        # Always include the e-commerce project
        ecommerce_project = """
\\jobtitle{Hong Yan AB - E-commerce Platform (smrtmart.com)}{Personal Project}{April 2024 - Present}{}
$\\bullet$ Fullstack e-commerce platform with Spring Boot backend and React frontend\\\\
$\\bullet$ Implemented microservices architecture with PostgreSQL and MongoDB database integration\\\\
$\\bullet$ Built comprehensive order management, inventory tracking, and payment processing systems\\\\
$\\bullet$ Developed RESTful APIs for frontend-backend communication and third-party integrations\\\\
$\\bullet$ Optimized application performance for maximum speed and scalability"""
        
        return projects.get(role_focus, projects['fullstack']) + ecommerce_project
    
    def create_tailored_cover_letter(self, job: Dict, role_focus: str, skills: List[str]) -> str:
        """Create job-specific cover letter"""
        
        company = job.get('company', 'Your Company')
        title = job.get('title', 'Developer Position')
        
        # Role-specific introduction paragraphs
        intro_paragraphs = {
            'devops': f"I am writing to express my strong interest in the {title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my DevOps expertise, infrastructure automation skills, and passion for scalable cloud solutions to your team.",
            
            'backend': f"I am writing to express my strong interest in the {title} position at {company}. With over 5 years of hands-on experience in backend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Java/Spring Boot, microservices architecture, and scalable backend solutions to your team.",
            
            'frontend': f"I am writing to express my strong interest in the {title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my frontend expertise, modern framework knowledge, and passion for exceptional user experiences to your team.",
            
            'fullstack': f"I am writing to express my strong interest in the {title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my technical expertise and passion for scalable software solutions to your team."
        }
        
        cl_template = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

% Define dark blue color (LinkedIn blue)
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue,
    pdfauthor={{Hongzhi Li}},
    pdftitle={{Hongzhi Li - {title} Cover Letter}}
}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{10pt}}

\\begin{{document}}

% Header
\\begin{{center}}
{{\\LARGE \\textbf{{\\textcolor{{darkblue}}{{Hongzhi Li}}}}}}\\\\
\\vspace{{5pt}}
{{\\large \\textcolor{{darkblue}}{{Fullstack Developer}}}}\\\\
\\vspace{{10pt}}
\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} --- 0728384299 --- 
\\href{{https://linkedin.com/in/hongzhi-li}}{{LinkedIn}} --- 
\\href{{https://github.com/bluehawana}}{{GitHub}}
\\end{{center}}

\\vspace{{20pt}}

\\today

{company} Hiring Team\\\\
{company}\\\\
Hiring Department

\\vspace{{20pt}}

\\textbf{{\\textcolor{{darkblue}}{{Subject: Application for {title} Position}}}}

Dear Hiring Manager,

{intro_paragraphs.get(role_focus, intro_paragraphs['fullstack'])}

In my current position, I have been leading infrastructure optimization projects and implementing cost-effective solutions, including migrating from Azure Kubernetes Service to local Kubernetes clusters. My experience spans the entire technology stack, from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core. I have successfully built microservices architectures, implemented RESTful APIs, and managed complex database integrations across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications at Synteda, has given me valuable experience in building scalable, enterprise-level applications. I have consistently delivered projects that improve system reliability and reduce operational costs.

\\textbf{{\\textcolor{{darkblue}}{{Key highlights of my experience include:}}}}
\\begin{{itemize}}
{self.get_role_specific_highlights(role_focus)}
\\end{{itemize}}

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals, along with my practical experience in containerization and microservices, position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience in {role_focus} development and infrastructure optimization can contribute to {company}'s continued success. Thank you for considering my application.

\\vspace{{20pt}}

Best regards,

Hongzhi Li

\\end{{document}}"""
        
        return cl_template
    
    def get_role_specific_highlights(self, role_focus: str) -> str:
        """Get role-specific highlights for cover letter"""
        highlights = {
            'devops': "\\item Leading infrastructure optimization and implementing automated deployment pipelines\n\\item Migrating from AKS to local Kubernetes clusters, reducing operational costs\n\\item Implementing modern monitoring solutions using Grafana and advanced scripting\n\\item Managing complex network systems and providing DevOps solution design\n\\item Working with diverse technology stacks including Docker, Kubernetes, AWS, and Azure",
            
            'backend': "\\item Developing comprehensive backend systems using Java/Spring Boot and .NET Core\n\\item Building scalable microservices architectures and RESTful APIs\n\\item Implementing database optimization and performance tuning strategies\n\\item Leading backend system integration and technical solution design\n\\item Working with diverse technology stacks including Java, C\\#, Python, and cloud platforms",
            
            'frontend': "\\item Building modern frontend applications using Angular, React, and Vue.js\n\\item Implementing responsive design and cross-platform user interfaces\n\\item Developing seamless frontend-backend integration and API consumption\n\\item Creating user-centric interfaces with optimal performance and UX\n\\item Working with diverse frontend technologies including TypeScript, React Native, and modern build tools",
            
            'fullstack': "\\item Leading infrastructure optimization and system integration projects\n\\item Developing comprehensive talent management systems using modern cloud architectures\n\\item Implementing CI/CD pipelines and automated testing frameworks\n\\item Managing complex network systems and providing technical solution design\n\\item Working with diverse technology stacks including Java, C\\#, Python, and JavaScript"
        }
        
        return highlights.get(role_focus, highlights['fullstack'])
    
    def compile_latex_to_pdf(self, tex_content: str, output_name: str) -> Optional[str]:
        """Compile LaTeX content to PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            try:
                # Run pdflatex twice for proper references
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
                    # Copy to current directory
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    return final_path
                else:
                    return None
                    
            except Exception as e:
                print(f"❌ Compilation error for {output_name}: {e}")
                return None
    
    def send_application_email(self, job: Dict, cv_path: str, cl_path: str) -> bool:
        """Send application email with CV and cover letter attachments"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        company = job.get('company', 'Company')
        title = job.get('title', 'Position')
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Application: {title} at {company}"
            
            # Email body
            body = f"""Hi,

New job application processed by JobHunter automation system:

🏢 Company: {company}
💼 Position: {title}
📍 Location: {job.get('location', 'Not specified')}
🔗 URL: {job.get('url', 'Not available')}

📎 Documents attached:
   • CV tailored for {title}
   • Cover letter customized for {company}

Best regards,
JobHunter Automation System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDFs
            for file_path, filename in [(cv_path, f"CV_{company}_{title}.pdf"), 
                                       (cl_path, f"CoverLetter_{company}_{title}.pdf")]:
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
            
            print(f"✅ Email sent for {title} at {company}")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed for {title} at {company}: {e}")
            return False

async def get_jobs_from_database() -> List[Dict]:
    """Get jobs from Supabase database"""
    # Mock jobs for testing - replace with actual Supabase query
    mock_jobs = [
        {
            'id': 1,
            'title': 'Senior Backend Developer',
            'company': 'Spotify Technology',
            'location': 'Stockholm, Sweden',
            'description': 'We are looking for a Senior Backend Developer to join our music streaming platform team. Key technologies: Java, Spring Boot, Kubernetes, PostgreSQL, microservices architecture.',
            'url': 'https://careers.spotify.com/backend-developer',
            'job_type': 'fulltime',
            'experience_level': 'senior'
        },
        {
            'id': 2,
            'title': 'DevOps Engineer',
            'company': 'Volvo Cars',
            'location': 'Gothenburg, Sweden',
            'description': 'Join our DevOps team to build and maintain CI/CD pipelines for automotive software. Technologies: Kubernetes, Docker, AWS, Jenkins, Terraform, monitoring with Grafana.',
            'url': 'https://careers.volvocars.com/devops-engineer',
            'job_type': 'fulltime',
            'experience_level': 'mid'
        },
        {
            'id': 3,
            'title': 'Fullstack Developer',
            'company': 'Klarna Bank',
            'location': 'Stockholm, Sweden',
            'description': 'Looking for a Fullstack Developer to work on our fintech platform. Tech stack: React, Node.js, Java, Spring Boot, PostgreSQL, AWS, microservices.',
            'url': 'https://careers.klarna.com/fullstack-developer',
            'job_type': 'fulltime',
            'experience_level': 'mid'
        }
    ]
    
    return mock_jobs

async def main():
    """Main workflow function"""
    processor = JobApplicationProcessor()
    
    print("🚀 Starting JobHunter Complete Workflow")
    print("=" * 60)
    
    # Get jobs from database
    print("📋 Fetching jobs from database...")
    jobs = await get_jobs_from_database()
    print(f"✅ Found {len(jobs)} jobs to process")
    
    successful_applications = 0
    
    # Process each job
    for i, job in enumerate(jobs, 1):
        print(f"\n🔄 Processing Job {i}/{len(jobs)}: {job['title']} at {job['company']}")
        print("-" * 50)
        
        try:
            # Extract skills and determine role focus
            skills = processor.extract_key_skills_from_description(job['description'], job['title'])
            role_focus = processor.determine_role_focus(job['title'], skills)
            
            print(f"📊 Role Focus: {role_focus}")
            print(f"🔧 Key Skills: {', '.join(skills[:5])}")  # Show first 5 skills
            
            # Generate tailored documents
            print("📄 Generating tailored CV...")
            cv_content = processor.create_tailored_cv(job, role_focus, skills)
            
            print("📄 Generating tailored cover letter...")
            cl_content = processor.create_tailored_cover_letter(job, role_focus, skills)
            
            # Create file names
            company_safe = processor.normalize_job_title(job['company'])
            title_safe = processor.normalize_job_title(job['title'])
            
            cv_name = f"hongzhi_{title_safe}_{company_safe}_cv"
            cl_name = f"hongzhi_{title_safe}_{company_safe}_cl"
            
            # Compile PDFs
            print("🔨 Compiling CV PDF...")
            cv_pdf = processor.compile_latex_to_pdf(cv_content, cv_name)
            
            print("🔨 Compiling cover letter PDF...")
            cl_pdf = processor.compile_latex_to_pdf(cl_content, cl_name)
            
            if cv_pdf and cl_pdf:
                # Send email
                print("📧 Sending application email...")
                email_sent = processor.send_application_email(job, cv_pdf, cl_pdf)
                
                if email_sent:
                    successful_applications += 1
                    print(f"🎉 SUCCESS: Application sent for {job['title']} at {job['company']}")
                    
                    # Clean up PDFs after sending
                    try:
                        os.remove(cv_pdf)
                        os.remove(cl_pdf)
                    except:
                        pass
                else:
                    print(f"❌ FAILED: Email not sent for {job['title']} at {job['company']}")
            else:
                print(f"❌ FAILED: PDF generation failed for {job['title']} at {job['company']}")
                
        except Exception as e:
            print(f"❌ ERROR processing {job['title']} at {job['company']}: {e}")
        
        # Add delay between applications to avoid overwhelming the email server
        if i < len(jobs):
            print("⏳ Waiting 5 seconds before next application...")
            await asyncio.sleep(5)
    
    # Final summary
    print(f"\n📊 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Successful applications: {successful_applications}/{len(jobs)}")
    print(f"📧 All emails sent to: {processor.recipient_email}")
    print(f"🎯 Check your inbox for {successful_applications} job applications!")

if __name__ == "__main__":
    asyncio.run(main())