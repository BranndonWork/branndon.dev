# Resume Generation Complete Workflow

**⚠️ STOP: This document is SELF-CONTAINED. Do not reference other docs. Everything needed is here.**

## Pre-Flight Checklist

Before proceeding, confirm you understand:

- [ ] Template locations: `docs/templates/resume-ats-template.json` and `docs/templates/job-tracking-template.yaml`
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

### Gap Identification and Master Resume Update

**CRITICAL**: When job requirements include technologies NOT found in webroot/branndon-coelho-resume.json:

1. **Stop customization process**
2. **Ask user**: "I found these required technologies missing from your master resume: [list]. Do you have experience with these? If yes, I need to update your master resume first."
3. **If user confirms experience**: Update webroot/branndon-coelho-resume.json with the new technologies in appropriate experience sections
4. **If user denies experience**: Note gaps in cover letter strategy, do NOT add to resume
5. **Resume customization only after master resume is updated**

This prevents fabrication and ensures the source of truth (master resume) is complete before generating job-specific versions.

## Step-by-Step Workflow

### Step 1: Validate Prerequisites & Company Review

```bash
# Check job directory exists
ls ./job-search/[Company-JobTitle]/

# Verify job-posting.md exists
cat ./job-search/[Company-JobTitle]/job-posting.md
```

**🚨 MANDATORY COMPANY REVIEW STEP:**

**If you already conducted comprehensive company research earlier in the current conversation, save the complete analysis to `./job-search/[Company-JobTitle]/company-research-analysis.md` and proceed to Step 4: Complete Job Tracking YAML.**

Before proceeding with resume generation, research company employee reviews:

1. **Web Search for Review Sites:**

   ```bash
   # Search for employee reviews (avoid Glassdoor - blocked by Cloudflare)
   WebSearch: "[Company Name] employee reviews indeed glassdoor"
   ```

2. **Scrape Available Review Sites:**

   ```bash
   # Use playwright scraper on Indeed or other accessible review sites from search results
   poetry run python scripts/playwright_scraper.py "[review-site-url]" --no-links --output company-reviews.txt
   ```

3. **Analyze and Present Summary:**
   Present comprehensive review summary including:
   - Overall rating and detailed ratings (work-life balance, pay/benefits, job security, management, culture)
   - Major red flags and concerns for the specific role level
   - Positive aspects
   - Bottom line assessment

4. **Decision Point:**
   **Always ask user**: "Based on these reviews, do you want to continue with resume generation or should I delete this job directory?"

**RED FLAGS TO HIGHLIGHT:**

- Job security rating < 3.0/5 ⚠️
- Management rating < 3.0/5 ⚠️
- Multiple mentions of: layoffs, micromanagement, high turnover, toxic culture, favoritism
- Recent reviews (last 6 months) showing declining conditions
- Ethical concerns or unethical business practices

### Step 2: Create Job Directory Structure (Only if user chooses to continue)

Use the setup script to create standardized directory structure with all templates:

```bash
# Create complete job directory with all templates and structure
poetry run python scripts/setup_job_directory.py "[Company Name]" "[Job Title]"

# Example:
# poetry run python scripts/setup_job_directory.py "PatientPoint" "Staff Python Engineer"
```

This creates:

- Complete directory structure with `interviews/` and `correspondence/` subdirectories
- All template files (job-tracking.yaml, resume templates, prep files)
- Proper naming conventions and structure
- Skips existing files to avoid overwriting customizations

### Step 4: Complete Job Tracking YAML FIRST

**🚨 CRITICAL: Fill out job-tracking.yaml BEFORE touching resume or cover letter**

**Primary workflow - comprehensive job analysis:**

```bash
# Edit the main job tracking file first - contains ALL job details
nano ./job-search/[Company-JobTitle]/job-tracking.yaml
```

This comprehensive YAML file will:

- Store complete job details, tech stack, company research
- Track application timeline and follow-up schedule
- Document your match analysis and learning opportunities
- Plan interview prep and decision factors

**Secondary workflow - quick resume customization strategy:**

```bash
# Edit the simplified customization analysis (references job-tracking.yaml)
nano ./job-search/[Company-JobTitle]/customization-analysis.md
```

This simplified file focuses only on resume keyword strategy since detailed analysis is in the YAML.

### Step 5: Customize Resume Using MultiEdit

#### What to Customize:

1. **Positions array**:
   - **CRITICAL PROCESS**: First identify which 3 positions will be included in experience section
   - Extract the EXACT position titles from those 3 chosen positions
   - Update header "positions" array to match those exact titles (no fabrication, no modification)
   - Order them from most relevant to job at top, working down
   - Remove any duplicates (e.g., multiple "Senior Software Engineer" titles)
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

