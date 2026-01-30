#!/usr/bin/env python3
"""
Ultra Simple Generator - Uses only core LaTeX packages
No external dependencies - guaranteed to work
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

# Import our smart editor
import sys
sys.path.append(str(Path(__file__).parent))
from smart_latex_editor import SmartLaTeXEditor

class UltraSimpleGenerator(SmartLaTeXEditor):
    def __init__(self):
        super().__init__()
    
    def create_basic_cv_template(self, job_title, company, role_focus):
        """Create ultra-basic CV template using only core LaTeX"""
        
        profile_summaries = {
            "devops": f"Experienced DevOps Engineer with 5+ years in infrastructure automation, cloud platforms, and CI/CD. Expert in Kubernetes, Docker, AWS/Azure. Currently at ECARX leading infrastructure optimization.",
            "backend": f"Experienced Backend Developer with 5+ years in Java/Spring Boot, REST APIs, and microservices. Expert in database management and scalable architectures. Currently at ECARX with comprehensive technical expertise.",
            "frontend": f"Experienced Frontend Developer with 5+ years in Angular, React, and modern web technologies. Expert in responsive design and user experience. Currently at ECARX bringing technical knowledge.",
            "fullstack": f"Experienced Fullstack Developer with 5+ years in end-to-end application development. Expert in Spring Boot, React/Angular, and database integration. Currently at ECARX with comprehensive expertise."
        }
        
        return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[margin=0.75in]{{geometry}}

\\begin{{document}}
\\pagestyle{{empty}}

% Header
\\begin{{center}}
{{\\Large \\textbf{{Hongzhi Li}}}}\\\\[5pt]
{{\\large {job_title}}}\\\\[5pt]
hongzhili01@gmail.com $|$ 0728384299 $|$ LinkedIn: hzl $|$ GitHub: bluehawana
\\end{{center}}

\\vspace{{10pt}}

% Profile Summary
\\noindent\\textbf{{Profile Summary}}\\\\
{profile_summaries.get(role_focus, profile_summaries["fullstack"])}

\\vspace{{10pt}}

% Technical Skills
\\noindent\\textbf{{Core Technical Skills}}\\\\
$\\bullet$ Programming: Java/J2EE, JavaScript, C\\#/.NET Core, Python, Bash\\\\
$\\bullet$ Frontend: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3\\\\
$\\bullet$ Backend: Spring Boot, .NET Core, ASP.NET, Node.js\\\\
$\\bullet$ APIs: RESTful APIs, GraphQL, Microservices Architecture\\\\
$\\bullet$ Databases: PostgreSQL, MySQL, MongoDB, AWS RDS\\\\
$\\bullet$ Cloud: AWS, Azure, GCP\\\\
$\\bullet$ DevOps: Docker, Kubernetes, Jenkins, GitHub Actions\\\\
$\\bullet$ Version Control: Git, GitHub, GitLab

\\vspace{{10pt}}

% Experience
\\noindent\\textbf{{Professional Experience}}

\\vspace{{5pt}}
\\noindent\\textbf{{ECARX $|$ IT/Infrastructure Specialist}}\\\\
October 2024 - Present $|$ Gothenburg, Sweden\\\\
$\\bullet$ Leading infrastructure optimization and system integration projects\\\\
$\\bullet$ Implementing cost optimization by migrating from AKS to local Kubernetes\\\\
$\\bullet$ Modern monitoring solutions using Grafana and advanced scripting\\\\
$\\bullet$ Managing complex network systems and technical solution design

\\vspace{{5pt}}
\\noindent\\textbf{{Synteda $|$ Azure Fullstack Developer (Freelance)}}\\\\
August 2023 - September 2024 $|$ Gothenburg, Sweden\\\\
$\\bullet$ Developed talent management system using C\\# and .NET Core\\\\
$\\bullet$ Built complete office management platform from scratch\\\\
$\\bullet$ Implemented RESTful APIs and microservices architecture\\\\
$\\bullet$ Integrated SQL and NoSQL databases with optimized performance

\\vspace{{5pt}}
\\noindent\\textbf{{IT-Hogskolan $|$ Backend Developer (Part-time)}}\\\\
January 2023 - May 2023 $|$ Gothenburg, Sweden\\\\
$\\bullet$ Migrated "Omstallningsstod.se" platform using Spring Boot\\\\
$\\bullet$ Developed RESTful APIs for frontend integration\\\\
$\\bullet$ Collaborated with UI/UX designers for seamless integration\\\\
$\\bullet$ Implemented automated tests as part of delivery process

\\vspace{{5pt}}
\\noindent\\textbf{{Senior Material (Europe) AB $|$ Platform Architect}}\\\\
January 2022 - December 2022 $|$ Eskilstuna, Sweden\\\\
$\\bullet$ Led migration of business-critical applications with microservices\\\\
$\\bullet$ Developed backend services with Spring Boot\\\\
$\\bullet$ Optimized applications for maximum speed and scalability\\\\
$\\bullet$ Participated in Agile ceremonies and sprint planning

\\vspace{{5pt}}
\\noindent\\textbf{{Pembio AB $|$ Fullstack Developer}}\\\\
October 2020 - September 2021 $|$ Lund, Sweden\\\\
$\\bullet$ Developed platform backend with Java and Spring Boot\\\\
$\\bullet$ Built frontend features using Vue.js framework\\\\
$\\bullet$ Developed RESTful APIs and database integration\\\\
$\\bullet$ Participated in Agile development processes

\\vspace{{10pt}}

% Projects
\\noindent\\textbf{{Hobby Projects}}

\\vspace{{5pt}}
\\noindent\\textbf{{Gothenburg TaxiCarPooling Web Application}}\\\\
May 2025 - Present\\\\
$\\bullet$ Intelligent carpooling platform using Spring Boot and Node.js\\\\
$\\bullet$ Cross-platform mobile application with React Native\\\\
$\\bullet$ Automated order matching algorithm and RESTful APIs\\\\
$\\bullet$ PostgreSQL database integration optimized for scalability

\\vspace{{5pt}}
\\noindent\\textbf{{SmartTV \\& VoiceBot - Android Auto Applications}}\\\\
March 2025 - Present\\\\
$\\bullet$ Android Auto apps with Java backend services\\\\
$\\bullet$ RESTful APIs for real-time data processing\\\\
$\\bullet$ Secure API integrations with SQL database optimization\\\\
$\\bullet$ Comprehensive testing framework

\\vspace{{5pt}}
\\noindent\\textbf{{Hong Yan AB - E-commerce Platform (smrtmart.com)}}\\\\
April 2024 - Present\\\\
$\\bullet$ Fullstack platform with Spring Boot and React\\\\
$\\bullet$ Microservices architecture with PostgreSQL and MongoDB\\\\
$\\bullet$ Order management, inventory tracking, payment processing\\\\
$\\bullet$ Optimized for maximum speed and scalability

\\vspace{{10pt}}

% Education
\\noindent\\textbf{{Education}}\\\\
\\textbf{{IT Hogskolan}}\\\\
Bachelor's in .NET Cloud Development $|$ 2021-2023\\\\
Bachelor's in Java Integration $|$ 2019-2021\\\\
\\textbf{{University of Gothenburg}}\\\\
Master's in International Business and Trade $|$ 2016-2019

\\vspace{{10pt}}

% Certifications
\\noindent\\textbf{{Certifications}}\\\\
$\\bullet$ AWS Certified Solutions Architect - Associate (Aug 2022)\\\\
$\\bullet$ Microsoft Certified: Azure Fundamentals (Jun 2022)\\\\
$\\bullet$ AWS Certified Developer - Associate (Nov 2022)

\\vspace{{10pt}}

% Additional
\\noindent\\textbf{{Additional Information}}\\\\
$\\bullet$ Languages: Fluent in English and Mandarin\\\\
$\\bullet$ Interests: Vehicle technology, energy sector, electrical charging\\\\
$\\bullet$ Website: bluehawana.com

\\end{{document}}"""
    
    def create_basic_cover_letter_template(self, job_title, company, department, address, city):
        """Create ultra-basic cover letter template using only core LaTeX"""
        
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

