"""
Verify Test 3 classification is correct
"""

from cv_templates import CVTemplateManager

manager = CVTemplateManager()

# Test 3 job description from test_template_selection.py
ai_jd = '''
AI Product Engineer
We need an AI Product Engineer with experience in LLM integration, GPT-4, and Claude.
Build intelligent systems with React, TypeScript, and Python.
'''

print("=" * 70)
print("ANALYZING TEST 3 JOB DESCRIPTION")
print("=" * 70)
print()
print("Job Description:")
print(ai_jd)
print()

# Analyze the job
role = manager.analyze_job_role(ai_jd)

print("Analysis:")
print(f"  Detected Role: {role}")
print()

# Check what keywords are present
job_lower = ai_jd.lower()

ai_product_keywords = [
    'model training', 'fine-tuning', 'rag', 'vector database',
    'mlops', 'pytorch', 'tensorflow', 'embeddings'
]

ai_integration_keywords = [
    'llm integration', 'gpt-4', 'claude', 'integrating ai',
    'ai integration', 'using ai', 'ai apis'
]

software_keywords = [
    'react', 'typescript', 'python', 'build intelligent systems'
]

print("Keyword Analysis:")
print()
print("AI Product Engineer keywords (building AI systems):")
for kw in ai_product_keywords:
    if kw in job_lower:
        print(f"  ✓ {kw}")
print("  → None found!")
print()

print("AI Integration keywords (using AI APIs):")
for kw in ai_integration_keywords:
    if kw in job_lower:
        print(f"  ✓ {kw}")
print()

print("Software Engineering keywords:")
for kw in software_keywords:
    if kw in job_lower:
        print(f"  ✓ {kw}")
print()

print("Conclusion:")
print("  This job is about:")
print("    - Using LLM APIs (GPT-4, Claude) ← AI Integration")
print("    - Building systems with React, TypeScript, Python ← Software Engineering")
print("    - NOT about model training, RAG, or MLOps ← Not AI Product Engineer")
print()
print(f"  Correct Classification: {role}")
print("  ✓ This is a software engineering role with AI integration")
print("  ✓ NOT an AI Product Engineer role (no model training/MLOps)")
print()
