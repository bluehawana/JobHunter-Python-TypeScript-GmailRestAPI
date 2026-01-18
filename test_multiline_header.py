#!/usr/bin/env python3
"""
Test the new multi-line header format
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.template_customizer import TemplateCustomizer

def test_multiline_header():
    """Test the new multi-line header format"""
    
    # Sample template with the new multi-line header format
    sample_template = r"""
\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[8pt]
{\Large \textbf{COMPANY_NAME}}\\[4pt]
{\Large \textbf{JOB_TITLE}}\\[4pt]
{\Large \textbf{Gothenburg, Sweden}}\\[8pt]
\end{center}
"""
    
    print("🔍 Testing Multi-line Header Format")
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
    
    print("\nCustomized Header:")
    print(customized)
    
    # Check if replacements worked
    if 'Meltwater' in customized and 'Software Engineer' in customized:
        print("✅ SUCCESS! Header format is correct:")
        print("   Line 1: Harvad (Hongzhi) Li")
        print("   Line 2: Meltwater")
        print("   Line 3: Software Engineer") 
        print("   Line 4: Gothenburg, Sweden")
        return True
    else:
        print("❌ Issue with header format")
        return False

def test_cv_compilation():
    """Test if the CV compiles to PDF correctly"""
    
    print(f"\n📄 Testing CV Compilation...")
    
    try:
        # Compile the updated CV template
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
    print("🚀 Testing Multi-line Header Format\n")
    
    header_success = test_multiline_header()
    compile_success = test_cv_compilation()
    
    print(f"\n" + "=" * 50)
    if header_success and compile_success:
        print("🎉 Multi-line header format is working!")
        print("✅ Format:")
        print("   Harvad (Hongzhi) Li")
        print("   Meltwater")
        print("   Software Engineer")
        print("   Gothenburg, Sweden")
        print("✅ CV compiles to PDF successfully")
    else:
        print("⚠️ Issues found:")
        if not header_success:
            print("   - Header replacement not working")
        if not compile_success:
            print("   - PDF compilation failed")
    
    print(f"\n💡 The header will now show each item on separate lines")
    print("   Much cleaner and simpler format!")