# Working Diary — JobHunter

## 2026-11-19 (second session) — DevOps/Cloud CV and CampX application

### What we built
- `generate_devops_cloud.py` and `AI_Job_Application/DevOps_Cloud/` — a general DevOps / Cloud / Platform Architecture CV (two pages) for a recruiter who asked for an infrastructure-first profile. Same facts as the Coretura CV and www.bluehawana.com, reordered: monitoring, website watchdog, hybrid load balancer, CI/CD, secrets and AI platform architecture at Volvo Group; ECARX in full (Azure AKS to bare-metal Kubernetes migration, 7.78-minute Android 15 AOSP clean build, 35% cost cut, monitoring, incident).
- `AI_Job_Application/CampX/` — CV for an open application to CampX by Volvo Group as AI Innovation Engineer (two pages), built from the Coretura bricks with Smart Vehicle and the HackDay result first. A one-page letter and a covering email were also written; see "Kept out of the repo".

### Decisions
- **CampX is an open application.** The Volvo Group careers site had no posting for "CampX" or for "innovation" in Gothenburg. The fit is the Venture Builder track and the "intelligent vehicle" and "services and solutions" focus areas.
- **Project driver, not only own ideas.** After feedback that CampX needs someone who drives projects, the letter and CV profile show that the Support Chatbot, DevBot and ClaimGenerationBot each started as another team's need.
- **Real job titles stay.** Only the header line of each CV changes per application.
- **Conflicting numbers left out.** The "faster than Azure" claim for the Android build appears as 48%, 259% and 3.5x in older files, so the new CVs only state the 7.78-minute record.

### Facts corrected
- **Phone number is +46 72 838 4299.** Updated in the DevOps and CampX files; the Coretura files and older CVs still show the old number.
- **Tianjin University of Technology removed from education.** Replaced by Campus Mölndal, Java Integration, 2019–2021, in the Coretura, CampX and DevOps CVs. Thirteen older CVs, templates and scripts, and the website, still list Tianjin.
- AWS Certified Developer – Associate (2022) added to the DevOps CV because the website lists it.

### Issues and how we fixed them
1. **WebFetch returned a condensed summary of the resume page.** Downloaded the page with `curl` and stripped the HTML locally to get the full text.
2. **Page count again.** Both new CVs first compiled to three pages; trimmed skills and the smaller roles to get back to two.
3. **HEIC photo could not be read directly.** Converted with `sips` to JPEG in the scratchpad.

### Kept out of the repo
- The CampX letter, the covering email and `generate_campx.py` (which contains the letter text). The repo is public, and these name colleagues and describe an internal conversation that is still open.
- PDFs are ignored by `.gitignore`, so only `.tex` sources are committed.

### Open points
- Availability in the CampX letter is 1 January 2027, carried over from Coretura; not confirmed.
- Not verified: the bare-metal migration details (networking, CSI storage, ingress) and the persistent-volume and artifact cleanup, which come from older notes in this repo.
- The website still lists Tianjin and puts Java Integration under IT-Högskolan.
- The Coretura CV already submitted still has the Tianjin line and the old phone number.

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