### Step 6: MANDATORY VERIFICATION GATEKEEPER

**🚨 CRITICAL: PDF generation is BLOCKED until verification passes**

**Use the resume-audit-validator agent for automated verification:**

```bash
# Use Task tool with resume-audit-validator agent
Task(subagent_type="resume-audit-validator", description="Verify resume claims",
     prompt="Please audit and validate the [Company] resume generation to ensure all claims are truthful and accurate.

Key files to audit:
- Generated resume: job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json
- Source resume: webroot/branndon-coelho-resume.json
- Job analysis: job-search/[Company-JobTitle]/job-tracking.yaml
- Customization strategy: job-search/[Company-JobTitle]/customization-analysis.md

Please verify all requirements and return detailed audit report.")
```

**MANUAL VERIFICATION BACKUP (if agent unavailable):**

```bash
# Read source of truth for fresh context
cat webroot/branndon-coelho-resume.json

# Read job tracking YAML
cat job-search/[Company-JobTitle]/job-tracking.yaml

# Read customized resume JSON
cat job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json

# Read cover letter
cat job-search/[Company-JobTitle]/cover-letter.txt
```

**VERIFICATION CHECKLIST - ALL must pass:**

- [ ] Every skill/technology in custom resume exists in source JSON
- [ ] Every achievement in custom resume exists in source JSON
- [ ] Every job description phrase exists in source JSON or is simple reorganization
- [ ] No fabricated capabilities (AI/ML, LLM, agentic systems unless explicitly in source)
- [ ] No fabricated experience or inflated role scope
- [ ] Cover letter contains no fabricated claims

**IF ANY FABRICATIONS FOUND:** Fix them first, do NOT proceed to PDF generation

### Step 7: Generate PDF (Only After Verification Passes)

```bash
# Copy to webroot
cp job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json webroot/branndon-coelho-resume-ats.json

# Ensure server is running using management script
./scripts/server.sh ensure

# Generate PDF with job directory name in filename
# Note: --url parameter defaults to http://localhost:8000, only include if using different server
poetry run python scripts/generate_resume_pdf.py --mode ats --output job-search/[Company-JobTitle]/[Company-JobTitle]-Resume.pdf --job-dir [Company-JobTitle]

# CRITICAL: Delete ATS file immediately
rm webroot/branndon-coelho-resume-ats.json

# Generate cover letter PDF with matching filename format
cd scripts && poetry run python text_to_pdf.py "../job-search/[Company-JobTitle]/cover-letter.txt" "../job-search/[Company-JobTitle]/[Company-JobTitle]-CoverLetter.pdf"
```

### Step 8: Verify Output & Generate LinkedIn URL

**First, extract Job ID from job-posting.md if available:**

```bash
# Look for Job ID in the job posting file
grep -i "job id" job-search/[Company-JobTitle]/job-posting.md
```

**If Job ID exists, generate LinkedIn application URL:**

- LinkedIn URL format: `https://www.linkedin.com/jobs/view/{JOB_ID}`
- Example: If Job ID is `4293623911`, URL is `https://www.linkedin.com/jobs/view/4293623911`

**Final Output Summary:**

- Confirm resume PDF was generated
- Confirm cover letter PDF was generated with matching filename format
- **ALWAYS provide this complete summary:**

```
✅ RESUME GENERATION COMPLETE FOR [COMPANY]

Generated Files:
- Resume PDF: file:///[full-path]/[Company-JobTitle]-Resume.pdf
- Cover Letter PDF: file:///[full-path]/[Company-JobTitle]-CoverLetter.pdf

LinkedIn Application URL: https://www.linkedin.com/jobs/view/{JOB_ID}
(Or "No LinkedIn Job ID available" if manually created job)

Next Steps:
1. Review PDFs for final quality check
2. Apply using LinkedIn URL above
3. [Any specific application notes for this company]
```

## Final Job Directory Structure

After completing resume generation, your job directory should contain:

