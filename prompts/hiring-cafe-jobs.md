# Hiring Cafe Jobs — Workflow Prompt

This prompt drives the `/hiring-cafe-jobs` slash command. It is the single source of truth for how to fetch, filter, score, and present hiring.cafe job results.

## Step 1: Read the Docs First

Before doing anything else, read these files in order. They define the full preference system:

```
docs/JOB_REQUIREMENTS.md          — hard requirements (remote, no on-call, no management, etc.)
docs/JOB_SEARCH_CRITERIA.md       — salary floors, tech stack preferences, company ratings
docs/over-employment-oe-knowledgebase.md  — OE scoring system (primary ranking factor)
```

Apply everything in those docs as the baseline. Then read the **Current Overrides** section below, which takes precedence over anything in the docs where there is a conflict.

---

## Step 2: Current Overrides & Active Preferences

These supplement or override the docs. Update this section as preferences evolve.

### Title Filter (HARD — disqualify before scoring)
- **Senior Software Engineer, Software Engineer, Backend Engineer only**
- Reject: Staff, Principal, Lead, Manager, Director, Architect (anything with leadership/coordination scope)
- Reason: Staff+ roles carry meetings, planning, cross-team coordination, and doc overhead that conflicts with OE and low-stress goals

### Remote Filter (HARD — disqualify before scoring)
- **Fully remote only — zero in-office days acceptable**
- "Optional hybrid" is not acceptable — application forms often make it a hard requirement regardless of listing copy
- Any mention of in-office days (even 1/week) is a disqualifier

### Primary Ranking Factor: OE Viability
Use the scoring system from `docs/over-employment-oe-knowledgebase.md` as the **primary sort**. Score each job 0–100 across:
1. Work structure & oversight (0-20)
2. Meeting load (0-20)
3. Schedule flexibility (0-20)
4. Work independence (0-20)
5. Organizational camouflage (0-20)

Salary is **secondary**. A $175k fully async job at a 1,000-person company beats a $250k high-intensity startup every time.

### Stack Preference
- Python must be genuinely primary — not one language in a list of ten
- Django is a strong plus but not required
- Elixir, Go, Rust, or other non-Python primary stacks: flag clearly, don't auto-reject but rank lower
- No new language ramp-up — if Python isn't the daily driver, the OE overhead goes up

### Company Size
- Prefer 200–2,000 employees — large enough for organizational camouflage, small enough to not be bureaucratic
- Under 100 employees: flag as high OE risk (you become load-bearing)
- Over 5,000: fine but watch for meeting-heavy cultures

### Salary
- Floor: $175k/yr (per `JOB_REQUIREMENTS.md`)
- Below floor: flag, do not auto-reject if other signals are exceptional
- Excited by $200k+

---

## Step 3: Run the Scraper

```bash
poetry run python scripts/hiring_cafe.py --output json 2>/dev/null
```

Default behavior fetches last 7 days, USD only, Python/remote/IC roles, excludes companies already in:
- `data/company_ignore_list.json`
- `job-search/*/job-application.yaml`

Widen if needed:
```bash
poetry run python scripts/hiring_cafe.py --output json --days 14
```

---

## Step 4: Check Current Pipeline

```bash
yq '.company + " [" + .status + "]"' job-search/*/job-application.yaml 2>/dev/null | sort
```

---

## Step 5: Filter and Score

Apply hard filters first (removes candidates before scoring):
1. Title must be Senior or below — no Staff/Principal/Lead
2. Fully remote — any in-office disqualifies
3. Python must be in the stack

Then score remaining jobs using the OE system from the knowledgebase doc. Estimate scores based on:
- Company size (proxy for camouflage and oversight)
- Known culture signals from funding stage (Series A startups = high intensity)
- Role title scope (SE vs Staff vs Architect)
- Any explicit signals in the requirements summary (on-call, standups, velocity tracking)

---

## Step 6: Present Top 10

Format each result:

```
### #N — OE Score: XX/100 — Salary Score: XX — [Title] @ [Company]
- **Salary:** [range and currency]
- **Stack:** [top 5 tech tools]
- **Posted:** [date]
- **Company:** [size] employees, [funding], founded [year]
- **YOE Required:** [N]+ yrs
- **OE Signals:** [what makes it good/bad for OE — meeting load, oversight, company size, async culture]
- **Why it fits:** [2-sentence match to Python background and OE goals]
- **Watch out for:** [any flags]
- **Apply:** [url]
```

After presenting, ask:
> "Which of these would you like to pursue? I can set up the job directory and start the resume workflow."

---

## Step 7: If a Job Is Selected

Set up the job directory:
```bash
poetry run python scripts/setup_job_directory.py "[Company]" "[Job Title]"
```

Then generate the resume:
```
/generate-resume [Company-JobTitle]
```

---

## File Locations Reference

| What | Where |
|------|-------|
| Hard requirements | `docs/JOB_REQUIREMENTS.md` |
| Salary/stack/company criteria | `docs/JOB_SEARCH_CRITERIA.md` |
| OE scoring system | `docs/over-employment-oe-knowledgebase.md` |
| Part-time platform research | `docs/PART_TIME_JOB_RESEARCH.md` |
| Company ignore list | `data/company_ignore_list.json` |
| Active job pipeline | `job-search/*/job-application.yaml` |
| Scraper script | `scripts/hiring_cafe.py` |
| Job directory setup | `scripts/setup_job_directory.py` |
| Resume generation workflow | `docs/RESUME_GENERATION_COMPLETE.md` |
| This prompt | `prompts/hiring-cafe-jobs.md` |

---

## Notes

- The hiring.cafe scraper caches results for 1 hour — safe to re-run
- Force fresh fetch: `--no-cache`
- Audit what's filtered: `--currencies all --no-filter`
- The scraper's built-in score (0-100) weights salary heavily — **do not use it as the primary sort**; use the OE score instead
