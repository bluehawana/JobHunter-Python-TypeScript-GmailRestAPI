"""
Test for Meltwater Software Engineer Job Classification
Ensures the system correctly classifies software engineering roles with AI integration
"""

import pytest
from cv_templates import CVTemplateManager


class TestMeltwaterJobClassification:
    """Test classification of the Meltwater Software Engineer job"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.template_manager = CVTemplateManager()
        
        # The actual Meltwater job description
        self.meltwater_job = """
        As a Software Engineer with the information retrieval team at Meltwater you will be building petabyte-scale search and analytics systems using Elasticsearch running on AWS. Every day, we add 1.3B new documents into our search platform and process over 6B engagement activities to provide the most complete dataset possible. This data fuels our products with robust insights that span key areas that include media, social, influencer, sales, and consumer intelligence.

        In addition to working with large-scale distributed systems, you will also have the opportunity to work on cutting-edge vector search technologies and explore use cases powered by Large Language Models (LLMs). These initiatives enable semantic search capabilities, enhanced content understanding, and more intelligent data discovery experiences for our users.

        Our culture is based on a fundamental belief in people with a passion for learning new things and a desire to help those around you. We are strong believers in team autonomy, DevOps culture and continuous delivery. Meltwater development teams fully own and operate their subsystems and infrastructure and run on-call rotations.

        We run on AWS and are heavy users of AWS services, Elasticsearch, Cassandra, Terraform, Docker; with a sprinkling of other database and messaging technologies depending on the need.

        For this role, you will benefit by having some experience with search engines, big data analytics, infrastructure, systems engineering and distributed systems. Experience with vector search and applied use of Large Language Models (LLMs) is also a plus. In our team you will get an opportunity to explore and push the technologies we use to their limits. This sometimes requires low level modifications to open-source libraries, other times it involves combining two existing technologies in an innovative way.

        On the software side we're heavy on Java and Kotlin, with some Spring, RxJava and plenty of microservices thrown in. We use Python for data science, machine learning and linear optimization purposes. Long experience with Java or Python is however not a requirement, instead we prefer an engineer with a history of rapidly acquiring new skills.

        For this position we are looking for Software Engineers that want to further grow in an organization based on collaboration across team and country boundaries. With the massive production scale of our systems, small decisions you make may have a big impact on our product and our many customers. If you get excited when talking about distributed systems at scale, or innovating on new ways to gain insights from all the world's information then you will love working with us.

        What You'll Bring:
        At least 3 years' experience in software development and distributed systems
        Experience with cloud services, preferably AWS (EC2, S3, SQS)
        Experience with Java and/or Kotlin
        You are curious and take pleasure in learning new things
        You enjoy solving problems with others
        You can carry a conversation in English
        You are eligible to work in Sweden

        Nice to have Skills and Experience:
        Experience working with Elasticsearch
        Knowledge of vector databases and embedding models
        Experience of applying LLMs / Gen AI to use-cases
        """
    
    def test_meltwater_job_classification(self):
        """Test that Meltwater job is correctly classified as backend_developer"""
        role_category = self.template_manager.analyze_job_role(self.meltwater_job)
        
        # Should be classified as backend_developer, not ai_product_engineer
        assert role_category == 'backend_developer', f"Expected backend_developer, got {role_category}"
    
    def test_meltwater_job_percentages(self):
        """Test that percentage distribution is correct for Meltwater job"""
        percentages = self.template_manager.get_role_percentages(self.meltwater_job)
        
        backend_pct = percentages.get('backend_developer', 0)
        ai_pct = percentages.get('ai_product_engineer', 0)
        devops_pct = percentages.get('devops_cloud', 0)
        
        # Backend should be the highest percentage
        assert backend_pct > ai_pct, f"Backend ({backend_pct:.1f}%) should be higher than AI ({ai_pct:.1f}%)"
        assert backend_pct > devops_pct, f"Backend ({backend_pct:.1f}%) should be higher than DevOps ({devops_pct:.1f}%)"
        
        # Backend should be at least 50% (dominant role)
        assert backend_pct >= 50.0, f"Backend percentage ({backend_pct:.1f}%) should be at least 50%"
        
        # AI should be relatively low (integration, not core development)
        assert ai_pct < 20.0, f"AI percentage ({ai_pct:.1f}%) should be less than 20% (integration role)"
    
    def test_meltwater_job_role_breakdown(self):
        """Test role breakdown for Meltwater job"""
        breakdown = self.template_manager.get_role_breakdown(self.meltwater_job, threshold=5.0)
        
        # Should have multiple roles but backend_developer should be first
        assert len(breakdown) >= 2, "Should detect multiple role aspects"
        assert breakdown[0][0] == 'backend_developer', f"Top role should be backend_developer, got {breakdown[0][0]}"
        
        # Backend should be significantly higher than others
        backend_pct = breakdown[0][1]
        second_pct = breakdown[1][1] if len(breakdown) > 1 else 0
        
        assert backend_pct > second_pct * 2, f"Backend ({backend_pct:.1f}%) should be at least 2x higher than second role ({second_pct:.1f}%)"
    
    def test_ai_integration_vs_ai_development_keywords(self):
        """Test that AI integration keywords are properly weighted vs AI development keywords"""
        from job_analyzer import JobAnalyzer
        
        analyzer = JobAnalyzer()
        role_indicators = analyzer.identify_role_indicators(self.meltwater_job, self.template_manager.ROLE_CATEGORIES)
        
        # Check backend keywords
        backend_keywords = role_indicators.get('backend_developer', {})
        ai_keywords = role_indicators.get('ai_product_engineer', {})
        
        # Backend should have more keyword matches
        backend_total = sum(backend_keywords.values())
        ai_total = sum(ai_keywords.values())
        
        assert backend_total > ai_total, f"Backend keywords ({backend_total}) should outnumber AI keywords ({ai_total})"
        
        # Verify specific AI integration keywords are detected in backend category
        integration_keywords = ['vector search', 'semantic search', 'applied use of', 'use cases powered by']
        found_integration_keywords = [kw for kw in integration_keywords if kw in backend_keywords]
        
        assert len(found_integration_keywords) > 0, f"Should detect AI integration keywords in backend category: {found_integration_keywords}"
    
    def test_software_engineering_context_detection(self):
        """Test that the system recognizes this as software engineering with AI integration"""
        percentages = self.template_manager.get_role_percentages(self.meltwater_job)
        
        # Software engineering roles (backend + devops) should dominate
        software_eng_total = percentages.get('backend_developer', 0) + percentages.get('devops_cloud', 0)
        ai_pct = percentages.get('ai_product_engineer', 0)
        
        assert software_eng_total > ai_pct * 3, f"Software engineering roles ({software_eng_total:.1f}%) should be 3x higher than AI ({ai_pct:.1f}%)"
        
        # The job should be recognized as software engineering with AI integration, not AI development
        role_category = self.template_manager.analyze_job_role(self.meltwater_job)
        assert role_category in ['backend_developer', 'devops_cloud'], f"Should be classified as software engineering role, got {role_category}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])