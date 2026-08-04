# VOLVO INTERVIEW MASTER CHEAT SHEET (45 MINS)

## 1. THE TEAM & INTRO (Lina - Team Lead)
*Goal: Show you are a professional consultant who fits the team.*

**"Tell us about yourself."**
> "I'm a Full Stack .NET Developer with a strong focus on Infrastructure and DevOps. I have extensive experience with **Azure**, **Kubernetes (AKS)**, and **CI/CD pipelines**. I’ve recently worked on migrating enterprise pipelines and building AI-driven tools. I enjoy complex systems like software configuration and I’m used to the consultant mindset—onboarding quickly and delivering value."

**"Why Volvo?"**
> "I admire Volvo's commitment to safety and the shift towards software-defined vehicles. The scale of the 'SW Configurator'—managing millions of parts and software variants—is exactly the kind of complex engineering challenge I thrive on."

---

## 2. PREDICTED QUESTIONS FROM YANN (Senior Analyst / Java Background)
*Yann cares about ANALYSIS, DESIGN, and LEGACY SYSTEMS.*

**Q1: "How do you approach a new feature request? Do you just start coding?"**
*   **The "Analyst" Answer:** "No. I start by understanding the *business goal*. I talk to stakeholders, break requirements into User Stories, and identify dependencies. I think about edge cases (What if the part number is missing? What if the service is down?) *before* writing code."

**Q2: "We have a lot of legacy code here. How do you handle modernizing it?"**
*   **The "Legacy" Answer:** "I use the **Strangler Fig Pattern**. We don't rewrite the whole system at once—that's too risky. We build new features in a modern .NET service and put a proxy in front to route traffic. Gradually, we migrate routes one by one until the old system can be retired."

**Q3: "I see you know Entity Framework. Have you used NHibernate? What's the difference?"**
*   **The "Java/C#" Answer:** "I know NHibernate is common in enterprise systems (and comes from Java's Hibernate). It's very powerful for complex mappings and legacy DB schemas. EF Core is modern and easier for code-first, but I respect NHibernate's maturity and I'm comfortable working with it."

**Q4: "How do you ensure data consistency across multiple services (e.g., SQL + Search Index)?"**
*   **The "Architecture" Answer:** "We can't use distributed transactions (2PC) in microservices—they kill performance. I use **Eventual Consistency**. When we write to SQL, we publish an event (e.g., `PartUpdated`) to a message bus (Azure Service Bus). The Search Service listens to this event and updates the index. It might take a few seconds, but the system stays fast and available."

---

## 3. PREDICTED QUESTIONS FROM DANKO (Consultant / DevOps)
*Danko cares about INFRASTRUCTURE, TOOLS, and DELIVERY.*

**Q1: "How do you manage infrastructure? Terraform?"**
*   **The "HCL" Answer:** "Yes, I use Terraform. It uses **HCL** (HashiCorp Configuration Language), *not YAML*. It lets us version-control our infrastructure. I always use remote state storage (Azure Storage Account) with locking to prevent conflicts."

**Q2: "How do you handle secrets in Kubernetes?"**
*   **The "Security" Answer:** "Never check secrets into Git! I use **Azure Key Vault** with the CSI Driver for Kubernetes. This mounts secrets as volumes or env vars into the pod without exposing them."

**Q3: "Tell me about your CI/CD pipeline."**
*   **The "Pipeline" Answer:** "I use GitHub Actions. My workflow has 3 stages:
    1.  **Build & Test:** Runs unit tests on every commit.
    2.  **Dockerize:** Builds the image and pushes to ACR.
    3.  **Deploy:** Updates the AKS manifest (or uses ArgoCD to sync)."

---

## 4. ARCHITECTURE (The Whiteboard Scenario)
*Scenario: "Design a Parts Search System (Millions of parts, Name/Number/Year)."*

**Draw This:**
`[User]` -> `[APIM]` -> `[.NET API]` -> `[Redis]` -> `[Azure AI Search]` -> `[SQL DB]`

**The Narrative (Say this while drawing):**
1.  **APIM:** Security gateway.
2.  **Redis Cache:** "Check this FIRST. If query is cached, return instantly (10ms)."
3.  **Azure AI Search:** "If not in cache, use this. It's optimized for full-text search and filtering (facets). SQL `LIKE` queries are too slow for millions of rows."
4.  **SQL DB:** "Source of truth for writing data."
5.  **Async/Parallel:** "In the backend, if I need to query SQL and an external API, I use `Task.WhenAll` to run them in **parallel** (simultaneously) rather than sequentially."

**PERFORMANCE IMPROVEMENTS:**
*   **Database:** Use **proper indexing** (Covering Indexes) on frequently searched columns like `PartNumber`. Avoid `SELECT *`.
*   **Search:** Use **Azure AI Search** for full-text queries instead of SQL `LIKE`.
*   **Caching:** Use **Redis** for hot data (reducing DB load by 80%).
*   **API:** Use **Async/Await** to free up threads and handle more concurrent users.
*   **Pagination:** Never return 1,000 items. Always use `Skip()` and `Take()` (e.g., 20 items per page).

