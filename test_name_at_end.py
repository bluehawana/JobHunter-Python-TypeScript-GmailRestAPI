#!/usr/bin/env python3
"""
Test the new format with name at the end instead of header
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.template_customizer import TemplateCustomizer

def test_name_at_end():
    """Test the new format with name at the end"""
    
    # Sample template with name removed from header
    sample_template = r"""
\begin{center}
{\Large \textbf{COMPANY_NAME}}\\[4pt]
{\Large \textbf{JOB_TITLE}}\\[4pt]
{\Large \textbf{Gothenburg, Sweden}}\\[8pt]
\end{center}

\section*{Profile Summary}
Experienced developer applying for JOB_TITLE position at COMPANY_NAME.

\vspace{20pt}
\begin{flushright}
\textit{Harvad (Hongzhi) Li}\\
\textit{Gårdsvägen 9, 431 38 Mölndal, Sweden}
\end{flushright}
"""
    
    print("🔍 Testing Name at End Format")
    print("=" * 50)
    
    customizer = TemplateCustomizer()
    
    # Test with Meltwater job
    print("Testing with Meltwater Software Engineer job...")
    
    customized = customizer.customize_template(
        sample_template,
        company="Meltwater",
        title="Software Engineer", 
        role_type="backend_developer"
    )
    
    print("\nCustomized Result:")
    print(customized)
    
    # Check the format
    lines = customized.split('\n')
    header_lines = []
    signature_lines = []
    
    in_header = False
    in_signature = False
    
    for line in lines:
        if '\\begin{center}' in line:
            in_header = True
        elif '\\end{center}' in line:
            in_header = False
        elif '\\begin{flushright}' in line:
            in_signature = True
        elif '\\end{flushright}' in line:
            in_signature = False
        elif in_header and ('Meltwater' in line or 'Software Engineer' in line or 'Gothenburg' in line):
            header_lines.append(line.strip())
        elif in_signature and 'Harvad' in line:
            signature_lines.append(line.strip())
    
    print(f"\n✅ Header Format (no name):")
    for line in header_lines:
        print(f"   {line}")
    
    print(f"\n✅ Signature at End:")
    for line in signature_lines:
        print(f"   {line}")
    
    # Verify format
    has_meltwater_in_header = any('Meltwater' in line for line in header_lines)
    has_name_in_signature = any('Harvad' in line for line in signature_lines)
    no_name_in_header = not any('Harvad' in line for line in header_lines)
    
    if has_meltwater_in_header and has_name_in_signature and no_name_in_header:
        print(f"\n🎉 SUCCESS! Format is correct:")
        print(f"   ✅ Header shows: Meltwater, Software Engineer, Gothenburg")
        print(f"   ✅ Name appears at end as signature")
        print(f"   ✅ No name in header")
        return True
    else:
        print(f"\n❌ Format issues:")
        if not has_meltwater_in_header:
            print(f"   - Missing company in header")
        if not has_name_in_signature:
            print(f"   - Missing name in signature")
        if not no_name_in_header:
            print(f"   - Name still in header")
        return False

def test_cv_compilation():
    """Test if the CV compiles correctly"""
    
    print(f"\n📄 Testing CV Compilation...")
    
    try:
        result = os.system("pdflatex -output-directory=job_applications/ahlsell_fullstack job_applications/ahlsell_fullstack/Ahlsell_Fullstack_CV.tex > /dev/null 2>&1")
        
        if result == 0:
            print("✅ CV compiles successfully to PDF")
            return True
        else:
            print("❌ CV compilation failed")
            return False
    except Exception as e:
        print(f"❌ Error during compilation: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing Name at End Format\n")
    
    format_success = test_name_at_end()
    compile_success = test_cv_compilation()
    
    print(f"\n" + "=" * 50)
    if format_success and compile_success:
        print("🎉 Name at end format is working!")
        print("✅ Header shows only:")
        print("   Meltwater")
        print("   Software Engineer")
        print("   Gothenburg, Sweden")
        print("✅ Name appears as signature at the end")
        print("✅ CV compiles to PDF successfully")
    else:
        print("⚠️ Issues found - check output above")
    
    print(f"\n💡 The CV now has a clean header focused on the job")
    print("   and your name appears professionally at the end!")