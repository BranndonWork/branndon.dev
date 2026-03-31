# OE Research Notes — March 2026

Permanent record of community-sourced research findings used to rebuild the OE scoring matrix and knowledgebase. All data points sourced from r/overemployed (430k+ members), overemployed.com, and related community resources.

---

## Community Statistics

- **430,000+** members in r/overemployed subreddit as of early 2026
- **37%** of US workers admitted to holding multiple full-time jobs in some form (survey-based, not all remote/tech)
- **63%** of people who get caught doing OE report it was due to their own behavior, not discovery from external systems
- **>50%** of those caught are fired from at least one job
- Most successful OE practitioners are SSEs and senior ICs — knowledge work with outcome-based evaluation
- Median additional income from J2: $80K–$180K/year range for SSE-level roles
- Some community members report 3–4 concurrent W2 jobs at $120K–$200K each ($400K–$600K+ total TC)

---

## TC/HPW Ratio — The Core OE Metric

**Total Compensation ÷ Hours Per Week (actual, not nominal)**

The community has shifted from evaluating "is this a good job" to "what is the TC/HPW ratio."

- A $150K job requiring 35 hrs/week = $4,285/HPW/year
- A $130K job requiring 15 hrs/week = $8,666/HPW/year — significantly better for OE
- Target ratio for J2/J3: maximize TC, minimize actual hours committed

The insight: a slightly lower-paying job with dramatically lower actual time commitment is worth far more in an OE context.

---

## J1/J2/J3 Priority System

The community convention for managing multiple jobs:

**J1 (Primary Job)**
- Highest total compensation or most career-strategic
- Always takes precedence in scheduling conflicts
- Protected at all costs — never sacrifice J1 meetings for J2/J3
- Treat as your "real" job publicly if pressed

**J2 (Secondary Job)**
- Second priority, ideally fully async or low-meeting-load
- Should have minimal overlap with J1's core hours
- Good J2: async-first, outcomes-based, distributed team

**J3+ (Additional)**
- Highest risk, lowest priority
- Only viable if J1 and J2 have extremely low actual time requirements
- Community consensus: most people can sustain 2 jobs without degraded performance; 3+ is high-risk

**Conflict Resolution Rule**: J1 wins all conflicts. If J2 has a conflict with J1, take a tentative or decline J2's request. Never the reverse.

---

## How People Get Caught — Ranked by Frequency

From community surveys and post-mortems:

1. **Poor performance** — The #1 cause. Slipping quality, missed deadlines, being "checked out" in meetings. Managers notice degraded output before they suspect OE.
2. **LinkedIn activity** — Updating LinkedIn with new job, connection requests, new endorsements. Employers and colleagues cross-reference. Even being searchable is a risk.
3. **Shared professional connections** — LinkedIn mutual connections, industry conferences, recruiters who work with both companies.
4. **The Work Number (TWN)** — Equifax's employment verification database. Contains all W2 employment history. Background check vendors query this automatically. If an employer or future employer runs a background check, all concurrent W2 jobs appear.
5. **Mouse jigglers / automation tools** — IT and security teams detect software-based activity simulation. Tools like Teramind, DLP systems flag this behavior.
6. **Talking about it** — Telling friends, family outside household, colleagues. Information spreads.
7. **IP address conflicts** — VPN/proxy mistakes or same-network usage creating logs showing activity from incompatible locations simultaneously.
8. **Tax document discrepancies** — W2 forms showing multiple employers; state tax withholding flags for some HR departments processing paperwork.
9. **Calendar mistakes** — Accidentally accepting/declining wrong-company meetings, wrong email account in calendar invites.
10. **Social media** — Mentioning employer names, team names, or project names that cross-reference to multiple companies.

---

## Operational OPSEC

Community consensus on standard operating procedure:

**Devices**
- Separate physical devices per job (laptop or desktop per J1/J2)
- KVM switch strongly recommended — one keyboard/mouse/monitor, multiple computers
- Never access J2 resources from J1 device
- Separate browsers or browser profiles for each job's SSO/email

**LinkedIn**
- Hibernate or deactivate LinkedIn entirely — do not leave an active profile
- If LinkedIn must remain: set to private, disable "Open to Work", remove connection notifications
- Do not update job titles or employers on LinkedIn
- Never accept connection requests from colleagues across jobs on the same profile

**The Work Number (TWN)**
- Freeze employment data at Equifax's The Work Number: employers/verifiers cannot see your records
- This is the single most important protective action for W2 concurrent employment
- Freeze URL: theworknumber.com → manage your employment records → freeze

**Communication Hygiene**
- Separate phone numbers per job (Google Voice or second SIM)
- Separate email addresses per job (company email is mandatory; no crossover)
- Calendar silos — never add J2 events to J1 calendar or vice versa

**Financial**
- Consult a tax professional — multiple W2s require estimated quarterly tax payments to avoid underpayment penalties
- Multiple W2s are fully legal; the IRS has no mechanism to flag OE as fraud

---

## Calendar Management Strategies

**Segmentation approach** (most common):
- Block J1 core meeting times (e.g., mornings)
- Use J2 for async work in the off-hours or schedule J2 meetings in J1 "deep work" blocks
- Mark J1 blocks as "busy" in both calendars to prevent double-booking

**Tentative decline technique**:
- Accept as tentative on J2 calendar when J1 has potential overlap
- Let J2 meeting organizers know you "may have a conflict" rather than hard-declining
- Watch for recurring meetings that shift

**Time zone arbitrage**:
- J1 in ET, J2 in PT — meetings rarely overlap fully
- Async J2 jobs that don't require fixed hours are ideal complements

**Focus block protection**:
- Schedule "focus time" or "no meeting" blocks in both calendars to create buffer zones
- This reduces the chance of back-to-back meetings across companies

---

## OE-Friendly Job Categories (Ranked by Stackability for SSEs)

From community experience and stackability reports:

1. **Data Engineering / Analytics Engineering** — High async, outcome-based, tickets-first workflow. Minimal real-time dependency. Strong J2 candidate.
2. **QA / Test Automation Engineering** — Often low visibility, clear outputs (test suites, coverage metrics), async by default.
3. **Cloud / Infrastructure / DevOps (non-SRE)** — Project-based work, Terraform/CDK deployments measurable. Avoid SRE if it includes on-call.
4. **Backend SWE — Maintenance/Feature** — At large cos, maintenance tickets are discrete and outcome-based. Startup BE roles are poor (full ownership expected).
5. **Platform / Developer Experience Engineering** — Outcomes visible (DX metrics, adoption rates), moderate meeting load at large companies.
6. **ML Engineering (deployment, not research)** — Model serving, pipelines. Less sync than research roles.

**Worst stackability:**
- SRE with on-call rotation
- Mobile engineering (frequent release coordination)
- Frontend at design-driven companies (constant design sync)
- Any founding-team or "first engineer" role
- Customer-facing engineering / solutions engineering

---

## Job Description Red-Flag Phrases (OE-Hostile Culture Signals)

Verbatim phrases found in JDs that correlate with OE-hostile environments:

| Phrase | What It Signals |
|---|---|
| "Fast-paced environment" | High cognitive load, constant context switching, reactive culture |
| "Wear multiple hats" | Scope creep, no boundaries, you are load-bearing |
| "Hands-on" | They want a doer, not a delegator — means high hours |
| "Work hard, play hard" | Long hours normalized and celebrated |
| "Team player who goes above and beyond" | Above-and-beyond is baseline expectation |
| "Collaborative culture" | Often means excessive sync, pair programming, constant availability |
| "Flat organization" | Everyone visible to everyone, no org chart silos |
| "Startup mentality" | You will wear hats, move fast, and be noticed |
| "High-growth trajectory" | Rapid pace, scope changes, high visibility on output |
| "Tight-knit team" | Everyone knows what you're doing |
| "Looking for a culture fit" | Small team, personality-driven hiring, you will be known |
| "Urgency and ownership" | They expect you to treat this as your primary priority |
| "Bias for action" | High pace, low deliberation, reactive |

---

## Green-Flag JD Phrases (OE-Friendly Signals)

| Phrase | What It Signals |
|---|---|
| "Async-first" | Explicit remote-friendly communication norm |
| "We measure by outcomes" / "results-oriented" | Output-based evaluation |
| "Flexible hours" / "work when you're productive" | No strict presence enforcement |
| "Globally distributed team" | Meetings are limited by timezone overlap, async is default |
| "Documentation-first culture" | Knowledge stored, not in people's heads requiring sync |
| "Strong work-life balance" with specific examples | Not just marketing copy |
| "Independent and self-directed" in requirements | They explicitly want someone who doesn't need hand-holding |

---

## Interview Questions to Probe OE-Friendliness (Without Revealing Intent)

Use these to surface culture signals naturally:

**Meeting load:**
- "Can you walk me through a typical sprint for the team? How much time is usually in meetings vs. heads-down work?"
- "How does the team handle standup — is it synchronous or do you use written/async formats?"
- "What does a 'deep work' day look like for engineers here?"

**Measurement model:**
- "How does the team define success for someone in this role in the first 6 months?"
- "Is the team more focused on shipped features or sprint velocity?"
- "How does your manager typically check in with engineers on progress?"

**On-call:**
- "Is there an on-call rotation for this team? How is it structured?"
- "How does the team handle production incidents? What's the escalation path?"

**Schedule flexibility:**
- "Are there core hours the team is expected to be online, or is it more flexible?"
- "Does the team do any pair programming or is most work done independently?"

**Team visibility:**
- "How large is the engineering team overall? How many people are on this specific team?"
- "How long has the current team been together? Is the product in a growth phase or more stability/maintenance?"

---

## Source References

- r/overemployed subreddit: community posts, AMAs, and mod-pinned guides
- overemployed.com: blog posts on OPSEC, TWN freezing, calendar management
- The Work Number (TWN): theworknumber.com — Equifax employment verification database
- BLS data and survey studies on multiple job holding (2023–2025)
- Community spreadsheets tracking stackable job categories (shared periodically in r/overemployed)
- IRS Publication 505: Tax Withholding and Estimated Tax (multiple W2 guidance)
