#!/usr/bin/env python3
"""
Create simplified LaTeX templates using standard packages
"""

import os
from pathlib import Path

def create_simple_latex_template(job_info):
    """Create a simple LaTeX resume template using standard packages"""
    
    company = job_info['company']
    position = job_info['title']
    location = job_info.get('location', 'Gothenburg, Sweden')
    
    # Use basic article class instead of moderncv
    latex_content = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}

% Remove page numbers
\\pagestyle{{empty}}

% Define section formatting
\\titleformat{{\\section}}{{\\large\\bfseries}}{{}}{{0em}}{{}}[\\titlerule]

\\begin{{document}}

% Header
\\begin{{center}}
{{\\LARGE \\textbf{{Your Full Name}}}} \\\\[0.2cm]
Software Developer \\\\[0.1cm]
Gothenburg, Sweden $\\cdot$ +46 70 123 4567 $\\cdot$ your.email@example.com \\\\
LinkedIn: linkedin.com/in/yourprofile $\\cdot$ GitHub: github.com/yourusername
\\end{{center}}

\\vspace{{0.5cm}}

% Customized for specific job
\\begin{{center}}
\\textit{{Application for {position} at {company}}}
\\end{{center}}

\\section{{Professional Summary}}
Experienced Software Developer with strong expertise in Python and backend development. {"Specialized in automotive software solutions and" if 'volvo' in company.lower() or 'automotive' in position.lower() else "Passionate about building scalable applications and"} proven track record in microservices architecture. Seeking to contribute technical skills to {company}'s {position.lower()} role.

\\section{{Technical Skills}}
\\begin{{itemize}}[leftmargin=0pt, itemsep=0pt]
\\item \\textbf{{Programming Languages:}} Python, JavaScript, TypeScript, SQL
\\item \\textbf{{Frameworks \\& Libraries:}} FastAPI, Django, React, Flask
\\item \\textbf{{Databases:}} PostgreSQL, MySQL, Redis, MongoDB
\\item \\textbf{{Tools \\& Technologies:}} Docker, Kubernetes, AWS, Git, Linux
\\item \\textbf{{Development:}} REST APIs, Microservices, CI/CD, Test-Driven Development
\\end{{itemize}}

\\section{{Work Experience}}

\\textbf{{Senior Software Developer}} \\hfill 2021 -- Present \\\\
\\textit{{TechCorp AB, Stockholm, Sweden}}
\\begin{{itemize}}[leftmargin=15pt, itemsep=0pt]
\\item Developed and maintained Python applications using FastAPI and Django frameworks
\\item Built microservices architecture serving 100,000+ daily users with 99.9\\% uptime
\\item Implemented CI/CD pipelines reducing deployment time by 60\\% and improving reliability
{"\\item Experience with automotive industry protocols and real-time embedded systems" if 'automotive' in position.lower() or 'volvo' in company.lower() else "\\item Led backend optimization projects improving API response times by 40\\%"}
{"\\item Mentored junior developers and led technical architecture decisions" if 'senior' in position.lower() else "\\item Collaborated with cross-functional teams on agile product development"}
\\end{{itemize}}

\\textbf{{Backend Developer}} \\hfill 2019 -- 2021 \\\\
\\textit{{Innovation Solutions, Gothenburg, Sweden}}
\\begin{{itemize}}[leftmargin=15pt, itemsep=0pt]
\\item Designed and implemented RESTful APIs using Python and PostgreSQL
\\item Integrated third-party services and payment processing systems
{"\\item Developed IoT data processing systems for industrial applications" if 'iot' in position.lower() or 'industrial' in company.lower() else "\\item Built data migration tools and performed database optimization"}
\\item Participated in agile development process and conducted thorough code reviews
\\end{{itemize}}

\\section{{Education}}

