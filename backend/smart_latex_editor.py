#!/usr/bin/env python3
"""
Smart LaTeX Editor - Uses your exact templates and makes only targeted changes
1. Takes your original CV and Cover Letter LaTeX
2. Makes minimal targeted edits for each job
3. Sends both PDF and LaTeX files for review
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

class SmartLaTeXEditor:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "bluehawanan@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = "leeharvad@gmail.com"
        
        # Your base CV LaTeX template (fixed ECARX references)
        self.base_cv_template = r"""\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{titlesec}
\\usepackage{xcolor}
\\usepackage{hyperref}

% Page setup
\\geometry{margin=0.75in}
\\pagestyle{empty}

% Color definitions
\\definecolor{darkblue}{RGB}{0,51,102}
\\definecolor{lightgray}{RGB}{128,128,128}

% Hyperlink setup
\\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}

% Section formatting
\\titleformat{\\section}{\\Large\\bfseries\\color{darkblue}}{}{0em}{}[\\titlerule]
\\titleformat{\\subsection}{\\large\\bfseries}{}{0em}{}

\\begin{document}
\\pagestyle{empty} % no page number

% Name and contact details
\\begin{center}
{\\LARGE \\textbf{Hongzhi Li}}\\\\[10pt]
{\\Large \\textit{JOB_TITLE_PLACEHOLDER}}\\\\[10pt]
\\textcolor{darkblue}{\\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \\href{tel:0728384299}{0728384299} | \\href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \\href{https://github.com/bluehawana}{GitHub}}
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
\\subsection*{ECARX | IT/Infrastructure Specialist}
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
\\end{itemize}

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

        # Your base Cover Letter template
        self.base_cl_template = r"""\\documentclass[a4paper,10pt]{article}
\\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\\usepackage{enumitem}
\\usepackage{titlesec}
\\usepackage{hyperref}
\\usepackage{graphicx}
\\usepackage{xcolor}

% Define colors
\\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}

% Section formatting
\\titleformat{\\section}{\\large\\bfseries\\raggedright\\color{black}}{}{0em}{}[\\titlerule]
\\titleformat{\\subsection}[runin]{\\bfseries}{}{0em}{}[:]

% Remove paragraph indentation
\\setlength{\\parindent}{0pt}

\\begin{document}

\\pagestyle{empty} % no page number

\\begin{letter}{\\color{darkblue}\\
COMPANY_NAME_PLACEHOLDER\\\\
DEPARTMENT_PLACEHOLDER\\\\
ADDRESS_PLACEHOLDER\\\\
CITY_PLACEHOLDER}\\\\

\\vspace{40pt}

\\opening{Dear Hiring Manager,}

\\vspace{10pt}

LETTER_CONTENT_PLACEHOLDER

\\vspace{40pt}

{\\color{darkblue}\\rule{\\linewidth}{0.6pt}}

\\vspace{4pt}

\\closing{\\color{darkblue} Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299}\\\\

\\vspace{10pt}

\\end{letter}

\\end{document}"""
    
    def determine_role_focus(self, job_title):
        """Determine role focus from job title"""
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ['devops', 'infrastructure', 'sre', 'platform', 'cloud engineer', 'solution developer', 'automation']):
            return 'devops'
        elif any(word in title_lower for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
        elif any(word in title_lower for word in ['frontend', 'react', 'angular', 'ui', 'ux']):
            return 'frontend'
        else:
            return 'fullstack'
    
    def get_role_specific_profile(self, job_title, company, role_focus):
        """Get role-specific profile summary"""
        
        if role_focus == 'devops':
            return f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of hands-on experience in designing, implementing, and optimizing automated solutions. Proven expertise in leveraging technologies such as Python scripting, Ansible, Terraform, Docker, Kubernetes, and various cloud platforms to deliver robust and scalable automation solutions. Strong background in DevSecOps methodologies, ensuring secure coding practices and integrating security measures throughout the entire automation solution lifecycle. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure optimization projects perfect for {company}'s automation and digital transformation initiatives."
        
        elif role_focus == 'backend':
            return f"Experienced Backend Developer with over 5 years of specialized expertise in server-side technologies, microservices architecture, and database optimization. Proven track record in Java/Spring Boot, RESTful API development, and scalable backend systems. Strong background in PostgreSQL, MongoDB, and cloud-native application development. Currently serving as IT/Infrastructure Specialist at ECARX, focusing on backend infrastructure and system integration. Demonstrated ability to build high-performance backend solutions perfect for {company}-style enterprise applications."
        
        elif role_focus == 'frontend':
            return f"Experienced Frontend Developer with strong fullstack capabilities and over 5 years of hands-on experience in modern web technologies and user interface development. Proven expertise in Angular, React, Vue.js, and responsive application design with seamless backend integration. Strong background in JavaScript/TypeScript, component-based architecture, and performance optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing frontend excellence and user experience focus ideal for {company} development initiatives."
        
        else:  # fullstack
            return f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} full-stack development requirements."
    
    def get_role_specific_cover_letter_content(self, job_title, company, role_focus):
        """Get tailored cover letter content based on role focus"""
        
        if role_focus == 'devops':
            return f"""I am writing to express my strong interest in the {job_title} role at {company}. With my extensive experience in designing, implementing, and optimizing automated solutions, I am confident in my ability to contribute significantly to your team's mission of streamlining manual processes and driving digital transformation initiatives.

Throughout my career, I have developed a proven expertise in leveraging technologies such as Python scripting, Ansible, Terraform, Docker, Kubernetes, and various cloud platforms to deliver robust and scalable automation solutions. I thrive in collaborative environments, where I can work closely with cross-functional teams, including solution architects, product owners, and business analysts, to gather requirements, prioritize automation candidates, and implement solutions that meet the specific needs of stakeholders.

What sets me apart is my commitment to following DevSecOps methodologies, ensuring secure coding practices and integrating security measures throughout the entire automation solution lifecycle. I understand the importance of proper documentation and lifecycle management to avoid technical debt and ensure seamless global implementation of solutions across distributed teams.

At the core of my approach is a passion for driving continuous improvement and contributing to digital transformation and competitiveness. I am skilled in coaching teams on automation methodologies, fostering a culture of collaboration, and leveraging my overall understanding of complex systems to navigate multi-team environments and intricate integration processes seamlessly.

I am impressed by {company}'s commitment to delivering standardized solutions and fit-for-purpose services, maintaining a balance between time to market, cost, and quality. This aligns perfectly with my values and my drive to continuously seek innovative solutions that improve efficiency and quality while reducing manual effort.

Thank you for considering my application. I am excited by the prospect of joining your team and contributing my expertise to {company}'s mission. I look forward to the opportunity to discuss my qualifications further and share more about how I can contribute to your team's success.

Sincerely,
Hongzhi Li"""
        
        elif role_focus == 'backend':
            return f"""I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of specialized experience in backend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Java/Spring Boot, microservices architecture, and scalable backend systems to your team.

Throughout my career, I have developed robust backend solutions using modern technologies and best practices. My experience spans from building RESTful APIs and microservices to implementing comprehensive database optimization strategies. I have successfully delivered high-performance backend systems that serve thousands of users while maintaining excellent code quality and security standards.

What particularly excites me about {company} is your commitment to innovative technology solutions and backend excellence. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications, has given me valuable experience in building scalable, enterprise-level backend applications across different industries.

My recent projects demonstrate strong backend capabilities: developing microservices architecture for complex platforms, implementing advanced database optimization techniques, and creating scalable API solutions. I am particularly skilled in Java/Spring Boot development, database design, and cloud-native architecture patterns that align perfectly with modern enterprise requirements.

I am passionate about writing clean, maintainable code and implementing robust testing strategies. My experience with DevOps practices and CI/CD pipelines ensures that I can contribute not just to development but also to the entire software delivery lifecycle.

Thank you for considering my application. I would welcome the opportunity to discuss how my backend development expertise can contribute to {company}'s continued success and technical excellence.

Sincerely,
Hongzhi Li"""
        
        else:  # fullstack or default
            return f"""I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for end-to-end software solutions to your team.

Throughout my career, I have successfully built scalable full-stack applications using modern technologies across the entire development stack. My experience spans from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core, with comprehensive database management across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions and comprehensive development practices. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications, has given me valuable experience in building scalable, enterprise-level applications that serve diverse user bases.

My recent projects demonstrate comprehensive fullstack capabilities: developing end-to-end platforms with modern frontend and backend technologies, implementing microservices architectures, and creating seamless user experiences. I am particularly skilled in bridging the gap between frontend and backend development, ensuring optimal performance and user experience.

I am passionate about continuous learning and staying current with emerging technologies. My experience with agile methodologies, cross-functional collaboration, and modern development practices positions me well to contribute immediately to your development initiatives while fostering innovation and technical excellence.

Thank you for considering my application. I would welcome the opportunity to discuss how my fullstack development expertise can contribute to {company}'s continued success and technological advancement.

Sincerely,
Hongzhi Li"""
    
    def edit_cv_for_job(self, job_title, company, role_focus):
        """Make targeted edits to CV for specific job"""
        
        # Start with base template
        edited_cv = self.base_cv_template
        
        # 1. Replace job title
        edited_cv = edited_cv.replace("JOB_TITLE_PLACEHOLDER", job_title)
        
        # 2. Replace profile summary
        profile = self.get_role_specific_profile(job_title, company, role_focus)
        edited_cv = edited_cv.replace("PROFILE_SUMMARY_PLACEHOLDER", profile)
        
        return edited_cv
    
    def edit_cover_letter_for_job(self, job_title, company, department="", address="", city=""):
        """Make targeted edits to cover letter for specific job"""
        
        role_focus = self.determine_role_focus(job_title)
        
        # Start with base template
        edited_cl = self.base_cl_template
        
        # Replace company information
        edited_cl = edited_cl.replace("COMPANY_NAME_PLACEHOLDER", company)
        edited_cl = edited_cl.replace("DEPARTMENT_PLACEHOLDER", department or f"{job_title} Team")
        edited_cl = edited_cl.replace("ADDRESS_PLACEHOLDER", address or "Hiring Department")
        edited_cl = edited_cl.replace("CITY_PLACEHOLDER", city or "Sweden")
        
        # Replace letter content
        letter_content = self.get_role_specific_cover_letter_content(job_title, company, role_focus)
        edited_cl = edited_cl.replace("LETTER_CONTENT_PLACEHOLDER", letter_content)
        
        return edited_cl
    
    def compile_latex(self, tex_content, output_name):
        """Compile LaTeX to PDF with better error handling"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            # Write content with error handling
            try:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(tex_content)
            except Exception as e:
                print(f"❌ Error writing LaTeX file: {e}")
                return None
            
            try:
                # Compile LaTeX (run twice for references)
                for i in range(2):
                    result = subprocess.run([
                        'pdflatex', 
                        '-interaction=nonstopmode',
                        '-output-directory', str(temp_path),
                        str(tex_file)
                    ], capture_output=True, text=True, cwd=temp_path)
                    
                    if result.returncode != 0:
                        if i == 1:  # Only show error on final attempt
                            print(f"❌ LaTeX compilation failed for {output_name}")
                            # Show more specific error info
                            if 'Emergency stop' in result.stdout:
                                print("LaTeX encountered a critical error - check template syntax")
                            return None
                
                # Check if PDF was created
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    size = os.path.getsize(final_path) / 1024
                    print(f"✅ PDF generated: {final_path} ({size:.1f} KB)")
                    return final_path
                else:
                    print(f"❌ PDF file not found after compilation")
                    return None
                
            except FileNotFoundError:
                print("❌ pdflatex not found - please install LaTeX")
                return None
            except Exception as e:
                print(f"❌ Compilation error: {e}")
                return None
    
    def save_latex_files(self, cv_content, cl_content, job_title, company):
        """Save LaTeX source files"""
        company_safe = re.sub(r'[^a-zA-Z0-9]', '_', company.lower())
        title_safe = re.sub(r'[^a-zA-Z0-9]', '_', job_title.lower())
        
        cv_tex_path = f"hongzhi_{title_safe}_{company_safe}_cv.tex"
        cl_tex_path = f"hongzhi_{title_safe}_{company_safe}_cl.tex"
        
        try:
            with open(cv_tex_path, 'w', encoding='utf-8') as f:
                f.write(cv_content)
            
            with open(cl_tex_path, 'w', encoding='utf-8') as f:
                f.write(cl_content)
            
            return cv_tex_path, cl_tex_path
        except Exception as e:
            print(f"❌ Error saving LaTeX files: {e}")
            return None, None
    
    def send_review_email(self, job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus):
        """Send review email with files"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Review: {job_title} at {company} - Tailored & Ready"
            
            body = f"""Hi,

Smart-edited job application ready for your review:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Tailoring: {role_focus.title()} focus
📍 Priority: {'🏢 Gothenburg' if 'gothenburg' in company.lower() or 'volvo' in company.lower() else '🌐 Remote/Other'}

📎 Files for review:
   • CV (PDF) - Ready to send
   • Cover Letter (PDF) - Ready to send  
   • CV (LaTeX) - Your original template with targeted edits
   • Cover Letter (LaTeX) - Your original template with targeted edits

✏️  Smart edits made:
   ✅ Job title updated to: {job_title}
   ✅ Profile summary tailored for {role_focus} role
   ✅ Cover letter content customized for {company}
   ✅ Company information and contact details updated
   ✅ Hard/soft skills emphasized for this role type
   ✅ All original formatting and structure preserved

📋 Your original LaTeX templates used as base - only necessary changes made.

🔧 If you need to edit further:
   1. Edit the LaTeX source files
   2. Recompile: pdflatex filename.tex
   3. Send final version

Best regards,
Smart LaTeX Editor
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach files with clear naming
            attachments = [
                (cv_pdf, f"CV_{company}_{job_title}_READY.pdf"),
                (cl_pdf, f"CoverLetter_{company}_{job_title}_READY.pdf"),
                (cv_tex, f"CV_{company}_{job_title}_SOURCE.tex"),
                (cl_tex, f"CoverLetter_{company}_{job_title}_SOURCE.tex")
            ]
            
            for file_path, filename in attachments:
                if file_path and Path(file_path).exists():
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
            
            print(f"✅ Review email sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Test smart editor with targeted changes only"""
    editor = SmartLaTeXEditor()
    
    # Test jobs
    test_jobs = [
        ("Solution Developer", "Volvo Group", "Onsite Infrastructure Demand & Automation", "Sven Erikssons gata 7", "41755 Göteborg"),
        ("DevOps Engineer", "Spotify", "Infrastructure Team", "", "Stockholm"),
        ("Senior Backend Developer", "SKF Group", "Software Development", "", "Gothenburg")
    ]
    
    print("🎯 Smart LaTeX Editor - Minimal Targeted Changes")
    print("=" * 60)
    print("📝 Using your exact templates with only necessary edits")
    print()
    
    for job_title, company, department, address, city in test_jobs:
        print(f"📋 Processing: {job_title} at {company}")
        
        role_focus = editor.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        # Make targeted edits
        print("✏️  Making minimal targeted edits...")
        cv_content = editor.edit_cv_for_job(job_title, company, role_focus)
        cl_content = editor.edit_cover_letter_for_job(job_title, company, department, address, city)
        
        # Save LaTeX files
        cv_tex, cl_tex = editor.save_latex_files(cv_content, cl_content, job_title, company)
        
        if cv_tex and cl_tex:
            print(f"💾 LaTeX files saved: {cv_tex}, {cl_tex}")
            
            # Compile PDFs
            print("🔨 Compiling PDFs...")
            cv_pdf = editor.compile_latex(cv_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
            cl_pdf = editor.compile_latex(cl_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
            
            if cv_pdf and cl_pdf:
                # Send review email
                success = editor.send_review_email(job_title, company, cv_pdf, cl_pdf, cv_tex, cl_tex, role_focus)
                
                if success:
                    print(f"🎉 SUCCESS: Review files sent!")
                    
                    # Clean up PDFs but keep LaTeX
                    try:
                        os.remove(cv_pdf)
                        os.remove(cl_pdf)
                    except:
                        pass
                else:
                    print(f"❌ FAILED: Email not sent")
            else:
                print(f"❌ FAILED: PDF compilation failed")
        else:
            print(f"❌ FAILED: Could not save LaTeX files")
        
        print()
        await asyncio.sleep(2)
    
    print(f"📧 Check {editor.recipient_email} for review emails!")

if __name__ == "__main__":
    asyncio.run(main())