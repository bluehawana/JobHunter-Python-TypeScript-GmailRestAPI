#!/usr/bin/env python3
"""
Generate Opera DevOps Application Package (Simplified Version)
- Enhanced CV with Prometheus/Grafana monitoring highlights
- Tailored Cover Letter with soft skills
- Email delivery
"""
import sys
import os
sys.path.append('backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

from beautiful_pdf_generator import create_beautiful_multi_page_pdf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_cover_letter_latex(job_data):
    """Create cover letter LaTeX content"""
    
    company = job_data.get('company', 'Company')
    position = job_data.get('title', 'Position')
    location = job_data.get('location', 'Location')
    current_date = time.strftime("%Y.%m.%d")
    
    # Determine greeting based on location
    if 'norway' in location.lower() or 'oslo' in location.lower():
        greeting = "Hej"
    else:
        greeting = "Dear Hiring Manager"
    
    cover_letter_latex = f"""
\\documentclass[a4paper,10pt]{{article}}
\\usepackage[left=1in,right=1in,top=1in,bottom=1in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}
\\usepackage{{graphicx}}
\\usepackage{{xcolor}}

% Define colors
\\definecolor{{darkblue}}{{rgb}}{{0.0, 0.2, 0.6}}

% Section formatting
\\titleformat{{\\section}}{{\\large\\bfseries\\raggedright\\color{{black}}}}{{}}{{0em}}{{}}[\\titlerule]
\\titleformat{{\\subsection}}[runin]{{\\bfseries}}{{}}{{0em}}{{}}[:]

% Remove paragraph indentation
\\setlength{{\\parindent}}{{0pt}}

\\begin{{document}}
\\pagestyle{{empty}} % no page number

\\begin{{letter}}{{\\color{{darkblue}}\\\\
{company}\\\\
{location}}}

\\\\
\\vspace{{40pt}}

\\opening{{{greeting},}}

\\vspace{{10pt}}

I am writing to express my sincere interest in the {position} role at {company}. As an experienced DevOps professional with a unique combination of technical expertise and cross-cultural communication skills, I am excited about the opportunity to contribute to your team's success while bringing a fresh perspective to your infrastructure challenges.

What particularly excites me about {company} is the opportunity to work on innovative browser technology and contribute to products used by millions worldwide. My current role at ECARX has given me deep insights into complex system integration challenges, and I am passionate about leveraging my technical expertise to enhance user experiences through robust infrastructure solutions.

Throughout my career, I have excelled in cross-functional collaboration, serving as a bridge between development teams and infrastructure operations. My experience at ECARX has strengthened my ability to communicate complex technical concepts to both technical and non-technical stakeholders, ensuring seamless project delivery across diverse teams.

What sets me apart is my multicultural perspective and cross-cultural communication skills. Having worked across Swedish, Norwegian, and international business environments, I bring a unique ability to navigate cultural nuances while maintaining technical excellence. This has been particularly valuable when coordinating between IT departments and business units, translating business requirements into technical solutions.

My expertise extends beyond technical implementation to system integration and process optimization. At ECARX, I led the migration from AKS to local Kubernetes clusters while implementing comprehensive Prometheus and Grafana monitoring solutions. This project required not only technical skills but also extensive collaboration with multiple departments, change management, and stakeholder alignment, showcasing my ability to integrate complex systems while managing organizational change.

My technical foundation includes expertise in Kubernetes, Docker, AWS, Azure, Prometheus, Grafana, Python, and various CI/CD tools. However, what truly differentiates me is my ability to leverage these technical skills within a collaborative, multicultural context, ensuring that infrastructure solutions align with business objectives and user needs.

At {company}, I am particularly excited about the opportunity to contribute not just my technical skills, but also my experience in fostering collaboration, managing stakeholder relationships, and driving successful project outcomes through effective communication and integration practices.

I am confident that my combination of technical expertise, soft skills, and integration experience will make a valuable contribution to your team. I look forward to discussing how my unique background can support {company}'s continued growth and success.

\\vspace{{20pt}}

Sincerely,

Hongzhi Li\\\\
{current_date}

\\vspace{{40pt}}

{{\\color{{darkblue}}\\rule{{\\linewidth}}{{0.6pt}}}}

\\vspace{{4pt}}

\\closing{{\\color{{darkblue}} 
Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299}}

\\\\
\\vspace{{10pt}}

\\end{{letter}}

\\end{{document}}
"""
    
    return cover_letter_latex.strip()

def compile_latex_to_pdf(latex_content, filename_prefix):
    """Compile LaTeX content to PDF"""
    try:
        import subprocess
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, f"{filename_prefix}.tex")
            pdf_file = os.path.join(temp_dir, f"{filename_prefix}.pdf")
            
            # Write LaTeX content
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile LaTeX (run twice for references)
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                    capture_output=True, text=True
                )
                
                if result.returncode != 0:
                    logger.error(f"LaTeX compilation failed: {result.stderr}")
                    return b""
            
            # Read PDF
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as f:
                    return f.read()
                    
    except Exception as e:
        logger.error(f"❌ LaTeX compilation failed: {e}")
        return b""

