# Requirements Document

## Introduction

The Intelligent CV Template Selection system enhances the job application automation by ensuring that when a new job description is pasted, the system intelligently selects the most relevant CV template based on the job requirements. The system uses a **percentage-based weighted scoring approach** to accurately classify jobs with mixed responsibilities (e.g., a job that is 85% senior software engineering, 10% AI integration, 5% leadership should use a software engineering template, not an AI template).

This prevents misclassification where the presence of AI keywords causes the system to incorrectly select an "AI Product Engineer" template for a job that is primarily software engineering with some AI integration work.

## Glossary

- **CV Template**: A LaTeX-formatted resume document tailored for a specific role type (e.g., Android Developer, DevOps Engineer)
- **Job Description (JD)**: Text describing a job position, including requirements, responsibilities, and qualifications
- **Role Category**: A classification of job types (e.g., android_developer, devops_cloud, incident_management_sre)
- **Template Manager**: The system component responsible for analyzing job descriptions and selecting appropriate templates
- **Keyword Matching**: The process of identifying relevant terms in a job description to determine role type
- **Template Path**: The file system location of a CV template file
- **Role Percentage**: A normalized score (0-100%) indicating how much a job description matches a specific role category
- **Role Breakdown**: A distribution showing percentage scores for all significant role categories in a job description
- **Weighted Scoring**: A scoring method that considers both keyword frequency and keyword importance to calculate accurate role percentages
- **Primary Role**: The role category with the highest percentage score, used for template selection

## Requirements

### Requirement 1: Job Description Analysis

**User Story:** As a job seeker, I want the system to analyze my job description and identify the role type, so that the most relevant CV template is selected automatically.

#### Acceptance Criteria

1. WHEN a user provides a job description THEN the system SHALL extract keywords related to technical skills and role types
2. WHEN analyzing a job description THEN the system SHALL identify role-specific terms such as "Android", "Kubernetes", "incident management", "full-stack", "CI/CD", "Jenkins", "Gerrit"
3. WHEN multiple role keywords are present THEN the system SHALL calculate a weighted score for each role category
4. WHEN scoring role categories THEN the system SHALL count keyword occurrences using word boundary matching
5. WHEN scoring role categories THEN the system SHALL prioritize exact keyword matches over partial matches
6. WHEN no clear role match is found THEN the system SHALL default to the most general template category

### Requirement 2: Template Selection Logic

**User Story:** As a job seeker, I want the system to select the CV template that best matches the job requirements, so that my application highlights the most relevant experience and avoids irrelevant content.

#### Acceptance Criteria

1. WHEN role scores are calculated THEN the system SHALL select the template with the highest weighted score
2. WHEN an Android-related job is detected THEN the system SHALL select the Android developer template
3. WHEN a CI/CD or DevOps job is detected THEN the system SHALL select the DevOps cloud template
4. WHEN an incident management or SRE job is detected THEN the system SHALL select the incident management template
5. WHEN a full-stack development job is detected THEN the system SHALL select the full-stack developer template
6. WHEN a FinTech-focused job is detected THEN the system SHALL select a template emphasizing financial domain experience
7. WHEN template selection occurs THEN the system SHALL verify the template file exists before using it
8. IF the selected template does not exist THEN the system SHALL fall back to the next best matching template
9. WHEN a template is selected THEN the system SHALL NOT default to a single template regardless of job type

### Requirement 3: Template Path Management

**User Story:** As a system administrator, I want template paths to be consistently managed, so that templates can be reliably located and loaded.

#### Acceptance Criteria

1. WHEN storing template paths THEN the system SHALL use consistent path formats for all templates
2. WHEN a template is in a directory THEN the system SHALL locate CV files using the pattern "*_CV.tex"
3. WHEN a template is a single file THEN the system SHALL use the direct file path
4. WHEN resolving template paths THEN the system SHALL handle both absolute and relative paths correctly
5. WHEN a template path is invalid THEN the system SHALL log an error and attempt fallback selection

### Requirement 4: Role Category Configuration

**User Story:** As a system administrator, I want to configure role categories with keywords and priorities, so that template matching can be tuned for accuracy.

#### Acceptance Criteria

1. WHEN defining role categories THEN the system SHALL associate each category with a list of keywords
2. WHEN defining role categories THEN the system SHALL assign a priority value to each category
3. WHEN calculating weighted scores THEN the system SHALL divide raw scores by priority values
4. WHEN updating role categories THEN the system SHALL support adding new categories without code changes
5. WHEN keywords are defined THEN the system SHALL support multi-word phrases as single keywords

### Requirement 5: Template Loading and Validation

**User Story:** As a job seeker, I want the system to load the correct template content, so that my CV is generated using the appropriate format and content.

#### Acceptance Criteria

1. WHEN a template is selected THEN the system SHALL load the template file content
2. WHEN loading a template THEN the system SHALL handle file encoding correctly (UTF-8)
3. WHEN a template fails to load THEN the system SHALL return an error message with details
4. WHEN template content is loaded THEN the system SHALL validate it contains LaTeX document structure
5. IF template loading fails THEN the system SHALL attempt to load a fallback template

### Requirement 6: Template Customization

**User Story:** As a job seeker, I want the selected template to be customized with the job-specific information, so that my CV is tailored to each application.

#### Acceptance Criteria

