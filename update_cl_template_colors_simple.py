#!/usr/bin/env python3
"""
Simple script to update CL templates with LinkedIn blue colors
"""

import os
from pathlib import Path

def update_cl_template(file_path):
    """Update a single CL template with LinkedIn blue colors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Skip if already has colored header
        if '{\color{linkedinblue}' in content and 'COMPANY\_NAME' in content:
            print(f"⚪ Already updated: {file_path}")
            return False
        
        # Update header to use LinkedIn blue
        if 'COMPANY\_NAME\\' in content and '{\color{linkedinblue}' not in content:
            # Find the header section
            lines = content.split('\n')
            new_lines = []
            in_header = False
            header_start = -1
            
            for i, line in enumerate(lines):
                if '% Header with job information' in line:
                    new_lines.append(line)
                    in_header = True
                    header_start = i
                elif in_header and 'COMPANY\_NAME' in line:
                    # Start the colored header
                    new_lines.append('{\color{linkedinblue}')
                    new_lines.append(line)
                elif in_header and 'Gothenburg, Sweden' in line:
                    # End the colored header
                    new_lines.append(line)
                    new_lines.append('}')
                    in_header = False
                elif '% Line separator' in line:
                    new_lines.append(line)
                    # Next line should be the hrule
                    if i + 1 < len(lines) and '\\hrule' in lines[i + 1]:
                        new_lines.append('{\color{linkedinblue}\\hrule height 0.5pt}')
                        i += 1  # Skip the original hrule line
                    else:
                        new_lines.append(line)
                elif '\\noindent Ebbe Lieberathsgatan' in line:
                    # Color the footer
                    new_lines.append('\\noindent {\\color{linkedinblue}Ebbe Lieberathsgatan 27\\\\')
                    new_lines.append('41265 Gothenburg, Sweden} \\hfill {\\color{linkedinblue}\\today}')
                elif 'Ebbe Lieberathsgatan 27, 41265 Gothenburg, Sweden' in line and '\\hfill' in line:
                    # Handle single line footer
                    new_lines.append('\\noindent {\\color{linkedinblue}Ebbe Lieberathsgatan 27\\\\')
                    new_lines.append('41265 Gothenburg, Sweden} \\hfill {\\color{linkedinblue}\\today}')
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⚪ No changes needed: {file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Update all CL templates"""
    print("🎨 Updating CL templates with LinkedIn blue colors...")
    
    # Find all CL template files
    job_applications_dir = Path("job_applications")
    cl_files = list(job_applications_dir.glob("**/*CL*.tex"))
    
    print(f"📁 Found {len(cl_files)} CL template files")
    
    updated_count = 0
    
    for cl_file in cl_files:
        if update_cl_template(cl_file):
            updated_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   Total CL files: {len(cl_files)}")
    print(f"   Files updated: {updated_count}")
    print(f"   Files already correct: {len(cl_files) - updated_count}")

if __name__ == '__main__':
    main()