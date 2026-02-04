#!/usr/bin/env python3
"""
Smart LaTeX Editor for Job Applications
Takes your existing LaTeX template and makes targeted edits for each job:
1. Updates job title
2. Tailors profile summary for role focus
3. Reorders/emphasizes relevant skills
4. Highlights relevant experience points
5. Fixes ECARX project references
6. Sends both PDF and LaTeX for review
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
import smtplib
import re
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class LaTeXJobEditor:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "bluehawanan@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = "leeharvad@gmail.com"
        
        # Your base LaTeX template (with ECARX references fixed)
        self.base_latex_template = r"""\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{titlesec}
\\usepackage{xcolor}
\\usepackage{hyperref}
\\usepackage{fontawesome}

% Page setup
\\geometry{margin=0.75in}
\\pagestyle{empty}

% Color definitions
\\definecolor{linkedinblue}{RGB}{0,119,181}
\\definecolor{lightgray}{RGB}{128,128,128}

% Hyperlink setup
\\hypersetup{
    colorlinks=true,
    linkcolor=linkedinblue,
    urlcolor=linkedinblue,
    citecolor=linkedinblue
}

% Section formatting
\\titleformat{\\section}{\\Large\\bfseries\\color{linkedinblue}}{}{0em}{}[\\titlerule]
\\titleformat{\\subsection}{\\large\\bfseries}{}{0em}{}