1. WHEN a template is loaded THEN the system SHALL replace placeholder text with job-specific information
2. WHEN customizing a template THEN the system SHALL update the job title in the CV header
3. WHEN customizing a template THEN the system SHALL escape special LaTeX characters in job titles
4. WHEN customizing a template THEN the system SHALL preserve the original template structure
5. WHEN customization occurs THEN the system SHALL maintain proper LaTeX formatting

### Requirement 7: Diagnostic and Debugging

**User Story:** As a developer, I want to see which template was selected and why, so that I can debug and improve the selection logic.

#### Acceptance Criteria

1. WHEN template selection occurs THEN the system SHALL log the selected role category
2. WHEN scoring role categories THEN the system SHALL log the scores for each category
3. WHEN a template is loaded THEN the system SHALL log the template path used
4. WHEN template selection fails THEN the system SHALL log detailed error information
5. WHEN debugging is enabled THEN the system SHALL provide keyword match details for each role category

### Requirement 8: API Integration

**User Story:** As a frontend developer, I want the template selection to integrate seamlessly with the existing API, so that users experience no disruption.

#### Acceptance Criteria

1. WHEN the analyze-job API is called THEN the system SHALL include the selected role category in the response
2. WHEN the generate-lego-application API is called THEN the system SHALL use the role category to select the template
3. WHEN API responses are returned THEN the system SHALL include template information for debugging
4. WHEN template selection occurs THEN the system SHALL complete within 2 seconds for typical job descriptions
5. IF template selection fails THEN the system SHALL return a graceful error response with fallback options

### Requirement 9: Template Content Relevance

**User Story:** As a job seeker, I want my CV to emphasize experience relevant to the job, so that I don't submit applications with irrelevant content like FinTech experience for a pure DevOps role.

#### Acceptance Criteria

1. WHEN a CI/CD DevOps job is detected THEN the system SHALL NOT select a template emphasizing FinTech or financial domain experience
2. WHEN a template is selected THEN the system SHALL ensure the template content aligns with the detected role category
3. WHEN multiple templates could match THEN the system SHALL select the template with the most relevant technical focus
4. WHEN a job emphasizes specific tools (Jenkins, Gerrit, Artifactory) THEN the system SHALL select a template highlighting those or similar tools
5. WHEN template content is irrelevant to the job THEN the system SHALL log a warning and attempt alternative template selection

### Requirement 10: Percentage-Based Role Scoring

**User Story:** As a job seeker, I want to see what percentage of the job matches different role categories, so that I understand the job composition and can verify the template selection is appropriate.

#### Acceptance Criteria

1. WHEN analyzing a job description THEN the system SHALL calculate percentage scores for all role categories
2. WHEN calculating percentages THEN the system SHALL normalize raw scores so all percentages sum to 100%
3. WHEN displaying role breakdown THEN the system SHALL show all roles with scores above 5%
4. WHEN a job matches multiple roles THEN the system SHALL return a ranked list of role percentages
5. WHEN the primary role is below 50% THEN the system SHALL log a warning indicating mixed role composition
6. WHEN API responses include role analysis THEN the system SHALL include the percentage breakdown for all significant roles
7. WHEN selecting a template THEN the system SHALL use the role with the highest percentage score

### Requirement 11: Prevent AI Misclassification

**User Story:** As a job seeker applying for senior software engineering roles that mention AI integration, I want the system to recognize these as software engineering jobs (not AI Product Engineer jobs), so that my CV emphasizes software engineering experience rather than AI/ML expertise.

#### Acceptance Criteria

1. WHEN a job description is primarily software engineering (>70%) with minor AI mentions (<20%) THEN the system SHALL classify it as a software engineering role
2. WHEN calculating role percentages THEN the system SHALL weight software engineering keywords higher than AI integration keywords
3. WHEN a job mentions "integrating AI", "using LLMs", "AI-powered features" THEN the system SHALL treat these as software engineering tasks, not AI Product Engineer tasks
4. WHEN a job is classified as AI Product Engineer THEN the system SHALL verify that AI/ML work comprises at least 50% of the role responsibilities
5. WHEN a job emphasizes building software with AI features THEN the system SHALL select fullstack_developer or backend_developer templates, not ai_product_engineer
6. WHEN displaying role breakdown THEN the system SHALL clearly distinguish between "AI Product Engineer" (building AI systems) and "Software Engineer with AI" (using AI APIs)

### Requirement 12: AI-Enhanced Analysis (Optional)

**User Story:** As a job seeker, I want the system to use AI to better understand job descriptions and template matching, so that template selection is more accurate than keyword matching alone.

#### Acceptance Criteria

1. WHERE AI analysis is enabled THEN the system SHALL use an AI model to analyze job descriptions
2. WHERE AI analysis is enabled THEN the system SHALL extract semantic meaning beyond simple keyword matching
3. WHERE AI analysis is enabled THEN the system SHALL identify implicit role requirements not explicitly stated
4. WHERE AI analysis is enabled THEN the system SHALL provide confidence scores for template matches
5. WHERE AI API keys are configured THEN the system SHALL use AI analysis as the primary method
6. IF AI analysis fails or is unavailable THEN the system SHALL fall back to keyword-based analysis
7. WHEN using AI analysis THEN the system SHALL complete within 5 seconds for typical job descriptions
