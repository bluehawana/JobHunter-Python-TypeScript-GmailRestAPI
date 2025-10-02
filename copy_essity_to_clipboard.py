#!/usr/bin/env python3
"""
Copy Essity LaTeX to clipboard for easy Overleaf pasting
"""
from pathlib import Path
import subprocess


def copy_to_clipboard(text):
    """Copy text to Windows clipboard"""
    try:
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"❌ Clipboard error: {e}")
        return False


def main():
    print("📋 Essity LaTeX → Clipboard → Overleaf")
    print("=" * 60)

    essity_folder = Path("job_applications/essity")
    cv_tex = essity_folder / "Essity_Cloud_DevOps_CV_20251002.tex"
    cl_tex = essity_folder / "Essity_Cloud_DevOps_CL_20251002.tex"

    print("\n1️⃣ CV - Ready to copy!")
    print(f"   File: {cv_tex.name}")
    input("   Press ENTER to copy CV to clipboard...")

    cv_content = cv_tex.read_text(encoding='utf-8')
    if copy_to_clipboard(cv_content):
        print("   ✅ CV copied to clipboard!")
        print("   📝 Now paste (Ctrl+V) into Overleaf")
        print("   🔄 Click 'Recompile' in Overleaf")
        print("   💾 Download PDF as: Essity_Cloud_DevOps_CV_HongzhiLi.pdf")

    print("\n2️⃣ Cover Letter - Ready to copy!")
    print(f"   File: {cl_tex.name}")
    input("   Press ENTER to copy Cover Letter to clipboard...")

    cl_content = cl_tex.read_text(encoding='utf-8')
    if copy_to_clipboard(cl_content):
        print("   ✅ Cover Letter copied to clipboard!")
        print("   📝 Now paste (Ctrl+V) into Overleaf")
        print("   🔄 Click 'Recompile' in Overleaf")
        print("   💾 Download PDF as: Essity_Cloud_DevOps_CL_HongzhiLi.pdf")

    print("\n" + "=" * 60)
    print("✅ Done! Both documents copied to clipboard")
    print("📂 Save PDFs to: job_applications/essity/")
    print("=" * 60)


if __name__ == '__main__':
    main()
