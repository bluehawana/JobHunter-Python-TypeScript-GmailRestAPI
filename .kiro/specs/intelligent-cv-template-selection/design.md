# Design Document: Intelligent CV Template Selection

## Overview

The Intelligent CV Template Selection system enhances the job application automation by implementing a **percentage-based weighted scoring approach** to accurately match job descriptions with CV templates. 

**Key Problem Solved**: The previous keyword-based system would misclassify jobs - for example, a senior software engineering role that mentions "AI integration" would be incorrectly classified as "AI Product Engineer" and use an AI-focused CV template, even though the job is 85% software engineering, 10% AI integration, and 5% leadership.

**Solution**: The system now calculates percentage scores for each role category, ensuring that:
- A job that is 85% software engineering gets classified as a software engineering role
- AI keywords only contribute their proportional weight (10%) to the scoring
- The template selection uses the role with the highest percentage

The system uses keyword-based analysis as the foundation, with optional AI-enhanced semantic analysis for improved accuracy.

## Architecture

The system follows a layered architecture with clear separation of concerns:

### Core Components

1. **Job Analyzer**: Extracts keywords and role indicators from job descriptions
2. **Template Matcher**: Scores and selects the best matching template
3. **Template Loader**: Loads and validates template files
4. **Template Customizer**: Customizes templates with job-specific information
5. **AI Analyzer (Optional)**: Provides semantic analysis using AI models

### Data Flow

```
Job Description → Job Analyzer → Template Matcher → Template Loader → Template Customizer → Customized CV
                       ↓                 ↓
                  AI Analyzer       Calculate Raw Scores
                   (optional)            ↓
                       ↓            Normalize to Percentages
                  Enhanced              ↓
                   Scoring         Select Highest %
```

### Weighted Scoring Algorithm

The system uses a multi-step scoring process:

1. **Keyword Extraction**: Extract all technical keywords from job description
2. **Raw Score Calculation**: For each role category, count matching keywords weighted by priority
   - Formula: `raw_score = Σ(keyword_matches) / priority`
   - Lower priority = higher importance (priority 1 is most important)
3. **Percentage Normalization**: Convert raw scores to percentages that sum to 100%
   - Formula: `percentage = (raw_score / Σ(all_raw_scores)) × 100`
4. **Template Selection**: Select the role with the highest percentage

**Example**:
- Job mentions: React (10x), Python (8x), Flask (5x), "AI integration" (2x), "LLM" (1x)
- Software Engineering score: (10+8+5)/1 = 23
- AI Product Engineer score: (2+1)/1 = 3
- Total: 26
- Percentages: Software Engineering = 88%, AI Product Engineer = 12%
- **Selected Template**: Software Engineering (not AI Product Engineer)

## Components and Interfaces

### 1. CVTemplateManager (Enhanced)

The central component managing all template operations.

**Responsibilities:**
- Maintain role category definitions with keywords and priorities
- Analyze job descriptions to determine role type
- Score and select the best matching template
- Load and validate template files
- Provide diagnostic information

**Interface:**
```python
class CVTemplateManager:
    def analyze_job_role(self, job_description: str, use_ai: bool = False) -> str
    def get_template_path(self, role_category: str) -> Optional[Path]
    def load_template(self, role_category: str) -> Optional[str]
    def get_role_info(self, role_category: str) -> Dict
    def get_role_scores(self, job_description: str) -> Dict[str, float]
    def get_role_percentages(self, job_description: str) -> Dict[str, float]
    def get_role_breakdown(self, job_description: str, threshold: float = 5.0) -> List[Tuple[str, float]]
    def list_available_templates(self) -> List[Dict]
```

### 2. JobAnalyzer

Extracts keywords and analyzes job descriptions.

**Responsibilities:**
- Extract technical keywords from job descriptions
- Identify role-specific terms
- Count keyword occurrences with word boundary matching
- Normalize text for analysis

**Interface:**
```python
class JobAnalyzer:
    def extract_keywords(self, job_description: str) -> List[str]
    def count_keyword_occurrences(self, text: str, keyword: str) -> int
    def normalize_text(self, text: str) -> str
    def identify_role_indicators(self, job_description: str) -> Dict[str, int]
```

### 3. TemplateMatcher

Scores templates and selects the best match.

**Responsibilities:**
- Calculate weighted scores for each role category
- Normalize scores to percentages (0-100%)
- Apply priority weighting
- Handle tie-breaking scenarios
- Provide confidence scores and role breakdowns

