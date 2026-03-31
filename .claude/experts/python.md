# Python Expert — branndon.dev Job Search Project

## Stack & Tooling
- Python 3.10+, Poetry for dependency management
- Playwright (browser automation, scraping)
- BeautifulSoup4 (HTML parsing)
- curl-cffi (anti-bot HTTP requests)
- diskcache (1-hour caching for API results)
- pyyaml (job tracking YAML files)
- yq (CLI YAML queries across pipeline)

## Key Docs
- `pyproject.toml` — dependency definitions at project root
- `scripts/pyproject.toml` — secondary pyproject for scripts subdirectory (legacy)

## Critical File Paths
- All automation scripts: `scripts/`
- Job scraper: `scripts/hiring_cafe.py`
- Job directory setup: `scripts/setup_job_directory.py`
- PDF generation: `scripts/generate_resume_pdf.py`, `scripts/text_to_pdf.py`
- Company research: `scripts/research_company.py`
- LinkedIn scraper: `scripts/linkedin_scraper.py`
- Job DB (SQLite): `scripts/job_db.py`, `scripts/job_tracker_db.py`
- YAML migration: `scripts/create_yaml_from_jobs.py`

## Architecture Decisions
- Scripts are standalone CLI tools — not a framework, no shared app state
- Each script is self-contained and invoked via `poetry run python scripts/[name].py`
- pathlib exclusively — no `os.path`
- Script output: always redirect to file before grepping — never pipe API output directly
- Caching: diskcache with 1-hour TTL on external API calls (hiring.cafe)
- Job pipeline data: YAML files at `job-search/*/job-application.yaml` — not SQLite (SQLite is legacy)

## Do Not Explore Blindly
These are pre-answered — use these paths directly:
- Job pipeline source of truth: `job-search/*/job-application.yaml`
- Master resume: `webroot/branndon-coelho-resume.json`
- Script entry points: `scripts/*.py` (all executable directly)
