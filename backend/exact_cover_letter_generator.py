#!/usr/bin/env python3
"""
Exact Cover Letter Generator - Uses your EXACT LaTeX template
Customizes company info, highlights soft skills not in resume
"""
import os
import sys
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')

import logging
import tempfile
import subprocess
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

class ExactCoverLetterGenerator:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
        self.claude_base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://anyrouter.top')
    
    def get_company_info_with_claude(self, company_name: str, job_title: str, job_description: str = "") -> Dict[str, str]:
        """Extract company info from job ad, then use Claude API as fallback"""
        try:
            # Skip job ad extraction for now - use Claude directly
            extracted_info = {'has_contact_info': False}
            
            if extracted_info['has_contact_info']:
                logger.info(f"✅ Extracted contact info from job ad for {company_name}")
                return extracted_info
            
            # Fallback to Claude API for company lookup
            prompt = f"""
            Find the company address and HR contact information for {company_name} in Gothenburg, Sweden area.
            This is for a {job_title} position application.
            
            Return ONLY a JSON object with these exact fields:
            {{
                "company_address": "Street address or 'Gothenburg Office'",
                "postal_code": "Postal code or '411 XX'", 
                "city": "Göteborg",
                "hr_contact": "HR contact name if known, otherwise 'Hiring Manager'"
            }}
            
            Focus on Gothenburg area companies. If specific address unknown, use general Gothenburg business address format.
            """
            
            headers = {
                'Authorization': f'Bearer {self.claude_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'claude-3-7-sonnet-20250219',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 300
            }
            
            response = requests.post(
                f'{self.claude_base_url}/v1/messages',
                headers=headers,
                json=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                claude_response = result['content'][0]['text']
                
                # Try to extract JSON
                import json
                try:
                    start_idx = claude_response.find('{')
                    end_idx = claude_response.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx != -1:
                        json_str = claude_response[start_idx:end_idx]
                        company_info = json.loads(json_str)
                        return company_info
                except:
                    pass
            
            # Fallback
            return self._get_fallback_company_info(company_name)
            
        except Exception as e:
            logger.warning(f"⚠️ Claude company info failed: {e}")
            return self._get_fallback_company_info(company_name)
    
    def _get_fallback_company_info(self, company_name: str) -> Dict[str, str]:
        """Fallback company info for Gothenburg companies"""
        return {
            "company_address": f"{company_name}\\\\Gothenburg Office",
            "postal_code": "411 XX",
            "city": "Göteborg",
            "hr_contact": "Hiring Manager"
        }
    
    def generate_cover_letter_content(self, job: Dict[str, Any]) -> str:
        """Generate cover letter content highlighting soft skills"""
        company = job['company']
        job_title = job['title']
        location = job.get('location', 'Gothenburg, Sweden')
        description = job.get('description', '')
        
        # Get company info
        company_info = self.get_company_info_with_claude(company, job_title)
        
        # Determine greeting and approach
        if 'sweden' in location.lower() or 'göteborg' in location.lower():
            greeting = "Hej"
            if company_info['hr_contact'] != 'Hiring Manager':
                greeting_line = f"Hej {company_info['hr_contact']},"
            else:
                greeting_line = "Hej,"
        else:
            greeting_line = f"Dear {company_info['hr_contact']},"
        
        # Analyze job for focus areas
        job_text = (job_title + ' ' + description).lower()
        
        is_devops = any(keyword in job_text for keyword in 
                       ['devops', 'infrastructure', 'kubernetes', 'docker', 'ci/cd', 'cloud'])
        is_backend = any(keyword in job_text for keyword in 
                        ['backend', 'api', 'microservices', 'spring', 'java']) and not is_devops
        is_automotive = any(keyword in job_text for keyword in 
                           ['automotive', 'car', 'vehicle', 'volvo', 'geely'])
        
        # Customize content based on role and company
        if is_automotive:
            industry_passion = f"As a seasoned {job_title.split()[0] if job_title else 'technology'} professional with a profound passion for the automotive industry, I am excited by the prospect of contributing to the development of cutting-edge solutions at {company}."
            
            company_attraction = f"What draws me to {company} is the opportunity to work on innovative projects that shape the future of the automotive industry."
            
            technical_alignment = "My expertise in containerization, infrastructure as code, and automation practices aligns perfectly with your need for a developer who can leverage their experiences to improve the workflows for other developers."
            
        elif is_devops:
            industry_passion = f"As an experienced DevOps professional with deep expertise in cloud technologies and infrastructure automation, I am excited about the opportunity to contribute to {company}'s technical excellence."
            
            company_attraction = f"What draws me to {company} is your commitment to innovation and the opportunity to work with cutting-edge technologies in a collaborative environment."
            
            technical_alignment = "With my proven experience in designing and optimizing CI/CD pipelines across multiple cloud platforms, I am confident in my ability to streamline the software delivery processes for your mission-critical applications."
            
        else:
            industry_passion = f"As an experienced software professional with expertise in modern development practices, I am excited about the opportunity to contribute to {company}'s innovative projects."
            
            company_attraction = f"What draws me to {company} is your reputation for technical excellence and the opportunity to work on challenging projects that make a real impact."
            
            technical_alignment = "My experience in full-stack development, API design, and system integration aligns well with your technical requirements."
        
        # Soft skills paragraph (not heavily featured in resume)
        soft_skills_content = """Throughout my career, I have consistently demonstrated a strong commitment to coaching cross-functional teams on modern development methodologies and fostering a culture of collaboration and continuous improvement. I thrive in multi-team environments, where I can leverage my overall understanding of complex systems and intricate integration processes to drive efficiency and innovation.
        
My multicultural background has equipped me with exceptional cross-cultural communication skills, having successfully worked across Swedish, Chinese, and international business environments. This unique perspective enables me to bridge communication gaps between technical teams and business stakeholders, ensuring that complex technical solutions align with business objectives and user needs."""
        
        # Technical skills (complement resume)
        if is_devops:
            technical_skills = "Python, Git, Cloud/Azure, Kubernetes, Linux, Ansible, Terraform, PostgreSQL, Grafana, TypeScript, ReactJS, and Docker"
        elif is_backend:
            technical_skills = "Java, Spring Boot, Python, PostgreSQL, MongoDB, REST APIs, Microservices, Docker, and cloud platforms"
        else:
            technical_skills = "Python, JavaScript, React, Node.js, PostgreSQL, Docker, Kubernetes, and modern development tools"
        
        # Company culture alignment
        culture_alignment = f"I am impressed by {company}'s commitment to innovation and technical excellence. As a proactive and results-driven professional, I welcome the opportunity to contribute to your team's success while growing professionally in this dynamic environment."
        
        # Current date
        import time
        current_date = time.strftime("%Y.%m.%d")
        
        # Generate the EXACT LaTeX template with customizations
        latex_content = f"""\\documentclass[a4paper,10pt]{{article}}
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

{{\\color{{darkblue}}
{company}\\\\
{company_info['company_address']}\\\\
{company_info['postal_code']} {company_info['city']}}}

\\vspace{{40pt}}

{greeting_line}

\\vspace{{10pt}}

I am writing to express my sincere interest in the {job_title} role at {company}. {industry_passion}

{company_attraction} {technical_alignment}

{soft_skills_content}

At {company}, I am eager to contribute my skills and knowledge in tools such as {technical_skills}. My hands-on experience with these technologies, combined with my passion for delivering high-quality solutions, makes me an ideal candidate for this role.

{culture_alignment}

Thank you for considering my application. I look forward to discussing how my expertise and collaborative approach can contribute to {company}'s continued success and innovation.

\\vspace{{20pt}}

Sincerely,

Hongzhi Li\\\\
{current_date}

\\vspace{{40pt}}

{{\\color{{darkblue}}\\rule{{\\linewidth}}{{0.6pt}}}}

\\vspace{{4pt}}

{{\\color{{darkblue}}
Ebbe Lieberathsgatan 27\\\\
412 65 Göteborg\\\\
hongzhili01@gmail.com\\\\
0728384299}}

\\end{{document}}"""
        
        return latex_content
    
    def compile_latex_to_pdf(self, latex_content: str) -> bytes:
        """Compile LaTeX to PDF using pdflatex"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                tex_file = os.path.join(temp_dir, "cover_letter.tex")
                pdf_file = os.path.join(temp_dir, "cover_letter.pdf")
                
                # Write LaTeX content
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile LaTeX (run twice for proper formatting)
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
                        pdf_content = f.read()
                    
                    logger.info(f"✅ Cover letter PDF compiled: {len(pdf_content)} bytes")
                    return pdf_content
                else:
                    logger.error("PDF file was not generated")
                    return b""
                    
        except Exception as e:
            logger.error(f"❌ LaTeX compilation failed: {e}")
            return b""
    
    def create_cover_letter(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete cover letter with LaTeX and PDF"""
        try:
            # Generate LaTeX content
            latex_content = self.generate_cover_letter_content(job)
            
            # Compile to PDF
            pdf_content = self.compile_latex_to_pdf(latex_content)
            
            return {
                'latex_content': latex_content,
                'pdf_content': pdf_content,
                'latex_size': len(latex_content),
                'pdf_size': len(pdf_content) if pdf_content else 0,
                'success': bool(pdf_content),
                'company': job['company'],
                'job_title': job['title']
            }
            
        except Exception as e:
            logger.error(f"❌ Cover letter creation failed: {e}")
            return {
                'latex_content': '',
                'pdf_content': b'',
                'latex_size': 0,
                'pdf_size': 0,
                'success': False,
                'error': str(e)
            }

def create_exact_cover_letter(job: Dict[str, Any]) -> Dict[str, Any]:
    """Main function to create cover letter"""
    generator = ExactCoverLetterGenerator()
    return generator.create_cover_letter(job)

if __name__ == "__main__":
    # Test with Opera job
    test_job = {
        'company': 'Opera',
        'title': 'DevOps Engineer',
        'location': 'Gothenburg, Sweden',
        'description': 'DevOps engineer role with Kubernetes, Docker, monitoring'
    }
    
    result = create_exact_cover_letter(test_job)
    
    print(f"✅ Success: {result['success']}")
    print(f"📝 LaTeX size: {result['latex_size']} chars")
    print(f"📄 PDF size: {result['pdf_size']} bytes")
    
    if result['success']:
        # Save files
        with open('test_exact_cover_letter.tex', 'w') as f:
            f.write(result['latex_content'])
        
        with open('test_exact_cover_letter.pdf', 'wb') as f:
            f.write(result['pdf_content'])
        
        print("💾 Files saved: test_exact_cover_letter.tex/.pdf")