**Interface:**
```python
class TemplateMatcher:
    def calculate_scores(self, keyword_counts: Dict[str, int], role_categories: Dict) -> Dict[str, float]
    def calculate_percentages(self, scores: Dict[str, float]) -> Dict[str, float]
    def get_role_breakdown(self, percentages: Dict[str, float], threshold: float = 5.0) -> List[Tuple[str, float]]
    def select_best_match(self, scores: Dict[str, float]) -> Tuple[str, float]
    def get_fallback_template(self, excluded: List[str]) -> str
```

### 4. AIAnalyzer (Optional)

Provides AI-enhanced semantic analysis using Minimax M2 API.

**Responsibilities:**
- Analyze job descriptions using Minimax M2 model
- Extract semantic meaning beyond keywords
- Provide confidence scores
- Handle API failures gracefully

**Interface:**
```python
class AIAnalyzer:
    def __init__(self, api_key: str, model: str = "abab6.5s-chat")
    def analyze_job_description(self, job_description: str) -> Dict
    def extract_role_type(self, job_description: str) -> Tuple[str, float]
    def is_available(self) -> bool
```

**Minimax M2 Integration:**
- API Endpoint: `https://api.minimax.chat/v1/text/chatcompletion_v2`
- Model: `abab6.5s-chat` (Minimax M2)
- Authentication: Bearer token from environment variable
- Request format: JSON with messages array
- Response parsing: Extract role category and confidence from AI response

### 5. TemplateCustomizer

Customizes templates with job-specific information.

**Responsibilities:**
- Replace placeholder text
- Escape LaTeX special characters
- Update job titles and company names
- Preserve template structure

**Interface:**
```python
class TemplateCustomizer:
    def customize_template(self, template_content: str, company: str, title: str, role_type: str) -> str
    def escape_latex_chars(self, text: str) -> str
    def replace_placeholders(self, template: str, replacements: Dict[str, str]) -> str
```

## Data Models

### RoleCategory

```python
@dataclass
class RoleCategory:
    key: str
    display_name: str
    keywords: List[str]
    template_path: str
    priority: int
    description: str
```

### TemplateMatch

```python
@dataclass
class TemplateMatch:
    role_category: str
    score: float
    percentage: float
    confidence: float
    template_path: Path
    keyword_matches: Dict[str, int]
    ai_enhanced: bool = False
```

### RoleBreakdown

