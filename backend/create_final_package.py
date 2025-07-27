#!/usr/bin/env python3
"""
Final LaTeX Compilation Solution
Creates ready-to-use files and instructions
"""

import os
import shutil
from pathlib import Path

def create_final_solution():
    """Create a complete solution package"""
    
    print("🎯 Final LaTeX Compilation Solution")
    print("=" * 50)
    
    # Create a ready-to-use package
    package_dir = Path("job_application_package")
    package_dir.mkdir(exist_ok=True)
    
    # Copy important files
    latex_dir = Path("latex_sources")
    if latex_dir.exists():
        # Copy all LaTeX files to package
        for tex_file in latex_dir.glob("*.tex"):
            shutil.copy2(tex_file, package_dir)
        
        tex_count = len(list(latex_dir.glob("*.tex")))
        print(f"✅ Copied {tex_count} LaTeX files to package")
    
    # Create Overleaf batch upload script
    overleaf_script = """#!/bin/bash
# Overleaf Batch Upload Instructions
echo "📱 OVERLEAF COMPILATION GUIDE"
echo "============================="
echo ""
echo "1. Go to: https://www.overleaf.com/"
echo "2. Create account (free)"
echo "3. Click 'New Project' > 'Upload Project'"
echo "4. Select files in this order:"
echo ""

echo "🏢 PRIORITY 1: Gothenburg CVs"
for file in cv_*volvo* cv_*polestar* cv_*skf* cv_*hasselblad* cv_*stena* cv_*cevt*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "📝 PRIORITY 2: Gothenburg Cover Letters"
for file in cover_letter_*volvo* cover_letter_*polestar* cover_letter_*skf* cover_letter_*hasselblad* cover_letter_*stena* cover_letter_*cevt*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "⭐ PRIORITY 3: High Match Companies"
for file in *spotify* *klarna* *techcorp*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "🔧 STEPS:"
echo "1. Upload 3-5 files at once to Overleaf"
echo "2. Click each file and press 'Recompile'"
echo "3. Download PDF for each compiled file"
echo "4. Repeat until all files are done"
"""
    
    with open(package_dir / "overleaf_guide.sh", 'w') as f:
        f.write(overleaf_script)
    
    os.chmod(package_dir / "overleaf_guide.sh", 0o755)
    
    # Create local compilation script  
    local_script = """#!/bin/bash
# Local LaTeX Compilation Script
echo "💻 LOCAL LATEX COMPILATION"
echo "=========================="

# Check if pdflatex exists
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found!"
    echo ""
    echo "📦 INSTALL LATEX:"
    echo "1. brew install --cask basictex"
    echo "2. Restart terminal"
    echo "3. Run: eval \\\"\\$(/usr/libexec/path_helper)\\\""
    echo "4. Install packages: sudo tlmgr install moderncv"
    echo "5. Run this script again"
    echo ""
    exit 1
fi

echo "✅ pdflatex found - starting compilation..."
echo ""

compiled=0
failed=0

# Compile priority files first
echo "🏢 COMPILING GOTHENBURG PRIORITY FILES:"
for file in cv_*volvo* cv_*polestar* cv_*skf* cv_*hasselblad* cv_*stena* cv_*cevt*; do
    if [ -f "$file" ]; then
        echo "📄 Compiling: $file"
        pdflatex -interaction=nonstopmode "$file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Success: ${file%.tex}.pdf"
            compiled=$((compiled + 1))
        else
            echo "❌ Failed: $file"
            failed=$((failed + 1))
        fi
    fi
done

echo ""
echo "📝 COMPILING COVER LETTERS:"
for file in cover_letter_*volvo* cover_letter_*polestar* cover_letter_*skf* cover_letter_*hasselblad* cover_letter_*stena* cover_letter_*cevt*; do
    if [ -f "$file" ]; then
        echo "📄 Compiling: $file"
        pdflatex -interaction=nonstopmode "$file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Success: ${file%.tex}.pdf"
            compiled=$((compiled + 1))
        else
            echo "❌ Failed: $file"
            failed=$((failed + 1))
        fi
    fi
done

# Compile remaining files
echo ""
echo "⭐ COMPILING REMAINING FILES:"
for file in *.tex; do
    # Skip if already compiled
    if [[ ! $file =~ (volvo|polestar|skf|hasselblad|stena|cevt) ]]; then
        echo "📄 Compiling: $file"
        pdflatex -interaction=nonstopmode "$file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Success: ${file%.tex}.pdf"
            compiled=$((compiled + 1))
        else
            echo "❌ Failed: $file"
            failed=$((failed + 1))
        fi
    fi
done

# Clean up auxiliary files
rm -f *.aux *.log *.out

echo ""
echo "🎯 COMPILATION RESULTS:"
echo "   ✅ Successful: $compiled"
echo "   ❌ Failed: $failed"
echo "   📁 PDFs created in current directory"

if [ $compiled -gt 0 ]; then
    echo ""
    echo "📋 GENERATED PDFs:"
    ls -1 *.pdf 2>/dev/null | head -10
    if [ $(ls -1 *.pdf 2>/dev/null | wc -l) -gt 10 ]; then
        echo "   ... and $(($(ls -1 *.pdf | wc -l) - 10)) more files"
    fi
fi
"""
    
    with open(package_dir / "compile_local.sh", 'w') as f:
        f.write(local_script)
    
    os.chmod(package_dir / "compile_local.sh", 0o755)
    
    # Create README
    readme_content = """# Job Application LaTeX Package

## 📊 Contents
- 26 LaTeX files (13 CVs + 13 Cover Letters)
- Customized for Swedish tech companies
- Priority focus on Gothenburg positions

## 🏢 Priority Companies (Gothenburg)
1. Volvo Group - Senior Python Developer  
2. Zenseact (Volvo) - Full Stack Developer
3. SKF Group - Backend Developer
4. Hasselblad - DevOps Engineer
5. Polestar - Machine Learning Engineer
6. CEVT - Data Engineer
7. Stena Line - Software Engineer

## 🔧 Compilation Options

### Option 1: Overleaf (Recommended)
```bash
./overleaf_guide.sh
```
Then follow the instructions to upload and compile online.

### Option 2: Local Installation
```bash
# Install LaTeX first
brew install --cask basictex

# Restart terminal, then:
./compile_local.sh
```

### Option 3: Manual Online
- Go to https://latexbase.com/
- Upload individual .tex files
- Click "Generate PDF"

## 📋 File Priority Order
1. **cv_Volvo_Group_Senior_Python_Developer.tex** (Highest Priority)
2. **cv_Polestar_Machine_Learning_Engineer.tex**
3. **cv_Zenseact_Volvo_Full_Stack_Developer.tex**
4. ... (see overleaf_guide.sh for complete order)

## 🎯 Next Steps
1. Compile PDFs using one of the methods above
2. Customize personal information in LaTeX files
3. Apply to positions with generated documents

Generated by JobHunter LaTeX Generator
"""
    
    with open(package_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    # Create quick start script
    quickstart = """#!/bin/bash
echo "🚀 JobHunter Application Package Quick Start"
echo "============================================="
echo ""
echo "📊 Package Contents:"
echo "   📄 $(ls *.tex | wc -l) LaTeX files ready for compilation"
echo "   🏢 16 Gothenburg priority positions"
echo "   ⭐ 10 high-match additional positions"
echo ""
echo "🔧 Choose compilation method:"
echo "   1. Type: ./overleaf_guide.sh (for online compilation)"
echo "   2. Type: ./compile_local.sh (for local compilation)"
echo "   3. Read: README.md (for detailed instructions)"
echo ""
echo "🎯 Recommended: Start with Overleaf for easiest PDF generation!"
"""
    
    with open(package_dir / "quickstart.sh", 'w') as f:
        f.write(quickstart)
    
    os.chmod(package_dir / "quickstart.sh", 0o755)
    
    print(f"✅ Created compilation scripts")
    print(f"✅ Created README.md")
    print(f"✅ Created quickstart guide")
    
    print(f"\n📦 COMPLETE PACKAGE READY:")
    print(f"   📁 Location: {package_dir}/")
    print(f"   📄 {len(list(package_dir.glob('*.tex')))} LaTeX files")
    print(f"   🔧 4 helper scripts")
    print(f"   📋 1 README file")
    
    print(f"\n🚀 TO START:")
    print(f"   cd {package_dir}")
    print(f"   ./quickstart.sh")
    
    # Show what's in the package
    print(f"\n📋 PACKAGE CONTENTS:")
    for item in sorted(package_dir.iterdir()):
        if item.is_file():
            if item.suffix == '.tex':
                print(f"   📄 {item.name}")
            elif item.suffix == '.sh':
                print(f"   🔧 {item.name}")
            else:
                print(f"   📋 {item.name}")

if __name__ == "__main__":
    create_final_solution()