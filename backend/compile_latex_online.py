#!/usr/bin/env python3
"""
Alternative PDF generation using online LaTeX compiler
"""

import os
import sys
import requests
import time
from pathlib import Path

def compile_latex_online(latex_content: str, filename: str) -> bool:
    """Compile LaTeX to PDF using online service"""
    
    # Use a public LaTeX compilation API
    try:
        # LaTeX.Online API
        url = "https://latex.api.aa.net.uk/latex/pdf"
        
        data = {
            'tex': latex_content
        }
        
        print(f"🔄 Compiling {filename} online...")
        
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            # Save PDF
            pdf_path = f"compiled_pdfs/{filename}.pdf"
            os.makedirs("compiled_pdfs", exist_ok=True)
            
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Success: {filename}.pdf")
            return True
        else:
            print(f"❌ Failed: {filename} (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error compiling {filename}: {e}")
        return False

def compile_all_latex_files():
    """Compile all LaTeX files to PDF using online service"""
    
    print("🚀 Online LaTeX to PDF Compilation")
    print("=" * 50)
    
    latex_dir = Path("latex_sources")
    if not latex_dir.exists():
        print("❌ latex_sources directory not found!")
        return
    
    # Get all .tex files
    tex_files = list(latex_dir.glob("*.tex"))
    
    if not tex_files:
        print("❌ No .tex files found!")
        return
    
    print(f"📄 Found {len(tex_files)} LaTeX files")
    print()
    
    successful = 0
    failed = 0
    
    # Prioritize Gothenburg jobs
    priority_files = []
    other_files = []
    
    for tex_file in tex_files:
        if any(company in tex_file.name.lower() for company in ['volvo', 'polestar', 'skf', 'hasselblad', 'stena', 'cevt']):
            priority_files.append(tex_file)
        else:
            other_files.append(tex_file)
    
    # Process priority files first
    all_files = priority_files + other_files
    
    for i, tex_file in enumerate(all_files, 1):
        print(f"{i}/{len(all_files)}: {tex_file.name}")
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            filename = tex_file.stem
            
            if compile_latex_online(latex_content, filename):
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Error reading {tex_file.name}: {e}")
            failed += 1
        
        # Add delay to avoid overwhelming the service
        time.sleep(2)
        print()
    
    print("🎯 COMPILATION RESULTS:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 PDFs saved to: compiled_pdfs/")
    
    if successful > 0:
        print(f"\n🎉 {successful} PDFs generated successfully!")
        
        # List generated PDFs
        pdf_dir = Path("compiled_pdfs")
        if pdf_dir.exists():
            pdfs = list(pdf_dir.glob("*.pdf"))
            if pdfs:
                print("\n📋 Generated PDFs:")
                for pdf in sorted(pdfs):
                    print(f"   📄 {pdf.name}")

def main():
    """Main function"""
    try:
        compile_all_latex_files()
    except KeyboardInterrupt:
        print("\n⚠️  Compilation interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()