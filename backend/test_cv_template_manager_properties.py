"""
Property-Based Tests for CVTemplateManager
Tests universal properties of template selection and diversity
"""

import pytest
from hypothesis import given, settings, strategies as st
from cv_templates import CVTemplateManager


# Test generators
@st.composite
def diverse_job_descriptions_generator(draw):
    """Generate diverse job descriptions for different role types"""
    
    job_templates = {
        'android_developer': [
            "We are looking for an Android Developer with Kotlin and Java experience. "
            "You will build mobile apps using Android SDK and AOSP. "
            "Experience with Jetpack and mobile development is required.",
            
            "Android Platform Engineer needed. Strong Kotlin skills required. "
            "Work on automotive infotainment systems using Android SDK. "
            "Mobile app development experience essential.",
            
            "Senior Android Developer position. Build cutting-edge mobile applications. "
            "Kotlin, Java, Android SDK, and APK development experience required."
        ],
        
        'devops_cloud': [
            "DevOps Engineer position. Must have AWS, Kubernetes, and Docker experience. "
            "Terraform and Infrastructure as Code knowledge required. "
            "CI/CD pipeline experience essential.",
            
            "Cloud Engineer needed. Strong Kubernetes and AWS skills. "
            "Experience with Docker, Helm, and ArgoCD required. "
            "DevOps practices and cloud infrastructure expertise needed.",
            
            "Senior DevOps role. Build and maintain cloud infrastructure. "
            "AWS, Azure, Kubernetes, Terraform, and CI/CD experience required."
        ],
        
        'incident_management_sre': [
            "Site Reliability Engineer position. On-call support and incident management. "
            "Experience with monitoring, observability, and MTTR reduction required. "
            "PagerDuty and production support experience essential.",
            
            "SRE needed. Strong incident management and monitoring skills. "
            "Experience with observability tools and on-call rotations. "
            "Production support and reliability engineering required.",
            
            "Senior SRE role. Manage incidents and improve system reliability. "
            "Monitoring, observability, incident management, and on-call experience needed."
        ],
        
        'fullstack_developer': [
            "Full-stack Developer position. React and TypeScript frontend experience. "
            "Backend development with Node.js or Python required. "
            "Web application development and full-stack skills essential.",
            
            "Fullstack Engineer needed. Strong React and JavaScript skills. "
            "Experience with backend APIs and web development. "
            "Full-stack development and TypeScript knowledge required.",
            
            "Senior Full-stack Developer. Build modern web applications. "
            "React, Vue, or Angular frontend plus backend API development. "
            "Full-stack experience and web development skills needed."
        ],
        
        'backend_developer': [
            "Backend Developer position. Strong Java and Spring Boot experience. "
            "Build microservices and RESTful APIs using Hibernate and JPA. "
            "Backend development and server-side programming required.",
            
            "Java Backend Engineer needed. Spring Framework and microservices. "
            "API development and backend programming experience essential. "
            "Java, Spring Boot, and server-side development skills required.",
            
            "Senior Backend Developer. Build scalable backend systems. "
            "Java, Spring Boot, microservices, and API development experience needed."
        ],
        
        'ai_product_engineer': [
            "AI Product Engineer position. Build and train machine learning models. "
            "Experience with PyTorch, TensorFlow, and model training required. "
            "RAG, vector databases, and MLOps experience essential.",
            
            "ML Engineer needed. Train and deploy deep learning models. "
            "Experience with model training, fine-tuning, and MLOps. "
            "PyTorch, TensorFlow, and neural networks expertise required.",
            
            "Senior AI Engineer. Build AI systems and train models. "
            "Machine learning, model training, RAG, and embeddings experience needed."
        ]
    }
    
    # Select a random role type
    role_type = draw(st.sampled_from(list(job_templates.keys())))
    
    # Select a random job description for that role
    job_description = draw(st.sampled_from(job_templates[role_type]))
    
    return role_type, job_description


