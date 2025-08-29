# Resume Generation Complete Workflow

**⚠️ STOP: This document is SELF-CONTAINED. Do not reference other docs. Everything needed is here.**

## Pre-Flight Checklist

Before proceeding, confirm you understand:

-   [ ] Template location: `docs/templates/resume-ats-template.json`
-   [ ] Skills source: Only from webroot/branndon-coelho-resume.json
-   [ ] #1 Rule: NEVER fabricate skills or experience
-   [ ] Workflow: Read ALL sections before starting

## Critical Rules (Memorize These First)

### The Golden Rule

**NEVER FABRICATE SKILLS, EXPERIENCE, OR ACHIEVEMENTS**

-   Only reorganize and emphasize existing content
-   If a job requirement doesn't match the resume JSON, ignore it
-   When in doubt, leave it out

### LLM-Specific Rules

1. **Use ONLY language from webroot/branndon-coelho-resume.json** - Don't paraphrase or create new terms
2. **Don't force job keywords** - Only use them if they naturally match existing experience
3. **Respect role scope** - Use "lead", "specialize", "develop" not "architect" unless actually an architect
4. **No buzzword inflation** - Keep technical descriptions clear and accurate
5. **Verify everything** - For every skill added, it must exist in webroot/branndon-coelho-resume.json

## Source of Truth: Resume JSON

**ALL skills, experience, and achievements must come from `webroot/branndon-coelho-resume.json`**

### How to Use the Resume JSON:

1. **Technologies**: Extract from `technologies` arrays in each job experience
2. **Skills**: All capabilities must be evidenced in job descriptions and achievements
3. **Experience**: Use `description` and `achievements` arrays for content
4. **Time periods**: Use exact dates from `time` fields
5. **Company details**: Use exact `companyName` and `position` titles

### Key Information Available:

-   **15+ years experience** (evidenced in "About" section)
-   **Current Role**: Senior Software Engineer at Headspace (2022-Present)
-   **Previous Roles**: Application Architect/Lead/Senior Developer at The Penny Hoarder, Senior Software Engineer at Webley Systems
-   **Specializations**: Backend Development, Python, Django, Scalable Systems
-   **Major Achievements**: Performance optimization (2.7s → 0.89s), ML email system, GDPR compliance, platform scaling

### Critical Instruction:

Before starting any resume customization, **READ the entire webroot/branndon-coelho-resume.json file** to understand available content. Only use technologies, skills, and achievements that exist in that file.

## Step-by-Step Workflow

### Step 1: Validate Prerequisites

```bash
# Check job directory exists
ls ./job-search/[Company-JobTitle]/

# Verify job-posting.md exists
cat ./job-search/[Company-JobTitle]/job-posting.md
```

### Step 2: Create Missing Files

Copy ALL templates from templates directory:

```bash
cp docs/templates/resume-ats-template.json ./job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json
cp docs/templates/customization-analysis-template.md ./job-search/[Company-JobTitle]/customization-analysis.md
cp docs/templates/application-tracking-template.md ./job-search/[Company-JobTitle]/application-tracking.md
cp docs/templates/interview-prep-template.md ./job-search/[Company-JobTitle]/interview-prep.md
cp docs/templates/cover-letter-template.txt ./job-search/[Company-JobTitle]/cover-letter.txt
```

### Step 4: Complete Customization Analysis FIRST

**🚨 CRITICAL: Fill out customization-analysis.md BEFORE touching resume or cover letter**

This pre-research document will:

-   Analyze job requirements vs your actual experience
-   Plan your customization strategy
-   Identify gaps honestly
-   Create cover letter outline
-   Prevent fabrication by planning ahead

```bash
# Edit the customization analysis first
nano ./job-search/[Company-JobTitle]/customization-analysis.md
```

### Step 5: Customize Resume Using MultiEdit

#### What to Customize:

1. **Positions array**: Fill in relevant role titles
2. **Summary**: 2-3 sentences with bolded keywords from job
3. **About descriptions**: 3 paragraphs emphasizing relevant experience
4. **Experience sections**:
    - Keep original position titles (preserve career progression)
    - Customize descriptions to emphasize relevant work
    - Reorder technologies to match job requirements
    - Maximum 3 positions total

#### ATS Keyword Optimization:

