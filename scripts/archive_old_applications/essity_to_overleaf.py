#!/usr/bin/env python3
"""
Quick Essity → Overleaf workflow (same as you did for Opera)
"""
from pathlib import Path
import webbrowser


def main():
    print("🚀 Essity Application → Overleaf (Quick Workflow)")
    print("=" * 60)

    essity_folder = Path("job_applications/essity")
    cv_tex = essity_folder / "Essity_Cloud_DevOps_CV_20251002.tex"
    cl_tex = essity_folder / "Essity_Cloud_DevOps_CL_20251002.tex"

    print("\n✅ LaTeX files ready:")
    print(f"   📄 CV: {cv_tex.name}")
    print(f"   💌 CL: {cl_tex.name}")

    print("\n📋 QUICK STEPS (same as Opera):")
    print("   1. Opening Overleaf now...")
    print("   2. Upload both .tex files to Overleaf")
    print("   3. Compile → Download PDFs")
    print("   4. Save as:")
    print("      • Essity_Cloud_DevOps_CV_HongzhiLi.pdf")
    print("      • Essity_Cloud_DevOps_CL_HongzhiLi.pdf")

    # Open Overleaf
    webbrowser.open("https://www.overleaf.com/project")

    print("\n📂 Files location:")
    print(f"   {essity_folder.absolute()}")

    print("\n" + "=" * 60)
    print("✅ Overleaf opened! Upload the .tex files and compile")
    print("=" * 60)


if __name__ == '__main__':
    main()