@st.composite
def diverse_job_set_generator(draw, min_roles=3, max_roles=6):
    """Generate a set of job descriptions with guaranteed role diversity"""
    
    all_role_types = [
        'android_developer', 'devops_cloud', 'incident_management_sre',
        'fullstack_developer', 'backend_developer', 'ai_product_engineer'
    ]
    
    # Select how many different roles we want
    num_roles = draw(st.integers(min_value=min_roles, max_value=min(max_roles, len(all_role_types))))
    
    # Select which roles (ensuring uniqueness)
    selected_roles = draw(st.lists(
        st.sampled_from(all_role_types),
        min_size=num_roles,
        max_size=num_roles,
        unique=True
    ))
    
    # Generate one job description for each selected role
    job_descriptions = []
    for role_type in selected_roles:
        # Use the diverse_job_descriptions_generator but filter for the specific role
        attempts = 0
        while attempts < 20:
            generated_role, job_desc = draw(diverse_job_descriptions_generator())
            if generated_role == role_type:
                job_descriptions.append((role_type, job_desc))
                break
            attempts += 1
    
    return job_descriptions


class TestCVTemplateManagerDiversityProperties:
    """Property-based tests for template diversity"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CVTemplateManager()
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_different_roles_different_templates(self, data):
        """
        Property: For any set of diverse job descriptions (Android, DevOps, SRE, Full-stack),
                 the system should select different templates, not defaulting to a single template
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9
        """
        # Generate multiple diverse job descriptions with GUARANTEED diversity
        job_set = data.draw(diverse_job_set_generator(min_roles=3, max_roles=6))
        
        # Skip if we didn't get enough diverse jobs
        if len(job_set) < 2:
            return
        
        # Analyze each job description
        detected_roles = []
        expected_roles = []
        for expected_role, job_desc in job_set:
            detected_role = self.manager.analyze_job_role(job_desc)
            detected_roles.append(detected_role)
            expected_roles.append(expected_role)
        
        # Check that we got different templates for different role types
        unique_detected_roles = set(detected_roles)
        
        # The system should not default to a single template for all jobs
        assert len(unique_detected_roles) > 1, \
            f"System should select different templates for diverse jobs, but got only: {unique_detected_roles}"
        
        # At least 50% of the jobs should get different templates
        diversity_ratio = len(unique_detected_roles) / len(detected_roles)
        assert diversity_ratio >= 0.5, \
            f"Template diversity ratio should be at least 50%, got {diversity_ratio:.1%}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_android_jobs_select_android_template(self, data):
        """
        Property: For any Android job description, the system should select
                 the Android template (not default to a generic template)
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9, 2.2
        """
        # Generate an Android job description
        _, android_job = data.draw(diverse_job_descriptions_generator())
        
        # Ensure it's actually an Android job by checking keywords
        if 'android' not in android_job.lower() and 'kotlin' not in android_job.lower():
            # Skip if the generator didn't produce an Android job
            return
        
        detected_role = self.manager.analyze_job_role(android_job)
        
        # Should select Android template for Android jobs
        assert detected_role == 'android_developer', \
            f"Android job should select 'android_developer' template, got '{detected_role}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_devops_jobs_select_devops_template(self, data):
        """
        Property: For any DevOps job description, the system should select
                 a DevOps-related template (not default to a generic template)
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9, 2.3
        """
        # Generate a DevOps job description
        _, devops_job = data.draw(diverse_job_descriptions_generator())
        
        # Ensure it's actually a DevOps job by checking keywords
        if 'devops' not in devops_job.lower() and 'kubernetes' not in devops_job.lower():
            # Skip if the generator didn't produce a DevOps job
            return
        
        detected_role = self.manager.analyze_job_role(devops_job)
        
        # Should select a DevOps-related template
        devops_templates = ['devops_cloud', 'devops_fintech', 'cloud_engineer', 'platform_engineer']
        assert detected_role in devops_templates, \
            f"DevOps job should select a DevOps template, got '{detected_role}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_sre_jobs_select_sre_template(self, data):
        """
        Property: For any SRE/incident management job description, the system should select
                 the SRE template (not default to a generic template)
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9, 2.4
        """
        # Generate an SRE job description
        _, sre_job = data.draw(diverse_job_descriptions_generator())
        
        # Ensure it's actually an SRE job by checking keywords
        if 'sre' not in sre_job.lower() and 'incident' not in sre_job.lower():
            # Skip if the generator didn't produce an SRE job
            return
        
        detected_role = self.manager.analyze_job_role(sre_job)
        
        # Should select SRE template for SRE jobs
        assert detected_role == 'incident_management_sre', \
            f"SRE job should select 'incident_management_sre' template, got '{detected_role}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_fullstack_jobs_select_fullstack_template(self, data):
        """
        Property: For any full-stack job description, the system should select
                 the full-stack template (not default to a generic template)
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9, 2.5
        """
        # Generate a full-stack job description
        _, fullstack_job = data.draw(diverse_job_descriptions_generator())
        
        # Ensure it's actually a full-stack job by checking keywords
        if 'full' not in fullstack_job.lower() and 'fullstack' not in fullstack_job.lower():
            # Skip if the generator didn't produce a full-stack job
            return
        
        detected_role = self.manager.analyze_job_role(fullstack_job)
        
        # Should select full-stack template for full-stack jobs
        assert detected_role == 'fullstack_developer', \
            f"Full-stack job should select 'fullstack_developer' template, got '{detected_role}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_consistent_for_same_job(self, data):
        """
        Property: For any job description, analyzing it multiple times should
                 consistently select the same template
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9
        """
        # Generate a job description
        _, job_desc = data.draw(diverse_job_descriptions_generator())
        
        # Analyze the same job multiple times
        detected_roles = []
        for _ in range(3):
            detected_role = self.manager.analyze_job_role(job_desc)
            detected_roles.append(detected_role)
        
        # All detections should be the same
        assert len(set(detected_roles)) == 1, \
            f"Same job should consistently select same template, got: {detected_roles}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_diversity_no_always_default_template(self, data):
        """
        Property: The system should not always return the same default template
                 regardless of job content
        Feature: intelligent-cv-template-selection, Property 4: Template Diversity
        Validates: Requirements 2.9
        """
        # Generate multiple diverse job descriptions with guaranteed diversity
        job_set = data.draw(diverse_job_set_generator(min_roles=3, max_roles=5))
        
        # Skip if we didn't get enough diverse jobs
        if len(job_set) < 2:
            return
        
        # Analyze all jobs
        detected_roles = [
            self.manager.analyze_job_role(job_desc)
            for _, job_desc in job_set
        ]
        
        # Should not all be the same template
        unique_roles = set(detected_roles)
        assert len(unique_roles) > 1, \
            f"System should not default to single template for all jobs, got only: {unique_roles}"


@st.composite
def mixed_role_job_generator(draw):
    """Generate job descriptions that should trigger mixed role warnings"""
    
    # Mixed role job templates that combine multiple role types
    mixed_job_templates = [
        # FactSet-style: Fullstack + AI + FinTech + Leadership
        """
        Lead and mentor a distributed team of engineers in designing, building, and scaling new features.
        Drive integration and deployment of generative AI and machine learning solutions—including LLM-based applications.
        Strong proficiency in web development across the full stack using modern web development frameworks.
        Experience with React, TypeScript, JavaScript, Python, Flask, SQLAlchemy.
        Demonstrable experience building, fine-tuning, and integrating generative AI/LLM solutions (OpenAI, Azure AI, AWS Bedrock).
        Shape cutting-edge products at the intersection of AI and finance, with FactSet's stability.
        Experience with financial data, analytics, and trading systems.
        Cloud/Infra: AWS (EC2, CloudFormation, RDS), Docker, Kubernetes.
        """,
        
        # Software Engineering + AI Integration + DevOps
        """
        Senior Software Engineer position. We need someone with strong React and TypeScript
        experience for frontend work, plus Python and Flask for backend APIs. You'll also
        help with our Kubernetes deployment and CI/CD pipelines. Experience integrating
        AI features using OpenAI API is a plus. AWS, Docker, and infrastructure knowledge required.
        """,
        
        # Fullstack + DevOps + AI + Leadership
        """
        Technical Lead role combining fullstack development with DevOps responsibilities.
        Build modern web applications using React, Vue, TypeScript, and Node.js.
        Manage cloud infrastructure with AWS, Kubernetes, and Terraform.
        Integrate AI capabilities using LLM APIs and generative AI solutions.
        Lead a team of engineers and drive technical decisions.
        Experience with CI/CD, monitoring, and production support required.
        """,
        
        # Backend + AI + FinTech + Platform
        """
        Platform Engineer at a financial technology company. Build scalable backend systems
        using Java, Spring Boot, and microservices architecture. Integrate machine learning
        models and AI solutions into trading platforms. Experience with financial data,
        payment processing, and compliance required. Knowledge of Kubernetes, Docker,
        and cloud platforms essential.
        """,
        
        # Android + AI + Platform + Leadership
        """
        Senior Android Platform Lead. Build mobile applications using Kotlin and Android SDK.
        Integrate AI-powered features and machine learning capabilities into mobile apps.
        Lead platform architecture decisions and mentor junior developers.
        Experience with AOSP, mobile development, and AI/ML integration required.
        Knowledge of cloud platforms and backend systems is a plus.
        """,
        
        # DevOps + AI + Fullstack + SRE
        """
        Site Reliability Engineer with fullstack development responsibilities.
        Build monitoring and observability tools using React and Python.
        Integrate AI-powered alerting and incident management systems.
        Manage Kubernetes clusters, AWS infrastructure, and CI/CD pipelines.
        On-call support and production troubleshooting experience required.
        Experience with machine learning and AI operations is preferred.
        """
    ]
    
    # Select a random mixed role job description
    job_description = draw(st.sampled_from(mixed_job_templates))
    
    return job_description


@st.composite
def clear_role_job_generator(draw):
    """Generate job descriptions with clear primary roles (>50%)"""
    
    clear_role_templates = {
        'android_developer': [
            """
            Android Developer position. Strong Kotlin and Java experience required.
            Build mobile applications using Android SDK and AOSP.
            Experience with Jetpack, mobile development, and APK creation essential.
            Android platform knowledge and mobile app development skills needed.
            """,
            """
            Senior Android Engineer. Work on automotive infotainment systems.
            Kotlin, Java, Android SDK, and mobile development experience required.
            AOSP knowledge and Android platform expertise essential.
            """
        ],
        
        'devops_cloud': [
            """
            DevOps Engineer position. AWS, Kubernetes, and Docker experience required.
            Terraform, Infrastructure as Code, and CI/CD pipeline knowledge essential.
            Cloud infrastructure management and DevOps practices needed.
            """,
            """
            Cloud Engineer role. Strong Kubernetes, AWS, and Docker skills required.
            Experience with Helm, ArgoCD, and cloud infrastructure management.
            DevOps practices and infrastructure automation expertise needed.
            """
        ],
        
        'fullstack_developer': [
            """
            Full-stack Developer position. React and TypeScript frontend experience required.
            Backend development with Node.js and Python essential.
            Web application development and fullstack skills needed.
            """,
            """
            Fullstack Engineer role. Strong React, JavaScript, and web development skills.
            Experience with backend APIs and full-stack development required.
            TypeScript and modern web frameworks knowledge essential.
            """
        ]
    }
    
    # Select a random role type
    role_type = draw(st.sampled_from(list(clear_role_templates.keys())))
    
    # Select a random job description for that role
    job_description = draw(st.sampled_from(clear_role_templates[role_type]))
    
    return role_type, job_description


class TestCVTemplateManagerMixedRoleProperties:
    """Property-based tests for mixed role warning functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CVTemplateManager()
    
    @settings(max_examples=100)
    @given(mixed_role_job_generator())
    def test_mixed_role_warning_triggered_for_mixed_jobs(self, mixed_job_desc):
        """
        Property: For any job analysis where the highest role percentage is below 50%,
                 the system should log a warning about mixed role composition
        Feature: intelligent-cv-template-selection, Property 20: Mixed Role Warning
        Validates: Requirements 10.5
        """
        # Capture log messages
        import logging
        import io
        
        # Create a string buffer to capture log output
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.WARNING)
        
        # Get the logger and add our handler
        logger = logging.getLogger('cv_templates')
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        
        try:
            # Get role breakdown (this should trigger the warning if primary role < 50%)
            breakdown = self.manager.get_role_breakdown(mixed_job_desc, threshold=5.0)
            
            # Get the log output
            log_output = log_capture.getvalue()
            
            # Check if we have a breakdown and if primary role is below 50%
            if breakdown and breakdown[0][1] < 50:
                # Should have logged a mixed role warning
                assert "Mixed role composition detected" in log_output, \
                    f"Expected mixed role warning for job with primary role {breakdown[0][1]:.1f}%, " \
                    f"but no warning was logged. Log output: '{log_output}'"
                
                # Verify the warning contains the expected information
                assert f"Primary role '{breakdown[0][0]}'" in log_output, \
                    f"Warning should mention the primary role '{breakdown[0][0]}'"
                
                assert f"{breakdown[0][1]:.1f}%" in log_output, \
                    f"Warning should mention the percentage {breakdown[0][1]:.1f}%"
            
            # If primary role is >= 50%, no warning should be logged
            elif breakdown and breakdown[0][1] >= 50:
                assert "Mixed role composition detected" not in log_output, \
                    f"Should not log mixed role warning for job with primary role {breakdown[0][1]:.1f}%, " \
                    f"but warning was logged: '{log_output}'"
        
        finally:
            # Clean up: remove our handler
            logger.removeHandler(handler)
            handler.close()
    
    @settings(max_examples=100)
    @given(st.data())
    def test_mixed_role_warning_not_triggered_for_clear_roles(self, data):
        """
        Property: For any job analysis where the highest role percentage is 50% or above,
                 the system should NOT log a mixed role warning
        Feature: intelligent-cv-template-selection, Property 20: Mixed Role Warning
        Validates: Requirements 10.5
        """
        # Generate a clear role job description
        expected_role, clear_job_desc = data.draw(clear_role_job_generator())
        
        # Capture log messages
        import logging
        import io
        
        # Create a string buffer to capture log output
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.WARNING)
        
        # Get the logger and add our handler
        logger = logging.getLogger('cv_templates')
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        
        try:
            # Get role breakdown
            breakdown = self.manager.get_role_breakdown(clear_job_desc, threshold=5.0)
            
            # Get the log output
            log_output = log_capture.getvalue()
            
            # If we have a breakdown and primary role is >= 50%, no warning should be logged
            if breakdown and breakdown[0][1] >= 50:
                assert "Mixed role composition detected" not in log_output, \
                    f"Should not log mixed role warning for job with primary role {breakdown[0][1]:.1f}%, " \
                    f"but warning was logged: '{log_output}'"
        
        finally:
            # Clean up: remove our handler
            logger.removeHandler(handler)
            handler.close()
    
    @settings(max_examples=100)
    @given(st.text(min_size=50, max_size=1000))
    def test_mixed_role_warning_threshold_consistency(self, job_description):
        """
        Property: For any job description, the mixed role warning should be triggered
                 consistently based on the 50% threshold
        Feature: intelligent-cv-template-selection, Property 20: Mixed Role Warning
        Validates: Requirements 10.5
        """
        # Skip job descriptions that are too short or contain only whitespace
        if len(job_description.strip()) < 20:
            return
        
        # Capture log messages
        import logging
        import io
        
        # Create a string buffer to capture log output
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.WARNING)
        
        # Get the logger and add our handler
        logger = logging.getLogger('cv_templates')
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        
        try:
            # Get role breakdown
            breakdown = self.manager.get_role_breakdown(job_description, threshold=5.0)
            
            # Get the log output
            log_output = log_capture.getvalue()
            
            # Check consistency: warning should be present if and only if primary role < 50%
            has_warning = "Mixed role composition detected" in log_output
            
            if breakdown and len(breakdown) > 0:
                primary_percentage = breakdown[0][1]
                should_have_warning = primary_percentage < 50
                
                assert has_warning == should_have_warning, \
                    f"Mixed role warning inconsistency: primary role is {primary_percentage:.1f}%, " \
                    f"should_have_warning={should_have_warning}, has_warning={has_warning}, " \
                    f"log_output='{log_output}'"
        
        finally:
            # Clean up: remove our handler
            logger.removeHandler(handler)
            handler.close()


