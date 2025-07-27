#!/usr/bin/env python3
"""
Simple PDF generation using basic LaTeX article class
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
                    print(result.stdout[-500:])  # Last 500 chars
                    if i == 1:  # Only fail on second pass
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
            print("❌ pdflatex not found. Please install LaTeX distribution")
            return None
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return None

def create_simple_cv_template(job_title="DevOps Engineer", company="Opera Software"):
    """
    Create simple CV template using article class
    """
    cv_template = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}

% Custom formatting
\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\bfseries}{}{0em}{}
\setlength{\parindent}{0pt}
\setlist{nosep}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue,
    pdfauthor={Hongzhi Li},
    pdftitle={Hongzhi Li - Fullstack Developer CV}
}

\begin{document}

% Header
\begin{center}
{\LARGE \textbf{Hongzhi Li}}\\
\vspace{5pt}
{\large Fullstack Developer}\\
\vspace{10pt}
\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} --- 0728384299 --- 
\href{https://linkedin.com/in/hongzhi-li}{LinkedIn} --- 
\href{https://github.com/bluehawana}{GitHub}
\end{center}

\vspace{20pt}

\section{Profile Summary}
Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Demonstrated ability to work across the entire technology stack from frontend user interfaces to backend services and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments.

\section{Core Technical Skills}
\textbf{Programming Languages:} Java/J2EE, JavaScript, C\#/.NET Core, Python, Bash, PowerShell\\
\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3\\
\textbf{Backend Frameworks:} Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js\\
\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture\\
\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3\\
\textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest\\
\textbf{Cloud Platforms:} AWS, Azure, GCP\\
\textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)\\
\textbf{Version Control:} Git, GitHub, GitLab\\
\textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI\\
\textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews\\
\textbf{Performance Optimization:} Application scaling, Database optimization, Caching strategies\\
\textbf{Security:} Application security, Data protection, Authentication/Authorization

\section{Professional Experience}

\subsection{ECARX --- IT/Infrastructure Specialist}
\textit{October 2024 - Present --- Gothenburg, Sweden}
\begin{itemize}
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses
\item Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\end{itemize}

\subsection{Synteda --- Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 --- Gothenburg, Sweden}
\begin{itemize}
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting both frontend and backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

\subsection{IT-Högskolan --- Backend Developer (Part-time)}
\textit{January 2023 - May 2023 --- Gothenburg, Sweden}
\begin{itemize}
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection{Senior Material (Europe) AB --- Platform Architect \& Project Coordinator}
\textit{January 2022 - December 2022 --- Eskilstuna, Sweden}
\begin{itemize}
\item Led migration of business-critical applications with microservices architecture
\item Developed backend services with Spring Boot and designed RESTful APIs for frontend consumption
\item Collaborated with development teams to optimize applications for maximum speed and scalability
\item Participated in Agile ceremonies including sprint planning, reviews, and retrospectives
\end{itemize}

\section{Education}
\textbf{IT Högskolan}\\
Bachelor's Degree in .NET Cloud Development --- 2021-2023, Mölndal Campus\\
Bachelor's Degree in Java Integration --- 2019-2021\\

\textbf{University of Gothenburg}\\
Master's Degree in International Business and Trade --- 2016-2019

\section{Certifications}
\begin{itemize}
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\end{itemize}

\section{Additional Information}
\textbf{Languages:} Fluent in English and Mandarin\\
\textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology\\
\textbf{Personal Website:} \href{https://bluehawana.com}{bluehawana.com}\\
\textbf{Customer Websites:} senior798.eu, mibo.se, omstallningsstod.se

\end{document}"""
    
    return cv_template

