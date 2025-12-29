# CV Templates

This folder contains LaTeX CV templates used by the LEGO Bricks system for intelligent job application generation.

## Template Structure

Each template follows the Overleaf format with:
- Blue clickable links for email, phone, LinkedIn, GitHub
- Consistent styling with `titlecolor` and `darkblue` colors
- Professional formatting optimized for ATS systems

## Available Templates

1. **android_developer_template.tex** - For Android/Mobile development roles
2. **devops_cloud_template.tex** - For DevOps, Cloud, and Infrastructure roles
3. **incident_management_template.tex** - For SRE and Incident Management roles
4. **ai_product_engineer_template.tex** - For AI/ML Product Engineer roles
5. **nasdaq_devops_template.tex** - Alternative DevOps template
6. **alten_cloud_engineer_template.tex** - Cloud Engineer focused template

## Template Selection Logic

The system uses AI (MiniMax M2) to analyze job descriptions and automatically select the most appropriate template based on:
- Role keywords (android, devops, cloud, sre, ai, etc.)
- Required skills and technologies
- Job responsibilities

See `backend/cv_templates.py` for the full template matching logic.

## Customization

Templates are automatically customized with:
- Job-specific title in the header
- Company name (when detected)
- Role-specific content emphasis

## Adding New Templates

1. Create a new `.tex` file in this folder
2. Follow the Overleaf format with blue clickable links
3. Update `backend/cv_templates.py` ROLE_CATEGORIES with new template path
4. Add relevant keywords for automatic matching

## Note

This folder is version controlled. The `job_applications/` folder (containing generated PDFs and personalized CVs) is gitignored to protect personal information.
