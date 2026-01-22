#!/usr/bin/env python3
"""
Compile Omnimodular AI Product Engineer application documents
"""

import subprocess
import sys
from pathlib import Path

def compile_latex(tex_file: Path) -> bool:
    """Compile LaTeX file to PDF"""
    print(f"\n📄 Compiling {tex_file.name}...")
    
    try:
        # Run pdflatex twice for proper references
        for i in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(tex_file.parent), str(tex_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"❌ Compilation failed on pass {i+1}")
                print(f"Error output:\n{result.stderr}")
                return False
        
        pdf_file = tex_file.with_suffix('.pdf')
        if pdf_file.exists():
            print(f"✅ Successfully created {pdf_file.name}")
            return True
        else:
            print(f"❌ PDF file not created: {pdf_file}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out")
        return False
    except FileNotFoundError:
        print("❌ pdflatex not found. Please install LaTeX distribution.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def cleanup_aux_files(directory: Path):
    """Remove auxiliary LaTeX files"""
    extensions = ['.aux', '.log', '.out', '.toc', '.synctex.gz']
    for ext in extensions:
        for file in directory.glob(f'*{ext}'):
            file.unlink()
            print(f"🧹 Cleaned up {file.name}")

def main():
    # Define paths
    app_dir = Path('job_applications/omnimodular_ai_product_engineer')
    cv_tex = app_dir / 'Omnimodular_AI_Product_Engineer_CV.tex'
    cl_tex = app_dir / 'Omnimodular_AI_Product_Engineer_CL.tex'
    
    # Check if files exist
    if not cv_tex.exists():
        print(f"❌ CV file not found: {cv_tex}")
        sys.exit(1)
    
    if not cl_tex.exists():
        print(f"❌ Cover letter file not found: {cl_tex}")
        sys.exit(1)
    
    print("🚀 Starting compilation for Omnimodular AI Product Engineer application")
    print("=" * 70)
    
    # Compile CV
    cv_success = compile_latex(cv_tex)
    
    # Compile Cover Letter
    cl_success = compile_latex(cl_tex)
    
    # Cleanup
    print("\n🧹 Cleaning up auxiliary files...")
    cleanup_aux_files(app_dir)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Compilation Summary:")
    print(f"  CV: {'✅ Success' if cv_success else '❌ Failed'}")
    print(f"  Cover Letter: {'✅ Success' if cl_success else '❌ Failed'}")
    
    if cv_success and cl_success:
        print("\n🎉 All documents compiled successfully!")
        print(f"\n📁 Output directory: {app_dir}")
        print(f"  - {cv_tex.with_suffix('.pdf').name}")
        print(f"  - {cl_tex.with_suffix('.pdf').name}")
        print("\n💡 You can now upload these files to Overleaf or use them directly!")
        return 0
    else:
        print("\n❌ Some documents failed to compile")
        return 1

if __name__ == '__main__':
    sys.exit(main())
