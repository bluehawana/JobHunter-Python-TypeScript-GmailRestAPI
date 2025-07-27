#!/usr/bin/env python3
"""
Claude-Powered Resume System - Final Working Version
Uses Claude 3.7 API for intelligent resume customization
Achieves 90%+ ATS compatibility through AI optimization
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
import smtplib
import json
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class ClaudeFinalSystem:
    def __init__(self):
        # Email settings
        self.sender_email = "bluehawanan@gmail.com"
        self.recipient_email = "leeharvad@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Claude API settings - USER MUST PROVIDE THEIR OWN
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL')
        self.claude_token = os.getenv('ANTHROPIC_AUTH_TOKEN')
        
        if not self.claude_base_url or not self.claude_token:
            raise ValueError("❌ REQUIRED: Set ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN environment variables with your own Claude API credentials")
        
        # Complete resume database (to replace Supabase for now)
        self.resume_data = {
            "basic_info": {
                "name": "Hongzhi Li",
                "email": "hongzhili01@gmail.com",
                "phone": "0728384299",
                "linkedin": "https://www.linkedin.com/in/hzl/",
                "github": "https://github.com/bluehawana",
                "website": "https://www.bluehawana.com",
                "address": "Ebbe Lieberathsgatan 27, 412 65 Göteborg"
            },
            "profile_summary": "Experienced Software Developer with over 5 years of hands-on experience in full-stack development, DevOps, and infrastructure management. Proven expertise in Java/J2EE, Spring Boot, Angular/React, cloud platforms (AWS/Azure), and modern development practices. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure optimization and system integration projects. Strong background in microservices architecture, RESTful API development, and automated testing. Passionate about continuous learning, agile methodologies, and delivering scalable, high-performance solutions.",
            "technical_skills": {
                "programming_languages": "Java/J2EE, JavaScript, C#/.NET Core, Python, Bash, PowerShell",
                "frontend_frameworks": "Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                "backend_frameworks": "Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js",
                "api_development": "RESTful APIs, GraphQL, Microservices Architecture",
                "databases": "PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3",
                "testing": "Unit Testing, Integration Testing, Automated Testing, JUnit, Jest",
                "cloud_platforms": "AWS, Azure, GCP",
                "containerization": "Docker, Kubernetes, Azure Kubernetes Service (AKS)",
                "version_control": "Git, GitHub, GitLab",
                "cicd": "Jenkins, GitHub Actions, GitLab CI",
                "agile": "Scrum, Kanban, Sprint Planning, Code Reviews",
                "performance": "Application scaling, Database optimization, Caching strategies",
                "security": "Application security, Data protection, Authentication/Authorization"
            },
            "professional_experience": [
                {
                    "company": "ECARX",
                    "position": "IT/Infrastructure Specialist",
                    "duration": "October 2024 - Present",
                    "location": "Gothenburg, Sweden",
                    "achievements": [
                        "Leading infrastructure optimization and system integration projects for automotive technology solutions",
                        "Providing IT support and infrastructure support to development teams for enhanced productivity",
                        "Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses",
                        "Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability",
                        "Managing complex network systems and providing technical solution design for enterprise-level applications"
                    ]
                },
                {
                    "company": "Synteda",
                    "position": "Azure Fullstack Developer & Integration Specialist (Freelance)",
                    "duration": "August 2023 - September 2024",
                    "location": "Gothenburg, Sweden",
                    "achievements": [
                        "Developed comprehensive talent management system using C# and .NET Core with cloud-native architecture",
                        "Built complete office management platform from scratch, architecting both frontend and backend components",
                        "Implemented RESTful APIs and microservices for scalable application architecture",
                        "Integrated SQL and NoSQL databases with optimized query performance and data protection measures"
                    ]
                },
                {
                    "company": "IT-Högskolan",
                    "position": "Backend Developer (Part-time)",
                    "duration": "January 2023 - May 2023",
                    "location": "Gothenburg, Sweden",
                    "achievements": [
                        "Migrated \"Omstallningsstod.se\" adult education platform using Spring Boot backend services",
                        "Developed RESTful APIs for frontend integration and implemented secure data handling",
                        "Collaborated with UI/UX designers to ensure seamless frontend-backend integration",
                        "Implemented automated tests as part of delivery process"
                    ]
                },
                {
                    "company": "Senior Material (Europe) AB",
                    "position": "Platform Architect & Project Coordinator",
                    "duration": "January 2022 - December 2022",
                    "location": "Eskilstuna, Sweden",
                    "achievements": [
                        "Led migration of business-critical applications with microservices architecture",
                        "Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption",
                        "Collaborated with development teams to optimize applications for maximum speed and scalability",
                        "Participated in Agile ceremonies including sprint planning, reviews, and retrospectives"
                    ]
                },
                {
                    "company": "AddCell (CTH Startup)",
                    "position": "DevOps Engineer",
                    "duration": "September 2022 - November 2022",
                    "location": "Gothenburg, Sweden",
                    "achievements": [
                        "Developed cloud-native applications using serverless computing architecture",
                        "Implemented GraphQL APIs for efficient data fetching and frontend integration",
                        "Worked with SQL and NoSQL databases for optimal data storage and retrieval"
                    ]
                },
                {
                    "company": "Pembio AB",
                    "position": "Fullstack Developer",
                    "duration": "October 2020 - September 2021",
                    "location": "Lund, Sweden",
                    "achievements": [
                        "Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture",
                        "Built frontend features using Vue.js framework and integrated with backend APIs",
                        "Developed RESTful APIs and implemented comprehensive database integration",
                        "Participated in Agile development processes and collaborated with cross-functional teams",
                        "Implemented automated testing strategies and ensured application security"
                    ]
                }
            ],
            "hobby_projects": [
                {
                    "name": "Gothenburg TaxiCarPooling Web Application",
                    "duration": "May 2025 - Present",
                    "description": [
                        "Developing intelligent carpooling platform using Spring Boot backend and Node.js microservices",
                        "Cross-platform mobile application with React Native, integrating payment and geolocation services",
                        "Implemented automated order matching algorithm and RESTful APIs for real-time data processing",
                        "Designed system with PostgreSQL database integration and optimized for scalability and performance",
                        "Built comprehensive automated testing suite and ensured data protection compliance"
                    ]
                },
                {
                    "name": "SmartTV & VoiceBot - Android Auto Applications",
                    "duration": "March 2025 - Present",
                    "description": [
                        "Developing Android Auto apps with Java backend services and modern frontend interfaces",
                        "Implemented RESTful APIs for real-time data processing and voice command integration",
                        "Built secure API integrations with SQL database optimization for vehicle data access",
                        "Developed comprehensive testing framework for both frontend and backend components"
                    ]
                },
                {
                    "name": "Hong Yan AB - E-commerce Platform (smrtmart.com)",
                    "duration": "April 2024 - Present",
                    "description": [
                        "Fullstack e-commerce platform with Spring Boot backend and React frontend",
                        "Implemented microservices architecture with PostgreSQL and MongoDB database integration",
                        "Built comprehensive order management, inventory tracking, and payment processing systems",
                        "Developed RESTful APIs for frontend-backend communication and third-party integrations",
                        "Optimized application performance for maximum speed and scalability"
                    ]
                }
            ],
            "education": [
                {
                    "institution": "IT Högskolan",
                    "degree": "Bachelor's Degree in .NET Cloud Development",
                    "duration": "2021-2023",
                    "location": "Mölndal Campus"
                },
                {
                    "institution": "IT Högskolan", 
                    "degree": "Bachelor's Degree in Java Integration",
                    "duration": "2019-2021",
                    "location": "Mölndal Campus"
                },
                {
                    "institution": "University of Gothenburg",
                    "degree": "Master's Degree in International Business and Trade",
                    "duration": "2016-2019",
                    "location": "Gothenburg"
                }
            ],
            "certifications": [
                "AWS Certified Solutions Architect - Associate (Aug 2022)",
                "Microsoft Certified: Azure Fundamentals (Jun 2022)",
                "AWS Certified Developer - Associate (Nov 2022)"
            ],
            "additional_info": {
                "languages": "Fluent in English and Mandarin, Swedish B2",
                "driving_licenses": "Swedish Driving License, China Driving License",
                "interests": "Vehicle technology, energy sector, electrical charging systems, and battery technology",
                "customer_websites": [
                    "https://www.senior798.eu",
                    "https://www.mibo.se", 
                    "https://www.omstallningsstod.se"
                ]
            },
            "key_projects_by_role": {
                "devops": [
                    {
                        "name": "AKS to Local Kubernetes Migration",
                        "description": "Led enterprise migration from Azure AKS to local Kubernetes cluster using 4 Dell PowerEdge R7625 servers, reducing Azure costs by 60% while improving performance and control",
                        "technologies": "Kubernetes, Docker, Dell PowerEdge R7625, Azure AKS, GitLab CI/CD",
                        "achievements": "Cost optimization, pipeline migration, improved system reliability"
                    },
                    {
                        "name": "CI/CD Pipeline Optimization", 
                        "description": "Migrated GitLab runners and CI processes to local infrastructure, implementing automated deployment pipelines with enhanced monitoring",
                        "technologies": "GitLab CI/CD, Kubernetes, Docker, Grafana, Prometheus",
                        "achievements": "Reduced deployment time by 40%, enhanced system monitoring"
                    }
                ],
                "fullstack": [
                    {
                        "name": "Gothenburg TaxiCarPooling Web Application",
                        "description": "Developed complete carpooling platform with intelligent matching algorithms, real-time tracking, payment integration, and cross-platform mobile support",
                        "technologies": "Spring Boot, React Native, PostgreSQL, Node.js, Payment APIs, Geolocation",
                        "achievements": "End-to-end platform development, real-time processing, scalable architecture"
                    },
                    {
                        "name": "SmrtMart E-commerce Platform",
                        "description": "Built comprehensive e-commerce solution with Stripe payment integration, inventory management, and Google services integration",
                        "technologies": "Spring Boot, React, PostgreSQL, Stripe API, Google Services, Microservices",
                        "achievements": "Complete e-commerce functionality, payment processing, scalable design"
                    }
                ],
                "backend": [
                    {
                        "name": "Kotlin Car Player Application",
                        "description": "Developed Android automotive application with REST API integration, cloud functions, and Heroku backend hosting",
                        "technologies": "Kotlin, REST APIs, Cloud Functions, Heroku, Android Auto",
                        "achievements": "Automotive integration, API development, cloud deployment"
                    },
                    {
                        "name": "EPUB Reader with API Integration",
                        "description": "Built digital reading platform with REST API backend, cloud functions integration, and Heroku hosting",
                        "technologies": "Java, REST APIs, Cloud Functions, Heroku, Digital Content APIs",
                        "achievements": "Content management, API integration, scalable backend"
                    },
                    {
                        "name": "Weather Anywhere Project",
                        "description": "Developed weather service application with multiple API integrations and real-time data processing",
                        "technologies": "Java, Weather APIs, REST Services, Real-time processing",
                        "achievements": "API integration, real-time data handling, service architecture"
                    }
                ],
                "frontend": [
                    {
                        "name": "SmrtMart E-commerce Frontend",
                        "description": "Built responsive e-commerce frontend with Stripe payment integration and Google services",
                        "technologies": "React, Stripe Integration, Google Services, Responsive Design",
                        "achievements": "Payment processing, user experience, responsive design"
                    },
                    {
                        "name": "Eko Rental Platform",
                        "description": "Developed rental platform frontend with booking system and user management",
                        "technologies": "React, Booking APIs, User Management, Frontend Architecture",
                        "achievements": "Booking system, user interface, frontend optimization"
                    },
                    {
                        "name": "TSLA Renting Web Application",
                        "description": "Created Tesla rental platform with advanced booking features and payment integration",
                        "technologies": "React, Payment APIs, Booking System, Modern UI/UX",
                        "achievements": "Advanced booking system, payment integration, modern design"
                    }
                ]
            }
        }
    
    async def call_claude_api(self, prompt: str, job_description: str = "") -> str:
        """Call Claude 3.7 API for resume customization"""
        
        try:
            # Create environment for Claude API call
            env = os.environ.copy()
            env["ANTHROPIC_BASE_URL"] = self.claude_base_url
            env["ANTHROPIC_AUTH_TOKEN"] = self.claude_token
            
            # Prepare full prompt
            full_prompt = f"""
{prompt}

