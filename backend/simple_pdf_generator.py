#!/usr/bin/env python3
"""
Simple PDF Generator - Uses basic LaTeX packages for reliable compilation
Creates simplified CV and Cover Letter templates that compile successfully
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

# Import our smart editor
import sys
sys.path.append(str(Path(__file__).parent))
from smart_latex_editor import SmartLaTeXEditor

class SimplePDFGenerator(SmartLaTeXEditor):
    def __init__(self):
        super().__init__()
    
    def create_simple_cv_template(self, job_title, company, role_focus):
        """Create a simplified CV template that compiles reliably"""
        
        profile_summaries = {
            "devops": f"Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of hands-on experience in designing, implementing, and optimizing automated solutions. Proven expertise in cloud platforms, Kubernetes, Docker, and CI/CD pipelines. Currently serving as IT/Infrastructure Specialist at ECARX, leading infrastructure optimization projects perfect for {company}'s automation and digital transformation initiatives.",
            "backend": f"Experienced Backend Developer with over 5 years of hands-on experience in Java/J2EE development and modern web technologies. Proven expertise in building scalable backend services using Spring Boot, RESTful APIs, and microservices architecture. Strong background in database management across SQL and NoSQL platforms. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} backend development requirements.",
            "frontend": f"Experienced Frontend Developer with over 5 years of hands-on experience in modern web technologies and user interface development. Proven expertise in Angular, React, Vue.js, and responsive web design. Strong background in building scalable frontend applications with excellent user experience. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} frontend development requirements.",
            "fullstack": f"Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing comprehensive technical knowledge perfect for {company} full-stack development requirements."
        }
        
        return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[margin=0.75in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage[utf8]{{inputenc}}

\\begin{{document}}
\\pagestyle{{empty}}

% Header
\\begin{{center}}
{{\\LARGE \\textbf{{Hongzhi Li}}}}\\\\[10pt]
{{\\Large {job_title}}}\\\\[10pt]
hongzhili01@gmail.com | 0728384299 | LinkedIn: hzl | GitHub: bluehawana
\\end{{center}}

\\vspace{{10pt}}

% Profile Summary
\\section*{{Profile Summary}}
{profile_summaries.get(role_focus, profile_summaries["fullstack"])}

% Technical Skills
\\section*{{Core Technical Skills}}
\\begin{{itemize}}[noitemsep]
\\item Programming Languages: Java/J2EE, JavaScript, C\\#/.NET Core, Python, Bash, PowerShell
\\item Frontend Frameworks: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3
\\item Backend Frameworks: Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js
\\item API Development: RESTful APIs, GraphQL, Microservices Architecture
\\item Databases: PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB
\\item Cloud Platforms: AWS, Azure, GCP
\\item Containerization: Docker, Kubernetes, Azure Kubernetes Service (AKS)
\\item Version Control: Git, GitHub, GitLab
\\item CI/CD: Jenkins, GitHub Actions, GitLab CI
\\end{{itemize}}

% Experience
\\section*{{Professional Experience}}

\\textbf{{ECARX | IT/Infrastructure Specialist}}\\\\
October 2024 - Present | Gothenburg, Sweden
\\begin{{itemize}}[noitemsep]
\\item Leading infrastructure optimization and system integration projects
\\item Implementing cost optimization by migrating from AKS to local Kubernetes cluster
\\item Implementing modern monitoring solutions using Grafana and advanced scripting
\\item Managing complex network systems and providing technical solution design
\\end{{itemize}}

\\textbf{{Synteda | Azure Fullstack Developer (Freelance)}}\\\\
August 2023 - September 2024 | Gothenburg, Sweden
\\begin{{itemize}}[noitemsep]
\\item Developed comprehensive talent management system using C\\# and .NET Core
\\item Built complete office management platform from scratch
\\item Implemented RESTful APIs and microservices for scalable architecture
\\item Integrated SQL and NoSQL databases with optimized performance
\\end{{itemize}}

\\textbf{{IT-Hogskolan | Backend Developer (Part-time)}}\\\\
January 2023 - May 2023 | Gothenburg, Sweden
\\begin{{itemize}}[noitemsep]
\\item Migrated "Omstallningsstod.se" platform using Spring Boot
\\item Developed RESTful APIs for frontend integration
\\item Collaborated with UI/UX designers for seamless integration
\\item Implemented automated tests as part of delivery process
\\end{{itemize}}

\\textbf{{Senior Material (Europe) AB | Platform Architect}}\\\\
January 2022 - December 2022 | Eskilstuna, Sweden
\\begin{{itemize}}[noitemsep]
\\item Led migration of business-critical applications with microservices
\\item Developed backend services with Spring Boot
\\item Collaborated with teams to optimize applications for scalability
\\item Participated in Agile ceremonies and sprint planning
\\end{{itemize}}

\\textbf{{Pembio AB | Fullstack Developer}}\\\\
October 2020 - September 2021 | Lund, Sweden
\\begin{{itemize}}[noitemsep]
\\item Developed Pembio.com platform backend with Java and Spring Boot
\\item Built frontend features using Vue.js framework
\\item Developed RESTful APIs and implemented database integration
\\item Participated in Agile development processes
\\end{{itemize}}

% Projects
\\section*{{Hobby Projects}}

\\textbf{{Gothenburg TaxiCarPooling Web Application}}\\\\
May 2025 - Present
\\begin{{itemize}}[noitemsep]
\\item Developing intelligent carpooling platform using Spring Boot and Node.js
\\item Cross-platform mobile application with React Native
\\item Implemented automated order matching algorithm and RESTful APIs
\\item PostgreSQL database integration optimized for scalability
\\end{{itemize}}

\\textbf{{SmartTV \\& VoiceBot - Android Auto Applications}}\\\\
March 2025 - Present
\\begin{{itemize}}[noitemsep]
\\item Developing Android Auto apps with Java backend services
\\item Implemented RESTful APIs for real-time data processing
\\item Built secure API integrations with SQL database optimization
\\item Comprehensive testing framework for frontend and backend
\\end{{itemize}}

\\textbf{{Hong Yan AB - E-commerce Platform (smrtmart.com)}}\\\\
April 2024 - Present
\\begin{{itemize}}[noitemsep]
\\item Fullstack e-commerce platform with Spring Boot and React
\\item Implemented microservices architecture with PostgreSQL and MongoDB
\\item Built order management, inventory tracking, and payment processing
\\item Optimized application performance for maximum speed and scalability
\\end{{itemize}}

% Education
\\section*{{Education}}
\\textbf{{IT Hogskolan}}\\\\
Bachelor's Degree in .NET Cloud Development | 2021-2023\\\\
Bachelor's Degree in Java Integration | 2019-2021\\\\

\\textbf{{University of Gothenburg}}\\\\
Master's Degree in International Business and Trade | 2016-2019

% Certifications
\\section*{{Certifications}}
\\begin{{itemize}}[noitemsep]
\\item AWS Certified Solutions Architect - Associate (Aug 2022)
\\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\\item AWS Certified Developer - Associate (Nov 2022)
\\end{{itemize}}

% Additional Information
\\section*{{Additional Information}}
\\begin{{itemize}}[noitemsep]
\\item Languages: Fluent in English and Mandarin
\\item Interests: Vehicle technology, energy sector, electrical charging systems
\\item Personal Website: bluehawana.com
\\end{{itemize}}

\\end{{document}}"""
    
    def create_simple_cover_letter_template(self, job_title, company, department, address, city):
        """Create a simplified cover letter template that compiles reliably"""
        
        role_introductions = {
            "devops": "I am writing to express my strong interest in the DevOps Engineer position",
            "backend": "I am writing to express my strong interest in the Backend Developer position", 
            "frontend": "I am writing to express my strong interest in the Frontend Developer position",
            "fullstack": "I am writing to express my strong interest in the Fullstack Developer position"
        }
        
        role_focus = self.determine_role_focus(job_title)
        intro = role_introductions.get(role_focus, "I am writing to express my strong interest in this position")
        
        return f"""\\documentclass[a4paper,11pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage[utf8]{{inputenc}}

\\begin{{document}}
\\pagestyle{{empty}}

% Header
\\begin{{flushleft}}
Hongzhi Li\\\\
Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299
\\end{{flushleft}}

\\vspace{{20pt}}

% Employer Address
\\begin{{flushleft}}
{company}\\\\
{department if department else "Hiring Department"}\\\\
{address if address else city if city else "Sweden"}
\\end{{flushleft}}

\\vspace{{20pt}}

% Date
\\begin{{flushleft}}
\\today
\\end{{flushleft}}

\\vspace{{20pt}}

% Salutation
Dear Hiring Manager,

\\vspace{{10pt}}

{intro} at {company}. With over 5 years of hands-on experience in software development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for innovative solutions to your team.

Throughout my career, I have successfully built scalable applications using modern technologies across the entire development stack. My experience spans from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core, with comprehensive database management across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions and comprehensive development practices. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications, has given me valuable experience in building scalable, enterprise-level applications that serve diverse user bases.

My recent projects demonstrate comprehensive technical capabilities: developing end-to-end platforms with modern technologies, implementing microservices architectures, and creating seamless user experiences. I am particularly skilled in bridging the gap between different technologies and ensuring optimal performance across the entire application stack.

I am passionate about continuous learning and staying current with emerging technologies. My experience with agile methodologies, cross-functional collaboration, and modern development practices positions me well to contribute immediately to your development initiatives while fostering innovation and technical excellence.

Thank you for considering my application. I would welcome the opportunity to discuss how my technical expertise can contribute to {company}'s continued success and technological advancement.

\\vspace{{20pt}}

Sincerely,\\\\
Hongzhi Li

\\end{{document}}"""
    
    def compile_simple_latex(self, tex_content, output_name):
        """Compile LaTeX with simplified approach"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            try:
                # Write the LaTeX file
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(tex_content)
                
                print(f"✅ Simple LaTeX file written: {tex_file}")
                
                # Simple compilation
                cmd = ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(tex_file)]
                
                # Run compilation twice for references
                for run in range(2):
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                    
                    if result.returncode != 0 and run == 1:
                        print(f"❌ Compilation failed. Error output:")
                        print(result.stdout[-500:] if result.stdout else "No stdout")
                        print(result.stderr[-500:] if result.stderr else "No stderr")
                        return None
                
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    size = os.path.getsize(final_path) / 1024
                    print(f"🎉 Simple PDF successfully generated: {final_path} ({size:.1f} KB)")
                    return final_path
                else:
                    print("❌ PDF file not generated")
                    return None
                    
            except Exception as e:
                print(f"❌ Error compiling simple LaTeX: {e}")
                return None
    
    def extract_simple_preview(self, tex_content, content_type="CV", job_title="Position", company="Company"):
        """Extract preview from simple LaTeX content"""
        
        if content_type == "CV":
            preview = f"""
