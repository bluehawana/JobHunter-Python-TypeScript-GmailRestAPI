import os
import subprocess
import tempfile
import logging
from typing import Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class LaTeXResumeService:
    """Service for generating customized LaTeX resumes and cover letters"""
    
    def __init__(self):
        # Your base CV template
        self.cv_template = r"""\documentclass[11pt,a4paper]{{article}}
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
{\Large \textit{{{job_role}}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\end{center}

% Personal Profile
\section*{Profile Summary}
{customized_profile}

% Areas of Expertise
\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
{skills_content}
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
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture, serving multiple client organizations
\item Built complete office management platform from scratch, architecting both frontend and backend components with scalable microservices design
\item Participated in business negotiations and requirement gathering sessions, bridging the gap between technical solutions and business objectives
\item Provided Azure cloud consulting services to cross-functional teams, resolving complex cloud infrastructure and integration challenges
\item Implemented RESTful APIs and microservices for scalable application architecture with comprehensive monitoring and logging
\item Integrated SQL and NoSQL databases with optimized query performance, data protection measures, and automated backup strategies
\item Led technical consulting sessions with stakeholders to align cloud solutions with business requirements and cost optimization goals
\item Mentored development teams on Azure best practices, cloud security, and modern development methodologies
\end{itemize}

\subsection*{IT-Högskolan | Cloud Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Supported developer teams by migrating "Omstallningsstod.se" adult education platform to Azure cloud services
\item Provided Azure cloud services integration and support for development teams using Spring Boot backend
\item Implemented Azure Key Vault for secure credential management and cloud infrastructure optimization
\item Established cloud-based development environment and Azure services configuration for team productivity
\end{itemize}

\subsection*{Senior Material (Europe) AB | Platform Architect \& Project Coordinator}
\textit{January 2022 - December 2022 | Eskilstuna, Sweden}
\begin{itemize}[noitemsep]
\item Led migration of business-critical applications with microservices architecture, serving as technical bridge between Swedish subsidiary and Senior Group in China
\item Architected and implemented unified platform solutions meeting both Chinese group standards and Swedish local regulatory requirements
\item Coordinated cross-cultural technical communications and facilitated knowledge transfer between international development teams
\item Managed MS365 and SharePoint integration projects, ensuring seamless collaboration between European and Asian operations
\item Designed and implemented networking infrastructure and security protocols compliant with both Chinese and Swedish standards
\item Oversaw factory facilities IT setup and industrial system integrations for manufacturing operations
\item Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption across multiple regional platforms
\item Led technical requirements analysis and solution design for complex international business scenarios
\item Participated in Agile ceremonies and coordinated sprint planning across different time zones and cultural contexts
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

\section*{Hobby Projects}

\subsection{Gothenburg TaxiCarPooling Web Application}
\textit{May 2025 - Present}
\begin{itemize}
\item Developing intelligent carpooling platform using Spring Boot backend and Node.js microservices
\item Cross-platform mobile application with React Native, integrating payment and geolocation services
\item Implemented automated order matching algorithm and RESTful APIs for real-time data processing
\item Designed system with PostgreSQL database integration and optimized for scalability and performance
\item Built comprehensive automated testing suite and ensured data protection compliance
\end{itemize}

\subsection{EcarxTV \& EcarxBot - Android Auto Applications}
\textit{March 2025 - Present}
\begin{itemize}
\item Developing Android Auto apps with Java backend services and modern frontend interfaces
\item Implemented RESTful APIs for real-time data processing and voice command integration
\item Built secure API integrations with SQL database optimization for vehicle data access
\item Developed comprehensive testing framework for both frontend and backend components
\end{itemize}

\subsection{Hong Yan AB - E-commerce Platform (smrtmart.com)}
\textit{April 2024 - Present}
\begin{itemize}
\item Fullstack e-commerce platform with Spring Boot backend and React frontend
\item Implemented microservices architecture with PostgreSQL and MongoDB database integration
\item Built comprehensive order management, inventory tracking, and payment processing systems
\item Developed RESTful APIs for frontend-backend communication and third-party integrations
\item Optimized application performance for maximum speed and scalability
\end{itemize}

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
\item \textbf{Languages:} Fluent in English and Mandarin, B2 for Swedish
\item \textbf{Interests:} Vehicle technology, energy sector, new media platform
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\item \textbf{Customer Websites:} \href{https://www.senior798.eu}{senior798.eu}, \href{https://www.mibo.se}{mibo.se}, \href{https://www.omstallningsstod.se}{omstallningsstod.se}
\end{itemize}

\end{document}"""

        # Your cover letter template
        self.cover_letter_template = r"""\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{titlesec}}
\usepackage{{hyperref}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}

% Define colors
\definecolor{{darkblue}}{{rgb}}{{0.0, 0.2, 0.6}}

% Section formatting
\titleformat{{\section}}{{\large\bfseries\raggedright\color{{black}}}}{{}}{{0em}}{{}}[\titlerule]
\titleformat{{\subsection}}[runin]{{\bfseries}}{{}}{{0em}}{{}}[:]

% Remove paragraph indentation
\setlength{{\parindent}}{{0pt}}

\begin{{document}}

\pagestyle{{empty}} % no page number

\begin{{letter}}{{\textcolor{{darkblue}}{{\\
{company_name}\\
{company_address}
}}}}\\

\vspace{{40pt}}

\opening{{Dear {hiring_manager},}}
\vspace{{10pt}}

{cover_letter_body}

\vspace{{20pt}}
Sincerely,

Hongzhi Li\\

{current_date}

\vspace{{40pt}}
{{\color{{darkblue}}\rule{{\linewidth}}{{0.6pt}}}}
\vspace{{4pt}}

\closing{{\color{{darkblue}} Ebbe Lieberathsgatan 27\\
412 65 Göteborg\\
hongzhili01@gmail.com\\
0728384299}}\\
\vspace{{10pt}}

\end{{letter}}

\end{{document}}"""
    
    async def generate_customized_cv(self, job: Dict) -> bytes:
        """Generate customized CV based on job requirements"""
        try:
            # Extract job information
            job_title = job.get('title', 'Software Developer')
            job_description = job.get('description', '')
            job_keywords = job.get('keywords', [])
            company = job.get('company', '')
            
            # Customize job role in header
            job_role = self._determine_job_role(job_title, job_keywords)
            
            # Generate customized profile summary
            customized_profile = self._generate_customized_profile(job, job_description, job_keywords)
            
            # Generate relevant skills section
            skills_content = self._generate_relevant_skills(job_keywords, job_description)
            
            # Fill in the template
            cv_content = self.cv_template.format(
                job_role=job_role,
                customized_profile=customized_profile,
                skills_content=skills_content
            )
            
            # Compile LaTeX to PDF
            pdf_content = await self._compile_latex_to_pdf(cv_content, f"cv_{company}")
            
            return pdf_content
            
        except Exception as e:
            logger.error("Error generating customized CV: %s", e)
            # Return basic CV if customization fails
            return await self._compile_latex_to_pdf(self.cv_template.format(
                job_role="Fullstack Developer",
                customized_profile=self._get_default_profile(),
                skills_content=self._get_default_skills()
            ), "cv_default")
    
    async def generate_customized_cover_letter(self, job: Dict) -> bytes:
        """Generate customized cover letter based on job"""
        try:
            company_name = job.get('company', 'Your Company')
            job_title = job.get('title', 'the position')
            job_description = job.get('description', '')
            job_url = job.get('url', '')
            
            # Generate cover letter body
            cover_letter_body = self._generate_cover_letter_body(job, job_description)
            
            # Determine hiring manager greeting
            hiring_manager = self._determine_hiring_manager(job_description)
            
            # Fill in template
            cover_letter_content = self.cover_letter_template.format(
                company_name=company_name,
                company_address=self._get_company_address(company_name),
                hiring_manager=hiring_manager,
                cover_letter_body=cover_letter_body,
                current_date=datetime.now().strftime("%Y.%m.%d")
            )
            
            # Compile to PDF
            pdf_content = await self._compile_latex_to_pdf(
                cover_letter_content, 
                f"cover_letter_{company_name}"
            )
            
            return pdf_content
            
        except Exception as e:
            logger.error("Error generating cover letter: %s", e)
            # Return basic cover letter if customization fails
            return await self._compile_latex_to_pdf(
                self._get_default_cover_letter(job),
                "cover_letter_default"
            )
    
    def _determine_job_role(self, job_title: str, keywords: list) -> str:
        """Determine the most appropriate job role for CV header"""
        title_lower = job_title.lower()
        keywords_lower = [k.lower() for k in keywords]
        
        # Role mapping based on job title and keywords
        if any(term in title_lower for term in ['fullstack', 'full stack', 'full-stack']):
            return "Fullstack Developer"
        elif any(term in title_lower for term in ['devops', 'devsecops']):
            return "DevOps Engineer"
        elif any(term in title_lower for term in ['cloud', 'azure', 'aws']):
            return "Cloud Developer"
        elif any(term in title_lower for term in ['architect']):
            return "Platform Architect"
        elif any(term in title_lower for term in ['backend', 'back-end']):
            return "Backend Developer"
        elif any(term in title_lower for term in ['frontend', 'front-end']):
            return "Frontend Developer"
        elif any(term in title_lower for term in ['java']):
            return "Java Developer"
        elif any(term in title_lower for term in ['c#', '.net']):
            return ".NET Developer"
        else:
            return "Software Developer"
    
    def _generate_customized_profile(self, job: Dict, description: str, keywords: list) -> str:
        """Generate customized profile summary based on job"""
        base_profile = "Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies."
        
        # Identify key technologies mentioned in job
        tech_mentions = []
        description_lower = description.lower()
        keywords_lower = [k.lower() for k in keywords]
        all_content = f"{description_lower} {' '.join(keywords_lower)}"
        
        # Technology mapping
        tech_map = {
            'java': 'Java/Spring Boot',
            'spring': 'Spring Boot',
            'c#': 'C#/.NET Core',
            '.net': '.NET Core',
            'azure': 'Azure cloud services',
            'aws': 'AWS cloud platforms',
            'react': 'React/Angular frontend frameworks',
            'angular': 'Angular/React frameworks',
            'microservices': 'microservices architecture',
            'kubernetes': 'Kubernetes container orchestration',
            'docker': 'Docker containerization',
            'devops': 'DevOps practices and CI/CD pipelines'
        }
        
        for tech, description_text in tech_map.items():
            if tech in all_content:
                tech_mentions.append(description_text)
        
        # Build customized profile
        if tech_mentions:
            tech_list = ', '.join(tech_mentions[:3])  # Limit to top 3
            customized_profile = f"""Experienced Fullstack Developer with over 5 years of hands-on experience specializing in {tech_list}. Proven expertise in building scalable full-stack applications with comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, modern web technologies, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments."""
        else:
            customized_profile = base_profile + " Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development."
        
        return customized_profile
    
    def _generate_relevant_skills(self, keywords: list, description: str) -> str:
        """Generate skills section emphasizing job-relevant technologies"""
        
        # Your complete skills organized by category
        skills_categories = {
            "Programming Languages": ["Java/J2EE", "JavaScript", "C#/.NET Core", "Python", "Bash", "PowerShell"],
            "Frontend Frameworks": ["Angular", "ReactJS", "React Native", "Vue.js", "HTML5", "CSS3"],
            "Backend Frameworks": ["Spring", "Spring Boot", "Spring MVC", ".NET Core", "ASP.NET", "Node.js"],
            "API Development": ["RESTful APIs", "GraphQL", "Microservices Architecture"],
            "Databases": ["PostgreSQL", "MySQL", "MongoDB", "AWS RDS", "Azure Cosmos DB", "S3"],
            "Testing": ["Unit Testing", "Integration Testing", "Automated Testing", "JUnit", "Jest"],
            "Cloud Platforms": ["AWS", "Azure", "GCP"],
            "Containerization": ["Docker", "Kubernetes", "Azure Kubernetes Service (AKS)"],
            "Version Control": ["Git", "GitHub", "GitLab"],
            "CI/CD": ["Jenkins", "GitHub Actions", "GitLab CI"],
            "Agile Methodologies": ["Scrum", "Kanban", "Sprint Planning", "Code Reviews"]
        }
        
        # Identify relevant keywords from job
        all_content = f"{' '.join(keywords)} {description}".lower()
        relevant_categories = []
        
        # Check which categories are most relevant
        for category, skills in skills_categories.items():
            relevance_score = 0
            for skill in skills:
                if any(word in all_content for word in skill.lower().split('/')):
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_categories.append((category, skills, relevance_score))
        
        # Sort by relevance and build skills content
        relevant_categories.sort(key=lambda x: x[2], reverse=True)
        
        skills_items = []
        for category, skills, _ in relevant_categories[:8]:  # Top 8 most relevant categories
            skills_text = ", ".join(skills)
            skills_items.append(f"\\item \\textbf{{{category}:}} {skills_text}")
        
        return "\n".join(skills_items)
    
    def _generate_cover_letter_body(self, job: Dict, description: str) -> str:
        """Generate customized cover letter body"""
        job_title = job.get('title', 'the position')
        company_name = job.get('company', 'your company')
        
        # Extract key requirements from job description
        key_techs = self._extract_key_technologies(description, job.get('keywords', []))
        
        # Build customized paragraphs
        intro = f"I am writing to express my sincere interest in the {job_title} role at {company_name}."
        
        if 'devops' in job_title.lower():
            experience_para = "As a seasoned DevOps professional with extensive experience in CI/CD pipeline design, cloud infrastructure management, and container orchestration, I am excited by the opportunity to contribute to your team's automation and deployment processes."
        elif 'cloud' in job_title.lower():
            experience_para = "As an experienced Cloud Developer with proven expertise in Azure and AWS cloud platforms, microservices architecture, and cloud-native application development, I am confident in my ability to contribute to your cloud transformation initiatives."
        elif 'fullstack' in job_title.lower():
            experience_para = "As an experienced Fullstack Developer with over 5 years of expertise in both frontend and backend technologies, I am excited about the opportunity to contribute to your development team with my comprehensive technical skill set."
        else:
            experience_para = f"With my proven experience in {', '.join(key_techs[:3]) if key_techs else 'modern software development'}, I am confident in my ability to contribute effectively to your team and deliver high-quality solutions."
        
        # Technical alignment paragraph
        if key_techs:
            tech_para = f"My hands-on experience with {', '.join(key_techs)} aligns perfectly with your requirements. Throughout my career at companies like ECARX, Synteda, and Senior Material, I have consistently demonstrated expertise in building scalable applications, implementing cloud solutions, and working in collaborative agile environments."
        else:
            tech_para = "Throughout my career at companies like ECARX, Synteda, and Senior Material, I have consistently demonstrated expertise in building scalable applications, implementing modern development practices, and working effectively in collaborative agile environments."
        
        # Closing paragraph
        closing_para = f"I am impressed by {company_name}'s commitment to innovation and would welcome the opportunity to contribute to your team's success. Thank you for considering my application, and I look forward to discussing how my experience and passion can benefit your organization."
        
        return f"{intro} {experience_para}\\n\\n{tech_para}\\n\\n{closing_para}"
    
    def _extract_key_technologies(self, description: str, keywords: list) -> list:
        """Extract key technologies mentioned in job posting"""
        content = f"{description} {' '.join(keywords)}".lower()
        
        # Technology keywords to look for
        tech_keywords = [
            'java', 'spring boot', 'c#', '.net', 'python', 'javascript',
            'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'gcp', 'kubernetes', 'docker',
            'postgresql', 'mysql', 'mongodb',
            'microservices', 'api', 'rest', 'graphql',
            'ci/cd', 'jenkins', 'devops', 'terraform'
        ]
        
        found_techs = []
        for tech in tech_keywords:
            if tech in content:
                found_techs.append(tech)
        
        return found_techs[:5]  # Return top 5 most relevant
    
    def _determine_hiring_manager(self, description: str) -> str:
        """Determine appropriate greeting for cover letter"""
        # Look for specific names or titles in job description
        if 'linda' in description.lower():
            return "Linda"
        elif any(title in description.lower() for title in ['hr manager', 'hiring manager', 'recruitment']):
            return "Hiring Manager"
        else:
            return "Hiring Manager"
    
    def _get_company_address(self, company_name: str) -> str:
        """Get company address or use generic Swedish address"""
        # You could expand this with a database of company addresses
        return f"{company_name}\\\\Göteborg, Sweden"
    
    async def _compile_latex_to_pdf(self, latex_content: str, filename: str) -> bytes:
        """Compile LaTeX content to PDF"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write LaTeX content to file
                tex_file = os.path.join(temp_dir, f"{filename}.tex")
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile LaTeX to PDF
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', temp_dir,
                    tex_file
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error("LaTeX compilation failed: %s", result.stderr)
                    raise Exception(f"LaTeX compilation failed: {result.stderr}")
                
                # Read PDF content
                pdf_file = os.path.join(temp_dir, f"{filename}.pdf")
                if os.path.exists(pdf_file):
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                else:
                    raise Exception("PDF file not generated")
                    
        except Exception as e:
            logger.error("Error compiling LaTeX: %s", e)
            # Return empty bytes if compilation fails
            return b""
    
    def _get_default_profile(self) -> str:
        """Get default profile summary"""
        return """Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments."""
    
    def _get_default_skills(self) -> str:
        """Get default skills section"""
        return """\\item \\textbf{Programming Languages:} Java/J2EE, JavaScript, C\\#/.NET Core, Python, Bash, PowerShell
\\item \\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
\\item \\textbf{Backend Frameworks:} Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
\\item \\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture
\\item \\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3
\\item \\textbf{Cloud Platforms:} AWS, Azure, GCP
\\item \\textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)
\\item \\textbf{Version Control:} Git, GitHub, GitLab"""
    
    def _get_default_cover_letter(self, job: Dict) -> str:
        """Get default cover letter"""
        company_name = job.get('company', 'Your Company')
        job_title = job.get('title', 'the position')
        
        return self.cover_letter_template.format(
            company_name=company_name,
            company_address=f"{company_name}\\\\Sweden",
            hiring_manager="Hiring Manager",
            cover_letter_body=f"I am writing to express my interest in the {job_title} position at {company_name}. With my extensive experience in fullstack development and cloud technologies, I believe I would be a valuable addition to your team.",
            current_date=datetime.now().strftime("%Y.%m.%d")
        )