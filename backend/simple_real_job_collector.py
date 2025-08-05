#!/usr/bin/env python3
"""
Simple real job collector from Gmail
Works without additional dependencies
"""
import imaplib
import email
import re
import json
import os
from datetime import datetime, timedelta

# Load environment variables manually
def load_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env_file()

def scan_gmail_for_real_jobs(days_back=7):
    """Scan Gmail for real job opportunities"""
    gmail_user = "bluehawana@gmail.com"
    gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")
    
    if not gmail_password:
        print("❌ GMAIL_APP_PASSWORD not set in .env file")
        return []
    
    try:
        print(f"🔍 Scanning Gmail {gmail_user} for jobs (last {days_back} days)...")
        
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")
        
        # Calculate date filter
        since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
        
        # Search queries for job-related emails
        search_queries = [
            f'(SINCE "{since_date}" FROM "linkedin")',
            f'(SINCE "{since_date}" FROM "indeed")',
            f'(SINCE "{since_date}" FROM "thelocal")',
            f'(SINCE "{since_date}" FROM "glassdoor")',
            f'(SINCE "{since_date}" SUBJECT "job")',
            f'(SINCE "{since_date}" SUBJECT "developer")',
            f'(SINCE "{since_date}" SUBJECT "engineer")',
            f'(SINCE "{since_date}" SUBJECT "software")',
        ]
        
        all_jobs = []
        processed_emails = set()
        
        for query in search_queries:
            try:
                status, messages = mail.search(None, query)
                if status == "OK" and messages[0]:
                    message_ids = messages[0].split()
                    print(f"📧 Found {len(message_ids)} emails for: {query}")
                    
                    # Process recent emails (last 10 per query)
                    for msg_id in message_ids[-10:]:
                        if msg_id not in processed_emails:
                            processed_emails.add(msg_id)
                            
                            # Extract job from email
                            job = extract_job_from_email(mail, msg_id)
                            if job:
                                all_jobs.append(job)
                                print(f"✅ Found: {job['company']} - {job['title']}")
                                
            except Exception as e:
                print(f"❌ Error with query {query}: {e}")
        
        mail.close()
        mail.logout()
        
        # Remove duplicates and get best jobs
        unique_jobs = filter_quality_jobs(all_jobs)
        print(f"🎯 Filtered to {len(unique_jobs)} quality job opportunities")
        
        return unique_jobs
        
    except Exception as e:
        print(f"❌ Error scanning Gmail: {e}")
        return []

def extract_job_from_email(mail, msg_id):
    """Extract job information from an email"""
    try:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        if status != "OK":
            return None
        
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)
        
        subject = email_message.get("Subject", "")
        sender = email_message.get("From", "")
        
        # Extract email content
        content = extract_email_content(email_message)
        
        # Check if this looks like a real job email
        if not is_job_email(subject, content, sender):
            return None
        
        # Extract job details
        title = extract_job_title(subject, content)
        company = extract_company_name(subject, content, sender)
        location = extract_location(content)
        url = extract_application_url(content)
        
        # Must have essential information
        if not title or not company or len(title) < 5 or len(company) < 2:
            return None
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'url': url,
            'source': 'gmail_real',
            'subject': subject,
            'sender': sender
        }
        
    except Exception as e:
        print(f"Error extracting job: {e}")
        return None

def extract_email_content(email_message):
    """Extract text content from email"""
    content = ""
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        content += payload.decode('utf-8', errors='ignore')
        else:
            payload = email_message.get_payload(decode=True)
            if payload:
                content = payload.decode('utf-8', errors='ignore')
    except:
        content = str(email_message.get_payload())
    
    return content

def is_job_email(subject, content, sender):
    """Check if email is a real job opportunity"""
    text = (subject + " " + content + " " + sender).lower()
    
    # Job indicators
    job_indicators = [
        "job", "position", "developer", "engineer", "software", "fullstack",
        "backend", "frontend", "devops", "hiring", "opportunity", "career",
        "apply", "application", "role", "team"
    ]
    
    # Spam indicators
    spam_indicators = [
        "unsubscribe", "newsletter", "promotional", "marketing",
        "discount", "free trial", "click here", "limited time"
    ]
    
    job_score = sum(1 for indicator in job_indicators if indicator in text)
    spam_score = sum(1 for indicator in spam_indicators if indicator in text)
    
    # Must have job indicators and minimal spam
    return job_score >= 2 and spam_score < 3

