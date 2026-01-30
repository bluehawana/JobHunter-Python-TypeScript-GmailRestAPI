"""
Property-Based Tests for Template Loading
Tests universal properties of template loading functionality
"""

import pytest
from hypothesis import given, settings, strategies as st
from pathlib import Path
from cv_templates import CVTemplateManager


# Test generators
@st.composite
def valid_role_category_generator(draw):
    """Generate valid role categories that have existing templates"""
    manager = CVTemplateManager()
    
    # Get all available role categories
    available_roles = []
    for role_key in manager.ROLE_CATEGORIES.keys():
        # Check if both CV and CL templates exist for this role
        cv_path = manager.get_template_path(role_key, 'cv')
        cl_path = manager.get_template_path(role_key, 'cl')
        
        if cv_path and cv_path.exists():
            available_roles.append((role_key, 'cv'))
        if cl_path and cl_path.exists():
            available_roles.append((role_key, 'cl'))
    
    if not available_roles:
        # Fallback to a known role if no templates found
        return ('devops_cloud', 'cv')
    
    return draw(st.sampled_from(available_roles))


class TestTemplateLoadingProperties:
    """Property-based tests for template loading success"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = CVTemplateManager()
    
    @settings(max_examples=100)
    @given(valid_role_category_generator())
    def test_template_loading_success_for_valid_paths(self, role_and_type):
        """
        Property 9: Template Loading Success
        
        For any valid template file path, the system should successfully load 
        the file content with UTF-8 encoding.
        
        Feature: intelligent-cv-template-selection, Property 9: Template Loading Success
        Validates: Requirements 5.1, 5.2
        """
        role_category, template_type = role_and_type
        
        # Get the template path
        template_path = self.manager.get_template_path(role_category, template_type)
        
        # Skip if template doesn't exist (should not happen with our generator)
        if not template_path or not template_path.exists():
            pytest.skip(f"Template not found for {role_category} ({template_type})")
        
        # Load the template
        template_content = self.manager.load_template(role_category, template_type)
        
        # Verify successful loading
        assert template_content is not None, \
            f"Template loading failed for {role_category} ({template_type}) at {template_path}"
        
        # Verify content is not empty
        assert len(template_content) > 0, \
            f"Template content is empty for {role_category} ({template_type})"
        
        # Verify content is a string (UTF-8 decoded successfully)
        assert isinstance(template_content, str), \
            f"Template content is not a string for {role_category} ({template_type})"
        
        # Verify content contains some LaTeX-like structure (basic validation)
        # This ensures the file was read correctly and contains expected content
        latex_indicators = ['\\', '{', '}']
        has_latex_structure = any(indicator in template_content for indicator in latex_indicators)
        assert has_latex_structure, \
            f"Template content does not appear to be LaTeX for {role_category} ({template_type})"
    
    @settings(max_examples=50)
    @given(st.sampled_from(['cv', 'cl']))
    def test_template_loading_handles_utf8_encoding(self, template_type):
        """
        Property: Template loading handles UTF-8 encoding correctly
        
        For any template type, the system should handle UTF-8 encoding correctly
        when loading template files.
        
        Feature: intelligent-cv-template-selection, Property 9: Template Loading Success
        Validates: Requirements 5.2
        """
        # Find a role with an existing template
        role_with_template = None
        for role_key in self.manager.ROLE_CATEGORIES.keys():
            template_path = self.manager.get_template_path(role_key, template_type)
            if template_path and template_path.exists():
                role_with_template = role_key
                break
        
        if not role_with_template:
            pytest.skip(f"No {template_type} templates found for UTF-8 encoding test")
        
        # Load the template
        template_content = self.manager.load_template(role_with_template, template_type)
        
        # Verify successful loading with UTF-8 encoding
        assert template_content is not None, \
            f"UTF-8 template loading failed for {role_with_template} ({template_type})"
        
        # Verify the content is properly decoded as UTF-8 string
        assert isinstance(template_content, str), \
            f"Template content is not properly UTF-8 decoded for {role_with_template} ({template_type})"
        
        # Try to encode back to UTF-8 to verify it's valid UTF-8 content
        try:
            template_content.encode('utf-8')
        except UnicodeEncodeError:
            pytest.fail(f"Template content contains invalid UTF-8 characters for {role_with_template} ({template_type})")
    
    @settings(max_examples=30)
    @given(st.sampled_from(list(CVTemplateManager.ROLE_CATEGORIES.keys())))
    def test_template_loading_returns_none_for_missing_files(self, role_category):
        """
        Property: Template loading returns None for missing files
        
        For any role category where the template file does not exist,
        the system should return None gracefully.
        
        Feature: intelligent-cv-template-selection, Property 9: Template Loading Success
        Validates: Requirements 5.3
        """
        # Test both CV and CL template types
        for template_type in ['cv', 'cl']:
            template_path = self.manager.get_template_path(role_category, template_type)
            
            # If template doesn't exist, loading should return None
            if not template_path or not template_path.exists():
                template_content = self.manager.load_template(role_category, template_type)
                assert template_content is None, \
                    f"Expected None for missing template {role_category} ({template_type}), got: {type(template_content)}"


    @settings(max_examples=100)
    @given(valid_role_category_generator())
    def test_latex_structure_validation_for_loaded_templates(self, role_and_type):
        r"""
        Property 10: LaTeX Structure Validation
        
        For any loaded or customized template, it should contain required LaTeX 
        structure markers (\documentclass, \begin{document}, \end{document}) 
        and maintain valid LaTeX formatting.
        
        Feature: intelligent-cv-template-selection, Property 10: LaTeX Structure Validation
        Validates: Requirements 5.4, 6.4, 6.5
        """
        role_category, template_type = role_and_type
        
        # Load the template
        template_content = self.manager.load_template(role_category, template_type)
        
        # Skip if template doesn't exist or failed to load
        if template_content is None:
            pytest.skip(f"Template not found or failed to load for {role_category} ({template_type})")
        
        # Validate required LaTeX structure markers
        self._validate_latex_structure(template_content, role_category, template_type)
    
    def _validate_latex_structure(self, content: str, role_category: str, template_type: str):
        """Helper method to validate LaTeX document structure"""
        
        # Required LaTeX structure markers
        required_markers = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}'
        ]
        
        # Check for required markers
        for marker in required_markers:
            assert marker in content, \
                f"Missing required LaTeX marker '{marker}' in {role_category} ({template_type}) template"
        
        # Validate document structure order
        documentclass_pos = content.find(r'\documentclass')
        begin_doc_pos = content.find(r'\begin{document}')
        end_doc_pos = content.find(r'\end{document}')
        
        assert documentclass_pos < begin_doc_pos, \
            f"\\documentclass must come before \\begin{{document}} in {role_category} ({template_type}) template"
        
        assert begin_doc_pos < end_doc_pos, \
            f"\\begin{{document}} must come before \\end{{document}} in {role_category} ({template_type}) template"
        
        # Validate basic LaTeX formatting - check for balanced braces
        self._validate_balanced_braces(content, role_category, template_type)
        
        # Validate no obvious LaTeX syntax errors
        self._validate_basic_latex_syntax(content, role_category, template_type)
    
    def _validate_balanced_braces(self, content: str, role_category: str, template_type: str):
        """Validate that LaTeX braces are balanced"""
        brace_count = 0
        for char in content:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                # Ensure we never have more closing braces than opening
                assert brace_count >= 0, \
                    f"Unbalanced braces (too many closing braces) in {role_category} ({template_type}) template"
        
        # Ensure all braces are closed
        assert brace_count == 0, \
            f"Unbalanced braces ({brace_count} unclosed) in {role_category} ({template_type}) template"
    
    def _validate_basic_latex_syntax(self, content: str, role_category: str, template_type: str):
        """Validate basic LaTeX syntax patterns"""
        
        # Check for common LaTeX syntax errors
        
        # 1. Validate \begin{} and \end{} environments are balanced
        import re
        
        # Find all \begin{environment} patterns
        begin_pattern = r'\\begin\{([^}]+)\}'
        end_pattern = r'\\end\{([^}]+)\}'
        
        begin_matches = re.findall(begin_pattern, content)
        end_matches = re.findall(end_pattern, content)
        
        # Count occurrences of each environment
        begin_counts = {}
        end_counts = {}
        
        for env in begin_matches:
            begin_counts[env] = begin_counts.get(env, 0) + 1
        
        for env in end_matches:
            end_counts[env] = end_counts.get(env, 0) + 1
        
        # Validate that each \begin{} has a matching \end{}
        for env, count in begin_counts.items():
            end_count = end_counts.get(env, 0)
            assert count == end_count, \
                f"Unbalanced LaTeX environment '{env}': {count} \\begin{{{env}}} but {end_count} \\end{{{env}}} in {role_category} ({template_type}) template"
        
        # Check for orphaned \end{} environments
        for env, count in end_counts.items():
            if env not in begin_counts:
                assert False, \
                    f"Orphaned \\end{{{env}}} without matching \\begin{{{env}}} in {role_category} ({template_type}) template"
        
        # 2. Validate no unescaped special characters in inappropriate contexts
        # (This is a basic check - more sophisticated validation would require a LaTeX parser)
        
        # Check for common problematic patterns
        problematic_patterns = [
            (r'(?<!\\)&(?![&\s])', "Unescaped & character (should be \\& in text)"),
            (r'(?<!\\)%(?![%\s])', "Unescaped % character (should be \\% in text)"),
            (r'(?<!\\)\$(?!\$)', "Unescaped $ character (should be \\$ in text or use $$ for math)"),
        ]
        
        for pattern, error_msg in problematic_patterns:
            matches = re.findall(pattern, content)
            # Only warn for now, as these might be legitimate in some contexts
            if matches:
                # Use a more lenient check - only fail if there are many unescaped characters
                # This avoids false positives in legitimate LaTeX usage
                if len(matches) > 5:  # Threshold for likely errors
                    assert False, \
                        f"{error_msg} (found {len(matches)} instances) in {role_category} ({template_type}) template"


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])