#!/usr/bin/env python3
"""Test skills reordering function"""

import sys
import re
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

# Read ALTEN template
template_path = Path('job_applications/alten_cloud/ALTEN_Cloud_Engineer_Harvad_CV.tex')
with open(template_path, 'r', encoding='utf-8') as f:
    template_content = f.read()

print("Testing skills reordering...")
print(f"Template length: {len(template_content)} chars")

# Test the regex pattern
skills_pattern = r'(\\section\*\{Core Technical (?:Skills|Competencies)\})(.*?)(\\section\*\{)'
match = re.search(skills_pattern, template_content, re.DOTALL)

if match:
    print("✓ Found Core Technical Competencies section")
    skills_content = match.group(2)
    print(f"  Skills content length: {len(skills_content)} chars")
    print(f"\nFirst 300 chars of skills content:")
    print(repr(skills_content[:300]))
    
    # Try different patterns
    patterns = [
        (r'\\item\s+\\textbf\{[^}]+\}:[^\n]+', 'Pattern 1: [^\\n]+'),
        (r'\\item\s+\\textbf\{[^}]+\}:.+', 'Pattern 2: .+'),
        (r'\\item[^\n]+', 'Pattern 3: Simple \\item[^\\n]+'),
    ]
    
    for pattern, desc in patterns:
        items = re.findall(pattern, skills_content)
        print(f"\n{desc}")
        print(f"  Found {len(items)} items")
        if items:
            print(f"  First item: {items[0][:80]}...")
    
else:
    print("❌ Could not find Core Technical Competencies section")
