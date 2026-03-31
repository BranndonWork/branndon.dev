---
description: "Score a job for OE suitability or ask OE strategy questions"
argument-hint: "[LinkedIn URL | job-dir-name | pasted JD text | company name | general question]"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# OE Command — Over-Employment Analysis

This is the single entry point for all OE analysis: score a job from a URL, existing job directory, pasted description, or company name — or ask general OE strategy questions.

## Step 1: Load Full Context

Before any analysis, read the complete knowledgebase:

```
Read: docs/over-employment-oe-knowledgebase.md
```

This contains the scoring matrix, hard disqualifiers, bonuses, community red flags, and interpretation guide. Do not proceed without reading it.

---

## Step 2: Identify Input Mode

Examine `$ARGUMENTS` and determine which mode applies:

| Input | Mode |
|---|---|
| Contains `linkedin.com/jobs/view/` | **Mode A: LinkedIn URL** |
| Looks like a directory name (e.g. `Acme-Senior-Engineer`) | **Mode B: Job directory** |
| Long block of text (200+ words, looks like a JD) | **Mode C: Pasted JD** |
| Short company/role name without directory format | **Mode D: Company/public signals only** |
| Empty or general question | **Mode E: Strategy question** |

---

## Mode A: LinkedIn URL

1. Extract the numeric job ID from the URL.
   - Example: `https://www.linkedin.com/jobs/view/4123456789` → ID is `4123456789`

2. Run the scraper with `--no-save` to fetch content without creating a directory:
   ```bash
   poetry run python scripts/linkedin_scraper.py --job-id [JOB_ID] --no-save > /tmp/oe-job-posting.txt 2>&1
   ```

3. Read the output:
   ```bash
   cat /tmp/oe-job-posting.txt
   ```

4. If scrape fails (rate limit, closed posting), state the error clearly and ask the user to paste the JD text instead. Do not continue with partial info.

5. Proceed to **Step 3: Score**.

---

## Mode B: Job Directory

1. Find the job directory. Try exact match first:
   ```bash
   ls job-search/ | grep -i "[ARGUMENT]"
   ```

2. Read the job posting:
   ```
   Read: job-search/[matched-directory]/job-posting.md
   ```

3. Also check for any existing notes:
   ```bash
   ls job-search/[matched-directory]/
   ```

4. Proceed to **Step 3: Score**.

---

## Mode C: Pasted JD Text

The job description is directly in `$ARGUMENTS`. Use it as-is.

Proceed to **Step 3: Score**.

---

## Mode D: Company / Public Signals Only

Score based on publicly available signals: company size, stage, funding, industry, known culture (e.g. Glassdoor reviews if you can WebSearch).

Optionally run a quick search:
```
WebSearch("[Company Name] engineering culture remote work async meeting load employee reviews 2024 2025")
```

Note clearly in the output that this score is based on public signals only, not a full JD.

Proceed to **Step 3: Score** with available information.

---

## Mode E: Strategy / General Question

Answer using the full knowledgebase context. Cover:
- Relevant scoring categories if applicable
- OPSEC guidance from the community best practices section
- J1/J2/J3 prioritization logic
- Any specific concerns raised by the user

Do not produce a score output. Provide a focused, practical answer.

---

## Step 3: Score the Job

Apply the **4-Category SSE Scoring Matrix** from the knowledgebase. Do this systematically:

### 3A: Check Hard Disqualifiers First

Before scoring categories, scan the JD for these automatic penalties. Report any found **prominently at the top of the output**:

| Disqualifier | Penalty |
|---|---|
| Surveillance software (Teramind, Hubstaff, screenshot tools, time logging) | -20 pts |
| Required on-call rotation as primary responsibility | -20 pts |
| Billable hours / consulting / staffing model | -20 pts | **Only applies when the JD contains explicit evidence**: timesheets, billable hour tracking, audited time, or multiple client assignment rotation. Do NOT apply just because the employer is a consulting or staffing company — engineers placed at client teams typically fold in like direct hires with no extra time overhead. If the JD is ambiguous, surface it in "Watch For" with interview questions instead of applying the penalty. |
| Security clearance investigation required | -15 pts |
| In-office requirements >1 day/week | -15 pts |
| Series A or earlier stage startup | -10 pts |

### 3B: Score the Four Categories

For each category, identify the specific signals in the JD that justify the score. Don't assign a score without citing a signal.

**Category 1: Work Measurement Model (0–25 pts)**
What signals how the company measures your work?
- Look for: "results-oriented", "outcome-based", "async-first", "core hours", "always available", activity monitoring mentions