\\textbf{{Bachelor of Science in Computer Science}} \\hfill 2015 -- 2019 \\\\
\\textit{{University of Gothenburg, Gothenburg, Sweden}}
\\begin{{itemize}}[leftmargin=15pt, itemsep=0pt]
\\item Specialization in Software Engineering and Database Systems
\\item Thesis: {"Automotive Software Systems and Real-time Data Processing" if 'automotive' in position.lower() else "Scalable Web Application Architecture and Performance Optimization"}
\\item Relevant coursework: Algorithms, Database Design, Software Architecture, System Design
\\end{{itemize}}

\\section{{Key Projects}}

\\textbf{{JobHunter Automation System}} \\hfill 2024 \\\\
\\textit{{Personal Project}}
\\begin{{itemize}}[leftmargin=15pt, itemsep=0pt]
\\item Built comprehensive job search automation using Python, FastAPI, and PostgreSQL
\\item Implemented database design with Supabase and automated document generation
\\item Integrated email processing and LaTeX-based CV/cover letter generation
\\item Technologies: Python, FastAPI, PostgreSQL, Supabase, LaTeX, Docker
\\end{{itemize}}

{"\\section{Certifications}" if any(cert in position.lower() for cert in ['aws', 'docker', 'devops']) else ""}
{"\\begin{itemize}[leftmargin=0pt, itemsep=0pt]" if any(cert in position.lower() for cert in ['aws', 'docker', 'devops']) else ""}
{"\\item Amazon Web Services Solutions Architect Associate" if 'aws' in position.lower() else ""}
{"\\item Docker Certified Associate" if 'docker' in position.lower() else ""}
{"\\end{itemize}" if any(cert in position.lower() for cert in ['aws', 'docker', 'devops']) else ""}

\\section{{Languages}}
\\begin{{itemize}}[leftmargin=0pt, itemsep=0pt]
\\item \\textbf{{Swedish:}} Native proficiency
\\item \\textbf{{English:}} Professional working proficiency
\\end{{itemize}}