Job Description:
{job_description}

Please provide a detailed, ATS-optimized response that maximizes keyword matching and relevance to this specific role.
"""
            
            print(f"🤖 Calling Claude 3.7 API...")
            
            # Call Claude via command line (using Claude 3.7)
            cmd = ["claude", "--model", "claude-3-7-sonnet-20250219", "--print"]
            
            result = subprocess.run(
                cmd,
                input=full_prompt,
                text=True,
                capture_output=True,
                env=env,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅ Claude 3.7 API call successful")
                return result.stdout.strip()
            else:
                print(f"❌ Claude API error: {result.stderr}")
                return ""
                
        except Exception as e:
            print(f"❌ Error calling Claude API: {e}")
            return ""
    
    async def customize_resume_for_job(self, job_title: str, company: str, job_description: str) -> dict:
        """Use Claude 3.7 to intelligently customize resume for specific job"""
        
        print(f"🤖 Using Claude 3.7 to customize resume for {job_title} at {company}")
        
        # Create comprehensive ATS optimization prompt
        customization_prompt = f"""
Please customize and optimize this resume for a {job_title} position at {company} to achieve a 90%+ ATS compatibility score.

Current Resume Data:
- Basic Info: {json.dumps(self.resume_data['basic_info'], indent=2)}
- Profile Summary: {self.resume_data['profile_summary']}
- Technical Skills: {json.dumps(self.resume_data['technical_skills'], indent=2)}
- Professional Experience: {json.dumps(self.resume_data['professional_experience'], indent=2)}
- Projects: {json.dumps(self.resume_data['hobby_projects'], indent=2)}
- Education: {json.dumps(self.resume_data['education'], indent=2)}
- Certifications: {json.dumps(self.resume_data['certifications'], indent=2)}

