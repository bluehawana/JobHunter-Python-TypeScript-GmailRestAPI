#!/usr/bin/env python3
"""
Test script to preview automated job application emails
"""
from automated_job_applicator import JobApplicationMatcher
from datetime import datetime

def preview_job_emails():
    """Preview what the individual job emails will look like"""
    matcher = JobApplicationMatcher()
    job_pairs = matcher.get_job_document_pairs()
    
    print("=== AUTOMATED JOB APPLICATION EMAIL PREVIEW ===\n")
    
    for i, job_pair in enumerate(job_pairs[:3], 1):  # Show first 3
        job = job_pair['job']
        
        print(f"📧 EMAIL {i}: {job['company']} - {job['title']}")
        print("="*60)
        print(f"SUBJECT: 🎯 Job Application Ready: {job['title']} at {job['company']}")
        print()
        print("BODY:")
        print(f"""
🎯 AUTOMATED JOB APPLICATION READY
============================================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Hello Hongzhi,

Your JobHunter system has prepared a tailored application package for this specific opportunity:

🏢 COMPANY: {job['company']}
💼 POSITION: {job['title']}
📍 LOCATION: {job.get('location', 'Not specified')}

🔗 DIRECT APPLICATION LINK:
{job['url']}

📄 ATTACHED DOCUMENTS:
==================================================
✅ Customized CV: {job_pair['cv_filename']}
✅ Tailored Cover Letter: {job_pair['cl_filename']}

Both documents are specifically optimized for:
• {job['company']}'s company culture and values
• {job['title']} role requirements
• ATS (Applicant Tracking System) compatibility
• Industry-specific keywords and terminology

🎯 NEXT STEPS:
1. Click the application link above
2. Upload the attached CV and Cover Letter
3. Complete the application form
4. Submit your application

💡 SUCCESS TIP: These documents are pre-customized for maximum impact at {job['company']}. The CV highlights relevant experience and the cover letter addresses their specific needs.

🤖 This is an automated application prepared by your JobHunter system.

Best of luck with your application!

---
JobHunter Automation System
""")
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    preview_job_emails()