"""Coretura — AI Platform Engineer CV, assembled LEGO-style.

Each brick is a self-contained LaTeX fragment. ASSEMBLY lists the bricks in
the order they appear, so a brick can be reordered, swapped or dropped for
another application without touching the rest.
"""
from pathlib import Path

OUTPUT_DIR = Path("AI_Job_Application/Coretura")
CV_NAME = "Harvad_Li_Coretura_AI_Platform_Engineer_CV"

BRICKS = {}

# ── Frame ────────────────────────────────────────────────────────────────────
BRICKS["preamble"] = r'''\documentclass[a4paper,10pt]{article}
\input{glyphtounicode}
\pdfgentounicode=1
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[none]{hyphenat}
\usepackage[left=0.7in,right=0.7in,top=0.55in,bottom=0.55in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}

\definecolor{darkblue}{RGB}{0,119,181}
\definecolor{linkedinblue}{RGB}{0,119,181}

\hypersetup{
    colorlinks=true,
    linkcolor=linkedinblue,
    urlcolor=linkedinblue,
    citecolor=linkedinblue,
    pdfborder={0 0 0}
}

\titleformat{\section}{\large\scshape\raggedright\color{darkblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}[runin]{\bfseries}{}{0em}{}[:]
\titlespacing*{\section}{0pt}{7pt}{4pt}
\titlespacing*{\subsection}{0pt}{5pt}{0.5em}

\setlength{\parindent}{0pt}
\sloppy
\setlist[itemize]{leftmargin=1.2em,itemsep=1pt,topsep=2pt,parsep=0pt}

\begin{document}
\pagestyle{empty}
'''

BRICKS["header"] = r'''\begin{center}
{\LARGE \textbf{Harvad Li}}\\[8pt]
{\Large \textit{AI Platform Engineer}}\\[8pt]
\textcolor{darkblue}{
  \href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} \textbar{}
  \href{tel:+46760067977}{+46 76 006 7977} \textbar{}
  Gothenburg, Sweden
}\\[3pt]
\textcolor{darkblue}{
  \href{https://www.linkedin.com/in/hzl/}{linkedin.com/in/hzl} \textbar{}
  \href{https://github.com/bluehawana}{github.com/bluehawana} \textbar{}
  \href{https://huggingface.co/bluehawana}{huggingface.co/bluehawana} \textbar{}
  \href{https://www.bluehawana.com}{www.bluehawana.com}
}
\end{center}
'''

# ── Summary ──────────────────────────────────────────────────────────────────
BRICKS["summary"] = r'''\section*{Profile}
Senior software engineer with 6+ years across full-stack development, cloud infrastructure and AI, now building and running the on-premises AI platform at Volvo Group Digital Technology \& Operations (DTO) and the AI agents that run on it. I own what I build end to end in production, including its roadmap, incidents and costs. I write code with AI coding agents (Claude Code) every day, and I know commercial-vehicle software from inside Volvo Group, one of Coretura's two owners.
'''

BRICKS["highlights"] = r'''\section*{AI at Volvo Group --- Highlights}
\begin{itemize}
  \item \textbf{2nd place of 16 teams at Volvo Group HackDay 2026}, leading the team behind ClaimGenerationBot; Volvo Trucks asked for a production rollout.
  \item \textbf{Built the first RAG system in Volvo Group DTO} (Support Chatbot, April 2026), in daily use by two teams and cutting support-ticket processing time by 35\%.
  \item \textbf{Four AI products in four months} (April to July 2026), each with a measured result: senior PR review time from 6 hours to 60 minutes, about 90\% less time to build a slide deck, and a three-agent system for trucks.
  \item \textbf{Run the platform underneath them:} open-weight models served on Volvo's own hardware, so no data goes to an outside AI service, at zero cloud API cost.
  \item \textbf{Teach it:} two company-wide sessions on RAG, agents and on-premises LLMs (74 and 71 registered participants).
\end{itemize}
'''

