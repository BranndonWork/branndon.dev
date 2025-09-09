---
description: "Handle job application rejection - update tracking files and documentation"
argument-hint: "[Company-JobTitle] [rejection_date]"
---

# Application Rejected Command

## Instructions

**This command handles the complete workflow when a job application gets rejected, updating all tracking files and documentation consistently.**

## Workflow

### Step 1: Locate Job Directory

Find the job application directory:

```bash
ls -la job-search/[Company-JobTitle]/
```

Verify these key files exist:

- `job-tracking.yaml` - Local job tracking file
- Application materials (resume, cover letter PDFs)

**CRITICAL: If the job directory doesn't exist, ask the user for the correct directory name or job details.**

### Step 2: Calculate Response Time

Determine the response time by checking the application timeline in the local job tracking file:

```bash
yq '.application_timeline.applied' job-search/[Company-JobTitle]/job-tracking.yaml
```

Calculate days between application date and rejection date for analysis.

### Step 3: Update Local Job Tracking File

Update the job-specific tracking file at `job-search/[Company-JobTitle]/job-tracking.yaml`:

**Required updates:**

1. **Status change:**

   ```yaml
   status: "rejected" # Application rejected
   ```

2. **Application timeline:**

   ```yaml
   application_timeline:
     applied: "[existing date]"
     rejected: "[rejection_date]"
     response_time: "[X] days"
   ```

3. **Follow-up section:**

   ```yaml
   follow_up:
     next_action: "Application rejected - no further action needed"
     rejection_date: "[rejection_date]"
     outcome: "[Response time description] despite [strong/moderate] resume match score ([score])"
   ```

4. **Notes section (prepend to existing notes):**

   ```yaml
   notes: |
     **REJECTED [rejection_date]** - [Quick/Slow] rejection ([X] days) despite [resume_score analysis].

     Original assessment:
     [Preserve all existing positive assessment content]

     Rejection suggests possible factors: [analysis of potential reasons]
   ```

### Step 4: Update Main Job Tracking File

Find and update the entry in `data/job_tracking.yaml`:

```bash
# Find the job entry by company or job_id
grep -A 10 -B 2 "[Company Name]" data/job_tracking.yaml
```

**Required updates:**

1. **Status and timestamp:**

   ```yaml
   status: rejected
   last_updated: "[rejection_date] [current_time]"
   ```

2. **Add rejection date:**

   ```yaml
   rejected: "[rejection_date]"
   ```

3. **Update notes with brief summary:**
   ```yaml
   notes: Application rejected after [X] days despite [strong/moderate] resume match ([score] score) - [brief reason analysis]
   ```

### Step 5: Analyze Rejection Pattern

Provide analysis of the rejection including:

**Timing Analysis:**

- Response time (days between application and rejection)
- Compare to typical response times for similar companies
- Flag unusually quick rejections (< 3 days) or slow rejections (> 2 weeks)

**Resume Score Context:**

- Reference the original resume_score from tracking files
- High score (90+) with quick rejection suggests possible factors
- Moderate score (75-89) rejections are more typical

**Potential Rejection Reasons:**

- Technical requirements stricter than advertised
- Experience level mismatch (too senior/junior)
- Domain knowledge gaps
- Internal candidate selected
- Hiring freeze or budget constraints
- Cultural fit screening

### Step 6: Update Documentation References

Check and update any documentation that references this company:

1. **CLAUDE.md examples:**

   ```bash
   grep -n "[Company Name]" CLAUDE.md
   ```

2. **Script examples:**
   ```bash
   grep -n "[Company Name]" scripts/job_tracker.py
   ```

Update example queries if the company was used as a sample.

### Step 7: Verification Commands

Run these commands to verify all updates were applied correctly:

```bash
echo "=== Local Job Tracking Status ==="
yq '.status, .application_timeline.rejected, .follow_up.outcome' job-search/[Company-JobTitle]/job-tracking.yaml

echo "=== Main Job Tracking Status ==="
yq '.jobs | to_entries[] | select(.value.company == "[Company Name]") | {status: .value.status, rejected: .value.rejected, notes: .value.notes}' data/job_tracking.yaml
```

### Step 8: Learning Documentation

Document insights for future applications:

**Pattern Recognition:**

- Track rejection timing patterns across similar companies
- Note common reasons for quick rejections
- Identify companies with consistently quick rejection patterns

**Application Strategy Updates:**

- Should similar roles be approached differently?
- Were job requirements accurately represented?
- Any red flags missed during initial screening?

**Next Steps:**

- Focus energy on remaining active applications
- Apply lessons learned to pending applications
- Update search criteria if patterns emerge

## Important Guidelines

### File Preservation

**DO NOT DELETE OR MODIFY:**

- Resume PDF files
- Cover letter PDF files
- ATS resume JSON files
- Interview preparation materials
- Company research documents
- Original application materials

**REASON:** These remain valuable for reference, learning, and similar future applications.

### Consistent Updates

**ALWAYS UPDATE BOTH FILES:**

1. Local job directory: `job-search/[Company-JobTitle]/job-tracking.yaml`
2. Main tracking: `data/job_tracking.yaml`

**MAINTAIN DATA INTEGRITY:**

- Keep job_id consistent across files
- Preserve original resume_score and assessment
- Add rejection context without removing historical data

### Analysis Quality

**TIMING PATTERNS:**

- < 2 days: Very quick rejection (possible automated screening)
- 2-7 days: Standard quick rejection (likely initial human review)
- 1-2 weeks: Normal timeline (full review process)
- > 2 weeks: Slow rejection (possible internal delays or competing priorities)

**REJECTION REASONS:**
Base analysis on observable factors:

- Resume score vs. response time patterns
- Job requirements vs. background match
- Company research findings (layoffs, hiring freezes)
- Market conditions and competition

## Verification Checklist

After completing the workflow, verify:

- [ ] Local job-tracking.yaml status = "rejected"
- [ ] Local job-tracking.yaml has rejection_date and response_time
- [ ] Local job-tracking.yaml notes updated with rejection header
- [ ] Main data/job_tracking.yaml status = "rejected"
- [ ] Main data/job_tracking.yaml has rejected date
- [ ] Main data/job_tracking.yaml notes updated with brief summary
- [ ] All original application materials preserved
- [ ] Verification commands run successfully

## Success Criteria

A successful `/application-rejected` execution should result in:

1. **Complete tracking updates** across both job tracking files
2. **Preserved application materials** for future reference
3. **Rejection analysis** with timing and potential reasons
4. **Verified data consistency** between tracking systems
5. **Documentation updates** where company was referenced as example

The job application should be cleanly marked as rejected with full context preserved for learning and pattern recognition.

## Error Handling

- If job directory not found, ask user for correct path or job details
- If YAML files are malformed, show error and ask for manual verification
- If grep/yq commands fail, provide manual editing instructions
- If verification commands show inconsistencies, highlight and request review

## Target Job Directory and Rejection Date

$ARGUMENTS
