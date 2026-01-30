#!/usr/bin/env python3
"""
Overleaf PDF Generator - Uses Overleaf's API for perfect LaTeX compilation
Upload LaTeX to temporary URL and let Overleaf compile it for us!
"""
import os
import tempfile
import logging
from typing import Dict, Any
import time

# Optional imports - only use if available
try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

logger = logging.getLogger(__name__)


class OverleafPDFGenerator:
    def __init__(self):
        # Cloudflare R2 credentials (if available)
        self.r2_access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.r2_secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.r2_bucket = os.getenv('R2_BUCKET_NAME', 'latex-temp-files')
        self.r2_endpoint = os.getenv('R2_ENDPOINT_URL')

        # Initialize R2 client if credentials and boto3 available
        self.r2_client = None
        if HAS_BOTO3 and all([self.r2_access_key, self.r2_secret_key, self.r2_endpoint]):
            self.r2_client = boto3.client(
                's3',
                endpoint_url=self.r2_endpoint,
                aws_access_key_id=self.r2_access_key,
                aws_secret_access_key=self.r2_secret_key,
                region_name='auto'
            )

    def upload_to_r2(self, latex_content: str, filename: str) -> str:
        """Upload LaTeX content to Cloudflare R2 and return public URL"""
        try:
            if not self.r2_client:
                logger.warning(
                    "R2 credentials not configured, falling back to local compilation")
                return None

            # Upload to R2
            self.r2_client.put_object(
                Bucket=self.r2_bucket,
                Key=filename,
                Body=latex_content.encode('utf-8'),
                ContentType='text/plain'
            )

            # Return public URL
            public_url = f"https://{self.r2_bucket}.{self.r2_endpoint.replace('https://', '')}/{filename}"
            logger.info(f"✅ Uploaded LaTeX to R2: {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"❌ Failed to upload to R2: {e}")
            return None

    def create_overleaf_pdf(self, job: Dict[str, Any], latex_content: str = "") -> bytes:
        """Generate PDF using Overleaf's compilation service"""
        try:
            # Generate LaTeX content with LEGO intelligence
            latex_template = self._generate_latex_content(job)

            # Create unique filename
            timestamp = int(time.time())
            filename = f"resume_{timestamp}.tex"

            # Try to upload to R2 first
            public_url = self.upload_to_r2(latex_template, filename)

            if public_url:
                # Use Overleaf API with public URL
                overleaf_url = f"https://www.overleaf.com/docs?snip_uri={public_url}"
                logger.info(f"🚀 Overleaf compilation URL: {overleaf_url}")

                # Unfortunately, Overleaf doesn't provide direct PDF download API
                # But we can provide the URL for manual compilation
                # For automation, we'll fall back to local compilation
                logger.info(
                    "📝 Overleaf URL generated - falling back to local compilation for automation")

                # Clean up R2 file after a delay (optional)
                # self._schedule_cleanup(filename)

            # Fall back to local LaTeX compilation
            return self._compile_latex_locally(latex_template)

        except Exception as e:
            logger.error(f"❌ Error in Overleaf PDF generation: {e}")
            return b""

    def _generate_latex_content(self, job: Dict[str, Any]) -> str:
        """Generate LaTeX content with LEGO intelligence"""
        # Your exact LaTeX template
        latex_content = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{hyperref}

% Page setup
\geometry{margin=0.75in}
\pagestyle{empty}

% Color definitions
\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{lightgray}{RGB}{128,128,128}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}

% Simple default section formatting (ATS-friendly)

