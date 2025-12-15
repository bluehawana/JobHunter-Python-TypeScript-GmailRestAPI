#!/usr/bin/env python3
"""
Compile Cleaning Robot Chinese Cover Letter to PDF
"""

import subprocess
import tempfile
import os
from pathlib import Path

def compile_chinese_cl():
    """Compile Chinese Cover Letter using xelatex"""
    
    print("🤖 Compiling Cleaning Robot Chinese Cover Letter")
    print("=" * 70)
    
    # Read LaTeX file
    tex_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CL_CN.tex")
    
    if not tex_file.exists():
        print(f"❌ Error: {tex_file} not found")
        return False
    
    latex_content = tex_file.read_text(encoding='utf-8')
    print(f"✅ Read LaTeX file: {tex_file}")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write LaTeX to temp file
            temp_tex = os.path.join(temp_dir, "cl.tex")
            with open(temp_tex, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"\n🔨 Compiling with xelatex...")
            
            # Compile twice for references
            for i in range(2):
                result = subprocess.run(
                    ['xelatex', '-interaction=nonstopmode', 
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
            temp_pdf = os.path.join(temp_dir, "cl.pdf")
            
            if os.path.exists(temp_pdf):
                # Copy PDF to output location
                output_pdf = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CL_CN.pdf")
                
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
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during compilation: {e}")
        return False

if __name__ == '__main__':
    import sys
    success = compile_chinese_cl()
    sys.exit(0 if success else 1)
