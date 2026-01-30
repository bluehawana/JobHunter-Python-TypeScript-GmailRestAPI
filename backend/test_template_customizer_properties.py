"""
Property-Based Tests for TemplateCustomizer
Tests universal properties of placeholder replacement and template customization
"""

import pytest
from hypothesis import given, settings, strategies as st
import re
from template_customizer import TemplateCustomizer


# Test generators
@st.composite
def template_with_placeholders_generator(draw):
    """Generate templates with various placeholder patterns"""
    
    # Actual placeholder names used by TemplateCustomizer
    placeholder_names = [
        'COMPANY_NAME', 'COMPANY_NAME_PLACEHOLDER', 'JOB_TITLE', 'JOB_TITLE_PLACEHOLDER',
        'ROLE_TITLE', 'ROLE_TITLE_PLACEHOLDER', 'Position'
    ]
    
    # Select some placeholders to include
    num_placeholders = draw(st.integers(min_value=1, max_value=4))
    selected_placeholders = draw(st.lists(
        st.sampled_from(placeholder_names),
        min_size=num_placeholders,
        max_size=num_placeholders,
        unique=True
    ))
    
    # Generate template content with placeholders
    template_parts = []
    
    # Add some LaTeX structure
    template_parts.append(r"\documentclass[11pt,a4paper]{article}")
    template_parts.append(r"\begin{document}")
    template_parts.append("")
    
    # Add content with placeholders
    for placeholder in selected_placeholders:
        # Use different placeholder formats
        format_choice = draw(st.integers(min_value=0, max_value=2))
        if format_choice == 0:
            # Direct placeholder: COMPANY_NAME
            template_parts.append(f"Working at {placeholder} is exciting.")
        elif format_choice == 1:
            # Braced placeholder: {COMPANY_NAME}
            template_parts.append(f"Position at {{{placeholder}}} requires skills.")
        else:
            # Mixed format
            template_parts.append(f"Apply to {placeholder} for {{{selected_placeholders[0]}}} role.")
    
    # Add some regular content without placeholders
    template_parts.append("Experience with software development required.")
    template_parts.append(r"\end{document}")
    
    template_content = "\n".join(template_parts)
    
    return template_content, selected_placeholders


@st.composite
def replacement_values_generator(draw):
    """Generate realistic replacement values for placeholders"""
    
    # Company names (including some with special characters)
    companies = [
        "Volvo Cars", "Google Inc", "Microsoft Corporation", "Apple Inc",
        "Amazon Web Services", "Meta Platforms", "Netflix Inc",
        "Spotify Technology", "Klarna Bank", "H&M Group",
        "IKEA Group", "Ericsson AB", "SKF Group", "Electrolux AB",
        "Volvo Cars & Technology", "AT&T Inc", "Johnson & Johnson",
        "Procter & Gamble", "3M Company", "General Electric"
    ]
    
    # Job titles (including some with special characters)
    titles = [
        "Software Engineer", "Senior Developer", "Full-stack Developer",
        "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
        "Backend Developer", "Frontend Developer", "Mobile Developer",
        "Data Engineer", "Machine Learning Engineer", "Cloud Architect",
        "Software Engineer & DevOps Specialist", "Senior Developer (Remote)",
        "Full-stack Engineer - $120k", "DevOps & Cloud Engineer",
        "Software Developer (100% Remote)", "Senior Engineer - FinTech"
    ]
    
    # Role types
    role_types = [
        "fullstack_developer", "backend_developer", "devops_cloud",
        "android_developer", "incident_management_sre", "ai_product_engineer"
    ]
    
    company = draw(st.sampled_from(companies))
    title = draw(st.sampled_from(titles))
    role_type = draw(st.sampled_from(role_types))
    
    return company, title, role_type


@st.composite
def placeholder_replacement_data_generator(draw):
    """Generate complete test data for placeholder replacement testing"""
    
    # Generate template with placeholders
    template_content, placeholders = draw(template_with_placeholders_generator())
    
    # Generate replacement values
    company, title, role_type = draw(replacement_values_generator())
    
    return template_content, placeholders, company, title, role_type


