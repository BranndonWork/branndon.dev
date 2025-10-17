---
description: "Process next job in pipeline with research and decision support"
argument-hint: "[additional-instructions]"
---

# Next Job Command

## Instructions

**This command processes the next highest-scoring unprocessed job from your job search pipeline, researches the company, and guides you through the decision process.**

## Workflow

### Step 1: Find Next Job

Use the database query to identify the next highest-scoring unprocessed job from the last 7 days:

```bash
poetry run  python scripts/job_db.py next-job
```

### Step 2: Extract Job Information

The database query already filters out processed jobs and provides all job details directly. Extract the following information from the query result:

-   Job ID for tracking
-   Job title, company, location
-   Resume score
-   Full job description and requirements
-   Tech stack and requirements
-   Created date

**CRITICAL: If no jobs are returned, inform the user that no unprocessed jobs remain in the pipeline.**

### Step 2.1: Company Ignore List (Automatic Filtering)

**NOTE: Companies on the ignore list are now automatically excluded by the database query.**

The `/next-job` command now automatically filters out ignored companies when searching for the next highest-scoring job. You should not receive jobs from ignored companies, but if you encounter one that should be ignored, use:

```bash
/ignore-company "[Company Name]" [brief reason]
```

This will add the company to the database ignore list and automatically exclude future jobs from that company.

### Step 2.2: Generate LinkedIn URL for Verification

**CRITICAL: Before doing research, provide LinkedIn URL for user verification:**

Generate and display the LinkedIn URL using the documented pattern:

-   LinkedIn URL format: `https://www.linkedin.com/jobs/view/{JOB_ID}`
-   Example: `https://www.linkedin.com/jobs/view/4294955231`

**Display the LinkedIn URL immediately** and continue with research in parallel. User can interrupt if job is closed/unavailable to avoid wasted research effort.

Extract the following information:

-   Job title, company, location, salary
-   Full job description and requirements
-   Job ID for tracking
-   Tech stack and requirements

### Step 2.3: Review Job Search Criteria

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
-   On-call responsibilities (flag as negative if mentioned in job description)
-   Meeting-heavy roles (flag if role suggests high coordination/management)

**Note: These are evaluation flags, not automatic disqualifiers. Present the analysis with clear flagged concerns so the user can make informed trade-off decisions.**

### Step 2.4: Early Checkpoint - Initial Assessment

**CRITICAL: STOP HERE and ask the user if they want to continue before doing company research.**

After displaying the job details and flagging obvious concerns, ask the user:

"**Initial Assessment:** Based on the job requirements and description above, would you like me to research this company further?"

**Options:**

-   **"continue"** or **"research"** - Proceed to Step 3 (Company Research)
-   **"skip"** - Mark as reviewed and find next job (go to Step 5B)

**When to skip at this stage:**

-   Niche technical requirements you don't have (e.g. specific proprietary systems)
-   Contract/1099 when you need full-time
-   Salary explicitly listed below threshold
-   Required onsite days
-   Other obvious deal-breakers visible in job description

This checkpoint prevents wasting time researching companies for jobs with clear disqualifiers.

### Step 3: Company Research & Analysis

**IMPORTANT: Follow the comprehensive research workflow documented in:**

```
.claude/commands/job/research.md
```

The research workflow includes:
- Automated company research using scripts and web search
- Management & organizational health assessment
- Comprehensive job analysis
- Risk evaluation and recommendation

**Refer to `job/research.md` for complete research steps and output formatting requirements.**

### Step 4: User Decision

Ask the user clearly:
"Based on this analysis, would you like to proceed with [Company Name] - [Job Title]?"

Options:

-   **"yes"** or **"proceed"** - Import job and continue with resume generation
-   **"no"** or **"skip"** - Mark as reviewed and find next job
-   **"research more"** - Gather additional information before deciding

### Step 5A: If Proceeding

1. Import the job using the import script:

    ```bash
    poetry run python scripts/import_job.py [job_id]
    ```

2. **Hand off to existing resume generation workflow:**

    Use the `/generate-resume [Company-JobTitle]` command (see [.claude/commands/generate-resume.md](.claude/commands/generate-resume.md))

    The job directory has been created at: `job-search/[Company-JobTitle]/`

### Step 5B: If Skipping

1. Update job tracker as reviewed:

    ```bash
    poetry run python scripts/job_db.py update-status [job_id] reviewed "User skipped after company research: [brief reason]"
    ```

2. Immediately find and present the next job (repeat from Step 1)

## Important Guidelines

### Output Formatting

**CRITICAL: Always use proper line breaks and spacing in all output to ensure readability in CLI.**

When presenting job summaries and analysis:

-   **Use double line breaks** between major sections
-   **Each bullet point on separate line** with proper spacing
-   **Avoid long single-line outputs** that run together
-   **Use clear section headers** with markdown formatting
-   **Break up dense information** into readable chunks

**REQUIRED: Use this exact format for job presentation:**

```
## 🎯 Next Job: [Company] - [Title]

---
**Job Details:**
- **Job ID:** [ID]
- **Resume Score:** [Score]/100
- **Posted:** [Date]
- **LinkedIn URL:** `https://www.linkedin.com/jobs/view/[JOB_ID]`

---
**Position Details:**
- **Title:** [Full Job Title]
- **Company:** [Company Name]
- **Location:** [Location/Remote]
- **Experience:** [Years Required]
- **Salary:** [Range if available]

---
**Tech Stack:**
- [Technology 1]
- [Technology 2]
- [Technology 3]

---
**Key Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

---
```

**CRITICAL: Always use horizontal separators (---) between sections and bullet points with proper spacing.**

### Research Guidelines

**For comprehensive research guidelines, refer to `.claude/commands/job/research.md`** which includes:
- Research quality standards
- Decision support criteria
- Output formatting requirements

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
