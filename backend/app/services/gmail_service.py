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
        Search for job-related emails in Gmail
        
        Args:
            keywords: List of keywords to search for
            days_back: Number of days to look back
            
        Returns:
            List of job-related emails with metadata
        """
        try:
            # Build search query
            date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Create search query for job-related emails
            job_keywords = ['job', 'position', 'opportunity', 'hiring', 'career', 'application']
            job_keywords.extend(keywords)
            
            # Build Gmail search query
            query_parts = []
            query_parts.append(f'after:{date_filter}')
            
            # Add keyword searches
            keyword_query = ' OR '.join([f'"{keyword}"' for keyword in job_keywords])
            query_parts.append(f'({keyword_query})')
            
            # Exclude common non-job emails
            exclude_terms = ['unsubscribe', 'newsletter', 'promotion', 'spam']
            for term in exclude_terms:
                query_parts.append(f'-{term}')
            
            query = ' '.join(query_parts)
            
            # Search emails
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            job_emails = []
            
            for message in messages:
                email_data = await self._get_email_details(message['id'])
                if email_data:
                    job_emails.append(email_data)
            
            return job_emails
            
        except HttpError as error:
            print(f'An error occurred: {error}')
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