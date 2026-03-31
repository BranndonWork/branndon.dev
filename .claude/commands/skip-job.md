---
description: "Skip a job and update tracking logs with reason"
argument-hint: "[job-id] [reason] or empty for last mentioned job"
---

# Skip Job Command

## Instructions

**This command marks a job as reviewed/skipped in the tracking system and optionally finds the next job.**

## Workflow

### Step 1: Identify Job to Skip

**If job ID provided as argument:**

-   Use the provided job ID

**If no argument provided:**

-   Extract the job ID from the most recent chat history where a job was mentioned
-   Look for patterns like "Job ID: 4294955231" or job references
-   If multiple jobs mentioned, use the most recent one

### Step 2: Determine Skip Reason

**Common skip reasons:**

-   Job posting closed/unavailable
-   Poor salary match
-   Company red flags discovered
-   Tech stack mismatch
-   Management responsibilities
-   Other user-specified reason

**If reason provided in argument:**

-   Use the provided reason

**If no reason provided:**

-   Use "Job posting closed or unavailable" as default
-   Or ask user for brief reason if context unclear

### Step 3: Update Job Tracker

Update the job tracking system to mark as reviewed:

```bash
poetry run python scripts/job_db.py update-status [job_id] reviewed "User skipped: [reason]"
```

### Step 4: Next Job Option

After skipping, ask user:
"Job [job_id] marked as skipped. Would you like me to find the next job?"

**If yes:** Execute the `/next-job` command workflow
**If no:** Confirm skip completed and provide job statistics

## Examples

**With job ID and reason:**

```
/skip-job 4294955231 posting closed
```

**With job ID only:**

```
/skip-job 4294955231
```

**No arguments (uses chat history):**

```
/skip-job
```

## Error Handling

-   If job ID cannot be determined from chat history, ask user to provide it
-   If database update fails, provide manual tracking instructions
-   If job ID doesn't exist in system, log warning but continue

## Success Criteria

-   Job marked as reviewed in tracking system
-   Clear confirmation message to user
-   Optional seamless transition to next job
