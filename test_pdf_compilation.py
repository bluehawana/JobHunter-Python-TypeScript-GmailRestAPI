#!/usr/bin/env python3
"""
Test PDF compilation to ensure LaTeX works correctly
"""

import subprocess
import os
import tempfile
from pathlib import Path

def test_latex_compilation():
    """Test that LaTeX compilation works"""
    print("📄 Testing LaTeX PDF compilation...")
    
    # Simple test LaTeX document
    test_latex = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=1in}
\definecolor{lightblue}{RGB}{0, 119, 181}

\begin{document}

{\color{lightblue}\textbf{Test Company}\\
Test Position\\
Gothenburg, Sweden}

\vspace{1cm}

Dear Hiring Manager,

This is a test document to verify LaTeX compilation works correctly.

\vspace{1cm}

Best Regards,\\
Harvad (Hongzhi) Li

\end{document}
"""
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / 'test.tex'
        pdf_file = temp_path / 'test.pdf'
        
        # Write test LaTeX file
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(test_latex)
        
        # Try to compile
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(tex_file)],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            if result.returncode == 0 and pdf_file.exists():
                print("✅ LaTeX compilation successful")
                print(f"✅ PDF generated: {pdf_file.stat().st_size} bytes")
                return True
            else:
                print("❌ LaTeX compilation failed")
                print(f"Return code: {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ LaTeX compilation timed out")
            return False
        except FileNotFoundError:
            print("❌ pdflatex not found - LaTeX not installed")
            return False

def test_template_compilation():
    """Test compilation of actual templates"""
    print("\n📋 Testing actual template compilation...")
    
    templates_to_test = [
        'backend/latex_sources/cover_letter_hongzhi_li_template.tex',
        'templates/cl_template_overleaf.tex'
    ]
    
    success_count = 0
    
    for template_path in templates_to_test:
        if not os.path.exists(template_path):
            print(f"⚠️ Template not found: {template_path}")
            continue
            
        print(f"Testing: {template_path}")
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace placeholders
        test_content = template_content.replace('COMPANY_NAME_PLACEHOLDER', 'Test Company')
        test_content = test_content.replace('JOB_TITLE_PLACEHOLDER', 'Test Position')
        test_content = test_content.replace('[COMPANY NAME]', 'Test Company')
        test_content = test_content.replace('[JOB TITLE]', 'Test Position')
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / 'template_test.tex'
            pdf_file = temp_path / 'template_test.pdf'
            
            # Write test file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Try to compile
            try:
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(tex_file)],
                    capture_output=True,
                    timeout=30,
                    text=True
                )
                
                if result.returncode == 0 and pdf_file.exists():
                    print(f"✅ {template_path} compiled successfully")
                    success_count += 1
                else:
                    print(f"❌ {template_path} compilation failed")
                    print(f"STDERR: {result.stderr[:500]}...")
                    
            except subprocess.TimeoutExpired:
                print(f"❌ {template_path} compilation timed out")
            except FileNotFoundError:
                print("❌ pdflatex not found")
                break
    
    return success_count

def main():
    """Run PDF compilation tests"""
    print("🚀 Starting PDF compilation tests...")
    
    # Test basic LaTeX compilation
    basic_test = test_latex_compilation()
    
    # Test template compilation
    template_success = test_template_compilation()
    
    print(f"\n📊 COMPILATION TEST RESULTS:")
    print(f"✅ Basic LaTeX: {'PASSED' if basic_test else 'FAILED'}")
    print(f"✅ Template compilation: {template_success} templates compiled successfully")
    
    if basic_test and template_success > 0:
        print("🎉 PDF COMPILATION TESTS PASSED!")
        return True
    else:
        print("⚠️ Some compilation tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)