\\begin{{document}}
\\pagestyle{{empty}}

% Header
\\noindent
Hongzhi Li\\\\
Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299

\\vspace{{20pt}}

% Employer
\\noindent
{company}\\\\
{department if department else "Hiring Department"}\\\\
{address if address else city if city else "Sweden"}

\\vspace{{20pt}}

% Date
\\noindent
\\today

\\vspace{{20pt}}

% Letter
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
    
    def compile_ultra_basic_latex(self, tex_content, output_name):
        """Compile ultra-basic LaTeX with only core packages"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / f"{output_name}.tex"
            
            try:
                # Write the LaTeX file
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(tex_content)
                
                print(f"✅ Ultra-basic LaTeX written: {output_name}.tex")
                
                # Ultra-simple compilation
                cmd = ['pdflatex', '-interaction=nonstopmode', str(tex_file)]
                
                # Run in temp directory
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                
                if result.returncode != 0:
                    print(f"❌ Ultra-basic compilation failed:")
                    print("STDOUT:", result.stdout[-300:] if result.stdout else "None")
                    print("STDERR:", result.stderr[-300:] if result.stderr else "None")
                    return None
                
                # Run second time for references
                subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                
                pdf_file = temp_path / f"{output_name}.pdf"
                if pdf_file.exists():
                    final_path = f"{output_name}.pdf"
                    shutil.copy2(pdf_file, final_path)
                    size = os.path.getsize(final_path) / 1024
                    print(f"🎉 Ultra-basic PDF generated: {final_path} ({size:.1f} KB)")
                    return final_path
                else:
                    print("❌ PDF file not found after compilation")
                    return None
                    
            except Exception as e:
                print(f"❌ Error in ultra-basic compilation: {e}")
                return None
    
    async def test_ultra_basic(self):
        """Test ultra-basic generation"""
        
        test_jobs = [
            ("Solution Developer", "Volvo Group", "devops"),
            ("Fullstack Developer", "Ericsson", "fullstack")
        ]
        
        print("🎯 Ultra-Basic PDF Generation Test")
        print("=" * 50)
        
        for job_title, company, role_focus in test_jobs:
            print(f"\\n📋 Testing: {job_title} at {company}")
            
            try:
                # Generate templates
                cv_content = self.create_basic_cv_template(job_title, company, role_focus)
                cl_content = self.create_basic_cover_letter_template(job_title, company, "", "", "Gothenburg")
                
                # Save LaTeX files
                cv_name = f"ultra_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cv"
                cl_name = f"ultra_{job_title.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}_cl"
                
                cv_tex = f"{cv_name}.tex"
                cl_tex = f"{cl_name}.tex"
                
                with open(cv_tex, 'w', encoding='utf-8') as f:
                    f.write(cv_content)
                with open(cl_tex, 'w', encoding='utf-8') as f:
                    f.write(cl_content)
                
                print(f"💾 Saved: {cv_tex}, {cl_tex}")
                
                # Try compilation
                print("🔨 Compiling ultra-basic PDFs...")
                cv_pdf = self.compile_ultra_basic_latex(cv_content, cv_name)
                cl_pdf = self.compile_ultra_basic_latex(cl_content, cl_name)
                
                if cv_pdf and cl_pdf:
                    print(f"✅ SUCCESS: Both PDFs compiled!")
                    
                    # Send email with working PDFs
                    success = await self.send_working_email(job_title, company, cv_tex, cl_tex, cv_pdf, cl_pdf, role_focus)
                    if success:
                        print("📧 Email sent successfully!")
                    
                    # Clean up PDFs
                    try:
                        os.remove(cv_pdf)
                        os.remove(cl_pdf)
                    except:
                        pass
                else:
                    print("❌ PDF compilation failed")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def send_working_email(self, job_title, company, cv_tex, cl_tex, cv_pdf, cl_pdf, role_focus):
        """Send email with working PDFs"""
        
        if not self.password:
            print("❌ SMTP_PASSWORD not set")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🎉 WORKING PDFs: {job_title} at {company} - Ready to Send!"
            
            body = f"""Hi!

