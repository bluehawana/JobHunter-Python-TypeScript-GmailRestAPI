"""
Test FactSet job role detection with percentage breakdown
"""

import logging
from cv_templates import CVTemplateManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# FactSet job description
factset_job = """
FactSet creates flexible, open data and software solutions for over 200,000 investment professionals worldwide, providing instant access to financial data and analytics that investors use to make crucial decisions.  At FactSet, our values are the foundation of everything we do. They express how we act and operate, serve as a compass in our decision-making, and play a big role in how we treat each other, our clients, and our communities. We believe that the best ideas can come from anyone, anywhere, at any time, and that curiosity is the key to anticipating our clients' needs and exceeding their expectations.  Cobalt, acquired by FactSet in 2021, is a market-leading portfolio monitoring tool for private capital. Our intuitive technology supports private equity and venture capital clients in collecting, analyzing, and reporting on fund and portfolio company data. By combining Cobalt's nimble, innovative spirit with FactSet's global reach and resources, we deliver critical insights and operational efficiencies to firms worldwide  What You'll Do Lead and mentor a distributed team of engineers in designing, building, and scaling new features and platform enhancements, ensuring quality and performance at every step.Drive integration and deployment of generative AI and machine learning solutions—including LLM-based applications.Oversee architectural decisions and technical direction to ensure sustainable and scalable system design.Collaborate with product, design, and cross-functional teams to accurately scope, define, and deliver complex projects.Foster a team culture of code quality, peer review, and continuous learning.Own agile development ceremonies, operational troubleshooting, and team knowledge-sharing.What We're Looking ForBachelor's or Master's degree in Computer Science or related field, or equivalent experience.5+ years of hands-on experience building web applications in production environments.Strong proficiency in web development across the full stack using modern web development frameworks.Demonstrable experience building, fine-tuning, and integrating generative AI/LLM solutions (OpenAI, Azure AI, AWS Bedrock and Databricks) into production systems and workflows.Experience leading, mentoring, or managing engineering teams, especially within globally distributed organizations.Excellent problem-solving skills and outstanding written and verbal communication.What's In It For YouShape cutting-edge products at the intersection of AI and finance, with FactSet's stability and Cobalt's spirit.Comprehensive health, retirement, and wellness benefits to support total well-being.Flexible work accommodations and a global, innovation-driven team culture.Career growth, dedicated learning time, and access to top-tier AI and cloud technologies.Key Skills and TechnologiesLanguages: Python, TypeScript, JavaScript, C#, SQLPython frameworks: Flask, SQLAlchemyJavaScript frameworks: React, NodeJSDatabases: PostgreSQL, RedisCloud/Infra: AWS (EC2, CloudFormation, RDS, RabbitMQ)Development Tools: Git, Webpack, Docker, Saltstackompany Overview FactSet (NYSE:FDS | NASDAQ:FDS) helps the financial community to see more, think bigger, and work better. Our digital platform and enterprise solutions deliver financial data, analytics, and open technology to more than 8,200 global clients, including over 200,000 individual users. Clients across the buy-side and sell-side, as well as wealth managers, private equity firms, and corporations, achieve more every day with our comprehensive and connected content, flexible next-generation workflow solutions, and client-centric specialized support. As a member of the S&P 500, we are committed to sustainable growth and have been recognized among the Best Places to Work in 2023 by Glassdoor as a Glassdoor Employees' Choice Award winner. Learn more atwww.factset.comand follow us onXandLinkedIn.At FactSet, we celebrate difference of thought, experience, and perspective. Qualified applicants will be considered for employment without regard to characteristics protected by law.
"""

def main():
    manager = CVTemplateManager()
    
    print("=" * 80)
    print("FACTSET JOB ANALYSIS")
    print("=" * 80)
    
    # Detect role
    detected_role = manager.analyze_job_role(factset_job)
    print(f"\n✓ Detected Role: {detected_role}")
    
    # Get all percentages
    print("\n" + "=" * 80)
    print("ALL ROLE PERCENTAGES")
    print("=" * 80)
    percentages = manager.get_role_percentages(factset_job)
    
    # Sort by percentage descending
    sorted_percentages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    for role, percentage in sorted_percentages:
        if percentage > 0:
            bar = "█" * int(percentage / 2)  # Visual bar
            print(f"{role:30s}: {percentage:5.1f}% {bar}")
    
    # Get role breakdown (>5%)
    print("\n" + "=" * 80)
    print("SIGNIFICANT ROLES (>5%)")
    print("=" * 80)
    breakdown = manager.get_role_breakdown(factset_job, threshold=5.0)
    
    for role, percentage in breakdown:
        print(f"  • {role:30s}: {percentage:5.1f}%")
    
    # Get role scores for debugging
    print("\n" + "=" * 80)
    print("RAW WEIGHTED SCORES")
    print("=" * 80)
    scores = manager.get_role_scores(factset_job)
    
    # Sort by score descending
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for role, score in sorted_scores:
        if score > 0:
            print(f"{role:30s}: {score:6.2f}")
    
    # Analysis summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    if breakdown:
        primary_role, primary_percentage = breakdown[0]
        print(f"Primary Role: {primary_role} ({primary_percentage:.1f}%)")
        
        if primary_percentage < 50:
            print(f"\n⚠️  WARNING: This is a MIXED ROLE job!")
            print(f"   The primary role only accounts for {primary_percentage:.1f}% of the job.")
            print(f"   This job has responsibilities across multiple areas:")
            for role, pct in breakdown[:3]:
                print(f"     - {role}: {pct:.1f}%")
        else:
            print(f"\n✓ Clear role match: {primary_role} is the dominant role")
        
        # Check for AI mentions
        if 'ai_product_engineer' in dict(breakdown):
            ai_pct = dict(breakdown)['ai_product_engineer']
            print(f"\n🤖 AI Component: {ai_pct:.1f}%")
            if ai_pct < 50:
                print(f"   This job involves AI integration/usage, not AI product engineering")
        
        # Check for fintech
        if 'devops_fintech' in dict(breakdown):
            fintech_pct = dict(breakdown)['devops_fintech']
            print(f"\n💰 FinTech Component: {fintech_pct:.1f}%")

if __name__ == '__main__':
    main()
