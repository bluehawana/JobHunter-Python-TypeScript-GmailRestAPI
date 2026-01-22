#!/usr/bin/env python3
"""
Generate CV and CL for Emerson IT Business Analyst role
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent / 'backend'))

from linkedin_job_extractor import extract_linkedin_job_info_from_content
from app.lego_api import analyze_job_description, customize_cover_letter, build_lego_cv, build_lego_cover_letter
from cv_templates import CVTemplateManager

def compile_latex_to_pdf(latex_content: str, output_name: str, output_dir: str) -> str:
    """Compile LaTeX to PDF and save to output directory"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, f"{output_name}.tex")

            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)

            # Run pdflatex twice for proper references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir
                )

            pdf_file = os.path.join(temp_dir, f"{output_name}.pdf")

            if os.path.exists(pdf_file):
                output_path = os.path.join(output_dir, f"{output_name}.pdf")
                # Copy to output directory
                import shutil
                shutil.copy(pdf_file, output_path)
                return output_path
            else:
                print(f"❌ PDF compilation failed")
                print(f"LaTeX errors: {result.stderr[:500] if result.stderr else 'None'}")
                # Save the .tex file for debugging
                debug_tex = os.path.join(output_dir, f"{output_name}.tex")
                with open(debug_tex, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                print(f"📄 Saved LaTeX source to: {debug_tex}")
                return None

    except Exception as e:
        print(f"❌ Error compiling LaTeX: {e}")
        return None

def generate_emerson_application():
    """Generate CV and CL for Emerson IT Business Analyst role"""

    emerson_job_description = """
    Job Description

    Are you eager to take your career to the next level? If yes, we encourage your application for IT Business Analyst role!

    In this role you be responsible for supporting and developing the IT function, while acting as a link for our business.

    By joining us as an IT Business Analyst in Mölnlycke, this role can be a strong foundation for your future career within Emerson. We encourage advancement and offer tangible development opportunities!

    In This Role, Your Responsibilities Will Be:

    Managing IT initiatives with a focus on digitalization and automation
    Analysing & document business processes and requirements
    Improving business processes using IT, business intelligence and automation
    Acting as project manager for identified initiatives. This includes project leadership, change management, analysing, developing specifications, planning, user training and implementation
    Developing IT solutions according to specification. Beside systemization and programming the development can include investigation, management documentation, user manuals, user training and implementation
    Providing the business with support in areas within the IT & Digitalization team's responsibility
    Applying best practices in development/support using tools in line with Emerson standards

    For This Role, You Will Need:

    Experience in business analysis and process improvement
    Project management skills with the ability to organize, structure, and plan effectively
    Experience with ERP systems and a solid understanding of business processes
    University degree in IT or equivalent experience
    Fluency in Swedish
    Proficiency in English language (verbal and written)
    General IT knowledge and at least 3 years of relevant professional experience

    Preferred Qualifications that Set You Apart:

    Experience in workshop facilitation and change management
    Professional experience from development of BI reports or RPA automations
    Experience from a manufacturing company
    Knowledge of Lean, Agile, and an interest in AI

    About Emerson

    Emerson is a global leader in automation technology and software.
    """

    emerson_url = "https://www.linkedin.com/jobs/view/emerson-it-business-analyst"
    output_dir = os.path.expanduser("~/Desktop")

    print("=" * 70)
    print("🚀 Generating Emerson IT Business Analyst Application")
    print("=" * 70)

    # Step 1: Analyze job
    print("\n1️⃣ Analyzing job description...")
    analysis = analyze_job_description(emerson_job_description, emerson_url)

    company = analysis.get('company', 'Emerson')
    title = analysis.get('title', 'IT Business Analyst')
    role_category = analysis.get('roleCategory', 'it_business_analyst')

    print(f"   Company: {company}")
    print(f"   Title: {title}")
    print(f"   Role: {role_category}")

    # Step 2: Generate CV
    print("\n2️⃣ Generating CV...")
    cv_latex = build_lego_cv(
        role_type=role_category,
        company=company,
        title=title,
        role_category=role_category,
        job_description=emerson_job_description
    )

    if cv_latex:
        cv_output = compile_latex_to_pdf(
            cv_latex,
            f"cv_itbusinessanalyst_emerson_harvad",
            output_dir
        )
        if cv_output:
            print(f"   ✅ CV saved to: {cv_output}")
        else:
            print("   ❌ CV compilation failed")
    else:
        print("   ❌ CV generation failed")

    # Step 3: Generate CL
    print("\n3️⃣ Generating Cover Letter...")
    cl_latex = build_lego_cover_letter(
        role_type=role_category,
        company=company,
        title=title,
        role_category=role_category,
        job_description=emerson_job_description
    )

    if cl_latex:
        cl_output = compile_latex_to_pdf(
            cl_latex,
            f"cl_itbusinessanalyst_emerson_harvad",
            output_dir
        )
        if cl_output:
            print(f"   ✅ CL saved to: {cl_output}")
        else:
            print("   ❌ CL compilation failed")
    else:
        print("   ❌ CL generation failed")

    # Summary
    print("\n" + "=" * 70)
    print("📊 GENERATION COMPLETE")
    print("=" * 70)
    print(f"   Output directory: {output_dir}")
    print(f"   Company: {company}")
    print(f"   Title: {title}")
    print("\n   Files generated:")
    print(f"   📄 cv_itbusinessanalyst_emerson_harvad.pdf")
    print(f"   📄 cl_itbusinessanalyst_emerson_harvad.pdf")
    print("\n   Please check the files on your Desktop!")

if __name__ == '__main__':
    generate_emerson_application()
