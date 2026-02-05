# JobHunter 🎯

**AI-powered job application automation. Paste a job URL, get tailored CV + cover letter in seconds.**

🔗 **Live Demo:** [jobs.bluehawana.com](https://jobs.bluehawana.com)  
📊 **Dashboard:** Real-time application tracking  
🤖 **AI Engine:** 95% accurate role detection with MiniMax M2

---

## TL;DR

Paste job URL → AI analyzes role → Generates custom CV + CL → Professional PDFs ready

**What it does:**
- Extracts company name & job title from any job site (LinkedIn, Indeed, Swedish sites)
- AI detects role type (DevOps, Full-Stack, Project Manager, etc.)
- Selects best CV template from 11+ role-specific templates
- Generates 1-page cover letter with your achievements
- Creates professional PDFs with LaTeX
- Smart filenames: `cv_harvad_CompanyName.pdf`

**Tech:** Python FastAPI + React TypeScript + MiniMax M2 AI + LaTeX

---

## Quick Start

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python run.py

# Frontend
cd frontend && npm install && npm start
```

**Required:** Python 3.8+, Node 16+, MiniMax API key, LaTeX

---

## Features

✅ **AI Role Detection** - 95% confidence, 11+ role types  
✅ **Smart Company Extraction** - Handles Swedish sites, removes prepositions  
✅ **Template Library** - .NET, Java, Full-Stack, DevOps, Project Manager, etc.  
✅ **1-Page Cover Letters** - LinkedIn blue styling, professional format  
✅ **Privacy First** - Separate personal/professional phone numbers  
✅ **Production Ready** - Deployed on VPS, systemd service

---

## API

```bash
# Generate application
POST /api/lego/generate
{
  "job_url": "https://...",
  "job_description": "Senior DevOps Engineer..."
}

# Returns
{
  "cv_pdf": "base64...",
  "cl_pdf": "base64...",
  "role_detected": "devops_cloud",
  "confidence": 95
}
```

**Docs:** [localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## Recent Updates

📅 **Feb 5, 2026** - [Template System Polish](./CHANGELOG_2026_02_05.md)
- All cover letters fit on 1 page
- LinkedIn blue consistency across all templates
- Smart company name extraction (removes "by", "till", etc.)
- Privacy: Updated to professional phone number
- Footer formatting: 3 lines, left-aligned

📅 **Jan 2026** - Swedish Job Site Support  
📅 **Dec 2025** - AI-powered role detection

[View Full Changelog →](./CHANGELOG_2026_02_05.md)

---

## Deployment

**One-liner:**
```bash
git push && ssh alphavps "cd /var/www/lego-job-generator && git pull && systemctl restart lego-backend"
```

**VPS:** jobs.bluehawana.com | **Service:** systemd | **Branch:** main

---

## Documentation

📖 [API Documentation](./backend/API_DOCUMENTATION.md)  
🎨 [Template System](./docs/COMPREHENSIVE_TEMPLATE_SYSTEM_COMPLETE.md)  
🔧 [Deployment Guide](./DEPLOY.md)  
🐛 [Troubleshooting](./FIX_VPS_500_ERROR.md)

---

## Stack

**Backend:** FastAPI, SQLAlchemy, MiniMax M2 AI, LaTeX  
**Frontend:** React, TypeScript, Material-UI  
**Deploy:** VPS, systemd, nginx  
**AI:** MiniMax M2 (role detection), Anthropic SDK

---

## License

MIT - Build cool stuff with it 🚀

---

**Made with ❤️ by [Harvad Li](https://modelsbluehawana.com)**