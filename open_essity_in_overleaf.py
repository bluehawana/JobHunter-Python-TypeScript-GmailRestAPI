#!/usr/bin/env python3
"""
Open Essity LaTeX files in Overleaf for PDF compilation
Simple solution without R2 - just copy/paste into Overleaf
"""
from pathlib import Path
import webbrowser


def open_in_overleaf():
    """Generate instructions for Overleaf compilation"""

    print("🚀 Essity Application - Overleaf Compilation Guide")
    print("=" * 60)

    essity_folder = Path("job_applications/essity")
    cv_tex = essity_folder / "Essity_Cloud_DevOps_CV_20251002.tex"
    cl_tex = essity_folder / "Essity_Cloud_DevOps_CL_20251002.tex"

    if not cv_tex.exists() or not cl_tex.exists():
        print(f"❌ LaTeX files not found in {essity_folder}")
        return False

    print("\n📋 STEP-BY-STEP INSTRUCTIONS:")
    print("\n1️⃣ OPEN OVERLEAF:")
    print("   Go to: https://www.overleaf.com")
    print("   (Opening in browser now...)")

    # Open Overleaf
    webbrowser.open("https://www.overleaf.com/project")

    print("\n2️⃣ CREATE NEW PROJECT:")
    print("   • Click 'New Project' → 'Blank Project'")
    print("   • Name it: 'Essity_Cloud_DevOps_Application'")

    print("\n3️⃣ COMPILE CV:")
    print("   • Delete the default content in main.tex")
    print(f"   • Open: {cv_tex.absolute()}")
    print("   • Copy ALL content from the file")
    print("   • Paste into Overleaf's main.tex")
    print("   • Click 'Recompile' button")
    print("   • Download PDF as: Essity_Cloud_DevOps_CV_HongzhiLi.pdf")

    print("\n4️⃣ COMPILE COVER LETTER:")
    print("   • Create new project or clear main.tex")
    print(f"   • Open: {cl_tex.absolute()}")
    print("   • Copy ALL content from the file")
    print("   • Paste into Overleaf's main.tex")
    print("   • Click 'Recompile' button")
    print("   • Download PDF as: Essity_Cloud_DevOps_CL_HongzhiLi.pdf")

    print("\n5️⃣ SAVE PDFs:")
    print(f"   • Save both PDFs to: {essity_folder.absolute()}")

    # Create a quick reference file
    ref_file = essity_folder / "OVERLEAF_INSTRUCTIONS.txt"
    instructions = f"""ESSITY APPLICATION - OVERLEAF COMPILATION

📁 LaTeX Files Location:
{cv_tex.absolute()}
{cl_tex.absolute()}

🌐 Overleaf: https://www.overleaf.com/project

📋 QUICK STEPS:
1. Go to Overleaf.com
2. Create new blank project
3. Copy content from CV .tex file → Paste in Overleaf
4. Click Recompile → Download PDF
5. Repeat for Cover Letter
6. Save PDFs in: {essity_folder.absolute()}

✅ FINAL FILES NEEDED:
- Essity_Cloud_DevOps_CV_HongzhiLi.pdf
- Essity_Cloud_DevOps_CL_HongzhiLi.pdf

💡 TIP: You can also upload the .tex files directly to Overleaf:
   Project → Upload → Select .tex file
"""

    ref_file.write_text(instructions, encoding='utf-8')
    print(f"\n📝 Instructions saved to: {ref_file}")

    print("\n" + "=" * 60)
    print("✅ Overleaf should be opening in your browser now!")
    print("📄 Follow the steps above to compile your PDFs")
    print("=" * 60)

    # Show file paths for easy access
    print("\n📂 FILE PATHS (for copy/paste):")
    print(f"\nCV LaTeX:")
    print(f"{cv_tex.absolute()}")
    print(f"\nCover Letter LaTeX:")
    print(f"{cl_tex.absolute()}")

    return True


if __name__ == '__main__':
    open_in_overleaf()
