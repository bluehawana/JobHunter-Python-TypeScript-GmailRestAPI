#!/usr/bin/env python3
"""
Proper PDF compilation script using pdflatex
Creates valid PDFs with format: hongzhi_devops_opera.pdf
"""
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

def compile_latex_to_pdf(tex_content, output_name, job_title="devops"):
    """
    Compile LaTeX content to PDF using pdflatex
    """
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / f"{output_name}.tex"
        
        # Write LaTeX content to file
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        
        # Compile with pdflatex (run twice for proper references)
        try:
            for i in range(2):
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', str(temp_path),
                    str(tex_file)
                ], capture_output=True, text=True, cwd=temp_path)
                
                if result.returncode != 0:
                    print(f"LaTeX compilation error (pass {i+1}):")
                    print(result.stdout)
                    print(result.stderr)
                    if i == 0:  # Continue to second pass even if first fails
                        continue
                    return None
            
            # Check if PDF was generated
            pdf_file = temp_path / f"{output_name}.pdf"
            if pdf_file.exists():
                # Copy to current directory with proper name
                final_name = f"hongzhi_{job_title}_opera.pdf"
                shutil.copy2(pdf_file, final_name)
                print(f"✅ PDF generated: {final_name}")
                return final_name
            else:
                print("❌ PDF file not found after compilation")
                return None
                
        except FileNotFoundError:
            print("❌ pdflatex not found. Please install LaTeX distribution (e.g., MacTeX)")
            return None
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return None

def create_modern_cv_template(job_title="DevOps Engineer", company="Opera Software"):
    """
    Create modern CV template based on the provided format
    """
    cv_template = r"""\documentclass[11pt,a4paper,sans]{moderncv}
\moderncvstyle{banking}
\moderncvcolor{blue}
\usepackage[scale=0.75]{geometry}
\usepackage[utf8]{inputenc}

% Personal data
\name{Hongzhi}{Li}
\title{Fullstack Developer}
\address{Gothenburg, Sweden}
\phone[mobile]{0728384299}
\email{hongzhili01@gmail.com}
\social[linkedin]{linkedin.com/in/hongzhi-li}
\social[github]{github.com/bluehawana}

\begin{document}
\makecvtitle

\section{Profile Summary}
\cvitem{}{Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments.}

\section{Core Technical Skills}
\cvitem{Programming Languages}{Java/J2EE, JavaScript, C\#/.NET Core, Python, Bash, PowerShell}
\cvitem{Frontend Frameworks}{Angular, ReactJS, React Native, Vue.js, HTML5, CSS3}
\cvitem{Backend Frameworks}{Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js}
\cvitem{API Development}{RESTful APIs, GraphQL, Microservices Architecture}
\cvitem{Databases}{PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3}
\cvitem{Testing}{Unit Testing, Integration Testing, Automated Testing, JUnit, Jest}
\cvitem{Cloud Platforms}{AWS, Azure, GCP}
\cvitem{Containerization}{Docker, Kubernetes, Azure Kubernetes Service (AKS)}
\cvitem{Version Control}{Git, GitHub, GitLab}
\cvitem{CI/CD}{Jenkins, GitHub Actions, GitLab CI}
\cvitem{Agile Methodologies}{Scrum, Kanban, Sprint Planning, Code Reviews}

\section{Experience}
\cventry{October 2024--Present}{IT/Infrastructure Specialist}{ECARX}{Gothenburg, Sweden}{}{
\begin{itemize}
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster
\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\end{itemize}}

\cventry{August 2023--September 2024}{Azure Fullstack Developer \& Integration Specialist}{Synteda}{Gothenburg, Sweden}{Freelance}{
\begin{itemize}
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting both frontend and backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}}

\cventry{January 2023--May 2023}{Backend Developer}{IT-Högskolan}{Gothenburg, Sweden}{Part-time}{
\begin{itemize}
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}}

\section{Education}
\cventry{2021--2023}{Bachelor's Degree in .NET Cloud Development}{IT Högskolan}{Mölndal Campus}{}{}
\cventry{2019--2021}{Bachelor's Degree in Java Integration}{IT Högskolan}{Mölndal Campus}{}{}
\cventry{2016--2019}{Master's Degree in International Business and Trade}{University of Gothenburg}{}{}{}

\section{Certifications}
\cvitem{AWS}{Certified Solutions Architect - Associate (Aug 2022)}
\cvitem{Microsoft}{Certified: Azure Fundamentals (Jun 2022)}
\cvitem{AWS}{Certified Developer - Associate (Nov 2022)}

\section{Additional Information}
\cvitem{Languages}{Fluent in English and Mandarin}
\cvitem{Interests}{Vehicle technology, energy sector, electrical charging systems, and battery technology}
\cvitem{Website}{bluehawana.com}

\end{document}"""
    
    return cv_template

