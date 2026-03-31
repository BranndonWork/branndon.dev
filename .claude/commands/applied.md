---
description: "Record a job application — scrape the JD and mark as applied"
argument-hint: "<linkedin-url | job-url | job-id> [optional notes]"
allowed-tools: ["read", "grep", "glob", "bash", "write"]
---

# Job Applied

Record a job you've already applied to. Scrapes the job description and creates a tracking file marked `applied`.

## Workflow

### Step 1 — Parse the input

Look at `$ARGUMENTS` and determine what was passed:

- **LinkedIn URL** (contains `linkedin.com`): Extract the numeric job ID from `currentJobId=NNNNNN` or `jobs/view/NNNNNN`
- **Raw numeric ID only**: Use directly as a LinkedIn job ID
- **Non-LinkedIn URL**: Use the non-LinkedIn scraping path
- Any text after the URL/ID is treated as a user note to store in `notes`

### Step 2a — LinkedIn job (primary path)

Run the scraper with the extracted job ID:

```bash
cd /Volumes/Storage/Dropbox/workspace/projects/branndon.dev && poetry run python scripts/linkedin_scraper.py --job-id <JOB_ID>
```

Capture stdout to get the exact directory name created (e.g. `Acme-Senior-Software-Engineer`).

### Step 2b — Non-LinkedIn URL

Try in order until one succeeds:
1. `curl -sL "<URL>"` — if it returns readable HTML with a job title, parse it
2. If blocked or empty, use the `/scrape-url` skill to fetch via Playwright

From the response extract: company, title, location, seniority level.
Create `job-search/<Company-Title>/job-posting.md` and `job-search/<Company-Title>/linkedin-url.txt` (use the source URL in the txt file).

### Step 3 — Read job-posting.md

Read `job-search/<dir>/job-posting.md` to confirm: company, title, location, seniority level.

### Step 4 — Write job-application.yaml

Write `job-search/<dir>/job-application.yaml` with status `applied`:

```yaml
job_id: '<JOB_ID>'
status: applied
company: <company from job-posting.md>
title: <title from job-posting.md>
location: <location from job-posting.md>
level: <seniority level from job-posting.md>
linkedin_url: https://www.linkedin.com/jobs/view/<JOB_ID>
application_timeline:
  scraped: '<YYYY-MM-DD>'
  applied: '<YYYY-MM-DD>'
  response_deadline: TBD
notes: '<any notes from user, or empty string>'
follow_up:
  next_action: Monitor for response
  check_date: TBD
last_updated: '<YYYY-MM-DD>'
```

- For non-LinkedIn jobs set `linkedin_url` to the source URL
- Use today's date (from `currentDate` in system context) for `scraped`, `applied`, `last_updated`

### Step 5 — Confirm

Output a summary:
- Directory name
- Company + title
- Confirm all three files exist: `job-posting.md` ✓  `linkedin-url.txt` ✓  `job-application.yaml` ✓

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
