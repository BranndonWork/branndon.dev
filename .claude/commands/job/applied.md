---
description: "Quick scrape of job you've already applied to"
allowed-tools: ["bash", "read", "glob", "write"]
---

# Job Applied Command

## Instructions

**This command quickly scrapes and saves a LinkedIn job posting for jobs you've already applied to. No resume generation, no research - just capture the job details and create a minimal tracking file.**

## Workflow

1. **Extract Job ID from User Input**
   - If user provides a LinkedIn URL like `https://www.linkedin.com/jobs/search/?currentJobId=4353672125` or `https://www.linkedin.com/jobs/view/4353672125`, extract the numeric job ID
   - If user provides just the job ID (numbers only), use it directly
   - Look for patterns: `currentJobId=NNNNNN` or `jobs/view/NNNNNN` or just raw digits
   - Any text beyond the URL or job ID is treated as a user note (e.g., "applied through their careers page")

2. **Run LinkedIn Scraper**
   - Execute: `poetry run python scripts/linkedin_scraper.py --job-id <JOB_ID>`
   - The script will automatically:
     - Scrape the job posting from LinkedIn
     - Create a directory in `job-search/` with format `Company-JobTitle`
     - Save `job-posting.md` with the full job description
     - Save `linkedin-url.txt` with the direct LinkedIn URL
     - Handle duplicate directories by auto-incrementing
   - Capture the output to get the exact directory name created

3. **Read the scraped job-posting.md**
   - Read `job-search/<dir>/job-posting.md` to extract: company, title, location, seniority level

4. **Create job-application.yaml**
   - Write `job-search/<dir>/job-application.yaml` with the structure below
   - Use today's date (ISO format: YYYY-MM-DD) for both `scraped` and `applied` fields
   - If the user provided any notes, include them in the `notes` field
   - If no notes were provided, set `notes` to an empty string

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
notes: '<any notes the user mentioned, or empty string>'
follow_up:
  next_action: Monitor for response
  check_date: TBD
last_updated: '<YYYY-MM-DD>'
```

5. **Display Results**
   - Show the directory name where the job was saved
   - Show the company name and job title
   - Confirm all three files were created: `job-posting.md`, `linkedin-url.txt`, `job-application.yaml`
   - Provide the path to the job directory for easy access

## Notes

- This command is for jobs you've ALREADY applied to - no resume or cover letter generation
- The scraper handles directory creation, file naming, and duplicate detection
- If the job ID is invalid or the posting is no longer available, the scraper will error
- Job directories follow the pattern: `job-search/Company-JobTitle/`
- If a directory with that name already exists, it will auto-increment (e.g., `Company-JobTitle-1`)

## Example Usage

- `/job:applied https://www.linkedin.com/jobs/search/?currentJobId=4353672125`
- `/job:applied https://www.linkedin.com/jobs/view/4353672125`
- `/job:applied 4353672125`
- `/job:applied 4353672125 also add a note that I applied through their careers page`

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