📋 Job Title: {job_title}
🏢 Company: {company}

📝 Profile Summary Preview:
Experienced developer with 5+ years in software development and infrastructure...

🔧 Technical Skills:
• Programming Languages: Java/J2EE, JavaScript, C#/.NET Core, Python
• Frontend: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3  
• Backend: Spring Boot, .NET Core, ASP.NET, Node.js
• Databases: PostgreSQL, MySQL, MongoDB, AWS RDS
• Cloud: AWS, Azure, GCP
• DevOps: Docker, Kubernetes, CI/CD

💼 Experience: 6 positions highlighted (ECARX, Synteda, IT-Högskolan, etc.)
🚀 Hobby Projects: 3 major projects (TaxiCarPooling, SmartTV, E-commerce)
🎓 Education: IT Högskolan, University of Gothenburg
📜 Certifications: AWS, Azure certifications
"""
        else:  # Cover Letter
            preview = f"""
🏢 Company: {company}
💼 Position: {job_title}

📝 Opening Paragraph:
I am writing to express my strong interest in this position at {company}. With over 5 years of hands-on experience...

✅ Content includes:
• Role-specific introduction and interest
• Technical expertise alignment  
• Project examples and achievements
• Company-specific motivation
• Professional closing
"""
        
        return preview.strip()
    
    def send_simple_review_email(self, job_title, company, cv_tex, cl_tex, cv_pdf=None, cl_pdf=None, role_focus="fullstack"):
        """Send email with simple PDFs and previews"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            # Read LaTeX content for preview
            cv_content = ""
            cl_content = ""
            
            if cv_tex and Path(cv_tex).exists():
                with open(cv_tex, 'r', encoding='utf-8') as f:
                    cv_content = f.read()
            
            if cl_tex and Path(cl_tex).exists():
                with open(cl_tex, 'r', encoding='utf-8') as f:
                    cl_content = f.read()
            
            # Extract previews
            cv_preview = self.extract_simple_preview(cv_content, "CV", job_title, company)
            cl_preview = self.extract_simple_preview(cl_content, "Cover Letter", job_title, company)
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"✅ JobHunter READY: {job_title} at {company} - PDF + LaTeX Complete"
            
            # Create comprehensive email body
            pdf_status = "✅ Successfully compiled" if cv_pdf and cl_pdf else "❌ Compilation failed"
            
            body = f"""Hi,

✅ COMPLETE job application package ready for immediate use:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Role Focus: {role_focus.title()}
📍 Priority: {'🏢 Gothenburg High Priority' if 'gothenburg' in company.lower() or 'volvo' in company.lower() else '🌐 Remote/Other'}

📎 Files attached:
   • CV (PDF): {pdf_status}
   • Cover Letter (PDF): {pdf_status}
   • CV (LaTeX source): ✅ Always included for editing
   • Cover Letter (LaTeX source): ✅ Always included for editing

📋 CV PREVIEW:
{cv_preview}

📋 COVER LETTER PREVIEW:  
{cl_preview}

🚀 READY TO SEND:
If PDFs are attached, you can send them directly to employers immediately!

🔧 IF YOU NEED TO EDIT:
1. Download the .tex files (LaTeX source)
2. Open in any text editor (VS Code, Sublime, Notepad++)
3. Make your changes to the text content
4. Compile to PDF:
   - Method 1: pdflatex filename.tex (run twice)
   - Method 2: Use online LaTeX editor (Overleaf.com)
   - Method 3: Use LaTeX software (MiKTeX, TeX Live)

🔧 COMPILATION COMMANDS:
   pdflatex {cv_tex}
   pdflatex {cv_tex}  # Run twice for references
   pdflatex {cl_tex}
   pdflatex {cl_tex}  # Run twice for references

🎯 This application uses simplified LaTeX templates optimized for reliable compilation.

Best regards,
JobHunter Complete System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach all available files
            attachments = []
            
            # Add PDFs if available
            if cv_pdf and Path(cv_pdf).exists():
                attachments.append((cv_pdf, f"CV_{company}_{job_title}_READY.pdf"))
            if cl_pdf and Path(cl_pdf).exists():
                attachments.append((cl_pdf, f"CoverLetter_{company}_{job_title}_READY.pdf"))
            
            # Always add LaTeX source files
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
            
            print(f"✅ Complete review email sent!")
            print(f"📎 Attached: {len(attachments)} files")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

async def main():
    """Test simple PDF generator with reliable compilation"""
    generator = SimplePDFGenerator()
    
    # Test jobs
    test_jobs = [
        ("Solution Developer", "Volvo Group", "Onsite Infrastructure", "Sven Erikssons gata 7", "Göteborg"),
        ("DevOps Engineer", "Spotify", "Infrastructure Team", "", "Stockholm")
    ]
    
    print("🎯 Simple PDF JobHunter - Reliable PDF Generation")
    print("=" * 60)
    print("📝 Creating simplified LaTeX templates for reliable compilation")
    print("👁️  Including content previews in email")
    print()
    
    for job_title, company, department, address, city in test_jobs:
        print(f"📋 Processing: {job_title} at {company}")
        
        role_focus = generator.determine_role_focus(job_title)
        print(f"🎯 Role Focus: {role_focus}")
        
        try:
            # Generate simple content
            print("✏️  Creating simplified templates...")
            cv_content = generator.create_simple_cv_template(job_title, company, role_focus)
            cl_content = generator.create_simple_cover_letter_template(job_title, company, department, address, city)
            
            # Save LaTeX files
            cv_tex = f"simple_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv.tex"
            cl_tex = f"simple_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl.tex"
            
            with open(cv_tex, 'w', encoding='utf-8') as f:
                f.write(cv_content)
            with open(cl_tex, 'w', encoding='utf-8') as f:
                f.write(cl_content)
            
            print(f"💾 Simple LaTeX saved: {cv_tex}, {cl_tex}")
            
            # Try to compile PDFs
            print("🔨 Compiling simple PDFs...")
            cv_pdf = generator.compile_simple_latex(cv_content, f"simple_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv")
            cl_pdf = generator.compile_simple_latex(cl_content, f"simple_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl")
            
            # Send comprehensive email
            print("📧 Sending simple package...")
            success = generator.send_simple_review_email(job_title, company, cv_tex, cl_tex, cv_pdf, cl_pdf, role_focus)
            
            if success:
                print(f"🎉 SUCCESS: Simple package sent!")
                
                # Clean up PDF files but keep LaTeX
                try:
                    if cv_pdf:
                        os.remove(cv_pdf)
                    if cl_pdf:
                        os.remove(cl_pdf)
                except:
                    pass
            else:
                print(f"❌ FAILED: Email not sent")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print()
        await asyncio.sleep(2)
    
    print(f"📧 Check {generator.recipient_email} for simple packages!")
    print("👁️  Each email includes content previews and ready-to-use PDFs!")

if __name__ == "__main__":
    asyncio.run(main())