```python
@dataclass
class RoleBreakdown:
    role_category: str
    percentage: float
    score: float
    keyword_matches: Dict[str, int]
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    role_type: str
    role_category: str
    keywords: List[str]
    required_skills: List[str]
    company: str
    title: str
    template_match: TemplateMatch
    scores: Dict[str, float]
    percentages: Dict[str, float]
    role_breakdown: List[RoleBreakdown]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Keyword Extraction Completeness
*For any* job description containing known technical keywords, the extraction function should identify and return all present keywords with correct word boundary matching.
**Validates: Requirements 1.1, 1.4, 1.5**

### Property 2: Role Score Calculation
*For any* job description with multiple role keywords, the system should calculate a weighted score for each role category by dividing raw keyword counts by priority values.
**Validates: Requirements 1.3, 4.3**

### Property 3: Best Match Selection
*For any* set of role scores, the system should select the role category with the highest weighted score as the best match.
**Validates: Requirements 2.1**

### Property 4: Template Diversity
*For any* set of diverse job descriptions (Android, DevOps, SRE, Full-stack), the system should select different templates, not defaulting to a single template.
**Validates: Requirements 2.9**

### Property 5: Role Category Structure
*For any* role category in the system, it should have both a non-empty list of keywords and a positive integer priority value.
**Validates: Requirements 4.1, 4.2**

### Property 6: Multi-word Keyword Support
*For any* multi-word keyword phrase (e.g., "full stack", "site reliability"), the system should treat it as a single matching unit, not as separate words.
**Validates: Requirements 4.5**

### Property 7: Template File Existence Verification
*For any* template selection, the system should verify the template file exists before attempting to use it.
**Validates: Requirements 2.7**

### Property 8: Path Format Consistency
*For any* template path in the system configuration, it should follow a consistent format (either all relative or properly resolved absolute paths).
**Validates: Requirements 3.1, 3.4**

### Property 9: Template Loading Success
*For any* valid template file path, the system should successfully load the file content with UTF-8 encoding.
**Validates: Requirements 5.1, 5.2**

### Property 10: LaTeX Structure Validation
*For any* loaded or customized template, it should contain required LaTeX structure markers (\documentclass, \begin{document}, \end{document}) and maintain valid LaTeX formatting.
**Validates: Requirements 5.4, 6.4, 6.5**

### Property 11: Placeholder Replacement
*For any* template with placeholders and job-specific information (company, title), all placeholders should be replaced with the provided values in the customized output.
**Validates: Requirements 6.1, 6.2**

### Property 12: LaTeX Character Escaping
*For any* job title or company name containing LaTeX special characters (&, %, $, #, _, {, }, ~, ^, \), those characters should be properly escaped in the customized template.
**Validates: Requirements 6.3**

### Property 13: Comprehensive Logging
*For any* template selection operation, the system should log the selected role category, role scores, and template path used.
**Validates: Requirements 7.1, 7.2, 7.3**

### Property 14: API Response Completeness
*For any* successful API call (analyze-job or generate-lego-application), the response should include the selected role category and template information.
**Validates: Requirements 8.1, 8.2, 8.3**

### Property 15: Template Content Alignment
*For any* template selection, the template content should align with the detected role category (e.g., DevOps templates for DevOps jobs, not FinTech templates).
**Validates: Requirements 9.2, 9.3**

### Property 16: Percentage Calculation for All Roles
*For any* job description, the system should calculate percentage scores for all configured role categories.
**Validates: Requirements 10.1**

### Property 17: Percentage Normalization
*For any* set of raw role scores, when normalized to percentages, the sum of all percentages should equal 100% (within floating-point precision tolerance of 0.01%).
**Validates: Requirements 10.2**

### Property 18: Role Breakdown Filtering
*For any* percentage distribution, the role breakdown should include only roles with percentages at or above the specified threshold (default 5%).
**Validates: Requirements 10.3**

### Property 19: Role Breakdown Ordering
*For any* role breakdown, the roles should be ordered in descending order by percentage score.
**Validates: Requirements 10.4**

### Property 20: Mixed Role Warning
*For any* job analysis where the highest role percentage is below 50%, the system should log a warning about mixed role composition.
**Validates: Requirements 10.5**

### Property 21: API Percentage Inclusion
*For any* API response containing role analysis, it should include a percentage breakdown field with all significant roles.
**Validates: Requirements 10.6**

### Property 22: Template Selection by Highest Percentage
*For any* percentage distribution, the selected template role should be the role with the maximum percentage score.
**Validates: Requirements 10.7**

### Property 23: AI Misclassification Prevention
*For any* job description where software engineering keywords significantly outnumber AI keywords (ratio > 3:1), the system should classify it as a software engineering role, not an AI Product Engineer role.
**Validates: Requirements 11.1, 11.5**

### Property 24: AI Integration vs AI Product Distinction
*For any* job description mentioning "integrating AI", "using LLMs", or "AI-powered features", these keywords should contribute to software engineering scores, not AI Product Engineer scores.
**Validates: Requirements 11.3, 11.6**

## Error Handling

### Template Selection Failures

**Scenario**: Selected template file does not exist
- **Action**: Log error with template path and role category
- **Fallback**: Select next best matching template based on scores
- **User Impact**: Transparent - user receives alternative template

**Scenario**: No templates match job description
- **Action**: Log warning with job description summary
- **Fallback**: Use default general-purpose template (devops_cloud)
- **User Impact**: User receives general template with notification

**Scenario**: Template file is corrupted or invalid LaTeX
- **Action**: Log error with file path and validation failure details
- **Fallback**: Attempt to load fallback template
- **User Impact**: User receives fallback template or error message

### AI Analysis Failures

**Scenario**: AI API key not configured
- **Action**: Log info message
- **Fallback**: Use keyword-based analysis
- **User Impact**: Transparent - keyword analysis still works

**Scenario**: AI API call fails (timeout, rate limit, error)
- **Action**: Log error with API response details
- **Fallback**: Use keyword-based analysis
- **User Impact**: Transparent - keyword analysis provides results

**Scenario**: AI returns invalid or unexpected response
- **Action**: Log warning with response content
- **Fallback**: Use keyword-based analysis
- **User Impact**: Transparent - keyword analysis provides results

### File System Errors

**Scenario**: Template directory not accessible
- **Action**: Log critical error with directory path
- **Fallback**: Use embedded fallback templates
- **User Impact**: User receives basic template or error message

**Scenario**: Permission denied reading template file
- **Action**: Log error with file path and permissions
- **Fallback**: Try alternative template or use embedded template
- **User Impact**: User receives alternative template

## Testing Strategy

### Unit Testing

The system will use pytest for unit testing with the following focus areas:

**JobAnalyzer Tests**:
- Test keyword extraction with various job descriptions
- Test word boundary matching (e.g., "cloud" vs "cloudformation")
- Test text normalization
- Test edge cases (empty text, special characters, very long text)

**TemplateMatcher Tests**:
- Test score calculation with known keyword counts
- Test priority weighting
- Test best match selection with various score distributions
- Test tie-breaking scenarios
- Test fallback selection

**CVTemplateManager Tests**:
- Test role detection with sample job descriptions
- Test template path resolution
- Test template loading
- Test error handling for missing files

**TemplateCustomizer Tests**:
- Test placeholder replacement
- Test LaTeX character escaping
- Test structure preservation
- Test edge cases (empty values, special characters)

### Property-Based Testing

The system will use Hypothesis (Python) for property-based testing with a minimum of 100 iterations per test.

**Property Test Configuration**:
```python
from hypothesis import given, settings
import hypothesis.strategies as st

