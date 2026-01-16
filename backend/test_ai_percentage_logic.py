"""
Test AI percentage-based classification logic
Verify that AI Product Engineer requires 50%+ AI-specific work
"""

from cv_templates import CVTemplateManager

def test_percentage_based_classification():
    """Test that AI classification uses percentage-based logic"""
    manager = CVTemplateManager()
    
    # Test: Job with 85% software engineering, 15% AI integration
    # Should classify as software engineering, not AI
    job_desc = """
    Senior Software Engineer - AI Integration
    
    We're building the next generation of web applications with AI capabilities.
    
    Responsibilities:
    - Design and build fullstack web applications using React and TypeScript
    - Develop backend services with Python, Flask, and FastAPI
    - Create RESTful APIs and microservices architecture
    - Implement frontend components with React, Vue, and Angular
    - Work with PostgreSQL, MongoDB, and Redis databases
    - Build CI/CD pipelines with Docker and Kubernetes
    - Integrate AI-powered features using OpenAI API
    - Leverage AI capabilities to enhance user experience
    - Use LLM integration for chatbot features
    - Deploy AI solutions to production
    - Mentor junior developers and lead technical discussions
    - Collaborate with product team on feature development
    - Write clean, maintainable code with TypeScript and JavaScript
    - Implement automated testing with Jest and Pytest
    - Optimize application performance and scalability
    
    Requirements:
    - 5+ years of fullstack development experience
    - Strong experience with React, TypeScript, and JavaScript
    - Expert knowledge of Python, Flask, and FastAPI
    - Experience with microservices and RESTful APIs
    - Knowledge of PostgreSQL, MongoDB, and Redis
    - Experience with Docker, Kubernetes, and CI/CD
    - Familiarity with AI APIs (OpenAI, Claude) is a plus
    - Experience integrating AI into web applications
    - Strong problem-solving and communication skills
    """
    
    result = manager.analyze_job_role(job_desc)
    
    print("=" * 70)
    print("PERCENTAGE-BASED AI CLASSIFICATION TEST")
    print("=" * 70)
    print()
    print("Job Description Analysis:")
    print("  - Heavy emphasis on fullstack development (React, TypeScript, Python)")
    print("  - Multiple mentions of web development, APIs, databases")
    print("  - Minor mentions of AI integration (using APIs, not building models)")
    print()
    print("Expected Behavior:")
    print("  - AI keywords should contribute ~10-15% to total score")
    print("  - Software engineering keywords should dominate (~85%)")
    print("  - Since AI < 50%, should NOT classify as ai_product_engineer")
    print()
    print(f"Result: {result}")
    print()
    
    if result in ['fullstack_developer', 'backend_developer']:
        print("✓ PASS - Correctly classified as software engineering role")
        print("  The 50% threshold prevented AI misclassification")
    else:
        print(f"✗ FAIL - Incorrectly classified as {result}")
        print("  Expected fullstack_developer or backend_developer")
    print()
    
    # Test 2: Job with 60% AI work, 40% software engineering
    # Should classify as AI Product Engineer
    job_desc_2 = """
    AI Product Engineer
    
    Build and deploy machine learning systems at scale.
    
    Responsibilities:
    - Train and fine-tune large language models using PyTorch
    - Build RAG systems with vector databases (Pinecone, Weaviate)
    - Implement MLOps pipelines for model deployment
    - Design embeddings systems for semantic search
    - Work with Hugging Face, LangChain, and LlamaIndex
    - Deploy models using model serving infrastructure
    - Optimize model performance and latency
    - Build data pipelines for model training
    - Implement feature engineering for ML models
    - Work with Python and FastAPI for model APIs
    - Collaborate with data science team
    
    Requirements:
    - Strong experience with model training and fine-tuning
    - Expert knowledge of PyTorch or TensorFlow
    - Experience with vector databases and embeddings
    - Knowledge of RAG and retrieval-augmented generation
    - Experience with MLOps and model deployment
    - Python programming skills
    """
    
    result_2 = manager.analyze_job_role(job_desc_2)
    
    print("=" * 70)
    print("TEST 2: High AI Content (>50%)")
    print("=" * 70)
    print()
    print("Job Description Analysis:")
    print("  - Heavy emphasis on model training, fine-tuning, RAG")
    print("  - Multiple mentions of MLOps, vector databases, embeddings")
    print("  - Minor mentions of general software engineering")
    print()
    print(f"Result: {result_2}")
    print()
    
    if result_2 == 'ai_product_engineer':
        print("✓ PASS - Correctly classified as AI Product Engineer")
        print("  AI work exceeds 50% threshold")
    else:
        print(f"✗ FAIL - Incorrectly classified as {result_2}")
        print("  Expected ai_product_engineer")
    print()

if __name__ == '__main__':
    test_percentage_based_classification()
