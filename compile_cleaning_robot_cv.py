#!/usr/bin/env python3
"""
Compile Cleaning Robot Chinese CV to PDF
Uses local pdflatex (same method as other resumes)
"""

import subprocess
import tempfile
import os
from pathlib import Path

def compile_chinese_cv():
    """Compile Chinese CV using pdflatex"""
    
    print("🤖 Compiling Cleaning Robot Chinese CV")
    print("=" * 70)
    
    # Read LaTeX file
    tex_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.tex")
    
    if not tex_file.exists():
        print(f"❌ Error: {tex_file} not found")
        return False
    
    latex_content = tex_file.read_text(encoding='utf-8')
    print(f"✅ Read LaTeX file: {tex_file}")
    
    # Check if xelatex is available (better for Chinese)
    try:
        result = subprocess.run(['which', 'xelatex'], capture_output=True, text=True)
        has_xelatex = result.returncode == 0
    except:
        has_xelatex = False
    
    # Check if pdflatex is available
    try:
        result = subprocess.run(['which', 'pdflatex'], capture_output=True, text=True)
        has_pdflatex = result.returncode == 0
    except:
        has_pdflatex = False
    
    if not has_xelatex and not has_pdflatex:
        print("\n❌ Neither xelatex nor pdflatex found on system")
        print("\n📝 Please install LaTeX:")
        print("   brew install --cask mactex")
        print("\n   Or use Overleaf:")
        print("   python3 open_cleaning_robot_cv_in_overleaf.py")
        return False
    
    compiler = 'xelatex' if has_xelatex else 'pdflatex'
    print(f"✅ Using {compiler} for compilation")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write LaTeX to temp file
            temp_tex = os.path.join(temp_dir, "cv.tex")
            with open(temp_tex, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"\n🔨 Compiling with {compiler}...")
            
            # Compile twice for references
            for i in range(2):
                result = subprocess.run(
                    [compiler, '-interaction=nonstopmode', 
                     '-output-directory', temp_dir, temp_tex],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if i == 0:
                    print(f"   Pass 1/2...")
                else:
                    print(f"   Pass 2/2...")
            
            # Check if PDF was created
            temp_pdf = os.path.join(temp_dir, "cv.pdf")
            
            if os.path.exists(temp_pdf):
                # Copy PDF to output location
                output_pdf = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.pdf")
                
                with open(temp_pdf, 'rb') as f:
                    pdf_content = f.read()
                
                output_pdf.write_bytes(pdf_content)
                
                print(f"\n✅ PDF compiled successfully!")
                print(f"   Output: {output_pdf}")
                print(f"   Size: {len(pdf_content) / 1024:.1f} KB")
                
                # Open PDF
                subprocess.run(['open', str(output_pdf)])
                print(f"📄 Opening PDF in default viewer...")
                
                return True
            else:
                print(f"\n❌ PDF compilation failed")
                print(f"\nCompiler output:")
                print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)
                print(f"\nCompiler errors:")
                print(result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during compilation: {e}")
        return False

if __name__ == '__main__':
    import sys
    success = compile_chinese_cv()
    sys.exit(0 if success else 1)
