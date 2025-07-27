#!/usr/bin/env python3
"""
Test single job processing with simpler LaTeX
"""
import asyncio
import subprocess
import tempfile
import shutil
import os
from pathlib import Path

def create_simple_tailored_cv(job_title, company):
    """Create simple CV with dark blue color"""
    return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=0.8in]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

% Define dark blue color (LinkedIn blue)
\\definecolor{{darkblue}}{{RGB}}{{0,51,102}}

\\hypersetup{{
    colorlinks=true,
    linkcolor=darkblue,
    urlcolor=darkblue,
    citecolor=darkblue
}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{8pt}}

\\begin{{document}}

% Header
\\begin{{center}}
{{\\huge \\textbf{{\\textcolor{{darkblue}}{{Hongzhi Li}}}}}}\\\\
\\vspace{{8pt}}
{{\\Large \\textcolor{{darkblue}}{{{job_title}}}}}\\\\
\\vspace{{12pt}}
hongzhili01@gmail.com $\\bullet$ 0728384299 $\\bullet$ LinkedIn $\\bullet$ GitHub
\\end{{center}}

\\vspace{{15pt}}

{{\\large\\textbf{{\\textcolor{{darkblue}}{{Profile Summary}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}
\\vspace{{8pt}}

Experienced Fullstack Developer with over 5 years specializing in {job_title.lower()} technologies. Proven expertise in building scalable applications for companies like {company}. Currently serving as IT/Infrastructure Specialist at ECARX.

\\vspace{{10pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Technical Skills}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}
\\vspace{{8pt}}

\\textbf{{Programming:}} Java/J2EE, JavaScript, C\\#/.NET Core, Python\\\\
\\textbf{{Frameworks:}} Spring Boot, Angular, React, .NET Core\\\\
\\textbf{{Cloud:}} AWS, Azure, Kubernetes, Docker\\\\
\\textbf{{Databases:}} PostgreSQL, MySQL, MongoDB

\\vspace{{10pt}}
{{\\large\\textbf{{\\textcolor{{darkblue}}{{Experience}}}}}}\\\\
\\textcolor{{darkblue}}{{\\hrule}}
\\vspace{{8pt}}

\\textbf{{ECARX}} --- IT/Infrastructure Specialist (Oct 2024 - Present)\\\\
Leading infrastructure optimization and system integration projects.

\\textbf{{Synteda}} --- Azure Fullstack Developer (Aug 2023 - Sep 2024)\\\\
Developed comprehensive talent management system using C\\# and .NET Core.

\\textbf{{IT-Högskolan}} --- Backend Developer (Jan 2023 - May 2023)\\\\
Migrated adult education platform using Spring Boot backend services.

\\end{{document}}"""

def compile_latex(tex_content, output_name):
    """Compile LaTeX to PDF"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / f"{output_name}.tex"
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        
        try:
            result = subprocess.run([
                'pdflatex', 
                '-interaction=nonstopmode',
                '-output-directory', str(temp_path),
                str(tex_file)
            ], capture_output=True, text=True, cwd=temp_path)
            
            if result.returncode != 0:
                print("LaTeX Error:")
                print(result.stdout[-500:])
                return None
            
            pdf_file = temp_path / f"{output_name}.pdf"
            if pdf_file.exists():
                final_path = f"{output_name}.pdf"
                shutil.copy2(pdf_file, final_path)
                return final_path
            
        except Exception as e:
            print(f"Error: {e}")
            return None

def main():
    print("🧪 Testing single job processing...")
    
    # Test simple CV generation
    cv_content = create_simple_tailored_cv("Backend Developer", "Spotify")
    cv_pdf = compile_latex(cv_content, "test_spotify_backend")
    
    if cv_pdf:
        size = os.path.getsize(cv_pdf) / 1024
        print(f"✅ CV generated: {cv_pdf} ({size:.1f} KB)")
        return True
    else:
        print("❌ CV generation failed")
        return False

if __name__ == "__main__":
    main()