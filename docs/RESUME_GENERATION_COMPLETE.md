# Resume Generation Complete Workflow

**⚠️ STOP: This document is SELF-CONTAINED. Do not reference other docs. Everything needed is here.**

## Pre-Flight Checklist
Before proceeding, confirm you understand:
- [ ] Template location: `docs/resume-ats-template.json`
- [ ] Skills source: Only from webroot/branndon-coelho-resume.json
- [ ] #1 Rule: NEVER fabricate skills or experience
- [ ] Workflow: Read ALL sections before starting

## Critical Rules (Memorize These First)

### The Golden Rule
**NEVER FABRICATE SKILLS, EXPERIENCE, OR ACHIEVEMENTS**
- Only reorganize and emphasize existing content
- If a job requirement doesn't match the resume JSON, ignore it
- When in doubt, leave it out

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
- **15+ years experience** (evidenced in "About" section)
- **Current Role**: Senior Software Engineer at Headspace (2022-Present)
- **Previous Roles**: Application Architect/Lead/Senior Developer at The Penny Hoarder, Senior Software Engineer at Webley Systems
- **Specializations**: Backend Development, Python, Django, Scalable Systems
- **Major Achievements**: Performance optimization (2.7s → 0.89s), ML email system, GDPR compliance, platform scaling

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

### Step 2: Copy Template (NOT another resume)
```bash
# CRITICAL: Copy from template, not from another job's resume
cp docs/resume-ats-template.json ./job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json
```

### Step 3: Create Missing Files
Copy these from example directory:
- `application-tracking.md`
- `interview-prep.md`

Create new based on job:
- `cover-letter.txt`
- `customization-analysis.md`

### Step 4: Analyze Job Requirements
Read job-posting.md and identify:
- Required skills that match webroot/branndon-coelho-resume.json
- Years of experience needed
- Technology stack mentioned
- Keywords to emphasize

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
- Bold key job keywords using `<strong>` tags
- Target: job title, primary technologies, key requirements
- Natural integration only - no keyword stuffing
- Maximum 8-10 bolded phrases per section

### Step 6: Generate PDF
```bash
# Copy to webroot
cp job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json webroot/branndon-coelho-resume-ats.json

# Check if server is running
if curl -s http://localhost:8000 | grep -q "resume-wrapper"; then
    SERVER_URL="http://localhost:8000"
else
    # Start server on port 8001
    cd webroot && python3 -m http.server 8001 &
    sleep 2
    SERVER_URL="http://localhost:8001"
fi

# Generate PDF
poetry run python scripts/generate_resume_pdf.py --mode ats --output job-search/[Company-JobTitle]/resume.pdf --url $SERVER_URL

# CRITICAL: Delete ATS file immediately
rm webroot/branndon-coelho-resume-ats.json
```

### Step 7: Verify Output
- Confirm PDF was generated
- Provide file:// links to resume.pdf and cover-letter.txt
- List final directory contents

## Section Limits (2-3 Page Target)

### Professional Summary
- **Limit**: 2-3 sentences maximum
- **Focus**: Most relevant experience + key technologies

### About Section  
- **Descriptions**: Maximum 3 paragraphs, 2-3 sentences each
- **Paragraph 1**: Most relevant experience
- **Paragraph 2**: Current role and matching technologies
- **Paragraph 3**: Business impact and scaling

### Experience Section
- **Positions**: Maximum 3 (current + 2 most relevant)
- **Descriptions**: Maximum 3 bullet points per position
- **Achievements**: Maximum 3 bullet points per position
- **Technologies**: 10 for current, 8 for previous roles

### Sections to Remove
- **Fun Facts Section**: Remove entirely for ATS
- **Recommendations Section**: Keep (shows credibility)

## Quality Assurance Checklist

### Before Starting
- [ ] Read this ENTIRE document first
- [ ] Located template at `docs/resume-ats-template.json`
- [ ] Identified job requirements from job-posting.md
- [ ] Mapped requirements to skills in webroot/branndon-coelho-resume.json

### During Customization
- [ ] Every skill exists in webroot/branndon-coelho-resume.json
- [ ] Using exact language from resume JSON
- [ ] Not forcing unmatched job keywords
- [ ] Preserving career progression titles
- [ ] Keeping descriptions truthful

### After Generation
- [ ] PDF generated successfully
- [ ] Total length 2-3 pages
- [ ] All content truthful to original experience
- [ ] Provided file:// verification links

## Common Mistakes to Avoid

1. **Copying another job's resume instead of template**
2. **Adding skills not in resume JSON**
3. **Inflating role scope** (architect vs developer)
4. **Creating technical nonsense** phrases
5. **Forgetting to delete ATS file from webroot**
6. **Not reading job-posting.md first**
7. **Skipping this document and referencing others**

---
*This document contains EVERYTHING needed for resume generation. Do not reference other docs.*