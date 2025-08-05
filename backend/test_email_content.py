#!/usr/bin/env python3
"""
Test the email content generation without actually sending email
"""
import os
import sys
import glob
import json
from datetime import datetime

def extract_job_info_from_filename(filename):
    """Extract job information from PDF filename"""
    name = filename.replace('.pdf', '')
    
    if 'cv_' in name.lower():
        parts = name.replace('cv_', '').replace('CV_', '').split('_')
    elif 'cover_letter_' in name.lower():
        parts = name.replace('cover_letter_', '').replace('Cover_Letter_', '').split('_')
    else:
        parts = name.split('_')
    
    company = ""
    position = ""
    
    if len(parts) >= 2:
        potential_companies = ['Spotify', 'Volvo', 'Ericsson', 'SKF', 'Hasselblad', 'Netflix', 'Zenseact']
        for part in parts:
            for known_company in potential_companies:
                if known_company.lower() in part.lower():
                    company = known_company
                    break
        
        position_keywords = ['developer', 'engineer', 'devops', 'backend', 'frontend', 'fullstack', 'senior']
        position_parts = []
        for part in parts:
            if any(keyword in part.lower() for keyword in position_keywords):
                position_parts.append(part.replace('_', ' ').title())
        
        position = ' '.join(position_parts) if position_parts else 'Software Position'
        if not company:
            company = parts[0].replace('_', ' ').title()
    
    return {
        'company': company or 'Unknown Company',
        'position': position or 'Software Position',
        'type': 'CV' if 'cv' in filename.lower() else 'Cover Letter'
    }

def get_recent_pdfs():
    """Get recently generated PDF documents with metadata"""
    pdf_patterns = [
        "*.pdf",
        "job_application_package/*.pdf", 
        "simple_pdfs/*.pdf"
    ]
    
    recent_pdfs = []
    for pattern in pdf_patterns:
        files = glob.glob(pattern)
        for file in files:
            if os.path.exists(file):
                basename = os.path.basename(file)
                job_info = extract_job_info_from_filename(basename)
                recent_pdfs.append({
                    'path': file,
                    'filename': basename,
                    'job_info': job_info,
                    'modified': os.path.getmtime(file)
                })
    
    recent_pdfs.sort(key=lambda x: x['modified'], reverse=True)
    return recent_pdfs[:10]

def get_job_application_links():
    """Get job application links from recent job processing"""
    try:
        job_files = [
            'processed_jobs.json',
            'linkedin_saved_jobs.json', 
            'recent_job_data.json'
        ]
        
        job_links = []
        
        for job_file in job_files:
            if os.path.exists(job_file):
                try:
                    with open(job_file, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for job in data:
                                if isinstance(job, dict) and 'url' in job:
                                    job_links.append({
                                        'company': job.get('company', 'Unknown'),
                                        'title': job.get('title', 'Position'),
                                        'url': job.get('url', '#'),
                                        'location': job.get('location', 'N/A')
                                    })
                        elif isinstance(data, dict):
                            for key, jobs in data.items():
                                if isinstance(jobs, list):
                                    for job in jobs:
                                        if isinstance(job, dict) and 'url' in job:
                                            job_links.append({
                                                'company': job.get('company', 'Unknown'),
                                                'title': job.get('title', 'Position'),
                                                'url': job.get('url', '#'),
                                                'location': job.get('location', 'N/A')
                                            })
                except Exception as e:
                    print(f"Could not parse {job_file}: {e}")
        
        # Add some default LinkedIn job links if no data found
        if not job_links:
            job_links = [
                {
                    'company': 'Ericsson',
                    'title': 'Senior Backend Developer',
                    'url': 'https://www.linkedin.com/jobs/search/?keywords=backend%20developer%20ericsson%20gothenburg',
                    'location': 'Gothenburg'
                },
                {
                    'company': 'Hasselblad',
                    'title': 'Cloud Engineer',
                    'url': 'https://www.linkedin.com/jobs/search/?keywords=cloud%20engineer%20hasselblad',
                    'location': 'Gothenburg'
                },
                {
                    'company': 'Netflix',
                    'title': 'Software Engineer',
                    'url': 'https://jobs.netflix.com/search?q=software%20engineer&location=europe',
                    'location': 'Remote (Europe)'
                }
            ]
        
        return job_links[:5]
        
    except Exception as e:
        print(f"Error getting job links: {e}")
        return []

def generate_email_content():
    """Generate the email content"""
    # Get job application links and PDF info
    job_links = get_job_application_links()
    recent_pdfs = get_recent_pdfs()
    
    # Build job links section
    job_links_text = ""
    if job_links:
        job_links_text = "\n🔗 JOB APPLICATION LINKS:\n" + "="*50 + "\n"
        for i, job in enumerate(job_links, 1):
            job_links_text += f"{i}. {job['title']} at {job['company']}\n"
            job_links_text += f"   📍 Location: {job['location']}\n"
            job_links_text += f"   🔗 Apply: {job['url']}\n\n"
    
    # Build PDF summary
    pdf_summary = ""
    if recent_pdfs:
        pdf_summary = "\n📄 ATTACHED DOCUMENTS:\n" + "="*50 + "\n"
        for i, pdf in enumerate(recent_pdfs, 1):
            job_info = pdf['job_info']
            pdf_summary += f"{i}. {pdf['filename']}\n"
            pdf_summary += f"   📋 {job_info['type']} for {job_info['position']} at {job_info['company']}\n"
            pdf_summary += f"   📅 Modified: {datetime.fromtimestamp(pdf['modified']).strftime('%Y-%m-%d %H:%M')}\n\n"

    # Email body
    body = f"""
🤖 JOBHUNTER DAILY APPLICATION REPORT
============================================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your JobHunter automation system has prepared the latest tailored CV and cover letter documents for your job applications.

{job_links_text}
{pdf_summary}

📧 EMAIL INSTRUCTIONS:
- PDFs are attached and ready to download
- Click the job links above to apply directly
- Each CV/CL is customized for the specific role and company
- Documents are optimized for ATS (Applicant Tracking Systems)

🎯 NEXT STEPS:
1. Download the attached PDFs
2. Review each document for accuracy
3. Click the job application links above
4. Submit your applications with the corresponding documents

💡 TIP: Each document is specifically tailored to match the job requirements and company culture for maximum impact.

Best regards,
🤖 JobHunter Automation System
"""
    
    return body, len(recent_pdfs)

if __name__ == "__main__":
    print("=== TESTING EMAIL CONTENT GENERATION ===\n")
    
    email_body, pdf_count = generate_email_content()
    
    print("EMAIL SUBJECT:")
    print(f"Daily Job Application Documents - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("\n" + "="*60 + "\n")
    
    print("EMAIL BODY:")
    print(email_body)
    
    print(f"\nATTACHMENTS: {pdf_count} PDF files would be attached")
    print("\n=== EMAIL CONTENT GENERATION TEST COMPLETE ===")