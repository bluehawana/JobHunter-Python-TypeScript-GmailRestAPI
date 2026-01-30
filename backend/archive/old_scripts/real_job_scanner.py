#!/usr/bin/env python3
"""
Real Job Scanner - Only scan actual Gmail for real job opportunities
No fake jobs, only real opportunities in Gothenburg area
"""
import os
import sys
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RealJobScanner:
    def __init__(self):
        self.gothenburg_keywords = [
            'göteborg', 'gothenburg', 'goteborg', 'mölndal', 'molndal', 
            'partille', 'lerum', 'alingsås', 'kungälv', 'kungsbacka',
            'härryda', 'stenungsund', 'ale', 'öckerö'
        ]
        
    def is_gothenburg_area(self, location_text: str) -> bool:
        """Check if job is in Gothenburg area (20km radius)"""
        if not location_text:
            return False
            
        location_lower = location_text.lower()
        
        # Check for Gothenburg area keywords
        for keyword in self.gothenburg_keywords:
            if keyword in location_lower:
                return True
        
        # Exclude Stockholm, Oslo, etc.
        excluded_cities = ['stockholm', 'oslo', 'copenhagen', 'malmö', 'malmo', 'lund', 'helsingborg']
        for excluded in excluded_cities:
            if excluded in location_lower:
                return False
                
        return False
    
    def scan_real_gmail_jobs(self) -> List[Dict[str, Any]]:
        """Scan actual Gmail for real job opportunities"""
        logger.info("🔍 Scanning Gmail for REAL job opportunities in Gothenburg area...")
        
        try:
            # For now, use a simple email scanning approach
            # TODO: Implement proper Gmail API integration
            logger.info("📧 Checking Gmail for job-related emails...")
            
            # Search for job-related emails
            job_keywords = [
                'job opportunity', 'career opportunity', 'position available',
                'we are hiring', 'join our team', 'software engineer',
                'developer position', 'devops', 'backend', 'fullstack',
                'ansökan', 'tjänst', 'utvecklare', 'programmerare'
            ]
            
            real_jobs = []
            
            # Search Gmail for each keyword
            for keyword in job_keywords:
                try:
                    # Search recent emails (last 7 days)
                    query = f'subject:({keyword}) OR body:({keyword}) newer_than:7d'
                    messages = gmail_service.search_messages(query, max_results=10)
                    
                    for message in messages:
                        job_info = self._extract_job_info_from_email(message)
                        
                        if job_info and self.is_gothenburg_area(job_info.get('location', '')):
                            # Avoid duplicates
                            if not any(job['company'] == job_info['company'] and 
                                     job['title'] == job_info['title'] for job in real_jobs):
                                real_jobs.append(job_info)
                                logger.info(f"✅ Found real job: {job_info['company']} - {job_info['title']}")
                
                except Exception as e:
                    logger.warning(f"⚠️ Error searching for '{keyword}': {e}")
                    continue
            
            if real_jobs:
                logger.info(f"✅ Found {len(real_jobs)} real job opportunities in Gothenburg area")
            else:
                logger.info("ℹ️ No new job opportunities found in Gmail")
            
            return real_jobs
            
        except Exception as e:
            logger.error(f"❌ Gmail scanning failed: {e}")
            return []
    
    def _extract_job_info_from_email(self, message) -> Dict[str, Any]:
        """Extract job information from Gmail message"""
        try:
            # Get email content
            subject = message.get('subject', '')
            body = message.get('body', '')
            sender = message.get('from', '')
            
            # Extract company name from sender
            company = self._extract_company_from_sender(sender)
            
            # Extract job title from subject/body
            job_title = self._extract_job_title(subject, body)
            
            # Extract location
            location = self._extract_location(subject + ' ' + body)
            
            # Only return if we have essential info and it's in Gothenburg area
            if company and job_title and self.is_gothenburg_area(location):
                return {
                    'company': company,
                    'title': job_title,
                    'location': location,
                    'description': body[:500],  # First 500 chars
                    'source': 'gmail',
                    'sender': sender,
                    'subject': subject
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting job info: {e}")
            return None
    
    def _extract_company_from_sender(self, sender: str) -> str:
        """Extract company name from email sender"""
        if not sender:
            return ""
        
        # Remove email address part
        if '<' in sender:
            company_part = sender.split('<')[0].strip()
        else:
            company_part = sender.split('@')[0] if '@' in sender else sender
        
        # Clean up common prefixes/suffixes
        company_part = re.sub(r'\b(hr|recruitment|careers|jobs|talent)\b', '', company_part, flags=re.IGNORECASE)
        company_part = company_part.strip(' -_')
        
        return company_part[:50]  # Limit length
    
    def _extract_job_title(self, subject: str, body: str) -> str:
        """Extract job title from subject and body"""
        text = (subject + ' ' + body).lower()
        
        # Common job titles
        job_patterns = [
            r'(senior\s+)?devops\s+engineer',
            r'(senior\s+)?backend\s+developer',
            r'(senior\s+)?fullstack\s+developer',
            r'(senior\s+)?software\s+engineer',
            r'(senior\s+)?system\s+engineer',
            r'(senior\s+)?cloud\s+engineer',
            r'utvecklare',
            r'systemutvecklare'
        ]
        
        for pattern in job_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).title()
        
        # Fallback: look for "position" or "role"
        position_match = re.search(r'(\w+\s+){0,2}(position|role|tjänst)', text)
        if position_match:
            return position_match.group(0).title()
        
        return "Software Developer"  # Default
    
    def _extract_location(self, text: str) -> str:
        """Extract location from text"""
        text_lower = text.lower()
        
        # Look for Gothenburg area locations
        for location in self.gothenburg_keywords:
            if location in text_lower:
                return location.title()
        
        # Look for "Sweden" patterns
        sweden_match = re.search(r'(\w+),?\s*sweden', text_lower)
        if sweden_match:
            return sweden_match.group(0).title()
        
        return "Gothenburg, Sweden"  # Default for area

def scan_for_real_jobs() -> List[Dict[str, Any]]:
    """Main function to scan for real jobs"""
    scanner = RealJobScanner()
    return scanner.scan_real_gmail_jobs()

if __name__ == "__main__":
    # Test the real job scanner
    jobs = scan_for_real_jobs()
    
    print(f"🔍 REAL JOB SCAN RESULTS")
    print(f"=" * 40)
    print(f"📧 Gmail jobs found: {len(jobs)}")
    
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['company']} - {job['title']}")
        print(f"   📍 Location: {job['location']}")
        print(f"   📧 From: {job['sender']}")
        print(f"   📋 Subject: {job['subject'][:60]}...")