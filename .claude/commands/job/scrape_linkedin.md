---
description: "Scrape LinkedIn job posting by job ID"
argument-hint: "[job-id]"
allowed-tools: ["bash", "read", "glob"]
---

# LinkedIn Job Scraper

## Instructions

Scrape a LinkedIn job posting using the provided job ID and save it to the job-search directory.

## Workflow

1. Extract the job ID from the user's arguments (look for numeric job ID from LinkedIn URL or direct ID)
2. Run the LinkedIn scraper script: `poetry run python scripts/linkedin_scraper.py --job-id <JOB_ID>`
3. Display the results showing:
   - Directory name where job was saved
   - Company name
   - Job title
   - Files created
4. If the user provided additional context about saving preferences (e.g., `--no-save` or `--raw`), pass those flags to the script

## Notes

- The script will automatically create a directory in `job-search/` with the format `Company-JobTitle`
- If the directory already exists, it will auto-increment with a suffix
- The script saves two files: `job-posting.md` and `linkedin-url.txt`
- Job IDs are typically found in LinkedIn URLs: `https://www.linkedin.com/jobs/view/<JOB_ID>`

## Example Usage

- `/job:scrape_linkedin 1234567890`
- `/job:scrape_linkedin https://www.linkedin.com/jobs/view/1234567890`
- `/job:scrape_linkedin 1234567890 --no-save` (just print, don't save)
- `/job:scrape_linkedin 1234567890 --raw` (output raw HTML)

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
