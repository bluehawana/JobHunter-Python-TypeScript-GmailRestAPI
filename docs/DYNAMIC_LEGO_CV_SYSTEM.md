# Dynamic LEGO CV System - AI-Driven Role Consistency

## Core Principle

**Every CV template tells a consistent story** where all work experiences relate to the target role's technology stack. The AI and LEGO logic dynamically select and emphasize relevant components based on the Job Description.

## System Architecture

```
Job Description (JD)
        ↓
    AI Analysis
        ↓
Role Classification → Select Base Template
        ↓
LEGO Bricks Selection → Choose Relevant Work Experience Bullets
        ↓
Dynamic Assembly → Build Role-Specific CV
        ↓
AI Quality Review → Verify Consistency with JD
        ↓
Final CV (3-4 pages, role-aligned)
```

## Work Experience Mapping by Role

### Your Actual Work History (Source of Truth)

Based on `linkedinworkingex.md`, here's what you ACTUALLY did at each company:

#### ECARX (Oct 2024 - Nov 2025)
**Technologies**: Infrastructure, Bash, Grafana, Networking, System Installation, Android
**Focus**: IT/Infrastructure Specialist, DevOps, System Administration

#### Synteda (Aug 2023 - Sep 2024)
**Technologies**: .NET, ASP.NET Core, Azure, C#, Docker, Kubernetes, REST API
**Focus**: .NET and Azure Integration Developer, Backend, Cloud

#### IT-Högskolan LIA 2 (Jan 2023 - May 2023)
**Technologies**: Azure DevOps, .NET, SQL Server, Azure Functions, CI/CD, Terraform
**Focus**: .NET Cloud Developer, Azure, DevOps

#### Senior Material (Jan 2022 - Dec 2022)
**Technologies**: Full-stack, Web Development, Azure Databricks, Spring MVC
**Focus**: Platform Architect, Full-stack Developer

#### AddCell LIA 1 (Sep 2022 - Nov 2022)
**Technologies**: .NET Blazor, SQL Server, Azure, AWS Lambda, Docker, Kubernetes, C#
**Focus**: .NET Developer, Cloud, DevOps

#### Pembio (Oct 2020 - Sep 2021)
**Technologies**: Java, Spring Boot, Spring MVC, Kubernetes, REST API, Microservices
**Focus**: Full Stack Engineer, Java Backend

#### CollabMaker (Jul 2020 - Oct 2020)
**Technologies**: React.js, Frontend, Scrum Master
**Focus**: Frontend Developer

## Role-Specific Work Experience Emphasis

### 1. .NET / C# Developer Roles

**Emphasize**:
- Synteda: ASP.NET Core, C#, .NET Core, Azure integration
- IT-Högskolan: .NET, Azure DevOps, Azure Functions
- AddCell: .NET Blazor, SQL Server, C#

**Example Bullets**:
```
Synteda AB | .NET and Azure Integration Developer
• Developed cloud-native applications using C# and ASP.NET Core with microservices architecture
• Built RESTful APIs with .NET Core and Entity Framework for Azure cloud deployment
• Implemented CI/CD pipelines using Azure DevOps for automated testing and deployment
• Managed Azure configurations including App Services, Functions, and Cosmos DB
```

### 2. Java Developer Roles

**Emphasize**:
- Pembio: Java, Spring Boot, Spring MVC, Microservices
- Senior Material: Spring MVC, Backend development
- Synteda: Java experience (mentioned in skills)

**Example Bullets**:
```
Pembio | Full Stack Engineer
• Developed backend services using Java and Spring Boot with microservices architecture
• Built RESTful APIs with Spring Framework and integrated with PostgreSQL databases
• Implemented JPA/Hibernate for ORM and database operations
• Participated in Agile/Scrum development with continuous integration practices
```

### 3. DevOps / Cloud Engineer Roles

**Emphasize**:
- ECARX: Infrastructure, Kubernetes, Grafana, System Administration
- Synteda: Docker, Kubernetes, Azure, DevOps
- IT-Högskolan: Azure DevOps, Terraform, CI/CD, Infrastructure as Code

