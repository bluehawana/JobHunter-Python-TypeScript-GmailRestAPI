#!/usr/bin/env python3
"""
LaTeX Resume and Cover Letter Generator for Saved Jobs
Generates customized documents for each job in the database
"""

import os
import sys
import subprocess
from datetime import datetime, date
from typing import List, Dict, Any, Optional

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

class LaTeXDocumentGenerator:
    """Generate customized LaTeX resumes and cover letters"""
    
    def __init__(self):
        self.output_dir = "generated_documents"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Personal information (customize this)
        self.personal_info = {
            "name": "Your Name",
            "email": "your.email@example.com",
            "phone": "+46 70 123 4567",
            "location": "Gothenburg, Sweden",
            "linkedin": "linkedin.com/in/yourprofile",
            "github": "github.com/yourusername"
        }
    
    def generate_resume_latex(self, job: Dict[str, Any]) -> str:
        """Generate customized LaTeX resume for specific job"""
        
        # Extract relevant skills from job requirements
        job_skills = job.get('skills_matched', [])
        job_requirements = job.get('requirements', '').lower()
        
        # Customize skills section based on job
        highlighted_skills = []
        all_skills = [
            "Python", "FastAPI", "Django", "PostgreSQL", "Docker", "Kubernetes",
            "AWS", "React", "TypeScript", "Git", "Linux", "CI/CD", "Machine Learning",
            "TensorFlow", "Apache Spark", "Microservices", "REST APIs"
        ]
        
        # Prioritize skills mentioned in job
        for skill in job_skills:
            if skill in all_skills and skill not in highlighted_skills:
                highlighted_skills.append(skill)
        
        # Add other relevant skills
        for skill in all_skills:
            if any(s.lower() in job_requirements for s in [skill.lower()]) and skill not in highlighted_skills:
                highlighted_skills.append(skill)
        
        # Limit to top 8 skills
        highlighted_skills = highlighted_skills[:8]
        
        latex_content = f"""\\documentclass[11pt,a4paper,sans]{{moderncv}}
\\moderncvstyle{{banking}}
\\moderncvcolor{{blue}}
\\usepackage[scale=0.75]{{geometry}}
\\usepackage[utf8]{{inputenc}}

% Personal data
\\name{{{self.personal_info['name']}}}{{}}
\\title{{Software Developer}}
\\address{{Gothenburg, Sweden}}
\\phone{{{self.personal_info['phone']}}}
\\email{{{self.personal_info['email']}}}
\\social[linkedin]{{{self.personal_info['linkedin']}}}
\\social[github]{{{self.personal_info['github']}}}

\\begin{{document}}
\\makecvtitle

% Customized for: {job['title']} at {job['company']}

\\section{{Professional Summary}}
\\cvitem{{}}{{Experienced Software Developer with strong expertise in Python and backend development. Specialized in building scalable applications and microservices. Passionate about {job['company'].lower()} and {job['title'].lower()} role with focus on {'automotive' if 'volvo' in job['company'].lower() or 'automotive' in job_requirements else 'technology'} solutions.}}

\\section{{Technical Skills}}
\\cvitem{{Programming}}{{\\textbf{{{', '.join(highlighted_skills[:4])}}}}}
\\cvitem{{Frameworks}}{{\\textbf{{{', '.join(highlighted_skills[4:8] if len(highlighted_skills) > 4 else highlighted_skills)}}}}}
\\cvitem{{Tools \& Cloud}}{{Docker, Kubernetes, AWS, Git, Linux, CI/CD}}
\\cvitem{{Databases}}{{PostgreSQL, MySQL, Redis, MongoDB}}

\\section{{Work Experience}}
\\cventry{{2021--Present}}{{Senior Software Developer}}{{Tech Company AB}}{{Stockholm, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Developed and maintained Python applications using FastAPI and Django
\\item Built microservices architecture serving 100K+ daily users
\\item Implemented CI/CD pipelines reducing deployment time by 60\\%
{"\\item Experience with automotive industry systems and protocols" if 'automotive' in job_requirements or 'volvo' in job['company'].lower() else "\\item Collaborated with cross-functional teams on product development"}
\\item Led backend optimization improving API response times by 40\\%
\\end{{itemize}}
}}

\\cventry{{2019--2021}}{{Backend Developer}}{{Startup Solutions}}{{Gothenburg, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Designed RESTful APIs and database schemas for web applications
\\item Worked with PostgreSQL and implemented data migration strategies
{"\\item Developed IoT data processing systems" if 'iot' in job_requirements else "\\item Integrated third-party APIs and payment systems"}
\\item Participated in agile development and code review processes
\\end{{itemize}}
}}

\\section{{Education}}
\\cventry{{2015--2019}}{{Bachelor of Science in Computer Science}}{{University of Gothenburg}}{{Gothenburg, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Focus on Software Engineering and Database Systems
\\item Thesis: {"Machine Learning Applications in Automotive Systems" if 'automotive' in job_requirements else "Scalable Web Application Development"}
\\end{{itemize}}
}}

\\section{{Projects}}
\\cventry{{}}{{Job Automation System}}{{Personal Project}}{{}}{{}}{{
\\begin{{itemize}}
\\item Built Python application for automated job searching and application tracking
\\item Implemented email integration and document generation using LaTeX
\\item Technologies: Python, FastAPI, PostgreSQL, Supabase
\\end{{itemize}}
}}

{"\\section{Certifications}" if 'aws' in job_requirements.lower() else ""}
{"\\cvitem{AWS}{Amazon Web Services Solutions Architect Associate}" if 'aws' in job_requirements.lower() else ""}
{"\\cvitem{Docker}{Docker Certified Associate}" if 'docker' in job_requirements.lower() else ""}

\\section{{Languages}}
\\cvitemwithcomment{{Swedish}}{{Native}}{{}}
\\cvitemwithcomment{{English}}{{Fluent}}{{Professional working proficiency}}

\\end{{document}}"""
        
        return latex_content
    
    def generate_cover_letter_latex(self, job: Dict[str, Any]) -> str:
        """Generate customized LaTeX cover letter for specific job"""
        
        company = job['company']
        position = job['title']
        location = job.get('location', 'Gothenburg, Sweden')
        
        # Customize content based on company and role
        company_specific = ""
        if 'volvo' in company.lower():
            company_specific = "I am particularly excited about Volvo's leadership in sustainable transportation and automotive innovation."
        elif 'spotify' in company.lower():
            company_specific = "I am passionate about Spotify's mission to unlock the potential of human creativity through music technology."
        elif 'klarna' in company.lower():
            company_specific = "I admire Klarna's innovative approach to financial technology and smooth payment solutions."
        elif 'polestar' in company.lower():
            company_specific = "I am excited about Polestar's vision for sustainable electric mobility and cutting-edge automotive technology."
        else:
            company_specific = f"I am impressed by {company}'s reputation for innovation and technical excellence."
        
        # Customize technical focus based on role
        technical_focus = ""
        if 'senior' in position.lower():
            technical_focus = "My experience leading backend development projects and mentoring junior developers aligns well with the senior responsibilities of this role."
        elif 'machine learning' in position.lower() or 'ml' in position.lower():
            technical_focus = "My background in Python and experience with data processing makes me well-suited for machine learning applications."
        elif 'devops' in position.lower():
            technical_focus = "My experience with Docker, Kubernetes, and CI/CD pipelines directly matches the DevOps requirements."
        elif 'full stack' in position.lower() or 'fullstack' in position.lower():
            technical_focus = "My comprehensive experience with both backend Python development and frontend technologies makes me ideal for full stack development."
        else:
            technical_focus = "My strong Python and backend development experience aligns perfectly with the technical requirements."
        
        latex_content = f"""\\documentclass[11pt,a4paper]{{letter}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{fontspec}}
\\setmainfont{{Times New Roman}}

\\signature{{{self.personal_info['name']}}}
\\address{{{self.personal_info['name']} \\\\ {self.personal_info['location']} \\\\ {self.personal_info['phone']} \\\\ {self.personal_info['email']}}}

\\begin{{document}}

\\begin{{letter}}{{Hiring Manager \\\\ {company} \\\\ {location}}}

\\opening{{Dear Hiring Manager,}}

I am writing to express my strong interest in the {position} position at {company}. With my extensive experience in Python development and passion for building scalable software solutions, I am confident that I would be a valuable addition to your team.

{company_specific}

In my current role as Senior Software Developer, I have developed expertise in Python, FastAPI, and PostgreSQL, which directly aligns with your requirements. I have successfully built and maintained microservices architectures serving over 100,000 daily users and implemented CI/CD pipelines that reduced deployment times by 60\\%.

{technical_focus} Additionally, my experience with Docker, Kubernetes, and cloud technologies enables me to contribute to modern development practices and infrastructure management.

What particularly attracts me to this position is the opportunity to work on {"automotive technology and sustainable transportation solutions" if any(word in company.lower() for word in ['volvo', 'polestar', 'automotive']) else "innovative technology solutions"} at {company}. My technical skills combined with my collaborative approach and problem-solving abilities make me well-suited for this challenging role.

Key highlights of my qualifications include:
\\begin{{itemize}}
\\item 5+ years of Python development experience with FastAPI and Django
\\item Proven track record in building scalable backend systems and APIs
\\item Experience with PostgreSQL, Docker, and cloud deployment
\\item Strong problem-solving skills and attention to code quality
{"\\item Knowledge of automotive industry standards and protocols" if any(word in company.lower() for word in ['volvo', 'polestar', 'automotive']) else "\\item Experience working in agile development environments"}
\\end{{itemize}}

I am excited about the possibility of contributing to {company}'s continued success and would welcome the opportunity to discuss how my skills and experience align with your team's needs. Thank you for considering my application.

\\closing{{Sincerely,}}

\\end{{letter}}
\\end{{document}}"""
        
        return latex_content
    
    def compile_latex_to_pdf(self, latex_content: str, filename: str) -> bool:
        """Compile LaTeX content to PDF"""
        try:
            # Write LaTeX content to file
            tex_file = os.path.join(self.output_dir, f"{filename}.tex")
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile to PDF
            result = subprocess.run(
                ['pdflatex', '-output-directory', self.output_dir, tex_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Generated PDF: {filename}.pdf")
                return True
            else:
                print(f"❌ LaTeX compilation failed for {filename}")
                print(f"Error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("❌ pdflatex not found. Please install TeX Live or MiKTeX")
            return False
        except Exception as e:
            print(f"❌ Error compiling {filename}: {e}")
            return False
    
    def generate_documents_for_job(self, job: Dict[str, Any]) -> tuple[bool, bool]:
        """Generate both resume and cover letter for a specific job"""
        company_clean = job['company'].replace(' ', '_').replace('(', '').replace(')', '')
        position_clean = job['title'].replace(' ', '_').replace('/', '_')
        
        print(f"📄 Generating documents for: {job['title']} at {job['company']}")
        
        # Generate resume
        resume_latex = self.generate_resume_latex(job)
        resume_filename = f"cv_{company_clean}_{position_clean}"
        resume_success = self.compile_latex_to_pdf(resume_latex, resume_filename)
        
        # Generate cover letter
        cover_letter_latex = self.generate_cover_letter_latex(job)
        cover_letter_filename = f"cover_letter_{company_clean}_{position_clean}"
        cover_letter_success = self.compile_latex_to_pdf(cover_letter_latex, cover_letter_filename)
        
        return resume_success, cover_letter_success

def get_saved_jobs() -> List[Dict[str, Any]]:
    """Retrieve all saved jobs from database"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Get all jobs, prioritizing Gothenburg and saved jobs
        result = supabase.table('jobs').select('*').order('match_score', desc=True).execute()
        
        if result.data:
            print(f"📊 Found {len(result.data)} jobs in database")
            return result.data
        else:
            print("❌ No jobs found in database")
            return []
            
    except Exception as e:
        print(f"❌ Error retrieving jobs: {e}")
        return []

def main():
    """Main function to generate documents for all saved jobs"""
    print("📄 LaTeX Resume & Cover Letter Generator")
    print("=" * 60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get jobs from database
    jobs = get_saved_jobs()
    if not jobs:
        print("No jobs to process!")
        return
    
    # Initialize generator
    generator = LaTeXDocumentGenerator()
    
    print(f"🔍 Processing {len(jobs)} jobs...")
    print()
    
    total_resumes = 0
    total_cover_letters = 0
    
    # Filter for priority jobs (Gothenburg and high match scores)
    priority_jobs = [job for job in jobs if 
                    'gothenburg' in job.get('location', '').lower() or 
                    job.get('match_score', 0) >= 0.90 or
                    job.get('source') == 'linkedin_saved']
    
    print(f"📋 Generating documents for {len(priority_jobs)} priority jobs:")
    
    for i, job in enumerate(priority_jobs, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job.get('location', 'N/A')}")
        print(f"   Match Score: {job.get('match_score', 0):.2f}")
        print(f"   Source: {job.get('source', 'N/A')}")
        
        resume_success, cover_letter_success = generator.generate_documents_for_job(job)
        
        if resume_success:
            total_resumes += 1
        if cover_letter_success:
            total_cover_letters += 1
    
    print(f"\n🎯 GENERATION RESULTS:")
    print(f"   📄 Resumes generated: {total_resumes}/{len(priority_jobs)}")
    print(f"   📝 Cover letters generated: {total_cover_letters}/{len(priority_jobs)}")
    print(f"   📁 Output directory: {generator.output_dir}/")
    
    if total_resumes > 0 or total_cover_letters > 0:
        print(f"\n✅ Document generation completed!")
        print(f"📂 Check the '{generator.output_dir}' folder for generated PDFs")
    else:
        print(f"\n⚠️  No documents were generated. Check LaTeX installation.")

if __name__ == "__main__":
    main()