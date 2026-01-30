"""
Test AI classification prevention
Verify that jobs with AI integration are classified as software engineering roles,
not AI Product Engineer roles.
"""

from cv_templates import CVTemplateManager

def test_ai_misclassification_prevention():
    """Test that AI integration keywords don't override software engineering classification"""
    manager = CVTemplateManager()
    
    # Test 1: Senior Software Engineer with AI integration (should NOT be AI Product Engineer)
    job_desc_1 = """
    Senior Software Engineer
    
    We're looking for a senior software engineer to build our next-generation web platform.
    You'll work with React, TypeScript, Node.js, and Python to create scalable applications.
    
    Responsibilities:
    - Build fullstack web applications using React and Node.js
    - Design and implement RESTful APIs
    - Integrate AI-powered features using OpenAI API
    - Leverage AI capabilities to enhance user experience
    - Work with PostgreSQL and Redis
    - Mentor junior developers
    
    Requirements:
    - 5+ years of software development experience
    - Strong experience with React, TypeScript, and Python
    - Experience integrating AI APIs (OpenAI, Claude)
    - Experience with microservices architecture
    """
    
    result_1 = manager.analyze_job_role(job_desc_1)
    print(f"Test 1 - Senior Software Engineer with AI integration:")
    print(f"  Expected: fullstack_developer or backend_developer")
    print(f"  Got: {result_1}")
    print(f"  ✓ PASS" if result_1 in ['fullstack_developer', 'backend_developer'] else "  ✗ FAIL")
    print()
    
    # Test 2: True AI Product Engineer (should be AI Product Engineer)
    job_desc_2 = """
    AI Product Engineer
    
    We're looking for an AI Product Engineer to build and deploy machine learning models.
    
    Responsibilities:
    - Train and fine-tune large language models
    - Build RAG systems with vector databases
    - Implement MLOps pipelines for model deployment
    - Work with PyTorch and TensorFlow
    - Design and implement embeddings systems
    - Build model serving infrastructure
    
    Requirements:
    - Strong experience with model training and fine-tuning
    - Experience with vector databases (Pinecone, Weaviate)
    - Experience with RAG and retrieval-augmented generation
    - Knowledge of MLOps and model deployment
    - Experience with PyTorch or TensorFlow
    """
    
    result_2 = manager.analyze_job_role(job_desc_2)
    print(f"Test 2 - True AI Product Engineer:")
    print(f"  Expected: ai_product_engineer")
    print(f"  Got: {result_2}")
    print(f"  ✓ PASS" if result_2 == 'ai_product_engineer' else "  ✗ FAIL")
    print()
    
    # Test 3: Backend Developer with minor AI mentions (should NOT be AI Product Engineer)
    job_desc_3 = """
    Backend Developer
    
    Join our team to build scalable backend services using Java and Spring Boot.
    
    Responsibilities:
    - Develop microservices using Spring Boot and Hibernate
    - Design RESTful APIs
    - Integrate third-party APIs including AI services
    - Work with PostgreSQL and MongoDB
    - Implement CI/CD pipelines
    
    Requirements:
    - Strong Java and Spring Boot experience
    - Experience with microservices architecture
    - Knowledge of AI APIs is a plus
    - Experience with Docker and Kubernetes
    """
    
    result_3 = manager.analyze_job_role(job_desc_3)
    print(f"Test 3 - Backend Developer with minor AI mentions:")
    print(f"  Expected: backend_developer")
    print(f"  Got: {result_3}")
    print(f"  ✓ PASS" if result_3 == 'backend_developer' else "  ✗ FAIL")
    print()
    
    # Test 4: Fullstack with AI-powered features (should be fullstack, not AI)
    job_desc_4 = """
    Fullstack Developer
    
    Build AI-powered web applications using modern technologies.
    
    Responsibilities:
    - Develop fullstack applications with React and Python
    - Build AI-powered features using LLM APIs
    - Create generative AI solutions for customers
    - Design and implement web applications
    - Work with TypeScript, Flask, and PostgreSQL
    
    Requirements:
    - Experience with React and TypeScript
    - Experience with Python and Flask
    - Experience using AI APIs (OpenAI, Claude)
    - Strong web development skills
    """
    
    result_4 = manager.analyze_job_role(job_desc_4)
    print(f"Test 4 - Fullstack with AI-powered features:")
    print(f"  Expected: fullstack_developer")
    print(f"  Got: {result_4}")
    print(f"  ✓ PASS" if result_4 == 'fullstack_developer' else "  ✗ FAIL")
    print()
    
    # Test 5: ML Engineer with model training (should be AI Product Engineer)
    job_desc_5 = """
    Machine Learning Engineer
    
    Build and deploy machine learning models at scale.
    
    Responsibilities:
    - Train deep learning models using PyTorch
    - Fine-tune large language models
    - Build vector databases for embeddings
    - Implement MLOps pipelines
    - Deploy models to production
    - Work with Hugging Face and LangChain
    
    Requirements:
    - Strong experience with model training
    - Experience with PyTorch or TensorFlow
    - Knowledge of vector databases
    - Experience with MLOps
    """
    
    result_5 = manager.analyze_job_role(job_desc_5)
    print(f"Test 5 - ML Engineer with model training:")
    print(f"  Expected: ai_product_engineer")
    print(f"  Got: {result_5}")
    print(f"  ✓ PASS" if result_5 == 'ai_product_engineer' else "  ✗ FAIL")
    print()

if __name__ == '__main__':
    print("=" * 70)
    print("AI CLASSIFICATION PREVENTION TESTS")
    print("=" * 70)
    print()
    test_ai_misclassification_prevention()
