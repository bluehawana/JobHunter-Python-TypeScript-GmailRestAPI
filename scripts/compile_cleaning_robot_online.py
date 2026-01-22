#!/usr/bin/env python3
"""
Compile Cleaning Robot Chinese CV using online LaTeX service
"""

import requests
from pathlib import Path
import subprocess

def compile_chinese_cv_online():
    """Compile Chinese CV using online LaTeX API"""
    
    print("🤖 Compiling Cleaning Robot Chinese CV (Online)")
    print("=" * 70)
    
    # Read LaTeX file
    tex_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.tex")
    
    if not tex_file.exists():
        print(f"❌ Error: {tex_file} not found")
        return False
    
    latex_content = tex_file.read_text(encoding='utf-8')
    print(f"✅ Read LaTeX file: {tex_file}")
    print(f"   Size: {len(latex_content)} characters")
    
    # Use LaTeX.Online API
    try:
        url = "https://latex.api.aa.net.uk/latex/pdf"
        
        data = {
            'tex': latex_content
        }
        
        print(f"\n🔄 Sending to online LaTeX compiler...")
        print(f"   API: {url}")
        
        response = requests.post(url, data=data, timeout=60)
        
        if response.status_code == 200:
            # Save PDF
            output_pdf = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.pdf")
            output_pdf.write_bytes(response.content)
            
            print(f"\n✅ PDF compiled successfully!")
            print(f"   Output: {output_pdf}")
            print(f"   Size: {len(response.content) / 1024:.1f} KB")
            
            # Open PDF
            subprocess.run(['open', str(output_pdf)])
            print(f"📄 Opening PDF in default viewer...")
            
            return True
        else:
            print(f"\n❌ Compilation failed (HTTP {response.status_code})")
            print(f"   Response: {response.text[:500]}")
            
            # Fallback to Overleaf
            print(f"\n💡 Trying Overleaf instead...")
            subprocess.run(['python3', 'open_cleaning_robot_cv_in_overleaf.py'])
            
            return False
            
    except requests.Timeout:
        print(f"\n❌ Request timed out (LaTeX compilation took too long)")
        print(f"\n💡 Trying Overleaf instead...")
        subprocess.run(['python3', 'open_cleaning_robot_cv_in_overleaf.py'])
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Trying Overleaf instead...")
        subprocess.run(['python3', 'open_cleaning_robot_cv_in_overleaf.py'])
        return False

if __name__ == '__main__':
    import sys
    success = compile_chinese_cv_online()
    sys.exit(0 if success else 1)
