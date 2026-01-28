#!/usr/bin/env python3
"""
Test CV generation for all role types
Generates sample CVs to verify 6+ years experience is showing correctly
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from cv_lego_bricks import CVLegoBricks
import subprocess
import os

def generate_latex_cv(role_type: str, output_filename: str):
    """Generate a CV for a specific role type"""
    
    lego = CVLegoBricks()
    
    # Mock job details for each role type
    job_details = {
        'devops_cloud': {
            'title': 'Senior DevOps Engineer',
            'company': 'Tech Company',
            'description': 'kubernetes docker terraform aws azure ci/cd devops infrastructure',
            'requirements': ['Kubernetes', 'Docker', 'Terraform', 'AWS', 'Azure']
        },
        'backend': {
            'title': 'Senior Backend Developer',
            'company': 'Tech Company',
            'description': 'java spring boot .net core backend api microservices postgresql',
            'requirements': ['Java', 'Spring Boot', '.NET Core', 'PostgreSQL']
        },
        'frontend': {
            'title': 'Senior Frontend Developer',
            'company': 'Tech Company',
            'description': 'react typescript angular vue.js frontend javascript',
            'requirements': ['React', 'TypeScript', 'Angular', 'Vue.js']
        },
        'fullstack': {
            'title': 'Senior Fullstack Developer',
            'company': 'Tech Company',
            'description': 'fullstack react node.js java spring boot .net frontend backend',
            'requirements': ['React', 'Node.js', 'Java', 'Spring Boot']
        },
        'android': {
            'title': 'Senior Android Developer',
            'company': 'Tech Company',
            'description': 'android kotlin java mobile app development sdk',
            'requirements': ['Android', 'Kotlin', 'Java', 'Mobile']
        },
        'business_analyst': {
            'title': 'IT Business Analyst',
            'company': 'Tech Company',
            'description': 'business analyst requirements gathering stakeholder workshops',
            'requirements': ['Business Analysis', 'Requirements', 'Stakeholder Management']
        }
    }
    
    job = job_details.get(role_type, job_details['devops_cloud'])
    
    # Build CV components
    cv_components = lego.build_cv_for_job(job, application_type=f'{role_type}_focused')
    
    # Build complete LaTeX document
    latex_content = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{titlesec}}

\\geometry{{left=2cm,right=2cm,top=2cm,bottom=2cm}}
\\setlength{{\\parindent}}{{0pt}}
\\pagestyle{{empty}}

\\definecolor{{titlecolor}}{{RGB}}{{0,102,204}}

\\titleformat{{\\section}}{{\\Large\\bfseries\\color{{titlecolor}}}}{{}}{{0em}}{{}}[\\titlerule]
\\titlespacing*{{\\section}}{{0pt}}{{12pt}}{{6pt}}

\\titleformat{{\\subsection}}{{\\large\\bfseries}}{{}}{{0em}}{{}}
\\titlespacing*{{\\subsection}}{{0pt}}{{8pt}}{{4pt}}

\\begin{{document}}

\\begin{{center}}
{{\\LARGE \\textbf{{Harvad (Hongzhi) Li}}}}\\\\[10pt]
{{\\Large \\textit{{{job['title']}}}}}\\\\[10pt]
\\textcolor{{titlecolor}}{{\\href{{mailto:hongzhili01@gmail.com}}{{hongzhili01@gmail.com}} | \\href{{tel:+46728384299}}{{+46 72 838 4299}} | \\href{{https://www.linkedin.com/in/hzl/}}{{LinkedIn}} | \\href{{https://github.com/bluehawana}}{{GitHub}}}}
\\end{{center}}

\\vspace{{8pt}}

\\section*{{Professional Summary}}
{cv_components['profile']}

\\section*{{Core Technical Skills}}
{cv_components['skills']}

\\section*{{Professional Experience}}
{cv_components['experience']}

{cv_components['projects']}

\\section*{{Education}}

\\textbf{{IT-Högskolan}} | Bachelor's in .NET Cloud Development | 2021-2023 | Gothenburg

\\textbf{{Molndal Campus}} | Bachelor's in Java Integration | 2019-2021 | Molndal

\\textbf{{University of Gothenburg}} | Master's in International Business | 2016-2019 | Gothenburg

\\section*{{Certifications}}

\\begin{{itemize}}[leftmargin=*, itemsep=2pt]
\\item AWS Certified Solutions Architect - Associate (2022)
\\item Microsoft Certified: Azure Fundamentals (2022)
\\item AWS Certified Data Analytics - Specialty (2022)
\\end{{itemize}}

\\section*{{Community Involvement}}

\\begin{{itemize}}[leftmargin=*, itemsep=2pt]
\\item Active member of AWS User Group Gothenburg
\\item Participant in CNCF Gothenburg community events
\\item CNCF Scholarship Recipient - CKAD Training \\& Exam Voucher
\\item Member of Kubernetes Community Gothenburg
\\end{{itemize}}

\\section*{{Additional Information}}

\\textbf{{Languages:}} English (Fluent), Swedish (B2), Chinese (Native)

\\textbf{{Work Authorization:}} Swedish Permanent Residence

\\textbf{{Availability:}} Immediate

\\end{{document}}
"""
    
    return latex_content


def compile_latex_to_pdf(latex_content: str, output_name: str):
    """Compile LaTeX to PDF"""
    
    # Create output directory
    output_dir = Path('test_cv_output')
    output_dir.mkdir(exist_ok=True)
    
    # Write LaTeX file
    tex_file = output_dir / f'{output_name}.tex'
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"📝 Generated LaTeX: {tex_file}")
    
    # Compile to PDF using pdflatex
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        pdf_file = output_dir / f'{output_name}.pdf'
        if pdf_file.exists():
            print(f"✅ Generated PDF: {pdf_file}")
            return True
        else:
            print(f"❌ PDF generation failed for {output_name}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ PDF compilation timeout for {output_name}")
        return False
    except FileNotFoundError:
        print("❌ pdflatex not found. Please install LaTeX (e.g., brew install --cask mactex-no-gui)")
        return False


def main():
    """Generate CVs for all role types"""
    
    print("🚀 Generating test CVs for all role types...\n")
    
    role_types = [
        ('devops_cloud', 'DevOps_Cloud_Engineer_CV'),
        ('backend', 'Backend_Developer_CV'),
        ('frontend', 'Frontend_Developer_CV'),
        ('fullstack', 'Fullstack_Developer_CV'),
        ('android', 'Android_Developer_CV'),
        ('business_analyst', 'IT_Business_Analyst_CV'),
    ]
    
    success_count = 0
    total_count = len(role_types)
    
    for role_type, output_name in role_types:
        print(f"\n{'='*60}")
        print(f"Generating CV for: {role_type.upper()}")
        print(f"{'='*60}")
        
        try:
            latex_content = generate_latex_cv(role_type, output_name)
            if compile_latex_to_pdf(latex_content, output_name):
                success_count += 1
        except Exception as e:
            print(f"❌ Error generating {role_type}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"📊 Summary: {success_count}/{total_count} CVs generated successfully")
    print(f"{'='*60}")
    
    if success_count > 0:
        print(f"\n✅ Generated CVs are in: test_cv_output/")
        print(f"\nTo deploy to VPS:")
        print(f"1. Review the generated PDFs")
        print(f"2. Commit changes: git add . && git commit -m 'Test CV generation'")
        print(f"3. Push to GitHub: git push origin main")
        print(f"4. SSH to VPS and pull: ssh user@vps 'cd /path/to/jobhunter && git pull'")


if __name__ == '__main__':
    main()
