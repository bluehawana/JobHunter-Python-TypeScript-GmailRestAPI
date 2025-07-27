#!/bin/bash
# LaTeX Compilation Script
# Run this to compile all .tex files to PDF

echo "🔄 Compiling LaTeX files to PDF..."
echo "=================================="

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found!"
    echo "Install LaTeX: brew install basictex"
    exit 1
fi

compiled=0
total=0

# Compile all .tex files
for file in *.tex; do
    if [ -f "$file" ]; then
        echo "📄 Compiling: $file"
        pdflatex -interaction=nonstopmode "$file" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "✅ Success: ${file%.tex}.pdf"
            compiled=$((compiled + 1))
        else
            echo "❌ Failed: $file"
        fi
        
        total=$((total + 1))
        
        # Clean up auxiliary files
        rm -f *.aux *.log *.out
    fi
done

echo "=================================="
echo "🎯 Results: $compiled/$total files compiled successfully"
echo "📁 Check for .pdf files in this directory"
