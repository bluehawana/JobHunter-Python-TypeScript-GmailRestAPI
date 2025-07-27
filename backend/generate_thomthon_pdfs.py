#!/usr/bin/env python3
"""
Generate PDFs for Thomthon Retuer application
Creates ready-to-send PDF resume and cover letter
"""
import subprocess
import tempfile
import shutil
import os
from pathlib import Path

def create_thomthon_cv():
    """Create CV template for Thomthon Retuer position"""
    return """\\documentclass[11pt,a4paper]{article}
\\usepackage[margin=0.75in]{geometry}

\\begin{document}
\\pagestyle{empty}

% Header
\\begin{center}
{\\Large \\textbf{Hongzhi Li}}\\\\[5pt]
{\\large Solution Developer}\\\\[5pt]
hongzhili01@gmail.com $|$ 0728384299 $|$ LinkedIn: hzl $|$ GitHub: bluehawana
\\end{center}

\\vspace{10pt}

% Profile Summary
\\noindent\\textbf{Profile Summary}\\\\
Experienced DevOps Engineer and Infrastructure Specialist with 5+ years in infrastructure automation, cloud platforms, and CI/CD. Expert in Kubernetes, Docker, AWS/Azure. Currently at ECARX leading infrastructure optimization projects perfect for Thomthon Retuer's automation and digital transformation initiatives.

\\vspace{10pt}

% Technical Skills
\\noindent\\textbf{Core Technical Skills}\\\\
$\\bullet$ Programming: Java/J2EE, JavaScript, C\\#/.NET Core, Python, Bash\\\\
$\\bullet$ Frontend: Angular, ReactJS, React Native, Vue.js, HTML5, CSS3\\\\
$\\bullet$ Backend: Spring Boot, .NET Core, ASP.NET, Node.js\\\\
$\\bullet$ APIs: RESTful APIs, GraphQL, Microservices Architecture\\\\
$\\bullet$ Databases: PostgreSQL, MySQL, MongoDB, AWS RDS\\\\
$\\bullet$ Cloud: AWS, Azure, GCP\\\\
$\\bullet$ DevOps: Docker, Kubernetes, Jenkins, GitHub Actions\\\\
$\\bullet$ Version Control: Git, GitHub, GitLab

\\vspace{10pt}

% Experience
\\noindent\\textbf{Professional Experience}

\\vspace{5pt}
\\noindent\\textbf{ECARX $|$ IT/Infrastructure Specialist}\\\\
October 2024 - Present $|$ Gothenburg, Sweden\\\\
$\\bullet$ Leading infrastructure optimization and system integration projects\\\\
$\\bullet$ Implementing cost optimization by migrating from AKS to local Kubernetes\\\\
$\\bullet$ Modern monitoring solutions using Grafana and advanced scripting\\\\
$\\bullet$ Managing complex network systems and technical solution design

\\vspace{5pt}
\\noindent\\textbf{Synteda $|$ Azure Fullstack Developer (Freelance)}\\\\
August 2023 - September 2024 $|$ Gothenburg, Sweden\\\\
$\\bullet$ Developed talent management system using C\\# and .NET Core\\\\
$\\bullet$ Built complete office management platform from scratch\\\\
$\\bullet$ Implemented RESTful APIs and microservices architecture\\\\
$\\bullet$ Integrated SQL and NoSQL databases with optimized performance

\\vspace{5pt}
\\noindent\\textbf{IT-Hogskolan $|$ Backend Developer (Part-time)}\\\\
January 2023 - May 2023 $|$ Gothenburg, Sweden\\\\
$\\bullet$ Migrated "Omstallningsstod.se" platform using Spring Boot\\\\
$\\bullet$ Developed RESTful APIs for frontend integration\\\\
$\\bullet$ Collaborated with UI/UX designers for seamless integration\\\\
$\\bullet$ Implemented automated tests as part of delivery process

\\vspace{5pt}
\\noindent\\textbf{Senior Material (Europe) AB $|$ Platform Architect}\\\\
January 2022 - December 2022 $|$ Eskilstuna, Sweden\\\\
$\\bullet$ Led migration of business-critical applications with microservices\\\\
$\\bullet$ Developed backend services with Spring Boot\\\\
$\\bullet$ Optimized applications for maximum speed and scalability\\\\
$\\bullet$ Participated in Agile ceremonies and sprint planning

\\vspace{5pt}
\\noindent\\textbf{Pembio AB $|$ Fullstack Developer}\\\\
October 2020 - September 2021 $|$ Lund, Sweden\\\\
$\\bullet$ Developed platform backend with Java and Spring Boot\\\\
$\\bullet$ Built frontend features using Vue.js framework\\\\
$\\bullet$ Developed RESTful APIs and database integration\\\\
$\\bullet$ Participated in Agile development processes

\\vspace{10pt}

% Projects
\\noindent\\textbf{Hobby Projects}

\\vspace{5pt}
\\noindent\\textbf{Gothenburg TaxiCarPooling Web Application}\\\\
May 2025 - Present\\\\
$\\bullet$ Intelligent carpooling platform using Spring Boot and Node.js\\\\
$\\bullet$ Cross-platform mobile application with React Native\\\\
$\\bullet$ Automated order matching algorithm and RESTful APIs\\\\
$\\bullet$ PostgreSQL database integration optimized for scalability

\\vspace{5pt}
\\noindent\\textbf{SmartTV \\& VoiceBot - Android Auto Applications}\\\\
March 2025 - Present\\\\
$\\bullet$ Android Auto apps with Java backend services\\\\
$\\bullet$ RESTful APIs for real-time data processing\\\\
$\\bullet$ Secure API integrations with SQL database optimization\\\\
$\\bullet$ Comprehensive testing framework

\\vspace{5pt}
\\noindent\\textbf{Hong Yan AB - E-commerce Platform (smrtmart.com)}\\\\
April 2024 - Present\\\\
$\\bullet$ Fullstack platform with Spring Boot and React\\\\
$\\bullet$ Microservices architecture with PostgreSQL and MongoDB\\\\
$\\bullet$ Order management, inventory tracking, payment processing\\\\
$\\bullet$ Optimized for maximum speed and scalability

\\vspace{10pt}

% Education
\\noindent\\textbf{Education}\\\\
\\textbf{IT Hogskolan}\\\\
Bachelor's in .NET Cloud Development $|$ 2021-2023\\\\
Bachelor's in Java Integration $|$ 2019-2021\\\\
\\textbf{University of Gothenburg}\\\\
Master's in International Business and Trade $|$ 2016-2019

\\vspace{10pt}

% Certifications
\\noindent\\textbf{Certifications}\\\\
$\\bullet$ AWS Certified Solutions Architect - Associate (Aug 2022)\\\\
$\\bullet$ Microsoft Certified: Azure Fundamentals (Jun 2022)\\\\
$\\bullet$ AWS Certified Developer - Associate (Nov 2022)

\\vspace{10pt}

% Additional
\\noindent\\textbf{Additional Information}\\\\
$\\bullet$ Languages: Fluent in English and Mandarin\\\\
$\\bullet$ Interests: Vehicle technology, energy sector, electrical charging\\\\
$\\bullet$ Website: bluehawana.com

\\end{document}"""

