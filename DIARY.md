# Working Diary — JobHunter

## 2026-11-19

### What we built
- `generate_coretura.py` — CV and cover letter for the Coretura AI Platform Engineer role, assembled LEGO-style: every section is a named brick and `ASSEMBLY` / `CL_ASSEMBLY` set the order, so a brick can be swapped or dropped for the next application.
- `AI_Job_Application/Coretura/` — the generated CV (two pages) and cover letter (one page), `.tex` and `.pdf`.

### Decisions
- **Volvo Group first.** Coretura is owned by Volvo Group and Daimler Truck, so Volvo work takes about a page and a half. ECARX is one sentence, older roles one line, hobby projects two lines.
- **Highlights block** under the profile: HackDay 2nd place, first RAG system in DTO, four AI products in four months, the platform, the two DTO sessions.
- **Business and personal kept apart.** The uploaded cover letter is addressed to the hiring team. The personal note to the recruiter goes by LinkedIn and is not in this repo.
- **Smart Vehicle wording:** "bring the experience of building it", not the system itself, because the work is Volvo IP.

### Facts corrected (older CVs and templates in this repo still have the old values)
- Volvo Group start date is **Mar 2026**, not Mar 2025.
- HackDay 2026: 2nd place of **16** teams, not 22 or 12.
- Organisation line: Software Configurator, Software Factory, DTO.
- New project numbers: Support Chatbot 35% faster ticket processing, DevBot senior review 6 hours to 60 minutes, OfficeBot about 90% time saved.

### Issues and how we fixed them
1. **Google Drive connector had no file permission.** Read the pitch deck from the local copy in `~/Projects/truckNav/demo` instead.
2. **No LaTeX on the Mac, and the online compile API (`latex.api.aa.net.uk`) dropped TLS connections.** Compiled on the `alphavps` server with `pdflatex` in a temp directory, copied the PDF back and deleted the temp directory.
3. **ATS parsing.** The first PDFs extracted as "OpenAIcompatible", "IT-H¨ogskolan" and odd bullet glyphs. Fixed with `glyphtounicode`, T1 fonts via `lmodern`, and hyphenation turned off. Contact links are written out as addresses.
4. **Two blues.** The template used a navy for headings and LinkedIn blue for links. Both colour names now point to RGB 0,119,181.
5. **Page count.** Every content addition pushed the CV to three pages; trimmed duplicated statements each time to stay at two.

### Open points
- The Smart Vehicle repo (`CoDriver-LLM-TTS`) is private and its new README is not pushed, so the link in the CV does not open for outsiders yet.
- Not verified by me: "first RAG system in DTO", and the guardrails described as limiting prompt injection.
- Older CVs, cover letters and templates still carry Mar 2025 and 22 teams.