---

## 5. FUNDAMENTALS & SENIOR CONCEPTS
*These are the topics that separate Seniors from Mid-level developers.*

### 📚 FROM "C# IN DEPTH" (Jon Skeet) - SENIOR CONCEPTS
*   **Captured Variables (Closures):** "When a lambda uses a local variable, the compiler generates a class to hold it. I’m careful in loops because the *variable* is captured, not the value, which can lead to bugs in async code."
*   **Struct vs Class (Stack vs Heap):** "Structs are value types (Stack), Classes are reference types (Heap/GC). I avoid using Structs unless they are small and immutable (under 16 bytes) to prevent 'Boxing' (performance hit)."
*   **IEnumerable vs IQueryable:** "Critical for DB performance. `IEnumerable` executes in memory (pulls all data). `IQueryable` executes in the database (SQL). I always use `IQueryable` for filtering DB results."
*   **Generics Constraints:** "I use `where T : class` or `where T : new()` to enforce type safety at compile time, avoiding runtime casting errors."

### 🏗️ DDD (DOMAIN DRIVEN DESIGN) - SENIOR CONCEPTS
*   **Aggregate Root:** "The entry point to a cluster of objects. You never modify a child entity directly; you go through the Root to ensure consistency. Example: `Order` is the Root; `OrderItem` is internal. This enforces business rules like 'Order total must be > 0'."
*   **Value Object:** "Defined by value, not ID. Immutable. Two `Money(50)` objects are equal. I use C# `record` types for these to avoid primitive obsession."
*   **Domain Events:** "Side effects (like sending email) are decoupled. When an Aggregate changes, it raises a Domain Event (`OrderPlaced`), handled by a separate handler."