**Category 2: Meeting Load Delta from SSE Baseline (0–25 pts)**
SSE baseline = ~10 hrs/week (standup, sprint planning, retro, 1:1, team sync).
- Look for: async standups, optional attendance, camera requirements, cross-team syncs, stakeholder involvement, client exposure
- Score the DELTA from baseline, not the absolute presence of standard Agile ceremonies

**Category 3: Schedule & On-Call Constraints (0–25 pts)**
- Look for: core hours language, timezone requirements, on-call mentions, travel requirements, security clearance mentions, 24/7 availability expectations

**Category 4: Organizational Camouflage (0–25 pts)**
- Look for: company size clues (headcount, funding stage), distributed team mentions, team size, product maturity (maintenance vs growth), organizational structure
- **"Working on a team" is universal — do NOT score it.** Every SSE works on a team. Camouflage measures whether *you specifically* are visible and load-bearing within that structure. Only penalize when the JD signals small headcount, sole ownership of critical systems, or founding-team dynamics where your individual presence/absence would be immediately noticed.
- **Executive visibility phrases are a real camouflage penalty.** JDs that advertise direct access to leadership — "work directly with the CTO", "report to the VP of Engineering", "collaborate closely with founders", "high visibility across the organization" — are signaling that you will be a known quantity to decision-makers. This is the opposite of camouflage. Treat these as explicit low-camouflage signals and score accordingly.

### 3C: Apply Bonuses

Check for these:
- Globally distributed team: +5
- Mature/maintenance-mode product: +5
- PE-owned or large bureaucratic parent org: +5
- No equity offered (easy exit, less "ownership" pressure): +3

---

## Step 4: Output the Score

Use exactly this format:

```
## OE Score — [Job Title] @ [Company]

### Disqualifiers
[List each disqualifier found with the penalty, or "None identified"]

### Scoring
| Category | Score | Key Signal |
|---|---|---|
| Work Measurement Model | XX/25 | [1 sentence from JD] |
| Meeting Load Delta | XX/25 | [1 sentence from JD] |
| Schedule & On-Call | XX/25 | [1 sentence from JD] |
| Org Camouflage | XX/25 | [1 sentence from JD] |
| Bonuses/Penalties | +/-X | [reason] |
| **Total** | **XX/100** | |

### Verdict
[EXCELLENT / GOOD / MODERATE / POOR / PASS] — [1–2 sentences summarizing the OE viability]

### Key OE Signals
**Green flags:**
- [signal 1]
- [signal 2]

**Red flags:**
- [signal 1]

### Watch For
[Ambiguous items that should be clarified in interview — e.g., "JD mentions 'availability' but doesn't define it; probe in interview"]
```

---

## Score Interpretation Reference

| Range | Label | Meaning |
|---|---|---|
| 85–100 | EXCELLENT | Strong OE candidate. Multiple green flags. |
| 70–84 | GOOD | Viable. Standard management needed. |
| 50–69 | MODERATE | Manageable but requires care and good performance. |
| 30–49 | POOR | Significant friction. High cognitive overhead. |
| 0–29 | PASS | Not compatible with OE for an SSE. |

---

## Important Scoring Notes

- **Universal SSE traits do NOT reduce score**: Agile ceremonies, code reviews, CI/CD, team collaboration, Git — these are baseline, not negatives. Do not penalize them.
- **"40 hours per week" is universal contract language**: Every full-time SSE offer says this. It is not a work measurement signal and must not reduce the Work Measurement Model score. Only explicit time tracking tools, activity monitoring, or timesheet requirements are signals worth scoring.
- **Score the variance**: Only traits that differ meaningfully from the SSE baseline should influence the score.
- **Consulting/staffing model disqualifier requires JD evidence**: Do not apply the -20 penalty simply because the employer is a consulting or staffing company. Engineers embedded at client teams routinely work with standard hours, no time tracking, and no extra requirements — indistinguishable from direct hires. Apply the penalty only when the JD explicitly mentions billable hours, timesheets, audited time, or rotating client assignments. Otherwise, note it in "Watch For" with specific interview questions to clarify (e.g., "Are there timesheet or billing hour requirements?", "Is this a single long-term engagement or rotational?").
- **One hard disqualifier can sink an otherwise good job**: Report them first. A 75-point job with a confirmed on-call rotation as primary responsibility is a PASS.
- **Uncertainty is not a penalty**: If the JD is ambiguous about meeting load, score at baseline (15/25) and surface it in "Watch For". Don't guess in either direction.
- **Company signals matter when JD is thin**: For staffing/recruiting agency postings, the company matters more than the recruiter JD. Research the actual employer.
