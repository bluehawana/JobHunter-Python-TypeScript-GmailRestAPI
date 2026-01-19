#!/usr/bin/env python3
"""
Fix CL Placeholder Issue - Replace COMPANY_NAME and JOB_TITLE with actual values
Uses the ECARX format (centered, bold header) with proper values filled in
"""

import os
import re
from pathlib import Path

def extract_company_and_job_from_path(folder_name: str) -> tuple:
    """Extract company and job title from folder name"""
    parts = folder_name.split('_')

    known_companies = {
        'ecarx': 'ECARX',
        'eworks': 'eWorks',
        'volvo': 'Volvo Group',
        'tata': 'Tata Consultancy Services',
        'benifex': 'Benifex',
        'incluso': 'Incluso',
        'ahlsell': 'Ahlsell',
        'alten': 'ALTEN',
        'doit': 'DoiT International',
        'kollmorgen': 'Kollmorgen',
        'saab': 'Saab AB',
        'cetasol': 'Cetasol',
        'omnimodular': 'OmniModular',
        'nasdaq': 'Nasdaq',
        'essity': 'Essity',
        'skf': 'SKF Group',
        'thomson': 'Thomson Reuters',
        'telia': 'Telia Company',
        'ascom': 'Ascom',
        'luxoft': 'Luxoft',
        'cleaning': 'Cleaning Robot Company',
        'gothenburg': 'Gothenburg Tech',
        'vfs': 'VFS Global',
    }

    company = None
    job_parts = []

    for part in parts:
        part_lower = part.lower()
        if part_lower in known_companies:
            company = known_companies[part_lower]
        else:
            job_parts.append(part)

    job_title = ' '.join(job_parts).title()
    job_title = job_title.replace('_', ' ')
    job_title = re.sub(r'\b(Cl|Cv|Complete|20\d+|Harvad|Li)\b', '', job_title, flags=re.IGNORECASE).strip()
    job_title = re.sub(r'\s+', ' ', job_title).strip()

    if not company:
        company = parts[0].title() if parts else 'Company'

    if not job_title or len(job_title) < 3:
        job_title = 'Software Developer'

    return company, job_title

def extract_info_from_content(content: str) -> tuple:
    """Try to extract company/job from CL body content"""
    company = None
    job_title = None

    # Look for "position at Company" pattern
    match = re.search(r'position at ([A-Z][A-Za-z\s&\.]+?)[\.\,]', content)
    if match:
        potential = match.group(1).strip()
        if potential and 'COMPANY' not in potential:
            company = potential

    # Look for "apply for the X position" pattern
    match = re.search(r'apply for the ([A-Za-z\s]+?) position', content)
    if match:
        potential = match.group(1).strip()
        if potential and 'JOB' not in potential:
            job_title = potential

    return company, job_title

def fix_cl_file(file_path: Path, company: str, job_title: str) -> bool:
    """Fix a single CL file with proper values"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Try to extract better values from content
        content_company, content_job = extract_info_from_content(content)
        if content_company:
            company = content_company
        if content_job:
            job_title = content_job

        # Replace placeholders using string replacement (not regex for simple cases)
        # Handle LaTeX escaped underscore: COMPANY\_NAME
        content = content.replace('COMPANY\\_NAME', company)
        content = content.replace('JOB\\_TITLE', job_title)
        # Handle non-escaped versions
        content = content.replace('COMPANY_NAME', company)
        content = content.replace('JOB_TITLE', job_title)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path.name}")
            print(f"   Company: {company}")
            print(f"   Job: {job_title}")
            return True
        else:
            print(f"⚪ No placeholders: {file_path.name}")
            return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all CL templates in job_applications"""
    print("🔧 Fixing CL Placeholder Issues")
    print("=" * 60)

    job_applications_dir = Path("job_applications")

    if not job_applications_dir.exists():
        print("❌ job_applications directory not found")
        return

    # Find all CL files
    cl_files = list(job_applications_dir.glob("**/*CL*.tex")) + list(job_applications_dir.glob("**/*_cl*.tex"))

    print(f"📁 Found {len(cl_files)} CL files\n")

    fixed_count = 0

    for cl_file in cl_files:
        folder_name = cl_file.parent.name
        company, job_title = extract_company_and_job_from_path(folder_name)

        if fix_cl_file(cl_file, company, job_title):
            fixed_count += 1

    print(f"\n{'=' * 60}")
    print(f"🎉 Fixed {fixed_count} files")

if __name__ == '__main__':
    main()
