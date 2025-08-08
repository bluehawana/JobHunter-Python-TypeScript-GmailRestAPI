#!/usr/bin/env python3
"""
Hongzhi Li's Cover Letter Template - Python-friendly version
Converted from your exact LaTeX template with proper escaping
"""

def get_base_cover_letter_template() -> str:
    """Return base cover letter components focusing on soft skills and unique value"""
    return """
    HONGZHI LI'S COVER LETTER SOFT SKILLS FOCUS:
    
    UNIQUE VALUE PROPOSITIONS:
    1. Cross-Cultural Bridge Builder
       - Chinese background with deep Swedish tech integration
       - Understands both Eastern and Western business cultures
       - Valuable for companies with global operations or Chinese markets
    
    2. Business-IT Translator
       - Master's in International Business + Technical expertise
       - Bridges gap between technical complexity and business needs
       - Translates technical solutions into business value
    
    3. Cultural Adaptability
       - Successfully integrated into Swedish tech culture
       - Multilingual communication (Mandarin, English, Swedish)
       - Thrives in diverse, multicultural team environments
    
    4. Global Perspective
       - International mindset from education and work experience
       - Understands global market dynamics and cultural nuances
       - Brings fresh perspectives to problem-solving
    
    5. Collaborative Leadership
       - Experience working with diverse international teams
       - Strong communication and interpersonal skills
       - Facilitates cross-functional collaboration
    
    SOFT SKILLS TO EMPHASIZE:
    - Cross-cultural communication
    - Business acumen combined with technical depth
    - Adaptability and continuous learning
    - Problem-solving with global perspective
    - Team collaboration and cultural sensitivity
    - Innovation through diverse thinking
    
    AVOID REPEATING FROM CV:
    - Technical certifications
    - Programming languages lists
    - Detailed technical achievements
    - Specific project implementations
    """

COVER_LETTER_TEMPLATE = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{xcolor}

% Define colors
\definecolor{darkblue}{rgb}{0.0, 0.2, 0.6}

% Section formatting
\titleformat{\section}{\large\bfseries\raggedright\color{black}}{}{0em}{}[\titlerule]
\titleformat{\subsection}[runin]{\bfseries}{}{0em}{}[:]

% Remove paragraph indentation
\setlength{\parindent}{0pt}

\begin{document}
\pagestyle{empty} % no page number

\begin{letter}{\color{darkblue}\\{company_name}\\{company_address}}

\vspace{40pt}

\opening{{greeting}}

\vspace{10pt}

{cover_letter_body}

\vspace{20pt}

Sincerely,

Hongzhi Li\\
{current_date}

\vspace{40pt}

{\color{darkblue}\rule{\linewidth}{0.6pt}}
\vspace{4pt}

\closing{\color{darkblue} Ebbe Lieberathsgatan 27\\
412 65 Göteborg\\
hongzhili01@gmail.com\\
0728384299}

\vspace{10pt}

\end{letter}
\end{document}
"""

# Base cover letter structure for customization
BASE_COVER_LETTER_BODY = """I am writing to express my sincere interest in the {job_title} role at {company}. As a seasoned DevOps professional with a profound passion for the {industry}, I am excited by the prospect of contributing to the development of cutting-edge {solutions} for {target_audience}.

What draws me to {company} is the opportunity to work on innovative projects that shape the future of the {industry}. With my proven experience in {technical_alignment}, I am confident in my ability to streamline the software delivery processes for your mission-critical applications. Furthermore, my expertise in {key_technologies} aligns perfectly with your need for a developer who can leverage their experiences to improve the workflows for other developers.

Throughout my career, I have consistently demonstrated a strong commitment to coaching cross-functional teams on {methodologies} and fostering a culture of collaboration and continuous improvement. I thrive in multi-team environments, where I can leverage my overall understanding of complex systems and intricate integration processes to drive efficiency and innovation.

At {company}, I am eager to contribute my skills and knowledge in tools such as {tool_list}. My hands-on experience with these technologies, combined with my passion for the {industry}, makes me an ideal candidate for this role.

I am impressed by {company}'s accountable culture that enables teams to influence and make quick decisions. As a proactive and results-driven professional, I welcome the opportunity to shape the development of this role while contributing to the company's success.

Thank you for considering my application. I look forward to discussing how my expertise and passion can contribute to {company}'s exciting mission in developing cutting-edge {solutions}."""

# Industry-specific customizations
INDUSTRY_CUSTOMIZATIONS = {
    'automotive': {
        'industry': 'automotive industry',
        'solutions': 'infotainment platforms',
        'target_audience': 'Volvo, Polestar, and other Geely brand cars',
        'methodologies': 'DevOps methodologies'
    },
    'fintech': {
        'industry': 'financial technology',
        'solutions': 'financial platforms',
        'target_audience': 'banking and payment systems',
        'methodologies': 'modern development methodologies'
    },
    'music_tech': {
        'industry': 'music streaming technology',
        'solutions': 'audio platforms',
        'target_audience': 'millions of music lovers worldwide',
        'methodologies': 'scalable development practices'
    },
    'gaming': {
        'industry': 'gaming industry',
        'solutions': 'gaming platforms',
        'target_audience': 'gamers worldwide',
        'methodologies': 'agile development methodologies'
    },
    'default': {
        'industry': 'technology sector',
        'solutions': 'innovative solutions',
        'target_audience': 'users worldwide',
        'methodologies': 'modern development methodologies'
    }
}

# Technical alignment based on job requirements
TECHNICAL_ALIGNMENTS = {
    'devops': 'designing and optimizing CI/CD pipelines across multiple cloud platforms',
    'backend': 'building scalable backend services and RESTful APIs',
    'fullstack': 'developing end-to-end applications with modern web technologies',
    'cloud': 'architecting cloud-native solutions and infrastructure',
    'frontend': 'creating responsive user interfaces and modern web applications',
    'default': 'full-stack development and modern DevOps practices'
}

# Technology lists based on job focus
TECHNOLOGY_LISTS = {
    'devops': 'Python, Git, Cloud/Azure, Kubernetes, Linux, Ansible, Terraform, PostgreSQL, Grafana, TypeScript, ReactJS, and Docker',
    'backend': 'Java, Spring Boot, Python, PostgreSQL, AWS, Docker, Kubernetes, and microservices architecture',
    'fullstack': 'Java/Spring Boot, React, Angular, PostgreSQL, AWS, Docker, and modern CI/CD practices',
    'cloud': 'AWS, Azure, Kubernetes, Docker, Terraform, Python, and infrastructure automation',
    'frontend': 'React, Angular, TypeScript, JavaScript, HTML5, CSS3, and modern frontend frameworks',
    'default': 'Python, Java, Spring Boot, React, Cloud/Azure/AWS, Kubernetes, Docker, PostgreSQL, and modern CI/CD practices'
}