def extract_job_title(subject, content):
    """Extract job title"""
    # Try subject first
    title_patterns = [
        r"(?:job|position|role)[:\s]+([^-\n|]{10,80})",
        r"([A-Z][^-\n|]{10,80})(?:\s*-\s*(?:job|position))",
        r"hiring[:\s]+([^-\n|]{10,60})",
        r"apply for[:\s]+([^-\n|]{10,60})"
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, subject, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            if any(keyword in title.lower() for keyword in ['developer', 'engineer', 'software']):
                return title
    
    # Try content patterns
    content_patterns = [
        r"job title[:\s]+([^\n]{10,60})",
        r"position[:\s]+([^\n]{10,60})",
        r"we are looking for\s+a\s+([^\n]{10,60})",
        r"seeking\s+a\s+([^\n]{10,60})"
    ]
    
    for pattern in content_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "Software Developer"

def extract_company_name(subject, content, sender):
    """Extract company name"""
    # Try sender domain first
    if "@" in sender:
        domain = sender.split("@")[-1].replace(">", "").lower()
        if not any(common in domain for common in ["linkedin", "indeed", "noreply", "gmail"]):
            company = domain.split(".")[0].title()
            if len(company) > 2:
                return company
    
    # Try content patterns
    company_patterns = [
        r"company[:\s]+([^\n]{3,40})",
        r"at\s+([A-Z][a-zA-Z\s&\.]{2,30})\s+(?:is|are|we)",
        r"([A-Z][a-zA-Z\s&\.]{3,30})\s+(?:is hiring|is looking)",
        r"join\s+([A-Z][a-zA-Z\s&\.]{3,30})"
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            if len(company) > 3:
                return company
    
    return "Tech Company"

def extract_location(content):
    """Extract location"""
    location_patterns = [
        r"location[:\s]+([^\n]{3,30})",
        r"(Stockholm|Göteborg|Gothenburg|Malmö|Sweden|Remote)",
        r"office[:\s]+([^\n]{3,30})",
        r"based in[:\s]+([^\n]{3,30})"
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "Sweden"

def extract_application_url(content):
    """Extract application URL"""
    url_patterns = [
        r"https?://[^\s]*linkedin\.com/jobs/view/\d+[^\s]*",
        r"https?://[^\s]*indeed\.com/viewjob\?jk=[^\s]+",
        r"https?://[^\s]*thelocal\.se/jobs/[^\s]+",
        r"https?://[^\s]*glassdoor\.com/job[^\s]*",
        r"https?://[^\s]*(?:apply|career|job)[^\s]*"
    ]
    
    for pattern in url_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            return matches[0]
    
    return ""

def filter_quality_jobs(jobs):
    """Filter to quality jobs only"""
    quality_jobs = []
    seen_combinations = set()
    
    for job in jobs:
        # Create unique identifier
        job_id = f"{job['company'].lower()}_{job['title'].lower().replace(' ', '_')}"
        
        if job_id in seen_combinations:
            continue
        seen_combinations.add(job_id)
        
        # Quality checks
        if len(job['title']) < 5 or len(job['company']) < 3:
            continue
        
        # Must have some way to apply
        if not job['url'] and '@' not in job.get('sender', ''):
            continue
        
        quality_jobs.append(job)
    
    return quality_jobs[:5]  # Top 5 jobs

def main():
    """Main function"""
    jobs = scan_gmail_for_real_jobs(days_back=7)
    
    if jobs:
        # Save to processed_jobs.json
        job_list = []
        for job in jobs:
            job_entry = {
                'company': job['company'],
                'title': job['title'],
                'url': job['url'] if job['url'] else f"mailto:{job['sender']}",
                'location': job['location']
            }
            job_list.append(job_entry)
        
        with open('processed_jobs.json', 'w') as f:
            json.dump(job_list, f, indent=2)
        
        print(f"\n🎉 SUCCESS: Found and saved {len(job_list)} real job opportunities!")
        print("\n📋 Jobs found:")
        for job in job_list:
            print(f"✅ {job['company']} - {job['title']}")
            print(f"   📍 {job['location']}")
            print(f"   🔗 {job['url'][:60]}...")
            print()
        
        return True
    else:
        print("❌ No real jobs found in Gmail")
        print("💡 Make sure you have job alert emails from LinkedIn, Indeed, etc.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)