@st.composite
def percentage_distribution_generator(draw):
    """Generate job descriptions with known percentage distributions"""
    
    # Create job descriptions with controlled keyword distributions
    job_templates = {
        'clear_android': {
            'description': """
            Android Developer position. Strong Kotlin and Java experience required.
            Build mobile applications using Android SDK and AOSP.
            Experience with Jetpack, mobile development, and APK creation essential.
            Android platform knowledge and mobile app development skills needed.
            Kotlin programming and Android SDK expertise required.
            """,
            'expected_primary': 'android_developer'
        },
        
        'clear_fullstack': {
            'description': """
            Full-stack Developer position. React and TypeScript frontend experience required.
            Backend development with Node.js and Python essential.
            Web application development and fullstack skills needed.
            React components and TypeScript interfaces required.
            Fullstack engineering and web development expertise essential.
            """,
            'expected_primary': 'fullstack_developer'
        },
        
        'clear_devops': {
            'description': """
            DevOps Engineer position. AWS, Kubernetes, and Docker experience required.
            Terraform, Infrastructure as Code, and CI/CD pipeline knowledge essential.
            Cloud infrastructure management and DevOps practices needed.
            Kubernetes orchestration and AWS cloud services required.
            DevOps automation and infrastructure expertise essential.
            """,
            'expected_primary': 'devops_cloud'
        },
        
        'clear_backend': {
            'description': """
            Backend Developer position. Strong Java and Spring Boot experience required.
            Build microservices and RESTful APIs using Hibernate and JPA.
            Backend development and server-side programming essential.
            Java programming and Spring Framework expertise required.
            Microservices architecture and API development needed.
            """,
            'expected_primary': 'backend_developer'
        },
        
        'mixed_fullstack_devops': {
            'description': """
            Senior Software Engineer position. We need someone with strong React and TypeScript
            experience for frontend work, plus Python and Flask for backend APIs. You'll also
            help with our Kubernetes deployment and CI/CD pipelines. Fullstack development
            experience required. DevOps knowledge is a plus.
            """,
            'expected_primary': 'fullstack_developer'  # Should be primary due to more keywords
        },
        
        'mixed_devops_backend': {
            'description': """
            Platform Engineer role. Build backend services using Java and Spring Boot.
            Manage Kubernetes clusters and AWS infrastructure. CI/CD pipeline experience
            required. DevOps practices and cloud infrastructure knowledge essential.
            Backend development and microservices architecture needed.
            """,
            'expected_primary': 'devops_cloud'  # Should be primary due to more keywords
        }
    }
    
    # Select a random job template
    job_key = draw(st.sampled_from(list(job_templates.keys())))
    job_data = job_templates[job_key]
    
    return job_data['description'], job_data['expected_primary']


