#!/usr/bin/env python3
"""
Fix all CL templates to have simple, clean headers like the Omegapoint/Ahlsell example
Convert centered bold headers to simple left-aligned format
"""

import os
import re
from pathlib import Path

def fix_cl_header(file_path):
    """Fix CL template header to be simple and clean"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Check if it has the centered bold format
        if '\\begin{center}' not in content or '{\\Large' not in content:
            print(f"  Already good format: {file_path.name}")
            return False

        # Extract company, title, location from centered header
        # Pattern: {\Large \textbf{VALUE}}
        pattern = r'\{\\Large\s*\\textbf\{([^}]+)\}\}'
        matches = re.findall(pattern, content)

        if len(matches) >= 3:
            company = matches[0]
            title = matches[1]
            location = matches[2]
        elif len(matches) >= 2:
            company = matches[0]
            title = matches[1]
            location = "Gothenburg, Sweden"
        else:
            print(f"  Could not extract header values from: {file_path.name}")
            return False

        # Build the simple header replacement (double backslash for LaTeX line break)
        simple_header = f"% Header with job information (simple left-aligned, Omegapoint style)\n{company}\\\\\\\\\n{title}\\\\\\\\\n{location}"

        # Replace the centered header block
        # Match from \begin{center} to \end{center}
        center_pattern = r'% Header with job information[^\n]*\n\s*\\begin\{center\}.*?\\end\{center\}'
        content = re.sub(center_pattern, simple_header, content, flags=re.DOTALL)

        # If that didn't work, try without the comment
        if content == original_content:
            center_pattern2 = r'\\begin\{center\}\s*\n(?:\s*\{\\Large\s*\\textbf\{[^}]+\}\}\\\\(?:\[\d+pt\])?\s*\n)+\s*\\end\{center\}'
            content = re.sub(center_pattern2, simple_header, content, flags=re.DOTALL)

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: {file_path.name} ({company} / {title})")
            return True
        else:
            print(f"  No changes needed: {file_path.name}")
            return False

    except Exception as e:
        print(f"  Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all CL template headers"""
    print("Fixing CL template headers to simple Omegapoint style...")
    print("=" * 60)

    # Find all CL template files
    job_applications_dir = Path("job_applications")
    cl_files = list(job_applications_dir.glob("**/*CL*.tex"))

    print(f"Found {len(cl_files)} CL template files\n")

    fixed_count = 0

    for cl_file in cl_files:
        if fix_cl_header(cl_file):
            fixed_count += 1

    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"   Total CL files: {len(cl_files)}")
    print(f"   Headers fixed: {fixed_count}")
    print(f"   Already simple: {len(cl_files) - fixed_count}")

    print(f"\nAll CL headers now use simple Omegapoint format:")
    print(f"   Company Name")
    print(f"   Job Title")
    print(f"   Gothenburg, Sweden")

if __name__ == '__main__':
    main()