🎉 SUCCESS! Working PDF files generated:

🏢 Company: {company}
💼 Position: {job_title}
🎯 Role Focus: {role_focus.title()}

📎 Files attached:
   ✅ CV (PDF) - Ready to send to employers
   ✅ Cover Letter (PDF) - Ready to send to employers  
   ✅ CV (LaTeX source) - For editing if needed
   ✅ Cover Letter (LaTeX source) - For editing if needed

🚀 These PDFs are ready to send directly to employers!

🔧 Content Preview:
• CV: 3-page professional format with all experience and projects
• Cover Letter: Tailored for {role_focus} role at {company}
• Templates use ultra-basic LaTeX for reliable compilation

📧 Ready for immediate use - no further compilation needed!

Best regards,
JobHunter Ultra-Basic System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach files
            attachments = [
                (cv_pdf, f"CV_{company}_{job_title}_READY.pdf"),
                (cl_pdf, f"CoverLetter_{company}_{job_title}_READY.pdf"),
                (cv_tex, f"CV_{company}_{job_title}_SOURCE.tex"),
                (cl_tex, f"CoverLetter_{company}_{job_title}_SOURCE.tex")
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
            
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

async def main():
    generator = UltraSimpleGenerator()
    await generator.test_ultra_basic()

if __name__ == "__main__":
    asyncio.run(main())