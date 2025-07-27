#!/bin/bash
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
    echo "3. Run: eval \"\$(/usr/libexec/path_helper)\""
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
