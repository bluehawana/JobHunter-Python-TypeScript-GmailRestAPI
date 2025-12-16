#!/usr/bin/env python3
"""
Compile Essity LaTeX files to PDF using pdflatex (same as Opera method)
"""
from backend.overleaf_pdf_generator import OverleafPDFGenerator
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append('backend')

# Load environment


def load_env():
    env = Path('.env')
    if env.exists():
        for raw in env.read_text(encoding='utf-8').splitlines():
            s = raw.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            k, v = s.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


load_env()


def compile_essity_pdfs():
    """Compile Essity LaTeX files to PDF"""

    print("🚀 Compiling Essity LaTeX files to PDF...")
    print("=" * 60)

    essity_folder = Path("job_applications/essity")
    cv_tex_path = essity_folder / "Essity_Cloud_DevOps_CV_20251002.tex"
    cl_tex_path = essity_folder / "Essity_Cloud_DevOps_CL_20251002.tex"

    if not cv_tex_path.exists() or not cl_tex_path.exists():
        print(f"❌ LaTeX files not found in {essity_folder}")
        return False

    # Read LaTeX content
    cv_latex = cv_tex_path.read_text(encoding='utf-8')
    cl_latex = cl_tex_path.read_text(encoding='utf-8')

    # Initialize PDF generator (same as Opera)
    generator = OverleafPDFGenerator()

    # Compile CV
    print("\n📄 Compiling CV...")
    cv_pdf_bytes = generator._compile_latex_locally(cv_latex)

    if cv_pdf_bytes:
        cv_pdf_path = essity_folder / "Essity_Cloud_DevOps_CV_HongzhiLi.pdf"
        cv_pdf_path.write_bytes(cv_pdf_bytes)
        size_kb = len(cv_pdf_bytes) / 1024
        print(f"✅ CV PDF created: {cv_pdf_path.name} ({size_kb:.1f} KB)")
    else:
        print("❌ CV PDF compilation failed")
        return False

    # Compile Cover Letter
    print("\n💌 Compiling Cover Letter...")
    cl_pdf_bytes = generator._compile_latex_locally(cl_latex)

    if cl_pdf_bytes:
        cl_pdf_path = essity_folder / "Essity_Cloud_DevOps_CL_HongzhiLi.pdf"
        cl_pdf_path.write_bytes(cl_pdf_bytes)
        size_kb = len(cl_pdf_bytes) / 1024
        print(
            f"✅ Cover Letter PDF created: {cl_pdf_path.name} ({size_kb:.1f} KB)")
    else:
        print("❌ Cover Letter PDF compilation failed")
        return False

    # Summary
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Essity PDFs compiled!")
    print("=" * 60)
    print(f"\n📂 Location: {essity_folder.absolute()}")
    print(f"\n📄 Files created:")
    print(f"   • {cv_pdf_path.name}")
    print(f"   • {cl_pdf_path.name}")
    print("\n✅ Ready to submit to Essity!")

    return True


if __name__ == '__main__':
    success = compile_essity_pdfs()
    sys.exit(0 if success else 1)