**Example Bullets**:
```
ECARX | IT/Infrastructure Specialist
• Managed IT infrastructure with 24/7 on-call support across 4 global offices
• Led Azure AKS to on-premise Kubernetes migration, reducing cloud costs by 45%
• Deployed Prometheus/Grafana monitoring stack for proactive incident detection
• Automated infrastructure provisioning using Terraform and configuration management tools
```

### 4. Full-Stack Developer Roles

**Emphasize**:
- Senior Material: Full-stack, Platform Architect, Web Development
- Pembio: Full Stack Engineer, Frontend + Backend
- CollabMaker: React.js Frontend
- Synteda: Backend + Cloud integration

**Example Bullets**:
```
Senior Material | Platform Architect & Full-Stack Developer
• Built full-stack web applications using React.js frontend and Spring MVC backend
• Designed and implemented RESTful APIs for seamless frontend-backend integration
• Optimized user experience and interface using modern design principles
• Integrated security measures to protect user data and ensure compliance
```

### 5. IT Support / Customer Support Roles

**Emphasize**:
- ECARX: System installation, troubleshooting, customer service, technical support
- All roles: Problem-solving, communication, training, Swedish language skills

**Example Bullets**:
```
ECARX | IT/Infrastructure Specialist
• Provided 24/7 technical support across 4 global offices (Gothenburg, London, Stuttgart, San Diego)
• Resolved critical system incidents through systematic troubleshooting and root cause analysis
• Delivered technical training and created documentation in Swedish and English
• Managed hardware maintenance, system installations, and configuration corrections
```

### 6. Android Developer Roles

**Emphasize**:
- ECARX: Android experience (mentioned in skills)
- Synteda: Android (mentioned in skills)
- AddCell: Mobile development context

**Example Bullets**:
```
ECARX | IT/Infrastructure Specialist (Android Focus)
• Supported Android automotive systems and in-vehicle infotainment platforms
• Troubleshot Android-based applications and system integrations
• Collaborated with development teams on Android Auto and automotive-grade solutions
• Managed testing and deployment of Android applications in production environments
```

### 7. IT Business Analyst Roles

**Emphasize**:
- Senior Material: Requirements analysis, stakeholder management, project coordination
- All roles: Communication, business analysis, technical requirements

**Example Bullets**:
```
Senior Material | Platform Architect & Project Coordinator
• Analyzed business requirements and translated them into technical specifications
• Coordinated with stakeholders and third-party vendors for web projects
• Developed and implemented business strategies to increase company visibility
• Managed project timelines, resources, and deliverables using Agile methodologies
```

## LEGO Bricks System

### Component Library

Each work experience has **multiple versions** emphasizing different aspects:

```python
work_experience_bricks = {
    'ecarx': {
        'devops': [
            'Managed IT infrastructure with 24/7 on-call support',
            'Led Kubernetes migration reducing cloud costs by 45%',
            'Deployed Prometheus/Grafana monitoring stack'
        ],
        'it_support': [
            'Provided 24/7 technical support across 4 global offices',
            'Resolved critical system incidents through troubleshooting',
            'Delivered technical training in Swedish and English'
        ],
        'android': [
            'Supported Android automotive systems and infotainment platforms',
            'Troubleshot Android-based applications',
            'Managed Android Auto deployments'
        ]
    },
    'synteda': {
        'dotnet': [
            'Developed applications using C# and ASP.NET Core',
            'Built RESTful APIs with .NET Core and Entity Framework',
            'Implemented Azure DevOps CI/CD pipelines'
        ],
        'cloud': [
            'Managed Azure cloud services and configurations',
            'Deployed applications to Azure App Services and Functions',
            'Implemented Infrastructure as Code with Terraform'
        ],
        'backend': [
            'Developed backend services with microservices architecture',
            'Built RESTful APIs for cloud deployment',
            'Managed database connectivity and API integrations'
        ]
    },
    'pembio': {
        'java': [
            'Developed backend using Java and Spring Boot',
            'Built RESTful APIs with Spring Framework',
            'Implemented JPA/Hibernate for database operations'
        ],
        'fullstack': [
            'Built full-stack applications with Vue.js and Spring Boot',
            'Developed RESTful APIs for frontend-backend integration',
            'Participated in Agile/Scrum development processes'
        ]
    }
}
```

