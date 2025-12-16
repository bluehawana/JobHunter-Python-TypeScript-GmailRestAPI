#!/usr/bin/env python3
"""
Create Chinese CV for Cleaning Robot Senior Support Engineer position
Uses Overleaf for PDF compilation
"""

import sys
from pathlib import Path
from backend.r2_latex_storage import R2LaTeXStorage
from backend.overleaf_pdf_generator import OverleafPDFGenerator

def create_cleaning_robot_cv():
    """Create and compile Chinese CV for cleaning robot position"""
    
    print("🤖 Creating Chinese CV for Cleaning Robot Senior Support Engineer")
    print("=" * 70)
    
    # Read the LaTeX file
    tex_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.tex")
    
    if not tex_file.exists():
        print(f"❌ Error: {tex_file} not found")
        return False
    
    latex_content = tex_file.read_text(encoding='utf-8')
    print(f"✅ Read LaTeX file: {tex_file}")
    
    # Initialize generators
    r2_storage = R2LaTeXStorage()
    overleaf_gen = OverleafPDFGenerator()
    
    # Upload to R2
    print("\n📤 Uploading to R2...")
    r2_url = r2_storage.upload_latex(
        latex_content,
        "cleaning_robot_cv_cn.tex"
    )
    
    if r2_url:
        print(f"✅ Uploaded to R2: {r2_url}")
    else:
        print("⚠️ R2 upload failed, continuing with Overleaf...")
    
    # Generate PDF via Overleaf
    print("\n🔨 Compiling PDF via Overleaf...")
    pdf_bytes = overleaf_gen.generate_pdf(latex_content)
    
    if pdf_bytes and len(pdf_bytes) > 10000:
        # Save PDF
        pdf_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.pdf")
        pdf_file.write_bytes(pdf_bytes)
        print(f"✅ PDF saved: {pdf_file}")
        print(f"   Size: {len(pdf_bytes) / 1024:.1f} KB")
        
        # Open PDF
        import subprocess
        subprocess.run(['open', str(pdf_file)])
        print(f"📄 Opening PDF in default viewer...")
        
        return True
    else:
        print("❌ PDF compilation failed")
        print("\n📝 Manual Overleaf Instructions:")
        print("1. Go to https://www.overleaf.com/project")
        print("2. Create new blank project")
        print(f"3. Copy content from: {tex_file}")
        print("4. Paste in Overleaf main.tex")
        print("5. Click 'Recompile' → Download PDF")
        print(f"6. Save as: Cleaning_Robot_Senior_Support_Engineer_CV_CN.pdf")
        
        return False

if __name__ == '__main__':
    success = create_cleaning_robot_cv()
    sys.exit(0 if success else 1)