### ⚙️ .NET CORE FUNDAMENTALS
*   **Middleware:** "A pipeline of delegates (Auth, Logging, MVC) that handle requests in order. I use custom middleware for structured logging and global exception handling. **Order matters** (Auth -> Controller)."
*   **MediatR (CQRS):** "Decouples Controllers from Business Logic. The Controller sends a `Command` (Write) or `Query` (Read), and a Handler executes it. This makes testing easy and keeps controllers thin."
*   **DDD (Domain Driven Design):** "Focus on the **Business Domain**, not database tables. I use specific types (`PartNumber` struct) instead of primitives (`string`) to enforce rules. The domain model should be pure C# and not depend on infrastructure."
*   **Clean Architecture (Onion):** "Dependencies point inward. `Domain` (Core) -> `Application` (Interfaces/MediatR) -> `Infrastructure` (EF Core/SQL) -> `Presentation` (API). The Core never depends on the DB."
*   **SOLID Principles:**
    *   **S:** Single Responsibility (One reason to change).
    *   **O:** Open/Closed (Extend, don't modify).
    *   **L:** Liskov Substitution (Subtypes must work like base types).
    *   **I:** Interface Segregation (Small interfaces are better than big ones).
    *   **D:** Dependency Inversion (Depend on abstractions, not concretions - use DI!).
*   **The "Lexis" Question (Lifecycle):** "You mean **Structured Concurrency**. In Kotlin/C#, we `launch` a task (moves to front/active), it `suspends` on I/O (moves to back/backlog), and `resumes` when ready. This lifecycle is managed by a Scope to prevent leaks."

**SYNC vs ASYNC vs PARALLEL (Important!):**
*   **Synchronous:** Blocking. Wait for A to finish before starting B. (Slow for I/O).
*   **Asynchronous:** Non-blocking. Start A, release thread to do other work, resume when A finishes. (Best for Web APIs).
*   **Parallel:** Simultaneous. Run A and B at the *exact same time* on different CPU cores. (Best for heavy calculations or multiple independent queries).
    > "In the Parts Search, I use `async/await` for the API to handle scale, and `Task.WhenAll` (Parallel) to query SQL and AI Search simultaneously to reduce total response time."

---

## 6. LINA'S JOB DESCRIPTION - SPECIFIC MATCHING
*This section maps your skills directly to the key requirements in the Job Description image.*

### 🔹 "Azure Red Hat OpenShift (ARO)"
*   **JD Requirement:** "Cloud-native development on Kubernetes, ideally Azure Red Hat OpenShift (ARO)."
*   **Your Answer:** "I have extensive experience with **AKS (Azure Kubernetes Service)**, which is fundamentally the same as OpenShift (both are Kubernetes). OpenShift adds strict security (SCC) and a developer console on top. My experience deploying to AKS via pipelines translates 100% to ARO, I just need to learn the specific `oc` CLI commands vs `kubectl`."

### 🔹 "Infrastructure as Code (IaC) using Terraform"
*   **JD Requirement:** "Infrastructure as Code using Terraform."
*   **Your Answer:** "I use Terraform (HCL) to provision Azure resources like Key Vault, ACR, and AKS clusters. I manage state in Azure Storage to enable team collaboration."

### 🔹 "GitOps with Argo CD"
*   **JD Requirement:** "GitOps with Argo CD."
*   **Your Answer:** "I implemented GitOps with Argo CD in my Fleet Management Dashboard project (2024). I set up Argo CD to watch our Kubernetes manifests in Git, automatically syncing deployments to our AKS cluster. This eliminated manual kubectl commands and configuration drift. When we push changes to the main branch, Argo CD detects them and applies the updates—Git became our single source of truth for the entire infrastructure state."

### 🔹 "Entra ID (Identity & Access Management)"
*   **JD Requirement:** "Entra ID (formerly Azure AD)."
*   **Your Answer:** "I use Entra ID for securing APIs (OAuth2/OpenID Connect) and for Managed Identities so services can talk to Key Vault/SQL without credentials in code."

### 🔹 "AI-Assisted Development"
*   **JD Requirement:** "Responsible adoption of AI in engineering."
*   **Your Answer:** "I actively use AI tools (like Copilot/Cursor) to speed up boilerplate code generation and write unit tests. I also built a hobby project that uses AI for invoice processing, so I understand how to integrate AI services into .NET apps."

---

## 7. RESUME-SPECIFIC QUESTIONS (YOUR "HOOKS")
*These questions leverage your specific experience at ECARX and Synteda.*

### 🚗 THE AUTOMOTIVE CONNECTION (ECARX Experience)
**Q: "You worked at ECARX supporting Volvo Cars. How is that relevant to this role?"**
*   **The "Insider" Answer:** "At ECARX, I supported the same ecosystem (Volvo, Polestar, Lynk&Co). I understand the specific challenges of automotive IT—high availability requirements, complex hardware/software integration, and the need for rigorous testing. I’ve managed the infrastructure that supports these vehicles, so I hit the ground running."

### 💰 THE "CONSULTANT VALUE" STORY (35% Cost Reduction)
**Q: "Tell us about a time you improved a system."**
*   **The "Value" Answer:** "At ECARX, I noticed our Azure spend was inefficient. I audited our resources, rightsized VMs, and implemented auto-scaling rules. This reduced monthly cloud costs by **35% (from 56k to 36k SEK)** without sacrificing performance. As a consultant, I always look for ways to optimize client value, not just write code."

### 🏗️ THE COMPLEX INFRA STORY (AKS to On-Prem)
**Q: "Tell us about a complex infrastructure challenge."**
*   **The "Danko" Answer:** "I led the migration of a Kubernetes cluster from Azure AKS to on-premise Dell PowerEdge servers. This required setting up the entire metal-to-cluster stack, including networking, storage (CSI), and ingress controllers, ensuring **zero downtime**. This gave me deep knowledge of how Kubernetes works under the hood, not just as a managed service."

### ⚛️ FRONTEND: REACT vs ANGULAR (Defending the Gap)
**Q: "We use Angular/Blazor. I see you mostly use React now."**
*   **The "Adaptable" Answer:** "Yes, my recent projects are React/Next.js, but I have professional experience with Angular (from Synteda) and Blazor (from AddCell). The core concepts—component lifecycle, state management, and dependency injection—are transferable. I can pick up the team's specific Angular patterns in a few days."

### 🚀 THE GITOPS STORY (Fleet Management Dashboard)
**Q: "Tell us about your experience with GitOps and Argo CD."**
*   **The "Modern DevOps" Answer:** "In my Fleet Management Dashboard project (2024), I implemented a full GitOps workflow with Argo CD. The project is a .NET 8 microservices platform deployed on Azure Kubernetes Service. I configured Argo CD to watch our Git repository where all Kubernetes manifests live—deployments, services, ingress rules, everything. When developers merge to main, Argo CD automatically detects the changes and syncs them to the cluster. This gave us:
    - **Zero manual deployments** - No more `kubectl apply` commands
    - **Full audit trail** - Every change is a Git commit with author and reason
    - **Easy rollbacks** - Just revert the Git commit and Argo CD syncs back
    - **Environment parity** - Dev, staging, and prod all use the same GitOps process
    
    The beauty is that Git became our single source of truth. If someone manually changes something in the cluster, Argo CD detects the drift and reverts it back to match Git. This eliminated configuration drift completely."

---

## 8. QUESTIONS TO ASK THEM
1.  **(To Yann):** "How do you balance modernizing the tech stack with the need to maintain the existing legacy logic in the configurator?"
2.  **(To Danko):** "As a consultant, how closely integrated is the team with Volvo's internal platform teams? Do we manage our own AKS clusters?"
3.  **(To Lina):** "What is the biggest challenge the SW Configurator team is facing right now—is it performance, scale, or complexity?"
