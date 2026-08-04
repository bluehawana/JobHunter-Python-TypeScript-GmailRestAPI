#!/usr/bin/env python3
"""
Generate sample CVs from updated Java and .NET templates
"""

import subprocess
import os
from datetime import datetime

def compile_latex(template_path, output_name):
    """Compile LaTeX template to PDF"""
    output_dir = f"sample_cvs_{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy template to output directory
    output_tex = f"{output_dir}/{output_name}.tex"
    subprocess.run(['cp', template_path, output_tex])
    
    # Compile to PDF
    print(f"🔨 Compiling {output_name}...")
    result = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, output_tex],
        capture_output=True,
        text=True
    )
    
    # Run twice for references
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, output_tex],
        capture_output=True
    )
    
    pdf_path = f"{output_dir}/{output_name}.pdf"
    if os.path.exists(pdf_path):
        print(f"✅ Generated: {pdf_path}")
        return pdf_path
    else:
        print(f"❌ Failed to generate {output_name}")
        return None

if __name__ == "__main__":
    print("=" * 80)
    print("Generating Sample Backend CVs with ECARX Experience")
    print("=" * 80)
    print()
    
    # Generate Java CV
    java_pdf = compile_latex(
        'templates/cv_templates/java_developer_template.tex',
        'cv_java_backend_developer_sample'
    )
    
    print()
    
    # Generate .NET CV
    dotnet_pdf = compile_latex(
        'templates/cv_templates/dotnet_developer_template.tex',
        'cv_dotnet_backend_developer_sample'
    )
    
    print()
    print("=" * 80)
    print("✅ Sample CVs Generated!")
    print("=" * 80)
    if java_pdf:
        print(f"📄 Java CV: {java_pdf}")
    if dotnet_pdf:
        print(f"📄 .NET CV: {dotnet_pdf}")
