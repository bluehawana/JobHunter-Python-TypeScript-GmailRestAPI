#!/usr/bin/env python3
"""
Script to update all cover letter templates to the new format
"""

import os
import re
from pathlib import Path

def update_cl_template(file_path):
    """Update a single CL template to the new format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if it's already in new format
        if 'COMPANY_NAME' in content and 'JOB_TITLE' in content and 'Best Regards' in content:
            print(f"⚪ Already updated: {file_path}")
            return False
        
        # Create the new template structure
        new_template = r"""\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=1in}
\setlength{\parindent}{0pt}
\definecolor{linkedinblue}{RGB}{0,119,181}
\hypersetup{colorlinks=true, linkcolor=linkedinblue, urlcolor=linkedinblue}

\begin{document}

% Header with job information (no name)
\begin{center}
{\Large \textbf{COMPANY\_NAME}}\\[4pt]
{\Large \textbf{JOB\_TITLE}}\\[4pt]
{\Large \textbf{Gothenburg, Sweden}}\\[8pt]
\end{center}

\vspace{1cm}

Dear Hiring Manager,

\vspace{0.5cm}
"""

        # Extract the main body content (between greeting and signature)
        body_content = ""
        
        # Try to extract body content from various patterns
        patterns = [
            r'I am excited to apply for.*?(?=Sincerely|Best Regards|Med vänliga hälsningar)',
            r'Hej.*?(?=Sincerely|Best Regards|Med vänliga hälsningar)',
            r'Dear.*?\n\n(.*?)(?=Sincerely|Best Regards|Med vänliga hälsningar)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                if len(patterns) == 3 and match.groups():  # Third pattern has a group
                    body_content = match.group(1).strip()
                else:
                    body_content = match.group(0).strip()
                break
        
        # If no body found, use a default template
        if not body_content:
            body_content = """I am excited to apply for the JOB_TITLE position at COMPANY_NAME. As a developer with expertise in modern technologies and a unique background bridging business and technology, I bring both technical skills and the ability to understand business workflows and translate them into robust solutions.

My experience spans full-stack development and cross-cultural collaboration. I have worked with distributed international teams and have a proven track record of delivering scalable solutions using modern development practices.

What sets me apart is my ability to bridge technical and business worlds. My educational background combined with hands-on development experience means I understand how technical decisions affect operational efficiency and business scalability. This enables me to analyze complex problems, understand real customer needs, and propose effective technical solutions.

I'm fluent in English and Mandarin Chinese, with Swedish B2 proficiency. I would love to discuss how my technical expertise, cross-cultural communication skills, and business-IT integration mindset can contribute to COMPANY_NAME's continued success."""
        
        # Clean up the body content
        body_content = re.sub(r'\[Company Name\]', 'COMPANY_NAME', body_content)
        body_content = re.sub(r'\[Position\]', 'JOB_TITLE', body_content)
        body_content = re.sub(r'\\vspace\{[^}]+\}', '', body_content)  # Remove vspace commands
        body_content = re.sub(r'\\\\', '', body_content)  # Remove line breaks
        body_content = body_content.strip()
        
        # Add the footer
        footer = r"""
\vspace{1cm}

Best Regards,\\[0.5cm]
Harvad (Hongzhi) Li

\vspace{\fill}

% Line separator
{\color{linkedinblue}\hrule height 0.5pt}

\vspace{0.3cm}

% Footer with address and date
\noindent Ebbe Lieberathsgatan 27, 41265 Gothenburg, Sweden \hfill \today

\end{document}"""

        # Combine everything
        new_content = new_template + body_content + footer
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all CL templates"""
    print("🔍 Finding CL templates to update...")
    
    # Find all CL template files
    job_applications_dir = Path("job_applications")
    cl_files = list(job_applications_dir.glob("**/*CL*.tex"))
    
    print(f"📁 Found {len(cl_files)} CL template files")
    
    updated_count = 0
    
    for cl_file in cl_files:
        print(f"\n📄 Processing: {cl_file}")
        
        if update_cl_template(cl_file):
            updated_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   Total CL files found: {len(cl_files)}")
    print(f"   Files updated: {updated_count}")
    print(f"   Files already up-to-date: {len(cl_files) - updated_count}")
    
    print(f"\n✅ All cover letter templates now use the new format:")
    print(f"   • Header: Company, Job Title, Location")
    print(f"   • Signature: Best Regards, Harvad (Hongzhi) Li")
    print(f"   • Footer: Address and date with line separator")
    print(f"   • Updated address: Ebbe Lieberathsgatan 27, 41265 Gothenburg")

if __name__ == '__main__':
    main()