## AI Quality Review Process

### Step 1: Generate CV with LEGO Bricks

```python
def build_lego_cv(role_type, company, title, role_category, job_description):
    # 1. Select base template
    template = load_template(role_category)
    
    # 2. AI analyzes JD for key technologies
    key_technologies = ai_extract_technologies(job_description)
    
    # 3. Select relevant work experience bricks
    experience_bricks = select_bricks_by_role(role_category, key_technologies)
    
    # 4. Assemble CV with role-specific emphasis
    cv = assemble_cv(template, experience_bricks)
    
    return cv
```

### Step 2: AI Reviews Generated CV

```python
def ai_review_documents(cv_latex, cl_latex, job_description, company, title):
    """
    AI reviews generated documents for:
    1. Technology consistency (CV mentions JD technologies)
    2. Role alignment (work experience matches target role)
    3. No placeholder text
    4. Appropriate language for role type
    """
    
    review_prompt = f"""
    Review this CV against the job description:
    
    JD: {job_description}
    CV: {cv_latex}
    
    Check for:
    1. Does CV emphasize technologies mentioned in JD?
    2. Do work experience bullets align with target role?
    3. Is language appropriate (e.g., no "software development" for IT Support)?
    4. Are there any placeholders or generic text?
    
    Score: 0-100
    Issues: List any problems
    """
    
    return ai_call(review_prompt)
```

## Implementation Plan

### Phase 1: Update All Templates (Current)
- ✅ IT Support template updated to full-length (153 lines)
- ⏳ Update remaining templates to full-length
- ⏳ Ensure all use LinkedIn blue (RGB: 0,119,181)

### Phase 2: Create LEGO Bricks Library
- ⏳ Extract all work experience variations
- ⏳ Map each company to role-specific bullets
- ⏳ Create selection logic based on role_category

### Phase 3: Enhance AI Review
- ✅ AI quality check function created
- ⏳ Add technology consistency checking
- ⏳ Add role alignment verification
- ⏳ Add scoring system (0-100)

### Phase 4: Dynamic Assembly
- ⏳ Implement brick selection algorithm
- ⏳ Add JD keyword matching
- ⏳ Test with real job descriptions

### Phase 5: Sync & Deploy
- ✅ Git sync between Mac and VPS working
- ✅ Deployment script created
- ⏳ Automated testing for all role types

## Success Metrics

### Quality Indicators
- ✅ CV length: 3-4 pages (150+ lines)
- ✅ AI quality score: > 80/100
- ✅ No placeholder text
- ✅ LinkedIn blue color consistent
- ⏳ Work experience matches role type
- ⏳ Technologies align with JD

### Consistency Checks
- ⏳ .NET roles → emphasize C#, ASP.NET Core, Azure
- ⏳ Java roles → emphasize Spring Boot, Java, Microservices
- ⏳ DevOps roles → emphasize Kubernetes, CI/CD, Infrastructure
- ⏳ IT Support roles → emphasize troubleshooting, support, training

## Next Steps

1. **Create work experience bricks library** for each company
2. **Implement dynamic selection logic** based on role_category
3. **Enhance AI review** to check technology alignment
4. **Test with multiple role types** (Java, .NET, DevOps, IT Support)
5. **Deploy and verify** on both Mac and VPS

## Maintenance

### When Adding New Experience
1. Add to `linkedinworkingex.md`
2. Create role-specific bullets for each relevant role type
3. Update all affected templates
4. Test with AI review
5. Commit and deploy

### When Updating Skills
1. Update Core Technical Competencies section
2. Add to relevant work experience bullets
3. Update all templates consistently
4. Test and deploy

---

**Last Updated**: 2026-02-05
**Status**: Phase 1 in progress (IT Support template updated)
**Next**: Create LEGO bricks library for dynamic work experience selection
