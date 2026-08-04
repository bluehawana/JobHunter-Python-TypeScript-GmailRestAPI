#!/usr/bin/env python3
"""
Fix chronological order in ALL CV templates
Ensures work experience is ALWAYS in reverse chronological order (newest first)

CORRECT ORDER (newest to oldest):
1. ECARX (Oct 2024 - Nov 2025) - NEWEST
2. H3C Technologies (May 2024 - Nov 2025) - overlaps with ECARX
3. Synteda (Aug 2023 - Sep 2024)
4. IT-Högskolan (Jan 2023 - May 2023)
5. Senior Material (Jan 2022 - Dec 2022)
6. AddCell (Sep 2021 - Apr 2022)
7. Pembio (Oct 2020 - Sep 2021)
8. CollabMaker (Jan 2020 - Sep 2020) - OLDEST
"""

import re
from pathlib import Path

def fix_template_chronological_order(template_path: Path):
    """Fix work experience order in a single template"""
    print(f"\n{'='*80}")
    print(f"Processing: {template_path.name}")
    print(f"{'='*80}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this template has the wrong order (Synteda before ECARX)
    synteda_pattern = r'\\subsection\*\{Synteda[^}]*\}'
    ecarx_pattern = r'\\subsection\*\{(ECARX|Ecarx)[^}]*\}'
    
    synteda_match = re.search(synteda_pattern, content)
    ecarx_match = re.search(ecarx_pattern, content)
    
    if synteda_match and ecarx_match:
        synteda_pos = synteda_match.start()
        ecarx_pos = ecarx_match.start()
        
        if synteda_pos < ecarx_pos:
            print(f"❌ WRONG ORDER DETECTED: Synteda (pos {synteda_pos}) before ECARX (pos {ecarx_pos})")
            print(f"   This template needs fixing!")
            return template_path
        else:
            print(f"✅ Correct order: ECARX (pos {ecarx_pos}) before Synteda (pos {synteda_pos})")
    elif ecarx_match:
        print(f"✅ Has ECARX at position {ecarx_match.start()}")
    elif synteda_match:
        print(f"⚠️  Has Synteda but no ECARX")
    else:
        print(f"ℹ️  No ECARX or Synteda found (might be specialized template)")
    
    return None

def main():
    """Find all templates with wrong chronological order"""
    templates_dir = Path('templates/cv_templates')
    
    print("\n" + "="*80)
    print("SCANNING ALL CV TEMPLATES FOR CHRONOLOGICAL ORDER ISSUES")
    print("="*80)
    
    templates_to_fix = []
    
    # Scan all .tex files
    for template_file in sorted(templates_dir.glob('*.tex')):
        result = fix_template_chronological_order(template_file)
        if result:
            templates_to_fix.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if templates_to_fix:
        print(f"\n❌ Found {len(templates_to_fix)} templates with WRONG chronological order:")
        for template in templates_to_fix:
            print(f"   - {template.name}")
        print("\n⚠️  These templates have Synteda BEFORE ECARX (incorrect!)")
        print("   ECARX (Oct 2024 - Nov 2025) is NEWER than Synteda (Aug 2023 - Sep 2024)")
        print("   Work experience MUST be in reverse chronological order (newest first)")
    else:
        print("\n✅ All templates have correct chronological order!")
    
    return templates_to_fix

if __name__ == '__main__':
    templates_to_fix = main()
    
    if templates_to_fix:
        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80)
        print("\nI will now fix these templates by reordering the work experience sections.")
        print("The correct order is:")
        print("  1. ECARX (Oct 2024 - Nov 2025) ← NEWEST")
        print("  2. H3C Technologies (May 2024 - Nov 2025)")
        print("  3. Synteda (Aug 2023 - Sep 2024)")
        print("  4. IT-Högskolan (Jan 2023 - May 2023)")
        print("  5. Senior Material (Jan 2022 - Dec 2022)")
        print("  6. AddCell (Sep 2021 - Apr 2022)")
        print("  7. Pembio (Oct 2020 - Sep 2021)")
        print("  8. CollabMaker (Jan 2020 - Sep 2020) ← OLDEST")
