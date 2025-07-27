#!/usr/bin/env python3
"""
Manual PDF Generation Guide and Summary
"""

import os
from pathlib import Path

def create_compilation_guide():
    """Create a detailed guide for manual PDF compilation"""
    
    print("📄 LaTeX to PDF Compilation Guide")
    print("=" * 60)
    
    # Check what we have
    latex_dir = Path("latex_sources")
    if latex_dir.exists():
        tex_files = list(latex_dir.glob("*.tex"))
        print(f"✅ Found {len(tex_files)} LaTeX files ready for compilation")
    else:
        print("❌ latex_sources directory not found!")
        return
    
    print("\n🔧 COMPILATION OPTIONS:")
    print()
    
    print("1. 📱 OVERLEAF (Recommended - Free & Easy):")
    print("   • Go to: https://www.overleaf.com/")
    print("   • Create free account")
    print("   • Click 'New Project' > 'Upload Project'")
    print("   • Upload all .tex files from latex_sources/")
    print("   • Click on each file and press 'Recompile'")
    print("   • Download PDFs using 'Download PDF' button")
    print()
    
    print("2. 💻 LOCAL INSTALLATION (macOS):")
    print("   • Install: brew install --cask basictex")
    print("   • Restart terminal or run: eval \"$(/usr/libexec/path_helper)\"")
    print("   • Update packages: sudo tlmgr update --self && sudo tlmgr install moderncv")
    print("   • Compile: cd latex_sources && pdflatex filename.tex")
    print()
    
    print("3. 🌐 ONLINE COMPILERS:")
    print("   • https://latexbase.com/ (Simple upload & compile)")
    print("   • https://www.sharelatex.com/")
    print("   • https://papeeria.com/")
    print()
    
    print("4. 🔄 BATCH COMPILATION SCRIPT:")
    compilation_script = """#!/bin/bash
# Save this as compile_pdfs.sh and run: chmod +x compile_pdfs.sh && ./compile_pdfs.sh

echo "🔄 Compiling LaTeX files to PDF..."
cd latex_sources

for file in *.tex; do
    echo "📄 Compiling: $file"
    pdflatex -interaction=nonstopmode "$file"
    if [ $? -eq 0 ]; then
        echo "✅ Success: ${file%.tex}.pdf"
    else
        echo "❌ Failed: $file"
    fi
done

# Clean up auxiliary files
rm -f *.aux *.log *.out

echo "🎯 Compilation complete! Check for .pdf files"
"""
    
    with open("compile_pdfs.sh", 'w') as f:
        f.write(compilation_script)
    
    os.chmod("compile_pdfs.sh", 0o755)
    print("   ✅ Created: compile_pdfs.sh (run after installing LaTeX)")
    print()
    
    # Show priority files
    priority_jobs = []
    for tex_file in tex_files:
        if any(company in tex_file.name.lower() for company in ['volvo', 'polestar', 'skf', 'hasselblad', 'stena', 'cevt']):
            priority_jobs.append(tex_file.name)
    
    print("🎯 PRIORITY FILES (Gothenburg Companies):")
    for i, job_file in enumerate(sorted(priority_jobs), 1):
        print(f"   {i:2}. {job_file}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   📄 Total LaTeX files: {len(tex_files)}")
    print(f"   🏢 Gothenburg priority: {len(priority_jobs)}")
    print(f"   📁 Location: latex_sources/")
    
    print(f"\n🚀 RECOMMENDED WORKFLOW:")
    print(f"   1. Go to Overleaf.com (easiest option)")
    print(f"   2. Upload 3-5 priority files first")
    print(f"   3. Compile to PDF and download")
    print(f"   4. Repeat for remaining files")
    
    # Create a prioritized file list
    create_priority_list(tex_files)

def create_priority_list(tex_files):
    """Create a prioritized list of files to compile"""
    
    print(f"\n📋 COMPILATION PRIORITY ORDER:")
    print("=" * 40)
    
    # Categorize files
    gothenburg_cv = []
    gothenburg_cover = []
    high_match_cv = []
    high_match_cover = []
    
    for tex_file in tex_files:
        name = tex_file.name.lower()
        
        # Gothenburg companies
        if any(company in name for company in ['volvo', 'polestar', 'skf', 'hasselblad', 'stena', 'cevt']):
            if 'cv_' in name:
                gothenburg_cv.append(tex_file.name)
            else:
                gothenburg_cover.append(tex_file.name)
        # High match score companies
        elif any(company in name for company in ['spotify', 'klarna', 'techcorp']):
            if 'cv_' in name:
                high_match_cv.append(tex_file.name)
            else:
                high_match_cover.append(tex_file.name)
    
    print("🏢 PHASE 1: Gothenburg CVs (Highest Priority)")
    for i, file in enumerate(sorted(gothenburg_cv), 1):
        print(f"   {i}. {file}")
    
    print(f"\n📝 PHASE 2: Gothenburg Cover Letters")
    for i, file in enumerate(sorted(gothenburg_cover), 1):
        print(f"   {i}. {file}")
    
    print(f"\n⭐ PHASE 3: High Match Score CVs")
    for i, file in enumerate(sorted(high_match_cv), 1):
        print(f"   {i}. {file}")
    
    print(f"\n📄 PHASE 4: High Match Score Cover Letters")
    for i, file in enumerate(sorted(high_match_cover), 1):
        print(f"   {i}. {file}")

if __name__ == "__main__":
    create_compilation_guide()