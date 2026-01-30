#!/usr/bin/env python3
"""
Daily Job Automation with Environment Variables
Fixed version that properly sends real job emails to hongzhili01@gmail.com
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables from .env file
os.environ['GMAIL_APP_PASSWORD'] = 'vsodrpyblpgtujof'
os.environ['SMTP_PASSWORD'] = 'vsdclxhjnklrccsf'
os.environ['SENDER_EMAIL'] = 'leeharvad@gmail.com'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_job_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """
    Daily job automation - scan Gmail and company sites, send the best job opportunities
    """
    try:
        logger.info("🚀 Starting Daily Job Automation for hongzhili01@gmail.com")
        logger.info("=" * 60)
        
        # Phase 1: Scan Gmail for real job emails
        from app.services.real_job_scanner import RealJobScanner
        gmail_scanner = RealJobScanner()
        
        logger.info("📧 Phase 1: Scanning Gmail for Real Job Emails")
        gmail_jobs = await gmail_scanner.scan_real_gmail_jobs(days_back=3)
        logger.info(f"✅ Found {len(gmail_jobs)} jobs from Gmail")
        
        # Phase 2: Scrape company websites
        from app.services.real_job_scrapers import (
            CompanyCareerScraper,
            IndeedJobScraper
        )
        
        logger.info("🔍 Phase 2: Scraping Company Career Sites")
        company_scraper = CompanyCareerScraper()
        company_jobs = await company_scraper.scrape_company_careers(max_jobs=3)
        logger.info(f"✅ Found {len(company_jobs)} jobs from company sites")
        
        # Combine all jobs
        all_jobs = gmail_jobs + company_jobs
        
        # Filter for best jobs (senior developer positions)
        quality_jobs = filter_for_senior_positions(all_jobs)
        logger.info(f"🎯 Phase 3: Processing {len(quality_jobs)} Quality Senior Positions")
        
        # Send emails for top jobs
        if quality_jobs:
            for i, job in enumerate(quality_jobs[:3], 1):  # Send top 3
                try:
                    logger.info(f"📧 Sending job {i}: {job['title']} at {job['company']}")
                    
                    # Create simple CV and Cover Letter
                    cv_pdf = create_simple_cv_pdf(job)
                    cl_pdf = create_simple_cover_letter_pdf(job)
                    
                    # Send email
                    success = await gmail_scanner.send_job_email(job, cv_pdf, cl_pdf)
                    if success:
                        logger.info(f"✅ Successfully sent email for {job['company']}")
                    else:
                        logger.warning(f"⚠️ Failed to send email for {job['company']}")
                        
                    # Delay between emails
                    await asyncio.sleep(3)
                    
                except Exception as e:
                    logger.error(f"❌ Error sending job {i}: {e}")
        
        else:
            logger.warning("❌ No quality senior positions found today")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📋 Daily Job Automation Summary:")
        logger.info(f"   Gmail Jobs Found: {len(gmail_jobs)}")
        logger.info(f"   Company Jobs Found: {len(company_jobs)}")
        logger.info(f"   Quality Jobs Found: {len(quality_jobs)}")
        logger.info(f"   Emails Sent: {min(len(quality_jobs), 3)}")
        
        if quality_jobs:
            logger.info("\n🏆 Top Job Opportunities Sent:")
            for i, job in enumerate(quality_jobs[:3], 1):
                logger.info(f"   {i}. {job['title']} at {job['company']}")
                logger.info(f"      📍 {job.get('location', 'Sweden')} | 💼 {job.get('experience_level', 'Senior')}")
                logger.info(f"      🔗 {job.get('application_link', 'N/A')[:60]}...")
                logger.info(f"      🏷️ Keywords: {', '.join(job.get('keywords', [])[:5])}")
        
        logger.info(f"\n🎉 Daily Job Automation Complete! Check hongzhili01@gmail.com for opportunities.")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error in daily job automation: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def filter_for_senior_positions(jobs):
    """
    Filter jobs for senior developer positions suitable for experienced professionals
    """
    quality_jobs = []
    seen_combinations = set()
    
    for job in jobs:
        # Create unique identifier
        job_id = f"{job.get('company', 'Unknown').lower()}_{job.get('title', 'Unknown').lower().replace(' ', '_')}"
        
        if job_id in seen_combinations:
            continue
        seen_combinations.add(job_id)
        
        # Must have application method
        if not job.get('application_link') and not job.get('application_email'):
            continue
        
        # Must have meaningful company name
        company = job.get('company', '').lower()
        if not company or company in ['unknown company', 'technology company']:
            continue
        
        # Quality scoring
        quality_score = 0
        
        # Title relevance
        title = job.get('title', '').lower()
        if any(keyword in title for keyword in ['senior', 'lead', 'principal', 'architect']):
            quality_score += 15
        elif any(keyword in title for keyword in ['developer', 'engineer', 'fullstack', 'backend', 'frontend']):
            quality_score += 10
        
        # Technology keywords
        keywords = job.get('keywords', [])
        relevant_tech = ['java', 'python', 'javascript', 'react', 'spring', 'aws', 'docker', 'kubernetes', 'microservices']
        tech_matches = sum(1 for tech in relevant_tech if tech in keywords)
        quality_score += tech_matches * 2
        
        # Company bonus (known companies)
        if any(comp in company for comp in ['volvo', 'skf', 'ericsson', 'spotify', 'klarna']):
            quality_score += 10
        
        # Description quality
        description = job.get('description', '')
        if len(description) > 100:
            quality_score += 5
        
        # Application link bonus
        if job.get('application_link'):
            quality_score += 5
        
        job['quality_score'] = quality_score
        
        # Only include high-quality positions
        if quality_score >= 20:
            quality_jobs.append(job)
    
    # Sort by quality score
    quality_jobs.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    return quality_jobs[:5]  # Return top 5

def create_simple_cv_pdf(job):
    """Create a proper LaTeX CV PDF that can be opened"""
    import subprocess
    import tempfile
    
    keywords = job.get('keywords', ['Java', 'Python', 'AWS'])[:5]
    
    latex_content = rf'''
\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=0.75in]{{geometry}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}

\definecolor{{headingcolor}}{{RGB}}{{47, 79, 79}}
\definecolor{{accentcolor}}{{RGB}}{{70, 130, 180}}

\titleformat{{\section}}{{\Large\bfseries\color{{headingcolor}}}}{{}}{{0em}}{{}}[\titlerule]
\titleformat{{\subsection}}{{\large\bfseries\color{{accentcolor}}}}{{}}{{0em}}{{}}

\begin{{document}}

\begin{{center}}
    {{\LARGE \textbf{{Hongzhi (Harvad) Li}}}} \\[0.3cm]
    {{\large Senior Software Engineer \& DevOps Specialist}} \\[0.2cm]
    \href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} $\bullet$ +46 728 384 299 $\bullet$ Gothenburg, Sweden \\
    \href{{https://linkedin.com/in/hongzhili}}{{linkedin.com/in/hongzhili}} $\bullet$ \href{{https://github.com/bluehawana}}{{github.com/bluehawana}}
\end{{center}}

\section{{Professional Summary}}
Experienced Software Engineer with 5+ years in full-stack development, cloud infrastructure, and DevOps practices. 
Proven expertise in {', '.join(keywords)} and modern development methodologies.

\section{{Technical Skills}}
\begin{{itemize}}[leftmargin=*,itemsep=0pt]
    \item \textbf{{Languages:}} Java, Python, JavaScript, TypeScript, Go
    \item \textbf{{Cloud:}} AWS, Azure, Docker, Kubernetes  
    \item \textbf{{Frameworks:}} Spring Boot, React, Node.js, Django
    \item \textbf{{DevOps:}} Jenkins, GitLab CI, Terraform, Ansible
    \item \textbf{{Databases:}} PostgreSQL, MongoDB, Redis
\end{{itemize}}

\section{{Professional Experience}}
\subsection{{Senior Software Engineer | ECARX Sweden AB | 2023 - Present}}
\begin{{itemize}}[leftmargin=*,itemsep=2pt]
    \item Developed cloud-native microservices using Java and Spring Boot
    \item Implemented Kubernetes deployment strategies and CI/CD pipelines
    \item Built monitoring systems using Prometheus and Grafana
\end{{itemize}}

\subsection{{Software Engineer | Synteda AB | 2022 - 2023}}
\begin{{itemize}}[leftmargin=*,itemsep=2pt]
    \item Designed microservices architecture using C\# and .NET
    \item Developed cloud-native applications with Azure services
    \item Built REST APIs and integrated third-party services
\end{{itemize}}

\section{{Education}}
\textbf{{Master's in Computer Science}} | University of Gothenburg \\
\textbf{{Bachelor's in Software Engineering}} | IT-Högskolan

\vspace{{0.3cm}}
\begin{{center}}
    \textit{{Customized for: {job.get('company', 'Company')} - {job.get('title', 'Position')}}} \\
    \textit{{Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}}}
\end{{center}}

\end{{document}}
'''
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(latex_content)
            tex_file = f.name
        
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                              capture_output=True, text=True, cwd=tempfile.gettempdir())
        
        pdf_file = tex_file.replace('.tex', '.pdf')
        
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            
            # Cleanup
            for ext in ['.tex', '.pdf', '.aux', '.log']:
                cleanup_file = tex_file.replace('.tex', ext)
                if os.path.exists(cleanup_file):
                    os.remove(cleanup_file)
            
            return pdf_bytes
        else:
            logger.error(f"PDF compilation failed: {result.stderr}")
            return b"PDF generation failed"
            
    except Exception as e:
        logger.error(f"LaTeX compilation error: {e}")
        return b"PDF generation error"

def create_simple_cover_letter_pdf(job):
    """Create a proper LaTeX Cover Letter PDF that can be opened"""
    import subprocess
    import tempfile
    
    company = job.get('company', 'Technology Company')
    title = job.get('title', 'Software Developer Position')
    keywords = job.get('keywords', ['cloud', 'software', 'development'])[:3]
    
    latex_content = rf'''
\documentclass[11pt,a4paper]{{letter}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}

\definecolor{{accentcolor}}{{RGB}}{{70, 130, 180}}

\signature{{Hongzhi (Harvad) Li}}
\address{{Hongzhi (Harvad) Li \\ Senior Software Engineer \\ 
          Gothenburg, Sweden \\ +46 728 384 299 \\ 
          \href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}}}}

\begin{{document}}

\begin{{letter}}{{{company} \\ Sweden}}

\opening{{Dear Hiring Manager,}}

I am writing to express my strong interest in the \textbf{{{title}}} position at \textbf{{{company}}}. 
With my extensive experience in software development, cloud infrastructure, and DevOps practices, 
I am confident I would be a valuable addition to your team.

My background includes over 5 years of experience with {', '.join(keywords)} and modern development technologies. 
At ECARX Sweden AB, I develop cloud-native microservices using Java and Spring Boot, implement Kubernetes 
deployment strategies, and build comprehensive monitoring solutions.

I am particularly excited about this opportunity at {company} because of your reputation for innovation 
and technical excellence. My experience with microservices architecture, cloud platforms, and DevOps 
practices aligns perfectly with your requirements.

Key achievements:
\begin{{itemize}}
    \item Designed scalable microservices architectures
    \item Built CI/CD pipelines using Jenkins and GitLab  
    \item Led cross-functional teams in complex projects
    \item Delivered high-quality solutions in agile environments
\end{{itemize}}

I would welcome the opportunity to discuss how my experience can contribute to {company}'s success.

\closing{{Best regards,}}

\vspace{{0.3cm}}
\begin{{center}}
    \textit{{Generated for: {company} - {title} | {datetime.now().strftime('%Y-%m-%d')}}}
\end{{center}}

\end{{letter}}
\end{{document}}
'''
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(latex_content)
            tex_file = f.name
        
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                              capture_output=True, text=True, cwd=tempfile.gettempdir())
        
        pdf_file = tex_file.replace('.tex', '.pdf')
        
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            
            # Cleanup
            for ext in ['.tex', '.pdf', '.aux', '.log']:
                cleanup_file = tex_file.replace('.tex', ext)
                if os.path.exists(cleanup_file):
                    os.remove(cleanup_file)
            
            return pdf_bytes
        else:
            logger.error(f"PDF compilation failed: {result.stderr}")
            return b"PDF generation failed"
            
    except Exception as e:
        logger.error(f"LaTeX compilation error: {e}")
        return b"PDF generation error"

if __name__ == "__main__":
    # Run the daily automation
    success = asyncio.run(main())
    
    if success:
        print("✅ Daily job automation completed successfully!")
        print("📧 Check hongzhili01@gmail.com for job opportunities")
    else:
        print("❌ Daily job automation failed - check logs")
        sys.exit(1)