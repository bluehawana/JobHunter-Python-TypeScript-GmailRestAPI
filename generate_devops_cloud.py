"""General DevOps / Cloud / Platform Architect CV, assembled LEGO-style.

Not tied to one employer: this is the version to hand to recruiters asking for
an infrastructure-first profile. Same facts as the AI Platform Engineer CV
(generate_coretura.py) and www.bluehawana.com, reordered so cloud, Kubernetes,
CI/CD, observability and architecture lead and the AI products become the
workloads running on the platform.
"""
from pathlib import Path

from generate_coretura import BRICKS as BASE

OUTPUT_DIR = Path("AI_Job_Application/DevOps_Cloud")
CV_NAME = "Harvad_Li_DevOps_Cloud_Architect_CV"

BRICKS = {}

# ── Frame (shared with the other CVs) ────────────────────────────────────────
BRICKS["preamble"] = BASE["preamble"]

BRICKS["header"] = r'''\begin{center}
{\LARGE \textbf{Harvad Li}}\\[8pt]
{\Large \textit{Senior DevOps \& Cloud Engineer --- Platform Architecture}}\\[8pt]
\textcolor{darkblue}{
  \href{mailto:hongzhili01@gmail.com}{hongzhili01@gmail.com} \textbar{}
  \href{tel:+46728384299}{+46 72 838 4299} \textbar{}
  Gothenburg, Sweden
}\\[3pt]
\textcolor{darkblue}{
  \href{https://www.linkedin.com/in/harvad/}{linkedin.com/in/harvad} \textbar{}
  \href{https://github.com/bluehawana}{github.com/bluehawana} \textbar{}
  \href{https://www.bluehawana.com}{www.bluehawana.com}
}
\end{center}
'''

BRICKS["summary"] = r'''\section*{Profile}
Senior engineer with 6+ years across cloud infrastructure, DevOps and full-stack development, working in automotive at Volvo Group and ECARX. I design platforms and then run them: Kubernetes on Azure and on bare metal, hybrid load balancing and failover between the two, monitoring with Prometheus and Grafana, infrastructure as code with Terraform and Bicep, and the architecture of an on-premises AI platform. I own what I build end to end in production, including its roadmap, incidents and costs. AWS Certified Solutions Architect with a developer's background in .NET, Java and Python.
'''

BRICKS["highlights"] = r'''\section*{Selected Results}
\begin{itemize}
  \item \textbf{Zero-downtime migration from Azure AKS to bare-metal Kubernetes} at ECARX, and \textbf{35\% lower cloud spend}.
  \item \textbf{Record Android 15 AOSP clean build of 7.78 minutes} on the on-premises build servers.
  \item \textbf{60\% shorter deployment time}, \textbf{35\% lower MTTR}, and a 26-server major incident resolved within 5 hours.
  \item \textbf{Hybrid load balancer at Volvo Group} that fails traffic over between on-premises hosts and Azure on Prometheus signals.
  \item \textbf{Architect and operator of Volvo Group DTO's on-premises AI platform}, at zero cloud API cost.
\end{itemize}
'''

BRICKS["skills"] = r'''\section*{Technical Skills}
\begin{itemize}
  \item \textbf{Cloud and architecture:} Azure (AKS, OpenShift ARO, Key Vault, Entra ID, Azure Automation), AWS (certified), hybrid cloud, bare-metal clusters, cloud-to-on-premises migration, high availability, microservices, cost optimisation
  \item \textbf{Kubernetes and containers:} Kubernetes (AKS, OpenShift ARO, on-premises from bare metal: networking, CSI storage, ingress), Helm, Argo CD and GitOps, Docker
  \item \textbf{Load balancing and resilience:} HAProxy, hybrid on-premises and Azure failover, round-robin load balancing, black-box probing
  \item \textbf{Monitoring and observability:} Prometheus (recording rules, black-box probes), Grafana, Alertmanager, Splunk, hybrid monitoring across cloud and data centre, build and delivery metrics, incident response
  \item \textbf{Infrastructure as code and CI/CD:} Terraform, Azure Bicep, Azure DevOps and Azure Pipelines, GitHub Actions, reusable pipeline templates, runbooks, PowerShell and Python scripting
  \item \textbf{AI architecture:} On-premises model serving (Ollama, MLX, SGLang), AI gateways and OpenAI-compatible endpoints, model failover, RAG with source citation, confidence scoring and audit trails, AI coding agents (Claude Code)
  \item \textbf{Security:} Least privilege, secrets management (Key Vault, managed identities, token rotation), Entra ID, secret and certificate expiry monitoring, data sovereignty
  \item \textbf{Languages:} Python (FastAPI), C\#/.NET, Java (Spring Boot), TypeScript/React, Kotlin, SQL, PowerShell; Android AOSP build infrastructure
\end{itemize}
'''

