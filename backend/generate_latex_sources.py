#!/usr/bin/env python3
"""
Generate LaTeX source files for resumes and cover letters (no compilation required)
"""

import os
import sys
from datetime import datetime, date
from typing import List, Dict, Any

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from supabase import create_client, Client

def generate_latex_sources():
    """Generate LaTeX source files for all priority jobs"""
    
    print("📄 LaTeX Document Source Generator")
    print("=" * 60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create output directory
    output_dir = "latex_sources"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get jobs from database
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        result = supabase.table('jobs').select('*').order('match_score', desc=True).execute()
        jobs = result.data if result.data else []
        
    except Exception as e:
        print(f"❌ Error retrieving jobs: {e}")
        return
    
    if not jobs:
        print("❌ No jobs found in database!")
        return
    
    print(f"📊 Found {len(jobs)} jobs in database")
    
    # Filter priority jobs (Gothenburg + high match scores)
    priority_jobs = [job for job in jobs if 
                    'gothenburg' in job.get('location', '').lower() or 
                    job.get('match_score', 0) >= 0.90]
    
    print(f"🎯 Generating LaTeX sources for {len(priority_jobs)} priority jobs:")
    print()
    
    generated_files = []
    
    for i, job in enumerate(priority_jobs, 1):
        company_clean = job['company'].replace(' ', '_').replace('(', '').replace(')', '')
        position_clean = job['title'].replace(' ', '_').replace('/', '_')
        
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   📍 {job.get('location', 'N/A')}")
        print(f"   ⭐ Match: {job.get('match_score', 0):.2f}")
        
        # Generate resume LaTeX
        resume_latex = generate_resume_latex_content(job)
        resume_filename = f"cv_{company_clean}_{position_clean}.tex"
        resume_path = os.path.join(output_dir, resume_filename)
        
        with open(resume_path, 'w', encoding='utf-8') as f:
            f.write(resume_latex)
        
        generated_files.append(resume_filename)
        print(f"   ✅ Resume: {resume_filename}")
        
        # Generate cover letter LaTeX
        cover_letter_latex = generate_cover_letter_latex_content(job)
        cover_letter_filename = f"cover_letter_{company_clean}_{position_clean}.tex"
        cover_letter_path = os.path.join(output_dir, cover_letter_filename)
        
        with open(cover_letter_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter_latex)
        
        generated_files.append(cover_letter_filename)
        print(f"   ✅ Cover Letter: {cover_letter_filename}")
        print()
    
    # Create compilation script
    create_compilation_script(output_dir, generated_files)
    
    print(f"🎯 RESULTS:")
    print(f"   📄 Generated {len(generated_files)} LaTeX files")
    print(f"   📁 Location: {output_dir}/")
    print()
    print(f"🔧 TO COMPILE TO PDF:")
    print(f"1. Install LaTeX: brew install basictex")
    print(f"2. Run: cd {output_dir} && ./compile_all.sh")
    print(f"3. Or manually: pdflatex filename.tex")

def generate_resume_latex_content(job: Dict[str, Any]) -> str:
    """Generate customized LaTeX resume content"""
    
    # Personal info (customize this)
    personal_info = {
        "name": "Your Full Name",
        "email": "your.email@example.com", 
        "phone": "+46 70 123 4567",
        "location": "Gothenburg, Sweden",
        "linkedin": "linkedin.com/in/yourprofile",
        "github": "github.com/yourusername"
    }
    
    # Extract job-specific information
    company = job['company']
    position = job['title']
    requirements = job.get('requirements', '').lower()
    skills_matched = job.get('skills_matched', [])
    
    # Prioritize skills based on job
    highlighted_skills = []
    all_skills = ["Python", "FastAPI", "Django", "PostgreSQL", "Docker", "Kubernetes", "AWS", "React", "TypeScript"]
    
    for skill in skills_matched:
        if skill in all_skills:
            highlighted_skills.append(skill)
    
    for skill in all_skills:
        if skill.lower() in requirements and skill not in highlighted_skills:
            highlighted_skills.append(skill)
    
    highlighted_skills = highlighted_skills[:6] if highlighted_skills else ["Python", "FastAPI", "PostgreSQL"]
    
    # Industry-specific customization
    is_automotive = any(word in company.lower() for word in ['volvo', 'polestar', 'automotive'])
    is_senior = 'senior' in position.lower()
    
    latex_content = f"""\\documentclass[11pt,a4paper,sans]{{moderncv}}
\\moderncvstyle{{banking}}
\\moderncvcolor{{blue}}
\\usepackage[scale=0.75]{{geometry}}
\\usepackage[utf8]{{inputenc}}

% Personal data
\\name{{{personal_info['name']}}}{{}}
\\title{{Software Developer}}
\\address{{{personal_info['location']}}}
\\phone{{{personal_info['phone']}}}
\\email{{{personal_info['email']}}}
\\social[linkedin]{{{personal_info['linkedin']}}}
\\social[github]{{{personal_info['github']}}}

\\begin{{document}}
\\makecvtitle

% Customized for: {position} at {company}

\\section{{Professional Summary}}
\\cvitem{{}}{{Experienced Software Developer with expertise in Python and backend systems. {"Strong background in automotive software development and" if is_automotive else "Passionate about building scalable applications and"} proven track record in microservices architecture. Seeking to contribute technical skills to {company}'s {position.lower()} role.}}

\\section{{Technical Skills}}
\\cvitem{{Languages}}{{\\textbf{{Python, JavaScript, TypeScript, SQL}}}}
\\cvitem{{Frameworks}}{{\\textbf{{{', '.join(highlighted_skills[:3])}}}}}
\\cvitem{{Technologies}}{{\\textbf{{{', '.join(highlighted_skills[3:6] if len(highlighted_skills) > 3 else ['Docker', 'Kubernetes', 'AWS'])}}}}}
\\cvitem{{Databases}}{{PostgreSQL, MySQL, Redis, MongoDB}}

\\section{{Work Experience}}
\\cventry{{2021--Present}}{{{"Senior " if is_senior else ""} Software Developer}}{{TechCorp AB}}{{Stockholm, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Developed Python applications using FastAPI and Django frameworks
\\item Built microservices architecture serving 100,000+ daily users
\\item Implemented CI/CD pipelines reducing deployment time by 60\\%
{"\\item Experience with automotive industry protocols and embedded systems" if is_automotive else "\\item Led backend optimization improving API response times by 40\\%"}
{"\\item Mentored junior developers and led technical architecture decisions" if is_senior else "\\item Collaborated with cross-functional teams on product development"}
\\end{{itemize}}
}}

\\cventry{{2019--2021}}{{Backend Developer}}{{Innovation Solutions}}{{Gothenburg, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Designed and implemented RESTful APIs using Python and PostgreSQL
\\item Integrated third-party services and payment processing systems
{"\\item Worked on IoT data processing and real-time analytics" if 'iot' in requirements else "\\item Developed data migration tools and database optimization"}
\\item Participated in agile development and conducted code reviews
\\end{{itemize}}
}}

\\section{{Education}}
\\cventry{{2015--2019}}{{Bachelor of Science in Computer Science}}{{University of Gothenburg}}{{Gothenburg, Sweden}}{{}}{{
\\begin{{itemize}}
\\item Specialization in Software Engineering and Database Systems
\\item Thesis: {"Automotive Software Systems and Real-time Processing" if is_automotive else "Scalable Web Application Architecture"}
\\item Relevant coursework: Algorithms, Database Design, Software Architecture
\\end{{itemize}}
}}

\\section{{Key Projects}}
\\cventry{{}}{{JobHunter Automation System}}{{Personal Project}}{{2024}}{{}}{{
\\begin{{itemize}}
\\item Built comprehensive job search automation using Python and FastAPI
\\item Implemented database design with PostgreSQL and Supabase
\\item Automated document generation using LaTeX and PDF processing
\\item Technologies: Python, FastAPI, PostgreSQL, Supabase, LaTeX
\\end{{itemize}}
}}

{"\\section{Certifications}" if any(cert in requirements for cert in ['aws', 'docker', 'kubernetes']) else ""}
{"\\cvitem{AWS}{Amazon Web Services Solutions Architect Associate}" if 'aws' in requirements else ""}
{"\\cvitem{Docker}{Docker Certified Associate}" if 'docker' in requirements else ""}

\\section{{Languages}}
\\cvitemwithcomment{{Swedish}}{{Native}}{{Fluent speaker}}
\\cvitemwithcomment{{English}}{{Professional}}{{Excellent written and verbal communication}}

\\end{{document}}"""
    
    return latex_content

def generate_cover_letter_latex_content(job: Dict[str, Any]) -> str:
    """Generate customized LaTeX cover letter content"""
    
    personal_info = {
        "name": "Your Full Name",
        "email": "your.email@example.com",
        "phone": "+46 70 123 4567",
        "location": "Gothenburg, Sweden"
    }
    
    company = job['company']
    position = job['title']
    location = job.get('location', 'Gothenburg, Sweden')
    requirements = job.get('requirements', '').lower()
    
    # Company-specific customization
    company_paragraph = ""
    if 'volvo' in company.lower():
        company_paragraph = "I am particularly drawn to Volvo's commitment to safety, sustainability, and innovation in the automotive industry. Your leadership in electric vehicles and autonomous driving technology aligns perfectly with my interests in cutting-edge software development."
    elif 'spotify' in company.lower():
        company_paragraph = "I am excited about Spotify's mission to unlock human creativity through music and audio. Your innovative approach to streaming technology and data-driven personalization represents the kind of impactful work I want to contribute to."
    elif 'klarna' in company.lower():
        company_paragraph = "I admire Klarna's revolutionary approach to financial technology and seamless payment solutions. Your focus on user experience and technical innovation in fintech is exactly where I want to apply my development skills."
    else:
        company_paragraph = f"I am impressed by {company}'s reputation for technical excellence and innovation. Your commitment to delivering high-quality solutions aligns with my professional values and technical standards."
    
    # Role-specific technical focus
    if 'senior' in position.lower():
        technical_focus = "My experience leading development projects and mentoring team members has prepared me well for the senior-level responsibilities of this role."
    elif 'machine learning' in position.lower():
        technical_focus = "My strong foundation in Python and data processing, combined with my experience in algorithm development, makes me well-suited for machine learning applications."
    elif 'devops' in position.lower():
        technical_focus = "My hands-on experience with Docker, Kubernetes, and CI/CD pipelines directly addresses the infrastructure and automation needs of this DevOps role."
    elif 'full stack' in position.lower():
        technical_focus = "My comprehensive experience with both backend Python development and frontend technologies positions me well for full stack development challenges."
    else:
        technical_focus = "My strong technical background in Python and backend development directly matches the requirements for this position."
    
    latex_content = f"""\\documentclass[11pt,a4paper]{{letter}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}

\\signature{{{personal_info['name']}}}
\\address{{{personal_info['name']} \\\\ {personal_info['location']} \\\\ {personal_info['phone']} \\\\ {personal_info['email']}}}

\\begin{{document}}

\\begin{{letter}}{{Hiring Manager \\\\ {company} \\\\ {location}}}

\\opening{{Dear Hiring Manager,}}

I am writing to express my strong interest in the {position} position at {company}. With my solid background in Python development and passion for building scalable software solutions, I am confident I would make a valuable contribution to your development team.

{company_paragraph}

In my current role as Software Developer, I have built extensive expertise in Python, FastAPI, and PostgreSQL, which aligns well with your technical requirements. I have successfully developed and maintained microservices architectures serving over 100,000 daily users and implemented CI/CD pipelines that improved deployment efficiency by 60\\%.

{technical_focus} My experience includes:

\\begin{{itemize}}
\\item 5+ years of Python development with modern frameworks (FastAPI, Django)
\\item Proven experience building scalable backend systems and RESTful APIs
\\item Strong database design skills with PostgreSQL and performance optimization
\\item Hands-on experience with Docker, Kubernetes, and cloud deployment
{"\\item Knowledge of automotive industry standards and embedded systems" if 'automotive' in requirements else "\\item Experience working in agile development environments with cross-functional teams"}
\\end{{itemize}}

What particularly excites me about this opportunity is the chance to work on {"innovative automotive technology and contribute to the future of sustainable transportation" if any(word in company.lower() for word in ['volvo', 'polestar']) else f"challenging technical problems and contribute to {company}'s continued innovation"}. My problem-solving approach, attention to code quality, and collaborative mindset make me well-suited for your team's dynamic environment.

I would welcome the opportunity to discuss how my technical skills and experience can contribute to {company}'s success. Thank you for your time and consideration.

\\closing{{Best regards,}}

\\end{{letter}}
\\end{{document}}"""
    
    return latex_content

def create_compilation_script(output_dir: str, generated_files: List[str]):
    """Create a shell script to compile all LaTeX files"""
    script_content = """#!/bin/bash
# LaTeX Compilation Script
# Run this to compile all .tex files to PDF

echo "🔄 Compiling LaTeX files to PDF..."
echo "=================================="

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found!"
    echo "Install LaTeX: brew install basictex"
    exit 1
fi

compiled=0
total=0

# Compile all .tex files
for file in *.tex; do
    if [ -f "$file" ]; then
        echo "📄 Compiling: $file"
        pdflatex -interaction=nonstopmode "$file" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "✅ Success: ${file%.tex}.pdf"
            compiled=$((compiled + 1))
        else
            echo "❌ Failed: $file"
        fi
        
        total=$((total + 1))
        
        # Clean up auxiliary files
        rm -f *.aux *.log *.out
    fi
done

echo "=================================="
echo "🎯 Results: $compiled/$total files compiled successfully"
echo "📁 Check for .pdf files in this directory"
"""
    
    script_path = os.path.join(output_dir, "compile_all.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)
    print(f"✅ Created compilation script: {script_path}")

if __name__ == "__main__":
    generate_latex_sources()