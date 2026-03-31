# Resume Expert — branndon.dev

## Candidate Profile
- Branndon Coelho — 15+ years backend engineering
- Core strengths: Python, Django, LLMs, Langchain, Node.js, distributed systems
- Current roles: Senior Software Engineer @ Headspace, Chief Digital Officer @ SpecialNeeds.com
- Targeting: Senior/Staff backend engineer roles, Python/Django-heavy preferred

## Two Resume Pipelines

### Fast pipeline (deterministic, ~7 seconds)
- Entry point: `poetry run python scripts/resume/generate.py <job-dir>/ --pdf`
- What it customizes: experience selection (top 3 of 5 by keyword score), description/achievement selection (top 3 by keyword density), technology ordering (JD-matching techs first), bold injection on matching keywords
- What it does NOT customize: summary text (master verbatim), about text (master verbatim), any sentence rewriting
- Output: `/tmp/resume-poc/` + copied to job dir

### LLM pipeline (generative, 5-10 minutes)
- Documented in `docs/RESUME_GENERATION_COMPLETE.md`
- Rewrites summary, about, descriptions to speak the JD's language
- Generates cover letter
- Use for high-priority roles or when fast pipeline produces weak keyword coverage

## Critical Files
- `webroot/branndon-coelho-resume.json` — master resume, source of truth, never fabricate
- `scripts/resume/keyword_extractor.py` — JD → keyword set (markdown + YAML sources)
- `scripts/resume/experience_scorer.py` — scoring: 2pts/tech match, 1pt/text match, recency bonus
- `scripts/resume/resume_builder.py` — assembles ATS JSON, selects/orders experiences
- `scripts/resume/bold_injector.py` — wraps keywords in `<strong>`, longest-first
- `scripts/resume/templates/summaries.json` — legacy summary templates (no longer used, fast pipeline uses master text)
- `scripts/resume/generate.py` — CLI, also handles PDF via isolated Playwright server

## ATS Output Structure
- `summarySection` — master text + full-vocab bold
- `aboutSection` — master paragraphs + full-vocab bold, reordered by JD keyword density
- `experienceSection.title` — always "Professional Experience"
- `experienceSection.experiences` — top 3 by score, displayed most-recent-first
- `recommendationsSection` — verbatim from master
- `funFactsSection` — always omitted

## Master Resume Experiences (all 5)
1. Chief Digital Officer — SpecialNeeds.com (2023–Present) — Django, Next.js, LLMs, Langchain
2. Senior Software Engineer — Headspace (2022–Present) — Django, Python, Node.js, TypeScript
3. Senior Software Engineer — Webley Systems (2020–2021) — Flask, Python, AWS Lambda, distributed systems
4. Application Architect / Lead Dev — The Penny Hoarder (2014–2020) — Python, Redis, MySQL, AWS, Node.js
5. Personal Projects — RAG, CrewAI, LLMs, agentic AI

## Known Fast Pipeline Limitations
- Summary/about don't speak the JD's language — they're always the master text
- Keyword matching is vocabulary-based: terms not in master resume tech arrays won't score (e.g. JD says "Lambda" not "AWS Lambda")
- JDs with very few tech keywords (<6) produce weak experience differentiation
- HTML entities in scraped company names carry through to filenames (e.g. `&amp;`)

## Decisions Already Made
- Never rewrite master resume content without explicit user request
- All fast pipeline output writes to `/tmp/resume-poc/` first, then copies to job dir
- `index.html` SummarySection has `display:none` — patched in temp webroot during PDF generation
- Experience display order is always most-recent-first regardless of score order