# ── Volvo Group: infrastructure first, AI products as the workloads ──────────
BRICKS["volvo_open"] = r'''\section*{Professional Experience}

\subsection*{Volvo Group --- Software Configurator, Software Factory, DTO, Gothenburg}
\textit{Full-Stack Developer \& AI Solution Engineer, Mar 2026 -- Present}
\begin{itemize}
'''

BRICKS["volvo_observability"] = r'''  \item \textbf{Monitoring and dashboards} (Prometheus, Grafana, Alertmanager): Replaced hard-to-read Splunk dashboards with Grafana dashboards the whole team reads at a glance: Argo CD sync status, pipeline runs, Azure DevOps activity per developer, and a delivery health index built from Prometheus recording rules.

  \item \textbf{Website watchdog} (Prometheus black-box probes, Alertmanager): Built black-box probing of the team's service website from the outside, so that when it is down or slow the alert names the real cause instead of a generic outage.

  \item \textbf{Hybrid load balancer} (HAProxy, .NET, Bicep, Prometheus): Built a failover controller that moves traffic from the on-premises hosts to Azure and back again, driven by Prometheus signals, and taught the design to the team in a knowledge-sharing session.
'''

BRICKS["volvo_pipelines"] = r'''  \item \textbf{CI/CD and configuration as code} (GitHub Actions, Azure Pipelines, Bicep): CI and CD through GitHub Actions, with reusable Azure Pipelines templates for build, infrastructure, publish and security steps. Configuration and knowledge bases live in their own versioned repositories, separate from the container image, so images ship with no secrets and every change is reviewed.
'''

BRICKS["volvo_security"] = r'''  \item \textbf{Secrets and identity} (Azure Automation, Entra ID, PowerShell): Wrote a daily runbook that uses a managed identity with read-only Graph access to warn the team before app secrets and certificates expire. Packaged developer access to Claude models through Volvo's GenAI Hub AI Gateway with short-lived Entra ID tokens instead of API keys.
'''

BRICKS["volvo_platform"] = r'''  \item \textbf{AI platform architecture} (Ollama, Docker, OpenAI-compatible APIs): Designed and run the on-premises model-serving layer for the team's AI products: two Mac Studio M2 Ultra servers with round-robin load balancing and automatic failover, exposed through OpenAI-compatible endpoints so each product can change model without code changes. Models run on Volvo's own hardware, so no data leaves the company and there is no cloud API cost. Products on top share one pattern: retrieval over a versioned knowledge base, answers with sources and a confidence score, escalation to a person when confidence is low, and an audit trail.
'''

BRICKS["volvo_workloads"] = r'''  \item \textbf{Products running on the platform:} Four AI products in four months: Support Chatbot, the first RAG system in DTO, cut support-ticket processing time by 35\%; DevBot cut senior pull-request review time from 6 hours to 60 minutes; ClaimGenerationBot took \textbf{2nd place of 16 teams at Volvo Group HackDay 2026}; and Volvo Smart Vehicle, a three-agent prototype for trucks (\href{https://github.com/bluehawana/CoDriver-LLM-TTS-Demo}{public demo}).
'''

BRICKS["volvo_sharing"] = r'''  \item \textbf{Documentation and mentoring:} Wrote the team's coding handbook from a review of every team repository, and gave two company-wide technical sessions (74 and 71 registered participants).
'''

BRICKS["volvo_close"] = r'''\end{itemize}
'''