@settings(max_examples=100)
```

**Test Generators**:
- Job description generator: Creates realistic job descriptions with varying keywords
- Keyword generator: Generates valid technical keywords
- Role category generator: Generates valid role category configurations
- Template content generator: Generates valid LaTeX template structures
- File path generator: Generates valid file paths (relative and absolute)

### Integration Testing

**API Integration Tests**:
- Test analyze-job endpoint with various job descriptions
- Test generate-lego-application endpoint with different role categories
- Test error responses for invalid inputs
- Test AI fallback when AI is unavailable

**File System Integration Tests**:
- Test template loading from actual file system
- Test path resolution with real directories
- Test error handling with missing files

### End-to-End Testing

**Complete Workflow Tests**:
1. Submit job description → Analyze → Select template → Load template → Customize → Verify output
2. Test with each role category (Android, DevOps, SRE, Full-stack, etc.)
3. Test with edge cases (no matches, multiple strong matches)
4. Test with AI enabled and disabled

## Performance Considerations

### Keyword-Based Analysis

**Target**: < 2 seconds for typical job descriptions (500-2000 words)

**Optimizations**:
- Pre-compile regex patterns for word boundary matching
- Cache role category definitions
- Use efficient string matching algorithms
- Limit keyword list to most discriminative terms

### AI-Enhanced Analysis

**Target**: < 5 seconds for typical job descriptions

**Optimizations**:
- Use streaming API responses when available
- Implement request timeout (5 seconds)
- Cache AI responses for identical job descriptions (optional)
- Use lightweight AI models when possible

### Template Loading

**Target**: < 100ms per template

**Optimizations**:
- Cache loaded templates in memory
- Use lazy loading for templates
- Implement template preloading for common roles

## Security Considerations

### AI API Keys

- Store API keys in environment variables, never in code
- Use secure key management services (e.g., AWS Secrets Manager)
- Rotate API keys regularly
- Implement rate limiting to prevent API abuse
- Log API usage for monitoring

### File System Access

- Validate all file paths to prevent directory traversal attacks
- Restrict template loading to designated directories
- Implement file size limits to prevent resource exhaustion
- Validate file content before processing

### Input Validation

- Sanitize job description input to prevent injection attacks
- Limit job description length (e.g., 50KB max)
- Validate company and title inputs before LaTeX insertion
- Escape all user-provided content in LaTeX output

## Deployment Considerations

### Configuration Management

**Environment Variables**:
```
AI_ENABLED=true|false
MINIMAX_API_KEY=<minimax_api_key>
AI_MODEL=abab6.5s-chat
TEMPLATE_DIR=/path/to/templates
LOG_LEVEL=INFO|DEBUG
```

**Configuration File** (optional):
```json
{
  "role_categories": {
    "android_developer": {
      "keywords": ["android", "kotlin", "java", "mobile"],
      "template_path": "job_applications/ecarx_android_developer",
      "priority": 1
    }
  },
  "ai_config": {
    "enabled": true,
    "model": "gpt-4",
    "timeout": 5
  }
}
```

### Monitoring and Logging

**Metrics to Track**:
- Template selection success rate
- Template selection time (p50, p95, p99)
- AI analysis success rate
- AI analysis time
- Fallback usage frequency
- Template load failures

**Log Levels**:
- DEBUG: Keyword matches, scores, detailed analysis
- INFO: Template selection, role detection
- WARNING: Fallback usage, AI failures
- ERROR: Template load failures, critical errors

### Backward Compatibility

- Maintain support for existing API contracts
- Provide migration path for old template formats
- Support both AI and non-AI modes
- Graceful degradation when new features unavailable

## Future Enhancements

1. **Template Versioning**: Track template versions and allow rollback
2. **A/B Testing**: Test different template selection strategies
3. **User Feedback Loop**: Learn from user template preferences
4. **Custom Templates**: Allow users to upload custom templates
5. **Multi-language Support**: Support job descriptions in multiple languages
6. **Template Recommendations**: Suggest template improvements based on job requirements
7. **Batch Processing**: Analyze multiple job descriptions efficiently
8. **Template Analytics**: Track which templates perform best for different roles