% Custom commands
\\newcommand{\\contactitem}[2]{\\textcolor{linkedinblue}{#1} #2}

\\begin{document}
\\pagestyle{empty} % no page number

% Name and contact details
\\begin{center}
{\\LARGE \\textbf{Hongzhi Li}}\\\\[10pt]
{\\Large \\textit{JOB_TITLE_PLACEHOLDER}}\\\\[10pt]
\\textcolor{linkedinblue}{\\href{mailto:hongzhili01@google.com}{hongzhili01@gmail.com} | \\href{tel:0728384299}{0728384299} | \\href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \\href{https://github.com/bluehawana}{GitHub}}
\\end{center}

% Personal Profile
\\section*{Profile Summary}
PROFILE_SUMMARY_PLACEHOLDER

% Areas of Expertise
\\section*{Core Technical Skills}
\\begin{itemize}[noitemsep]
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
\\end{itemize}

% Experience
EXPERIENCE_SECTION_PLACEHOLDER

\\section*{Hobby Projects}

\\subsection{Gothenburg TaxiCarPooling Web Application}
\\textit{May 2025 - Present}
\\begin{itemize}
\\item Developing intelligent carpooling platform using Spring Boot backend and Node.js microservices
\\item Cross-platform mobile application with React Native, integrating payment and geolocation services
\\item Implemented automated order matching algorithm and RESTful APIs for real-time data processing
\\item Designed system with PostgreSQL database integration and optimized for scalability and performance
\\item Built comprehensive automated testing suite and ensured data protection compliance
\\end{itemize}

\\subsection{SmartTV \\& VoiceBot - Android Auto Applications}
\\textit{March 2025 - Present}
\\begin{itemize}
\\item Developing Android Auto apps with Java backend services and modern frontend interfaces
\\item Implemented RESTful APIs for real-time data processing and voice command integration
\\item Built secure API integrations with SQL database optimization for vehicle data access
\\item Developed comprehensive testing framework for both frontend and backend components
\\end{itemize}

\\subsection{Hong Yan AB - E-commerce Platform (smrtmart.com)}
\\textit{April 2024 - Present}
\\begin{itemize}
\\item Fullstack e-commerce platform with Spring Boot backend and React frontend
\\item Implemented microservices architecture with PostgreSQL and MongoDB database integration
\\item Built comprehensive order management, inventory tracking, and payment processing systems
\\item Developed RESTful APIs for frontend-backend communication and third-party integrations
\\item Optimized application performance for maximum speed and scalability
\\end{itemize}

\\vspace{6pt}
\\section*{Education}
\\textbf{IT Högskolan}\\\\
\\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\\\
\\textbf{Mölndal Campus}\\\\
\\textit{Bachelor's Degree in Java Integration} | 2019-2021\\\\
\\textbf{University of Gothenburg}\\\\
\\textit{Master's Degree in International Business and Trade} | 2016-2019\\\\

\\vspace{6pt}
\\section*{Certifications}
\\begin{itemize}
\\item AWS Certified Solutions Architect - Associate (Aug 2022)
\\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\\item AWS Certified Developer - Associate (Nov 2022)
\\end{itemize}

\\vspace{6pt}
\\section*{Additional Information}
\\begin{itemize}
\\item \\textbf{Languages:} Fluent in English and Mandarin
\\item \\textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology
\\item \\textbf{Personal Website:} \\href{https://www.bluehawana.com}{bluehawana.com}
\\item \\textbf{Customer Websites:} \\href{https://www.senior798.eu}{senior798.eu}, \\href{https://www.mibo.se}{mibo.se}, \\href{https://www.omstallningsstod.se}{omstallningsstod.se}
\\end{itemize}

\\end{document}"""
    
    def determine_role_focus(self, job_title):
        """Determine role focus from job title"""
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ['devops', 'infrastructure', 'sre', 'platform', 'cloud engineer']):
            return 'devops'
        elif any(word in title_lower for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
        elif any(word in title_lower for word in ['frontend', 'react', 'angular', 'ui', 'ux']):
            return 'frontend'
        else:
            return 'fullstack'
    
    def get_tailored_profile_summary(self, job_title, company, role_focus):
        """Get role-specific profile summary"""
        
        profile_summaries = {
            'devops': f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of hands-on experience in cloud platforms, containerization, and CI/CD automation. Proven expertise in Kubernetes, Docker, AWS/Azure, and infrastructure optimization. Strong background in system reliability, monitoring solutions, and cost optimization strategies. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure projects and implementing modern DevOps practices. Demonstrated ability to reduce operational expenses and improve system reliability for {company}-type technology solutions.",
            
            'backend': f"Experienced Backend Developer with over 5 years of specialized expertise in server-side technologies, microservices architecture, and database optimization. Proven track record in Java/Spring Boot, RESTful API development, and scalable backend systems. Strong background in PostgreSQL, MongoDB, and cloud-native application development. Currently serving as IT/Infrastructure Specialist at ECARX, focusing on backend infrastructure and system integration. Demonstrated ability to build high-performance backend solutions perfect for {company}-style enterprise applications.",
            
            'frontend': f"Experienced Frontend Developer with strong fullstack capabilities and over 5 years of hands-on experience in modern web technologies and user interface development. Proven expertise in Angular, React, Vue.js, and responsive application design with seamless backend integration. Strong background in JavaScript/TypeScript, component-based architecture, and performance optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing frontend excellence and user experience focus ideal for {company} development initiatives.",
            
            'fullstack': f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} full-stack development requirements."
        }
        
        return profile_summaries.get(role_focus, profile_summaries['fullstack'])
    
    def get_role_tailored_experience(self, role_focus):
        """Get experience section tailored to role focus"""
        
        if role_focus == 'devops':
            return """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\\item Managing complex network systems and providing technical solution design for enterprise-level applications
\\item Providing infrastructure automation and DevOps support to development teams for enhanced productivity
\\end{itemize}

\\subsection*{Synteda | Azure DevOps Engineer \\& Integration Specialist (Freelance)}
\\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Developed cloud-native talent management system with comprehensive Azure infrastructure automation
\\item Built complete office management platform with focus on deployment automation and CI/CD pipelines
\\item Implemented containerized microservices architecture with Docker and Kubernetes deployment strategies
\\item Integrated monitoring, logging, and alerting systems for production environment reliability
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
        
        elif role_focus == 'backend':
            return """\\subsection*{ECARX | IT/Infrastructure Specialist}
\\textit{October 2024 - Present | Gothenburg, Sweden}
\\begin{itemize}[noitemsep]
\\item Leading backend system optimization and integration projects for automotive technology solutions
\\item Providing IT support and infrastructure support to development teams for enhanced productivity
\\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\\item Managing complex network systems and providing technical solution design for enterprise-level applications
\\item Developing scalable microservices architecture and API design for high-performance systems
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
        
        else:  # fullstack or default - use original experience
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
    
    def edit_latex_for_job(self, job_title, company, role_focus):
        """Edit the base LaTeX template for specific job"""
        
        # Start with base template
        edited_latex = self.base_latex_template
        
        # 1. Replace job title
        edited_latex = edited_latex.replace("JOB_TITLE_PLACEHOLDER", job_title)
        
        # 2. Replace profile summary
        profile_summary = self.get_tailored_profile_summary(job_title, company, role_focus)
        edited_latex = edited_latex.replace("PROFILE_SUMMARY_PLACEHOLDER", profile_summary)
        
        # 3. Replace experience section
        experience_section = self.get_role_tailored_experience(role_focus)
        edited_latex = edited_latex.replace("EXPERIENCE_SECTION_PLACEHOLDER", experience_section)
        
        return edited_latex
    
    def create_tailored_cover_letter(self, job_title, company, role_focus):
        """Create tailored cover letter"""
        
        # Role-specific intro paragraphs
        intro_paragraphs = {
            'devops': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in DevOps engineering and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in infrastructure automation, cloud platforms, and cost optimization strategies to your team.",
            
            'backend': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of specialized experience in backend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Java/Spring Boot, microservices architecture, and scalable backend systems to your team.",
            
            'frontend': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in frontend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Angular, React, and modern web technologies to your team.",
            
            'fullstack': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for end-to-end software solutions to your team."
        }
        
        intro = intro_paragraphs.get(role_focus, intro_paragraphs['fullstack'])
        
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

In my current position, I have been leading infrastructure optimization projects and implementing cost-effective solutions, including migrating from Azure Kubernetes Service to local Kubernetes clusters. My experience spans the entire technology stack, and I have successfully built microservices architectures, implemented RESTful APIs, and managed complex database integrations across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications at Synteda, has given me valuable experience in building scalable, enterprise-level applications.

My recent hobby projects demonstrate my passion for {role_focus} development: developing the Gothenburg TaxiCarPooling platform with Spring Boot and React Native, building SmartTV applications for Android Auto, and creating a comprehensive e-commerce platform. These projects showcase my ability to work with modern technologies and deliver end-to-end solutions.

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals, along with my practical project experience, position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience in {role_focus} development can contribute to {company}'s continued success. Thank you for considering my application.

\\vspace{{20pt}}

Best regards,

Hongzhi Li

\\end{{document}}"""
        
        return cl_template
    
    def compile_latex(self, tex_content, output_name):
        """Compile LaTeX to PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            try:
                # Run twice for proper references
                for i in range(2):
                    result = subprocess.run([
                        'pdflatex', 
                        '-interaction=nonstopmode',
                        '-output-directory', str(temp_path),
                        str(tex_file)
                    ], capture_output=True, text=True, cwd=temp_path)
                    
                    if result.returncode != 0 and i == 1:
                        print(f"❌ LaTeX compilation failed for {output_name}")
                        print("Error output:", result.stdout[-300:])
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
    
    def send_review_email(self, job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus):
        """Send email with both PDF and LaTeX files for review"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Review: {job_title} at {company} - Tailored for {role_focus.title()}"
            
            body = f"""Hi,

Job application tailored and ready for your review:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Role Focus: {role_focus.title()}
📍 Priority: {'🏢 Gothenburg' if 'gothenburg' in company.lower() else '🌐 Remote/Other'}

📎 Files attached for review:
   • CV (PDF) - Compiled and ready
   • Cover Letter (PDF) - Compiled and ready  
   • CV (LaTeX source) - For your editing/polishing
   • Cover Letter (LaTeX source) - For your editing/polishing

🎯 Tailoring applied for {role_focus.title()} role:
   ✅ Job title updated to: {job_title}
   ✅ Profile summary customized for {role_focus} focus
   ✅ Experience section emphasizes {role_focus} achievements
   ✅ Cover letter highlights {role_focus} expertise
   ✅ ECARX project references cleaned up
   ✅ 3-page format maintained with all hobby projects

📝 Review Process:
   1. Check PDF files for content and formatting
   2. Edit LaTeX source files for final polish if needed
   3. Recompile if you make changes: pdflatex filename.tex
   4. Send final application or approve automation

🔧 Technical Details:
   • Based on your original LaTeX template
   • Dark blue (LinkedIn) colors maintained
   • All formatting and structure preserved
   • Only targeted edits for job-specific content

Best regards,
JobHunter Smart Editor
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach all files
            attachments = [
                (cv_pdf, f"CV_{company}_{job_title}_tailored.pdf"),
                (cl_pdf, f"CoverLetter_{company}_{job_title}_tailored.pdf"),
                (cv_tex, f"CV_{company}_{job_title}_source.tex"),
                (cl_tex, f"CoverLetter_{company}_{job_title}_source.tex")
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
            
            print(f"✅ Review email sent for {job_title} at {company}")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Test LaTeX editor system"""
    editor = LaTeXJobEditor()
    
    # Test jobs with different role focus
    test_jobs = [
        ("DevOps Engineer", "Volvo Cars"),
        ("Senior Backend Developer", "Spotify"),
        ("Fullstack Developer", "SKF Group")
    ]
    
    print("🎯 Smart LaTeX Editor - Targeted Job Tailoring")
    print("=" * 60)
    print("📝 Using your existing LaTeX template with targeted edits")
    print()
    
    for job_title, company in test_jobs:
        print(f"📋 Processing: {job_title} at {company}")
        
        role_focus = editor.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        # Edit LaTeX for this specific job
        print("✏️  Making targeted edits to your LaTeX template...")
        cv_content = editor.edit_latex_for_job(job_title, company, role_focus)
        cl_content = editor.create_tailored_cover_letter(job_title, company, role_focus)
        
        # Save LaTeX files
        cv_tex, cl_tex = editor.save_latex_files(cv_content, cl_content, job_title, company)
        print(f"💾 LaTeX files saved: {cv_tex}, {cl_tex}")
        
        # Compile PDFs
        print("🔨 Compiling PDFs...")
        cv_pdf = editor.compile_latex(cv_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
        cl_pdf = editor.compile_latex(cl_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
        
        if cv_pdf and cl_pdf:
            # Send review email
            success = editor.send_review_email(job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus)
            
            if success:
                print(f"🎉 SUCCESS: Review email sent with both PDF and LaTeX files")
                
                # Clean up PDF files but keep LaTeX for editing
                try:
                    os.remove(cv_pdf)
                    os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"❌ FAILED: Email not sent")
        else:
            print(f"❌ FAILED: PDF compilation failed")
        
        print()
        await asyncio.sleep(2)
    
    print(f"📧 Check {editor.recipient_email} for review emails!")
    print("📝 Each email contains both PDF (ready) and LaTeX (for editing)")

if __name__ == "__main__":
    asyncio.run(main())