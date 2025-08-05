#!/usr/bin/env python3
"""
Hongzhi Li's Cover Letter Template - Python-friendly version
Converted from your exact LaTeX template with proper escaping
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

\begin{letter}{\color{darkblue}\\COMPANY_NAME\\COMPANY_ADDRESS}

\vspace{40pt}

\opening{GREETING}

\vspace{10pt}

COVER_LETTER_BODY

\vspace{20pt}

Sincerely,

Hongzhi Li\\
CURRENT_DATE

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