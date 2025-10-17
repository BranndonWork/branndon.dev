---
description: "Research and analyze companies and jobs for decision support"
argument-hint: "[company-name] [job-id]"
---

# Job Research Command

## Instructions

**This command performs comprehensive company research and job analysis to support informed application decisions.**

## Company Research Process

### Step 1: Automated Company Research

Research the company using the research script with job-specific naming to avoid conflicts:
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

### Step 2: Management & Organizational Health Assessment

**CRITICAL: Actively evaluate signs of company mismanagement and organizational chaos.**

#### Required Additional Research

Perform this targeted search to detect management dysfunction:

```bash
WebSearch("[Company Name] management leadership direction communication chaos confusion priorities processes dysfunction")
```

#### Red Flags That Indicate Mismanagement

**🚩 Severe Management Issues:**

-   **Frequent Layoffs Pattern:** "Layoffs every 6 months," "annual layoffs to meet targets"
-   **Strategic Confusion:** "Priorities change weekly," "projects cancelled constantly," "don't know what we're building"
-   **Management Ratings:** Below 3.0/5 on Glassdoor with comments like "poor leadership," "no direction"
-   **Process Breakdown:** "No processes exist," "everything is ad-hoc," "processes change constantly"
-   **Communication Failures:** "Zero transparency," "leadership avoids conversations," "find out through rumors"
-   **High Turnover Signals:** "Everyone is leaving," "revolving door," "can't retain talent," "all the good people left"

#### Evaluation Criteria

**Rate Management Health:**

-   **🟢 Well-Managed:** Clear processes, stable leadership, consistent strategy, good communication
-   **🟡 Management Concerns:** Some dysfunction but manageable, isolated team issues
-   **🔴 Severely Mismanaged:** Multiple red flags, systemic chaos, avoid at all costs

**Include in Analysis:**

-   **Management Rating:** [Well-Managed/Concerns/Severely Mismanaged]
-   **Specific Issues Found:** List key problems discovered
-   **Impact Assessment:** How dysfunction affects day-to-day work experience

### Step 3: Job Analysis

Provide a comprehensive analysis including:

**Company Assessment:**

-   Overall employee rating (/5 stars)
-   **Management Health:** [Well-Managed/Concerns/Severely Mismanaged] with specific issues identified
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

**Salary Range Guidelines:**

**Example:**
- Range: $148k - $274k
- ✅ This is EXCELLENT - high end ($274k) exceeds excited threshold
- With 15 years experience, expect offers around $250k-$274k range
- LOW end is irrelevant - that's for junior people at this title

**DO NOT flag salary floor as a risk when:**
- The high end meets requirements
- User has 15+ years experience
- The spread is wide (indicates room for experience-based negotiation)

**Strategic Fit:**

-   How this role advances user's career goals
-   Risk vs. reward assessment
-   Comparison to already applied positions

### Step 4: Recommendation

Provide clear recommendation:

-   🟢 **PROCEED** - Strong match, stable company, good opportunity
-   🟡 **CONDITIONAL** - Good match with noted concerns to consider
-   🔴 **SKIP** - Poor match, unstable company, or better options available

Include specific reasoning for the recommendation.

## Research Quality Guidelines

-   Always verify company information from multiple sources
-   Look for recent news about layoffs, funding, or leadership changes
-   Check employee reviews from the last 6-12 months specifically
-   Note any industry-specific challenges affecting the company

## Decision Support Guidelines

-   Be honest about potential risks (layoffs, financial issues, culture problems)
-   Compare to already applied positions when relevant
-   Consider user's stated preferences (stability, tech stack, remote work)
-   Factor in the user's current employment situation

## Output Format

**REQUIRED: Use this exact format for research presentation:**

```
## 📊 Company Research: [Company Name]

---
**Company Overview:**
- **Employee Rating:** [X.X]/5 stars
- **Management Health:** [Well-Managed/Concerns/Severely Mismanaged]
- **Company Size:** [Employee count]
- **Funding:** [Stage/Status]

---
**Recent Activity:**
- **Layoffs:** [Details or "None detected"]
- **Financial Health:** [Assessment]
- **Recent News:** [Key updates]

---
**Culture & Work Environment:**
- **Work-Life Balance:** [Assessment]
- **Remote Policy:** [Details]
- **Management Issues:** [Specific problems if any]

---
**Tech Stack Match:**
- **Primary Technologies:** [List]
- **Match Percentage:** [X]%
- **Missing Skills:** [List if any]

---
**Risk Assessment:**
- 🟢/🟡/🔴 [Specific risks or positive indicators]

---
```

**CRITICAL: Always use horizontal separators (---) between sections and bullet points with proper spacing.**

## Success Criteria

A successful research execution should provide:

1. **Comprehensive company assessment** with verified information
2. **Clear risk evaluation** with specific evidence
3. **Actionable recommendation** with reasoning
4. **Management health rating** with supporting details

The user should have all information needed to make an informed application decision.
