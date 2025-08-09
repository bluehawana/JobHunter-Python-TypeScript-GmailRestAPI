# 🤖 Claude API Usage Breakdown - What We Built

## 📊 Claude API Token Usage Explanation

Yesterday you saw **Sonnet 3.7 token usage** because we implemented a comprehensive AI-powered job application system. Here's exactly what Claude is doing:

## 🎯 Primary Claude API Functions

### 1. **Job Analysis & LEGO Strategy** 🧠
**Location**: `improved_working_automation.py` → `_get_claude_lego_strategy()`
**What it does**:
```python
# Claude analyzes each job posting and decides:
- Primary focus: DevOps/Backend/Frontend/Fullstack
- Skills to highlight: Which technical skills to emphasize
- Experience order: Which job experience should lead
- Profile angle: How to position you for this specific role
- Keywords to include: ATS optimization terms
- Tone: Professional tone to match company culture
```

**Example prompt sent to Claude**:
```
Analyze this job and create LEGO strategy for Hongzhi Li:

Job: Senior Backend Developer at Spotify
Description: Java, Spring Boot, microservices, Kubernetes, AWS, international team

Return JSON:
{
    "primary_focus": "backend",
    "skills_to_highlight": ["Java", "Spring Boot", "AWS"],
    "role_title": "Backend Developer & API Specialist"
}
```

### 2. **Resume Customization** 📄
**Location**: `improved_working_automation.py` → `_build_claude_lego_resume()`
**What it does**:
- Takes your exact LaTeX template
- Applies Claude's LEGO strategy to customize content
- Tailors profile summary based on job requirements
- Reorders and emphasizes skills based on job keywords
- Integrates ATS-friendly keywords naturally

**Token usage**: ~1000-1500 tokens per resume

### 3. **Cover Letter Personalization** 💌
**Location**: `improved_working_automation.py` → `_build_claude_cover_letter()`
**What it does**:
- Creates personalized cover letters focusing on soft skills
- Emphasizes cross-cultural bridge building (Chinese-Swedish)
- Highlights business-IT translation abilities
- Adapts tone for different industries (automotive, music tech, etc.)

**Token usage**: ~800-1200 tokens per cover letter

## 🔄 Multiple Automation Systems Using Claude

We built **several different automation systems**, each using Claude:

### 1. **Improved Working Automation** (Main System)
- File: `improved_working_automation.py`
- Uses Claude for job analysis + resume/cover letter generation
- **Most active system** - likely source of your token usage

### 2. **LEGO Mode Automation**
- File: `lego_mode_automation.py`
- Uses Claude for intelligent LEGO component selection
- Focuses on using your exact LaTeX templates

### 3. **True Template Automation**
- File: `true_template_automation.py`
- Uses Claude for template customization
- Maintains your exact formatting while customizing content

### 4. **LEGO Automation System**
- File: `lego_automation_system.py`
- Uses Claude for component-based customization

## 📈 Token Usage Breakdown

**Per Job Application** (when Claude API works):
- Job analysis: ~300-500 tokens
- Resume generation: ~1000-1500 tokens  
- Cover letter: ~800-1200 tokens
- **Total per job**: ~2100-3200 tokens

**If you processed 10 jobs yesterday**: ~21,000-32,000 tokens
**If you processed 20 jobs yesterday**: ~42,000-64,000 tokens

## 🎯 What Claude is NOT Doing

❌ **Not generating templates from scratch** - We use your exact LaTeX templates
❌ **Not replacing your content** - We enhance and tailor your existing content
❌ **Not changing your formatting** - We maintain your professional LaTeX structure

## ✅ What Claude IS Doing

✅ **Analyzing job requirements** to understand what employers want
✅ **Deciding LEGO strategy** - which skills to highlight for each job
✅ **Customizing your content** to match specific job requirements
✅ **Optimizing for ATS** by naturally integrating relevant keywords
✅ **Personalizing cover letters** with soft skills and cultural fit

## 🔧 Current Configuration

**Model**: `claude-3-7-sonnet-20250219` (Third-party API)
**Fallback**: `claude-3-5-sonnet-20241022` (Your official API - low credits)
**Cost optimization**: 1500 max tokens, temperature 0.2

## 💡 Why Token Usage Happened

The token usage you saw yesterday was from:

1. **Testing the system** - We ran multiple test jobs
2. **Multiple automation files** - Each system we built uses Claude
3. **Retry logic** - When third-party API fails, it retries multiple times
4. **Complete workflow** - Job analysis + resume + cover letter for each job

## 🎯 Current Status

**Third-party API**: Currently overloaded (timeouts)
**Official API**: Low credits  
**Intelligent Fallback**: Working perfectly without Claude
**System**: Fully operational with or without Claude

The system is designed to work with Claude for maximum intelligence, but falls back to smart keyword analysis when Claude is unavailable - ensuring you never miss job opportunities!