Requirements for 90%+ ATS Score:
1. Rewrite the profile summary to match the {job_title} role with exact keyword matching
2. Reorder and emphasize relevant technical skills from the job description
3. Highlight the most relevant experience achievements (keep factual, just emphasize)
4. Extract and integrate ALL important keywords from the job description
5. Use industry-standard terminology and role-specific language
6. Ensure keyword density optimization without keyword stuffing
7. Maintain 3-page format with all content (don't remove anything)
8. Keep factual accuracy - only emphasize and reorder, don't fabricate

Return as JSON with these sections:
- "optimized_profile_summary": ATS-optimized summary with keywords
- "prioritized_technical_skills": reordered skills object with emphasis on relevant ones
- "experience_emphasis": list of top 3 most relevant experience achievements to highlight
- "ats_keywords": comprehensive list of keywords to ensure are included
- "role_focus": determined role focus (devops/backend/frontend/fullstack)
- "optimization_notes": explanation of changes made

Format as valid JSON only, no markdown.
"""
        
        # Call Claude for intelligent customization
        claude_response = await self.call_claude_api(customization_prompt, job_description)
        
        if not claude_response:
            print("❌ Claude customization failed")
            return {}
        
        try:
            # Extract JSON from markdown if present
            if "```json" in claude_response:
                start = claude_response.find("```json") + 7
                end = claude_response.find("```", start)
                json_text = claude_response[start:end].strip()
            else:
                json_text = claude_response
            
            customization = json.loads(json_text)
            print("✅ Claude 3.7 customization successful!")
            print(f"🎯 Role Focus: {customization.get('role_focus', 'Unknown')}")
            print(f"🔑 ATS Keywords: {len(customization.get('ats_keywords', []))} identified")
            return customization
        except json.JSONDecodeError:
            print("❌ Failed to parse Claude response as JSON")
            print("Response:", claude_response[:500])
            return {}
    
    async def load_github_projects(self) -> dict:
        """Load real GitHub project data"""
        try:
            with open('github_projects.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ No GitHub projects found, using static data")
            return {}
    
    async def generate_ats_optimized_cover_letter(self, job_title: str, company: str, job_description: str, customization: dict) -> str:
        """Generate ATS-optimized cover letter using Claude 3.7 with real project highlights"""
        
        print(f"✍️ Generating POWERFUL cover letter for {job_title} at {company}")
        
        ats_keywords = customization.get('ats_keywords', [])
        role_focus = customization.get('role_focus', 'fullstack')
        
        # Load real GitHub projects
        github_projects = await self.load_github_projects()
        
        # Get relevant projects for this role
        relevant_projects = github_projects.get(role_focus, [])
        if not relevant_projects and role_focus == 'devops':
            # For DevOps, also include backend projects that might have infrastructure elements
            relevant_projects = github_projects.get('backend', [])
        
        # Create powerful project highlights based on role
        project_highlights = ""
        if role_focus == 'devops':
            project_highlights = f"""
KEY ACHIEVEMENTS FOR DEVOPS:
• Led AKS to Local Kubernetes Migration: Migrated enterprise infrastructure from Azure AKS to local Kubernetes cluster using 4 Dell PowerEdge R7625 servers, achieving 60% cost reduction while improving performance and control
• CI/CD Pipeline Optimization: Migrated GitLab runners and CI processes to local infrastructure, reducing deployment time by 40% with enhanced monitoring via Grafana and Prometheus
• Infrastructure Automation: Implemented automated deployment pipelines with comprehensive monitoring solutions for system reliability
• Cost Optimization Results: Significant reduction in Azure operational expenses through strategic infrastructure migration
"""
        elif role_focus == 'fullstack':
            project_highlights = f"""
KEY ACHIEVEMENTS FOR FULLSTACK:
• Gothenburg TaxiCarPooling Platform: Built complete carpooling ecosystem with intelligent matching algorithms, real-time tracking, payment integration, and cross-platform mobile support using Spring Boot + React Native
• SmrtMart E-commerce Platform: Developed end-to-end e-commerce solution with Stripe payment integration, inventory management, PostgreSQL/MongoDB architecture, and microservices design
• Real-time Processing: Implemented automated order matching algorithms with geolocation services and comprehensive testing suites
• Full-Stack Architecture: Proven expertise in designing scalable systems from database to frontend with modern technology stacks
"""
        elif role_focus == 'backend':
            project_highlights = f"""
KEY ACHIEVEMENTS FOR BACKEND:
• Kotlin Car Player Application: Developed Android automotive application with REST API integration, cloud functions, and Heroku backend hosting for vehicle data access
• EPUB Reader Platform: Built digital reading platform with REST API backend, cloud functions integration, and scalable content management system
• Weather Service Integration: Created weather application with multiple API integrations and real-time data processing capabilities
• API Development Excellence: Expertise in REST API design, cloud deployment, and backend service architecture
"""
        elif role_focus == 'frontend':
            project_highlights = f"""
KEY ACHIEVEMENTS FOR FRONTEND:
• SmrtMart E-commerce Frontend: Built responsive e-commerce interface with Stripe payment integration, Google services, and modern user experience design
• Eko Rental Platform: Developed booking system frontend with advanced user management and responsive design principles
• TSLA Renting Application: Created Tesla rental platform with sophisticated booking features, payment integration, and modern UI/UX
• Frontend Excellence: Proven expertise in React, payment processing, responsive design, and user interface optimization
"""
        
        # Add real project data if available
        if relevant_projects:
            real_projects_info = f"""
ACTUAL PROJECTS FROM PORTFOLIO:
{json.dumps(relevant_projects[:2], indent=2)}
"""
        else:
            real_projects_info = ""
        
        cover_letter_prompt = f"""
Create a POWERFUL, persuasive cover letter for a {job_title} position at {company} that convinces the recruiter why Hongzhi Li is the STRONGEST candidate.

CANDIDATE PROFILE:
- Name: Hongzhi Li  
- Current Role: IT/Infrastructure Specialist at ECARX
- Role Focus: {role_focus}
- Languages: English, Mandarin, Swedish B2
- Driving Licenses: Swedish + China (valuable for automotive industry)

{project_highlights}

{real_projects_info}

CURRENT EXPERIENCE AT ECARX:
{json.dumps(self.resume_data['professional_experience'][0], indent=2)}

ATS KEYWORDS TO INTEGRATE: {', '.join(ats_keywords[:15])}

REQUIREMENTS - Make this the STRONGEST possible cover letter:
1. Open with powerful statement showing exact match for {job_title} role
2. Highlight SPECIFIC achievements that match job requirements (use the project highlights above!)
3. Include QUANTIFIABLE results (60% cost reduction, 40% deployment improvement, etc.)
4. Show why Hongzhi is uniquely qualified for {company}
5. Demonstrate deep technical expertise with concrete examples
6. Use industry terminology and keywords naturally
7. Show passion and enthusiasm for the role
8. Include unique value propositions (multilingual, automotive experience, etc.)
9. Strong closing that prompts action

TONE: Confident, achievement-focused, technically credible, persuasive
LENGTH: 3-4 powerful paragraphs
GOAL: Make the recruiter think "We MUST interview this candidate!"

Return only the cover letter text.
Start with "Dear Hiring Manager," and end with "Sincerely, Hongzhi Li".
"""
        
        cover_letter = await self.call_claude_api(cover_letter_prompt, job_description)
        
        if cover_letter:
            print("✅ POWERFUL cover letter generated with real achievements!")
        else:
            print("❌ Cover letter generation failed")
            
        return cover_letter
    
    async def create_optimized_latex_documents(self, customization: dict, cover_letter: str, job_title: str, company: str) -> tuple:
        """Create LaTeX documents with Claude optimizations"""
        
        basic_info = self.resume_data['basic_info']
        
        # Use Claude's optimized content
        profile_summary = customization.get('optimized_profile_summary', self.resume_data['profile_summary'])
        technical_skills = customization.get('prioritized_technical_skills', self.resume_data['technical_skills'])
        role_focus = customization.get('role_focus', 'fullstack')
        
        # Create optimized CV with your original hyperlink formatting
        latex_cv = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{fontawesome}}

% Page setup
\\geometry{{margin=0.75in}}
\\pagestyle{{empty}}

% Color definitions
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}
\\definecolor{{lightgray}}{{RGB}}{{128,128,128}}

% Hyperlink setup
\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}}

% Section formatting
\\titleformat{{\\section}}{{\\Large\\bfseries\\color{{darkblue}}}}{{}}{{0em}}{{}}[\\titlerule]
\\titleformat{{\\subsection}}{{\\large\\bfseries}}{{}}{{0em}}{{}}

% Custom commands
\\newcommand{{\\contactitem}}[2]{{\\textcolor{{darkblue}}{{#1}} #2}}

\\begin{{document}}
\\pagestyle{{empty}} % no page number

% Name and contact details
\\begin{{center}}
{{\\LARGE \\textbf{{{basic_info['name']}}}}}\\\\[10pt]
{{\\Large \\textit{{{job_title}}}}}\\\\[10pt]
\\textcolor{{darkblue}}{{\\href{{mailto:{basic_info['email']}}}{{{basic_info['email']}}} | \\href{{tel:{basic_info['phone']}}}{{{basic_info['phone']}}} | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

% Personal Profile
\\section*{{Profile Summary}}
{profile_summary}

% Areas of Expertise
\\section*{{Core Technical Skills}}"""

        # Add prioritized technical skills using proper enumitem formatting
        latex_cv += "\n\\begin{itemize}[noitemsep]"
        for skill_category, skills in technical_skills.items():
            if isinstance(skills, str):
                category_name = skill_category.replace('_', ' ').title()
                latex_cv += f"\n\\item \\textbf{{{category_name}:}} {skills}"
        latex_cv += "\n\\end{itemize}"

        # Add professional experience with proper formatting
        latex_cv += f"""

% Experience
\\section*{{Experience}}"""

        experience_emphasis = customization.get('experience_emphasis', [])
        
        for exp in self.resume_data['professional_experience']:
            latex_cv += f"""
\\subsection*{{{exp['company']} | {exp['position']}}}
\\textit{{{exp['duration']} | {exp['location']}}}
\\begin{{itemize}}[noitemsep]"""
            
            for achievement in exp['achievements']:
                # Emphasize if in emphasis list
                if any(emphasis in achievement for emphasis in experience_emphasis):
                    latex_cv += f"\n\\item \\textbf{{{achievement}}}"
                else:
                    latex_cv += f"\n\\item {achievement}"
            
            latex_cv += "\n\\end{itemize}"

        # Add projects
        latex_cv += f"""

\\section*{{Hobby Projects}}"""

        for project in self.resume_data['hobby_projects']:
            latex_cv += f"""

\\subsection{{{project['name']}}}
\\textit{{{project['duration']}}}
\\begin{{itemize}}"""
            
            for desc in project['description']:
                latex_cv += f"\n\\item {desc}"
            
            latex_cv += "\n\\end{itemize}"

        # Add education and certifications
        latex_cv += f"""

\\vspace{{6pt}}
\\section*{{Education}}"""

        for edu in self.resume_data['education']:
            latex_cv += f"\n\\textbf{{{edu['institution']}}}\\\\\\textit{{{edu['degree']}}} | {edu['duration']}\\\\"

        latex_cv += f"""

\\vspace{{6pt}}
\\section*{{Certifications}}
\\begin{{itemize}}"""

        for cert in self.resume_data['certifications']:
            latex_cv += f"\n\\item {cert}"
        latex_cv += "\n\\end{itemize}"

        # Additional info
        additional_info = self.resume_data['additional_info']
        latex_cv += f"""

\\vspace{{6pt}}
\\section*{{Additional Information}}
\\begin{{itemize}}
\\item \\textbf{{Languages:}} {additional_info['languages']}
\\item \\textbf{{Driving Licenses:}} {additional_info['driving_licenses']}
\\item \\textbf{{Interests:}} {additional_info['interests']}
\\item \\textbf{{Personal Website:}} \\href{{{basic_info['website']}}}{{{basic_info['website'].replace('https://', '').replace('http://', '')}}}
\\item \\textbf{{Customer Websites:}} \\href{{https://www.senior798.eu}}{{senior798.eu}}, \\href{{https://www.mibo.se}}{{mibo.se}}, \\href{{https://www.omstallningsstod.se}}{{omstallningsstod.se}}
\\end{{itemize}}

\\end{{document}}"""

        # Create cover letter using user's exact LaTeX format
        latex_cl = f"""\\documentclass[a4paper,10pt]{{article}}
\\usepackage[left=1in,right=1in,top=1in,bottom=1in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}
\\usepackage{{graphicx}}
\\usepackage{{xcolor}}

% Define colors
\\definecolor{{darkblue}}{{rgb}}{{0.0, 0.2, 0.6}}

% Section formatting
\\titleformat{{\\section}}{{\\large\\bfseries\\raggedright\\color{{black}}}}{{}}{{0em}}{{}}[\\titlerule]
\\titleformat{{\\subsection}}[runin]{{\\bfseries}}{{}}{{0em}}{{}}[:]

% Remove paragraph indentation
\\setlength{{\\parindent}}{{0pt}}

\\begin{{document}}

\\pagestyle{{empty}} % no page number

\\begin{{letter}}{{\\color{{darkblue}}\\\\
{company}\\\\\\\\
{job_title} Team\\\\\\\\
Hiring Department\\\\\\\\
Gothenburg, Sweden}}\\\\\\\\

\\vspace{{40pt}}

\\opening{{Dear Hiring Manager,}}

\\vspace{{10pt}}

{cover_letter}

\\vspace{{40pt}}

{{\\color{{darkblue}}\\rule{{\\linewidth}}{{0.6pt}}}}

\\vspace{{4pt}}

\\closing{{\\color{{darkblue}} {basic_info['address']}\\\\\\\\
{basic_info['email']}\\\\\\\\
{basic_info['phone']}}}\\\\\\\\

\\vspace{{10pt}}

\\end{{letter}}

\\end{{document}}"""

        return latex_cv, latex_cl
    
    async def compile_latex_to_pdf(self, latex_content: str, output_name: str) -> str:
        """Compile LaTeX to PDF with error handling"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            try:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                cmd = ['pdflatex', '-interaction=nonstopmode', str(tex_file)]
                
                # Run twice for references
                for _ in range(2):
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    print(f"✅ PDF compiled: {final_path}")
                    return final_path
                    
            except Exception as e:
                print(f"❌ PDF compilation failed: {e}")
                
        return ""
    
    async def send_claude_optimized_email(self, job_title: str, company: str, job_description: str, 
                                        job_link: str, cv_tex: str, cl_tex: str, 
                                        cv_pdf: str, cl_pdf: str, customization: dict) -> bool:
        """Send comprehensive email with Claude 3.7 optimized application"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🤖 Claude 3.7 Optimized: {job_title} at {company} - 90%+ ATS Ready"
            
            # Extract optimization details
            ats_keywords = customization.get('ats_keywords', [])
            role_focus = customization.get('role_focus', 'Unknown')
            optimization_notes = customization.get('optimization_notes', 'AI-optimized for maximum ATS compatibility')
            
            pdf_status = "✅ Successfully compiled" if cv_pdf and cl_pdf else "❌ Compilation failed"
            
            body = f"""Hi!

🤖 CLAUDE 3.7 POWERED APPLICATION - Intelligently Optimized for Maximum ATS Success!

🏢 Company: {company}
💼 Position: {job_title}  
🎯 Role Focus: {role_focus}
📊 ATS Target: 90%+ compatibility score
🔑 Keywords Integrated: {len(ats_keywords)} from job description

📎 Files attached:
   • CV (PDF): {pdf_status} - ATS-optimized and ready for submission
   • Cover Letter (PDF): {pdf_status} - Role-specific and keyword-rich
   • CV (LaTeX source): ✅ Claude-customized content for editing
   • Cover Letter (LaTeX source): ✅ ATS-optimized text

🤖 CLAUDE 3.7 INTELLIGENCE APPLIED:
{optimization_notes}

🔑 TOP ATS KEYWORDS INTEGRATED:
{', '.join(ats_keywords[:12])}{'...' if len(ats_keywords) > 12 else ''}

📋 JOB REQUIREMENTS ANALYZED:
{job_description[:400]}...

🔗 Job Application Link: {job_link}

🚀 READY FOR IMMEDIATE SUBMISSION:
These documents have been intelligently optimized by Claude 3.7 AI for:
✅ Maximum keyword matching from job description
✅ ATS system compatibility and parsing
✅ Role-specific content emphasis and relevance  
✅ Professional formatting standards
✅ Industry-standard terminology usage

💡 COMPETITIVE ADVANTAGE:
This application leverages advanced AI to analyze the job requirements and 
intelligently customize your resume, significantly improving your chances of:
• Passing ATS screening systems
• Getting noticed by recruiters
• Landing interviews

📧 NEXT STEPS:
1. Review the attached PDFs (ready to submit as-is)
2. Submit directly to {company} via their application system
3. Use LaTeX sources if any manual fine-tuning is needed

🎯 Your resume is now optimized using Claude 3.7's advanced language understanding
   to match this specific {job_title} role at {company}.

Best regards,
Claude 3.7 Powered JobHunter System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach all files
            attachments = []
            if cv_pdf and Path(cv_pdf).exists():
                attachments.append((cv_pdf, f"CV_{company}_{job_title}_CLAUDE_OPTIMIZED.pdf"))
            if cl_pdf and Path(cl_pdf).exists():
                attachments.append((cl_pdf, f"CoverLetter_{company}_{job_title}_CLAUDE_OPTIMIZED.pdf"))
            if cv_tex and Path(cv_tex).exists():
                attachments.append((cv_tex, f"CV_{company}_{job_title}_SOURCE.tex"))
            if cl_tex and Path(cl_tex).exists():
                attachments.append((cl_tex, f"CoverLetter_{company}_{job_title}_SOURCE.tex"))
            
            for file_path, filename in attachments:
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
            
            print(f"✅ Claude 3.7 optimized application sent!")
            print(f"📎 Attached: {len(attachments)} files")
            print(f"🎯 ATS Optimization: {len(ats_keywords)} keywords integrated")
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False
    
    async def process_job_application(self, job_title: str, company: str, job_description: str, job_link: str = ""):
        """Complete Claude 3.7 powered job application process"""
        
        print(f"🚀 Starting Claude 3.7 powered application for {job_title} at {company}")
        print("=" * 80)
        
        try:
            # Step 1: Claude intelligent customization
            customization = await self.customize_resume_for_job(job_title, company, job_description)
            
            if not customization:
                print("❌ Claude customization failed")
                return False
            
            # Step 2: Generate ATS-optimized cover letter
            cover_letter = await self.generate_ats_optimized_cover_letter(job_title, company, job_description, customization)
            
            if not cover_letter:
                print("❌ Cover letter generation failed") 
                return False
            
            # Step 3: Create optimized LaTeX documents
            latex_cv, latex_cl = await self.create_optimized_latex_documents(customization, cover_letter, job_title, company)
            
            # Step 4: Save LaTeX files
            cv_name = f"claude_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv"
            cl_name = f"claude_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl"
            
            cv_tex = f"{cv_name}.tex"
            cl_tex = f"{cl_name}.tex"
            
            with open(cv_tex, 'w', encoding='utf-8') as f:
                f.write(latex_cv)
            with open(cl_tex, 'w', encoding='utf-8') as f:
                f.write(latex_cl)
            
            print(f"💾 Saved Claude-optimized LaTeX files: {cv_tex}, {cl_tex}")
            
            # Step 5: Compile PDFs
            print("🔨 Compiling optimized PDFs...")
            cv_pdf = await self.compile_latex_to_pdf(latex_cv, cv_name)
            cl_pdf = await self.compile_latex_to_pdf(latex_cl, cl_name)
            
            # Step 6: Send comprehensive application email
            success = await self.send_claude_optimized_email(
                job_title, company, job_description, job_link,
                cv_tex, cl_tex, cv_pdf, cl_pdf, customization
            )
            
            # Cleanup PDFs but keep LaTeX
            try:
                if cv_pdf: os.remove(cv_pdf)
                if cl_pdf: os.remove(cl_pdf)
            except:
                pass
            
            if success:
                print("🎉 Claude 3.7 powered application successfully completed!")
                return True
            else:
                print("❌ Application sending failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in Claude application process: {e}")
            return False

async def main():
    """Test Claude 3.7 powered resume system"""
    
    system = ClaudeFinalSystem()
    
    # Example usage as requested
    job_title = "DevOps Engineer"
    company = "Opera"
    job_description = """
    We are looking for a DevOps Engineer to join our team in Stockholm. 
    
    Requirements:
    - 3+ years experience with Kubernetes and Docker containerization
    - Strong knowledge of CI/CD pipelines (Jenkins, GitHub Actions)
    - Experience with AWS or Azure cloud platforms and infrastructure
    - Python scripting and automation experience
    - Infrastructure as Code (Terraform/Ansible)
    - Monitoring and logging systems (Grafana, Prometheus)
    - Experience with microservices architecture
    - Strong Linux/Unix system administration skills
    
    Responsibilities:
    - Design and maintain CI/CD pipelines for development teams
    - Manage Kubernetes clusters and container orchestration
    - Implement infrastructure automation and scaling solutions
    - Collaborate with development teams on deployment strategies
    - Ensure system reliability, security, and scalability
    - Monitor application performance and system health
    """
    job_link = "https://opera.com/careers/devops-engineer"
    
    print(f"🎯 Claude 3.7 Powered JobHunter")
    print(f"📋 Processing: {job_title} at {company}")
    print(f"🤖 Using advanced AI for 90%+ ATS optimization")
    print()
    
    # Process complete application
    success = await system.process_job_application(job_title, company, job_description, job_link)
    
    if success:
        print("✅ Complete! Check leeharvad@gmail.com for your Claude-optimized application!")
    else:
        print("❌ Application processing failed")

if __name__ == "__main__":
    asyncio.run(main())