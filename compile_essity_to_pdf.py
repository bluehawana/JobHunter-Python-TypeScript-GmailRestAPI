#!/usr/bin/env python3
"""
Compile Essity LaTeX files to PDF using R2 + Overleaf
"""
from backend.r2_latex_storage import R2LaTeXStorage
import os
import sys
from pathlib import Path

sys.path.append('backend')

# Load environment variables


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


def upload_and_get_overleaf_urls():
    """Upload Essity LaTeX files to R2 and get Overleaf URLs"""

    print("🚀 Uploading Essity LaTeX files to R2 for Overleaf compilation...")
    print("=" * 60)

    # Initialize R2 storage
    r2 = R2LaTeXStorage()

    if not r2.client:
        print("❌ R2 client not available. Please check your .env file:")
        print("   - R2_ACCESS_KEY_ID")
        print("   - R2_SECRET_ACCESS_KEY")
        print("   - R2_ENDPOINT_URL")
        print("   - R2_PUBLIC_DOMAIN")
        return False

    # Read LaTeX files
    essity_folder = Path("job_applications/essity")
    cv_tex = essity_folder / "Essity_Cloud_DevOps_CV_20251002.tex"
    cl_tex = essity_folder / "Essity_Cloud_DevOps_CL_20251002.tex"

    if not cv_tex.exists() or not cl_tex.exists():
        print(f"❌ LaTeX files not found in {essity_folder}")
        return False

    # Job data for metadata
    job_data = {
        'company': 'Essity',
        'title': 'Cloud_DevOps_Engineer',
        'location': 'Munich_Germany'
    }

    # Upload CV
    print("\n📄 Uploading CV...")
    cv_content = cv_tex.read_text(encoding='utf-8')
    cv_result = r2.upload_latex_file(cv_content, job_data)

    if cv_result:
        print(f"✅ CV uploaded successfully!")
        print(f"   📁 Filename: {cv_result['filename']}")
        print(f"   🔗 Public URL: {cv_result['public_url']}")
        print(f"   🎯 Overleaf URL: {cv_result['overleaf_url']}")
    else:
        print("❌ CV upload failed")
        return False

    # Upload Cover Letter
    print("\n💌 Uploading Cover Letter...")
    cl_content = cl_tex.read_text(encoding='utf-8')
    job_data['title'] = 'Cloud_DevOps_CL'
    cl_result = r2.upload_latex_file(cl_content, job_data)

    if cl_result:
        print(f"✅ Cover Letter uploaded successfully!")
        print(f"   📁 Filename: {cl_result['filename']}")
        print(f"   🔗 Public URL: {cl_result['public_url']}")
        print(f"   🎯 Overleaf URL: {cl_result['overleaf_url']}")
    else:
        print("❌ Cover Letter upload failed")
        return False

    # Save URLs to file
    urls_file = essity_folder / "OVERLEAF_URLS.txt"
    urls_content = f"""Essity Cloud DevOps Application - Overleaf Compilation URLs
Generated: {Path().cwd()}

CV OVERLEAF URL:
{cv_result['overleaf_url']}

COVER LETTER OVERLEAF URL:
{cl_result['overleaf_url']}

INSTRUCTIONS:
1. Click on each URL above (Ctrl+Click in most editors)
2. Overleaf will open with the LaTeX file loaded
3. Click "Recompile" button in Overleaf
4. Download the PDF using "Download PDF" button
5. Save as:
   - Essity_Cloud_DevOps_CV_HongzhiLi.pdf
   - Essity_Cloud_DevOps_CL_HongzhiLi.pdf

DIRECT LATEX URLS (if needed):
CV: {cv_result['public_url']}
CL: {cl_result['public_url']}
"""

    urls_file.write_text(urls_content, encoding='utf-8')
    print(f"\n📝 URLs saved to: {urls_file}")

    # Summary
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Your Essity application is ready for compilation!")
    print("=" * 60)
    print("\n📋 NEXT STEPS:")
    print("1. Open the URLs below in your browser")
    print("2. Overleaf will load and compile the LaTeX automatically")
    print("3. Download the PDFs from Overleaf")
    print("\n🔗 OVERLEAF URLS:")
    print(f"\n📄 CV:")
    print(f"   {cv_result['overleaf_url']}")
    print(f"\n💌 Cover Letter:")
    print(f"   {cl_result['overleaf_url']}")
    print("\n💡 TIP: Ctrl+Click the URLs to open them directly!")

    return True


if __name__ == '__main__':
    success = upload_and_get_overleaf_urls()
    sys.exit(0 if success else 1)
