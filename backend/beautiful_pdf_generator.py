#!/usr/bin/env python3
"""
Beautiful Multi-Page PDF Generator - NO MORE ONE-PAGE SHIT!
Now uses EXACT LaTeX template for perfect Overleaf quality!
BONUS: Also generates Overleaf URLs for manual editing!
"""
import logging
import os
from latex_pdf_generator import create_latex_pdf
from overleaf_pdf_generator import OverleafPDFGenerator

logger = logging.getLogger(__name__)

def create_beautiful_multi_page_pdf(job: dict, latex_content: str = "") -> bytes:
    """Create BEAUTIFUL multi-page PDF using EXACT LaTeX template - Overleaf quality!"""
    try:
        # Generate PDF using LaTeX
        pdf_content = create_latex_pdf(job, latex_content)
        
        # BONUS: Upload to R2 and create Overleaf URL for manual editing
        try:
            from r2_latex_storage import R2LaTeXStorage
            
            generator = OverleafPDFGenerator()
            latex_template = generator._generate_latex_content(job)
            
            # Try R2 upload first
            r2_storage = R2LaTeXStorage()
            r2_result = r2_storage.upload_latex_file(latex_template, job)
            
            if r2_result:
                logger.info(f"🎯 OVERLEAF URL (R2): {r2_result['overleaf_url']}")
                logger.info(f"☁️ LaTeX uploaded to R2: {r2_result['filename']}")
                logger.info(f"✨ Professional Overleaf integration ready!")
            else:
                # Fallback to local storage
                company = job.get('company', 'company').lower().replace(' ', '_')
                job_title = job.get('title', 'position').lower().replace(' ', '_')
                
                import time
                timestamp = int(time.time())
                filename = f"resume_{company}_{job_title}_{timestamp}.tex"
                
                # Create latex_files directory
                latex_dir = os.path.join(os.path.dirname(__file__), 'latex_files')
                os.makedirs(latex_dir, exist_ok=True)
                
                # Save LaTeX file locally
                file_path = os.path.join(latex_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(latex_template)
                
                # Generate local Overleaf URL
                base_url = os.getenv('BASE_URL', 'https://jobs.bluehawana.com')
                latex_url = f"{base_url}/api/v1/latex/{filename}"
                overleaf_url = f"https://www.overleaf.com/docs?snip_uri={latex_url}"
                
                logger.info(f"🎯 OVERLEAF URL (Local): {overleaf_url}")
                logger.info(f"📝 LaTeX saved locally: {file_path}")
                logger.warning(f"⚠️ R2 upload failed, using local fallback")
            
        except Exception as overleaf_error:
            logger.warning(f"⚠️ Overleaf integration failed (PDF still created): {overleaf_error}")
        
        return pdf_content
        
    except Exception as e:
        logger.error(f"❌ Error creating LaTeX PDF: {e}")
        return b""
        
        # Parse job for LEGO logic
        job_title = job.get('title', '').lower()
        job_description = job.get('description', '').lower()
        company = job.get('company', 'Company')
        
        # LEGO intelligence
        is_devops = any(keyword in job_title + job_description for keyword in 
                       ['devops', 'infrastructure', 'kubernetes', 'docker', 'aws', 'cloud', 'ci/cd'])
        is_backend = any(keyword in job_title + job_description for keyword in 
                        ['backend', 'api', 'microservices', 'spring', 'java', 'database']) and not is_devops
        is_frontend = any(keyword in job_title + job_description for keyword in 
                         ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui']) and not is_devops and not is_backend
        
        # EXACT LaTeX template styling - matching your Overleaf template
        styles = getSampleStyleSheet()
        dark_blue = HexColor('#003366')  # Your exact color from LaTeX
        
        # Title style - EXACTLY like your LaTeX template
        title_style = ParagraphStyle(
            'LaTeXTitle', parent=styles['Normal'], fontSize=24, spaceAfter=10,
            alignment=1, textColor=dark_blue, fontName='Times-Bold',
            leading=28, spaceBefore=0
        )
        
        # Subtitle style - matching your LaTeX role title
        subtitle_style = ParagraphStyle(
            'LaTeXSubtitle', parent=styles['Normal'], fontSize=16, spaceAfter=10,
            alignment=1, textColor=dark_blue, fontName='Times-Italic',
            leading=20
        )
        
        # Section headers - EXACTLY like your LaTeX sections
        section_style = ParagraphStyle(
            'LaTeXSection', parent=styles['Normal'], fontSize=14, spaceAfter=6, spaceBefore=12,
            textColor=dark_blue, fontName='Times-Bold', leading=16,
            borderWidth=0.5, borderColor=dark_blue, borderPadding=2,
            keepWithNext=True
        )
        
        # Content style - matching your LaTeX body text
        content_style = ParagraphStyle(
            'LaTeXContent', parent=styles['Normal'], fontSize=11, spaceAfter=4,
            fontName='Times-Roman', leading=13, leftIndent=0, rightIndent=0
        )
        
        # Contact style - for header contact info
        contact_style = ParagraphStyle(
            'LaTeXContact', parent=styles['Normal'], fontSize=11, spaceAfter=8,
            alignment=1, fontName='Times-Roman', leading=13, textColor=dark_blue
        )
        
        # Build professional multi-page resume
        story = []
        
        # HEADER - Professional like your LaTeX
        story.append(Paragraph("HONGZHI LI", title_style))
        
        # LEGO role positioning
        if is_devops:
            role_title = "DevOps Engineer & Cloud Infrastructure Specialist"
        elif is_backend:
            role_title = "Backend Developer & API Specialist"
        elif is_frontend:
            role_title = "Frontend Developer & UI Specialist"
        else:
            role_title = "Senior Fullstack Developer"
        
        story.append(Paragraph(role_title, subtitle_style))
        
        # Contact info - EXACTLY like your LaTeX template
        contact_info = '''
        <a href="mailto:hongzhili01@gmail.com" color="#003366">hongzhili01@gmail.com</a> | 
        <a href="tel:0728384299" color="#003366">0728384299</a> | 
        <a href="https://www.linkedin.com/in/hzl/" color="#003366">LinkedIn</a> | 
        <a href="https://github.com/bluehawana" color="#003366">GitHub</a>
        '''
        story.append(Paragraph(contact_info, contact_style))
        story.append(Spacer(1, 20))
        
        # PROFILE SUMMARY - Tailored to job
        story.append(Paragraph("PROFILE SUMMARY", section_style))
        
        if is_devops:
            summary = f"""Experienced DevOps Engineer and Infrastructure Specialist with over 5 years of expertise in cloud technologies, 
            system optimization, and automated deployment pipelines. Currently serving as IT/Infrastructure Specialist at ECARX with proven 
            track record in Kubernetes, AWS, Docker, and infrastructure automation. Strong background in migrating from AKS to local Kubernetes 
            clusters, implementing monitoring solutions using Grafana, and managing complex network systems. Demonstrated ability to work across 
            the entire infrastructure stack from cloud platforms to system reliability and enterprise-level technical solution design. 
            Specialized in infrastructure optimization roles for companies like {company}."""
        elif is_backend:
            summary = f"""Experienced Backend Developer with over 5 years of expertise in API development, microservices architecture, 
            and database optimization. Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in Spring Boot, 
            RESTful APIs, and scalable backend systems. Strong background in building comprehensive talent management systems using C# and .NET Core, 
            implementing microservices for scalable application architecture, and integrating SQL and NoSQL databases with optimized query performance. 
            Specialized in backend development roles for companies like {company}."""
        else:
            summary = f"""Experienced Fullstack Developer with over 5 years of hands-on experience in Java/J2EE development with modern web technologies. 
            Currently serving as IT/Infrastructure Specialist at ECARX with proven track record in building scalable applications. Strong background 
            in both frontend and backend development, from React and Angular to Spring Boot and .NET Core, with expertise in cloud platforms and DevOps practices. 
            Specialized in end-to-end development roles for companies like {company}."""
        
        story.append(Paragraph(summary, content_style))
        story.append(Spacer(1, 16))
        
        # TECHNICAL SKILLS - Comprehensive and organized
        story.append(Paragraph("CORE TECHNICAL SKILLS", section_style))
        
        if is_devops:
            skills_data = [
                ["Cloud Platforms", "AWS, Azure, GCP, Alibaba Cloud ECS"],
                ["Containerization", "Docker, Kubernetes, Azure Kubernetes Service (AKS)"],
                ["CI/CD", "Jenkins, GitHub Actions, GitLab CI, Automated Testing, Deployment Pipelines"],
                ["Infrastructure", "Infrastructure as Code, System Integration, Network Management, Cost Optimization"],
                ["Monitoring", "Grafana, Advanced Scripting, System Reliability, Performance Monitoring"],
                ["Programming", "Python, Bash, PowerShell, Java, JavaScript, Go"],
                ["Databases", "PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB"],
                ["Security", "Application security, Data protection, Authentication/Authorization"]
            ]
        elif is_backend:
            skills_data = [
                ["Programming Languages", "Java/J2EE, C#/.NET Core, Python, JavaScript, TypeScript"],
                ["Backend Frameworks", "Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI"],
                ["API Development", "RESTful APIs, GraphQL, Microservices Architecture"],
                ["Databases", "PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB"],
                ["Cloud Platforms", "AWS, Azure, GCP, Alibaba Cloud"],
                ["Performance", "Database optimization, Caching strategies, Application scaling"],
                ["Security", "Application security, Data protection, Authentication/Authorization"],
                ["DevOps", "Docker, Kubernetes, Jenkins, GitHub Actions"]
            ]
        else:
            skills_data = [
                ["Programming Languages", "Java/J2EE, JavaScript, C#/.NET Core, Python, TypeScript"],
                ["Frontend Technologies", "Angular, ReactJS, React Native, Vue.js, HTML5, CSS3"],
                ["Backend Frameworks", "Spring Boot, Spring MVC, .NET Core, Node.js, FastAPI"],
                ["Databases", "PostgreSQL, MySQL, MongoDB, AWS RDS, Azure Cosmos DB"],
                ["Cloud Platforms", "AWS, Azure, GCP, Alibaba Cloud"],
                ["DevOps", "Docker, Kubernetes, Jenkins, GitHub Actions, GitLab CI"],
                ["Version Control", "Git, GitHub, GitLab"],
                ["Methodologies", "Agile, Scrum, Kanban, Sprint Planning, Code Reviews"]
            ]
        
        # NO TABLE! Use bullet points like your LaTeX template
        for skill in skills_data:
            skill_text = f"<b>{skill[0]}:</b> {skill[1]}"
            story.append(Paragraph(f"• {skill_text}", content_style))
        story.append(skills_table)
        story.append(Spacer(1, 16))
        
        # PROFESSIONAL EXPERIENCE - Detailed and tailored
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
        
        # ECARX Experience - Always include, emphasize for DevOps
        story.append(Paragraph("<b>ECARX | IT/Infrastructure Specialist</b>", content_style))
        story.append(Paragraph("<i>October 2024 - Present | Gothenburg, Sweden</i>", content_style))
        
        ecarx_points = [
            "Leading infrastructure optimization and system integration projects for automotive technology solutions",
            "Implementing cost optimization project by migrating from AKS to local Kubernetes cluster, reducing operational expenses",
            "Implementing modern monitoring solutions using Grafana and advanced scripting for system reliability",
            "Managing complex network systems and providing technical solution design for enterprise-level applications",
            "Providing IT support and infrastructure support to development teams for enhanced productivity"
        ]
        
        for point in ecarx_points:
            story.append(Paragraph(f"• {point}", content_style))
        story.append(Spacer(1, 12))
        
        # Synteda Experience - Tailored based on job focus
        story.append(Paragraph("<b>Synteda | Azure Fullstack Developer & Integration Specialist</b>", content_style))
        story.append(Paragraph("<i>August 2023 - September 2024 | Gothenburg, Sweden</i>", content_style))
        
        synteda_points = [
            "Developed comprehensive talent management system using C# and .NET Core with cloud-native architecture",
            "Built complete office management platform from scratch, architecting both frontend and backend components",
            "Implemented RESTful APIs and microservices for scalable application architecture",
            "Integrated SQL and NoSQL databases with optimized query performance and data protection measures",
            "Collaborated with cross-functional teams to deliver high-quality software solutions"
        ]
        
        for point in synteda_points:
            story.append(Paragraph(f"• {point}", content_style))
        story.append(Spacer(1, 12))
        
        # Additional Experience
        story.append(Paragraph("<b>Senior Material (Europe) AB | Platform Architect & Project Coordinator</b>", content_style))
        story.append(Paragraph("<i>January 2022 - December 2022 | Eskilstuna, Sweden</i>", content_style))
        
        senior_material_points = [
            "Led migration of business-critical applications with microservices architecture",
            "Collaborated with development teams to optimize applications for maximum speed and scalability",
            "Participated in Agile ceremonies including sprint planning, reviews, and retrospectives"
        ]
        
        for point in senior_material_points:
            story.append(Paragraph(f"• {point}", content_style))
        story.append(Spacer(1, 16))
        
        # PROJECTS - Show technical depth
        story.append(Paragraph("KEY PROJECTS", section_style))
        
        projects = [
            {
                "name": "Weather_Anywhere.CLOUD_API_Encoding",
                "period": "Feb 2024 - Present",
                "tech": "SpringBoot, AlibabaCloudECS, ApsaraDBRDS(MySQL), Heroku",
                "description": "Weather tracking app for Swedish and global cities using OpenCageData and Open-Meteo APIs. Deployed on Alibaba Cloud ECS with city coordinates and weather data stored in ApsaraDB MySQL. Dynamic city lookup and caching mechanism for optimized API usage and response speed.",
                "demo": "https://weather.bluehawana.com"
            },
            {
                "name": "Gothenburg_TaxiPooling_Java_ReactNative_PythonALGO",
                "period": "May 2024 - Present",
                "tech": "SpringBoot, ReactNative, PostgreSQL, Python, ML, PSQL",
                "description": "Neural network-powered carpooling platform with automated passenger matching and real-time geolocation tracking. Developed cross-platform mobile application using React Native and Spring Boot microservices. Integrated secure payment processing, RESTful APIs, and PostgreSQL for scalable data handling."
            },
            {
                "name": "SmrtMart.com_COMMERCE.WEB",
                "period": "April 2024 - Present",
                "tech": "Go, Next.js, PostgreSQL, Microservices, StripeAPI",
                "description": "Fullstack e-commerce platform with microservices-based architecture for seamless scalability. Implemented comprehensive order management, inventory tracking, and payment systems. Optimized backend API performance and integrated PostgreSQL and MongoDB for hybrid data storage."
            }
        ]
        
        for project in projects:
            story.append(Paragraph(f"<b>{project['name']}</b>", content_style))
            story.append(Paragraph(f"<i>{project['period']} | {project['tech']}</i>", content_style))
            story.append(Paragraph(project['description'], content_style))
            if 'demo' in project:
                story.append(Paragraph(f"Demo: <a href='{project['demo']}' color='blue'>{project['demo']}</a>", content_style))
            story.append(Spacer(1, 8))
        
        story.append(Spacer(1, 16))
        
        # EDUCATION
        story.append(Paragraph("EDUCATION", section_style))
        
        education_data = [
            ["IT Högskolan", "Bachelor's Degree in .NET Cloud Development", "2021-2023"],
            ["Mölndal Campus", "Bachelor's Degree in Java Integration", "2019-2021"],
            ["University of Gothenburg", "Master's Degree in International Business and Trade", "2016-2019"]
        ]
        
        for edu in education_data:
            story.append(Paragraph(f"<b>{edu[0]}</b>", content_style))
            story.append(Paragraph(f"{edu[1]} | {edu[2]}", content_style))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 16))
        
        # CERTIFICATIONS
        story.append(Paragraph("CERTIFICATIONS", section_style))
        
        certs = [
            "AWS Certified Solutions Architect - Associate (Aug 2022)",
            "Microsoft Certified: Azure Fundamentals (Jun 2022)",
            "AWS Certified Developer - Associate (Nov 2022)"
        ]
        
        for cert in certs:
            story.append(Paragraph(f"• {cert}", content_style))
        
        # Build the beautiful multi-page PDF
        doc.build(story)
        buffer.seek(0)
        
        pdf_size = len(buffer.getvalue())
        logger.info(f"🎉 BEAUTIFUL MULTI-PAGE PDF: Generated professional {role_title} resume for {company} ({pdf_size} bytes)")
        logger.info(f"✅ NO MORE ONE-PAGE SHIT - This is a proper professional resume!")
        
        return buffer.getvalue()
        
    except Exception as e:
        logger.error(f"❌ Error creating beautiful PDF: {e}")
        return b""

if __name__ == "__main__":
    # Test the beautiful PDF generator
    test_job = {
        'title': 'Senior Backend Developer',
        'company': 'Volvo Group',
        'description': 'Java, Spring Boot, microservices, Kubernetes, AWS'
    }
    
    pdf_content = create_beautiful_multi_page_pdf(test_job)
    
    if pdf_content:
        with open('test_beautiful_resume.pdf', 'wb') as f:
            f.write(pdf_content)
        print(f"✅ Generated beautiful resume: {len(pdf_content)} bytes")
    else:
        print("❌ Failed to generate PDF")