# ── Skills (ordered to mirror the Coretura job description) ──────────────────
BRICKS["skills"] = r'''\section*{Technical Skills}
\begin{itemize}
  \item \textbf{AI platform, model APIs and gateways:} Access to AI models across providers (Azure OpenAI, Anthropic Claude, Gemini API, Groq, NVIDIA NIM) and on-premises model serving (Ollama, MLX, SGLang, llama.cpp), AI gateway, OpenAI-compatible endpoints, failover and load balancing, model versions, benchmarking, quantization
  \item \textbf{AI agents and retrieval (RAG):} Agent harnesses and agent loops with tool calling, multi-agent systems, tool integrations, retrieval-augmented generation, knowledge bases, embeddings, vector search, prompts and prompt engineering, vision OCR, speech (Whisper, TTS)
  \item \textbf{Evaluations and observability:} Evaluations of answer quality (confidence scoring, grounded answers with sources, human escalation), model benchmarks, end-to-end test rigs, latency logging, audit trails, monitoring and alerting with Prometheus and Grafana
  \item \textbf{Security and safety:} Least privilege, secrets management (Azure Key Vault, managed identities, token rotation), Entra ID, data sovereignty, agent guardrails that limit prompt injection (tool allow-lists, grounded answers, human approval before actions)
  \item \textbf{Cloud infrastructure as code and CI/CD:} Terraform, Azure Bicep, Kubernetes (AKS, OpenShift ARO, on-premises), Helm, Argo CD, Docker, automated pipelines with Azure DevOps and GitHub Actions, resilience and failover, cost optimisation
  \item \textbf{Languages and testing:} Python (FastAPI, asyncio, pytest), C\#/.NET, TypeScript/React, Kotlin (Android Automotive, AOSP), SQL, PowerShell; well-tested, maintainable code, code review
  \item \textbf{AI coding agents:} Claude Code, GitHub Copilot, local coder models (Qwen Coder) in daily use; mentoring engineers to adopt them safely
\end{itemize}
'''

# ── Experience: Volvo Group (one brick per project) ──────────────────────────
BRICKS["volvo_open"] = r'''\section*{Professional Experience}

\subsection*{Volvo Group --- Software Configurator, Software Factory, DTO, Gothenburg}
\textit{Full-Stack Developer \& AI Solution Engineer, Mar 2026 -- Present}
\begin{itemize}
'''

BRICKS["volvo_platform"] = r'''  \item \textbf{Shared AI platform (on-premises):} Designed and run the model-serving layer behind the bots below: two Mac Studio M2 Ultra servers running Ollama with round-robin load balancing and automatic failover, exposed through OpenAI-compatible endpoints so each product can change model without code changes. Published 12+ custom models to \href{https://ollama.com/bluehawana}{Ollama} and \href{https://huggingface.co/bluehawana}{HuggingFace}, and contributed Apple Silicon concurrent-inference support to the open-source SGLang serving framework.
'''

BRICKS["volvo_smart_vehicle"] = r'''  \item \textbf{Volvo Smart Vehicle --- three agents on one truck record} (Jul 2026; Android Automotive/AOSP, Kotlin, FastAPI, Whisper, Gemma 4 on Ollama, MLX, Docker): Built a working prototype in which three agents read and write one record keyed by the registration plate and call each other instead of starting over. \textit{Co-Driver} is a hands-free voice agent in the cab with 33 tools that plans routes and rest breaks against EU driving-time rules, explains dashboard warning lamps from the handbook and books workshop service. \textit{ClaimBot} settles who pays for a repair from contract tier, warranty and open campaigns, and drafts the claim. \textit{Fleet Manager} gives the office a live view of every truck and relays customer changes to the driver. About 1 s per direct voice turn and 3--4 s when a turn crosses all three agents. Model chosen by benchmark against three alternatives, with an MLX failover. Agents only quote what the record returns and never report an unconfirmed booking; an end-to-end voice test rig and a 14-truck scenario fleet check every stage. Designed as one platform for any truck brand: the wake word and brand are configuration, and all data stays in the manufacturer's own cloud. Built with Claude Code. Code, architecture and a 10-minute demo: \href{https://github.com/bluehawana/CoDriver-LLM-TTS-Demo}{github.com/bluehawana/CoDriver-LLM-TTS-Demo}
'''

