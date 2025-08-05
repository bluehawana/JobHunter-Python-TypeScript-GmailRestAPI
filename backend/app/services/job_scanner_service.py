import os
import logging
import asyncio
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import json

logger = logging.getLogger(__name__)

class JobScannerService:
    """
    Comprehensive job scanning service for Gmail and LinkedIn
    Sends personalized emails with CV/CL and direct application links
    """
    
    def __init__(self):
        # Email configuration
        self.gmail_user = "bluehawana@gmail.com"
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")  # Need app password for bluehawana@gmail.com
        self.sender_email = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        self.target_email = "hongzhili01@gmail.com"
        
        # Job search keywords
        self.job_keywords = [
            "fullstack developer", "full stack developer", "senior developer",
            "backend developer", "frontend developer", "software engineer",
            "devops engineer", "cloud engineer", "java developer", "react developer",
            "python developer", "javascript developer", "software developer"
        ]
        
        # Company blacklist (companies to avoid)
        self.company_blacklist = [
            "recruitment agency", "staffing", "consulting", "outsourcing"
        ]
        
        # Job sites pattern matching
        self.job_site_patterns = {
            "linkedin": r"linkedin\.com/jobs/view/(\d+)",
            "indeed": r"indeed\.com/viewjob\?jk=([a-zA-Z0-9]+)",
            "thelocal": r"thelocal\.se/jobs/[^/]+/(\d+)",
            "arbetsformedlingen": r"arbetsformedlingen\.se/jobb/annons/(\d+)",
            "glassdoor": r"glassdoor\.com/job-listing/[^/]+/JV_IC(\d+)",
            "monster": r"monster\.se/jobb/[^/]+/(\d+)"
        }
        
    async def scan_gmail_jobs(self, days_back: int = 7) -> List[Dict]:
        """
        Scan Gmail for job-related emails and extract job information
        """
        try:
            logger.info(f"Scanning Gmail {self.gmail_user} for job emails from last {days_back} days")
            
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.gmail_user, self.gmail_password)
            mail.select("inbox")
            
            # Calculate date range
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Search for job-related emails
            search_criteria = [
                '(OR SUBJECT "job" SUBJECT "position" SUBJECT "opportunity")',
                '(OR SUBJECT "developer" SUBJECT "engineer" SUBJECT "software")',
                '(OR FROM "linkedin.com" FROM "indeed.com" FROM "glassdoor.com")',
                '(OR FROM "thelocal.se" FROM "arbetsformedlingen.se")',
                f'(SINCE "{since_date}")'
            ]
            
            jobs_found = []
            
            for criteria in search_criteria:
                try:
                    status, messages = mail.search(None, criteria)
                    if status == "OK":
                        message_ids = messages[0].split()
                        logger.info(f"Found {len(message_ids)} emails matching: {criteria}")
                        
                        for msg_id in message_ids[-20:]:  # Process last 20 emails
                            try:
                                job_info = await self._extract_job_from_email(mail, msg_id)
                                if job_info:
                                    jobs_found.append(job_info)
                            except Exception as e:
                                logger.warning(f"Error processing email {msg_id}: {e}")
                                
                except Exception as e:
                    logger.warning(f"Error with search criteria {criteria}: {e}")
            
            mail.close()
            mail.logout()
            
            # Remove duplicates based on application link
            unique_jobs = []
            seen_links = set()
            
            for job in jobs_found:
                link = job.get('application_link', '')
                if link and link not in seen_links:
                    seen_links.add(link)
                    unique_jobs.append(job)
            
            logger.info(f"Found {len(unique_jobs)} unique job opportunities from Gmail")
            return unique_jobs
            
        except Exception as e:
            logger.error(f"Error scanning Gmail for jobs: {e}")
            return []
    
    async def _extract_job_from_email(self, mail, msg_id) -> Optional[Dict]:
        """
        Extract job information from an email
        """
        try:
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                return None
                
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            subject = email_message["Subject"] or ""
            sender = email_message["From"] or ""
            date = email_message["Date"] or ""
            
            # Get email content
            content = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Check if this is actually a job-related email
            if not self._is_job_email(subject, content):
                return None
            
            # Extract job information
            job_info = {
                'source': 'gmail',
                'email_subject': subject,
                'sender': sender,
                'date_received': date,
                'title': self._extract_job_title(subject, content),
                'company': self._extract_company_name(subject, content, sender),
                'location': self._extract_location(content),
                'description': self._extract_job_description(content),
                'application_link': self._extract_application_link(content),
                'keywords': self._extract_keywords(content),
                'salary': self._extract_salary(content),
                'employment_type': self._extract_employment_type(content)
            }
            
            # Skip if blacklisted company
            company_lower = job_info['company'].lower()
            if any(blacklist in company_lower for blacklist in self.company_blacklist):
                logger.info(f"Skipping blacklisted company: {job_info['company']}")
                return None
            
            # Require application link
            if not job_info['application_link']:
                logger.info(f"Skipping job without application link: {job_info['title']}")
                return None
                
            return job_info
            
        except Exception as e:
            logger.error(f"Error extracting job from email: {e}")
            return None
    
    def _is_job_email(self, subject: str, content: str) -> bool:
        """
        Determine if email is job-related
        """
        text = (subject + " " + content).lower()
        
        job_indicators = [
            "job", "position", "opportunity", "hiring", "vacancy", "career",
            "developer", "engineer", "software", "programmer", "analyst",
            "apply now", "job alert", "new job", "job match"
        ]
        
        spam_indicators = [
            "unsubscribe", "marketing", "newsletter", "promotion",
            "advertisement", "free", "click here", "limited time"
        ]
        
        job_score = sum(1 for indicator in job_indicators if indicator in text)
        spam_score = sum(1 for indicator in spam_indicators if indicator in text)
        
        return job_score >= 2 and spam_score < 3
    
    def _extract_job_title(self, subject: str, content: str) -> str:
        """
        Extract job title from email
        """
        # Try subject first
        title_patterns = [
            r"(?:job|position|role|opportunity)[:\s]+([^-\n]{10,80})",
            r"([A-Z][^-\n]{10,80})(?:\s*-\s*(?:job|position|role))",
            r"We're hiring[:\s]+([^-\n]{10,60})",
            r"Apply for[:\s]+([^-\n]{10,60})"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Try content
        content_patterns = [
            r"Job Title[:\s]+([^\n]{10,60})",
            r"Position[:\s]+([^\n]{10,60})",
            r"Role[:\s]+([^\n]{10,60})"
        ]
        
        for pattern in content_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Software Developer Position"
    
    def _extract_company_name(self, subject: str, content: str, sender: str) -> str:
        """
        Extract company name
        """
        # Try to extract from sender domain
        if "@" in sender:
            domain = sender.split("@")[-1].replace(">", "")
            if "linkedin" not in domain and "indeed" not in domain and "noreply" not in domain:
                company = domain.split(".")[0].title()
                if len(company) > 3:
                    return company
        
        # Try content patterns
        company_patterns = [
            r"Company[:\s]+([^\n]{3,40})",
            r"Employer[:\s]+([^\n]{3,40})",
            r"at\s+([A-Z][a-zA-Z\s&]{2,30})\s+(?:is|are|seeks)",
            r"([A-Z][a-zA-Z\s&]{3,30})\s+is\s+(?:hiring|looking|seeking)"
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Technology Company"
    
    def _extract_location(self, content: str) -> str:
        """
        Extract job location
        """
        location_patterns = [
            r"Location[:\s]+([^\n]{3,30})",
            r"Based in[:\s]+([^\n]{3,30})",
            r"(?:Stockholm|Gothenburg|Göteborg|Malmö|Sweden)[,\s]*([^\n]{0,20})",
            r"Remote|Hybrid|On-site"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.group(1) else match.group(0)
        
        return "Sweden"
    
    def _extract_job_description(self, content: str) -> str:
        """
        Extract relevant job description
        """
        # Clean content
        content = re.sub(r'http[s]?://[^\s]+', '', content)  # Remove URLs
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        
        # Look for description sections
        desc_patterns = [
            r"(?:Job Description|Description|About the role|Role|Responsibilities)[:\s]+(.*?)(?:\n\n|Requirements|Qualifications|Skills|Apply)",
            r"(?:What you'll do|Your responsibilities|Key responsibilities)[:\s]+(.*?)(?:\n\n|Requirements|What we|Skills|Apply)",
            r"We are looking for(.*?)(?:\n\n|Requirements|Skills|Apply|Contact)"
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                desc = match.group(1).strip()[:500]  # Limit to 500 chars
                return desc
        
        # Fallback: take first 300 characters of meaningful content
        sentences = content.split('.')[:5]
        return '. '.join(sentences)[:300] + "..."
    
    def _extract_application_link(self, content: str) -> str:
        """
        Extract application link from email content
        """
        # Look for job site URLs
        for site, pattern in self.job_site_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                if site == "linkedin":
                    return f"https://www.linkedin.com/jobs/view/{matches[0]}"
                elif site == "indeed":
                    return f"https://se.indeed.com/viewjob?jk={matches[0]}"
                elif site == "thelocal":
                    return f"https://www.thelocal.se/jobs/job/{matches[0]}"
                elif site == "arbetsformedlingen":
                    return f"https://arbetsformedlingen.se/jobb/annons/{matches[0]}"
                # Add more site patterns as needed
        
        # Look for general apply links
        apply_patterns = [
            r"https?://[^\s]*(?:apply|job|career|position)[^\s]*",
            r"Apply here[:\s]+(https?://[^\s]+)",
            r"Application link[:\s]+(https?://[^\s]+)"
        ]
        
        for pattern in apply_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return ""
    
    def _extract_keywords(self, content: str) -> List[str]:
        """
        Extract relevant technical keywords
        """
        tech_keywords = [
            "java", "javascript", "python", "react", "angular", "vue", "nodejs", "node.js",
            "spring", "spring boot", "docker", "kubernetes", "aws", "azure", "gcp",
            "microservices", "rest api", "graphql", "postgresql", "mysql", "mongodb",
            "ci/cd", "jenkins", "gitlab", "github", "terraform", "ansible",
            "fullstack", "frontend", "backend", "devops", "cloud", "agile", "scrum"
        ]
        
        content_lower = content.lower()
        found_keywords = [kw for kw in tech_keywords if kw in content_lower]
        return found_keywords[:10]  # Limit to 10 keywords
    
    def _extract_salary(self, content: str) -> str:
        """
        Extract salary information
        """
        salary_patterns = [
            r"(\d{2,3}[,\s]*\d{3}[,\s]*\d{3})\s*SEK",
            r"(\d{2,3}[,\s]*\d{3})\s*-\s*(\d{2,3}[,\s]*\d{3})\s*SEK",
            r"Salary[:\s]+([^\n]{10,50})",
            r"(\d{2,3}k)\s*-\s*(\d{2,3}k)\s*SEK"
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_employment_type(self, content: str) -> str:
        """
        Extract employment type
        """
        content_lower = content.lower()
        
        if "permanent" in content_lower or "full-time" in content_lower or "tillsvidare" in content_lower:
            return "Permanent"
        elif "contract" in content_lower or "consultant" in content_lower or "konsult" in content_lower:
            return "Contract"
        elif "part-time" in content_lower or "deltid" in content_lower:
            return "Part-time"
        elif "remote" in content_lower:
            return "Remote"
        
        return "Full-time"
    
    async def scan_linkedin_jobs(self, keywords: List[str] = None) -> List[Dict]:
        """
        Scan LinkedIn for job recommendations (placeholder for LinkedIn API integration)
        """
        try:
            # Note: LinkedIn's official API has limited job search capabilities
            # This would require either:
            # 1. LinkedIn Talent Solutions API (enterprise)
            # 2. Web scraping (against ToS)
            # 3. RSS feeds from LinkedIn job alerts
            # 4. Integration with job aggregators
            
            logger.info("LinkedIn job scanning - would require LinkedIn API access")
            
            # Placeholder implementation - return mock jobs for testing
            mock_linkedin_jobs = [
                {
                    'source': 'linkedin',
                    'title': 'Senior Full Stack Developer',
                    'company': 'Spotify Technology',
                    'location': 'Stockholm, Sweden',
                    'description': 'We are looking for a passionate Full Stack Developer to join our engineering team. Experience with React, Node.js, and cloud technologies required.',
                    'application_link': 'https://www.linkedin.com/jobs/view/3721234567',
                    'keywords': ['javascript', 'react', 'nodejs', 'aws', 'fullstack'],
                    'salary': '650,000 - 850,000 SEK',
                    'employment_type': 'Permanent',
                    'date_received': datetime.now().strftime('%Y-%m-%d')
                }
            ]
            
            return mock_linkedin_jobs
            
        except Exception as e:
            logger.error(f"Error scanning LinkedIn jobs: {e}")
            return []
    
    async def send_job_email(self, job: Dict, cv_pdf: bytes, cl_pdf: bytes) -> bool:
        """
        Send personalized job email with CV/CL attachments and application link
        """
        try:
            logger.info(f"Sending job email for {job['company']} - {job['title']}")
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.target_email
            msg['Subject'] = f"🎯 Job Match: {job['title']} at {job['company']}"
            
            # Create email body
            email_body = self._create_job_email_body(job)
            msg.attach(MIMEText(email_body, 'html'))
            
            # Attach CV PDF
            if cv_pdf:
                cv_attachment = MIMEApplication(cv_pdf, _subtype='pdf')
                cv_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CV_{job['company']}_{job['title'].replace(' ', '_')}.pdf"
                )
                msg.attach(cv_attachment)
            
            # Attach Cover Letter PDF
            if cl_pdf:
                cl_attachment = MIMEApplication(cl_pdf, _subtype='pdf')
                cl_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f"CL_{job['company']}_{job['title'].replace(' ', '_')}.pdf"
                )
                msg.attach(cl_attachment)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            text = msg.as_string()
            server.sendmail(self.sender_email, self.target_email, text)
            server.quit()
            
            logger.info(f"✅ Successfully sent job email for {job['company']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending job email: {e}")
            return False
    
    def _create_job_email_body(self, job: Dict) -> str:
        """
        Create HTML email body for job notification
        """
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <h1 style="margin: 0; font-size: 24px;">🎯 New Job Match Found!</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Personalized CV & Cover Letter Ready</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="color: #2c3e50; margin-top: 0;">{job['title']}</h2>
                    <p style="font-size: 18px; color: #3498db; margin: 5px 0;"><strong>{job['company']}</strong></p>
                    <p style="color: #666; margin: 5px 0;">📍 {job.get('location', 'Sweden')}</p>
                    {f'<p style="color: #27ae60; margin: 5px 0;">💰 {job["salary"]}</p>' if job.get('salary') else ''}
                    <p style="color: #666; margin: 5px 0;">⏰ {job.get('employment_type', 'Full-time')}</p>
                </div>
                
                <div style="background: white; padding: 20px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="color: #2c3e50; margin-top: 0;">📋 Job Description</h3>
                    <p style="color: #555; line-height: 1.6;">{job.get('description', 'Full job description available via application link.')[:400]}...</p>
                    
                    {f'''
                    <h3 style="color: #2c3e50;">🔧 Key Skills</h3>
                    <div style="margin: 10px 0;">
                        {' '.join([f'<span style="background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin: 2px;">{kw}</span>' for kw in job.get('keywords', [])[:8]])}
                    </div>
                    ''' if job.get('keywords') else ''}
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{job.get('application_link', '#')}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 25px; 
                              font-weight: bold; 
                              font-size: 16px;
                              display: inline-block;
                              box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                        🚀 APPLY NOW
                    </a>
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #856404; margin-top: 0;">📎 Attachments Included</h3>
                    <ul style="color: #856404; margin: 0;">
                        <li>✅ Customized CV tailored for this position</li>
                        <li>✅ Personalized Cover Letter with company research</li>
                        <li>✅ ATS-optimized with relevant keywords</li>
                    </ul>
                </div>
                
                <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="color: #155724; margin: 0; text-align: center;">
                        <strong>💡 Quality Check Complete</strong><br>
                        If you're satisfied with the CV and Cover Letter quality, click "APPLY NOW" to submit your application directly!
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; font-size: 12px;">
                    <p>📧 Source: {job.get('source', 'Gmail').title()} | 🤖 Generated by JobHunter AI</p>
                    <p>Received: {job.get('date_received', datetime.now().strftime('%Y-%m-%d'))}</p>
                </div>
            </div>
        </body>
        </html>
        """