def create_simple_cover_letter_template(job_title="DevOps Engineer", company="Opera Software"):
    """
    Create simple cover letter template using article class
    """
    cl_template = rf"""\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}

\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue,
    pdfauthor={{Hongzhi Li}},
    pdftitle={{Hongzhi Li - Cover Letter}}
}}

\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{10pt}}

\begin{{document}}

% Header
\begin{{center}}
{{\LARGE \textbf{{Hongzhi Li}}}}\\
\vspace{{5pt}}
{{\large Fullstack Developer}}\\
\vspace{{10pt}}
\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} --- 0728384299 --- 
\href{{https://linkedin.com/in/hongzhi-li}}{{LinkedIn}} --- 
\href{{https://github.com/bluehawana}}{{GitHub}}
\end{{center}}

\vspace{{20pt}}

\today

{company} Hiring Team\\
{company}\\
Hiring Department

\vspace{{20pt}}

\textbf{{Subject: Application for {job_title} Position}}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With over 5 years of hands-on experience in fullstack development and my current role as IT/Infrastructure Specialist at ECARX, I am excited to bring my technical expertise and passion for scalable software solutions to your team.

In my current position, I have been leading infrastructure optimization projects and implementing cost-effective solutions, including migrating from Azure Kubernetes Service to local Kubernetes clusters. My experience spans the entire technology stack, from frontend frameworks like Angular and React to backend services using Spring Boot and .NET Core. I have successfully built microservices architectures, implemented RESTful APIs, and managed complex database integrations across SQL and NoSQL platforms.

What particularly excites me about {company} is your commitment to innovative technology solutions. My background in automotive technology at ECARX, combined with my freelance work developing cloud-native applications at Synteda, has given me valuable experience in building scalable, enterprise-level applications. I have consistently delivered projects that improve system reliability and reduce operational costs.

\textbf{{Key highlights of my experience include:}}
\begin{{itemize}}
\item Leading infrastructure optimization and system integration projects
\item Developing comprehensive talent management systems using modern cloud architectures  
\item Implementing CI/CD pipelines and automated testing frameworks
\item Managing complex network systems and providing technical solution design
\item Working with diverse technology stacks including Java, C\#, Python, and JavaScript
\end{{itemize}}

I am particularly drawn to opportunities where I can combine my technical skills with my experience in agile methodologies and cross-functional collaboration. My certifications in AWS Solutions Architecture and Azure Fundamentals, along with my practical experience in containerization and microservices, position me well to contribute immediately to your development initiatives.

I would welcome the opportunity to discuss how my experience in fullstack development and infrastructure optimization can contribute to {company}'s continued success. Thank you for considering my application.

\vspace{{20pt}}

Best regards,

Hongzhi Li

\end{{document}}"""
    
    return cl_template

def main():
    """Main function to generate PDFs"""
    print("🔨 Compiling Simple LaTeX PDFs...")
    print("=" * 50)
    
    # Generate CV
    print("\n📄 Generating CV...")
    cv_content = create_simple_cv_template()
    cv_pdf = compile_latex_to_pdf(cv_content, "hongzhi_cv", "devops")
    
    # Generate Cover Letter  
    print("\n📄 Generating Cover Letter...")
    cl_content = create_simple_cover_letter_template()
    cl_pdf = compile_latex_to_pdf(cl_content, "hongzhi_cover_letter", "devops")
    
    print("\n📊 Results:")
    print("=" * 30)
    if cv_pdf:
        print(f"✅ CV: {cv_pdf}")
        # Check file size
        size = os.path.getsize(cv_pdf) / 1024
        print(f"   Size: {size:.1f} KB")
    else:
        print("❌ CV generation failed")
        
    if cl_pdf:
        print(f"✅ Cover Letter: {cl_pdf}")
        # Check file size
        size = os.path.getsize(cl_pdf) / 1024
        print(f"   Size: {size:.1f} KB")
    else:
        print("❌ Cover Letter generation failed")
    
    if cv_pdf and cl_pdf:
        print(f"\n🎉 Success! Ready to email PDFs with proper format")
        return [cv_pdf, cl_pdf]
    else:
        print(f"\n⚠️  Some PDFs failed to generate")
        return []

if __name__ == "__main__":
    main()