def create_modern_cover_letter_template(job_title="DevOps Engineer", company="Opera Software"):
    """
    Create modern cover letter template
    """
    cl_template = rf"""\documentclass[11pt,a4paper,sans]{{moderncv}}
\moderncvstyle{{banking}}
\moderncvcolor{{blue}}
\usepackage[scale=0.75]{{geometry}}
\usepackage[utf8]{{inputenc}}

% Personal data
\name{{Hongzhi}}{{Li}}
\title{{Fullstack Developer}}
\address{{Gothenburg, Sweden}}
\phone[mobile]{{0728384299}}
\email{{hongzhili01@gmail.com}}
\social[linkedin]{{linkedin.com/in/hongzhi-li}}
\social[github]{{github.com/bluehawana}}

\begin{{document}}

\recipient{{{company} Hiring Team}}{{{company}\\Hiring Department}}
\date{{\today}}
\opening{{Dear Hiring Manager,}}
\closing{{Best regards,}}

\makelettertitle

I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my technical expertise and passion for scalable software solutions to your team.

In my current position, I have been leading infrastructure optimization projects and implementing cost-effective solutions, including migrating from Azure Kubernetes Service to local Kubernetes clusters. My experience spans the entire technology stack, from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core. I have successfully built microservices architectures, implemented RESTful APIs, and managed complex database integrations across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications at Synteda, has given me valuable experience in building scalable, enterprise-level applications. I have consistently delivered projects that improve system reliability and reduce operational costs.

Key highlights of my experience include:
• Leading infrastructure optimization and system integration projects
• Developing comprehensive talent management systems using modern cloud architectures  
• Implementing CI/CD pipelines and automated testing frameworks
• Managing complex network systems and providing technical solution design
• Working with diverse technology stacks including Java, C\#, Python, and JavaScript

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals, along with my practical experience in containerization and microservices, position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience in fullstack development and infrastructure optimization can contribute to {company}'s continued success. Thank you for considering my application.

\makeletterclosing

\end{{document}}"""
    
    return cl_template

def main():
    """Main function to generate PDFs"""
    print("🔨 Compiling proper LaTeX PDFs...")
    print("=" * 50)
    
    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
        print("✅ pdflatex found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pdflatex not found. Installing BasicTeX...")
        # Try to install if on macOS
        if os.system("which brew") == 0:
            os.system("brew install basictex")
        else:
            print("Please install LaTeX distribution manually")
            return
    
    # Generate CV
    print("\n📄 Generating CV...")
    cv_content = create_modern_cv_template()
    cv_pdf = compile_latex_to_pdf(cv_content, "hongzhi_cv", "devops")
    
    # Generate Cover Letter  
    print("\n📄 Generating Cover Letter...")
    cl_content = create_modern_cover_letter_template()
    cl_pdf = compile_latex_to_pdf(cl_content, "hongzhi_cover_letter", "devops")
    
    print("\n📊 Results:")
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
        print(f"\n🎉 Success! Ready to email PDFs with proper format")
        return True
    else:
        print(f"\n⚠️  Some PDFs failed to generate")
        return False

if __name__ == "__main__":
    main()