% Custom commands
\newcommand{\contactitem}[2]{\textcolor{darkblue}{#1} #2}
% ATS-friendly bullets and margins
\setlist[itemize]{label=-, leftmargin=*}

\begin{document}
\pagestyle{empty} % no page number

% Name and contact details
\begin{center}
{\LARGE \textbf{Hongzhi Li}}\\[10pt]
{\Large \textit{ROLE_TITLE_PLACEHOLDER}}\\[10pt]
\textcolor{darkblue}{\href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} | \href{tel:0728384299}{0728384299} | \href{https://www.linkedin.com/in/hzl/}{LinkedIn} | \href{https://github.com/bluehawana}{GitHub}}
\\[6pt]
Phone: +46 728 384 299 | Email: hongzhili01@gmail.com | Location: Gothenburg, Sweden | LinkedIn: linkedin.com/in/hzl | GitHub: github.com/bluehawana
\end{center}

% Personal Profile
\section*{Profile Summary}
PROFILE_SUMMARY_PLACEHOLDER

% Areas of Expertise
\section*{Core Technical Skills}
\begin{itemize}[noitemsep]
SKILLS_PLACEHOLDER
\end{itemize}

% Experience
\section*{Professional Experience}

\subsection*{ECARX | IT/Infrastructure Specialist}
\textit{October 2024 - Present | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Leading infrastructure optimization and system integration projects for automotive technology solutions
\item Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses by 40\%
\item Deployed comprehensive monitoring stack using Prometheus and Grafana to observe high-performance local cluster servers, tracking CPU usage, I/O performance, memory utilization, and network throughput
\item Conducted detailed performance analysis comparing on-premises GitLab runner environment with Azure Kubernetes Service (AKS), identifying 25\% performance improvement in CI/CD pipeline execution times
\item Implemented advanced Grafana dashboards for real-time infrastructure observability, enabling proactive issue detection and system optimization
\item Managing complex network systems and providing technical solution design for enterprise-level applications
\item Providing IT support and infrastructure support to development teams for enhanced productivity
\end{itemize}

\subsection*{Synteda | Azure Fullstack Developer \& Integration Specialist (Freelance)}
\textit{August 2023 - September 2024 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Developed comprehensive talent management system using C\# and .NET Core with cloud-native architecture
\item Built complete office management platform from scratch, architecting both frontend and backend components
\item Implemented RESTful APIs and microservices for scalable application architecture
\item Integrated SQL and NoSQL databases with optimized query performance and data protection measures
\end{itemize}

ADDITIONAL_EXPERIENCE_PLACEHOLDER

\section*{Hobby Projects}
PROJECTS_PLACEHOLDER

\section*{Education}
\textbf{IT Högskolan}\\
\textit{Bachelor's Degree in .NET Cloud Development} | 2021-2023\\
\textbf{Mölndal Campus}\\
\textit{Bachelor's Degree in Java Integration} | 2019-2021\\
\textbf{University of Gothenburg}\\
\textit{Master's Degree in International Business and Trade} | 2016-2019\\

\section*{Certifications}
\begin{itemize}
\item AWS Certified Solutions Architect - Associate (Aug 2022)
\item Microsoft Certified: Azure Fundamentals (Jun 2022)
\item AWS Certified Developer - Associate (Nov 2022)
\end{itemize}

\section*{Additional Information}
\begin{itemize}
\item \textbf{Languages:} Fluent in English and Mandarin
\item \textbf{Interests:} Vehicle technology, energy sector, electrical charging systems, and battery technology
\item \textbf{Personal Website:} \href{https://www.bluehawana.com}{bluehawana.com}
\item \textbf{Customer Websites:} \href{https://www.senior798.eu}{senior798.eu}, \href{https://www.mibo.se}{mibo.se}, \href{https://www.omstallningsstod.se}{omstallningsstod.se}
\end{itemize}

\end{document}
"""

        # LEGO intelligence - same as before
        job_title = job.get('title', '').lower()
        job_description = job.get('description', '').lower()
        company = job.get('company', 'Company')

        # Determine role focus
        is_devops = any(keyword in job_title + job_description for keyword in
                        ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
        is_backend = any(keyword in job_title + job_description for keyword in
                         ['backend', 'api', 'microservices', 'spring', 'java', 'database']) and not is_devops

        # Extract accurate company information first (optional)
        try:
            from company_info_extractor import CompanyInfoExtractor

            extractor = CompanyInfoExtractor()
            company_result = extractor.extract_and_validate_company_info(job)

            if company_result['success']:
                accurate_company_name = company_result['company_info']['company_name']
                logger.info(
                    f"✅ Using accurate company name: {accurate_company_name}")
            else:
                accurate_company_name = company
                logger.warning(
                    f"⚠️ Using fallback company name: {accurate_company_name}")
        except Exception as e:
            logger.warning(f"⚠️ Company extraction skipped: {e}")
            accurate_company_name = company

        # LEGO role positioning
        if is_devops:
            role_title = "DevOps Engineer \\& Cloud Infrastructure Specialist"
            profile_summary = f"""Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Kubernetes, AWS, Docker, and infrastructure automation. Specialized in infrastructure optimization roles for companies like {accurate_company_name}."""

            skills = [
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud ECS, Infrastructure as Code",
                r"\item \textbf{Containerization:} Docker, Kubernetes, Azure Kubernetes Service (AKS), Container Orchestration",
                r"\item \textbf{CI/CD:} Jenkins, GitHub Actions, GitLab CI, Automated Testing, Deployment Pipelines",
                r"\item \textbf{Infrastructure:} System Integration, Network Management, Cost Optimization, Performance Monitoring",
                r"\item \textbf{Monitoring \& Observability:} Prometheus, Grafana, Advanced Scripting, System Reliability, Performance Analysis, Infrastructure Metrics, GitLab Runner Optimization",
                r"\item \textbf{Programming:} Python, Bash, PowerShell, Java, JavaScript, Go, Infrastructure Automation",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, Database Optimization",
                r"\item \textbf{Security:} Application security, Data protection, Authentication/Authorization, Network Security"
            ]
        elif is_backend:
            role_title = "Backend Developer \\& API Specialist"
            profile_summary = f"""Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, RESTful APIs, and scalable backend systems. Specialized in backend development roles for companies like {accurate_company_name}."""

            skills = [
                r"\item \textbf{Programming Languages:} Java/J2EE, C\#/.NET Core, Python, JavaScript, TypeScript, Go",
                r"\item \textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI, Express.js",
                r"\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture, API Gateway",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, Database Design",
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud, Serverless Computing",
                r"\item \textbf{Performance:} Database optimization, Caching strategies, Application scaling, Load Balancing",
                r"\item \textbf{Security:} Application security, Data protection, Authentication/Authorization, OAuth",
                r"\item \textbf{DevOps:} Docker, Kubernetes, Jenkins, GitHub Actions, CI/CD Pipelines"
            ]
        else:
            role_title = "Senior Fullstack Developer"
            profile_summary = f"""Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Specialized in end-to-end development roles for companies like {accurate_company_name}."""

            skills = [
                r"\item \textbf{Programming Languages:} Java/J2EE, JavaScript, C\#/.NET Core, Python, TypeScript, Bash",
                r"\item \textbf{Frontend Frameworks:} Angular, ReactJS, React Native, Vue.js, HTML5, CSS3",
                r"\item \textbf{Backend Frameworks:} Spring Boot, Spring MVC, .NET Core, Node.js, ASP.NET",
                r"\item \textbf{API Development:} RESTful APIs, GraphQL, Microservices Architecture",
                r"\item \textbf{Databases:} PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB, S3",
                r"\item \textbf{Cloud Platforms:} AWS, Azure, GCP, Alibaba Cloud",
                r"\item \textbf{DevOps:} Docker, Kubernetes, Jenkins, GitHub Actions, GitLab CI",
                r"\item \textbf{Methodologies:} Agile, Scrum, Kanban, Sprint Planning, Code Reviews"
            ]

        # Additional experience and projects (same as before)
        additional_experience = r"""
\subsection*{IT-Högskolan | Backend Developer (Part-time)}
\textit{January 2023 - May 2023 | Gothenburg, Sweden}
\begin{itemize}[noitemsep]
\item Migrated "Omstallningsstod.se" adult education platform using Spring Boot backend services
\item Developed RESTful APIs for frontend integration and implemented secure data handling
\item Collaborated with UI/UX designers to ensure seamless frontend-backend integration
\item Implemented automated tests as part of delivery process
\end{itemize}

\subsection*{Pembio AB | Fullstack Developer}
\textit{October 2020 - September 2021 | Lund, Sweden}
\begin{itemize}[noitemsep]
\item Developed Pembio.com platform backend with Java and Spring Boot in microservices architecture
\item Built frontend features using Vue.js framework and integrated with backend APIs
\item Developed RESTful APIs and implemented comprehensive database integration
\item Participated in Agile development processes and collaborated with cross-functional teams
\end{itemize}
"""

        projects = r"""
\subsection{Weather\_Anywhere.CLOUD\_API\_Encoding}
\textit{Feb 2024 -- Present} \\
\textbf{SpringBoot, AlibabaCloudECS, ApsaraDBRDS(MySQL), Heroku}
\begin{itemize}
\item Weather tracking app for Swedish and global cities using OpenCageData and Open-Meteo APIs
\item Deployed on Alibaba Cloud ECS with city coordinates and weather data stored in ApsaraDB MySQL
\item Demo: https://weather.bluehawana.com
\end{itemize}

\subsection{Jobhunter\_Python\_TypeScript\_RESTAPI}
\textit{July 2024 -- Present} \\
\textbf{Python, TypeScript, GmailRESTAPI, LinkedinAPI}
\begin{itemize}
\item Automated job hunting pipeline integrating Gmail search, job scraping, and resume customization
\item Generated resumes and cover letters based on job descriptions using NLP techniques
\item Demo: https://jobs.bluehawana.com
\end{itemize}
"""

        # Replace placeholders
        latex_content = latex_content.replace(
            "ROLE_TITLE_PLACEHOLDER", role_title)
        latex_content = latex_content.replace(
            "PROFILE_SUMMARY_PLACEHOLDER", profile_summary)
        latex_content = latex_content.replace(
            "SKILLS_PLACEHOLDER", "\n".join(skills))
        latex_content = latex_content.replace(
            "ADDITIONAL_EXPERIENCE_PLACEHOLDER", additional_experience)
        latex_content = latex_content.replace("PROJECTS_PLACEHOLDER", projects)

        return latex_content

    def _compile_latex_locally(self, latex_content: str) -> bytes:
        """Fallback: compile LaTeX locally using pdflatex"""
        try:
            import subprocess

            with tempfile.TemporaryDirectory() as temp_dir:
                tex_file = os.path.join(temp_dir, "resume.tex")
                pdf_file = os.path.join(temp_dir, "resume.pdf")

                # Write LaTeX content
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)

                # Compile LaTeX (run twice for references)
                for _ in range(2):
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode',
                            '-output-directory', temp_dir, tex_file],
                        capture_output=True, text=True
                    )

                    if result.returncode != 0:
                        logger.error(
                            f"LaTeX compilation failed: {result.stderr}")
                        return b""

                # Read PDF
                if os.path.exists(pdf_file):
                    with open(pdf_file, 'rb') as f:
                        return f.read()

        except Exception as e:
            logger.error(f"❌ Local LaTeX compilation failed: {e}")
            return b""

# Convenience function for backward compatibility


def create_overleaf_pdf(job: Dict[str, Any], latex_content: str = "") -> bytes:
    """Create PDF using Overleaf API or local compilation"""
    generator = OverleafPDFGenerator()
    return generator.create_overleaf_pdf(job, latex_content)


if __name__ == "__main__":
    # Test the Overleaf PDF generator
    test_job = {
        'title': 'Senior DevOps Engineer',
        'company': 'Spotify',
        'description': 'Kubernetes, AWS, Docker, infrastructure automation, CI/CD pipelines, monitoring'
    }

    generator = OverleafPDFGenerator()
    pdf_content = generator.create_overleaf_pdf(test_job)

    if pdf_content:
        with open('test_overleaf_resume.pdf', 'wb') as f:
            f.write(pdf_content)
        print(f"✅ Generated Overleaf-quality resume: {len(pdf_content)} bytes")
    else:
        print("❌ Failed to generate PDF")
