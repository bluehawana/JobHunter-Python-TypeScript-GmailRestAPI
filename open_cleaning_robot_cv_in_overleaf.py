#!/usr/bin/env python3
"""
Open Cleaning Robot CV in Overleaf for compilation
"""

import webbrowser
from pathlib import Path

def open_in_overleaf():
    """Open Overleaf and provide instructions"""
    
    tex_file = Path("job_applications/cleaning_robot/Cleaning_Robot_Senior_Support_Engineer_CV_CN.tex")
    output_folder = tex_file.parent
    
    print("🤖 Cleaning Robot Senior Support Engineer - Chinese CV")
    print("=" * 70)
    print("\n📄 LaTeX Source File:")
    print(f"   {tex_file.absolute()}")
    print("\n📁 Output Folder:")
    print(f"   {output_folder.absolute()}")
    
    print("\n" + "=" * 70)
    print("📝 OVERLEAF COMPILATION INSTRUCTIONS")
    print("=" * 70)
    print("\n1. Opening Overleaf now...")
    print("2. Create new blank project (or use existing)")
    print(f"3. Copy content from: {tex_file.name}")
    print("4. Paste into Overleaf main.tex")
    print("5. Click 'Recompile' button")
    print("6. Download PDF")
    print("7. Save as: Cleaning_Robot_Senior_Support_Engineer_CV_CN.pdf")
    print(f"8. Save in folder: {output_folder.absolute()}")
    
    print("\n" + "=" * 70)
    print("💡 IMPORTANT NOTES:")
    print("=" * 70)
    print("• This is a CHINESE resume (简体中文)")
    print("• Photo placeholder is in top-left corner (3cm x 3.5cm)")
    print("• Resume is designed for 2 pages maximum")
    print("• Highlights: H3C (2024.5-now), Senior Matrial (SRE), Ecarx (IT Support)")
    print("• Languages: Chinese (native), English (fluent), Swedish (fluent)")
    
    print("\n" + "=" * 70)
    
    # Open Overleaf
    webbrowser.open('https://www.overleaf.com/project')
    
    print("\n✅ Overleaf should be opening in your browser now!")
    print("📄 Follow the steps above to compile your PDF")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    open_in_overleaf()
