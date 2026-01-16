"""
Template Matcher Component
Scores templates and selects the best match using percentage-based scoring
"""

from typing import Dict, List, Tuple, Optional


class TemplateMatcher:
    """Matches job descriptions to templates using percentage-based scoring"""
    
    def __init__(self, role_categories: Dict):
        """
        Initialize the TemplateMatcher
        
        Args:
            role_categories: Dictionary of role categories with keywords and priorities
                           Format: {role_key: {'keywords': [...], 'priority': int, ...}}
        """
        self.role_categories = role_categories
    
    def calculate_scores(self, keyword_counts: Dict[str, Dict[str, int]]) -> Dict[str, float]:
        """
        Calculate weighted scores for each role category
        
        Args:
            keyword_counts: Dictionary mapping role keys to their keyword match counts
                          Format: {role_key: {keyword: count, ...}}
        
        Returns:
            Dictionary mapping role keys to their weighted scores
            Format: {role_key: weighted_score}
        """
        role_scores = {}
        
        for role_key, role_data in self.role_categories.items():
            # Get keyword matches for this role
            matches = keyword_counts.get(role_key, {})
            
            # Calculate raw score (sum of all keyword occurrences)
            raw_score = sum(matches.values())
            
            # Apply priority weighting (lower priority number = higher weight)
            # Divide by priority to give higher scores to lower priority numbers
            priority = role_data.get('priority', 1)
            weighted_score = raw_score / priority
            
            role_scores[role_key] = weighted_score
        
        return role_scores
    
    def calculate_percentages(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize scores to percentages (0-100%) that sum to 100%
        
        Args:
            scores: Dictionary mapping role keys to their weighted scores
        
        Returns:
            Dictionary mapping role keys to their percentage scores
            Format: {role_key: percentage}
        """
        # Calculate total score
        total_score = sum(scores.values())
        
        # Handle edge case: no scores
        if total_score == 0:
            return {role_key: 0.0 for role_key in scores.keys()}
        
        # Normalize to percentages
        percentages = {}
        for role_key, score in scores.items():
            percentage = (score / total_score) * 100.0
            percentages[role_key] = percentage
        
        return percentages
    
    def get_role_breakdown(
        self, 
        percentages: Dict[str, float], 
        threshold: float = 5.0
    ) -> List[Tuple[str, float]]:
        """
        Filter and rank roles by percentage, returning only significant roles
        
        Args:
            percentages: Dictionary mapping role keys to their percentage scores
            threshold: Minimum percentage to include in breakdown (default 5%)
        
        Returns:
            List of (role_key, percentage) tuples, sorted by percentage descending
        """
        # Filter roles above threshold
        significant_roles = [
            (role_key, percentage)
            for role_key, percentage in percentages.items()
            if percentage >= threshold
        ]
        
        # Sort by percentage descending
        significant_roles.sort(key=lambda x: x[1], reverse=True)
        
        return significant_roles
    
    def select_best_match(self, scores: Dict[str, float]) -> Tuple[str, float]:
        """
        Select the role with the highest score
        
        Args:
            scores: Dictionary mapping role keys to their weighted scores
        
        Returns:
            Tuple of (best_role_key, best_score)
        """
        if not scores:
            return ('', 0.0)
        
        # Find role with maximum score
        best_role = max(scores, key=scores.get)
        best_score = scores[best_role]
        
        return (best_role, best_score)
    
    def get_fallback_template(self, excluded: Optional[List[str]] = None) -> str:
        """
        Get a fallback template when primary selection fails
        
        Args:
            excluded: List of role keys to exclude from fallback selection
        
        Returns:
            Role key for fallback template (typically 'devops_cloud')
        """
        if excluded is None:
            excluded = []
        
        # Default fallback is devops_cloud
        default_fallback = 'devops_cloud'
        
        # If default is excluded, find the role with lowest priority number
        # (highest priority) that's not excluded
        if default_fallback in excluded:
            available_roles = [
                (role_key, role_data.get('priority', 999))
                for role_key, role_data in self.role_categories.items()
                if role_key not in excluded
            ]
            
            if available_roles:
                # Sort by priority (lowest number = highest priority)
                available_roles.sort(key=lambda x: x[1])
                return available_roles[0][0]
        
        return default_fallback
    
    def calculate_confidence_score(
        self, 
        best_score: float, 
        second_best_score: float,
        total_score: float
    ) -> float:
        """
        Calculate confidence score for the best match
        
        Confidence is based on:
        1. How much better the best score is compared to second best
        2. How significant the total score is (more keywords = higher confidence)
        
        Args:
            best_score: Score of the best matching role
            second_best_score: Score of the second best matching role
            total_score: Sum of all role scores
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if total_score == 0:
            return 0.0
        
        # Calculate separation ratio (how much better is best vs second best)
        if second_best_score == 0:
            separation = 1.0  # Perfect separation
        else:
            separation = (best_score - second_best_score) / best_score
            separation = max(0.0, min(1.0, separation))  # Clamp to [0, 1]
        
        # Calculate score significance (normalized by a reasonable threshold)
        # Assume 10+ keyword matches is "high confidence"
        significance = min(1.0, total_score / 10.0)
        
        # Combine separation and significance
        # Weight separation more heavily (70%) than significance (30%)
        confidence = (0.7 * separation) + (0.3 * significance)
        
        return confidence


# Example usage and tests
if __name__ == '__main__':
    # Sample role categories (simplified)
    role_categories = {
        'android_developer': {
            'keywords': ['android', 'kotlin', 'mobile'],
            'priority': 1
        },
        'fullstack_developer': {
            'keywords': ['fullstack', 'react', 'typescript'],
            'priority': 2
        },
        'devops_cloud': {
            'keywords': ['devops', 'kubernetes', 'aws'],
            'priority': 4
        }
    }
    
    matcher = TemplateMatcher(role_categories)
    
    # Test case 1: Clear fullstack match
    print("=" * 60)
    print("TEST CASE 1: Clear Fullstack Match")
    print("=" * 60)
    
    keyword_counts_1 = {
        'android_developer': {'android': 1},
        'fullstack_developer': {'fullstack': 3, 'react': 5, 'typescript': 4},
        'devops_cloud': {'kubernetes': 2}
    }
    
    scores_1 = matcher.calculate_scores(keyword_counts_1)
    print(f"Raw scores: {scores_1}")
    
    percentages_1 = matcher.calculate_percentages(scores_1)
    print(f"Percentages: {percentages_1}")
    
    breakdown_1 = matcher.get_role_breakdown(percentages_1)
    print(f"Role breakdown (>5%): {breakdown_1}")
    
    best_role_1, best_score_1 = matcher.select_best_match(scores_1)
    print(f"Best match: {best_role_1} (score: {best_score_1:.2f})")
    
    # Test case 2: Mixed role (software engineering with AI mentions)
    print("\n" + "=" * 60)
    print("TEST CASE 2: Mixed Role")
    print("=" * 60)
    
    keyword_counts_2 = {
        'android_developer': {},
        'fullstack_developer': {'fullstack': 8, 'react': 10, 'typescript': 8},
        'devops_cloud': {'kubernetes': 3, 'aws': 2}
    }
    
    scores_2 = matcher.calculate_scores(keyword_counts_2)
    print(f"Raw scores: {scores_2}")
    
    percentages_2 = matcher.calculate_percentages(scores_2)
    print(f"Percentages: {percentages_2}")
    
    # Check if percentages sum to 100%
    total_percentage = sum(percentages_2.values())
    print(f"Total percentage: {total_percentage:.2f}% (should be 100%)")
    
    breakdown_2 = matcher.get_role_breakdown(percentages_2)
    print(f"Role breakdown (>5%): {breakdown_2}")
    
    best_role_2, best_score_2 = matcher.select_best_match(scores_2)
    print(f"Best match: {best_role_2} (score: {best_score_2:.2f})")
    
    # Test case 3: Confidence score calculation
    print("\n" + "=" * 60)
    print("TEST CASE 3: Confidence Score")
    print("=" * 60)
    
    sorted_scores = sorted(scores_2.values(), reverse=True)
    best = sorted_scores[0] if len(sorted_scores) > 0 else 0
    second_best = sorted_scores[1] if len(sorted_scores) > 1 else 0
    total = sum(scores_2.values())
    
    confidence = matcher.calculate_confidence_score(best, second_best, total)
    print(f"Best score: {best:.2f}")
    print(f"Second best score: {second_best:.2f}")
    print(f"Total score: {total:.2f}")
    print(f"Confidence: {confidence:.2f}")
    
    # Test case 4: Fallback template
    print("\n" + "=" * 60)
    print("TEST CASE 4: Fallback Template")
    print("=" * 60)
    
    fallback_1 = matcher.get_fallback_template()
    print(f"Default fallback: {fallback_1}")
    
    fallback_2 = matcher.get_fallback_template(excluded=['devops_cloud'])
    print(f"Fallback (excluding devops_cloud): {fallback_2}")