def create_thomthon_cover_letter():
    """Create cover letter template for Thomthon Retuer position"""
    return """\\documentclass[a4paper,11pt]{article}
\\usepackage[margin=1in]{geometry}

\\begin{document}
\\pagestyle{empty}

% Header
\\noindent
Hongzhi Li\\\\
Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299

\\vspace{20pt}

% Employer
\\noindent
Thomthon Retuer\\\\
Hiring Department\\\\
Sweden

\\vspace{20pt}

% Date
\\noindent
\\today

\\vspace{20pt}

% Letter
Dear Hiring Manager,

\\vspace{10pt}

I am writing to express my strong interest in the Solution Developer position at Thomthon Retuer. With over 5 years of hands-on experience in software development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my comprehensive technical expertise and passion for innovative solutions to your team.

Throughout my career, I have successfully built scalable applications using modern technologies across the entire development stack. My experience spans from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core, with comprehensive database management across SQL and NoSQL platforms.

What particularly excites me about Thomthon Retuer is your commitment to innovative technology solutions and comprehensive development practices. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications, has given me valuable experience in building scalable, enterprise-level applications that serve diverse user bases.

My recent projects demonstrate comprehensive technical capabilities: developing end-to-end platforms with modern technologies, implementing microservices architectures, and creating seamless user experiences. I am particularly skilled in bridging the gap between different technologies and ensuring optimal performance across the entire application stack.

I am passionate about continuous learning and staying current with emerging technologies. My experience with agile methodologies, cross-functional collaboration, and modern development practices positions me well to contribute immediately to your development initiatives while fostering innovation and technical excellence.

Thank you for considering my application. I would welcome the opportunity to discuss how my technical expertise can contribute to Thomthon Retuer's continued success and technological advancement.

\\vspace{20pt}

Sincerely,\\\\
Hongzhi Li

\\end{document}"""

