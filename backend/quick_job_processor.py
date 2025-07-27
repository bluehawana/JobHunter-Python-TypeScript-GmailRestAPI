#!/usr/bin/env python3
"""
Quick and working job application processor
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

class QuickJobProcessor:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "bluehawanan@gmail.com"
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient_email = "leeharvad@gmail.com"
    
    def create_tailored_cv(self, job_title, company, role_focus):
        """Create tailored CV based on job"""
        
        # Role-specific profile summaries
        profiles = {
            'backend': f"Experienced Backend Developer with over 5 years specializing in server-side technologies and database management. Proven expertise in Java/Spring Boot, microservices architecture, and RESTful API development. Currently serving as IT/Infrastructure Specialist at ECARX, focusing on scalable backend solutions for {company}-type applications.",
            
            'devops': f"Experienced DevOps Engineer with over 5 years in infrastructure automation and cloud platforms. Proven expertise in Kubernetes, Docker, CI/CD pipelines, and monitoring solutions. Currently serving as IT/Infrastructure Specialist at ECARX, implementing cost-effective infrastructure solutions ideal for {company}-style operations.",
            
            'fullstack': f"Experienced Fullstack Developer with over 5 years in end-to-end application development. Proven expertise in Java/Spring Boot backend with Angular/React frontend integration. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical skills perfect for {company} development initiatives."
        }
        
        # Role-specific skills highlighting
        skills_sections = {
            'backend': """\\textbf{Backend Expertise:} Java/J2EE, Spring Boot, .NET Core, Microservices\\\\
\\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis, Query Optimization\\\\
\\textbf{APIs:} RESTful APIs, GraphQL, API Design, Documentation\\\\
\\textbf{Cloud:} AWS, Azure, Containerization, Scalable Architecture""",
            
            'devops': """\\textbf{DevOps Tools:} Kubernetes, Docker, Jenkins, GitHub Actions, CI/CD\\\\
\\textbf{Cloud Platforms:} AWS, Azure, Infrastructure as Code, Terraform\\\\
\\textbf{Monitoring:} Grafana, Prometheus, System Reliability, Performance\\\\
\\textbf{Programming:} Python, Bash, Java, Infrastructure Automation""",
            
            'fullstack': """\\textbf{Frontend:} Angular, React, Vue.js, TypeScript, HTML5/CSS3\\\\
