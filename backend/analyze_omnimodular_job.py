from ai_analyzer import AIAnalyzer

job_description = """
Product Engineer (AI & SaaS) – Build the "Brain" of Next-Generation Fintech
Omnimodular AB, Sweden
From 60,000 SEK per month - Part-time, Full-time

About Us:
Omnimodular is a deep-tech company with PhDs and industry experts building infrastructure for next generation financial software. Our Post-Template technology is used by leading platforms in Sweden.

The Role: "The Stitcher"
As a Product Engineer, you sit at the intersection of Engineering, Product, and AI. You'll be the architect who brings our powerful AI engines into the hands of users.

What You'll Do:
- Build & Prototype: Develop full-stack features (React/TypeScript/Python) that leverage LLMs to solve complex data extraction and matching problems
- Tame the AI: Design robust logic and guardrails ensuring AI models (GPT-4, etc.) deliver reliable, hallucination-free outputs for critical financial data
- Own the Experience: Design and build UX/UI where users interact with the AI
- Data Architecture: Implement RAG strategies (Retrieval-Augmented Generation)
- Ship at Scale: Take features from raw idea to production API used by enterprise customers across Europe

Who You Are:
- A Builder: Strong full-stack experience (React, Node.js, Python)
- AI-Curious: Experimented with OpenAI APIs, LangChain, or Vercel AI SDK
- Product-Oriented: Understand business goals and figure out best technical solutions
- A "Mini-PM": Care about user friction, latency, and time-to-value
- Fearless: Not intimidated by complex problems or working alongside PhDs

Tech Stack: React, TypeScript, Python, OpenAI API, Cloud-Native Architecture
"""

analyzer = AIAnalyzer()
result = analyzer.analyze_job_description(job_description)

if result:
    print(f"✓ Role Category: {result['role_category']}")
    print(f"✓ Confidence: {result['confidence']:.0%}")
    print(f"✓ Key Technologies: {', '.join(result.get('key_technologies', [])[:10])}")
    print(f"✓ Reasoning: {result['reasoning']}")
else:
    print("AI analysis failed")