def compile_latex_to_pdf(tex_content, output_name):
    """Compile LaTeX content to PDF"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / f"{output_name}.tex"
        
        try:
            # Write the LaTeX file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            print(f"✅ LaTeX file written: {output_name}.tex")
            
            # Compile PDF
            cmd = ['pdflatex', '-interaction=nonstopmode', str(tex_file)]
            
            # Run compilation twice for references
            for run in range(2):
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path, timeout=30)
                
                if result.returncode != 0 and run == 1:
                    print(f"❌ Compilation failed for {output_name}")
                    print("STDOUT:", result.stdout[-500:] if result.stdout else "None")
                    print("STDERR:", result.stderr[-500:] if result.stderr else "None")
                    return None
            
            pdf_file = temp_path / f"{output_name}.pdf"
            if pdf_file.exists():
                final_path = f"{output_name}.pdf"
                shutil.copy2(pdf_file, final_path)
                size = os.path.getsize(final_path) / 1024
                print(f"🎉 PDF generated: {final_path} ({size:.1f} KB)")
                return final_path
            else:
                print("❌ PDF file not found after compilation")
                return None
                
        except Exception as e:
            print(f"❌ Error compiling LaTeX: {e}")
            return None

def main():
    """Generate PDFs for Thomthon Retuer application"""
    print("🎯 Generating PDFs for Thomthon Retuer Application")
    print("=" * 60)
    
    # Generate CV
    print("📄 Creating CV...")
    cv_content = create_thomthon_cv()
    cv_pdf = compile_latex_to_pdf(cv_content, "thomthon_retuer_cv")
    
    # Generate Cover Letter
    print("📄 Creating Cover Letter...")
    cl_content = create_thomthon_cover_letter()
    cl_pdf = compile_latex_to_pdf(cl_content, "thomthon_retuer_cover_letter")
    
    # Results
    print("\\n📊 Results:")
    print("=" * 30)
    if cv_pdf:
        print(f"✅ CV: {cv_pdf}")
    else:
        print("❌ CV generation failed")
        
    if cl_pdf:
        print(f"✅ Cover Letter: {cl_pdf}")
    else:
        print("❌ Cover Letter generation failed")
    
    if cv_pdf and cl_pdf:
        print(f"\\n🎉 Success! Both PDFs ready for Thomthon Retuer application")
        print(f"📎 You can now directly send these PDFs to employers")
        return True
    else:
        print(f"\\n⚠️  Some PDFs failed to generate")
        return False

if __name__ == "__main__":
    main()