BRICKS["volvo_hackday"] = r'''  \item \textbf{ClaimGenerationBot --- 2nd place of 16 teams, Volvo Group HackDay 2026} (Python/FastAPI, .NET, RAG): Automated service-contract generation for Volvo Trucks: plate number in, the agent retrieves truck profile, service history and parts data, drafts the contract and books the workshop, and a human approves the final step. \textbf{From about 40 minutes to near-instant.}
'''

BRICKS["volvo_supportbot"] = r'''  \item \textbf{Support Chatbot} (Apr 2026; .NET 10, SignalR, llama3.3:70b, nomic-embed-text, qwen3-vl, SQLite): Built the first RAG system in DTO, a support assistant on a Karpathy-style LLM wiki knowledge base for the Software Configurator and SWES teams, whose L1--L3 support engineers use it in their daily work. \textbf{Cut support-ticket processing time by 35\%.} Answers cite their sources and carry a confidence score, low-confidence answers are escalated to a specialist, screenshots are read with vision OCR, and every conversation is stored for audit.
'''

BRICKS["volvo_devbot"] = r'''  \item \textbf{DevBot --- AI pull-request review} (May 2026; Python, aiohttp, Microsoft Teams Bot Framework, Azure DevOps webhooks, Qwen Coder): Junior mode analyses a developer's changes and their risks and suggests how to get the PR approved. Senior mode shows what changed in the codebase and the likely result of approving the merge. \textbf{Cut average senior review time from 6 hours to 60 minutes.} Path-based review rules and incremental reviews, with documented secret handling and rotation.
'''

BRICKS["volvo_officebot"] = r'''  \item \textbf{OfficeBot --- slides from plain text} (Jun 2026; LLM, HTML): Turns plain text and a prompt into an HTML slide deck with the Volvo Group logo, colour theme and fonts applied automatically. \textbf{Saves about 90\% of the time} compared with building the deck by hand.
'''

BRICKS["volvo_coding_agents"] = r'''  \item \textbf{AI coding agents for the team, through the gateway} (PowerShell, Entra ID): Packaged a Claude Code setup that reaches Claude models through Volvo's GenAI Hub AI Gateway with short-lived Entra ID tokens instead of API keys, with an installer and a smoke test so any developer reproduces it in minutes.
'''

BRICKS["volvo_assets_security"] = r'''  \item \textbf{AI assets as code, and security} (GitHub Actions, Azure Pipelines, Bicep, Azure Automation): Keep each bot's knowledge base and configuration in its own versioned repository, separate from the container image, so the application ships with no secrets and no Volvo data and a knowledge change is reviewed and traceable. CI and CD through GitHub Actions, with reusable Azure Pipelines templates for build, infrastructure, publish and security steps. Wrote a daily runbook that uses a managed identity with read-only Graph access to warn the team before app secrets and certificates expire.
'''

BRICKS["volvo_observability"] = r'''  \item \textbf{Observability and resilience} (May 2026; Prometheus, Grafana, Alertmanager, HAProxy, .NET, Bicep): Replaced hard-to-read Splunk dashboards with Grafana dashboards the whole team reads at a glance: Argo CD sync status, pipeline runs, Azure DevOps activity per developer and a delivery health index built from recording rules. Added black-box probes that alert on the real cause when the service website is down or slow, and built a failover controller that moves traffic from on-premises hosts to Azure and back on Prometheus signals.
'''

BRICKS["volvo_sharing"] = r'''  \item \textbf{Team knowledge as data, and mentoring:} Wrote the team's coding handbook by reviewing every team repository, published as chapters for people and as a versioned knowledge base for retrieval, and built an LLM-generated 3D knowledge graph of the team's services and processes used for onboarding. Mentor colleagues adopting AI coding agents and local models.
'''

BRICKS["volvo_close"] = r'''\end{itemize}
'''

