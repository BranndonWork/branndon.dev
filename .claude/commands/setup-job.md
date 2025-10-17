---
description: "Set up standardized job directory with templates and interview structure"
argument-hint: "[company-name] [job-title] or empty to prompt for details"
---

# Setup Job Command

## User Input

$ARGUMENTS

## Instructions

USe the above user input to get company name and job title. If missing, ask user for details.

Run the setup script:

```bash
poetry run python scripts/setup_job_directory_simple.py "Company Name" "Job Title"
```

This creates `job-search/Company-JobTitle/` with:

-   All template files (job-tracking.yaml, resume templates, etc.)
-   `interviews/` and `correspondence/` subdirectories
-   Skips existing files to avoid overwriting

Tell user next steps:

1. Fill out `job-tracking.yaml` first
2. Add job posting to `job-posting.md` if available
3. Follow RESUME_GENERATION_COMPLETE.md workflow
