import imaplib
import email
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from email.header import decode_header
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailScannerService:
    """Service for scanning Gmail emails using IMAP with app password"""
    
    def __init__(self):
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
    
    async def scan_job_emails(self, days_back: int = 1) -> List[Dict]:
        """
        Scan Gmail for job-related emails from LinkedIn, Indeed, etc.
        
        Args:
            days_back: Number of days to look back (default 1 for daily scanning)
            
        Returns:
            List of parsed job opportunities
        """
        try:
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.smtp_user, self.smtp_password)
            
            # Select inbox
            mail.select('inbox')
            
            # Calculate date filter
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Search for job-related emails
            job_emails = []
            
            # Search LinkedIn job emails
            linkedin_jobs = await self._scan_linkedin_emails(mail, since_date)
            job_emails.extend(linkedin_jobs)
            
            # Search Indeed job emails  
            indeed_jobs = await self._scan_indeed_emails(mail, since_date)
            job_emails.extend(indeed_jobs)
            
            # Search other job board emails
            other_jobs = await self._scan_other_job_emails(mail, since_date)
            job_emails.extend(other_jobs)
            
            mail.close()
            mail.logout()
            
            logger.info(f"Found {len(job_emails)} job opportunities in emails")
            return job_emails
            
        except Exception as e:
            logger.error(f"Error scanning emails: {e}")
            return []
    
    async def _scan_linkedin_emails(self, mail, since_date: str) -> List[Dict]:
        """Scan for LinkedIn job alert emails"""
        try:
            # Search for LinkedIn emails
            search_criteria = f'(SINCE {since_date} FROM "linkedin.com" SUBJECT "job")'
            status, messages = mail.search(None, search_criteria)
            
            if status != 'OK':
                return []
            
            job_emails = []
            message_ids = messages[0].split()
            
            for msg_id in message_ids[-10:]:  # Process last 10 emails
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    continue
                    
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Parse LinkedIn job email
                jobs = await self._parse_linkedin_email(email_message)
                job_emails.extend(jobs)
            
            return job_emails
            
        except Exception as e:
            logger.error(f"Error scanning LinkedIn emails: {e}")
            return []
    
    async def _scan_indeed_emails(self, mail, since_date: str) -> List[Dict]:
        """Scan for Indeed job alert emails"""
        try:
            # Search for Indeed emails
            search_criteria = f'(SINCE {since_date} FROM "indeed.com" SUBJECT "job")'
            status, messages = mail.search(None, search_criteria)
            
            if status != 'OK':
                return []
            
            job_emails = []
            message_ids = messages[0].split()
            
            for msg_id in message_ids[-10:]:  # Process last 10 emails
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    continue
                    
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Parse Indeed job email
                jobs = await self._parse_indeed_email(email_message)
                job_emails.extend(jobs)
            
            return job_emails
            
        except Exception as e:
            logger.error(f"Error scanning Indeed emails: {e}")
            return []
    
    async def _scan_other_job_emails(self, mail, since_date: str) -> List[Dict]:
        """Scan for other job board emails (Glassdoor, Monster, etc.)"""
        try:
            job_domains = [
                "glassdoor.com", "monster.com", "ziprecruiter.com", 
                "dice.com", "careerbuilder.com", "simplyhired.com"
            ]
            
            job_emails = []
            
            for domain in job_domains:
                search_criteria = f'(SINCE {since_date} FROM "{domain}")'
                status, messages = mail.search(None, search_criteria)
                
                if status != 'OK':
                    continue
                
                message_ids = messages[0].split()
                
                for msg_id in message_ids[-5:]:  # Process last 5 emails per domain
                    status, msg_data = mail.fetch(msg_id, '(RFC822)')
                    if status != 'OK':
                        continue
                        
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Parse general job email
                    jobs = await self._parse_general_job_email(email_message, domain)
                    job_emails.extend(jobs)
            
            return job_emails
            
        except Exception as e:
            logger.error(f"Error scanning other job emails: {e}")
            return []
    
    async def _parse_linkedin_email(self, email_message) -> List[Dict]:
        """Parse LinkedIn job alert email"""
        try:
            subject = self._decode_header(email_message['Subject'])
            body = self._get_email_body(email_message)
            date_received = email_message['Date']
            
            jobs = []
            
            # LinkedIn job patterns
            job_patterns = [
                r'([^\\n]+?)\\s+at\\s+([^\\n]+?)(?:\\s*(?:-|\\||•))',
                r'([^\\n]+?)\\s+•\\s+([^\\n]+?)\\s+•',
                r'Job:\\s*([^\\n]+?)\\s+Company:\\s*([^\\n]+?)(?:\\s|\\n)',
            ]
            
            # Extract job URLs
            url_pattern = r'https://www\\.linkedin\\.com/jobs/view/\\d+'
            job_urls = re.findall(url_pattern, body)
            
            # Parse job information
            for pattern in job_patterns:
                matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
                
                for i, match in enumerate(matches[:5]):  # Limit to 5 jobs per email
                    if len(match) == 2:
                        title, company = match[0].strip(), match[1].strip()
                        
                        if len(title) > 3 and len(company) > 2:
                            job = {
                                'id': f"linkedin_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'source': 'linkedin_email',
                                'url': job_urls[i] if i < len(job_urls) else '',
                                'location': self._extract_location(body),
                                'description': self._extract_description(body, title),
                                'posting_date': self._parse_date(date_received),
                                'salary': None,
                                'job_type': 'fulltime',
                                'remote_option': 'remote' in body.lower(),
                                'email_subject': subject,
                                'confidence_score': 0.9
                            }
                            jobs.append(job)
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn email: {e}")
            return []
    
    async def _parse_indeed_email(self, email_message) -> List[Dict]:
        """Parse Indeed job alert email"""
        try:
            subject = self._decode_header(email_message['Subject'])
            body = self._get_email_body(email_message)
            date_received = email_message['Date']
            
            jobs = []
            
            # Indeed job patterns
            job_patterns = [
                r'([^\\n]+?)\\s*-\\s*([^\\n]+?)(?:\\s*\\$|\\s*\\n)',
                r'([^\\n]+?)\\s+at\\s+([^\\n]+?)(?:\\s*\\n|\\s*-)',
                r'Job:\\s*([^\\n]+?)\\s+Company:\\s*([^\\n]+?)(?:\\s|\\n)',
            ]
            
            # Extract job URLs
            url_pattern = r'https://www\\.indeed\\.com/viewjob\\?jk=[a-zA-Z0-9]+'
            job_urls = re.findall(url_pattern, body)
            
            # Extract salary information
            salary_pattern = r'\\$([0-9,]+)(?:\\s*-\\s*\\$([0-9,]+))?'
            salaries = re.findall(salary_pattern, body)
            
            # Parse job information
            for pattern in job_patterns:
                matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
                
                for i, match in enumerate(matches[:5]):  # Limit to 5 jobs per email
                    if len(match) == 2:
                        title, company = match[0].strip(), match[1].strip()
                        
                        if len(title) > 3 and len(company) > 2:
                            salary_info = None
                            if i < len(salaries) and salaries[i][0]:
                                salary_info = {
                                    'min': int(salaries[i][0].replace(',', '')),
                                    'max': int(salaries[i][1].replace(',', '')) if salaries[i][1] else None,
                                    'currency': 'USD'
                                }
                            
                            job = {
                                'id': f"indeed_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'source': 'indeed_email',
                                'url': job_urls[i] if i < len(job_urls) else '',
                                'location': self._extract_location(body),
                                'description': self._extract_description(body, title),
                                'posting_date': self._parse_date(date_received),
                                'salary': salary_info,
                                'job_type': 'fulltime',
                                'remote_option': 'remote' in body.lower() or 'work from home' in body.lower(),
                                'email_subject': subject,
                                'confidence_score': 0.9
                            }
                            jobs.append(job)
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error parsing Indeed email: {e}")
            return []
    
    async def _parse_general_job_email(self, email_message, domain: str) -> List[Dict]:
        """Parse general job board email"""
        try:
            subject = self._decode_header(email_message['Subject'])
            body = self._get_email_body(email_message)
            date_received = email_message['Date']
            
            # Check if this is likely a job alert
            job_keywords = ['job', 'position', 'opportunity', 'hiring', 'career']
            if not any(keyword in subject.lower() or keyword in body.lower() for keyword in job_keywords):
                return []
            
            jobs = []
            
            # Generic job patterns
            job_patterns = [
                r'([^\\n]+?)\\s+at\\s+([^\\n]+?)(?:\\s*\\n|\\s*-|\\s*\\|)',
                r'([^\\n]+?)\\s*-\\s*([^\\n]+?)(?:\\s*\\n|\\s*\\$)',
                r'Position:\\s*([^\\n]+?)\\s+Company:\\s*([^\\n]+?)(?:\\s|\\n)',
            ]
            
            # Parse job information
            for pattern in job_patterns:
                matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
                
                for match in matches[:3]:  # Limit to 3 jobs per email
                    if len(match) == 2:
                        title, company = match[0].strip(), match[1].strip()
                        
                        if len(title) > 3 and len(company) > 2:
                            job = {
                                'id': f"{domain.split('.')[0]}_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'source': f"{domain.split('.')[0]}_email",
                                'url': '',
                                'location': self._extract_location(body),
                                'description': self._extract_description(body, title),
                                'posting_date': self._parse_date(date_received),
                                'salary': None,
                                'job_type': 'fulltime',
                                'remote_option': 'remote' in body.lower(),
                                'email_subject': subject,
                                'confidence_score': 0.7
                            }
                            jobs.append(job)
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error parsing general job email: {e}")
            return []
    
    def _decode_header(self, header) -> str:
        """Decode email header"""
        if header is None:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_header = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_header += part.decode(encoding or 'utf-8')
            else:
                decoded_header += part
        
        return decoded_header
    
    def _get_email_body(self, email_message) -> str:
        """Extract email body text"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if (content_type == "text/plain" and 
                    "attachment" not in content_disposition):
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                body = str(email_message.get_payload())
        
        return body
    
    def _extract_location(self, body: str) -> str:
        """Extract location from email body"""
        location_patterns = [
            r'([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*,\\s*[A-Z]{2})',  # "San Francisco, CA"
            r'\\b(Remote)\\b',  # "Remote"
            r'([A-Z][a-z]+,\\s*[A-Z][a-z]+)',  # "Boston, Massachusetts"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(1)
        
        return ""
    
    def _extract_description(self, body: str, title: str) -> str:
        """Extract job description around the title"""
        title_index = body.lower().find(title.lower())
        if title_index == -1:
            return body[:200]
        
        start = max(0, title_index - 100)
        end = min(len(body), title_index + len(title) + 200)
        
        description = body[start:end].strip()
        description = re.sub(r'\\s+', ' ', description)
        
        return description[:300]
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse email date string"""
        if not date_string:
            return None
        
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_string)
        except:
            return datetime.utcnow()