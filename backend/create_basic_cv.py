#!/usr/bin/env python3
"""
Create basic CV with minimal LaTeX dependencies
"""
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

def compile_latex_to_pdf(tex_content, output_name):
    """Compile LaTeX content to PDF using pdflatex"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / f"{output_name}.tex"
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        
        try:
            for i in range(2):
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', str(temp_path),
                    str(tex_file)
                ], capture_output=True, text=True, cwd=temp_path)
                
                if result.returncode != 0 and i == 1:
                    print(f"LaTeX compilation error:")
                    print(result.stdout[-300:])
                    return None
            
            pdf_file = temp_path / f"{output_name}.pdf"
            if pdf_file.exists():
                final_name = f"hongzhi_devops_cv.pdf"
                shutil.copy2(pdf_file, final_name)
                print(f"✅ CV PDF generated: {final_name}")
                return final_name
            else:
                return None
                
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return None

def create_basic_cv():
    """Create basic CV with minimal packages"""
    cv_template = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.8in]{geometry}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue,
    pdfauthor={Hongzhi Li},
    pdftitle={Hongzhi Li - Fullstack Developer CV}
}

\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\newcommand{\sectiontitle}[1]{
    \vspace{10pt}
    {\large\textbf{#1}}
    \vspace{5pt}
    \hrule
    \vspace{8pt}
}

\newcommand{\jobtitle}[4]{
    \textbf{#1} --- #2\\
    \textit{#3 --- #4}\\
}

\begin{document}

% Header
\begin{center}
{\huge \textbf{Hongzhi Li}}\\
\vspace{8pt}
{\Large Fullstack Developer}\\
\vspace{12pt}
\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} $\bullet$ 0728384299 $\bullet$ 
\href{https://linkedin.com/in/hongzhi-li}{LinkedIn} $\bullet$ 
\href{https://github.com/bluehawana}{GitHub}
\end{center}

\vspace{15pt}

\sectiontitle{Profile Summary}
Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Proven expertise in building scalable full-stack applications using Spring Boot, Angular/React frontend integration, and comprehensive database management across SQL and NoSQL platforms. Strong background in RESTful API development, microservices architecture, and end-to-end application development. Currently serving as IT/Infrastructure Specialist at ECARX, bringing deep technical knowledge to complex software solutions and collaborative development environments.

\sectiontitle{Core Technical Skills}
\textbf{Programming Languages:} Java/J2EE, JavaScript, C\#/.NET Core, Python, Bash, PowerShell

\textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3

\textbf{Backend Frameworks:} Spring, Spring Boot, Spring MVC, .NET Core, ASP.NET, Node.js

\textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture

\textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3

\textbf{Testing:} Unit Testing, Integration Testing, Automated Testing, JUnit, Jest

\textbf{Cloud Platforms:} AWS, Azure, GCP

\textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS)

\textbf{Version Control:} Git, GitHub, GitLab

\textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI

\textbf{Agile Methodologies:} Scrum, Kanban, Sprint Planning, Code Reviews

\sectiontitle{Professional Experience}

\jobtitle{ECARX}{IT/Infrastructure Specialist}{October 2024 - Present}{Gothenburg, Sweden}
$\bullet$ Leading infrastructure optimization and system integration projects for automotive technology solutions\\
$\bullet$ Providing IT support and infrastructure support to development teams for enhanced productivity\\
$\bullet$ Implementing cost optimization project by migrating from AKS to local Kubernetes cluster\\
$\bullet$ Implementing modern monitoring solutions using Grafana and advanced scripting\\
$\bullet$ Managing complex network systems and providing technical solution design

\jobtitle{Synteda}{Azure Fullstack Developer \& Integration Specialist (Freelance)}{August 2023 - September 2024}{Gothenburg, Sweden}
$\bullet$ Developed comprehensive talent management system using C\# and .NET Core\\
$\bullet$ Built complete office management platform from scratch, architecting both frontend and backend\\
$\bullet$ Implemented RESTful APIs and microservices for scalable application architecture\\
$\bullet$ Integrated SQL and NoSQL databases with optimized query performance

\jobtitle{IT-H\"ogskolan}{Backend Developer (Part-time)}{January 2023 - May 2023}{Gothenburg, Sweden}
$\bullet$ Migrated "Omstallningsstod.se" adult education platform using Spring Boot\\
$\bullet$ Developed RESTful APIs for frontend integration and implemented secure data handling\\
$\bullet$ Collaborated with UI/UX designers to ensure seamless frontend-backend integration\\
$\bullet$ Implemented automated tests as part of delivery process

\jobtitle{Senior Material (Europe) AB}{Platform Architect \& Project Coordinator}{January 2022 - December 2022}{Eskilstuna, Sweden}
$\bullet$ Led migration of business-critical applications with microservices architecture\\
$\bullet$ Developed backend services with Spring Boot and designed RESTful APIs\\
$\bullet$ Collaborated with development teams to optimize applications for maximum speed\\
$\bullet$ Participated in Agile ceremonies including sprint planning, reviews, and retrospectives

\jobtitle{AddCell (CTH Startup)}{DevOps Engineer}{September 2022 - November 2022}{Gothenburg, Sweden}
$\bullet$ Developed cloud-native applications using serverless computing architecture\\
$\bullet$ Implemented GraphQL APIs for efficient data fetching and frontend integration\\
$\bullet$ Worked with SQL and NoSQL databases for optimal data storage and retrieval

\jobtitle{Pembio AB}{Fullstack Developer}{October 2020 - September 2021}{Lund, Sweden}
$\bullet$ Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture\\
$\bullet$ Built frontend features using Vue.js framework and integrated with backend APIs\\
$\bullet$ Developed RESTful APIs and implemented comprehensive database integration\\
$\bullet$ Participated in Agile development processes and collaborated with cross-functional teams\\
$\bullet$ Implemented automated testing strategies and ensured application security

\sectiontitle{Hobby Projects}

\jobtitle{Gothenburg TaxiCarPooling Web Application}{Personal Project}{May 2025 - Present}{}
$\bullet$ Developing intelligent carpooling platform using Spring Boot backend and Node.js microservices\\
$\bullet$ Cross-platform mobile application with React Native, integrating payment and geolocation services\\
$\bullet$ Implemented automated order matching algorithm and RESTful APIs for real-time data processing\\
$\bullet$ Designed system with PostgreSQL database integration and optimized for scalability and performance\\
$\bullet$ Built comprehensive automated testing suite and ensured data protection compliance

\jobtitle{SmartTV \& VoiceBot - Android Auto Applications}{Personal Project}{March 2025 - Present}{}
$\bullet$ Developing Android Auto apps with Java backend services and modern frontend interfaces\\
$\bullet$ Implemented RESTful APIs for real-time data processing and voice command integration\\
$\bullet$ Built secure API integrations with SQL database optimization for vehicle data access\\
$\bullet$ Developed comprehensive testing framework for both frontend and backend components

\jobtitle{Hong Yan AB - E-commerce Platform (smrtmart.com)}{Personal Project}{April 2024 - Present}{}
$\bullet$ Fullstack e-commerce platform with Spring Boot backend and React frontend\\
$\bullet$ Implemented microservices architecture with PostgreSQL and MongoDB database integration\\
$\bullet$ Built comprehensive order management, inventory tracking, and payment processing systems\\
$\bullet$ Developed RESTful APIs for frontend-backend communication and third-party integrations\\
$\bullet$ Optimized application performance for maximum speed and scalability

\sectiontitle{Education}
\textbf{IT H\"ogskolan}\\
Bachelor's Degree in .NET Cloud Development --- 2021-2023, M\"olndal Campus\\
Bachelor's Degree in Java Integration --- 2019-2021

\textbf{University of Gothenburg}\\
Master's Degree in International Business and Trade --- 2016-2019

\sectiontitle{Certifications}
$\bullet$ AWS Certified Solutions Architect - Associate (Aug 2022)\\
$\bullet$ Microsoft Certified: Azure Fundamentals (Jun 2022)\\
$\bullet$ AWS Certified Developer - Associate (Nov 2022)

\sectiontitle{Additional Information}
\textbf{Languages:} Fluent in English and Mandarin\\
\textbf{Interests:} Vehicle technology, energy sector, electrical charging systems\\
\textbf{Website:} \href{https://bluehawana.com}{bluehawana.com}

\end{document}"""
    
    return cv_template

def main():
    print("🔨 Creating Basic CV PDF...")
    print("=" * 40)
    
    cv_content = create_basic_cv()
    cv_pdf = compile_latex_to_pdf(cv_content, "hongzhi_cv_basic")
    
    if cv_pdf:
        size = os.path.getsize(cv_pdf) / 1024
        print(f"   Size: {size:.1f} KB")
        return cv_pdf
    else:
        print("❌ CV generation failed")
        return None

if __name__ == "__main__":
    main()