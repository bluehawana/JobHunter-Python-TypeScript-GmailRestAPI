---
description: CV and Cover Letter Formatting Standards
---

# CV and Cover Letter Formatting Standards

This workflow defines the standard formatting preferences for all job application CVs and cover letters.

## CV Formatting

### Color Scheme
- Use **Dark blue** (RGB: 0,51,102) for:
  - Section headers
  - Hyperlinks (email, phone, LinkedIn, GitHub)
  - Section underlines (via titlerule)
- **DO NOT** add a horizontal line between header and first section

### Typography
- Font size: **11pt** (not 10pt)
- **No paragraph indentation** (`\setlength{\parindent}{0pt}`)
- Margins: **0.75in** for balanced layout

### Section Formatting
- Use `titlesec` package for section headers with dark blue underlines
- Format: `\titleformat{\section}{\Large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]`
- Subsections: `\titleformat{\subsection}{\large\bfseries}{}{0em}{}`

### Certifications
- Display each certification on **separate lines** (not all on one line with pipes)
- Example:
  ```
  \begin{itemize}[noitemsep]
  \item AWS Certified Solutions Architect - Associate (Aug 2022)
  \item AWS Certified Developer - Associate (Nov 2022)
  \item Microsoft Certified: Azure Fundamentals (Jun 2022)
  \end{itemize}
  ```

### Header Structure
```latex
\begin{center}
{\LARGE \textbf{Harvad (Hongzhi) Li}}\\[10pt]
{\Large \textit{[Job Title]}}\\[10pt]
\textcolor{darkblue}{email | phone | LinkedIn | GitHub}
\end{center}
```

## Cover Letter Formatting

### Layout (Swedish Business Format)
- **Recipient address** at top left in dark blue
- **Dark blue horizontal line** below recipient address
- **Greeting:** "Hej [Name]," (Swedish informal professional)
- **Spacing:** `\vspace{0.5cm}` after greeting
- **Physical address only** at bottom (no email, phone, LinkedIn, GitHub - those are in CV)

### Structure
```latex
{\color{darkblue}
\noindent [Company Name] \\
[Contact Name] \\
[Email] \\
[Street Address] \\
[Postal Code City, Country]
}

{\color{darkblue}\hrule height 0.5pt}
\vspace{0.3cm}

Hej [Name],

\vspace{0.5cm}
[Body content...]

Sincerely, \\
Harvad (Hongzhi) Li

\vspace{2cm}

{\color{darkblue}\hrule height 0.5pt}
\vspace{0.3cm}

\noindent [Physical Address] \\
[Postal Code City, Country]
```

### Content Guidelines
- **Keep concise** - focus on what's NOT in CV
- **Remove redundant details:**
  - No "4 global offices" or similar non-relevant specifics
  - No cross-cultural communication unless directly relevant
  - Focus on job-relevant experience only
- **Emphasize:**
  - Microsoft stack expertise (C#/.NET, React, Azure)
  - CI/CD and cloud management
  - Cost optimization achievements
  - Business-tech bridge (Master's in International Business)
  - Relevant hobby projects (e.g., SmrtMart.com for e-commerce roles)

### Typography
- Font size: **10pt**
- **No paragraph indentation** (`\setlength{\parindent}{0pt}`)
- Margins: **1in**

## LaTeX Packages Required
```latex
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{hyperref}
```

## Color Definition
```latex
\definecolor{darkblue}{RGB}{0,51,102}
\hypersetup{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}
```

## Section Formatting
```latex
\titleformat{\section}{\Large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\large\bfseries}{}{0em}{}
```

## Notes
- Always compile PDFs twice with pdflatex for proper references
- Clean up auxiliary files after compilation (*.aux, *.log, *.out)
- Section underlines should appear in dark blue under all section headings
