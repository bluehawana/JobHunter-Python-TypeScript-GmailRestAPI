"""
Job Analyzer Component
Extracts keywords and analyzes job descriptions for template matching
"""

import re
import logging
from typing import Dict, List

# Configure logging
logger = logging.getLogger(__name__)


class JobAnalyzer:
    """Analyzes job descriptions to extract keywords and role indicators"""
    
    def __init__(self):
        """Initialize the JobAnalyzer"""
        pass
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for consistent analysis
        
        Args:
            text: Raw text to normalize
            
        Returns:
            Normalized text (lowercase, whitespace normalized)
        """
        if not text:
            return ""
        
        # Convert to lowercase
        normalized = text.lower()
        
        # Normalize whitespace (replace multiple spaces/newlines with single space)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Strip leading/trailing whitespace
        normalized = normalized.strip()
        
        return normalized
    
    def count_keyword_occurrences(self, text: str, keyword: str) -> int:
        """
        Count occurrences of a keyword in text using word boundary matching
        
        Args:
            text: Text to search in (should be normalized)
            keyword: Keyword to search for (can be multi-word phrase)
            
        Returns:
            Number of occurrences found
        """
        if not text or not keyword:
            return 0
        
        try:
            # Normalize both text and keyword for comparison
            text_lower = text.lower()
            keyword_lower = keyword.lower()
            
            # Escape special regex characters in the keyword
            escaped_keyword = re.escape(keyword_lower)
            
            # Use word boundary matching to find exact matches
            # \b matches word boundaries (start/end of words)
            pattern = r'\b' + escaped_keyword + r'\b'
            
            # Find all matches
            matches = re.findall(pattern, text_lower)
            
            return len(matches)
            
        except Exception as e:
            logger.error(f"Error counting keyword occurrences for '{keyword}': {e}")
            return 0
    
    def extract_keywords(self, job_description: str, keyword_list: List[str]) -> Dict[str, int]:
        """
        Extract keywords from job description and count their occurrences
        
        Args:
            job_description: The job description text to analyze
            keyword_list: List of keywords to search for (can include multi-word phrases)
            
        Returns:
            Dictionary mapping keywords to their occurrence counts
        """
        if not job_description:
            logger.warning("Empty job description provided for keyword extraction")
            return {}
        
        if not keyword_list:
            logger.warning("Empty keyword list provided for extraction")
            return {}
        
        try:
            # Normalize the job description
            normalized_text = self.normalize_text(job_description)
            
            # Count occurrences of each keyword
            keyword_counts = {}
            
            for keyword in keyword_list:
                if not keyword:
                    continue
                
                try:
                    # Normalize the keyword
                    normalized_keyword = self.normalize_text(keyword)
                    
                    # Count occurrences using word boundary matching
                    count = self.count_keyword_occurrences(normalized_text, normalized_keyword)
                    
                    # Only include keywords that were found
                    if count > 0:
                        keyword_counts[keyword] = count
                        
                except Exception as e:
                    logger.error(f"Error processing keyword '{keyword}': {e}")
                    continue
            
            return keyword_counts
            
        except Exception as e:
            logger.error(f"Error extracting keywords from job description: {e}")
            logger.error(f"Keyword extraction failure - Error: {type(e).__name__}")
            return {}
    
    def identify_role_indicators(self, job_description: str, role_categories: Dict) -> Dict[str, Dict[str, int]]:
        """
        Identify role indicators by extracting keywords for each role category
        
        Args:
            job_description: The job description text to analyze
            role_categories: Dictionary of role categories with their keywords
                            Format: {role_key: {'keywords': [list of keywords], ...}}
            
        Returns:
            Dictionary mapping role keys to their keyword match counts
            Format: {role_key: {keyword: count, ...}}
        """
        if not job_description or not role_categories:
            logger.warning("Empty job description or role categories provided")
            return {}
        
        logger.debug(f"Analyzing job description for {len(role_categories)} role categories")
        
        role_indicators = {}
        
        for role_key, role_data in role_categories.items():
            keywords = role_data.get('keywords', [])
            
            if not keywords:
                logger.debug(f"No keywords defined for role: {role_key}")
                continue
            
            # Extract keywords for this role
            keyword_counts = self.extract_keywords(job_description, keywords)
            
            # Store the results
            role_indicators[role_key] = keyword_counts
            
            # Log keyword matches when debugging enabled
            if logger.isEnabledFor(logging.DEBUG) and keyword_counts:
                total_matches = sum(keyword_counts.values())
                logger.debug(f"Role {role_key}: {total_matches} keyword matches - {keyword_counts}")
        
        return role_indicators


# Example usage and tests
if __name__ == '__main__':
    analyzer = JobAnalyzer()
    
    # Test text normalization
    print("=" * 60)
    print("TEXT NORMALIZATION TEST")
    print("=" * 60)
    
    test_text = "  Hello   World\n\nThis  is   a   test  "
    normalized = analyzer.normalize_text(test_text)
    print(f"Original: '{test_text}'")
    print(f"Normalized: '{normalized}'")
    
    # Test keyword counting
    print("\n" + "=" * 60)
    print("KEYWORD COUNTING TEST")
    print("=" * 60)
    
    job_desc = """
    We are looking for a Full-Stack Developer with experience in React, TypeScript,
    and cloud technologies. You should have strong full stack development skills
    and experience with fullstack projects. Knowledge of cloud platforms is essential.
    """
    
    test_keywords = [
        'full-stack',
        'fullstack',
        'full stack',
        'react',
        'typescript',
        'cloud',
        'python'  # Not in text
    ]
    
    for keyword in test_keywords:
        count = analyzer.count_keyword_occurrences(
            analyzer.normalize_text(job_desc),
            keyword
        )
        print(f"'{keyword}': {count} occurrences")
    
    # Test keyword extraction
    print("\n" + "=" * 60)
    print("KEYWORD EXTRACTION TEST")
    print("=" * 60)
    
    keyword_counts = analyzer.extract_keywords(job_desc, test_keywords)
    print("Extracted keywords:")
    for keyword, count in keyword_counts.items():
        print(f"  {keyword}: {count}")
    
    # Test multi-word keyword support
    print("\n" + "=" * 60)
    print("MULTI-WORD KEYWORD TEST")
    print("=" * 60)
    
    multi_word_text = """
    We need a site reliability engineer with experience in incident management.
    The ideal candidate has worked as a site reliability engineer before.
    This website is not relevant.
    """
    
    multi_word_keywords = [
        'site reliability',
        'site reliability engineer',
        'incident management',
        'website'  # Should match 'website' but not 'site' in 'site reliability'
    ]
    
    for keyword in multi_word_keywords:
        count = analyzer.count_keyword_occurrences(
            analyzer.normalize_text(multi_word_text),
            keyword
        )
        print(f"'{keyword}': {count} occurrences")