def send_application_email(cv_pdf, cover_letter_pdf, job_data):
    """Send application package via email"""
    try:
        # Email configuration
        sender_email = os.getenv('SENDER_EMAIL', 'leeharvad@gmail.com')
        sender_password = os.getenv('SENDER_GMAIL_PASSWORD')
        recipient_email = 'hongzhili01@gmail.com'
        
        if not sender_password:
            logger.error("❌ Email password not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🎭 Opera DevOps Engineer Application Package - Enhanced with Monitoring Expertise"
        
        # Email body
        body = f"""
🎭 OPERA DEVOPS ENGINEER APPLICATION PACKAGE

Dear Hongzhi,

Your customized application package for the DevOps Engineer position at {job_data['company']} is ready!

📊 PACKAGE CONTENTS:
✅ Enhanced CV (PDF) - DevOps focused with Prometheus/Grafana monitoring expertise
✅ Tailored Cover Letter (PDF) - Cross-cultural communication and integration skills
✅ Specific monitoring highlights added to ECARX experience
✅ Performance analysis and optimization achievements featured

🎯 KEY ENHANCEMENTS ADDED TO CV:
• Comprehensive monitoring stack using Prometheus and Grafana
• High-performance local cluster server observation (CPU, I/O, memory, network)
• Performance analysis comparing on-premises GitLab runners with AKS
• 25% performance improvement in CI/CD pipeline execution times
• 40% cost reduction from AKS to local Kubernetes migration
• Advanced Grafana dashboards for real-time infrastructure observability
• Proactive issue detection and system optimization capabilities

📝 COVER LETTER HIGHLIGHTS:
• Cross-cultural communication skills (Swedish/Norwegian/International)
• Bridge between technical teams and business stakeholders
• System integration and process optimization expertise
• Multicultural perspective and cultural nuance navigation
• Collaborative approach to complex infrastructure challenges

🚀 READY FOR OPERA APPLICATION!

The documents are specifically tailored for Opera's DevOps Engineer role with:
• Infrastructure focus matching their requirements
• Kubernetes/Docker expertise highlighted
• Prometheus/Grafana monitoring experience featured
• Cross-functional collaboration skills emphasized
• Norwegian cultural approach in cover letter
• Browser technology industry alignment

📍 Position Details:
Company: {job_data['company']}
Role: {job_data['title']}
Location: {job_data['location']}
URL: {job_data.get('url', 'https://jobs.opera.com/jobs/6060392-devops-engineer')}

Best of luck with your Opera application! 🎉

---
Generated by JobHunter Automation System with Enhanced Monitoring Expertise
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CV PDF
        if cv_pdf:
            cv_attachment = MIMEBase('application', 'octet-stream')
            cv_attachment.set_payload(cv_pdf)
            encoders.encode_base64(cv_attachment)
            cv_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="Hongzhi_Li_CV_Opera_DevOps_Enhanced.pdf"'
            )
            msg.attach(cv_attachment)
        
        # Attach Cover Letter PDF
        if cover_letter_pdf:
            cl_attachment = MIMEBase('application', 'octet-stream')
            cl_attachment.set_payload(cover_letter_pdf)
            encoders.encode_base64(cl_attachment)
            cl_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="Hongzhi_Li_CoverLetter_Opera_DevOps.pdf"'
            )
            msg.attach(cl_attachment)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"✅ Application package sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        return False

def main():
    """Generate complete Opera DevOps application package"""
    
    print("🎭 GENERATING OPERA DEVOPS APPLICATION PACKAGE")
    print("=" * 60)
    
    # Opera DevOps job data with enhanced monitoring requirements
    opera_job = {
        'title': 'DevOps Engineer',
        'company': 'Opera',
        'description': '''
        We are looking for a DevOps Engineer to join our team and help us build and maintain our infrastructure.
        
        Key responsibilities:
        - Design, implement and maintain CI/CD pipelines
        - Manage cloud infrastructure on AWS and Azure
        - Implement monitoring and alerting solutions using Prometheus and Grafana
        - Automate deployment processes
        - Work with Kubernetes and Docker containers
        - Collaborate with development teams
        - Ensure security best practices
        - Optimize system performance and reliability
        - Monitor high-performance cluster servers
        - Analyze CPU usage, I/O performance, and system metrics
        - Compare on-premises and cloud infrastructure performance
        
        Required skills:
        - Experience with AWS, Azure, or GCP
        - Proficiency in Kubernetes and Docker
        - CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
        - Infrastructure as Code (Terraform, CloudFormation)
        - Monitoring tools (Prometheus, Grafana, ELK stack)
        - Performance analysis and optimization
        - Scripting languages (Python, Bash, PowerShell)
        - Linux system administration
        - Security best practices
        - Agile methodologies
        ''',
        'location': 'Oslo, Norway',
        'url': 'https://jobs.opera.com/jobs/6060392-devops-engineer'
    }
    
    print(f"🏢 Company: {opera_job['company']}")
    print(f"💼 Position: {opera_job['title']}")
    print(f"📍 Location: {opera_job['location']}")
    print(f"🔗 URL: {opera_job['url']}")
    
    # Generate enhanced CV
    print(f"\n📄 Generating enhanced CV with Prometheus/Grafana monitoring highlights...")
    cv_pdf = create_beautiful_multi_page_pdf(opera_job)
    
    cv_success = bool(cv_pdf)
    cv_size = len(cv_pdf) if cv_pdf else 0
    
    print(f"✅ CV Generated: {cv_size:,} bytes" if cv_success else "❌ CV Generation Failed")
    
    # Generate cover letter
    print(f"\n📝 Generating tailored cover letter...")
    cover_letter_latex = create_cover_letter_latex(opera_job)
    cover_letter_pdf = compile_latex_to_pdf(cover_letter_latex, "cover_letter")
    
    cl_success = bool(cover_letter_pdf)
    cl_size = len(cover_letter_pdf) if cover_letter_pdf else 0
    
    print(f"✅ Cover Letter Generated: {cl_size:,} bytes" if cl_success else "❌ Cover Letter Generation Failed")
    
    # Save files locally
    if cv_pdf:
        with open('Opera_DevOps_CV_Enhanced_HongzhiLi.pdf', 'wb') as f:
            f.write(cv_pdf)
        print(f"💾 CV saved: Opera_DevOps_CV_Enhanced_HongzhiLi.pdf")
    
    if cover_letter_pdf:
        with open('Opera_DevOps_CoverLetter_HongzhiLi.pdf', 'wb') as f:
            f.write(cover_letter_pdf)
        print(f"💾 Cover Letter saved: Opera_DevOps_CoverLetter_HongzhiLi.pdf")
    
    # Save LaTeX files for reference
    if cover_letter_latex:
        with open('Opera_DevOps_CoverLetter_HongzhiLi.tex', 'w') as f:
            f.write(cover_letter_latex)
        print(f"💾 Cover Letter LaTeX saved: Opera_DevOps_CoverLetter_HongzhiLi.tex")
    
    # Send email with application package
    print(f"\n📧 Sending application package to hongzhili01@gmail.com...")
    
    email_success = send_application_email(cv_pdf, cover_letter_pdf, opera_job)
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 OPERA DEVOPS APPLICATION SUMMARY")
    print(f"=" * 60)
    
    print(f"✅ Enhanced CV Generated: {cv_success} ({cv_size:,} bytes)")
    print(f"✅ Cover Letter Generated: {cl_success} ({cl_size:,} bytes)")
    print(f"✅ Email Sent: {email_success}")
    
    if email_success:
        print(f"\n🎉 COMPLETE SUCCESS!")
        print(f"📧 Application package delivered to hongzhili01@gmail.com")
        print(f"📄 CV: Enhanced with Prometheus/Grafana monitoring expertise")
        print(f"📝 Cover Letter: Tailored with cross-cultural communication focus")
        print(f"\n🎯 KEY ENHANCEMENTS:")
        print(f"   • Prometheus & Grafana monitoring stack implementation")
        print(f"   • High-performance cluster server observation")
        print(f"   • GitLab runner vs AKS performance comparison")
        print(f"   • 25% CI/CD performance improvement achievement")
        print(f"   • 40% cost reduction from infrastructure optimization")
        print(f"   • Cross-cultural communication and integration skills")
        print(f"\n🚀 Ready to apply to Opera!")
    else:
        print(f"\n⚠️ PARTIAL SUCCESS")
        print(f"📄 Documents generated successfully")
        print(f"❌ Email delivery failed - check email configuration")
        print(f"💡 Documents saved locally for manual submission")
    
    return {
        'cv_success': cv_success,
        'cl_success': cl_success,
        'email_success': email_success,
        'cv_size': cv_size,
        'cl_size': cl_size
    }

if __name__ == "__main__":
    result = main()
    
    if result['cv_success'] and result['cl_success'] and result['email_success']:
        print(f"\n🎭 OPERA DEVOPS APPLICATION COMPLETE! 🎉")
        print(f"📧 Check your email: hongzhili01@gmail.com")
    else:
        print(f"\n⚠️ Check the summary above for any issues")