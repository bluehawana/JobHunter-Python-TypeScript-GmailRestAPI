"""
AI-Powered Resume Enhancement Prompts
Collection of proven prompts for improving resumes, targeting roles, and interview prep
"""

class AIResumePrompts:
    """
    Proven AI prompts for resume optimization and job search strategy
    Based on successful patterns that help candidates get more interviews
    """
    
    @staticmethod
    def resume_rewrite(resume_text: str) -> str:
        """
        Rewrite resume to improve interview chances
        Adds measurable achievements, strong action verbs, and ATS-friendly formatting
        """
        return f"""Here's my resume:

{resume_text}

Rewrite it to improve my chances of getting interviews. Follow these guidelines:
1. Add measurable achievements with specific numbers and percentages
2. Use strong action verbs (built, led, achieved, reduced, increased, implemented)
3. Make it ATS-friendly with clear section headers and keyword optimization
4. Highlight impact and outcomes, not just responsibilities
5. Keep it concise - one page for <10 years experience, two pages for 10+ years
6. Remove weak phrases like "responsible for" or "helped with"
7. Quantify everything possible (team size, budget, users, performance improvements)

Focus on making every bullet point answer: "So what? What was the impact?"
"""

    @staticmethod
    def role_targeting(experience_text: str) -> str:
        """
        Identify high-paying roles based on experience
        Helps candidates understand their market value and opportunities
        """
        return f"""Based on my experience:

{experience_text}

Identify 10 high-paying roles I'm qualified for, ranked by:
1. Average salary range (provide specific numbers in SEK/EUR/USD)
2. Market demand (high/medium/low with explanation)
3. Skills match percentage (how well my experience aligns)

For each role, include:
- Role title
- Salary range
- Key requirements I already meet
- Skills I should highlight
- Any gaps I should address

Direction matters more than effort - help me target the right opportunities.
"""

    @staticmethod
    def jd_match_check(job_description: str, resume_text: str) -> str:
        """
        Compare JD with resume and optimize for 90% keyword alignment
        Most resumes aren't "bad" - they're just mismatched
        """
        return f"""Job description:
{job_description}

My resume:
{resume_text}

Compare the keywords and requirements between the job description and my resume:

1. List all key requirements from the JD
2. Identify which requirements I meet (with evidence from my resume)
3. Identify missing keywords that I should add (without exaggerating)
4. Calculate current alignment percentage
5. Revise my resume to reach ~90% alignment while staying truthful

Focus on:
- Technical skills and tools mentioned in JD
- Soft skills and competencies
- Industry-specific terminology
- Measurable outcomes that match their needs

Provide the revised resume with highlighted changes.
"""

    @staticmethod
    def interview_prep(position: str, job_description: str = "") -> str:
        """
        Generate realistic interview questions with confident sample answers
        Practice once ahead of time and your nerves drop fast
        """
        jd_context = f"\n\nJob description:\n{job_description}" if job_description else ""
        
        return f"""For the role of {position}{jd_context}

Give me 15 realistic interview questions covering:
- Technical skills (5 questions)
- Behavioral/situational (5 questions)
- Role-specific scenarios (3 questions)
- Company culture fit (2 questions)

For each question, provide:
1. The question
2. Why they're asking it (what they want to learn)
3. A clear, confident sample answer using the STAR method where appropriate
4. Key points to emphasize

Help me practice so I can walk in confident and prepared.
"""

    @staticmethod
    def proof_projects(position: str, job_description: str) -> str:
        """
        Suggest small projects to demonstrate required skills
        Work samples beat claims every time
        """
        return f"""For the role of {position}

Job requirements:
{job_description}

Suggest 3 small projects I can complete this week that directly demonstrate the required skills:

For each project:
1. Project name and description
2. Specific skills it demonstrates (matching JD requirements)
3. Time estimate (should be completable in 1-3 days)
4. Deliverables (what to show in portfolio/GitHub)
5. How to present it in interviews

Focus on projects that:
- Solve real problems (not just tutorials)
- Show technical depth
- Can be completed quickly
- Demonstrate multiple skills from the JD
- Are impressive but achievable

Work samples beat claims - help me prove I can do the job.
"""

    @staticmethod
    def salary_negotiation(position: str, experience_years: int, location: str = "Sweden") -> str:
        """
        Research salary ranges and negotiation strategy
        """
        return f"""For the role of {position} with {experience_years} years of experience in {location}:

Provide:
1. Salary range (25th, 50th, 75th percentile) in local currency
2. Factors that increase compensation (skills, certifications, company size)
3. Total compensation beyond base salary (bonus, equity, benefits)
4. Negotiation strategy:
   - When to discuss salary
   - How to anchor high
   - What to say when they ask for current salary
   - How to handle lowball offers
5. Market data sources to cite

Help me understand my market value and negotiate confidently.
"""

    @staticmethod
    def cover_letter_generator(job_description: str, resume_text: str, company_name: str) -> str:
        """
        Generate compelling cover letter that tells a story
        """
        return f"""Generate a compelling cover letter for:

Company: {company_name}

Job description:
{job_description}

My resume:
{resume_text}

Create a cover letter that:
1. Opens with a hook (not "I'm writing to apply...")
2. Tells a story connecting my experience to their needs
3. Shows I researched the company (mention specific products/values)
4. Highlights 2-3 key achievements relevant to the role
5. Explains why I'm excited about THIS company (not just any job)
6. Closes with confidence and a call to action
7. Keeps it under 400 words

Make it personal, specific, and memorable - not a generic template.
"""

    @staticmethod
    def linkedin_optimization(resume_text: str, target_roles: list) -> str:
        """
        Optimize LinkedIn profile for recruiter searches
        """
        roles_str = ", ".join(target_roles)
        
        return f"""Based on my resume:

{resume_text}

Target roles: {roles_str}

Optimize my LinkedIn profile:

1. Headline (120 chars) - keyword-rich and compelling
2. About section (2600 chars) - tell my story with keywords
3. Experience bullets - rewrite for impact and SEO
4. Skills section - prioritize top 10 skills recruiters search for
5. Featured section - what to showcase
6. Recommendations - who to ask and what to request

Focus on:
- Keywords recruiters search for these roles
- Quantified achievements
- Social proof and credibility signals
- Call-to-action for recruiters

Make my profile irresistible to recruiters searching for {roles_str}.
"""