```
job-search/[Company-JobTitle]/
├── job-tracking.yaml                    # Primary tracking file with YAML structure
├── job-posting.md                       # Original job posting content
├── company-research-report.md           # Company analysis and red flags
├── customization-analysis.md            # Job requirements analysis
├── cover-letter.txt                     # Text version for editing
├── [Company-JobTitle]-Resume.pdf        # Final resume PDF
├── [Company-JobTitle]-CoverLetter.pdf   # Final cover letter PDF
├── resume-branndon-coelho-[company]-ats.json  # ATS-optimized resume JSON
├── application-tracking.md              # Application status and next steps
├── interview-prep.md                    # General interview preparation template
├── correspondence/                      # All non-interview communications
│   ├── emails.md                       # Email correspondence with recruiters/hiring managers
│   └── scheduling.md                   # Interview scheduling communications (optional)
└── interviews/                         # All interview-related materials
    ├── preparation-round-1.md          # Round 1 interview preparation
    ├── preparation-round-2.md          # Round 2+ preparations (as needed)
    ├── coding-test-1-[description].py  # Coding challenges and solutions
    ├── coding-test-2-[description].py  # Additional tests (as needed)
    ├── technical-interview-round-1-notes.md  # Interview notes and questions
    ├── technical-interview-round-2-notes.md  # Additional rounds (as needed)
    ├── post-interview-follow-up.md     # Follow-up strategy and actions
    ├── post-interview-thank-you-notes.md    # Thank you messages sent
    └── post-interview-feedback-received.md  # Feedback from interviews
```

**Note**: The `interviews/` and `correspondence/` directories are created automatically when interview processes begin. The job-tracking.yaml file includes references to these structured paths for comprehensive tracking.

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

### Cover Letter Limits (CRITICAL)

- **Total Length**: Maximum 3 paragraphs + greeting/closing
- **Paragraph 1**: Around 60 words - Personal connection to company (human, not AI corporate speak)
- **Paragraph 2**: Around 60 words - Most relevant technical experience match (accurate timeline/company)
- **Paragraph 3**: Around 60 words - Value proposition + professional call to action
- **Sentence Length**: Maximum 25 words per sentence
- **Writing Style**: Follow Buffer cover letter example - professional but conversational, no fluff or jargon
- **Validation**: Check for duplicate contact info, fabricated timelines, corporate buzzwords
- **Read complete files**: ALWAYS read entire documents - context is critical, don't use line limits unless file exceeds tool capacity

### Cover Letter Writing Style Guide

**Reference Example**: `job-search/Buffer-Senior-Product-Engineer-Backend/cover-letter.txt`

**Language Characteristics:**

- **Direct and clear**: "I'm interested in what you folks are building" - straightforward, no unnecessary words
- **Specific details**: "67% performance improvement" not "significant improvements"
- **Professional but human**: "I'm genuinely curious" not "I am excited to leverage synergies"
- **Technical without jargon**: "enhanced our Hapi API system with server-driven UI capabilities" - precise but accessible
- **Natural transitions**: "This experience building scalable content systems seems like a natural fit"
- **No buzzwords**: Avoid "passionate," "innovative," "cutting-edge," "synergistic," etc.
- **No casual slang**: Professional tone without being overly informal
- **Action-oriented**: "I'd love to discuss" not "I would be honored to have the opportunity to potentially explore"
- **Specific technical focus**: "applying machine learning to insurance workflows" not "transforming the insurance industry"
- **Authentic interest**: "I'm genuinely curious about [specific technical challenge]" not "I'm excited about your amazing mission"

**What to Avoid:**

- Corporate buzzword salad ("leverage core competencies to drive innovative solutions")
- Overly casual language ("Hey there!" or "Sounds like fun!" or "Let's chat!")
- **Folksy language** ("you folks" - use "you're" or "your team" instead)
- **Regurgitating company marketing speak** ("transforming the industry", "revolutionizing", "disrupting")
- **Generic praise** ("your talented team", "amazing company", "incredible mission")
- **Buzzword combinations** ("cutting-edge technology", "innovative solutions", "next-generation platform")
- **Grand transformation language** ("changing the world", "transforming industries") - focus on specific work instead
- AI "thing" pattern ("That transparency thing, refreshing" - dismissive and robotic)
- Redundant phrases ("in order to," "at this point in time")
- Vague achievements ("improved performance significantly")
- Generic enthusiasm ("thrilled about this amazing opportunity")
- **NEVER use "I've been following [Company/Product]"** - dishonest pattern that sounds fake and researched

### Sections to Remove

- **Fun Facts Section**: Remove entirely for ATS
- **Recommendations Section**: Keep (shows credibility)

## Quality Assurance Checklist

### Before Starting

- [ ] Read this ENTIRE document first
- [ ] Located templates at `docs/templates/resume-ats-template.json` and `docs/templates/job-tracking-template.yaml`
- [ ] Identified job requirements from job-posting.md
- [ ] Filled out comprehensive job-tracking.yaml file
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

_This document contains EVERYTHING needed for resume generation. Do not reference other docs._
