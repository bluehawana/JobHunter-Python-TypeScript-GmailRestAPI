#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append('backend')

from app.lego_api import analyze_job_description, build_lego_cv, build_lego_cover_letter

# Emerson job description
job_description = """
IT Business Analyst
Emerson
Gothenburg, Sweden

We are looking for an IT Business Analyst to join our team. The role involves bridging the gap between IT and business requirements, analyzing business processes, and implementing technology solutions that drive operational efficiency.

Key responsibilities:
- Analyze business requirements and translate them into technical specifications
- Work with stakeholders to understand business needs and processes
- Design and implement business intelligence solutions
- Support ERP system implementations and optimizations
- Lead process improvement initiatives
- Collaborate with cross-functional teams
- Create documentation and training materials

Requirements:
- Bachelor's degree in Business, IT, or related field
- Experience with business analysis and process improvement
- Knowledge of ERP systems and business intelligence tools
- Strong analytical and communication skills
- Project management experience
- Ability to work with diverse stakeholders
"""

print("🔍 Generating Emerson IT Business Analyst Application")
print("=" * 60)

# Step 1: Analyze job
print("\n1️⃣ Analyzing job...")
analysis = analyze_job_description(job_description)
print(f"✓ Role detected: {analysis.get('roleCategory', 'Unknown')}")

# Step 2: Generate CV
print("\n2️⃣ Generating CV...")
cv_content = build_lego_cv(
    role_type="IT Business Analyst",
    company="Emerson",
    title="IT Business Analyst",
    role_category="it_business_analyst",
    job_description=job_description
)

# Save CV
with open('Emerson_IT_Business_Analyst_CV.tex', 'w', encoding='utf-8') as f:
    f.write(cv_content)
print("✓ CV saved: Emerson_IT_Business_Analyst_CV.tex")

# Step 3: Generate Cover Letter
print("\n3️⃣ Generating Cover Letter...")
cl_content = build_lego_cover_letter(
    role_type="IT Business Analyst",
    company="Emerson",
    title="IT Business Analyst",
    role_category="it_business_analyst",
    job_description=job_description
)

# Save CL
with open('Emerson_IT_Business_Analyst_CL.tex', 'w', encoding='utf-8') as f:
    f.write(cl_content)
print("✓ CL saved: Emerson_IT_Business_Analyst_CL.tex")

print("\n4️⃣ Compiling PDFs...")
import subprocess

# Compile CV
try:
    subprocess.run(['pdflatex', 'Emerson_IT_Business_Analyst_CV.tex'], 
                   capture_output=True, check=True)
    print("✓ CV PDF compiled: Emerson_IT_Business_Analyst_CV.pdf")
except:
    print("⚠️ CV PDF compilation failed")

# Compile CL
try:
    subprocess.run(['pdflatex', 'Emerson_IT_Business_Analyst_CL.tex'], 
                   capture_output=True, check=True)
    print("✓ CL PDF compiled: Emerson_IT_Business_Analyst_CL.pdf")
except:
    print("⚠️ CL PDF compilation failed")

print("\n🎉 Emerson application ready!")
print("📄 Files generated:")
print("   • Emerson_IT_Business_Analyst_CV.pdf")
print("   • Emerson_IT_Business_Analyst_CL.pdf")
print("   • Emerson_IT_Business_Analyst_CV.tex")
print("   • Emerson_IT_Business_Analyst_CL.tex")