class TestCVTemplateManagerPercentageProperties:
    """Property-based tests for percentage-based template selection"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CVTemplateManager()
    
    @settings(max_examples=100)
    @given(percentage_distribution_generator())
    def test_template_selection_by_highest_percentage(self, job_data):
        """
        Property: For any percentage distribution, the selected template role should be
                 the role with the maximum percentage score
        Feature: intelligent-cv-template-selection, Property 22: Template Selection by Highest Percentage
        Validates: Requirements 10.7
        """
        job_description, expected_primary = job_data
        
        # Get role percentages
        role_percentages = self.manager.get_role_percentages(job_description)
        
        # Find the role with the highest percentage
        if role_percentages:
            max_percentage_role = max(role_percentages, key=role_percentages.get)
            max_percentage = role_percentages[max_percentage_role]
        else:
            max_percentage_role = None
            max_percentage = 0
        
        # Get the actual selected template
        selected_role = self.manager.analyze_job_role(job_description)
        
        # The selected role should be the one with the highest percentage
        assert selected_role == max_percentage_role, \
            f"Selected role '{selected_role}' should match the role with highest percentage '{max_percentage_role}' " \
            f"({max_percentage:.1f}%). Role percentages: {role_percentages}"
        
        # Additional validation: the selected role should have a meaningful percentage
        if max_percentage_role and max_percentage_role in role_percentages:
            selected_percentage = role_percentages[selected_role]
            assert selected_percentage > 0, \
                f"Selected role '{selected_role}' should have a positive percentage, got {selected_percentage:.1f}%"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_selection_consistency_with_percentages(self, data):
        """
        Property: For any job description, the template selection should be consistent
                 with the percentage-based ranking
        Feature: intelligent-cv-template-selection, Property 22: Template Selection by Highest Percentage
        Validates: Requirements 10.7
        """
        # Generate a job description
        job_description, _ = data.draw(percentage_distribution_generator())
        
        # Get role breakdown (sorted by percentage descending)
        role_breakdown = self.manager.get_role_breakdown(job_description, threshold=0.0)
        
        # Get the selected template
        selected_role = self.manager.analyze_job_role(job_description)
        
        # If we have a breakdown, the selected role should be the top role
        if role_breakdown:
            top_role, top_percentage = role_breakdown[0]
            
            # The selected role should match the top role from percentage breakdown
            assert selected_role == top_role, \
                f"Selected role '{selected_role}' should match the top role from breakdown '{top_role}' " \
                f"({top_percentage:.1f}%). Full breakdown: {role_breakdown}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_selection_ignores_zero_percentages(self, data):
        """
        Property: For any job description, roles with 0% should not be selected
                 even if they appear in the role categories
        Feature: intelligent-cv-template-selection, Property 22: Template Selection by Highest Percentage
        Validates: Requirements 10.7
        """
        # Generate a job description
        job_description, _ = data.draw(percentage_distribution_generator())
        
        # Get role percentages
        role_percentages = self.manager.get_role_percentages(job_description)
        
        # Get the selected template
        selected_role = self.manager.analyze_job_role(job_description)
        
        # The selected role should not have 0% (unless all roles have 0%)
        selected_percentage = role_percentages.get(selected_role, 0)
        
        # Check if all roles have 0%
        all_zero = all(percentage == 0 for percentage in role_percentages.values())
        
        if not all_zero:
            assert selected_percentage > 0, \
                f"Selected role '{selected_role}' should not have 0% when other roles have positive percentages. " \
                f"Selected percentage: {selected_percentage:.1f}%, All percentages: {role_percentages}"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_selection_respects_percentage_ordering(self, data):
        """
        Property: For any job description with multiple significant roles,
                 the selected template should correspond to the role with the highest percentage
        Feature: intelligent-cv-template-selection, Property 22: Template Selection by Highest Percentage
        Validates: Requirements 10.7
        """
        # Generate a job description
        job_description, _ = data.draw(percentage_distribution_generator())
        
        # Get role percentages
        role_percentages = self.manager.get_role_percentages(job_description)
        
        # Filter out roles with 0% and sort by percentage descending
        significant_roles = [
            (role, percentage) 
            for role, percentage in role_percentages.items() 
            if percentage > 0
        ]
        significant_roles.sort(key=lambda x: x[1], reverse=True)
        
        # Get the selected template
        selected_role = self.manager.analyze_job_role(job_description)
        
        # If we have significant roles, the selected role should be the top one
        if significant_roles:
            top_role, top_percentage = significant_roles[0]
            
            assert selected_role == top_role, \
                f"Selected role '{selected_role}' should be the role with highest percentage '{top_role}' " \
                f"({top_percentage:.1f}%). Significant roles: {significant_roles}"
        
        # If no significant roles, should fall back to default
        else:
            # Default fallback should be used
            assert selected_role in self.manager.ROLE_CATEGORIES, \
                f"When no significant roles found, should select a valid fallback role, got '{selected_role}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_template_selection_handles_ties_consistently(self, data):
        """
        Property: For any job description where multiple roles have the same highest percentage,
                 the system should consistently select one of them (deterministic tie-breaking)
        Feature: intelligent-cv-template-selection, Property 22: Template Selection by Highest Percentage
        Validates: Requirements 10.7
        """
        # Generate a job description
        job_description, _ = data.draw(percentage_distribution_generator())
        
        # Analyze the same job multiple times to check consistency
        selected_roles = []
        for _ in range(3):
            selected_role = self.manager.analyze_job_role(job_description)
            selected_roles.append(selected_role)
        
        # All selections should be the same (deterministic)
        assert len(set(selected_roles)) == 1, \
            f"Template selection should be deterministic for the same job description, " \
            f"but got different results: {selected_roles}"
        
        # The selected role should have the maximum percentage
        role_percentages = self.manager.get_role_percentages(job_description)
        selected_role = selected_roles[0]
        selected_percentage = role_percentages.get(selected_role, 0)
        max_percentage = max(role_percentages.values()) if role_percentages else 0
        
        assert selected_percentage == max_percentage, \
            f"Selected role '{selected_role}' should have the maximum percentage. " \
            f"Selected: {selected_percentage:.1f}%, Maximum: {max_percentage:.1f}%, " \
            f"All percentages: {role_percentages}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
