---
description: "Add a company to the ignore list to skip in future job searches"
argument-hint: "[company-name] [reason]"
---

# Ignore Company Command

## Instructions

**This command adds a company to the ignore list so it will be automatically skipped in future job searches.**

## Usage

```
/ignore-company [Company Name] [brief reason]
```

**Examples:**

- `/ignore-company "GEICO" layoffs and toxic culture`
- `/ignore-company "Meta" hiring freeze`
- `/ignore-company Salesforce poor work-life balance`

## Workflow

### Step 1: Add Company to Database

**CRITICAL: Base ignore reasons on company research findings, NOT job fit analysis.**

When adding a company to the ignore list:

- Use research data about the company (layoffs, culture issues, financial problems)
- Do NOT use job-specific criteria (salary range, tech stack mismatch, role requirements)
- Focus on company-wide issues that would affect any role at that company

Add the company to the database using the job_db.py script:

```bash
poetry run python scripts/job_db.py add-ignored-company "[Company Name]" "[reason1]" "[reason2]" --source "[Research source]" --job-id "[job_id if applicable]"
```

**Examples:**

```bash
# Single reason
poetry run python scripts/job_db.py add-ignored-company "GEICO" "Massive layoffs and toxic culture" --source "Glassdoor reviews 2024-2025"

# Multiple reasons
poetry run python scripts/job_db.py add-ignored-company "Microsoft" "Layoffs targeting engineers" "AI automation reducing need for human engineers" --source "TechCrunch 2024-2025" --job-id "4294668541"
```

### Step 2: Mark Current Job as Reviewed (if applicable)

If this company ignore is being added during `/next-job` processing, mark the current job as reviewed:

```bash
poetry run python scripts/job_db.py update-status [job_id] reviewed "User skipped after company research: [brief reason from research]"
```

This closes the job and allows the workflow to continue to the next opportunity.

## Additional Commands

### List All Ignored Companies

```bash
poetry run python scripts/job_db.py list-ignored-companies
```

### Check if Company is Ignored

```bash
poetry run python scripts/job_db.py check-company-ignored "Company Name"
```

## Database Storage

The ignore list is now stored in the SQLite database (`jobs_database.db`) in the `company_ignore` table. This allows for more efficient filtering during job queries - ignored companies are automatically excluded when running `/next-job`.

## Success Confirmation

After adding the company, confirm with the user:
"Added [Company Name] to ignore list. Future jobs from this company will be automatically skipped."