\\textbf{Backend:} Java/Spring Boot, .NET Core, Node.js, Microservices\\\\
\\textbf{Database:} PostgreSQL, MySQL, MongoDB, Database Design\\\\
\\textbf{Cloud:} AWS, Azure, Docker, Kubernetes, Full-Stack Deployment"""
        }
        
        profile = profiles.get(role_focus, profiles['fullstack'])
        skills = skills_sections.get(role_focus, skills_sections['fullstack'])
        
        return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=0.75in]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

% Define dark blue color (LinkedIn blue)
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{6pt}}

\\begin{{document}}

% Header
\\begin{{center}}
{{\\huge \\textbf{{\\textcolor{{darkblue}}{{Hongzhi Li}}}}}}\\\\
\\vspace{{6pt}}
{{\\Large \\textcolor{{darkblue}}{{{job_title}}}}}\\\\
\\vspace{{10pt}}
\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} $\\bullet$ 0728384299 $\\bullet$ \\href{{https://linkedin.com/in/hongzhi-li}}{{LinkedIn}} $\\bullet$ \\href{{https://github.com/bluehawana}}{{GitHub}}
\\end{{center}}

\\vspace{{12pt}}

{{\\large\\textbf{{\\textcolor{{darkblue}}{{Profile Summary}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}\\vspace{{6pt}}
{profile}

\\vspace{{8pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Core Technical Skills}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}\\vspace{{6pt}}
{skills}

\\vspace{{8pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Professional Experience}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}\\vspace{{6pt}}

\\textbf{{ECARX --- IT/Infrastructure Specialist}} (October 2024 - Present)\\\\
\\textit{{Gothenburg, Sweden}}\\\\
$\\bullet$ Leading infrastructure optimization and system integration projects\\\\
$\\bullet$ Implementing cost optimization through Kubernetes migration\\\\
$\\bullet$ Modern monitoring solutions using Grafana and advanced scripting\\\\
$\\bullet$ Managing complex network systems for enterprise applications

\\vspace{{4pt}}
\\textbf{{Synteda --- Azure Fullstack Developer (Freelance)}} (August 2023 - September 2024)\\\\
\\textit{{Gothenburg, Sweden}}\\\\
$\\bullet$ Developed comprehensive talent management system using C\\# and .NET Core\\\\
$\\bullet$ Built complete office management platform with cloud-native architecture\\\\
$\\bullet$ Implemented RESTful APIs and microservices for scalable systems\\\\
$\\bullet$ Integrated SQL and NoSQL databases with optimized performance

\\vspace{{4pt}}
\\textbf{{IT-Högskolan --- Backend Developer (Part-time)}} (January 2023 - May 2023)\\\\
\\textit{{Gothenburg, Sweden}}\\\\
$\\bullet$ Migrated "Omstallningsstod.se" platform using Spring Boot services\\\\
$\\bullet$ Developed RESTful APIs for frontend integration and secure data handling\\\\
$\\bullet$ Collaborated with UI/UX designers for seamless integration\\\\
$\\bullet$ Implemented automated tests as part of delivery process

\\vspace{{4pt}}
\\textbf{{Senior Material (Europe) AB --- Platform Architect}} (January 2022 - December 2022)\\\\
\\textit{{Eskilstuna, Sweden}}\\\\
$\\bullet$ Led migration of business-critical applications with microservices\\\\
$\\bullet$ Developed backend services with Spring Boot and RESTful APIs\\\\
$\\bullet$ Optimized applications for maximum speed and scalability\\\\
$\\bullet$ Participated in Agile ceremonies and sprint planning

\\vspace{{8pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Key Projects}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}\\vspace{{6pt}}

\\textbf{{Gothenburg TaxiCarPooling Platform}} (May 2025 - Present)\\\\
Spring Boot backend with React Native mobile app, PostgreSQL integration

\\textbf{{SmartTV \\& VoiceBot Applications}} (March 2025 - Present)\\\\
Android Auto applications with Java backend and voice command integration

\\textbf{{E-commerce Platform (smrtmart.com)}} (April 2024 - Present)\\\\
Fullstack platform with Spring Boot, React, microservices architecture

\\vspace{{8pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Education \\& Certifications}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}\\vspace{{6pt}}

\\textbf{{IT Högskolan}} --- Bachelor's in .NET Cloud Development (2021-2023)\\\\
\\textbf{{University of Gothenburg}} --- Master's in International Business (2016-2019)\\\\
\\textbf{{Certifications:}} AWS Solutions Architect, Azure Fundamentals, AWS Developer

\\vspace{{6pt}}
\\textbf{{Languages:}} Fluent in English and Mandarin $\\bullet$ \\textbf{{Website:}} bluehawana.com

\\end{{document}}"""
    
    def create_tailored_cover_letter(self, job_title, company, role_focus):
        """Create tailored cover letter"""
        
        intros = {
            'backend': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in backend development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my expertise in Java/Spring Boot, microservices architecture, and scalable backend solutions to your team.",
            
            'devops': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in infrastructure automation and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my DevOps expertise, cloud platform knowledge, and passion for efficient deployment pipelines to your team.",
            
            'fullstack': f"I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for end-to-end software solutions to your team."
        }
        
        highlights = {
            'backend': """\\item Developing scalable backend systems using Java/Spring Boot and microservices architecture
\\item Implementing database optimization and RESTful API design for high-performance systems
\\item Leading backend system integration and performance optimization projects
\\item Working with diverse technology stacks including Java, C\\#, PostgreSQL, and cloud platforms""",
            
            'devops': """\\item Leading infrastructure optimization and implementing automated deployment pipelines
\\item Migrating from AKS to local Kubernetes clusters, reducing operational costs significantly
\\item Implementing modern monitoring solutions using Grafana and advanced scripting
\\item Managing complex network systems and providing DevOps solution design""",
            
            'fullstack': """\\item Leading infrastructure optimization and system integration projects
\\item Developing comprehensive applications from frontend to backend with modern frameworks
\\item Implementing CI/CD pipelines and automated testing frameworks
\\item Working with diverse technology stacks including Java, React, Angular, and cloud platforms"""
        }
        
        intro = intros.get(role_focus, intros['fullstack'])
        highlight_list = highlights.get(role_focus, highlights['fullstack'])
        
        return f"""\\documentclass[11pt,a4paper]{{article}}
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
    citecolor=darkblue
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
\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} --- 0728384299 --- \\href{{https://linkedin.com/in/hongzhi-li}}{{LinkedIn}} --- \\href{{https://github.com/bluehawana}}{{GitHub}}
\\end{{center}}

\\vspace{{20pt}}

\\today

{company} Hiring Team\\\\
{company}\\\\
Hiring Department

\\vspace{{20pt}}

\\textbf{{\\textcolor{{darkblue}}{{Subject: Application for {job_title} Position}}}}

Dear Hiring Manager,

{intro}

In my current position, I have been leading infrastructure optimization projects and implementing cost-effective solutions. My experience spans the entire technology stack, and I have successfully built microservices architectures, implemented RESTful APIs, and managed complex database integrations across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications, has given me valuable experience in building scalable, enterprise-level applications.

\\textbf{{\\textcolor{{darkblue}}{{Key highlights of my experience include:}}}}
\\begin{{itemize}}
{highlight_list}
\\end{{itemize}}

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience can contribute to {company}'s continued success. Thank you for considering my application.

\\vspace{{20pt}}

Best regards,

Hongzhi Li

\\end{{document}}"""
    
    def determine_role_focus(self, title):
        """Determine role focus from job title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['devops', 'infrastructure', 'sre', 'platform']):
            return 'devops'
        elif any(word in title_lower for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
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
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', str(temp_path),
                    str(tex_file)
                ], capture_output=True, text=True, cwd=temp_path)
                
                if result.returncode != 0:
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
    
    def send_email(self, job_title, company, cv_path, cl_path):
        """Send application email"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"JobHunter Application: {job_title} at {company}"
            
            body = f"""Hi,

New tailored job application from JobHunter automation:

🏢 Company: {company}
💼 Position: {job_title}
📍 Location: Gothenburg/Stockholm, Sweden

📎 Documents attached:
   • CV specifically tailored for {job_title} role
   • Cover letter customized for {company}

Both documents use dark blue (LinkedIn blue) colors and are optimized for ATS systems.

Best regards,
JobHunter Automation System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDFs
            for file_path, filename in [(cv_path, f"CV_{company}_{job_title}.pdf"), 
                                       (cl_path, f"CoverLetter_{company}_{job_title}.pdf")]:
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
            
            print(f"✅ Email sent for {job_title} at {company}")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Process multiple jobs"""
    processor = QuickJobProcessor()
    
    # Sample jobs - replace with database query
    jobs = [
        ("Senior Backend Developer", "Spotify Technology"),
        ("DevOps Engineer", "Volvo Cars"), 
        ("Fullstack Developer", "Klarna Bank")
    ]
    
    print("🚀 Starting JobHunter Workflow")
    print("=" * 50)
    
    successful = 0
    
    for i, (job_title, company) in enumerate(jobs, 1):
        print(f"\n🔄 Processing {i}/{len(jobs)}: {job_title} at {company}")
        
        role_focus = processor.determine_role_focus(job_title)
        print(f"📊 Role Focus: {role_focus}")
        
        # Generate documents
        print("📄 Generating CV...")
        cv_content = processor.create_tailored_cv(job_title, company, role_focus)
        cv_pdf = processor.compile_latex(cv_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
        
        print("📄 Generating cover letter...")
        cl_content = processor.create_tailored_cover_letter(job_title, company, role_focus)
        cl_pdf = processor.compile_latex(cl_content, f"hongzhi_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
        
        if cv_pdf and cl_pdf:
            print("📧 Sending email...")
            if processor.send_email(job_title, company, cv_pdf, cl_pdf):
                successful += 1
                print(f"🎉 SUCCESS: {job_title} at {company}")
                
                # Clean up files
                try:
                    os.remove(cv_pdf)
                    os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"❌ FAILED: Email not sent")
        else:
            print(f"❌ FAILED: PDF generation failed")
        
        # Wait between applications
        if i < len(jobs):
            print("⏳ Waiting 3 seconds...")
            await asyncio.sleep(3)
    
    print(f"\n📊 COMPLETE: {successful}/{len(jobs)} applications sent!")
    print(f"📧 Check {processor.recipient_email} for emails")

if __name__ == "__main__":
    asyncio.run(main())