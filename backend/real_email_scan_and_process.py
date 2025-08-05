#!/usr/bin/env python3
"""
Real Email Scanning and Job Processing System

This script will:
1. Scan bluehawana@gmail.com for real job emails
2. Extract job details from LinkedIn, Indeed, and other job boards
3. Generate customized CV and cover letter for each job
4. Send processed applications to leeharvad@gmail.com

Usage: python real_email_scan_and_process.py
"""

import asyncio
import sys
import os
import logging
from datetime import datetime, timedelta
import imaplib
import email
import re
from email.header import decode_header
from typing import List, Dict, Optional

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealEmailScanner:
    """Real email scanner for bluehawana@gmail.com"""
    
    def __init__(self):
        self.email_address = "bluehawana@gmail.com"
        self.app_password = "vsodrpyblpgtujof"  # From .env file
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
    
    async def scan_for_job_emails(self, days_back: int = 7) -> List[Dict]:
        """Scan Gmail for real job-related emails"""
        try:
            logger.info(f"🔍 Connecting to {self.email_address}...")
            
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.app_password)
            
            # Select inbox
            mail.select('inbox')
            
            # Calculate date filter
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            logger.info(f"📅 Scanning emails since {since_date}")
            
            job_emails = []
            
            # Search patterns for different job sources
            search_patterns = [
                # LinkedIn job alerts
                '(FROM "linkedin.com" SUBJECT "job")',
                '(FROM "linkedin.com" SUBJECT "opportunity")',
                '(FROM "linkedin.com" SUBJECT "position")',
                
                # Indeed job alerts
                '(FROM "indeed.com" SUBJECT "job")',
                '(FROM "indeed.com" SUBJECT "alert")',
                
                # Other job boards
                '(FROM "glassdoor.com")',
                '(FROM "monster.com")',
                '(FROM "ziprecruiter.com")',
                
                # Company direct emails
                '(SUBJECT "job" SUBJECT "opportunity")',
                '(SUBJECT "position" SUBJECT "available")',
                '(SUBJECT "hiring" SUBJECT "career")',
                
                # Volvo specific
                '(FROM "volvo" OR SUBJECT "volvo")',
                '(SUBJECT "IT support" OR SUBJECT "technical support")',
            ]
            
            for pattern in search_patterns:
                try:
                    search_criteria = f'(SINCE {since_date} {pattern})'
                    logger.info(f"🔎 Searching with pattern: {pattern}")
                    
                    status, messages = mail.search(None, search_criteria)
                    
                    if status == 'OK' and messages[0]:
                        message_ids = messages[0].split()
                        logger.info(f"📧 Found {len(message_ids)} emails matching pattern")
                        
                        # Process each email (limit to last 5 per pattern)
                        for msg_id in message_ids[-5:]:
                            try:
                                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                                if status != 'OK':
                                    continue
                                    
                                email_body = msg_data[0][1]
                                email_message = email.message_from_bytes(email_body)
                                
                                # Parse email for job information
                                job_info = await self._parse_job_email(email_message)
                                if job_info:
                                    job_emails.append(job_info)
                                    
                            except Exception as e:
                                logger.error(f"Error processing email {msg_id}: {e}")
                                continue
                                
                except Exception as e:
                    logger.error(f"Error with search pattern {pattern}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
            # Remove duplicates based on job URL or title+company
            unique_jobs = self._remove_duplicate_jobs(job_emails)
            
            logger.info(f"✅ Found {len(unique_jobs)} unique job opportunities")
            return unique_jobs
            
        except Exception as e:
            logger.error(f"❌ Error scanning emails: {e}")
            return []
    
    async def _parse_job_email(self, email_message) -> Optional[Dict]:
        """Parse individual email for job information"""
        try:
            subject = self._decode_header(email_message['Subject'])
            sender = self._decode_header(email_message['From'])
            date_received = email_message['Date']
            body = self._get_email_body(email_message)
            
            # Skip if not job-related
            if not self._is_job_related(subject, body, sender):
                return None
            
            # Extract job details
            job_info = {
                'id': f"email_{hash(subject + sender + str(date_received))}",
                'email_subject': subject,
                'sender': sender,
                'date_received': self._parse_date(date_received),
                'body': body[:1000],  # First 1000 chars
                'source': self._determine_source(sender, body),
                'title': self._extract_job_title(subject, body),
                'company': self._extract_company_name(sender, body),
                'location': self._extract_location(body),
                'description': self._extract_job_description(body),
                'url': self._extract_job_url(body),
                'keywords': self._extract_keywords(subject, body),
                'job_type': self._extract_job_type(body),
                'remote_option': self._check_remote_option(body),
                'confidence_score': self._calculate_confidence_score(subject, body, sender)
            }
            
            # Only return if confidence score is high enough
            if job_info['confidence_score'] >= 0.6:
                logger.info(f"📋 Found job: {job_info['title']} at {job_info['company']} (confidence: {job_info['confidence_score']:.2f})")
                return job_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing job email: {e}")
            return None
    
    def _decode_header(self, header) -> str:
        """Decode email header"""
        if header is None:
            return ""
        
        try:
            decoded_parts = decode_header(header)
            decoded_header = ""
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    decoded_header += part.decode(encoding or 'utf-8')
                else:
                    decoded_header += part
            
            return decoded_header
        except:
            return str(header)
    
    def _get_email_body(self, email_message) -> str:
        """Extract email body text"""
        body = ""
        
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    if (content_type == "text/plain" and 
                        "attachment" not in content_disposition):
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        except:
                            continue
            else:
                try:
                    body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    body = str(email_message.get_payload())
        except:
            body = ""
        
        return body
    
    def _is_job_related(self, subject: str, body: str, sender: str) -> bool:
        """Check if email is job-related"""
        job_keywords = [
            'job', 'position', 'opportunity', 'hiring', 'career', 'vacancy',
            'employment', 'opening', 'role', 'work', 'apply', 'application',
            'developer', 'engineer', 'support', 'analyst', 'manager',
            'volvo', 'energy', 'IT support', 'technical support'
        ]
        
        content = f"{subject} {body} {sender}".lower()
        
        # Check for job keywords
        keyword_matches = sum(1 for keyword in job_keywords if keyword in content)
        
        # Check for job board domains
        job_domains = ['linkedin.com', 'indeed.com', 'glassdoor.com', 'monster.com', 'ziprecruiter.com']
        domain_match = any(domain in sender.lower() for domain in job_domains)
        
        # Check for company emails with job content
        company_indicators = ['hr@', 'careers@', 'jobs@', 'recruiting@', 'talent@']
        company_match = any(indicator in sender.lower() for indicator in company_indicators)
        
        return keyword_matches >= 2 or domain_match or company_match
    
    def _determine_source(self, sender: str, body: str) -> str:
        """Determine the source of the job posting"""
        sender_lower = sender.lower()
        
        if 'linkedin' in sender_lower:
            return 'linkedin'
        elif 'indeed' in sender_lower:
            return 'indeed'
        elif 'glassdoor' in sender_lower:
            return 'glassdoor'
        elif 'monster' in sender_lower:
            return 'monster'
        elif 'volvo' in sender_lower or 'volvo' in body.lower():
            return 'volvo'
        else:
            return 'direct_email'
    
    def _extract_job_title(self, subject: str, body: str) -> str:
        """Extract job title from email"""
        # Common patterns for job titles in subjects
        title_patterns = [
            r'(?:job|position|role|opportunity):\s*([^\\n\\r,]+)',
            r'([^\\n\\r,]+?)\s*(?:position|role|job|opportunity)',
            r'hiring\s+([^\\n\\r,]+)',
            r'([^\\n\\r,]+?)\s*at\s+[^\\n\\r,]+',
            r'apply\s+for\s+([^\\n\\r,]+)',
        ]
        
        content = f"{subject} {body[:200]}"
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 3 and len(title) < 100:
                    return title
        
        # Fallback: look for common job titles
        common_titles = [
            'software developer', 'software engineer', 'fullstack developer',
            'backend developer', 'frontend developer', 'web developer',
            'IT support', 'technical support', 'system administrator',
            'data analyst', 'project manager', 'product manager'
        ]
        
        content_lower = content.lower()
        for title in common_titles:
            if title in content_lower:
                return title.title()
        
        return "Software Developer Position"
    
    def _extract_company_name(self, sender: str, body: str) -> str:
        """Extract company name from email"""
        # Try to extract from sender email
        if '@' in sender:
            domain_part = sender.split('@')[1].split('.')[0]
            if domain_part not in ['linkedin', 'indeed', 'glassdoor', 'monster', 'gmail', 'yahoo']:
                return domain_part.title()
        
        # Look for company patterns in body
        company_patterns = [
            r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\\n|,)',
            r'([A-Z][a-zA-Z\s&]+?)\s+is\s+(?:hiring|looking|seeking)',
            r'join\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\\n)',
            r'([A-Z][a-zA-Z\s&]+?)\s+team',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, body)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 50:
                    return company
        
        # Check for Volvo specifically
        if 'volvo' in body.lower() or 'volvo' in sender.lower():
            return "Volvo Energy"
        
        return "Technology Company"
    
    def _extract_location(self, body: str) -> str:
        """Extract location from email body"""
        location_patterns = [
            r'([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*,\\s*[A-Z]{2})',  # "San Francisco, CA"
            r'([A-Z][a-z]+,\\s*Sweden)',  # "Stockholm, Sweden"
            r'\\b(Remote)\\b',  # "Remote"
            r'([A-Z][a-z]+,\\s*[A-Z][a-z]+)',  # "Boston, Massachusetts"
            r'(Stockholm|Gothenburg|Malmö|Uppsala|Västerås|Örebro)',  # Swedish cities
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(1)
        
        return "Sweden"
    
    def _extract_job_description(self, body: str) -> str:
        """Extract job description from email body"""
        # Clean up the body text
        description = re.sub(r'\\s+', ' ', body)
        description = re.sub(r'[\\r\\n]+', ' ', description)
        
        # Try to find the main job description section
        desc_patterns = [
            r'(?:description|about|role|responsibilities|requirements)[:.]\\s*([^\\n]{100,500})',
            r'we are (?:looking|seeking|hiring)\\s+([^\\n]{100,500})',
            r'join (?:our|us)\\s+([^\\n]{100,500})',
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:500]
        
        # Fallback: return first 300 characters
        return description[:300].strip()
    
    def _extract_job_url(self, body: str) -> str:
        """Extract job application URL from email body"""
        url_patterns = [
            r'https://www\\.linkedin\\.com/jobs/view/\\d+',
            r'https://[^\\s]+\\.indeed\\.com/viewjob\\?jk=[a-zA-Z0-9]+',
            r'https://[^\\s]+\\.glassdoor\\.com/job-listing/[^\\s]+',
            r'https://[^\\s]+/jobs?/[^\\s]+',
            r'https://[^\\s]+/careers?/[^\\s]+',
            r'https://[^\\s]+/apply[^\\s]*',
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_keywords(self, subject: str, body: str) -> List[str]:
        """Extract technical keywords from email content"""
        content = f"{subject} {body}".lower()
        
        tech_keywords = [
            'java', 'spring', 'spring boot', 'python', 'javascript', 'typescript',
            'react', 'angular', 'vue', 'node.js', 'c#', '.net', '.net core',
            'aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker', 'devops',
            'postgresql', 'mysql', 'mongodb', 'sql', 'nosql',
            'microservices', 'api', 'rest', 'restful', 'graphql',
            'ci/cd', 'jenkins', 'git', 'agile', 'scrum',
            'fullstack', 'frontend', 'backend', 'web development',
            'IT support', 'technical support', 'system administration',
            'network', 'security', 'infrastructure', 'helpdesk'
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        return found_keywords[:10]
    
    def _extract_job_type(self, body: str) -> str:
        """Extract job type from email body"""
        body_lower = body.lower()
        
        if 'part-time' in body_lower or 'part time' in body_lower:
            return 'part-time'
        elif 'contract' in body_lower or 'contractor' in body_lower:
            return 'contract'
        elif 'freelance' in body_lower:
            return 'freelance'
        elif 'internship' in body_lower or 'intern' in body_lower:
            return 'internship'
        else:
            return 'full-time'
    
    def _check_remote_option(self, body: str) -> bool:
        """Check if job offers remote work option"""
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'telecommute']
        body_lower = body.lower()
        
        return any(keyword in body_lower for keyword in remote_keywords)
    
    def _calculate_confidence_score(self, subject: str, body: str, sender: str) -> float:
        """Calculate confidence score for job relevance"""
        score = 0.0
        
        # Job board emails get high confidence
        job_domains = ['linkedin.com', 'indeed.com', 'glassdoor.com']
        if any(domain in sender.lower() for domain in job_domains):
            score += 0.4
        
        # Job keywords in subject
        job_keywords = ['job', 'position', 'opportunity', 'hiring', 'career']
        subject_lower = subject.lower()
        for keyword in job_keywords:
            if keyword in subject_lower:
                score += 0.1
        
        # Technical keywords in content
        tech_keywords = ['developer', 'engineer', 'support', 'IT', 'technical']
        content_lower = f"{subject} {body}".lower()
        for keyword in tech_keywords:
            if keyword in content_lower:
                score += 0.1
        
        # Company-specific indicators
        if 'volvo' in content_lower:
            score += 0.2
        
        # URL presence
        if 'http' in body:
            score += 0.1
        
        return min(score, 1.0)
    
    def _remove_duplicate_jobs(self, job_emails: List[Dict]) -> List[Dict]:
        """Remove duplicate job postings"""
        seen = set()
        unique_jobs = []
        
        for job in job_emails:
            # Create a unique identifier
            identifier = f"{job['title']}_{job['company']}_{job['source']}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse email date string"""
        if not date_string:
            return None
        
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_string)
        except:
            return datetime.utcnow()

async def main():
    """Main function to run real email scanning and job processing"""
    print("🚀 REAL EMAIL SCANNING AND JOB PROCESSING")
    print("=" * 60)
    print("📧 Scanning bluehawana@gmail.com for actual job opportunities...")
    print("🎯 Looking for IT support positions at Volvo Energy and other opportunities")
    print()
    
    try:
        # Initialize email scanner
        scanner = RealEmailScanner()
        
        # Scan for job emails (last 7 days)
        print("🔍 Step 1: Scanning emails from the last 7 days...")
        job_opportunities = await scanner.scan_for_job_emails(days_back=7)
        
        if not job_opportunities:
            print("📭 No job opportunities found in recent emails.")
            print("💡 Try increasing the days_back parameter or check email filters.")
            return
        
        print(f"✅ Found {len(job_opportunities)} job opportunities!")
        print()
        
        # Display found jobs
        print("📋 FOUND JOB OPPORTUNITIES:")
        print("-" * 40)
        
        for i, job in enumerate(job_opportunities, 1):
            print(f"{i}. 📌 {job['title']} at {job['company']}")
            print(f"   📍 Location: {job['location']}")
            print(f"   📧 Source: {job['source']} (confidence: {job['confidence_score']:.2f})")
            print(f"   🏷️  Keywords: {', '.join(job['keywords'][:5])}")
            if job['url']:
                print(f"   🔗 URL: {job['url']}")
            print(f"   📅 Received: {job['date_received'].strftime('%Y-%m-%d %H:%M') if job['date_received'] else 'Unknown'}")
            print()
        
        # Process jobs with document generation
        print("📄 Step 2: Processing jobs and generating documents...")
        
        # Import job processor
        try:
            from app.services.job_application_processor import JobApplicationProcessor
            processor = JobApplicationProcessor()
            
            processed_jobs = []
            
            for i, job in enumerate(job_opportunities, 1):
                print(f"\\n🔄 Processing job {i}/{len(job_opportunities)}: {job['title']} at {job['company']}")
                
                try:
                    # Generate documents
                    processed_job = await processor.process_job_and_generate_documents(job)
                    
                    if processed_job['status'] == 'success':
                        print("   ✅ Documents generated successfully")
                        
                        # Send email
                        email_sent = await processor.send_job_application_email(processed_job)
                        processed_job['email_sent'] = email_sent
                        
                        if email_sent:
                            print("   📤 Application email sent to leeharvad@gmail.com")
                        else:
                            print("   ❌ Failed to send email")
                    else:
                        print(f"   ❌ Document generation failed: {processed_job.get('error', 'Unknown error')}")
                    
                    processed_jobs.append(processed_job)
                    
                    # Add delay between jobs
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing job {job['title']}: {e}")
                    print(f"   ❌ Error processing job: {e}")
        
        except ImportError as e:
            print(f"❌ Could not import job processor: {e}")
            print("📄 Displaying job information only (no document generation)")
            
            # Just display the jobs without processing
            processed_jobs = [{'job': job, 'status': 'info_only', 'email_sent': False} for job in job_opportunities]
        
        # Final summary
        print("\\n" + "=" * 60)
        print("📊 PROCESSING SUMMARY")
        print("=" * 60)
        
        successful_jobs = [job for job in processed_jobs if job['status'] == 'success']
        failed_jobs = [job for job in processed_jobs if job['status'] == 'error']
        emails_sent = [job for job in processed_jobs if job.get('email_sent', False)]
        
        print(f"📧 Email account scanned: bluehawana@gmail.com")
        print(f"🔍 Job opportunities found: {len(job_opportunities)}")
        print(f"✅ Successfully processed: {len(successful_jobs)}")
        print(f"❌ Failed to process: {len(failed_jobs)}")
        print(f"📤 Emails sent to leeharvad@gmail.com: {len(emails_sent)}")
        
        # Highlight Volvo Energy jobs
        volvo_jobs = [job for job in job_opportunities if 'volvo' in job['company'].lower() or 'volvo' in job['title'].lower()]
        if volvo_jobs:
            print(f"🚗 Volvo Energy related jobs: {len(volvo_jobs)}")
            for job in volvo_jobs:
                print(f"   • {job['title']} at {job['company']}")
        
        print("\\n🎉 Real email scanning completed!")
        print("📧 Check leeharvad@gmail.com for processed job applications")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())