class TestTemplateCustomizerPlaceholderProperties:
    """Property-based tests for placeholder replacement functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.customizer = TemplateCustomizer()
    
    @settings(max_examples=100)
    @given(placeholder_replacement_data_generator())
    def test_placeholder_replacement_completeness(self, test_data):
        """
        Property 11: Placeholder Replacement
        For any template with placeholders and job-specific information (company, title),
        all placeholders should be replaced with the provided values in the customized output.
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.2
        """
        template_content, placeholders, company, title, role_type = test_data
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, company, title, role_type
        )
        
        # Verify that customization was performed
        assert customized_content != "", "Customized content should not be empty"
        assert customized_content != template_content, \
            "Customized content should be different from original template"
        
        # Check that all expected placeholders have been replaced
        expected_replacements = {
            'COMPANY_NAME': company,
            'COMPANY_NAME_PLACEHOLDER': company,
            'JOB_TITLE': title,
            'JOB_TITLE_PLACEHOLDER': title,
            'ROLE_TITLE': title,
            'ROLE_TITLE_PLACEHOLDER': title,
            'Position': title
        }
        
        # For each placeholder that was in the original template
        for placeholder in placeholders:
            if placeholder in expected_replacements:
                expected_value = expected_replacements[placeholder]
                
                # Check direct placeholder replacement
                assert placeholder not in customized_content, \
                    f"Placeholder '{placeholder}' should be replaced but still found in customized content"
                
                # Check braced placeholder replacement
                braced_placeholder = f"{{{placeholder}}}"
                assert braced_placeholder not in customized_content, \
                    f"Braced placeholder '{braced_placeholder}' should be replaced but still found in customized content"
                
                # Verify the replacement value appears in the content
                # (accounting for LaTeX escaping)
                escaped_value = self.customizer.escape_latex_chars(expected_value)
                assert escaped_value in customized_content, \
                    f"Expected replacement value '{escaped_value}' should appear in customized content. " \
                    f"Original value: '{expected_value}', Placeholder: '{placeholder}'"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_preserves_non_placeholder_content(self, data):
        """
        Property: For any template with placeholders, non-placeholder content should be preserved
        during replacement
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.4, 6.5
        """
        # Generate test data
        test_data = data.draw(placeholder_replacement_data_generator())
        template_content, placeholders, company, title, role_type = test_data
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, company, title, role_type
        )
        
        # Check that LaTeX structure is preserved
        latex_markers = [r'\documentclass', r'\begin{document}', r'\end{document}']
        for marker in latex_markers:
            if marker in template_content:
                assert marker in customized_content, \
                    f"LaTeX marker '{marker}' should be preserved during customization"
        
        # Check that non-placeholder text is preserved
        # Find text that doesn't contain placeholders
        non_placeholder_patterns = [
            "Experience with software development required",
            "software development",
            "required",
            "exciting"
        ]
        
        for pattern in non_placeholder_patterns:
            if pattern in template_content:
                assert pattern in customized_content, \
                    f"Non-placeholder text '{pattern}' should be preserved during customization"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_handles_empty_values(self, data):
        """
        Property: For any template with placeholders, empty replacement values should be handled gracefully
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.2
        """
        # Generate template with placeholders
        template_content, placeholders = data.draw(template_with_placeholders_generator())
        
        # Use empty values
        empty_company = ""
        empty_title = ""
        role_type = "fullstack_developer"
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, empty_company, empty_title, role_type
        )
        
        # Should not crash and should return valid content
        assert customized_content != "", "Should handle empty values gracefully"
        
        # Should still preserve LaTeX structure
        latex_markers = [r'\documentclass', r'\begin{document}', r'\end{document}']
        for marker in latex_markers:
            if marker in template_content:
                assert marker in customized_content, \
                    f"LaTeX marker '{marker}' should be preserved even with empty replacement values"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_handles_special_characters(self, data):
        """
        Property: For any template with placeholders and replacement values containing special characters,
        the special characters should be properly escaped in LaTeX
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.2, 6.3
        """
        # Generate template with placeholders
        template_content, placeholders = data.draw(template_with_placeholders_generator())
        
        # Use values with special LaTeX characters
        special_companies = [
            "Johnson & Johnson", "AT&T Inc", "Procter & Gamble",
            "H&M Group", "3M Company", "R&D Solutions"
        ]
        special_titles = [
            "Software Engineer & DevOps Specialist",
            "Senior Developer (100% Remote)",
            "Full-stack Engineer - $120k",
            "DevOps & Cloud Engineer"
        ]
        
        company = data.draw(st.sampled_from(special_companies))
        title = data.draw(st.sampled_from(special_titles))
        role_type = "fullstack_developer"
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, company, title, role_type
        )
        
        # Should not crash and should return valid content
        assert customized_content != "", "Should handle special characters gracefully"
        
        # Check that special characters are properly escaped based on what placeholders are actually in the template
        company_placeholders = ['COMPANY_NAME', 'COMPANY_NAME_PLACEHOLDER']
        title_placeholders = ['JOB_TITLE', 'JOB_TITLE_PLACEHOLDER', 'ROLE_TITLE', 'ROLE_TITLE_PLACEHOLDER', 'Position']
        
        # Check company-related escaping only if company placeholders are in the template
        if any(placeholder in placeholders for placeholder in company_placeholders):
            if '&' in company:
                assert r'\&' in customized_content, \
                    f"Ampersand (&) in company '{company}' should be escaped as \\& in LaTeX"
            if '$' in company:
                assert r'\$' in customized_content, \
                    f"Dollar ($) in company '{company}' should be escaped as \\$ in LaTeX"
            if '%' in company:
                assert r'\%' in customized_content, \
                    f"Percent (%) in company '{company}' should be escaped as \\% in LaTeX"
        
        # Check title-related escaping only if title placeholders are in the template
        if any(placeholder in placeholders for placeholder in title_placeholders):
            if '&' in title:
                assert r'\&' in customized_content, \
                    f"Ampersand (&) in title '{title}' should be escaped as \\& in LaTeX"
            if '$' in title:
                assert r'\$' in customized_content, \
                    f"Dollar ($) in title '{title}' should be escaped as \\$ in LaTeX"
            if '%' in title:
                assert r'\%' in customized_content, \
                    f"Percent (%) in title '{title}' should be escaped as \\% in LaTeX"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_is_deterministic(self, data):
        """
        Property: For any template and replacement values, placeholder replacement should be deterministic
        (same input produces same output)
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.2
        """
        # Generate test data
        test_data = data.draw(placeholder_replacement_data_generator())
        template_content, placeholders, company, title, role_type = test_data
        
        # Customize the template multiple times
        results = []
        for _ in range(3):
            customized_content = self.customizer.customize_template(
                template_content, company, title, role_type
            )
            results.append(customized_content)
        
        # All results should be identical
        assert len(set(results)) == 1, \
            f"Placeholder replacement should be deterministic, but got different results: {len(set(results))} unique outputs"
        
        # Verify the result is not empty
        assert results[0] != "", "Customized content should not be empty"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_longest_first_priority(self, data):
        """
        Property: For any template with overlapping placeholders (e.g., JOB_TITLE and JOB_TITLE_PLACEHOLDER),
        longer placeholders should be replaced first to avoid partial replacements
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.1, 6.2
        """
        # Create a template with overlapping placeholders
        template_content = """
        \\documentclass[11pt,a4paper]{article}
        \\begin{document}
        
        Position: JOB_TITLE
        Full Position: JOB_TITLE_PLACEHOLDER
        Company: COMPANY_NAME
        Full Company: COMPANY_NAME_PLACEHOLDER
        
        \\end{document}
        """
        
        company = "Test Company"
        title = "Software Engineer"
        role_type = "fullstack_developer"
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, company, title, role_type
        )
        
        # Verify that both placeholders were replaced correctly
        # Should not have partial replacements like "Software Engineer_PLACEHOLDER"
        assert "JOB_TITLE" not in customized_content, \
            "JOB_TITLE placeholder should be completely replaced"
        assert "JOB_TITLE_PLACEHOLDER" not in customized_content, \
            "JOB_TITLE_PLACEHOLDER should be completely replaced"
        assert "COMPANY_NAME" not in customized_content, \
            "COMPANY_NAME placeholder should be completely replaced"
        assert "COMPANY_NAME_PLACEHOLDER" not in customized_content, \
            "COMPANY_NAME_PLACEHOLDER should be completely replaced"
        
        # Should not have artifacts like "_PLACEHOLDER" left over
        assert "_PLACEHOLDER" not in customized_content, \
            "Should not have placeholder artifacts left over from partial replacements"
        
        # Should contain the expected replacement values
        escaped_title = self.customizer.escape_latex_chars(title)
        escaped_company = self.customizer.escape_latex_chars(company)
        
        assert escaped_title in customized_content, \
            f"Escaped title '{escaped_title}' should appear in customized content"
        assert escaped_company in customized_content, \
            f"Escaped company '{escaped_company}' should appear in customized content"
    
    @settings(max_examples=100)
    @given(st.data())
    def test_placeholder_replacement_preserves_latex_structure(self, data):
        """
        Property: For any valid LaTeX template with placeholders, the LaTeX document structure
        should be preserved after placeholder replacement
        Feature: intelligent-cv-template-selection, Property 11: Placeholder Replacement
        Validates: Requirements 6.4, 6.5
        """
        # Generate test data
        test_data = data.draw(placeholder_replacement_data_generator())
        template_content, placeholders, company, title, role_type = test_data
        
        # Customize the template
        customized_content = self.customizer.customize_template(
            template_content, company, title, role_type
        )
        
        # Check that essential LaTeX structure is preserved
        essential_markers = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}'
        ]
        
        for marker in essential_markers:
            if marker in template_content:
                assert marker in customized_content, \
                    f"Essential LaTeX marker '{marker}' should be preserved during placeholder replacement"
        
        # Check that the number of LaTeX sections hasn't changed dramatically
        original_sections = len(re.findall(r'\\section\{', template_content))
        customized_sections = len(re.findall(r'\\section\{', customized_content))
        
        # Allow for minor differences but not major structural changes
        assert abs(original_sections - customized_sections) <= 1, \
            f"LaTeX section count should be preserved (±1). Original: {original_sections}, Customized: {customized_sections}"
        
        # Check that braces are balanced (basic LaTeX validity check)
        original_open_braces = template_content.count('{')
        original_close_braces = template_content.count('}')
        customized_open_braces = customized_content.count('{')
        customized_close_braces = customized_content.count('}')
        
        # The difference in brace counts should be the same (balanced)
        original_balance = original_open_braces - original_close_braces
        customized_balance = customized_open_braces - customized_close_braces
        
        assert original_balance == customized_balance, \
            f"LaTeX brace balance should be preserved. Original balance: {original_balance}, Customized balance: {customized_balance}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])