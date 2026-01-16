# Implementation Plan

## Overview

This implementation plan adds percentage-based weighted scoring to prevent misclassification of jobs. The key improvement is distinguishing between "AI Product Engineer" (building AI systems) and "Software Engineer with AI integration" (using AI APIs in software).

## Current Status

The codebase already has:
- ✅ CVTemplateManager with role categories and keyword-based scoring
- ✅ AIAnalyzer component using Minimax M2 API
- ✅ Basic template selection and loading
- ✅ API endpoints (analyze-job, generate-lego-application)
- ✅ AI misclassification prevention logic (checks for strong AI signals vs integration)

What's missing:
- ❌ Percentage-based scoring (currently uses raw weighted scores)
- ❌ Separate JobAnalyzer and TemplateMatcher components
- ❌ get_role_percentages() and get_role_breakdown() methods
- ❌ Property-based tests for the template selection system
- ❌ API responses don't include percentage breakdown

## Tasks

- [x] 1. Update role category definitions to prevent AI misclassification
  - Already implemented in CVTemplateManager.analyze_job_role()
  - Has logic to check for strong AI signals vs AI integration
  - Distinguishes between building AI systems vs using AI APIs
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [x] 2. Refactor CVTemplateManager to use separate components
  - [x] 2.1 Create JobAnalyzer class with keyword extraction
    - Extract keyword extraction logic from analyze_job_role into JobAnalyzer
    - Implement extract_keywords method with word boundary matching
    - Implement count_keyword_occurrences with regex
    - Implement normalize_text for consistent analysis
    - Handle multi-word keywords as single units
    - _Requirements: 1.1, 1.2, 1.4, 1.5, 4.5_

  - [x] 2.2 Write property test for keyword extraction
    - **Property 1: Keyword Extraction Completeness**
    - **Validates: Requirements 1.1, 1.4, 1.5**

  - [x]* 2.3 Write property test for multi-word keyword support
    - **Property 6: Multi-word Keyword Support**
    - **Validates: Requirements 4.5**

- [x] 3. Create TemplateMatcher component with percentage-based scoring
  - [x] 3.1 Create TemplateMatcher class with scoring logic
    - Implement calculate_scores with priority weighting (existing logic)
    - Implement calculate_percentages to normalize scores to 0-100%
    - Implement get_role_breakdown to filter and rank roles by percentage
    - Implement select_best_match to find highest score
    - Implement get_fallback_template for error cases
    - Add confidence score calculation
    - _Requirements: 1.3, 2.1, 4.3, 10.1, 10.2, 10.3, 10.4_

  - [ ]* 3.2 Write property test for role score calculation
    - **Property 2: Role Score Calculation**
    - **Validates: Requirements 1.3, 4.3**

  - [ ]* 3.3 Write property test for best match selection
    - **Property 3: Best Match Selection**
    - **Validates: Requirements 2.1**

  - [ ]* 3.4 Write property test for percentage calculation
    - **Property 16: Percentage Calculation for All Roles**
    - **Validates: Requirements 10.1**

  - [ ]* 3.5 Write property test for percentage normalization
    - **Property 17: Percentage Normalization**
    - **Validates: Requirements 10.2**

  - [ ]* 3.6 Write property test for role breakdown filtering
    - **Property 18: Role Breakdown Filtering**
    - **Validates: Requirements 10.3**

  - [ ]* 3.7 Write property test for role breakdown ordering
    - **Property 19: Role Breakdown Ordering**
    - **Validates: Requirements 10.4**

  - [ ]* 3.8 Write property test for AI misclassification prevention
    - **Property 23: AI Misclassification Prevention**
    - **Validates: Requirements 11.1, 11.5**

  - [ ]* 3.9 Write property test for AI integration vs AI product distinction
    - **Property 24: AI Integration vs AI Product Distinction**
    - **Validates: Requirements 11.3, 11.6**