# ── ECARX: the core infrastructure role, in full ─────────────────────────────
BRICKS["ecarx"] = r'''
\subsection*{ECARX Technology (Automotive Infotainment), Gothenburg}
\textit{Infrastructure Engineer \& Full-Stack Developer, Oct 2024 -- Nov 2025}
\begin{itemize}
  \item \textbf{Azure to on-premises migration:} Ran the zero-downtime migration from Azure AKS to an on-premises Kubernetes cluster on 4 $\times$ Dell PowerEdge R7625 servers. Built the full stack from bare metal to cluster, including networking, storage (CSI) and ingress controllers, and moved workloads over with Helm and Argo CD while production kept running.
  \item \textbf{Record Android build on bare metal:} Tuned the on-premises build servers at system level for Android AOSP compilation and reached a \textbf{7.78-minute clean build of Android 15}, the fastest the company had recorded, for the infotainment software delivered to Volvo Cars, Polestar, Lynk\&Co and Geely.
  \item \textbf{Cloud cost:} Led the Azure cost optimisation that cut monthly spend by \textbf{35\%} (56,000 to 36,780 SEK) through resource right-sizing, moving expensive workloads to the on-premises cluster, tighter persistent-volume usage and automated cleanup of build artifacts.
  \item \textbf{Monitoring:} Deployed the Prometheus and Grafana stack across Azure and the on-premises data centre, with real-time dashboards for the build infrastructure (CPU, I/O, memory, network), and reduced MTTR by \textbf{35\%} through proactive alerting.
  \item \textbf{CI/CD and infrastructure as code:} Reduced deployment time by \textbf{60\%} with Azure DevOps and GitHub Actions pipelines, and implemented Terraform for all environments.
  \item \textbf{Incident response:} Resolved a 26-server major incident within 5 hours, maintaining SLA compliance.
\end{itemize}
'''

BRICKS["synteda"] = r'''
\subsection*{Synteda AB, Gothenburg}
\textit{.NET and Azure Integration Developer (Freelance), Aug 2023 -- Sep 2024}
\begin{itemize}
  \item Designed talent and office management systems on Azure with C\#/.NET Core and microservices, with Entra ID authentication, Azure Key Vault and Terraform; CI/CD pipelines reduced deployment time by 50\%.
  \item Advised stakeholders on Azure cloud strategy and cost optimisation.
\end{itemize}
'''

BRICKS["senior_material"] = r'''
\subsection*{Senior Material (Europe) AB (Lithium-Ion Battery Manufacturing), Eskilstuna}
\textit{Platform Architect \& Full-Stack Developer, Jan 2022 -- Dec 2022}
\begin{itemize}
  \item Architected the Spring Boot and React platform, migrated the monolith to containerised microservices, and set up GitHub Actions CI/CD.
  \item Managed international server infrastructure and factory IT deployments, bridging the Swedish and Chinese teams during software migrations.
\end{itemize}
'''

BRICKS["pembio"] = r'''
\subsection*{Pembio AB}
\textit{Full-Stack Developer, Oct 2020 -- Sep 2021.} Java Spring Boot and Vue.js platform with microservices and automated testing.
'''

BRICKS["projects"] = r'''
\section*{Open Source --- \href{https://github.com/bluehawana}{github.com/bluehawana}}
\textbf{\href{https://github.com/bluehawana/Qwen3.827B-SGLang-mpbm5max}{Qwen 27B on Apple Silicon}}: model-serving gateway with admission control and metrics; contributed Apple Silicon support to SGLang. \textbf{\href{https://github.com/bluehawana/nvidia-nim-switch-python}{NVIDIA NIM Switch}}: model gateway for 180+ NVIDIA NIM models.
'''

BRICKS["education"] = r'''
\section*{Certifications, Education and Languages}
\textbf{Certifications (2022):} AWS Solutions Architect -- Associate \textbar{} AWS Developer -- Associate \textbar{} AWS Data Analytics -- Specialty \textbar{} Azure Fundamentals AZ-900 \textbar{} CNCF Scholarship Recipient (CKAD)\\[3pt]
\textbf{IT-H\"ogskolan}, Gothenburg --- Bachelor's Degree in .NET Cloud Development, 2021--2023\\
\textbf{Campus M\"olndal} --- Java Integration, 2019--2021\\
\textbf{University of Gothenburg} --- Master's Degree in International Business and Trade, 2017--2019\\[3pt]
\textbf{Languages:} English (fluent) \textbar{} Swedish (B2, professional) \textbar{} Chinese (native)\\
\textbf{Work authorization:} Swedish permanent residence, based in Gothenburg
'''

BRICKS["end"] = r'''
\end{document}
'''

ASSEMBLY = [
    "preamble",
    "header",
    "summary",
    "highlights",
    "skills",
    "volvo_open",
    "volvo_observability",
    "volvo_pipelines",
    "volvo_security",
    "volvo_platform",
    "volvo_workloads",
    "volvo_sharing",
    "volvo_close",
    "ecarx",
    "synteda",
    "senior_material",
    "pembio",
    "projects",
    "education",
    "end",
]


def build() -> str:
    return "\n".join(BRICKS[name] for name in ASSEMBLY)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUTPUT_DIR / f"{CV_NAME}.tex"
    tex_path.write_text(build(), encoding="utf-8")
    print(f"CV written: {tex_path} ({len(ASSEMBLY)} bricks)")