-   Bold key job keywords using `<strong>` tags
-   Target: job title, primary technologies, key requirements
-   Natural integration only - no keyword stuffing
-   Maximum 8-10 bolded phrases per section

### Step 6: MANDATORY VERIFICATION GATEKEEPER

**🚨 CRITICAL: PDF generation is BLOCKED until verification passes**

```bash
# Read source of truth for fresh context
cat webroot/branndon-coelho-resume.json

# Read customized resume JSON
cat job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json

# Read cover letter
cat job-search/[Company-JobTitle]/cover-letter.txt
```

**VERIFICATION CHECKLIST - ALL must pass:**

-   [ ] Every skill/technology in custom resume exists in source JSON
-   [ ] Every achievement in custom resume exists in source JSON
-   [ ] Every job description phrase exists in source JSON or is simple reorganization
-   [ ] No fabricated capabilities (AI/ML, LLM, agentic systems unless explicitly in source)
-   [ ] No fabricated experience or inflated role scope
-   [ ] Cover letter contains no fabricated claims

**IF ANY FABRICATIONS FOUND:** Fix them first, do NOT proceed to PDF generation

### Step 7: Generate PDF (Only After Verification Passes)

```bash
# Copy to webroot
cp job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json webroot/branndon-coelho-resume-ats.json

# Ensure server is running using management script
./scripts/server.sh ensure
SERVER_URL="http://localhost:8000"

# Generate PDF with job directory name in filename
poetry run python scripts/generate_resume_pdf.py --mode ats --output job-search/[Company-JobTitle]/[Company-JobTitle]-Resume.pdf --job-dir [Company-JobTitle] --url $SERVER_URL

# CRITICAL: Delete ATS file immediately
rm webroot/branndon-coelho-resume-ats.json

# Generate cover letter PDF with matching filename format
cd scripts && poetry run python text_to_pdf.py "../job-search/[Company-JobTitle]/cover-letter.txt" "../job-search/[Company-JobTitle]/[Company-JobTitle]-CoverLetter.pdf"
```

### Step 8: Verify Output

-   Confirm resume PDF was generated
-   Confirm cover letter PDF was generated with matching filename format
-   Provide file:// links to [Company-JobTitle]-Resume.pdf and [Company-JobTitle]-CoverLetter.pdf
-   List final directory contents

## Section Limits (2-3 Page Target)

### Professional Summary

-   **Limit**: 2-3 sentences maximum
-   **Focus**: Most relevant experience + key technologies

### About Section

-   **Descriptions**: Maximum 3 paragraphs, 2-3 sentences each
-   **Paragraph 1**: Most relevant experience
-   **Paragraph 2**: Current role and matching technologies
-   **Paragraph 3**: Business impact and scaling

### Experience Section

-   **Positions**: Maximum 3 (current + 2 most relevant)
-   **Descriptions**: Maximum 3 bullet points per position
-   **Achievements**: Maximum 3 bullet points per position
-   **Technologies**: 10 for current, 8 for previous roles

### Sections to Remove

-   **Fun Facts Section**: Remove entirely for ATS
-   **Recommendations Section**: Keep (shows credibility)

## Quality Assurance Checklist

### Before Starting

-   [ ] Read this ENTIRE document first
-   [ ] Located template at `docs/templates/resume-ats-template.json`
-   [ ] Identified job requirements from job-posting.md
-   [ ] Mapped requirements to skills in webroot/branndon-coelho-resume.json

### During Customization

-   [ ] Every skill exists in webroot/branndon-coelho-resume.json
-   [ ] Using exact language from resume JSON
-   [ ] Not forcing unmatched job keywords
-   [ ] Preserving career progression titles
-   [ ] Keeping descriptions truthful

### After Generation

-   [ ] PDF generated successfully
-   [ ] Total length 2-3 pages
-   [ ] All content truthful to original experience
-   [ ] Provided file:// verification links

## Common Mistakes to Avoid

1. **Copying another job's resume instead of template**
2. **Adding skills not in resume JSON**
3. **Inflating role scope** (architect vs developer)
4. **Creating technical nonsense** phrases
5. **Forgetting to delete ATS file from webroot**
6. **Not reading job-posting.md first**
7. **Skipping this document and referencing others**

---

_This document contains EVERYTHING needed for resume generation. Do not reference other docs._