- [ ] 4. Update CVTemplateManager with percentage-based methods
  - [ ] 4.1 Integrate JobAnalyzer and TemplateMatcher
    - Use JobAnalyzer to extract keywords from job description
    - Use TemplateMatcher to calculate scores and percentages
    - Update analyze_job_role to use new components
    - Maintain backward compatibility with existing code
    - _Requirements: 1.1, 1.3, 2.1, 7.1, 7.2_

  - [ ] 4.2 Add percentage-based methods to CVTemplateManager
    - Implement get_role_percentages method
    - Implement get_role_breakdown method with threshold parameter
    - Add mixed role warning when primary role < 50%
    - Update analyze_job_role to include percentage data
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.7_

  - [ ]* 4.3 Write property test for template diversity
    - **Property 4: Template Diversity**
    - **Validates: Requirements 2.9**

  - [ ]* 4.4 Write property test for mixed role warning
    - **Property 20: Mixed Role Warning**
    - **Validates: Requirements 10.5**

  - [ ]* 4.5 Write property test for template selection by highest percentage
    - **Property 22: Template Selection by Highest Percentage**
    - **Validates: Requirements 10.7**

  - [ ]* 4.6 Write unit tests for specific role detection
    - Test Android job → Android template
    - Test CI/CD job → DevOps template
    - Test SRE job → Incident Management template
    - Test Full-stack job → Full-stack template
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [ ] 5. Enhance template path validation and loading
  - [ ] 5.1 Add template file existence verification
    - Already partially implemented in get_template_path
    - Add fallback to next best template if missing
    - Log errors for missing templates
    - _Requirements: 2.7, 2.8, 3.5_

  - [ ]* 5.2 Write property test for template file existence verification
    - **Property 7: Template File Existence Verification**
    - **Validates: Requirements 2.7**

  - [ ] 5.3 Improve template path resolution
    - Already handles both directory and file paths
    - Validate path format consistency
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [ ]* 5.4 Write property test for path format consistency
    - **Property 8: Path Format Consistency**
    - **Validates: Requirements 3.1, 3.4**

  - [ ] 5.5 Enhance template loading with validation
    - Already loads with UTF-8 encoding
    - Add LaTeX structure validation after loading
    - Return detailed errors on failure
    - Implement fallback template loading
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 5.6 Write property test for template loading success
    - **Property 9: Template Loading Success**
    - **Validates: Requirements 5.1, 5.2**

  - [ ]* 5.7 Write property test for LaTeX structure validation
    - **Property 10: LaTeX Structure Validation**
    - **Validates: Requirements 5.4, 6.4, 6.5**

- [ ] 6. Create TemplateCustomizer component
  - [ ] 6.1 Create TemplateCustomizer class
    - Implement customize_template function
    - Replace placeholders with job-specific information
    - Escape LaTeX special characters in titles and company names
    - Preserve template structure during customization
    - Validate LaTeX formatting after customization
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 6.2 Write property test for placeholder replacement
    - **Property 11: Placeholder Replacement**
    - **Validates: Requirements 6.1, 6.2**

  - [ ]* 6.3 Write property test for LaTeX character escaping
    - **Property 12: LaTeX Character Escaping**
    - **Validates: Requirements 6.3**

- [ ] 7. Add comprehensive logging
  - [ ] 7.1 Add logging to template selection process
    - Log selected role category
    - Log role scores for all categories
    - Log role percentages for debugging
    - Log template path used
    - Log keyword matches when debugging enabled
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

  - [ ]* 7.2 Write property test for comprehensive logging
    - **Property 13: Comprehensive Logging**
    - **Validates: Requirements 7.1, 7.2, 7.3**

  - [ ] 7.3 Add error logging for failures
    - Log detailed errors for template selection failures
    - Log template load failures with file paths
    - Log fallback usage
    - _Requirements: 7.4_

- [ ] 8. Update API endpoints with percentage-based data
  - [ ] 8.1 Update analyze-job endpoint in lego_api.py
    - Include role category in response (already done)
    - Include template information for debugging (already done)
    - Add role_percentages field with percentage breakdown
    - Add role_breakdown field with ranked percentages (threshold 5%)
    - Include confidence scores
    - Add error handling with graceful responses
    - _Requirements: 8.1, 8.3, 8.5, 10.6_

  - [ ]* 8.2 Write property test for API response completeness
    - **Property 14: API Response Completeness**
    - **Validates: Requirements 8.1, 8.2, 8.3**

  - [ ]* 8.3 Write property test for API percentage inclusion
    - **Property 21: API Percentage Inclusion**
    - **Validates: Requirements 10.6**

  - [ ] 8.4 Update generate-lego-application endpoint
    - Already uses role category from analysis
    - Include percentage breakdown in response
    - Handle template selection failures gracefully
    - _Requirements: 8.2, 8.5, 10.6_

- [ ] 9. Implement template content alignment validation
  - [ ] 9.1 Add template content relevance checking
    - Verify template content aligns with role category
    - Log warnings for misaligned templates
    - Implement alternative template selection for misalignment
    - Add specific check to prevent FinTech template for pure DevOps jobs
    - _Requirements: 9.1, 9.2, 9.3, 9.5_

  - [ ]* 9.2 Write property test for template content alignment
    - **Property 15: Template Content Alignment**
    - **Validates: Requirements 9.2, 9.3**

  - [ ]* 9.3 Write unit test for CI/CD job not selecting FinTech template
    - Test that CI/CD job description does not select FinTech template
    - _Requirements: 9.1_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Documentation and deployment preparation
  - [ ] 11.1 Update API documentation
    - Document new response fields (role_percentages, role_breakdown)
    - Document AI configuration options
    - Add examples for different role types
    - _Requirements: 8.1, 8.3_

  - [ ] 11.2 Create deployment guide
    - Document environment variables
    - Document configuration file format
    - Add troubleshooting section
    - Document monitoring and logging

  - [ ]* 11.3 Write integration tests
    - Test complete workflow from job description to customized CV
    - Test with each role category
    - Test AI enabled and disabled modes
    - Test error scenarios and fallbacks

