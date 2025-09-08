# Next Job Command

## Instructions

**This command processes the next highest-scoring unprocessed job from your job search pipeline, researches the company, and guides you through the decision process.**

## Workflow

### Step 1: Find Next Job

Use the find_top_jobs script to identify the next highest-scoring unprocessed job:

```bash
poetry run python scripts/find_top_jobs.py --exclude-processed --top 1 --show-details
```

### Step 2: Extract Job Information

Read the job posting file to get full details. Job files are located at `/Volumes/Home/Documents/job-search-2025/data/jobs/` and named `[job_id].md`:

```bash
# Example: For job ID 4293623911, read the file:
# /Volumes/Home/Documents/job-search-2025/data/jobs/4293623911.md
```

**CRITICAL: If the job file does not exist, STOP immediately and inform the user.**

Ask the user: "Job ID [job_id] not found. Would you like me to scrape this job?"

If user says yes, run:

```bash
cd /Volumes/Home/Documents/job-search-2025/
poetry run python job_scraper/scrape_single_job.py [job_id]
```

Then retry reading the job file and continue with the workflow.

Extract the following information:

-   Job title, company, location, salary
-   Full job description and requirements
-   Job ID for tracking
-   Tech stack and requirements

### Step 2.5: Review Job Search Criteria

**CRITICAL: Always read the job search criteria before analysis:**

```bash
# Read the criteria file to understand requirements
Read: docs/JOB_SEARCH_CRITERIA.md
```

**Flag potential concerns early:**

-   Salary below $175K (flag for evaluation - could be acceptable with trade-offs)
-   **People management responsibilities** (flag as major concern - user strongly prefers to avoid)
-   Missing Python in tech stack (flag but evaluate full stack)
-   Recent layoffs or financial troubles (flag for company stability assessment)
-   On-call responsibilities (flag as negative)
-   Meeting-heavy roles (flag if role suggests high coordination/management)

**Note: These are evaluation flags, not automatic disqualifiers. Present the analysis with clear flagged concerns so the user can make informed trade-off decisions.**

### Step 3: Company Research

Automatically research the company using the research script with job-specific naming to avoid conflicts:
Never use glassdoor.com as it is paywalled.

```bash
poetry run python scripts/research_company.py "[Company Name]" --urls "https://www.indeed.com/cmp/[Company-Name]/reviews" --output-dir data/research
```

**Note:** If the results from the indeed reviews are insufficient, supplement with additional research from sources like:

⏺ Web Search("[Company Name] company reviews glassdoor indeed employee experience culture")
⏺ Web Search("[Company Name] shopping platform company layoffs financial troubles funding")
⏺ Web Search("[Company Name] company business model revenue profitability employee count")
⏺ Web Search("[Company Name] working at company salary benefits work life balance 2024 2025")

This will create a research report at `data/research/company-research-report.md` (gitignored to avoid conflicts).

Analyze and present:

-   Employee satisfaction ratings (Glassdoor/Indeed)
-   Recent layoffs or financial health issues
-   Company culture and work-life balance
-   Funding status and business stability
-   Any red flags or positive indicators

### Step 4: Job Analysis

Provide a comprehensive analysis including:

**Company Assessment:**

-   Overall employee rating (/5 stars)
-   Layoff history (2022-2025)
-   Financial stability
-   Growth stage and funding
-   Culture fit indicators

**Role Analysis:**

-   Tech stack match with user's background
-   Estimated match percentage
-   Career growth opportunity
-   Compensation competitiveness
-   Remote work policies

**Strategic Fit:**

-   How this role advances user's career goals
-   Risk vs. reward assessment
-   Comparison to already applied positions

### Step 5: Recommendation

Provide clear recommendation:

-   🟢 **PROCEED** - Strong match, stable company, good opportunity
-   🟡 **CONDITIONAL** - Good match with noted concerns to consider
-   🔴 **SKIP** - Poor match, unstable company, or better options available

Include specific reasoning for the recommendation.

### Step 6: User Decision

Ask the user clearly:
"Based on this analysis, would you like to proceed with [Company Name] - [Job Title]?"

Options:

-   **"yes"** or **"proceed"** - Import job and continue with resume generation
-   **"no"** or **"skip"** - Mark as reviewed and find next job
-   **"research more"** - Gather additional information before deciding

### Step 7A: If Proceeding

1. Import the job using the import script:

    ```bash
    poetry run python scripts/import_job.py [job_id]
    ```

2. **Hand off to existing resume generation workflow:**

    Use the `/generate-resume [Company-JobTitle]` command (see [.claude/commands/generate-resume.md](.claude/commands/generate-resume.md))

    The job directory has been created at: `job-search/[Company-JobTitle]/`

### Step 7B: If Skipping

1. Update job tracker as reviewed:

    ```bash
    poetry run python scripts/job_tracker.py update [job_id] reviewed --notes "User skipped after company research: [brief reason]"
    ```

2. Immediately find and present the next job (repeat from Step 1)

## Important Guidelines

### Research Quality

-   Always verify company information from multiple sources
-   Look for recent news about layoffs, funding, or leadership changes
-   Check employee reviews from the last 6-12 months specifically
-   Note any industry-specific challenges affecting the company

### Decision Support

-   Be honest about potential risks (layoffs, financial issues, culture problems)
-   Compare to already applied positions when relevant
-   Consider user's stated preferences (stability, tech stack, remote work)
-   Factor in the user's current employment situation at Headspace

### Processing Efficiency

-   Use existing scripts to minimize manual work
-   Batch operations where possible (read multiple files, run parallel research)
-   Maintain job tracking throughout the process
-   Research reports are automatically saved to `data/research/` (gitignored) to avoid conflicts between concurrent job analyses

### Follow-Up Actions

-   If proceeding, ensure complete resume generation workflow
-   If skipping, immediately continue to next job to maintain momentum
-   Update all tracking systems consistently
-   Provide LinkedIn URLs for easy application access

## Success Criteria

A successful `/next-job` execution should result in either:

1. **Complete application package** ready for submission (resume, cover letter, LinkedIn URL)
2. **Next viable job candidate** identified and analyzed for decision

The user should have clear, actionable next steps and never be left wondering what to do next.

## Error Handling

-   If no unprocessed jobs remain, indicate completion of pipeline
-   If company research fails, proceed with available information but note limitations
-   If job import fails, provide troubleshooting steps
-   If resume generation fails, check source JSON integrity and requirements matching
