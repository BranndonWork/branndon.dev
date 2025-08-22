# Resume Customization Workflow

## Philosophy

**CRITICAL RULE: Never fabricate skills, experience, or achievements.** Only reorganize, emphasize, and reorder existing content from the original resume. The goal is to highlight relevant experience, not create false credentials.

## Directory Structure

All job applications go in `./job-search/[Company-JobTitle]/` format:
- `./job-search/Google-Senior-Django-Developer/`
- `./job-search/Netflix-Backend-Engineer/`
- `./job-search/Stripe-Python-Developer/`

This naming convention:
- ✅ Makes sense to developers and hiring managers
- ✅ Shows organizational skills and attention to detail  
- ✅ Clearly separates from actual applications/projects
- ✅ Professional and searchable

## Step-by-Step Process

### 1. Create Application Directory
```bash
mkdir "./job-search/[Company-JobTitle]"
cd "./job-search/[Company-JobTitle]"
```

### 2. Copy Original Resume
```bash
cp "../../webroot/branndon-coelho-resume.json" "./resume-branndon-coelho-[company].json"
```
**Why copy?** Preserves original structure and saves tokens. Faster for LLM processing.

### 3. Analyze Job Posting
Create `job-posting.md` with:
- Required skills (must-have vs nice-to-have)
- Years of experience needed
- Technology stack mentioned
- Key responsibilities
- Company culture keywords
- Compensation/benefits if listed

### 4. Read Entire Resume File
**Critical:** Use Read tool to understand full context before making changes. This ensures:
- No fabrication of skills/experience
- Proper understanding of existing achievements
- Accurate skill level representation
- Maintains consistency across sections

### 5. Customize Using MultiEdit
Use MultiEdit tool for efficiency. Make all changes in one operation:

#### Title Modifications
- Only adjust titles that are truthful variations
- Example: "Senior Software Engineer" → "Senior Django Developer" (if Django is primary skill)
- Never: "Junior Developer" → "Senior Developer"

#### Summary Section
- Emphasize relevant experience from original
- Use their terminology when it matches your actual experience
- Lead with most relevant achievement
- Never add skills not in original resume
- **CRITICAL**: Maintain accurate role scope - use "specialize in", "lead", "guide", "develop" not "architect" unless you're actually the system architect
- Your senior-level contributions are impressive without inflating scope

#### Experience Reordering
- Move most relevant positions to top
- Emphasize relevant projects/achievements
- Use exact metrics from original (never inflate)
- Highlight technologies that match requirements

#### Skills Section
- Reorder to match job requirements
- Only use skill levels from original resume
- Group related technologies together
- Remove less relevant skills to save space (but don't remove core competencies)

#### Technologies List
- Prioritize those mentioned in job posting
- Only include technologies actually used in listed projects
- Match their exact terminology when possible

### 6. Create Cover Letter
Use template in `cover-letter.txt`:
- Hook with most relevant achievement
- Address their specific pain points
- Show knowledge of company/role
- Include metrics from actual experience
- Professional but personality-appropriate close

### 7. Track Application
Create separate tracking files:
- `customization-analysis.md`: Job requirements analysis, customizations made, cover letter strategy, ATS optimization
- `application-tracking.md`: Submission details, follow-up schedule, communication log, status updates
- `interview-prep.md`: Technical preparation, company research, questions to ask, salary discussion prep

## Quality Assurance Checklist

### Before Customization
- [ ] Read entire original resume for context
- [ ] Identify all actual skills and experience levels
- [ ] Note all quantified achievements and metrics
- [ ] Understand current project details

### During Customization
- [ ] Every change references existing content
- [ ] No new skills added that aren't in original
- [ ] Skill levels match or are lower than original
- [ ] All metrics are accurate to original
- [ ] Company/role-specific terminology used appropriately

### After Customization
- [ ] Compare side-by-side with original for accuracy
- [ ] Verify no false claims were introduced
- [ ] Check that all required keywords are naturally incorporated
- [ ] Ensure formatting remains ATS-friendly
- [ ] Spell check and grammar review

## Example: Good vs Bad Customizations

### ✅ GOOD - Emphasizing Existing Skills
**Original:** "Django" in technologies list
**Customized:** Move Django to top of backend skills, change title to "Senior Django Developer"

### ❌ BAD - Fabricating Experience  
**Original:** No mention of "e-commerce"
**Customized:** Adding "e-commerce platform development" to summary

### ✅ GOOD - Accurate Role Language
**Original:** "specializing in Django-based application development"
**Customized:** "specialize in Django backend development serving millions of users"

### ❌ BAD - Inflating Role Scope
**Original:** "guiding software architecture decisions"
**Customized:** "architect Django backend systems" (implies you're THE architect)

### ✅ GOOD - Reordering for Relevance
**Original:** Multiple projects listed
**Customized:** Lead with Server-Driven UI project for mobile development role

### ❌ BAD - Inflating Skill Levels
**Original:** "React.js - Some Experience - 85%"
**Customized:** "React.js - Expert - 95%"

## Tools and Efficiency

1. **Read** - Always read entire resume first for context
2. **MultiEdit** - Make all changes at once for consistency and speed
3. **Copy original** - Preserves structure, saves tokens, faster processing
4. **Track changes** - Document what was modified and why

## Success Metrics

A well-customized resume should:
- Pass ATS keyword matching (75%+ match rate)
- Remain 100% truthful to original experience
- Show clear relevance to specific role
- Demonstrate understanding of company needs
- Maintain professional formatting and readability

Remember: The goal is to present your actual experience in the most relevant light, not to become someone you're not.