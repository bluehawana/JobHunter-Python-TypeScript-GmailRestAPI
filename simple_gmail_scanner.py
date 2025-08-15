#!/usr/bin/env python3
"""
Simple Gmail Scanner - Scan for real job emails using IMAP
Only processes real LinkedIn, Indeed, and company job emails
"""
import imaplib
import email
import re
import os
import sys
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

# Add backend to path and load environment
sys.path.append('backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')

logger = logging.getLogger(__name__)

class SimpleGmailScanner:
    def __init__(self):
        # Scan job ads from bluehawana@gmail.com (where LinkedIn/Indeed alerts arrive)
        self.gmail_user = 'bluehawana@gmail.com'
        self.gmail_password = os.getenv('BLUEHAWANA_GMAIL_PASSWORD')  # Need this password
        
        # Fallback to sender credentials if bluehawana password not available
        if not self.gmail_password:
            self.gmail_user = 'leeharvad@gmail.com'
            self.gmail_password = os.getenv('SENDER_GMAIL_PASSWORD')
        
    def scan_for_real_jobs(self, days_back: int = 3) -> List[Dict[str, Any]]:
        """Scan Gmail for real job opportunities"""
        # Check if we have bluehawana Gmail password (where job alerts arrive)
        bluehawana_password = os.getenv('BLUEHAWANA_GMAIL_PASSWORD')
        
        if not bluehawana_password:
            logger.warning("⚠️ Bluehawana Gmail password not configured - using manual job input")
            # Use manual job input as fallback
            from manual_job_input import get_real_jobs_from_bluehawana
            manual_jobs = get_real_jobs_from_bluehawana()
            logger.info(f"📧 Using manual job input: {len(manual_jobs)} jobs available")
            return manual_jobs
        
        try:
            logger.info(f"📧 Connecting to Gmail for {self.gmail_user}...")
            
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_user, self.gmail_password)
            mail.select('inbox')
            
            # Calculate date range
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Search for job-related emails
            job_searches = [
                # LinkedIn job alerts
                f'(FROM "linkedin.com" SUBJECT "job" SINCE {since_date})',
                f'(FROM "linkedin.com" SUBJECT "opportunity" SINCE {since_date})',
                f'(FROM "linkedin.com" SUBJECT "hiring" SINCE {since_date})',
                
                # Indeed job alerts  
                f'(FROM "indeed.com" SUBJECT "job" SINCE {since_date})',
                f'(FROM "indeed.com" SUBJECT "alert" SINCE {since_date})',
                
                # General job emails
                f'(SUBJECT "job opportunity" SINCE {since_date})',
                f'(SUBJECT "career opportunity" SINCE {since_date})',
                f'(SUBJECT "we are hiring" SINCE {since_date})',
                f'(SUBJECT "position available" SINCE {since_date})',
                
                # Swedish job terms
                f'(SUBJECT "tjänst" SINCE {since_date})',
                f'(SUBJECT "utvecklare" SINCE {since_date})',
            ]
            
            all_jobs = []
            processed_subjects = set()  # Avoid duplicates
            
            for search_query in job_searches:
                try:
                    logger.info(f"🔍 Searching: {search_query}")
                    
                    status, messages = mail.search(None, search_query)
                    
                    if status == 'OK':
                        message_ids = messages[0].split()
                        logger.info(f"📧 Found {len(message_ids)} emails for this search")
                        
                        for msg_id in message_ids[-10:]:  # Process last 10 emails
                            try:
                                job_info = self._process_email(mail, msg_id)
                                
                                if job_info and job_info['subject'] not in processed_subjects:
                                    # Check if it's in Gothenburg area or remote
                                    if self._is_relevant_location(job_info.get('location', '')):
                                        all_jobs.append(job_info)
                                        processed_subjects.add(job_info['subject'])
                                        logger.info(f"✅ Found job: {job_info['company']} - {job_info['title']}")
                                
                            except Exception as e:
                                logger.warning(f"⚠️ Error processing email {msg_id}: {e}")
                                continue
                
                except Exception as e:
                    logger.warning(f"⚠️ Search failed for {search_query}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
            logger.info(f"✅ Gmail scan complete: {len(all_jobs)} real job opportunities found")
            return all_jobs
            
        except Exception as e:
            logger.error(f"❌ Gmail scanning failed: {e}")
            return []
    
    def _process_email(self, mail, msg_id) -> Dict[str, Any]:
        """Process individual email to extract job information"""
        try:
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract basic email info
            subject = email_message['Subject'] or ''
            from_addr = email_message['From'] or ''
            date_str = email_message['Date'] or ''
            
            # Get email body
            body = self._get_email_body(email_message)
            
            # Extract job information
            job_info = self._extract_job_info(subject, body, from_addr)
            
            if job_info:
                job_info.update({
                    'subject': subject,
                    'from': from_addr,
                    'date': date_str,
                    'source': 'gmail_real',
                    'email_body': body[:500]  # First 500 chars for context
                })
                
                return job_info
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Error processing email: {e}")
            return None
    
    def _get_email_body(self, email_message) -> str:
        """Extract text body from email message"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif part.get_content_type() == "text/html" and not body:
                    html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    # Simple HTML to text conversion
                    body = re.sub('<[^<]+?>', '', html_body)
        else:
            body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body
    
    def _extract_job_info(self, subject: str, body: str, from_addr: str) -> Dict[str, Any]:
        """Extract job information from email content"""
        
        # Determine if this is a job-related email
        job_indicators = [
            'job', 'position', 'opportunity', 'hiring', 'career',
            'developer', 'engineer', 'tjänst', 'utvecklare'
        ]
        
        content = (subject + ' ' + body).lower()
        
        if not any(indicator in content for indicator in job_indicators):
            return None
        
        # Extract company name
        company = self._extract_company(from_addr, subject, body)
        
        # Extract job title
        title = self._extract_job_title(subject, body)
        
        # Extract location
        location = self._extract_location(subject + ' ' + body)
        
        # Extract job URL if present
        job_url = self._extract_job_url(body)
        
        return {
            'company': company,
            'title': title,
            'location': location,
            'description': body[:300],  # First 300 chars
            'url': job_url,
            'requirements': self._extract_requirements(body),
        }
    
    def _extract_company(self, from_addr: str, subject: str, body: str) -> str:
        """Extract company name from email"""
        
        # Try to get company from email domain
        if '@' in from_addr:
            domain = from_addr.split('@')[1].split('.')[0]
            
            # Known job sites
            if domain in ['linkedin', 'indeed', 'glassdoor', 'monster']:
                # Try to extract company from subject/body
                company_patterns = [
                    r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s|$|,|\.|!)',
                    r'från\s+([A-Z][a-zA-Z\s&]+?)(?:\s|$|,|\.|!)',
                    r'hos\s+([A-Z][a-zA-Z\s&]+?)(?:\s|$|,|\.|!)',
                ]
                
                for pattern in company_patterns:
                    match = re.search(pattern, subject + ' ' + body)
                    if match:
                        return match.group(1).strip()[:50]
                
                return domain.title()
            else:
                return domain.title()
        
        return "Unknown Company"
    
    def _extract_job_title(self, subject: str, body: str) -> str:
        """Extract job title from subject and body"""
        
        # Common job title patterns
        title_patterns = [
            r'(Senior\s+)?DevOps\s+Engineer',
            r'(Senior\s+)?Backend\s+Developer',
            r'(Senior\s+)?Fullstack\s+Developer',
            r'(Senior\s+)?Software\s+Engineer',
            r'(Senior\s+)?System\s+Engineer',
            r'(Senior\s+)?Cloud\s+Engineer',
            r'Utvecklare',
            r'Systemutvecklare',
        ]
        
        content = subject + ' ' + body
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Fallback: look for job-related words in subject
        if any(word in subject.lower() for word in ['developer', 'engineer', 'utvecklare']):
            return subject[:50]
        
        return "Software Developer"
    
    def _extract_location(self, content: str) -> str:
        """Extract location from content"""
        
        # Gothenburg area patterns
        gothenburg_patterns = [
            r'Göteborg', r'Gothenburg', r'Goteborg',
            r'Mölndal', r'Molndal', r'Partille', r'Lerum'
        ]
        
        for pattern in gothenburg_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return pattern
        
        # Remote work patterns
        if re.search(r'\b(remote|distans|hemarbete)\b', content, re.IGNORECASE):
            return "Remote"
        
        # Sweden patterns
        if re.search(r'Sweden|Sverige', content, re.IGNORECASE):
            return "Sweden"
        
        return "Not specified"
    
    def _extract_job_url(self, body: str) -> str:
        """Extract job URL from email body"""
        
        url_patterns = [
            r'https://www\.linkedin\.com/jobs/view/\d+',
            r'https://[a-zA-Z0-9.-]+\.indeed\.com/viewjob\?jk=[a-zA-Z0-9]+',
            r'https://[a-zA-Z0-9.-]+/jobs?/[a-zA-Z0-9-]+',
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_requirements(self, body: str) -> str:
        """Extract job requirements from body"""
        
        tech_keywords = [
            'kubernetes', 'docker', 'aws', 'azure', 'gcp',
            'python', 'java', 'javascript', 'react', 'node.js',
            'devops', 'ci/cd', 'jenkins', 'git', 'linux',
            'prometheus', 'grafana', 'terraform', 'ansible'
        ]
        
        found_keywords = []
        body_lower = body.lower()
        
        for keyword in tech_keywords:
            if keyword in body_lower:
                found_keywords.append(keyword)
        
        return ', '.join(found_keywords[:10])  # Limit to 10 keywords
    
    def _is_relevant_location(self, location: str) -> bool:
        """Check if location is relevant (Gothenburg area or remote)"""
        
        if not location:
            return True  # Include if location not specified
        
        location_lower = location.lower()
        
        # Gothenburg area
        gothenburg_keywords = [
            'göteborg', 'gothenburg', 'goteborg', 'mölndal', 'molndal',
            'partille', 'lerum', 'remote', 'distans', 'hemarbete'
        ]
        
        return any(keyword in location_lower for keyword in gothenburg_keywords)

def scan_real_gmail_jobs() -> List[Dict[str, Any]]:
    """Main function to scan Gmail for real jobs"""
    scanner = SimpleGmailScanner()
    return scanner.scan_for_real_jobs()

if __name__ == "__main__":
    # Test the Gmail scanner
    jobs = scan_real_gmail_jobs()
    
    print(f"📧 REAL GMAIL JOB SCAN")
    print(f"=" * 40)
    print(f"Found {len(jobs)} real job opportunities")
    
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['company']} - {job['title']}")
        print(f"   📍 {job['location']}")
        print(f"   📧 From: {job['from']}")
        if job.get('url'):
            print(f"   🔗 {job['url']}")