# Hunter — branndon.dev Job Search Project

## What This Project Is
A personal job search management system for Branndon Coelho — a senior Python/Django backend engineer with 15+ years experience, currently employed at Headspace, running an active job search with OE (over-employment) as a primary goal.

## Hard Requirements (Non-Negotiable)
- Fully remote — zero in-office days, "optional hybrid" is a disqualifier
- Individual contributor — no people management, no Staff/Principal/Lead title scope
- No salary floor — any compensation is acceptable (unemployed since Oct 2025)
- Python primary or hybrid Python/React stack — full stack roles mixing Python/Django + React/TypeScript are acceptable

## Primary Ranking Factor: OE Viability
OE score (0-100) using the 4-category matrix in `docs/over-employment-oe-knowledgebase.md` is the primary sort. Salary is secondary. See `/expert:oe` for scoring.

## The Expert Team
- `/expert:hunter` — you, the lead. Strategy, pipeline oversight, routing.
- `/expert:oe` — OE scoring and sustainability analysis
- `/expert:interview` — interview prep, STAR coaching, system design, company research
- `/expert:communications` — resume customization, cover letters, all emails

## Key Docs
- `docs/RESUME_GENERATION_COMPLETE.md` — complete resume generation workflow (self-contained)
- `docs/JOB_REQUIREMENTS.md` — hard requirements and scoring thresholds
- `docs/over-employment-oe-knowledgebase.md` — OE scoring system
- `docs/JOB_SEARCH_CRITERIA.md` — salary floors, tech preferences, company size targets

## Critical File Paths
- Master resume (source of truth): `webroot/branndon-coelho-resume.json`
- ATS resume template: `docs/templates/resume-ats-template.json`
- Job tracking template: `docs/templates/job-tracking-template.yaml`
- Active pipeline: `job-search/*/job-application.yaml`
- Company ignore list: `data/company_ignore_list.json`
- Job scraper: `scripts/hiring_cafe.py`
- Job directory setup: `scripts/setup_job_directory.py`

## Pipeline Structure
Each job lives in `job-search/[Company-JobTitle]/` with a `job-application.yaml` tracking file.

Query pipeline state:
```bash
yq '.company + " [" + .status + "]"' job-search/*/job-application.yaml | sort
```

## Candidate Background (Key Facts)
- Current: Senior Software Engineer @ Headspace (2022–present)
- Previous: Application Architect/Lead/Senior Developer @ The Penny Hoarder; Senior SE @ Webley Systems
- Core stack: Python, Django, PostgreSQL, REST APIs, AWS
- Major achievements: Performance optimization (2.7s → 0.89s load time), ML email system, GDPR compliance, platform scaling
- 15+ years experience

## Decisions Already Made
- OE score is primary ranking — salary is secondary
- Title filter: Senior SSE, SSE, Backend Engineer only — no Staff, Principal, Lead, Manager
- Company size sweet spot: 200–2,000 employees
- Under 100 employees = high OE risk (load-bearing)
- Series A or earlier = always flagged
