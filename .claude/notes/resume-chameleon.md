🦎 ResumeChameleon - Claude Code Powered Job Search Platform

Comprehensive Open Source Migration Plan

---

★ Insight ─────────────────────────────────────
Your current system is tightly coupled to:

1. Personal webroot - React app that renders your resume
2. Personal resume JSON - branndon-coelho-resume.json
3. Database/file-based job pipeline - mixing job scraping with application tracking

The key to open sourcing is separating the resume generation engine from your personal website infrastructure.
─────────────────────────────────────────────────

---

🎯 Project Name: ResumeChameleon

Why Chameleon?

- Chameleons are masters of adaptation (like job seekers adapting to different roles)
- They change colors to match their environment (like customizing resumes for each job)
- Patient and strategic hunters (job search requires persistence and strategy)
- They display the right colors at the right time (highlighting your best-fit skills for each opportunity)

Tagline: "Adaptive Job Hunting with AI-Powered Resume Customization"

---

📊 Current Architecture Analysis

Webroot Dependencies (MUST REMOVE)

Current Flow:

1. generate_resume_pdf.py → launches browser
2. Browser loads http://localhost:8000 (webroot/index.html)
3. React app fetches branndon-coelho-resume.json OR branndon-coelho-resume-ats.json
4. Playwright captures PDF from rendered page

Problems for Open Source:

- Requires running local web server
- Tied to your personal website styling
- Resume JSON includes personal info
- Not portable/distributable

Personal Info Coupling (MUST ANONYMIZE)

Files with personal data:

- webroot/branndon-coelho-resume.json - Complete work history
- webroot/assets/images/branndon-coelho.jpg - Photo
- .claude/commands/\* - References to Headspace, personal job search
- docs/RESUME_GENERATION_COMPLETE.md - Examples using your name/experience

---

🏗️ New Architecture (Open Source Ready)

Core Principle: Template-Based HTML Generation

New Flow:

1. User provides master resume JSON (their own)
2. LinkedIn URL provided → extract job details
3. Claude analyzes job → customizes resume JSON
4. Python generates HTML from Jinja2 template (no React, no server)
5. Playwright captures PDF from file:// protocol

Directory Structure

resumechameleon/
├── .claude/
│ └── commands/
│ ├── generate-application.md # NEW: Main entry point
│ ├── research-company.md # Keep (generic)
│ ├── setup-job.md # Keep (generic)
│ └── ignore-company.md # Keep (generic)
├── templates/
│ ├── resume-template.html # NEW: Jinja2 template (replaces webroot)
│ ├── resume-template.css # NEW: Styling
│ ├── master-resume-template.json # Anonymized template
│ ├── job-tracking-template.yaml # Keep (already generic)
│ └── cover-letter-template.txt # Keep (already generic)
├── scripts/
│ ├── linkedin_parser.py # NEW: Extract job from LinkedIn URL
│ ├── resume_generator.py # NEW: Jinja2 → HTML
│ ├── pdf_generator.py # Simplified (file:// only)
│ ├── company_research.py # Keep (already generic)
│ ├── text_to_pdf.py # Keep
│ └── job_tracker_yaml.py # Keep (YAML tracking)
├── docs/
│ ├── GETTING_STARTED.md # NEW: User onboarding
│ ├── RESUME_CUSTOMIZATION_GUIDE.md # Anonymized version of current doc
│ └── WORKFLOW.md # LinkedIn URL → Application flow
├── examples/
│ ├── sample-master-resume.json # Fictional person
│ └── sample-job-application/ # Full example with generated files
├── applications/ # User's job directories (gitignored)
│ └── Company-JobTitle/
├── .gitignore
├── pyproject.toml
├── README.md
└── LICENSE (MIT or Apache 2.0)

---

🔄 Migration Steps

Phase 1: Remove Webroot Dependency

1.1 Create Jinja2 HTML Template

- Convert webroot/index.html React code to Jinja2 template
- Inline all CSS (no external dependencies)
- Remove jQuery/React CDN dependencies
- Pure HTML + inline styles for PDF rendering

  1.2 Build HTML Generator Script

# scripts/resume_generator.py

def generate_resume_html(resume_json: dict, output_path: str):
"""Generate static HTML from resume JSON using Jinja2"""
template = env.get_template('resume-template.html')
html = template.render(resume_data=resume_json)
with open(output_path, 'w') as f:
f.write(html)

1.3 Update PDF Generator

# scripts/pdf_generator.py

async def generate_pdf(html_file: Path, output_pdf: Path):
"""Generate PDF from local HTML file (no server needed)"""
async with async_playwright() as p:
browser = await p.chromium.launch()
page = await browser.new_page()
await page.goto(f'file://{html_file.absolute()}')
await page.pdf(path=output_pdf, format='A4', ...)

Phase 2: LinkedIn URL-Based Workflow

2.1 Create LinkedIn Parser

# scripts/linkedin_parser.py

def extract_job_from_linkedin(url: str) -> dict:
"""
Extract job details from LinkedIn URL - Parse job ID from URL - Scrape job posting (or use API if available) - Extract: title, company, description, requirements
"""

2.2 New Main Command

# .claude/commands/generate-application.md

USAGE: /generate-application https://www.linkedin.com/jobs/view/123456789

WORKFLOW:

1. Parse LinkedIn URL → extract job details
2. Research company (optional but recommended)
3. Analyze job requirements vs master resume
4. Customize resume JSON
5. Generate HTML → PDF
6. Generate cover letter
7. Create job directory with all files

Phase 3: Anonymize Documentation

3.1 Create Generic Examples

