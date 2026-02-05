#!/usr/bin/env python3
"""Test NVIDIA extraction"""

# Exact text you provided
nvidia_text = """even this id nividia the forefront of research and engineering around the greatest advances in technology Industry Solution Architect At Nvidia Gothenburg, Sweden"""

# Check if nvidia is in text
text_lower = nvidia_text.lower()
print(f"Text contains 'nvidia': {'nvidia' in text_lower}")
print(f"Text contains 'nividia': {'nividia' in text_lower}")

# Priority company check
priority_companies = [
    ('nvidia', 'NVIDIA'),
]

company = 'Company'
for search_term, proper_name in priority_companies:
    if search_term in text_lower:
        company = proper_name
        print(f"📍 Found priority company: {company}")
        break

print(f"\n✅ Extracted Company: {company}")

# Note: There's a typo "nividia" in the text, but "Nvidia" (correct spelling) also appears
# The search will find "nvidia" (lowercase) in "Nvidia"