# ── Experience: earlier roles ────────────────────────────────────────────────
BRICKS["ecarx"] = r'''
\subsection*{ECARX Technology (Automotive Infotainment), Gothenburg}
\textit{Infrastructure Engineer \& Full-Stack Developer, Oct 2024 -- Nov 2025.} Cut cloud spend by 35\%, ran a zero-downtime migration from Azure AKS to on-premises Kubernetes (Helm, Argo CD, Terraform), and reduced MTTR by 35\% with Prometheus and Grafana.
'''

BRICKS["synteda"] = r'''
\subsection*{Earlier roles}
.NET and Azure Integration Developer (Freelance), Synteda AB, Aug 2023 -- Sep 2024 \textbar{} Platform Architect \& Full-Stack Developer, Senior Material (Europe) AB, Jan 2022 -- Dec 2022
'''

BRICKS["senior_material"] = r''''''

# ── Projects ─────────────────────────────────────────────────────────────────
BRICKS["projects"] = r'''
\section*{Open Source --- \href{https://github.com/bluehawana}{github.com/bluehawana}}
\textbf{\href{https://github.com/bluehawana/nvidia-nim-switch-python}{NVIDIA NIM Switch}}: model gateway that lets Claude Code run against 180+ NVIDIA NIM models, with a published compatibility report for all 182. \textbf{\href{https://github.com/bluehawana/Qwen3.827B-SGLang-mpbm5max}{Qwen 27B on Apple Silicon}}: OpenAI- and Anthropic-compatible gateway with admission control and metrics for concurrent serving.
'''

# ── Education and the rest ───────────────────────────────────────────────────
BRICKS["education"] = r'''
\section*{Education, Certifications and Languages}
\textbf{IT-H\"ogskolan}, Gothenburg --- Bachelor's Degree in .NET Cloud Development, 2021--2023\\
\textbf{Campus M\"olndal} --- Java Integration, 2019--2021\\
\textbf{University of Gothenburg} --- Master's Degree in International Business and Trade, 2017--2019\\[3pt]
AWS Certified Solutions Architect -- Associate (2022) \textbar{} AWS Certified Data Analytics -- Specialty (2022) \textbar{} Microsoft Azure Fundamentals AZ-900 (2022) \textbar{} CNCF Scholarship Recipient (CKAD)'''

BRICKS["additional"] = r'''\\[3pt]
\textbf{Languages:} English (fluent) \textbar{} Swedish (B2, professional) \textbar{} Chinese (native)\\
\textbf{Work authorization:} Swedish permanent residence, based in Gothenburg
'''

BRICKS["end"] = r'''
\end{document}
'''

# ── Assembly for this application ────────────────────────────────────────────
ASSEMBLY = [
    "preamble",
    "header",
    "summary",
    "highlights",
    "skills",
    "volvo_open",
    "volvo_platform",
    "volvo_smart_vehicle",
    "volvo_hackday",
    "volvo_supportbot",
    "volvo_devbot",
    "volvo_officebot",
    "volvo_coding_agents",
    "volvo_assets_security",
    "volvo_observability",
    "volvo_sharing",
    "volvo_close",
    "ecarx",
    "synteda",
    "senior_material",
    "projects",
    "education",
    "additional",
    "end",
]


def build() -> str:
    return "\n".join(BRICKS[name] for name in ASSEMBLY)


# ── Cover letter for the application form (the private note to the recruiter
#    is a separate LinkedIn message, not generated here) ─────────────────────
CL_NAME = "Harvad_Li_Coretura_AI_Platform_Engineer_CL"

CL_BRICKS = {}

CL_BRICKS["preamble"] = r'''\documentclass[a4paper,10pt]{article}
\usepackage[left=0.9in,right=0.9in,top=0.8in,bottom=0.8in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\usepackage{xcolor}

\definecolor{darkblue}{RGB}{0,119,181}
\definecolor{linkedinblue}{RGB}{0,119,181}
\hypersetup{colorlinks=true,linkcolor=linkedinblue,urlcolor=linkedinblue,pdfborder={0 0 0}}

\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

\begin{document}
\pagestyle{empty}

{\color{darkblue}
\textbf{Coretura AB}\\
AI Lab\\
Gothenburg, Sweden
}

\vspace{14pt}

\textbf{Dear Hiring Team,}
'''

