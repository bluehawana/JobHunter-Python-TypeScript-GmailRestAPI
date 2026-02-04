#!/usr/bin/env python3
"""
Hongzhi Li's Cover Letter Template - Python-friendly version
Converted from your exact LaTeX template with proper escaping
"""
from datetime import datetime

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
\documentclass[10pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{geometry}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}

\geometry{{margin=1in}}
\setlength{{\parindent}}{{0pt}}
\definecolor{{darkblue}}{{RGB}}{{0,51,102}}
\hypersetup{{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}}

\begin{{document}}

% Header with job information (light blue)
{{\color{{darkblue}}\textbf{{{company_name}}}\\
{job_title}\\
Gothenburg, Sweden}}

\vspace{{1cm}}

{greeting}

\vspace{{0.5cm}}

{cover_letter_body}

\vspace{{1cm}}

Best Regards,\\[0.5cm]
Harvad (Hongzhi) Li

\vspace{{\fill}}

% Line separator
{{\color{{darkblue}}\hrule height 0.5pt}}

\vspace{{0.3cm}}

% Footer with address and date
{{\color{{darkblue}}Ebbe Lieberathsgatan 27\\
412 65, Gothenburg, Sweden\\
\hfill \today}}

\end{{document}}
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

class LegoCoverLetterBuilder:
    """LEGO Component Cover Letter Builder - Intelligently tailors cover letter based on job requirements"""
    
    def __init__(self):
        self.base_template = COVER_LETTER_TEMPLATE
        self.base_body = BASE_COVER_LETTER_BODY
        self.industry_customizations = INDUSTRY_CUSTOMIZATIONS
        self.technical_alignments = TECHNICAL_ALIGNMENTS
        self.technology_lists = TECHNOLOGY_LISTS
    
    def generate_tailored_cover_letter(self, job_data: dict, company_info: dict = None) -> str:
        """Generate LEGO-tailored cover letter based on job requirements"""
        
        # Analyze job requirements
        job_title = job_data.get('title', 'Software Developer')
        company = job_data.get('company', 'Technology Company')
        job_description = job_data.get('description', '').lower()
        
        # Use extracted company info if available
        if company_info:
            company = company_info.get('company_name', company)
            location = company_info.get('company_address') or job_data.get('location') or "Gothenburg, Sweden"
            greeting = company_info.get('greeting', "Dear Hiring Manager,")
        else:
            location = job_data.get('location') or "Gothenburg, Sweden"
            greeting = "Dear Hiring Manager,"
        
        # Determine industry and technical focus
        industry_key = self._determine_industry(company, job_description)
        tech_focus = self._determine_tech_focus(job_title, job_description)
        
        # Get LEGO components
        industry_info = self.industry_customizations.get(industry_key, self.industry_customizations['default'])
        technical_alignment = self.technical_alignments.get(tech_focus, self.technical_alignments['default'])
        tool_list = self.technology_lists.get(tech_focus, self.technology_lists['default'])
        
        # Build cover letter body
        customized_body = self.base_body.format(
            job_title=job_title,
            company=company,
            industry=industry_info['industry'],
            solutions=industry_info['solutions'],
            target_audience=industry_info['target_audience'],
            technical_alignment=technical_alignment,
            key_technologies="containerization, infrastructure as code, and automation practices",
            methodologies=industry_info['methodologies'],
            tool_list=tool_list
        )
        
        # Build complete cover letter
        cover_letter = self.base_template.format(
            company_name=company,
            job_title=job_title,
            location=location,
            greeting=greeting,
            current_date=datetime.now().strftime("%B %d, %Y"),
            cover_letter_body=customized_body
        )
        
        return cover_letter
    
    def _determine_industry(self, company: str, description: str) -> str:
        """Determine industry for LEGO component selection"""
        content = f"{company} {description}".lower()
        
        if any(word in content for word in ['volvo', 'automotive', 'car', 'vehicle', 'ecarx']):
            return 'automotive'
        elif any(word in content for word in ['spotify', 'music', 'audio', 'streaming']):
            return 'music_tech'
        elif any(word in content for word in ['klarna', 'bank', 'financial', 'fintech', 'payment']):
            return 'fintech'
        elif any(word in content for word in ['game', 'gaming', 'king', 'dice']):
            return 'gaming'
        else:
            return 'default'
    
    def _determine_tech_focus(self, job_title: str, description: str) -> str:
        """Determine technical focus for LEGO component selection"""
        content = f"{job_title} {description}".lower()
        
        if any(word in content for word in ['devops', 'infrastructure', 'kubernetes', 'ci/cd']):
            return 'devops'
        elif any(word in content for word in ['backend', 'api', 'microservices', 'server']):
            return 'backend'
        elif any(word in content for word in ['frontend', 'react', 'angular', 'ui', 'ux']):
            return 'frontend'
        elif any(word in content for word in ['cloud', 'aws', 'azure', 'gcp']):
            return 'cloud'
        elif any(word in content for word in ['fullstack', 'full stack', 'full-stack']):
            return 'fullstack'
        else:
            return 'default'

# Create global instance for easy access
lego_cover_letter_builder = LegoCoverLetterBuilder()

def generate_tailored_cover_letter(job_data: dict, company_info: dict = None) -> str:
    """Main function to generate LEGO-tailored cover letter"""
    return lego_cover_letter_builder.generate_tailored_cover_letter(job_data, company_info)
