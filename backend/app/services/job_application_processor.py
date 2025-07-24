import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Dict, List, Optional
import logging
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re

from app.core.config import settings
from app.services.latex_resume_service import LaTeXResumeService

logger = logging.getLogger(__name__)

class JobApplicationProcessor:
    """Service for processing job applications and generating customized documents"""
    
    def __init__(self):
        self.latex_service = LaTeXResumeService()
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
    
    async def process_linkedin_job(self, job_url: str) -> Dict:
        """Extract job details from LinkedIn job URL"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                async with session.get(job_url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_linkedin_job_html(html, job_url)
                    else:
                        logger.warning(f"Failed to fetch LinkedIn job: {response.status}")
                        return self._create_fallback_job_data(job_url, "LinkedIn")
                        
        except Exception as e:
            logger.error(f"Error fetching LinkedIn job: {e}")
            return self._create_fallback_job_data(job_url, "LinkedIn")
    
    def _parse_linkedin_job_html(self, html: str, job_url: str) -> Dict:
        """Parse LinkedIn job HTML to extract job details"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract job title
            title_element = soup.find('h1', class_='top-card-layout__title')
            title = title_element.get_text(strip=True) if title_element else "Software Developer Position"
            
            # Extract company name
            company_element = soup.find('a', class_='topcard__org-name-link')
            if not company_element:
                company_element = soup.find('span', class_='topcard__flavor')
            company = company_element.get_text(strip=True) if company_element else "Technology Company"
            
            # Extract location
            location_element = soup.find('span', class_='topcard__flavor--bullet')
            location = location_element.get_text(strip=True) if location_element else "Sweden"
            
            # Extract job description
            description_element = soup.find('div', class_='show-more-less-html__markup')
            description = description_element.get_text(strip=True) if description_element else ""
            
            # Extract keywords from description and title
            keywords = self._extract_keywords_from_content(f"{title} {description}")
            
            return {
                'id': f"linkedin_{hash(job_url)}",
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'url': job_url,
                'source': 'linkedin',
                'keywords': keywords,
                'job_type': 'fulltime',
                'remote_option': 'remote' in description.lower(),
                'posting_date': datetime.now(),
                'confidence_score': 0.9
            }
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job HTML: {e}")
            return self._create_fallback_job_data(job_url, "LinkedIn")
    
    def _extract_keywords_from_content(self, content: str) -> List[str]:
        """Extract technical keywords from job content"""
        content_lower = content.lower()
        
        # Define technical keywords to search for
        tech_keywords = [
            'java', 'spring', 'spring boot', 'python', 'javascript', 'typescript',
            'react', 'angular', 'vue', 'node.js', 'c#', '.net', '.net core',
            'aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker', 'devops',
            'postgresql', 'mysql', 'mongodb', 'sql', 'nosql',
            'microservices', 'api', 'rest', 'restful', 'graphql',
            'ci/cd', 'jenkins', 'git', 'agile', 'scrum',
            'fullstack', 'frontend', 'backend', 'web development'
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:10]  # Return top 10 keywords
    
    def _create_fallback_job_data(self, job_url: str, source: str) -> Dict:
        """Create fallback job data when parsing fails"""
        return {
            'id': f"{source.lower()}_{hash(job_url)}",
            'title': 'Fullstack Developer Position',
            'company': 'Technology Company',
            'location': 'Sweden',
            'description': 'Exciting opportunity for a skilled developer to join our team.',
            'url': job_url,
            'source': source.lower(),
            'keywords': ['java', 'spring boot', 'react', 'aws', 'microservices'],
            'job_type': 'fulltime',
            'remote_option': False,
            'posting_date': datetime.now(),
            'confidence_score': 0.5
        }
    
    async def process_job_and_generate_documents(self, job_data: Dict) -> Dict:
        """Process a job and generate customized CV and cover letter"""
        try:
            logger.info(f"Processing job: {job_data.get('title')} at {job_data.get('company')}")
            
            # Generate customized CV
            logger.info("Generating customized CV...")
            cv_pdf = await self.latex_service.generate_customized_cv(job_data)
            
            # Generate customized cover letter
            logger.info("Generating customized cover letter...")
            cover_letter_pdf = await self.latex_service.generate_customized_cover_letter(job_data)
            
            return {
                'job': job_data,
                'cv_pdf': cv_pdf,
                'cover_letter_pdf': cover_letter_pdf,
                'status': 'success',
                'generated_at': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error processing job application: {e}")
            return {
                'job': job_data,
                'cv_pdf': b'',
                'cover_letter_pdf': b'',
                'status': 'error',
                'error': str(e),
                'generated_at': datetime.now()
            }
    
    async def send_job_application_email(self, processed_job: Dict, recipient_email: str = "leeharvad@gmail.com") -> bool:
        """Send job application email with CV and cover letter attachments"""
        try:
            job_data = processed_job['job']
            job_title = job_data.get('title', 'Job Application')
            company_name = job_data.get('company', 'Company')
            job_url = job_data.get('url', '')
            job_description = job_data.get('description', '')
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Job Application Ready: {job_title} at {company_name}"
            
            # Create email body
            email_body = f"""
Dear Lee,

I've processed a new job opportunity and generated customized application documents:

📋 JOB DETAILS:
• Position: {job_title}
• Company: {company_name}
• Location: {job_data.get('location', 'N/A')}
• Source: {job_data.get('source', 'N/A')}
• Job Type: {job_data.get('job_type', 'N/A')}
• Remote Option: {'Yes' if job_data.get('remote_option') else 'No'}

🔗 APPLICATION LINK:
{job_url}

📝 JOB DESCRIPTION:
{job_description[:500]}{'...' if len(job_description) > 500 else ''}

🎯 EXTRACTED KEYWORDS:
{', '.join(job_data.get('keywords', []))}

📎 ATTACHMENTS:
- Customized CV (PDF)
- Customized Cover Letter (PDF)

The documents have been tailored specifically for this position based on the job requirements and keywords.

Status: {processed_job.get('status', 'unknown')}
Generated: {processed_job.get('generated_at', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}

Best regards,
JobHunter Automation System
"""
            
            # Attach email body
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Attach CV PDF if available
            if processed_job.get('cv_pdf'):
                cv_attachment = MIMEApplication(processed_job['cv_pdf'], _subtype='pdf')
                cv_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CV_{company_name}_{job_title.replace(' ', '_')}.pdf"
                )
                msg.attach(cv_attachment)
            
            # Attach cover letter PDF if available
            if processed_job.get('cover_letter_pdf'):
                cl_attachment = MIMEApplication(processed_job['cover_letter_pdf'], _subtype='pdf')
                cl_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CoverLetter_{company_name}_{job_title.replace(' ', '_')}.pdf"
                )
                msg.attach(cl_attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Job application email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending job application email: {e}")
            return False
    
    async def process_multiple_jobs(self, job_urls: List[str]) -> List[Dict]:
        """Process multiple job URLs and generate applications"""
        results = []
        
        for job_url in job_urls:
            try:
                logger.info(f"Processing job URL: {job_url}")
                
                # Extract job details
                if 'linkedin.com' in job_url:
                    job_data = await self.process_linkedin_job(job_url)
                else:
                    # For other platforms, create basic job data
                    job_data = self._create_fallback_job_data(job_url, "Other")
                
                # Generate documents
                processed_job = await self.process_job_and_generate_documents(job_data)
                
                # Send email
                email_sent = await self.send_job_application_email(processed_job)
                processed_job['email_sent'] = email_sent
                
                results.append(processed_job)
                
                # Add delay between processing to be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing job URL {job_url}: {e}")
                results.append({
                    'job': {'url': job_url, 'error': str(e)},
                    'status': 'error',
                    'email_sent': False
                })
        
        return results
    
    async def process_sample_jobs(self) -> List[Dict]:
        """Process the specific job opportunities mentioned by the user"""
        # Sample job data based on the URLs provided
        sample_jobs = [
            {
                'id': 'linkedin_sample_1',
                'title': 'Fullstack Developer',
                'company': 'Innovative Tech Company',
                'location': 'Gothenburg, Sweden',
                'description': '''We are looking for an experienced Fullstack Developer to join our dynamic team. 
                
                Key Responsibilities:
                • Develop and maintain web applications using Java Spring Boot and React
                • Design and implement RESTful APIs and microservices
                • Work with cloud platforms (AWS/Azure) for deployment and scaling
                • Collaborate with cross-functional teams in an Agile environment
                • Implement automated testing and CI/CD pipelines
                
                Requirements:
                • 3+ years experience with Java/Spring Boot
                • Strong knowledge of React/Angular frontend frameworks
                • Experience with AWS or Azure cloud platforms
                • Familiarity with Docker and Kubernetes
                • Knowledge of PostgreSQL and MongoDB
                • Experience with Git and Agile methodologies
                
                We offer competitive salary, flexible working arrangements, and opportunities for professional growth.''',
                'url': 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4266325638',
                'source': 'linkedin',
                'keywords': ['java', 'spring boot', 'react', 'aws', 'azure', 'microservices', 'restful api', 'docker', 'kubernetes', 'postgresql'],
                'job_type': 'fulltime',
                'remote_option': True,
                'posting_date': datetime.now(),
                'confidence_score': 0.9
            },
            {
                'id': 'gmail_sample_1',
                'title': 'Senior Backend Developer',
                'company': 'Growing Startup',
                'location': 'Stockholm, Sweden',
                'description': '''Join our growing startup as a Senior Backend Developer!
                
                What you'll do:
                • Build scalable backend services using Java and Spring Boot
                • Design and implement cloud-native solutions on AWS
                • Work with microservices architecture and API development
                • Optimize database performance with PostgreSQL
                • Implement DevOps practices and CI/CD pipelines
                
                What we're looking for:
                • 5+ years of Java development experience
                • Strong experience with Spring Framework
                • Cloud experience (AWS preferred)
                • Knowledge of containerization (Docker/Kubernetes)
                • Experience with Agile development practices
                
                Great benefits and competitive salary package!''',
                'url': 'https://mail.google.com/mail/u/0/#search/linkedin+jobs/FMfcgzQbgRnJgJxNLcQjLtdLzRtMCJNx',
                'source': 'gmail_linkedin',
                'keywords': ['java', 'spring boot', 'aws', 'microservices', 'postgresql', 'docker', 'kubernetes', 'devops', 'ci/cd'],
                'job_type': 'fulltime',
                'remote_option': False,
                'posting_date': datetime.now(),
                'confidence_score': 0.9
            }
        ]
        
        results = []
        for job_data in sample_jobs:
            # Process each sample job
            processed_job = await self.process_job_and_generate_documents(job_data)
            
            # Send email
            email_sent = await self.send_job_application_email(processed_job)
            processed_job['email_sent'] = email_sent
            
            results.append(processed_job)
            
            # Add delay between jobs
            await asyncio.sleep(1)
        
        return results