# Example usage functions
def enhance_resume_with_ai(resume_text: str) -> dict:
    """
    Generate all enhancement prompts for a given resume
    Returns dict of prompt types and their generated prompts
    """
    prompts = AIResumePrompts()
    
    return {
        'rewrite': prompts.resume_rewrite(resume_text),
        'role_targeting': prompts.role_targeting(resume_text),
        'linkedin': prompts.linkedin_optimization(resume_text, ['DevOps Engineer', 'SRE', 'Cloud Engineer'])
    }


def prepare_for_application(job_description: str, resume_text: str, company_name: str, position: str) -> dict:
    """
    Generate all prompts needed for a specific job application
    """
    prompts = AIResumePrompts()
    
    return {
        'jd_match': prompts.jd_match_check(job_description, resume_text),
        'cover_letter': prompts.cover_letter_generator(job_description, resume_text, company_name),
        'interview_prep': prompts.interview_prep(position, job_description),
        'proof_projects': prompts.proof_projects(position, job_description)
    }


if __name__ == "__main__":
    # Example usage
    prompts = AIResumePrompts()
    
    sample_resume = """
    DevOps Engineer with 5 years experience.
    Worked with Kubernetes, AWS, and CI/CD pipelines.
    """
    
    print("=== Resume Rewrite Prompt ===")
    print(prompts.resume_rewrite(sample_resume))
    print("\n=== Role Targeting Prompt ===")
    print(prompts.role_targeting(sample_resume))
