import os
import logging
import asyncio
import aiohttp
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

logger = logging.getLogger(__name__)

class RealJobScanner:
    """
    Real job scanner that fetches actual job advertisements from multiple sources
    """
    
    def __init__(self):
        # Email configuration - you need to set the Gmail app password
        self.gmail_user = "bluehawana@gmail.com"
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")
        self.sender_email = os.getenv("SENDER_EMAIL", "leeharvad@gmail.com")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        self.target_email = "hongzhili01@gmail.com"
        
        # Job search configuration with enhanced filtering for 5+ years experience
        self.search_keywords = [
            "senior fullstack developer", "senior full stack developer", "senior developer",
            "senior backend developer", "senior frontend developer", "senior software engineer",
            "lead developer", "tech lead", "principal engineer", "software architect",
            "fullstack developer", "backend developer", "frontend developer", "software engineer",
            "devops engineer", "cloud engineer", "cloud architect", "cloud developer",
            "java developer", "python developer", "javascript developer", "react developer", 
            "nodejs developer", "microservices developer", "api developer"
        ]
        
        self.locations = ["Stockholm", "Göteborg", "Gothenburg", "Malmö", "Sweden", "Remote"]
        
        # Headers for web scraping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    async def scan_real_gmail_jobs(self, days_back: int = 3) -> List[Dict]:
        """
        Scan actual Gmail inbox for real job notifications
        """
        try:
            if not self.gmail_password:
                logger.error("❌ Gmail app password not set! Please set GMAIL_APP_PASSWORD in .env")
                return []
            
            logger.info(f"🔍 Scanning real Gmail jobs from {self.gmail_user} (last {days_back} days)")
            
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.gmail_user, self.gmail_password)
            mail.select("inbox")
            
            # Search for recent job-related emails
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Multiple search queries for comprehensive job finding
            search_queries = [
                f'(SINCE "{since_date}" SUBJECT "job")',
                f'(SINCE "{since_date}" SUBJECT "developer")',
                f'(SINCE "{since_date}" SUBJECT "engineer")',
                f'(SINCE "{since_date}" SUBJECT "position")',
                f'(SINCE "{since_date}" SUBJECT "opportunity")',
                f'(SINCE "{since_date}" FROM "linkedin")',
                f'(SINCE "{since_date}" FROM "indeed")',
                f'(SINCE "{since_date}" FROM "thelocal")',
                f'(SINCE "{since_date}" FROM "arbetsformedlingen")',
                f'(SINCE "{since_date}" FROM "glassdoor")',
                f'(SINCE "{since_date}" FROM "@*recruit*")',
                f'(SINCE "{since_date}" FROM "@*career*")',
                f'(SINCE "{since_date}" BODY "apply")',
                f'(SINCE "{since_date}" BODY "software")'
            ]
            
            all_job_emails = []
            processed_msg_ids = set()
            
            for query in search_queries:
                try:
                    status, messages = mail.search(None, query)
                    if status == "OK" and messages[0]:
                        message_ids = messages[0].split()
                        logger.info(f"Found {len(message_ids)} emails for query: {query}")
                        
                        for msg_id in message_ids:
                            if msg_id not in processed_msg_ids:
                                processed_msg_ids.add(msg_id)
                                job_info = await self._extract_real_job_from_email(mail, msg_id)
                                if job_info:
                                    all_job_emails.append(job_info)
                                    
                except Exception as e:
                    logger.warning(f"Error with query {query}: {e}")
            
            mail.close()
            mail.logout()
            
            # Remove duplicates and filter quality jobs
            unique_jobs = self._filter_quality_jobs(all_job_emails)
            
            logger.info(f"✅ Found {len(unique_jobs)} real job opportunities from Gmail")
            return unique_jobs
            
        except Exception as e:
            logger.error(f"❌ Error scanning Gmail: {e}")
            return []
    
    async def _extract_real_job_from_email(self, mail, msg_id) -> Optional[Dict]:
        """
        Extract comprehensive job information from real emails
        """
        try:
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                return None
            
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            subject = email_message.get("Subject", "")
            sender = email_message.get("From", "")
            date = email_message.get("Date", "")
            
            # Extract email content
            content = self._extract_email_content(email_message)
            
            # Enhanced job validation
            if not self._is_real_job_email(subject, content, sender):
                return None
            
            # Extract comprehensive job information
            job_info = {
                'source': 'gmail_real',
                'email_subject': subject,
                'sender': sender,
                'date_received': date,
                'raw_content': content[:1000],  # Keep first 1000 chars for analysis
                'title': self._extract_job_title_enhanced(subject, content),
                'company': self._extract_company_name_enhanced(subject, content, sender),
                'location': self._extract_location_enhanced(content),
                'description': self._extract_comprehensive_job_description(content),
                'requirements': self._extract_job_requirements(content),
                'application_link': self._extract_application_link_enhanced(content),
                'application_email': self._extract_application_email(content),
                'keywords': self._extract_technical_keywords(content),
                'salary': self._extract_salary_info(content),
                'employment_type': self._extract_employment_type_enhanced(content),
                'benefits': self._extract_benefits(content),
                'company_info': self._extract_company_info(content),
                'contact_person': self._extract_contact_person(content),
                'deadline': self._extract_application_deadline(content),
                'experience_level': self._extract_experience_level(content)
            }
            
            # Quality check - must have essential info
            if not job_info['application_link'] and not job_info['application_email']:
                logger.info(f"Skipping job without application method: {job_info['title']}")
                return None
            
            if not job_info['company'] or job_info['company'] == "Unknown Company":
                logger.info(f"Skipping job without clear company: {job_info['title']}")
                return None
            
            return job_info
            
        except Exception as e:
            logger.error(f"Error extracting job from email: {e}")
            return None
    
    def _extract_email_content(self, email_message) -> str:
        """
        Extract clean text content from email
        """
        content = ""
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            content += payload.decode('utf-8', errors='ignore')
                    elif content_type == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            html_content = payload.decode('utf-8', errors='ignore')
                            # Extract text from HTML
                            soup = BeautifulSoup(html_content, 'html.parser')
                            content += soup.get_text()
            else:
                payload = email_message.get_payload(decode=True)
                if payload:
                    content = payload.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.warning(f"Error extracting email content: {e}")
        
        return content
    
    def _is_real_job_email(self, subject: str, content: str, sender: str) -> bool:
        """
        Enhanced job email detection
        """
        text = (subject + " " + content + " " + sender).lower()
        
        # Strong job indicators
        strong_indicators = [
            "job opportunity", "job opening", "we're hiring", "join our team",
            "software engineer", "developer position", "engineering role",
            "apply now", "job alert", "career opportunity", "new position",
            "fullstack", "backend", "frontend", "devops", "python", "java",
            "react", "nodejs", "kubernetes", "aws", "azure"
        ]
        
        # Spam/newsletter indicators
        spam_indicators = [
            "unsubscribe", "newsletter", "promotional", "marketing campaign",
            "limited time offer", "click here for", "free trial", "discount",
            "viagra", "casino", "lottery", "congratulations you won"
        ]
        
        # Company/recruiter domains (more likely to be real jobs)
        recruiter_domains = [
            "linkedin.com", "indeed.com", "glassdoor.com", "thelocal.se",
            "arbetsformedlingen.se", "monster.se", "stepstone.se", "jobs.se"
        ]
        
        strong_score = sum(1 for indicator in strong_indicators if indicator in text)
        spam_score = sum(1 for indicator in spam_indicators if indicator in text)
        recruiter_score = sum(1 for domain in recruiter_domains if domain in sender.lower())
        
        # Enhanced scoring
        total_score = strong_score + (recruiter_score * 2) - (spam_score * 2)
        
        return total_score >= 2 and spam_score < 2
    
    def _extract_job_title_enhanced(self, subject: str, content: str) -> str:
        """
        Enhanced job title extraction
        """
        # Try subject line first
        title_patterns = [
            r"job[:\s]+([^-\n|]{15,80})",
            r"position[:\s]+([^-\n|]{15,80})",
            r"role[:\s]+([^-\n|]{15,80})",
            r"hiring[:\s]+([^-\n|]{15,80})",
            r"([A-Z][^-\n|]{15,80})(?:\s*-\s*(?:job|position|role))",
            r"apply for[:\s]+([^-\n|]{15,60})",
            r"opportunity[:\s]+([^-\n|]{15,60})"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 10 and any(keyword in title.lower() for keyword in ['developer', 'engineer', 'software', 'fullstack', 'backend', 'frontend', 'devops']):
                    return title
        
        # Try content patterns
        content_patterns = [
            r"job title[:\s]+([^\n]{15,60})",
            r"position[:\s]+([^\n]{15,60})",
            r"we are looking for\s+a\s+([^\n]{15,60})",
            r"seeking\s+a\s+([^\n]{15,60})",
            r"hiring\s+a\s+([^\n]{15,60})"
        ]
        
        for pattern in content_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 10:
                    return title
        
        return "Software Developer Position"
    
    def _extract_comprehensive_job_description(self, content: str) -> str:
        """
        Extract comprehensive job description
        """
        # Clean content
        content = re.sub(r'http[s]?://[^\s]+', '[LINK]', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Look for description sections
        desc_patterns = [
            r"(?:job description|about the role|role description|responsibilities|what you'll do)[:\s]+(.*?)(?:requirements|qualifications|skills|what we offer|benefits|apply|contact)",
            r"(?:we are looking for|we're seeking|join our team)[:\s]+(.*?)(?:requirements|skills|qualifications|apply)",
            r"(?:position summary|role overview)[:\s]+(.*?)(?:requirements|skills|apply)"
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                description = match.group(1).strip()
                if len(description) > 100:
                    return description[:800]  # Limit but allow more detail
        
        # Fallback: extract first meaningful paragraphs
        sentences = content.split('.')
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 50 and any(keyword in s.lower() for keyword in ['develop', 'engineer', 'software', 'team', 'experience', 'work'])]
        
        return '. '.join(meaningful_sentences[:5])[:600] + "..."
    
    def _extract_job_requirements(self, content: str) -> List[str]:
        """
        Extract job requirements/qualifications
        """
        requirements = []
        
        req_patterns = [
            r"(?:requirements|qualifications|skills required|must have)[:\s]+(.*?)(?:benefits|salary|apply|contact|what we offer)",
            r"(?:you should have|ideal candidate|we're looking for someone with)[:\s]+(.*?)(?:benefits|apply|contact)"
        ]
        
        for pattern in req_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                req_text = match.group(1).strip()
                # Split into individual requirements
                req_lines = re.split(r'[•\-\*\n]', req_text)
                for line in req_lines:
                    line = line.strip()
                    if len(line) > 10 and len(line) < 200:
                        requirements.append(line)
                break
        
        return requirements[:10]  # Limit to 10 requirements
    
    def _filter_quality_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Filter and prioritize quality job opportunities
        """
        quality_jobs = []
        seen_combinations = set()
        
        for job in jobs:
            # Create unique identifier
            job_id = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
            
            if job_id in seen_combinations:
                continue
            seen_combinations.add(job_id)
            
            # Quality checks
            quality_score = 0
            
            # Check for complete information
            if job['application_link']:
                quality_score += 3
            if job['application_email']:
                quality_score += 2
            if len(job['description']) > 200:
                quality_score += 2
            if job['keywords']:
                quality_score += len(job['keywords'][:5])  # Up to 5 points for keywords
            if job['salary']:
                quality_score += 1
            
            # Prioritize relevant keywords
            relevant_keywords = ['fullstack', 'backend', 'frontend', 'devops', 'python', 'java', 'react', 'nodejs', 'kubernetes', 'aws', 'azure']
            content_lower = f"{job['title']} {job['description']}".lower()
            relevant_score = sum(1 for kw in relevant_keywords if kw in content_lower)
            quality_score += relevant_score
            
            # Must meet minimum quality threshold
            if quality_score >= 8:  # Minimum threshold for quality
                quality_jobs.append(job)
        
        # Sort by quality score and return top jobs
        quality_jobs.sort(key=lambda x: len(x.get('keywords', [])) + len(x.get('description', '')), reverse=True)
        
        return quality_jobs[:10]  # Return top 10 quality jobs
    
    # Additional extraction methods...
    def _extract_company_name_enhanced(self, subject: str, content: str, sender: str) -> str:
        """Enhanced company name extraction"""
        # Try sender domain first
        if "@" in sender:
            domain = sender.split("@")[-1].replace(">", "").lower()
            if not any(common in domain for common in ["linkedin", "indeed", "noreply", "no-reply", "gmail", "yahoo"]):
                company = domain.split(".")[0].title()
                if len(company) > 2:
                    return company
        
        # Content patterns
        company_patterns = [
            r"company[:\s]+([^\n]{3,40})",
            r"employer[:\s]+([^\n]{3,40})",
            r"at\s+([A-Z][a-zA-Z\s&\.]{2,30})\s+(?:is|are|we|our)",
            r"([A-Z][a-zA-Z\s&\.]{3,30})\s+(?:is hiring|is looking|seeks|is seeking)",
            r"join\s+([A-Z][a-zA-Z\s&\.]{3,30})",
            r"([A-Z][a-zA-Z\s&\.]{3,30})\s+team"
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 3 and not any(word in company.lower() for word in ["the job", "this role", "your team"]):
                    return company
        
        return "Technology Company"
    
    def _extract_location_enhanced(self, content: str) -> str:
        """Enhanced location extraction"""
        location_patterns = [
            r"location[:\s]+([^\n]{3,30})",
            r"based in[:\s]+([^\n]{3,30})",
            r"office[:\s]+([^\n]{3,30})",
            r"(Stockholm|Göteborg|Gothenburg|Malmö|Sweden|Remote|Hybrid)[,\s]*([^\n]{0,20})",
            r"work from[:\s]+([^\n]{3,30})"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                location = match.group(1).strip() if match.group(1) else match.group(0)
                if location:
                    return location
        
        return "Sweden"
    
    def _extract_technical_keywords(self, content: str) -> List[str]:
        """Extract technical keywords with enhanced matching"""
        tech_keywords = [
            # Programming Languages
            "java", "javascript", "python", "c#", "csharp", "go", "rust", "kotlin", "swift", "typescript",
            # Frontend
            "react", "angular", "vue", "svelte", "html", "css", "sass", "webpack", "vite",
            # Backend
            "nodejs", "node.js", "spring", "spring boot", "django", "flask", "express", ".net", "dotnet",
            # Databases
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sql", "nosql",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab", "github actions",
            "terraform", "ansible", "helm", "prometheus", "grafana",
            # Methodologies
            "agile", "scrum", "ci/cd", "tdd", "microservices", "api", "rest", "graphql",
            # Specializations
            "fullstack", "full-stack", "backend", "frontend", "devops", "cloud", "machine learning", "ai"
        ]
        
        content_lower = content.lower()
        found_keywords = []
        
        for keyword in tech_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:15]  # Return up to 15 keywords
    
    def _extract_application_link_enhanced(self, content: str) -> str:
        """Enhanced application link extraction"""
        # Job site patterns
        job_patterns = [
            r"https?://[^\s]*linkedin\.com/jobs/view/\d+[^\s]*",
            r"https?://[^\s]*indeed\.com/viewjob\?jk=[^\s]+",
            r"https?://[^\s]*thelocal\.se/jobs/[^\s]+",
            r"https?://[^\s]*arbetsformedlingen\.se/jobb/annons/\d+[^\s]*",
            r"https?://[^\s]*glassdoor\.com/job-listing/[^\s]+",
            r"https?://[^\s]*monster\.se/jobb/[^\s]+",
            r"https?://[^\s]*stepstone\.se/jobb/[^\s]+",
            r"https?://[^\s]*(?:apply|career|job|position|hiring)[^\s]*"
        ]
        
        for pattern in job_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return ""
    
    def _extract_application_email(self, content: str) -> str:
        """Extract application email"""
        email_patterns = [
            r"apply to[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"send your cv to[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"contact[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                email = matches[0]
                # Filter out common non-application emails
                if not any(exclude in email.lower() for exclude in ["noreply", "no-reply", "unsubscribe", "marketing"]):
                    return email
        
        return ""
    
    def _extract_salary_info(self, content: str) -> str:
        """Extract salary information"""
        salary_patterns = [
            r"(\d{2,3}[,\s]*\d{3}[,\s]*\d{3})\s*(?:sek|kr|kronor)",
            r"(\d{2,3}[,\s]*\d{3})\s*-\s*(\d{2,3}[,\s]*\d{3})\s*(?:sek|kr|kronor)",
            r"salary[:\s]+([^\n]{10,50})",
            r"lön[:\s]+([^\n]{10,50})",
            r"(\d{2,3}k)\s*-\s*(\d{2,3}k)\s*(?:sek|kr|per year|annually)"
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_employment_type_enhanced(self, content: str) -> str:
        """Enhanced employment type extraction"""
        content_lower = content.lower()
        
        if any(term in content_lower for term in ["permanent", "fast anställning", "tillsvidare", "full-time", "heltid"]):
            return "Permanent"
        elif any(term in content_lower for term in ["contract", "konsult", "consultant", "kontakt", "vikariat"]):
            return "Contract"
        elif any(term in content_lower for term in ["part-time", "deltid", "halvtid"]):
            return "Part-time"
        elif any(term in content_lower for term in ["remote", "distans", "hemarbete"]):
            return "Remote"
        elif any(term in content_lower for term in ["hybrid"]):
            return "Hybrid"
        
        return "Full-time"
    
    def _extract_benefits(self, content: str) -> List[str]:
        """Extract job benefits"""
        benefits = []
        
        benefit_patterns = [
            r"(?:benefits|förmåner|erbjuder vi)[:\s]+(.*?)(?:apply|contact|requirements)",
            r"(?:what we offer|vad vi erbjuder)[:\s]+(.*?)(?:apply|contact|requirements)"
        ]
        
        for pattern in benefit_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                benefit_text = match.group(1).strip()
                benefit_lines = re.split(r'[•\-\*\n]', benefit_text)
                for line in benefit_lines:
                    line = line.strip()
                    if len(line) > 5 and len(line) < 100:
                        benefits.append(line)
                break
        
        return benefits[:5]
    
    def _extract_company_info(self, content: str) -> str:
        """Extract company information"""
        company_patterns = [
            r"(?:about us|about the company|företaget)[:\s]+(.*?)(?:role|position|requirements|apply)",
            r"(?:we are|vi är)[:\s]+(.*?)(?:seeking|looking|role|position)"
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                info = match.group(1).strip()
                if len(info) > 50:
                    return info[:300]
        
        return ""
    
    def _extract_contact_person(self, content: str) -> str:
        """Extract contact person information"""
        contact_patterns = [
            r"contact[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"recruiter[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"hiring manager[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)[,\s]+(?:recruiter|hr|talent|hiring)"
        ]
        
        for pattern in contact_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_application_deadline(self, content: str) -> str:
        """Extract application deadline"""
        deadline_patterns = [
            r"(?:deadline|last day|sista dag|apply by)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(?:deadline|last day|sista dag|apply by)[:\s]+(\d{1,2}\s+[a-zA-Z]+\s+\d{2,4})",
            r"applications close[:\s]+([^\n]{10,30})"
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_experience_level(self, content: str) -> str:
        """Extract required experience level"""
        content_lower = content.lower()
        
        if any(term in content_lower for term in ["senior", "lead", "principal", "architect", "5+ years", "5-10 years"]):
            return "Senior"
        elif any(term in content_lower for term in ["junior", "entry level", "graduate", "0-2 years", "recent graduate"]):
            return "Junior"
        elif any(term in content_lower for term in ["mid-level", "intermediate", "2-5 years", "3+ years"]):
            return "Mid-level"
        
        return "Mid-level"  # Default