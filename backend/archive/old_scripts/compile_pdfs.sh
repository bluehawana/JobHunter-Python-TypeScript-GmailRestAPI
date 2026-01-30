#!/bin/bash
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
