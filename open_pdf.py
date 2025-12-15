#!/usr/bin/env python3
"""
Simple utility to open PDF files from job_applications folder using system PDF viewer.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def find_pdfs(base_dir="job_applications"):
    """Find all PDF files in the job_applications directory."""
    pdf_files = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Error: Directory '{base_dir}' not found")
        return []
    
    for pdf_file in base_path.rglob("*.pdf"):
        pdf_files.append(pdf_file)
    
    return sorted(pdf_files)


def list_pdfs():
    """List all available PDF files."""
    pdfs = find_pdfs()
    
    if not pdfs:
        print("No PDF files found in job_applications directory")
        return
    
    print(f"\nFound {len(pdfs)} PDF file(s):\n")
    for i, pdf in enumerate(pdfs, 1):
        size = pdf.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(pdf.stat().st_mtime)
        rel_path = pdf.relative_to("job_applications")
        print(f"{i}. {rel_path}")
        print(f"   Size: {size:.1f} KB | Modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def open_pdf(pdf_path):
    """Open a PDF file using the system default viewer (macOS)."""
    path = Path(pdf_path)
    
    # If relative path provided, try from job_applications
    if not path.is_absolute() and not path.exists():
        path = Path("job_applications") / pdf_path
    
    if not path.exists():
        print(f"Error: File not found: {pdf_path}")
        return False
    
    if not path.suffix.lower() == '.pdf':
        print(f"Error: Not a PDF file: {pdf_path}")
        return False
    
    try:
        # Use 'open' command on macOS to open with default app
        subprocess.run(['open', str(path)], check=True)
        print(f"✓ Opened: {path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening PDF: {e}")
        return False


def open_latest():
    """Open the most recently modified PDF."""
    pdfs = find_pdfs()
    
    if not pdfs:
        print("No PDF files found in job_applications directory")
        return
    
    # Sort by modification time, most recent first
    latest = max(pdfs, key=lambda p: p.stat().st_mtime)
    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
    
    print(f"Opening most recent PDF (modified {mtime.strftime('%Y-%m-%d %H:%M:%S')}):")
    open_pdf(latest)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python open_pdf.py list                    # List all PDFs")
        print("  python open_pdf.py latest                  # Open most recent PDF")
        print("  python open_pdf.py <path>                  # Open specific PDF")
        print("  python open_pdf.py <path1> <path2> ...     # Open multiple PDFs")
        print("\nExamples:")
        print("  python open_pdf.py kollmorgen/Kollmorgen_CL_20251119.pdf")
        print("  python open_pdf.py job_applications/essity/Essity_Cloud_Developer_CL_Harvad.pdf")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_pdfs()
    elif command == "latest":
        open_latest()
    else:
        # Open one or more PDFs
        success_count = 0
        for pdf_path in sys.argv[1:]:
            if open_pdf(pdf_path):
                success_count += 1
        
        if len(sys.argv) > 2:
            print(f"\n✓ Successfully opened {success_count}/{len(sys.argv)-1} file(s)")


if __name__ == "__main__":
    main()
