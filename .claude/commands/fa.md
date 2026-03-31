---
description: "Fast apply: LinkedIn URL or job dir → ATS JSON + PDF in ~10 seconds"
argument-hint: "[linkedin-url-or-job-dir]"
allowed-tools: ["bash", "read", "glob"]
---

# /fa

Given a LinkedIn job URL or an existing job directory, generate a fully customized ATS resume PDF in seconds using the deterministic pipeline (no LLM).

## Workflow

**If the argument is a LinkedIn URL:**
1. Extract the job ID from the URL (the `currentJobId` query param, or the ID in a `/jobs/view/{id}` URL)
2. Run: `poetry run python scripts/linkedin_scraper.py --job-id {job_id}`
3. Note the job directory name printed by the scraper
4. Run: `poetry run python scripts/resume/generate.py job-search/{dir}/ --pdf`
5. Report the PDF path and elapsed time

**If the argument is a job directory path (e.g. `job-search/Recharge-Platform-Software-Engineer/`):**
1. Skip scraping — directory already has `job-posting.md`
2. Run: `poetry run python scripts/resume/generate.py {dir}/ --pdf`
3. Report the PDF path and elapsed time

## Output

All files are written to `/tmp/resume-poc/` — nothing in the project tree is modified.
Report the full PDF path at the end so the user can open it immediately for review.

## Notification Step

Before asking the user whether they applied, run this command directly (do NOT use the `/notify` skill — call the CLI directly):

```bash
cd /Volumes/Storage/Dropbox/workspace && poetry run python -m lib.notifications.notify.main "Resume ready for [Company Name]" --buttons "Dismiss,Open iTerm" --action "Open iTerm:open -a iTerm" --sound Ping
```

This sends a blocking modal with an "Open iTerm" button that activates iTerm2 when clicked.

## Post-PDF Step

After reporting the PDF path, use the `AskUserQuestion` tool to ask:

> "Have you applied for this job?"

- **Yes** → run the `/applied` workflow for this job
- **No** → do nothing more

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