\\end{{document}}"""
    
    return latex_content

def create_simple_cover_letter_template(job_info):
    """Create a simple LaTeX cover letter template"""
    
    company = job_info['company']
    position = job_info['title']
    location = job_info.get('location', 'Gothenburg, Sweden')
    
    latex_content = f"""\\documentclass[11pt,a4paper]{{letter}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage[utf8]{{inputenc}}

\\signature{{Your Full Name}}
\\address{{Your Full Name \\\\ Gothenburg, Sweden \\\\ +46 70 123 4567 \\\\ your.email@example.com}}

\\begin{{document}}

\\begin{{letter}}{{Hiring Manager \\\\ {company} \\\\ {location}}}

\\opening{{Dear Hiring Manager,}}

I am writing to express my strong interest in the {position} position at {company}. With my extensive experience in Python development and passion for building scalable software solutions, I am confident that I would be a valuable addition to your development team.

{"I am particularly excited about " + company + "'s leadership in automotive innovation and sustainable transportation technology." if 'volvo' in company.lower() or 'polestar' in company.lower() else "I am impressed by " + company + "'s reputation for technical excellence and innovative solutions."}

In my current role as Senior Software Developer, I have developed comprehensive expertise in Python, FastAPI, and PostgreSQL, which directly aligns with your technical requirements. I have successfully built and maintained microservices architectures serving over 100,000 daily users and implemented CI/CD pipelines that reduced deployment times by 60\\%.

{"My experience with automotive industry standards and real-time systems" if 'automotive' in position.lower() or 'volvo' in company.lower() else "My strong technical background in backend development"} makes me well-suited for this role. Additionally, my experience with Docker, Kubernetes, and cloud technologies enables me to contribute to modern development practices and infrastructure management.

Key highlights of my qualifications include:
\\begin{{itemize}}
\\item 5+ years of Python development experience with FastAPI and Django
\\item Proven track record in building scalable backend systems and RESTful APIs
\\item Experience with PostgreSQL, Docker, and cloud deployment platforms
\\item Strong problem-solving skills and commitment to code quality and best practices
{"\\item Knowledge of automotive industry protocols and embedded systems" if 'automotive' in position.lower() or 'volvo' in company.lower() else "\\item Experience working in agile development environments with cross-functional teams"}
\\end{{itemize}}

I am excited about the opportunity to contribute to {company}'s continued success and would welcome the chance to discuss how my skills and experience align with your team's needs. Thank you for considering my application.

\\closing{{Sincerely,}}

\\end{{letter}}
\\end{{document}}"""
    
    return latex_content

def compile_simple_documents():
    """Compile documents using simple LaTeX templates"""
    
    print("🚀 Compiling Simple LaTeX Documents")
    print("=" * 50)
    
    # Create simple_pdfs directory
    output_dir = Path("simple_pdfs")
    output_dir.mkdir(exist_ok=True)
    
    # Priority Gothenburg jobs
    priority_jobs = [
        {"company": "Volvo Group", "title": "Senior Python Developer", "location": "Gothenburg, Sweden"},
        {"company": "Polestar", "title": "Machine Learning Engineer", "location": "Gothenburg, Sweden"},
        {"company": "Zenseact (Volvo)", "title": "Full Stack Developer", "location": "Gothenburg, Sweden"},
        {"company": "SKF Group", "title": "Backend Developer", "location": "Gothenburg, Sweden"},
        {"company": "Hasselblad", "title": "DevOps Engineer", "location": "Gothenburg, Sweden"},
    ]
    
    compiled_count = 0
    
    for job in priority_jobs:
        company_clean = job['company'].replace(' ', '_').replace('(', '').replace(')', '')
        position_clean = job['title'].replace(' ', '_')
        
        print(f"📄 Generating: {job['title']} at {job['company']}")
        
        # Create CV
        cv_latex = create_simple_latex_template(job)
        cv_filename = f"cv_{company_clean}_{position_clean}.tex"
        cv_path = output_dir / cv_filename
        
        with open(cv_path, 'w', encoding='utf-8') as f:
            f.write(cv_latex)
        
        # Create Cover Letter
        cl_latex = create_simple_cover_letter_template(job)
        cl_filename = f"cover_letter_{company_clean}_{position_clean}.tex"
        cl_path = output_dir / cl_filename
        
        with open(cl_path, 'w', encoding='utf-8') as f:
            f.write(cl_latex)
        
        print(f"   ✅ Created: {cv_filename}")
        print(f"   ✅ Created: {cl_filename}")
        
    print(f"\n🔧 Now compiling to PDF...")
    
    # Compile all .tex files in simple_pdfs
    os.chdir(output_dir)
    
    for tex_file in Path('.').glob('*.tex'):
        print(f"📄 Compiling: {tex_file.name}")
        
        # Use full path to pdflatex
        result = os.system(f"/usr/local/texlive/2025basic/bin/universal-darwin/pdflatex -interaction=nonstopmode {tex_file.name} > /dev/null 2>&1")
        
        if result == 0:
            print(f"   ✅ Success: {tex_file.stem}.pdf")
            compiled_count += 1
        else:
            print(f"   ❌ Failed: {tex_file.name}")
    
    # Clean up auxiliary files
    for aux_file in Path('.').glob('*.aux'):
        aux_file.unlink()
    for log_file in Path('.').glob('*.log'):
        log_file.unlink()
    for out_file in Path('.').glob('*.out'):
        out_file.unlink()
    
    # List generated PDFs
    pdf_files = list(Path('.').glob('*.pdf'))
    
    print(f"\n🎯 COMPILATION RESULTS:")
    print(f"   ✅ Successfully compiled: {compiled_count} documents")
    print(f"   📁 Location: simple_pdfs/")
    
    if pdf_files:
        print(f"\n📋 GENERATED PDFs:")
        for pdf in sorted(pdf_files):
            print(f"   📄 {pdf.name}")
    
    os.chdir('..')
    
    return compiled_count

if __name__ == "__main__":
    compiled = compile_simple_documents()
    if compiled > 0:
        print(f"\n🎉 Successfully generated {compiled} PDF documents!")
        print(f"📂 Check the 'simple_pdfs' folder for your job application materials.")
    else:
        print(f"\n⚠️  No documents were compiled successfully.")