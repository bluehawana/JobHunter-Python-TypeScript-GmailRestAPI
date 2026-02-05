# CV Template Strategy - Full-Length with AI Customization

## Philosophy

All CV templates should be **full-length** (3-4 pages) with comprehensive sections. The AI and LEGO logic then **selectively emphasize** relevant components based on the job description, rather than removing sections.

## Template Structure

### Standard Full-Length Template (153 lines)

Every role template includes:

1. **Header** (Name, Title, Contact)
2. **Professional Summary** (Role-specific focus)
3. **Core Technical Competencies** (8-10 skill categories)
4. **Professional Experience** (4 positions with 3-5 bullets each)
5. **Infrastructure & Automation Projects** (3 major projects)
6. **Education** (3 degrees)
7. **Certifications** (3-5 certifications)
8. **Community Involvement** (4 activities)
9. **Additional Information** (Languages, Work Authorization, Availability)

## Role-Specific Customization

### How It Works

The system maintains **one full-length base template per role** but customizes the **work experience emphasis** based on the target role:

#### Example: Java Developer Role
```
Professional Experience:
- Pembio AB | Full-Stack Developer (Java/Spring Boot focus)
  • Developed backend using Java/Spring Boot with microservices
  • Built RESTful APIs with Spring Framework
  • Implemented JPA/Hibernate for database operations
```

#### Example: .NET Developer Role
```
Professional Experience:
- Synteda AB | Azure Developer (C#/.NET focus)
  • Developed platforms using C#/.NET Core with microservices
  • Built ASP.NET Core APIs with Entity Framework
  • Managed Azure configurations and deployments
```

#### Example: DevOps Engineer Role
```
Professional Experience:
- Ecarx | IT/Infrastructure Specialist (DevOps focus)
  • Managed IT infrastructure with 24/7 on-call support
  • Led Azure AKS to on-premise Kubernetes migration
  • Deployed Prometheus/Grafana monitoring stack
```

#### Example: IT Support / Customer Support Role
```
Professional Experience:
- H3C Technologies | Technical Support Engineer
  • Resolved critical incident affecting 26 servers within 5 hours
  • Performed on-site hardware maintenance
  • Delivered technical training in Swedish and English
```

## Current Template Mappings

| Role Category | Template File | Focus Area |
|--------------|---------------|------------|
| `devops_cloud` | `devops_cloud_template.tex` | Infrastructure, CI/CD, Kubernetes |
| `fullstack_developer` | `fullstack_developer_template.tex` | Full-stack, APIs, Frontend+Backend |
| `backend_developer` | `backend_developer_template.tex` | Backend services, APIs, Databases |
| `android_developer` | `android_developer_template.tex` | Mobile, Kotlin/Java, Android SDK |
| `it_support` | `incident_management_template.tex` | Support, Troubleshooting, Incident Management |
| `it_business_analyst` | `it_business_analyst_template.tex` | Requirements, Analysis, Stakeholder Management |
| `ai_product_engineer` | `ai_product_engineer_template.tex` | AI/ML, Product Development, Data |

## AI Customization Logic

### What the AI Does

1. **Analyzes Job Description** → Extracts key technologies and requirements
2. **Selects Base Template** → Chooses role-appropriate full-length template
3. **Emphasizes Relevant Sections** → Highlights matching skills and experience
4. **Preserves All Content** → Keeps full template intact (no removal)
5. **Updates Job Title** → Replaces title in header with target position

### What the AI Does NOT Do

❌ Remove sections from the template
❌ Shorten the CV to fit arbitrary page limits
❌ Generate content from scratch
❌ Modify the core structure

## Benefits of This Approach

### ✅ Consistency
- All CVs have the same professional structure
- Hiring managers see familiar format across applications
- Easy to maintain and update templates

### ✅ Completeness
- Shows full breadth of experience
- Demonstrates versatility across technologies
- Provides comprehensive skill overview

### ✅ ATS Optimization
- More keywords = better ATS matching
- Comprehensive sections = higher relevance scores
- Full experience history = stronger candidate profile

### ✅ Role Flexibility
- Same base content works for multiple roles
- AI emphasizes relevant parts per job
- No need to maintain separate short/long versions

## Template Maintenance

### When to Update Templates

1. **New Certification** → Add to Certifications section in ALL templates
2. **New Project** → Add to Projects section in ALL templates
3. **New Job** → Add to Professional Experience in ALL templates
4. **New Skill** → Add to Core Competencies in ALL templates

### How to Update

```bash
# 1. Update the template file
vim templates/cv_templates/incident_management_template.tex

# 2. Commit and push
git add templates/cv_templates/incident_management_template.tex
git commit -m "Update: Add new certification to IT Support template"
git push origin main

# 3. Deploy to VPS
./deploy_ai_quality_check.sh
```

## Color Standards

All templates use **LinkedIn Blue**:
- RGB: `0,119,181`
- LaTeX: `\definecolor{linkedinblue}{RGB}{0,119,181}`

## File Locations

### Local (Mac)
```
templates/cv_templates/
├── incident_management_template.tex (153 lines)
├── devops_cloud_template.tex
├── fullstack_developer_template.tex
├── android_developer_template.tex
└── ...
```

### VPS (jobs.bluehawana.com)
```
/var/www/lego-job-generator/templates/cv_templates/
├── incident_management_template.tex (153 lines)
├── devops_cloud_template.tex
├── fullstack_developer_template.tex
├── android_developer_template.tex
└── ...
```

## Quality Assurance

### Template Checklist

Before deploying any template update:

- [ ] Template is 150+ lines (full-length)
- [ ] Uses LinkedIn blue (RGB: 0,119,181)
- [ ] Includes all 9 standard sections
- [ ] Has role-specific Professional Summary
- [ ] Contains 4 work experiences with 3-5 bullets each
- [ ] Includes 3 project sections
- [ ] Lists all certifications
- [ ] No placeholder text ([COMPANY NAME], etc.)
- [ ] Compiles successfully with pdflatex
- [ ] Generates 3-4 page PDF

## Success Metrics

The full-length template approach is working when:

✅ All generated CVs are 3-4 pages
✅ AI quality check scores > 80/100
✅ No placeholder text in generated documents
✅ Consistent formatting across all roles
✅ Templates sync correctly between Mac and VPS

## Last Updated

- **Date**: 2026-02-05
- **Version**: Full-length template v1.0
- **Status**: ✅ Deployed to production
- **Template Lines**: 153 (incident_management_template.tex)