- Sample resume: "Alex Johnson" (fictional software engineer)
- Sample applications with common job types
- Remove all Branndon-specific references

  3.2 Rewrite Documentation

- RESUME_CUSTOMIZATION_GUIDE.md - Generic principles
- Remove company names (Headspace, Penny Hoarder)
- Use placeholder examples

Phase 4: User Configuration System

4.1 Config File

# resumechameleon.config.yaml (user creates this)

master_resume: ./my-resume.json
applications_dir: ./applications
preferences:
min_salary: 150000
avoid_management: true
preferred_stack: [Python, Django, PostgreSQL]
work_arrangement: [Remote, Hybrid]

4.2 First-Time Setup
poetry run resumechameleon init

# Guides user through:

1. Creating master resume JSON
2. Setting preferences
3. Creating config file

---

🗑️ Commands to Remove/Transform

❌ REMOVE (Too Personal/Specific)

- /next-job - Assumes external job database scraping system
- /application-rejected - Too workflow-specific

✅ KEEP (Generic/Useful)

- /setup-job → Rename to /setup-application
- /skip-job → Remove (not needed with LinkedIn URL flow)
- /ignore-company → Keep
- /generate-resume → Replace with /generate-application

🔄 TRANSFORM

- /next-job logic → Optional addon module for job scraping
- Database tracking → Simplified YAML tracking only

---

📝 Key Files Transformation

Master Resume Template

{
"overviewData": {
"name": "[Your Full Name]",
"positions": ["[Primary Role]", "[Secondary Role]"],
"imageSrc": "path/to/photo.jpg", // Optional
"socialLinks": [
{"url": "[LinkedIn URL]", "icon": "fab fa-linkedin-in"},
{"url": "[GitHub URL]", "icon": "fab fa-github"},
{"url": "[Website]", "icon": "fas fa-globe"},
{"url": "mailto:[email]", "icon": "fas fa-envelope"}
]
},
"experienceSection": {
"experiences": [
{
"position": "[Job Title]",
"companyName": "[Company]",
"time": "YYYY - YYYY",
"description": ["[Role description]"],
"achievements": ["[Achievement 1]"],
"technologies": ["Tech1", "Tech2"]
}
]
}
}

Workflow Documentation

# WORKFLOW.md

## Quick Start

1. **Provide LinkedIn Job URL:**
   /generate-application https://www.linkedin.com/jobs/view/123456789

2. **Claude will:**
   - Extract job details
   - Research company (with your approval)
   - Analyze requirements vs your resume
   - Customize resume and generate PDF
   - Create cover letter
   - Package everything in application folder

3. **Review and apply!**

---

🚀 Launch Checklist (v1.0)

Must-Have Features

- LinkedIn URL parsing (job ID extraction)
- Jinja2 HTML template system (no webroot)
- PDF generation from file:// (no server)
- Company research integration
- Master resume → customized resume flow
- Cover letter generation
- YAML job tracking
- Configuration system

Nice-to-Have (Post v1.0)

- Job board integrations (Indeed, etc.)
- Resume parsing (upload existing PDF)
- Web UI (optional, for non-CLI users)
- Resume analytics (ATS scoring)
- Interview prep automation

Documentation

- README with quick start
- Installation guide
- Master resume creation guide
- Workflow documentation
- Contributing guidelines
- Example applications

---

🎨 Branding & Marketing

Project Description:
ResumeChameleon is an AI-powered job application assistant built for Claude Code. Provide a LinkedIn job URL, and ResumeChameleon automatically researches the company, customizes your resume to match job requirements,
generates ATS-optimized PDFs, and creates compelling cover letters—all while maintaining complete honesty and never fabricating experience.

Key Differentiators:

1. Claude Code Native - Designed specifically for Claude Code workflow
2. Truthfulness First - Never fabricates skills or experience
3. LinkedIn-First - Start with just a URL, no complex setup
4. Company Intelligence - Automated research with red flag detection
5. Zero Infrastructure - No servers, no databases, pure Python + templates

---

🛠️ Technical Implementation Notes

★ Insight ─────────────────────────────────────
Critical architectural changes:

1. Template engine: Jinja2 replaces React (eliminates server dependency)
2. File protocol: file:///path/to/resume.html replaces http://localhost:8000
3. Inline styles: All CSS embedded in HTML for PDF rendering
4. Job initiation: LinkedIn URL replaces database queries

This dramatically simplifies deployment - users just need Python/Poetry, no web stack.
─────────────────────────────────────────────────

---

📦 Repository Structure

Main Repo: github.com/[your-username]/resumechameleon

Key Files:
README.md # Project overview, quick start
INSTALLATION.md # Poetry setup, dependencies
WORKFLOW.md # LinkedIn URL → application flow
CONTRIBUTING.md # How to contribute
LICENSE # MIT or Apache 2.0
pyproject.toml # Python dependencies
.claude/settings.json # Claude Code configuration

---

🎯 Success Metrics (Post-Launch)

- GitHub stars/forks
- User testimonials (successful job placements)
- Community contributions
- Documentation clarity (measured by support questions)
- Feature adoption (which commands are most used)

---

Next Steps

Would you like me to:

1. Start the migration - Create the new repo structure in a separate directory?
2. Build the Jinja2 template - Convert your React resume to template first?
3. Create the LinkedIn parser - Start with job URL extraction?
4. Write the documentation - Begin with README and GETTING_STARTED?

The cleanest approach would be creating a parallel resumechameleon/ directory, building the new system piece by piece, then testing with your actual job search before releasing. This lets you continue using your
current system while developing the open source version.

What's your preference for getting started?
