"""
Template Customizer Component
Customizes CV templates with job-specific information
"""

import re
import logging
from typing import Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)


class TemplateCustomizer:
    """
    Customizes templates with job-specific information.
    
    Responsibilities:
    - Replace placeholder text with job-specific information
    - Escape LaTeX special characters in job titles and company names
    - Update job titles in CV headers
    - Preserve original template structure
    - Maintain proper LaTeX formatting
    """
    
    # LaTeX special characters that need escaping
    LATEX_SPECIAL_CHARS = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}'
        # Note: Backslash (\) is handled separately to avoid conflicts
    }
    
    def __init__(self):
        """Initialize the TemplateCustomizer"""
        pass
    
    def customize_template(
        self, 
        template_content: str, 
        company: str, 
        title: str, 
        role_type: str
    ) -> str:
        """
        Customize template with job-specific information
        
        Args:
            template_content: The original template content
            company: Company name for the job
            title: Job title
            role_type: Role category (e.g., 'fullstack_developer')
            
        Returns:
            Customized template content with placeholders replaced
            
        Validates: Requirements 6.1, 6.2, 6.4, 6.5
        """
        if not template_content:
            logger.error("Template content is empty or None")
            return ""
        
        # Check if this is the new multi-line format
        has_multiline_format = 'COMPANY_NAME' in template_content and 'JOB_TITLE' in template_content
        
        # Clean up inputs
        clean_title = self._clean_title(title, role_type)
        clean_company = company.strip() if company else ""
        
        # Escape LaTeX special characters
        escaped_title = self.escape_latex_chars(clean_title)
        escaped_company = self.escape_latex_chars(clean_company)
        
        logger.info(f"Customizing template for {escaped_company} - {escaped_title}")
        
        # Create replacement dictionary
        replacements = {
            'COMPANY_NAME': escaped_company,
            'COMPANY_NAME_PLACEHOLDER': escaped_company,
            'JOB_TITLE': escaped_title,
            'JOB_TITLE_PLACEHOLDER': escaped_title,
            'ROLE_TITLE': escaped_title,
            'ROLE_TITLE_PLACEHOLDER': escaped_title,
            'Position': escaped_title,  # Common placeholder in templates
        }
        
        # Apply replacements
        customized_content = self.replace_placeholders(template_content, replacements)
        
        # Update job title in CV header (LaTeX-specific patterns) - skip for new multi-line format
        if not has_multiline_format:
            customized_content = self._update_cv_header_title(customized_content, escaped_title)
        else:
            logger.debug("Skipping header title update - using new multi-line format")
        
        # Validate that structure is preserved
        if not self._validate_structure_preserved(template_content, customized_content):
            logger.warning("Template structure may have been altered during customization")
        
        logger.info("Template customization completed successfully")
        return customized_content
    
    def escape_latex_chars(self, text: str) -> str:
        """
        Escape special LaTeX characters in text
        
        Args:
            text: Text that may contain LaTeX special characters
            
        Returns:
            Text with LaTeX special characters properly escaped
            
        Validates: Requirements 6.3
        """
        if not text:
            return ""
        
        escaped_text = text
        
        # Only escape the most common problematic characters in job titles
        # Be conservative to avoid over-escaping
        common_escapes = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#'
        }
        
        # Escape each special character
        for char, replacement in common_escapes.items():
            escaped_text = escaped_text.replace(char, replacement)
        
        return escaped_text
    
    def replace_placeholders(self, template: str, replacements: Dict[str, str]) -> str:
        """
        Replace placeholder text with actual values
        
        Args:
            template: Template content with placeholders
            replacements: Dictionary mapping placeholder names to replacement values
            
        Returns:
            Template with placeholders replaced
            
        Validates: Requirements 6.1
        """
        if not template:
            return ""
        
        result = template
        
        # Sort replacements by length (longest first) to avoid partial replacements
        sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        for placeholder, replacement in sorted_replacements:
            if replacement:  # Only replace if replacement value is not empty
                # Replace direct placeholder matches (exact match)
                result = result.replace(placeholder, replacement)
                
                # Replace placeholder patterns with braces (common in LaTeX)
                result = result.replace(f"{{{placeholder}}}", replacement)
        
        return result
    
    def _clean_title(self, title: str, role_type: str) -> str:
        """Clean up job title, removing extra whitespace and newlines"""
        if not title or title.strip() == 'Position':
            # Use role_type as fallback, convert to readable format
            return role_type.replace('_', ' ').title() if role_type else "Software Developer"
        
        # Clean up the title - remove extra whitespace and newlines
        clean_title = title.strip().split('\n')[0] if title else ""
        
        # Remove excessive whitespace
        clean_title = re.sub(r'\s+', ' ', clean_title)
        
        return clean_title
    
    def _update_cv_header_title(self, content: str, title: str) -> str:
        """
        Update job title in CV header using LaTeX-specific patterns
        
        This handles common LaTeX CV header patterns like:
        - {\Large DevOps & Cloud Engineer | FinTech Specialist}
        - {\Large Software Engineer | Automotive & Embedded Systems Enthusiast}
        
        Skip this if we have the new multi-line format with COMPANY_NAME and JOB_TITLE placeholders
        """
        
        # Skip header title update if we have the new multi-line format
        if 'COMPANY_NAME' in content or 'JOB_TITLE' in content:
            logger.debug("Skipping header title update - using new multi-line format")
            return content
        
        # Pattern 1: Replace the {\Large ...} line after the name
        # This matches lines like "{\Large DevOps & Cloud Engineer | FinTech Specialist}"
        pattern = r'\{\\Large\s+[^\}]+\}'
        
        # Find the pattern
        match = re.search(pattern, content)
        if match:
            # Replace with clean title
            replacement = f'{{\\Large {title}}}'
            content = content.replace(match.group(0), replacement, 1)
            logger.debug(f"Updated CV header title pattern: {match.group(0)} -> {replacement}")
        
        # Pattern 2: Look for other common title patterns
        # {\large Title} or {\LARGE Title}
        for size in ['large', 'LARGE', 'huge', 'Huge']:
            pattern = rf'\{{\\{size}\s+[^\}}]+\}}'
            match = re.search(pattern, content)
            if match and 'Hongzhi Li' not in match.group(0):  # Don't replace name
                replacement = f'{{\\{size} {title}}}'
                content = content.replace(match.group(0), replacement, 1)
                logger.debug(f"Updated CV header title pattern: {match.group(0)} -> {replacement}")
                break
        
        return content
    
    def _validate_structure_preserved(self, original: str, customized: str) -> bool:
        """
        Validate that the original template structure is preserved
        
        Checks that essential LaTeX structure elements are still present
        """
        # Check that essential LaTeX markers are preserved
        essential_markers = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}'
        ]
        
        for marker in essential_markers:
            if marker in original and marker not in customized:
                logger.error(f"Essential LaTeX marker '{marker}' was removed during customization")
                return False
        
        # Check that the number of sections hasn't dramatically changed
        original_sections = len(re.findall(r'\\section\{', original))
        customized_sections = len(re.findall(r'\\section\{', customized))
        
        if original_sections > 0 and abs(original_sections - customized_sections) > 1:
            logger.warning(f"Section count changed significantly: {original_sections} -> {customized_sections}")
            return False
        
        return True


# Example usage and testing
if __name__ == '__main__':
    # Configure logging for demo
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    customizer = TemplateCustomizer()
    
    # Test LaTeX character escaping
    test_title = "Software Engineer & DevOps Specialist (100% Remote) - $120k"
    escaped = customizer.escape_latex_chars(test_title)
    print(f"Original: {test_title}")
    print(f"Escaped:  {escaped}")
    
    # Test template customization
    sample_template = r"""
\documentclass[11pt,a4paper]{article}
\begin{document}

\begin{center}
{\LARGE \textbf{Hongzhi Li}}\\[2pt]
{\Large JOB_TITLE_PLACEHOLDER}\\[4pt]
\end{center}

\section{Professional Summary}
Experienced developer applying for COMPANY_NAME_PLACEHOLDER.

\section{Experience}
\subsection{Current Role}
Working on projects for various companies including COMPANY_NAME.

\end{document}
"""
    
    customized = customizer.customize_template(
        sample_template,
        "Volvo Cars & Technology",
        "Senior Software Engineer & DevOps Specialist",
        "fullstack_developer"
    )
    
    print("\n" + "="*60)
    print("CUSTOMIZED TEMPLATE:")
    print("="*60)
    print(customized)