#!/usr/bin/env python3
"""Test PDF generation on server"""

import subprocess
from pathlib import Path
from cv_templates import CVTemplateManager

# Test template loading
manager = CVTemplateManager()
template = manager.load_template('android_developer')

if template:
    print(f"✓ Template loaded: {len(template)} characters")
    
    # Create test directory
    test_dir = Path('test_pdf_output')
    test_dir.mkdir(exist_ok=True)
    
    # Save template
    tex_file = test_dir / 'test.tex'
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✓ Template saved to: {tex_file}")
    
    # Try to compile
    print("\nAttempting PDF compilation...")
    result = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(test_dir), str(tex_file)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print(f"Return code: {result.returncode}")
    
    if result.returncode != 0:
        print("\n❌ COMPILATION FAILED")
        print("\nSTDERR:")
        print(result.stderr)
        print("\nSTDOUT (last 50 lines):")
        print('\n'.join(result.stdout.split('\n')[-50:]))
    else:
        pdf_file = test_dir / 'test.pdf'
        if pdf_file.exists():
            print(f"\n✓ PDF created successfully: {pdf_file}")
        else:
            print(f"\n❌ PDF not found at: {pdf_file}")
else:
    print("❌ Failed to load template")