CL_BRICKS["opening"] = r'''
I am applying for the AI Platform Engineer role in Coretura's AI Lab. I work in the Software Factory at Volvo Group Digital Technology \& Operations (DTO), where I build and run an on-premises AI platform and the agents on top of it, so I already know commercial-vehicle software, its security constraints and how one of your two owners works. \textbf{I am available from 1 January 2027.}
'''

CL_BRICKS["why_coretura"] = r'''
What draws me to Coretura is the AI Lab's mandate: one shared platform that every team uses to build and run AI products safely and reliably. That is what I have been doing at Volvo Group, on a smaller scale. This year I built the first RAG system in DTO, a support chatbot that two teams use every day and that cut ticket processing time by 35\%. I followed it with DevBot, which cut senior pull-request review time from 6 hours to 60 minutes, and OfficeBot, which saves about 90\% of the time it takes to build a slide deck. All of them run on a local model platform that I set up and operate, with no data going to an outside AI service. At Volvo Group HackDay 2026 I led a newly formed team to \textbf{2nd place of 16 teams} with ClaimGenerationBot.
'''

CL_BRICKS["job_match"] = r'''
Your job description asks for someone who sets the platform's direction and also takes on the hands-on work: model access across providers, retrieval, agent harnesses, security, cost, and the observability that shows whether an AI product gives the right answer and not just whether it is running. That matches how I work. My models sit behind OpenAI-compatible endpoints with failover, so a product changes model without code changes. Answers carry sources and a confidence score, and low-confidence answers go to a specialist. Knowledge bases are versioned separately from the application, so a change is reviewed and traceable. I set up Claude Code for my team through Volvo's AI gateway with short-lived tokens instead of API keys, and I use AI coding agents in my own work every day.
'''

CL_BRICKS["smart_vehicle"] = r'''
The project closest to Coretura's mission is \textbf{Volvo Smart Vehicle}: three AI agents working together on one truck record. Co-Driver talks with the driver in the cab, ClaimBot settles who pays for a repair, and Fleet Manager runs the haulier's office. They hand work to each other in real time, so a warning lamp on the dashboard becomes a booked workshop slot and a settled claim before the truck arrives, in about a second per voice turn. I believe an intelligent cabin like this belongs on a shared software platform for commercial vehicles, and I would bring the experience of having built it end to end.
'''

CL_BRICKS["how_i_work"] = r'''
You are also looking for someone who builds to discover and then shares what they learn. I have presented twice to the whole of DTO, with more than 70 colleagues registered each time, I run knowledge-sharing sessions in my team, and I wrote the team's coding handbook, because the biggest multiplier for any engineer is the team around them.
'''

CL_BRICKS["closing"] = r'''
I would welcome the chance to discuss how I can contribute to the AI Lab, and to show a 10-minute demo of Smart Vehicle.

\vspace{6pt}

Sincerely,\\[10pt]
\textbf{Harvad (Hongzhi) Li}

\vspace{10pt}
{\color{darkblue}\rule{\linewidth}{0.6pt}}

{\color{darkblue}\small
Gothenburg, Sweden \textbar{} \href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} \textbar{} +46 76 006 7977\\
LinkedIn: \href{https://www.linkedin.com/in/hzl/}{linkedin.com/in/hzl} \textbar{} GitHub: \href{https://github.com/bluehawana}{github.com/bluehawana}
}

\end{document}
'''

CL_ASSEMBLY = ["preamble", "opening", "why_coretura", "job_match", "smart_vehicle", "how_i_work", "closing"]


def build_cl() -> str:
    return "\n".join(CL_BRICKS[name] for name in CL_ASSEMBLY)



if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUTPUT_DIR / f"{CV_NAME}.tex"
    tex_path.write_text(build(), encoding="utf-8")
    print(f"CV written: {tex_path} ({len(ASSEMBLY)} bricks)")
    cl_path = OUTPUT_DIR / f"{CL_NAME}.tex"
    cl_path.write_text(build_cl(), encoding="utf-8")
    print(f"Letter written: {cl_path} ({len(CL_ASSEMBLY)} bricks)")
