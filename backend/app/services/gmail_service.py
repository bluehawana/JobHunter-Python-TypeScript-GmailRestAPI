import base64
import email
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from datetime import datetime, timedelta

class GmailService:
    """Service for interacting with Gmail API"""
    
    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.service = build('gmail', 'v1', credentials=credentials)
    
    async def search_job_emails(self, keywords: List[str], days_back: int = 7) -> List[Dict]:
        """
        Search for job-related emails in Gmail including LinkedIn and Indeed subscriptions
        
        Args:
            keywords: List of keywords to search for
            days_back: Number of days to look back
            
        Returns:
            List of job-related emails with metadata
        """
        try:
            all_job_emails = []
            
            # Search for LinkedIn job alerts
            linkedin_jobs = await self._search_linkedin_job_emails(keywords, days_back)
            all_job_emails.extend(linkedin_jobs)
            
            # Search for Indeed job alerts
            indeed_jobs = await self._search_indeed_job_emails(keywords, days_back)
            all_job_emails.extend(indeed_jobs)
            
            # Search for general job-related emails
            general_jobs = await self._search_general_job_emails(keywords, days_back)
            all_job_emails.extend(general_jobs)
            
            # Remove duplicates and sort by date
            unique_jobs = self._remove_duplicate_emails(all_job_emails)
            return sorted(unique_jobs, key=lambda x: x.get('date_received', datetime.min), reverse=True)
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    async def _search_linkedin_job_emails(self, keywords: List[str], days_back: int) -> List[Dict]:
        """Search specifically for LinkedIn job alert emails"""
        try:
            date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # LinkedIn-specific search query
            query_parts = [
                f'after:{date_filter}',
                'from:linkedin.com OR from:@linkedin.com',
                '(jobs OR "job alert" OR "new jobs" OR "recommended jobs")',
                '-unsubscribe'
            ]
            
            # Add user keywords if provided
            if keywords:
                keyword_query = ' OR '.join([f'"{keyword}"' for keyword in keywords])
                query_parts.append(f'({keyword_query})')
            
            query = ' '.join(query_parts)
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=25
            ).execute()
            
            messages = results.get('messages', [])
            linkedin_jobs = []
            
            for message in messages:
                email_data = await self._get_email_details(message['id'])
                if email_data:
                    # Parse LinkedIn-specific job data
                    parsed_jobs = await self._parse_linkedin_job_email(email_data)
                    linkedin_jobs.extend(parsed_jobs)
            
            return linkedin_jobs
            
        except Exception as e:
            print(f'LinkedIn email search error: {e}')
            return []
    
    async def _search_indeed_job_emails(self, keywords: List[str], days_back: int) -> List[Dict]:
        """Search specifically for Indeed job alert emails"""
        try:
            date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Indeed-specific search query
            query_parts = [
                f'after:{date_filter}',
                'from:indeed.com OR from:@indeed.com',
                '(jobs OR "job alert" OR "new jobs" OR "recommended jobs")',
                '-unsubscribe'
            ]
            
            # Add user keywords if provided
            if keywords:
                keyword_query = ' OR '.join([f'"{keyword}"' for keyword in keywords])
                query_parts.append(f'({keyword_query})')
            
            query = ' '.join(query_parts)
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=25
            ).execute()
            
            messages = results.get('messages', [])
            indeed_jobs = []
            
            for message in messages:
                email_data = await self._get_email_details(message['id'])
                if email_data:
                    # Parse Indeed-specific job data
                    parsed_jobs = await self._parse_indeed_job_email(email_data)
                    indeed_jobs.extend(parsed_jobs)
            
            return indeed_jobs
            
        except Exception as e:
            print(f'Indeed email search error: {e}')
            return []
    
    async def _search_general_job_emails(self, keywords: List[str], days_back: int) -> List[Dict]:
        """Search for general job-related emails"""
        try:
            date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Create search query for job-related emails
            job_keywords = ['job', 'position', 'opportunity', 'hiring', 'career', 'application']
            job_keywords.extend(keywords or [])
            
            # Build Gmail search query
            query_parts = []
            query_parts.append(f'after:{date_filter}')
            
            # Add keyword searches
            keyword_query = ' OR '.join([f'"{keyword}"' for keyword in job_keywords])
            query_parts.append(f'({keyword_query})')
            
            # Exclude common non-job emails and already processed emails
            exclude_terms = [
                'unsubscribe', 'newsletter', 'promotion', 'spam',
                '-from:linkedin.com', '-from:indeed.com'  # Exclude LinkedIn/Indeed since we handle them separately
            ]
            for term in exclude_terms:
                query_parts.append(f'{term}')
            
            query = ' '.join(query_parts)
            
            # Search emails
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=25
            ).execute()
            
            messages = results.get('messages', [])
            job_emails = []
            
            for message in messages:
                email_data = await self._get_email_details(message['id'])
                if email_data:
                    # Extract job information from general emails
                    job_info = await self._extract_job_information(email_data)
                    if job_info.get('is_job_posting'):
                        email_data.update(job_info)
                        job_emails.append(email_data)
            
            return job_emails
            
        except Exception as e:
            print(f'General job email search error: {e}')
            return []
    
    async def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            
            # Extract email metadata
            email_data = {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'snippet': message.get('snippet', ''),
                'date': None,
                'from': None,
                'to': None,
                'subject': None,
                'body': None,
                'attachments': []
            }
            
            # Parse headers
            for header in headers:
                name = header['name'].lower()
                value = header['value']
                
                if name == 'date':
                    email_data['date'] = value
                elif name == 'from':
                    email_data['from'] = value
                elif name == 'to':
                    email_data['to'] = value
                elif name == 'subject':
                    email_data['subject'] = value
            
            # Extract email body
            email_data['body'] = await self._extract_email_body(message['payload'])
            
            # Extract job-related information
            job_info = await self._extract_job_information(email_data)
            email_data.update(job_info)
            
            return email_data
            
        except HttpError as error:
            print(f'An error occurred getting email details: {error}')
            return None
    
    async def _extract_email_body(self, payload: Dict) -> str:
        """Extract the body text from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8')
                    # Convert HTML to plain text (basic conversion)
                    body = re.sub('<[^<]+?>', '', html_body)
        else:
            if payload['body'].get('data'):
                body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')
        
        return body
    
    async def _extract_job_information(self, email_data: Dict) -> Dict:
        """Extract job-specific information from email content"""
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        content = f"{subject} {body}"
        
        job_info = {
            'is_job_posting': False,
            'company_name': None,
            'position_title': None,
            'location': None,
            'salary_range': None,
            'job_type': None,
            'application_deadline': None,
            'job_url': None,
            'confidence_score': 0.0
        }
        
        # Check if this is likely a job posting
        job_indicators = [
            'job opening', 'position available', 'now hiring', 'job opportunity',
            'career opportunity', 'join our team', 'we are looking for',
            'job posting', 'employment opportunity', 'vacancy'
        ]
        
        confidence_score = 0.0
        for indicator in job_indicators:
            if indicator in content:
                confidence_score += 0.2
        
        if confidence_score > 0.3:
            job_info['is_job_posting'] = True
            job_info['confidence_score'] = min(confidence_score, 1.0)
            
            # Extract company name from sender
            from_email = email_data.get('from', '')
            if '@' in from_email:
                domain = from_email.split('@')[1].split('.')[0]
                job_info['company_name'] = domain.title()
            
            # Extract position title (basic pattern matching)
            title_patterns = [
                r'position[:\s]+([^\n\r]+)',
                r'role[:\s]+([^\n\r]+)',
                r'job[:\s]+([^\n\r]+)',
                r'hiring[:\s]+([^\n\r]+)'
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    job_info['position_title'] = match.group(1).strip()[:100]
                    break
            
            # Extract URLs (potential job posting links)
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, body)
            if urls:
                job_info['job_url'] = urls[0]  # Take the first URL found
        
        return job_info
    
    async def send_application_email(
        self, 
        to_email: str, 
        subject: str, 
        body: str, 
        attachments: List[Dict] = None
    ) -> bool:
        """
        Send an application email with resume and cover letter attachments
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            attachments: List of attachment dictionaries with 'filename' and 'content'
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            message = self._create_message_with_attachments(
                to_email, subject, body, attachments or []
            )
            
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            return True
            
        except HttpError as error:
            print(f'An error occurred sending email: {error}')
            return False
    
    def _create_message_with_attachments(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        attachments: List[Dict]
    ) -> Dict:
        """Create an email message with attachments"""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Add attachments
        for attachment in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment['content'])
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {attachment["filename"]}'
            )
            message.attach(part)
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    async def monitor_application_responses(self, application_emails: List[str]) -> List[Dict]:
        """
        Monitor for responses to job applications
        
        Args:
            application_emails: List of email addresses where applications were sent
            
        Returns:
            List of response emails with classification
        """
        try:
            responses = []
            
            for email_addr in application_emails:
                # Search for emails from this address in the last 30 days
                query = f'from:{email_addr} newer_than:30d'
                
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=10
                ).execute()
                
                messages = results.get('messages', [])
                
                for message in messages:
                    email_data = await self._get_email_details(message['id'])
                    if email_data:
                        # Classify the response
                        classification = await self._classify_application_response(email_data)
                        email_data['classification'] = classification
                        responses.append(email_data)
            
            return responses
            
        except HttpError as error:
            print(f'An error occurred monitoring responses: {error}')
            return []
    
    async def _classify_application_response(self, email_data: Dict) -> str:
        """
        Classify an application response email
        
        Returns:
            Classification: 'rejection', 'interview', 'offer', 'acknowledgment', 'other'
        """
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        content = f"{subject} {body}"
        
        # Rejection indicators
        rejection_keywords = [
            'unfortunately', 'regret to inform', 'not selected', 'not moving forward',
            'decided to pursue', 'other candidates', 'thank you for your interest',
            'position has been filled', 'not a match', 'declined'
        ]
        
        # Interview indicators
        interview_keywords = [
            'interview', 'schedule', 'meet', 'discuss', 'next step',
            'phone call', 'video call', 'in person', 'available times'
        ]
        
        # Offer indicators
        offer_keywords = [
            'offer', 'congratulations', 'pleased to offer', 'job offer',
            'welcome to', 'start date', 'salary', 'compensation'
        ]
        
        # Acknowledgment indicators
        ack_keywords = [
            'received your application', 'thank you for applying',
            'application received', 'under review', 'reviewing your'
        ]
        
        # Check for each classification
        if any(keyword in content for keyword in offer_keywords):
            return 'offer'
        elif any(keyword in content for keyword in interview_keywords):
            return 'interview'
        elif any(keyword in content for keyword in rejection_keywords):
            return 'rejection'
        elif any(keyword in content for keyword in ack_keywords):
            return 'acknowledgment'
        else:
            return 'other'
    
    async def _parse_linkedin_job_email(self, email_data: Dict) -> List[Dict]:
        """Parse LinkedIn job alert email to extract individual job postings"""
        jobs = []
        
        try:
            body = email_data.get('body', '')
            subject = email_data.get('subject', '')
            
            # Common LinkedIn job alert patterns
            job_patterns = [
                # Pattern 1: Job title at Company name
                r'([^\n]+)\s+at\s+([^\n]+?)(?:\s*\n|\s*-|\s*\|)',
                # Pattern 2: Company is hiring for Position
                r'([^\n]+?)\s+is\s+hiring\s+for\s+([^\n]+)',
                # Pattern 3: New job at Company
                r'New\s+job\s+at\s+([^\n]+?):\s*([^\n]+)',
            ]
            
            # Extract job URLs
            url_pattern = r'https://www\.linkedin\.com/jobs/view/\d+'
            job_urls = re.findall(url_pattern, body)
            
            # Extract job information using patterns
            for pattern in job_patterns:
                matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    if len(match) == 2:
                        title, company = match[0].strip(), match[1].strip()
                        
                        # Skip if title or company is too short/generic
                        if len(title) < 3 or len(company) < 2:
                            continue
                        
                        job = {
                            'title': title,
                            'company': company,
                            'source': 'linkedin_email',
                            'email_source': 'linkedin.com',
                            'description': self._extract_job_description_from_email(body, title),
                            'url': job_urls.pop(0) if job_urls else '',
                            'location': self._extract_location_from_email(body, title),
                            'posting_date': self._parse_email_date(email_data.get('date')),
                            'salary': None,  # LinkedIn emails rarely include salary
                            'job_type': 'fulltime',  # Default assumption
                            'remote_option': 'remote' in body.lower(),
                            'keywords': self._extract_keywords_from_email(body, title),
                            'confidence_score': 0.9,  # High confidence for LinkedIn emails
                            'match_score': 0.0,  # Will be calculated later
                            'ats_score': 0.7,  # LinkedIn jobs typically have good ATS compatibility
                            'email_id': email_data.get('id'),
                            'email_date': email_data.get('date'),
                            'requirements': [],
                            'benefits': [],
                            'experience_level': self._infer_experience_level(title),
                            'category': 'general'
                        }
                        jobs.append(job)
            
            # If no pattern matches, try to extract from subject line
            if not jobs and 'job' in subject.lower():
                job = {
                    'title': self._extract_title_from_subject(subject),
                    'company': 'LinkedIn',
                    'source': 'linkedin_email',
                    'email_source': 'linkedin.com',
                    'description': email_data.get('snippet', ''),
                    'url': job_urls[0] if job_urls else '',
                    'location': '',
                    'posting_date': self._parse_email_date(email_data.get('date')),
                    'salary': None,
                    'job_type': 'fulltime',
                    'remote_option': False,
                    'keywords': [],
                    'confidence_score': 0.6,
                    'match_score': 0.0,
                    'ats_score': 0.7,
                    'email_id': email_data.get('id'),
                    'email_date': email_data.get('date'),
                    'requirements': [],
                    'benefits': [],
                    'experience_level': 'mid',
                    'category': 'general'
                }
                jobs.append(job)
            
        except Exception as e:
            print(f'Error parsing LinkedIn email: {e}')
        
        return jobs
    
    async def _parse_indeed_job_email(self, email_data: Dict) -> List[Dict]:
        """Parse Indeed job alert email to extract individual job postings"""
        jobs = []
        
        try:
            body = email_data.get('body', '')
            subject = email_data.get('subject', '')
            
            # Common Indeed job alert patterns
            job_patterns = [
                # Pattern 1: Job title - Company name
                r'([^\n]+?)\s*-\s*([^\n]+?)(?:\s*\n|\s*View Job)',
                # Pattern 2: Company name is hiring Position
                r'([^\n]+?)\s+is\s+hiring\s+([^\n]+)',
                # Pattern 3: Position at Company
                r'([^\n]+)\s+at\s+([^\n]+?)(?:\s*\n|\s*-|\s*\$)',
            ]
            
            # Extract job URLs
            url_pattern = r'https://www\.indeed\.com/viewjob\?jk=[a-zA-Z0-9]+'
            job_urls = re.findall(url_pattern, body)
            
            # Extract salary information
            salary_pattern = r'\$([0-9,]+)(?:\s*-\s*\$([0-9,]+))?(?:\s*(?:per\s+hour|hourly|/hr|annually|per\s+year|/year))?'
            salaries = re.findall(salary_pattern, body)
            
            # Extract locations
            location_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})'
            locations = re.findall(location_pattern, body)
            
            # Extract job information using patterns
            for pattern in job_patterns:
                matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
                
                for i, match in enumerate(matches):
                    if len(match) == 2:
                        title, company = match[0].strip(), match[1].strip()
                        
                        # Skip if title or company is too short/generic
                        if len(title) < 3 or len(company) < 2:
                            continue
                        
                        # Get corresponding URL, salary, and location
                        job_url = job_urls[i] if i < len(job_urls) else ''
                        salary_info = self._parse_indeed_salary(salaries[i]) if i < len(salaries) else None
                        location = locations[i] if i < len(locations) else ''
                        
                        job = {
                            'title': title,
                            'company': company,
                            'source': 'indeed_email',
                            'email_source': 'indeed.com',
                            'description': self._extract_job_description_from_email(body, title),
                            'url': job_url,
                            'location': location,
                            'posting_date': self._parse_email_date(email_data.get('date')),
                            'salary': salary_info,
                            'job_type': self._infer_job_type_from_title(title),
                            'remote_option': 'remote' in body.lower() or 'work from home' in body.lower(),
                            'keywords': self._extract_keywords_from_email(body, title),
                            'confidence_score': 0.9,  # High confidence for Indeed emails
                            'match_score': 0.0,  # Will be calculated later
                            'ats_score': 0.8,  # Indeed jobs typically have good ATS compatibility
                            'email_id': email_data.get('id'),
                            'email_date': email_data.get('date'),
                            'requirements': [],
                            'benefits': [],
                            'experience_level': self._infer_experience_level(title),
                            'category': 'general'
                        }
                        jobs.append(job)
            
            # If no pattern matches, try to extract from subject line
            if not jobs and 'job' in subject.lower():
                job = {
                    'title': self._extract_title_from_subject(subject),
                    'company': 'Indeed',
                    'source': 'indeed_email',
                    'email_source': 'indeed.com',
                    'description': email_data.get('snippet', ''),
                    'url': job_urls[0] if job_urls else '',
                    'location': locations[0] if locations else '',
                    'posting_date': self._parse_email_date(email_data.get('date')),
                    'salary': self._parse_indeed_salary(salaries[0]) if salaries else None,
                    'job_type': 'fulltime',
                    'remote_option': False,
                    'keywords': [],
                    'confidence_score': 0.6,
                    'match_score': 0.0,
                    'ats_score': 0.8,
                    'email_id': email_data.get('id'),
                    'email_date': email_data.get('date'),
                    'requirements': [],
                    'benefits': [],
                    'experience_level': 'mid',
                    'category': 'general'
                }
                jobs.append(job)
            
        except Exception as e:
            print(f'Error parsing Indeed email: {e}')
        
        return jobs
    
    def _extract_job_description_from_email(self, body: str, title: str) -> str:
        """Extract job description from email body around the job title"""
        
        # Find the section of the email containing this job
        title_lower = title.lower()
        body_lower = body.lower()
        
        title_index = body_lower.find(title_lower)
        if title_index == -1:
            return body[:300]  # Return first 300 chars if title not found
        
        # Extract 200 characters around the title
        start = max(0, title_index - 100)
        end = min(len(body), title_index + len(title) + 200)
        
        description = body[start:end].strip()
        
        # Clean up the description
        description = re.sub(r'\s+', ' ', description)  # Normalize whitespace
        description = re.sub(r'View Job.*?$', '', description, flags=re.IGNORECASE)  # Remove "View Job" links
        
        return description[:500]  # Limit to 500 characters
    
    def _extract_location_from_email(self, body: str, title: str) -> str:
        """Extract location information from email body"""
        
        # Common location patterns
        location_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})',  # "San Francisco, CA"
            r'([A-Z][a-z]+,\s*[A-Z][a-z]+)',  # "Boston, Massachusetts"
            r'\b(Remote)\b',  # "Remote"
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b'  # "New York"
        ]
        
        # Search around the job title
        title_lower = title.lower()
        body_lower = body.lower()
        title_index = body_lower.find(title_lower)
        
        if title_index != -1:
            # Search in 200 characters around the title
            start = max(0, title_index - 100)
            end = min(len(body), title_index + len(title) + 100)
            search_area = body[start:end]
            
            for pattern in location_patterns:
                match = re.search(pattern, search_area)
                if match:
                    return match.group(1)
        
        # If not found around title, search entire email
        for pattern in location_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(1)
        
        return ''
    
    def _extract_keywords_from_email(self, body: str, title: str) -> List[str]:
        """Extract relevant keywords from job email"""
        
        text = f"{title} {body}".lower()
        
        # Common job keywords
        keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'sql', 'database', 'aws', 'cloud', 'docker', 'kubernetes',
            'machine learning', 'data science', 'ai', 'analytics',
            'frontend', 'backend', 'fullstack', 'devops', 'mobile',
            'agile', 'scrum', 'remote', 'senior', 'junior', 'lead'
        ]
        
        found_keywords = []
        for keyword in keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords[:10]  # Limit to top 10
    
    def _parse_email_date(self, date_string: str) -> Optional[datetime]:
        """Parse email date string to datetime"""
        if not date_string:
            return None
        
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_string)
        except Exception:
            return datetime.utcnow()
    
    def _parse_indeed_salary(self, salary_match) -> Optional[Dict]:
        """Parse Indeed salary information"""
        if not salary_match or not salary_match[0]:
            return None
        
        try:
            min_salary = int(salary_match[0].replace(',', ''))
            max_salary = int(salary_match[1].replace(',', '')) if salary_match[1] else None
            
            return {
                'min': min_salary,
                'max': max_salary,
                'currency': 'USD',
                'type': 'yearly'
            }
        except (ValueError, IndexError):
            return None
    
    def _infer_experience_level(self, title: str) -> str:
        """Infer experience level from job title"""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ['senior', 'sr.', 'lead', 'principal', 'staff']):
            return 'senior'
        elif any(term in title_lower for term in ['junior', 'jr.', 'entry', 'associate']):
            return 'junior'
        elif any(term in title_lower for term in ['intern', 'internship']):
            return 'internship'
        else:
            return 'mid'
    
    def _infer_job_type_from_title(self, title: str) -> str:
        """Infer job type from title"""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ['part time', 'part-time', 'parttime']):
            return 'parttime'
        elif any(term in title_lower for term in ['contract', 'contractor', 'freelance']):
            return 'contract'
        elif any(term in title_lower for term in ['intern', 'internship']):
            return 'internship'
        else:
            return 'fulltime'
    
    def _extract_title_from_subject(self, subject: str) -> str:
        """Extract job title from email subject line"""
        
        # Remove common email prefixes
        subject = re.sub(r'^(re:|fwd?:|new\s+job\s*alert?:?|job\s*alert:?)\s*', '', subject, flags=re.IGNORECASE)
        
        # Remove bracketed content
        subject = re.sub(r'\[.*?\]', '', subject)
        
        # Remove parenthetical content
        subject = re.sub(r'\(.*?\)', '', subject)
        
        # Clean up and limit length
        subject = subject.strip()[:100]
        
        return subject if subject else 'Job Opportunity'
    
    def _remove_duplicate_emails(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs from email parsing"""
        
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create unique key based on title and company
            key = (
                job.get('title', '').lower().strip(),
                job.get('company', '').lower().strip()
            )
            
            if key not in seen and key != ('', ''):
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs