# Communications Expert — branndon.dev Job Search Project

## The Golden Rule
NEVER fabricate skills, experience, or achievements. Every claim must be traceable to `webroot/branndon-coelho-resume.json`. Reorganize and emphasize — never invent.

## Master Resume
**Source of truth**: `webroot/branndon-coelho-resume.json`
All resume customizations read this file first. Technologies, achievements, and role descriptions must come from it verbatim or be a minor reorder/reemphasis.

## Key Templates
- ATS resume template: `docs/templates/resume-ats-template.json`
- Cover letter template: `docs/templates/cover-letter-template.txt`
- Job tracking template: `docs/templates/job-tracking-template.yaml`

## Resume Generation Workflow
Full workflow in `docs/RESUME_GENERATION_COMPLETE.md` (self-contained, do not reference other docs when using it).

Output: JSON file saved to `job-search/[Company-JobTitle]/resume-branndon-coelho-[slug]-ats.json`

## Candidate Voice & Tone
- Clear, technical, precise — no buzzwords
- First-person implied (no "I" in resume bullets)
- Achievement-focused: metrics where they exist (2.7s → 0.89s, scale numbers, team sizes)
- Conservative scope language: "developed", "led", "built", "optimized" — not "architected" unless actually architecting

## Gap Handling
When a JD requires a technology NOT in the master resume:
1. Stop and ask: "This skill is missing from your master resume — do you have experience with it?"
2. If yes → update master resume first, then customize
3. If no → note the gap, do NOT add to resume

## Email Templates in Use
- Application follow-up: brief, professional, under 100 words
- Thank-you post-interview: specific to what was discussed, under 150 words
- Salary negotiation: always anchor with a specific number, not a range
- Rejection acknowledgment: brief, gracious, leave door open

## Decisions Already Made
- No buzzwords: "passionate", "rockstar", "ninja", "synergy", "fast-paced"
- Cover letters: 3 paragraphs, under 300 words, add context not present in the resume
- Negotiation emails: give a number, not a range — anchor high
- All resume JSON output must validate against the ATS template structure
