#!/usr/bin/env python3

# Test the cover letter replacement logic

template_content = r"""
\begin{center}
{\Large \textbf{COMPANY\_NAME}}\\[4pt]
{\Large \textbf{JOB\_TITLE}}\\[4pt]
{\Large \textbf{Gothenburg, Sweden}}\\[8pt]
\end{center}
"""

def customize_cover_letter(template_content: str, company: str, title: str) -> str:
    """Customize cover letter template with company and title"""
    import re
    from datetime import datetime

    # Clean up title - remove leading articles (an, a, the)
    if title:
        title = re.sub(r'^(an?|the)\s+', '', title, flags=re.IGNORECASE).strip()
        # Capitalize first letter of each word
        title = title.title() if title else title

    print(f"Original template:\n{template_content}")
    print(f"Company: '{company}', Title: '{title}'")

    # Replace both old and new placeholder formats
    if company and company != 'Company':
        template_content = template_content.replace('[Company Name]', company)
        template_content = template_content.replace('COMPANY\_NAME', company)
        template_content = template_content.replace('COMPANY_NAME', company)

    # Replace [Position] placeholder and new format
    if title and title != 'Position':
        template_content = template_content.replace('[Position]', title)
        template_content = template_content.replace('JOB\_TITLE', title)
        template_content = template_content.replace('JOB_TITLE', title)

    print(f"After replacement:\n{template_content}")
    return template_content

# Test
result = customize_cover_letter(template_content, "Emerson", "It Business Analyst")
print("Final result:")
print(result)