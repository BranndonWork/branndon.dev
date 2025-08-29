# Job Application Customization Process

## Folder Structure

When applying to a specific position, create this structure:

```
/job-search/                      # Root folder for all job applications (GITIGNORED)
├── CompanyName-JobTitle/          # Individual application folder
│   ├── job-posting.md             # Original job description
│   ├── resume-branndon-coelho-[company].json  # Customized resume data
│   ├── cover-letter.txt           # Cover letter source
│   ├── customization-analysis.md  # Job analysis, customizations made, cover letter strategy, ATS optimization
│   ├── application-tracking.md    # Submission details, follow-up schedule, communication log
│   └── interview-prep.md          # Technical prep, company research, questions to prepare
```

## Customization Workflow

### Step 1: Analyze Job Posting

1. Copy job description to `job-posting.md`
2. Highlight key requirements:
    - Required technologies
    - Years of experience
    - Specific responsibilities
    - Company values/culture keywords
    - Industry-specific terms

### Step 2: Keyword Mapping

Create a keyword map from job posting to your experience:

| Job Requirement | Your Experience | Keywords to Use    |
| --------------- | --------------- | ------------------ |
| Their term      | Your equivalent | Exact match phrase |

### Step 3: Resume Customization

#### Priority Order for Changes:

1. **Professional Summary** - Rewrite to mirror job description language
2. **Recent Job Title** - Adjust if needed to match target role
3. **Achievements** - Reorder to put most relevant first
4. **Technologies** - Reorder to match job requirements order
5. **Remove/Add** - Remove irrelevant items, add missing relevant ones

#### Customization Rules:

-   **Never lie** - Only reorganize and emphasize existing experience
-   **Match their language** - If they say "Python Developer" not "Software Engineer", adjust accordingly
-   **Quantify when possible** - Add metrics that relate to their needs
-   **Industry context** - Add relevant industry terms they use

### Step 4: Cover Letter Structure

```markdown
# [Your Name]

[Date]

Dear [Hiring Manager Name or "Hiring Team"],

## Opening Paragraph

-   State position applying for
-   How you found it
-   One sentence hook about why you're perfect

## Body Paragraph 1 - Direct Match

-   Address their #1 requirement
-   Specific example from your experience
-   Quantifiable result

## Body Paragraph 2 - Additional Value

-   Address 2-3 other requirements
-   Show understanding of their challenges
-   How you've solved similar problems

## Body Paragraph 3 - Cultural Fit

-   Reference company values/mission
-   Personal connection to their work
-   Enthusiasm for specific aspects

## Closing Paragraph

-   Reiterate interest
-   Next steps
-   Contact availability

Sincerely,
[Your Name]
```

### Step 5: Application Tracking

Create three separate tracking files:

#### `customization-analysis.md`:

-   Job requirements analysis
-   Keywords incorporated
-   Customizations made and rationale
-   Cover letter strategy
-   ATS optimization score

#### `application-tracking.md`:

-   Submission details (date, platform, job ID)
-   Follow-up schedule
-   Communication log
-   Status updates

#### `interview-prep.md`:

-   Technical preparation
-   Company research
-   Questions to ask them
-   Salary discussion prep

## Template Files

All templates are located in `/docs/templates/`:

-   `resume-ats-template.json` - Clean resume template for customization
-   `application-tracking-template.md` - Track application status and follow-ups
-   `interview-prep-template.md` - Prepare for interviews
-   `customization-analysis-template.md` - Document customization decisions
-   `cover-letter-template.txt` - Cover letter structure

## Human + LLM Workflow

Use Claude Code to efficiently set up new applications:

1. Create directory: `mkdir "./job-search/CompanyName-JobTitle"`
2. Copy ALL templates from templates directory:

```bash
cp docs/templates/resume-ats-template.json ./job-search/CompanyName-JobTitle/resume-branndon-coelho-company.json
cp docs/templates/application-tracking-template.md ./job-search/CompanyName-JobTitle/application-tracking.md
cp docs/templates/interview-prep-template.md ./job-search/CompanyName-JobTitle/interview-prep.md
cp docs/templates/customization-analysis-template.md ./job-search/CompanyName-JobTitle/customization-analysis.md
cp docs/templates/cover-letter-template.txt ./job-search/CompanyName-JobTitle/cover-letter.txt
```

3. Use Claude to read original resume, analyze job posting, and customize all files using MultiEdit
4. Fill in templates with job-specific details

## Important Notes

### Maintaining Authenticity

-   All information must be truthful
-   Customization means emphasizing, not fabricating
-   Reordering and highlighting, not inventing

### ATS Optimization Per Application

-   Run each customized resume through ATS scanner
-   Aim for 70%+ keyword match rate
-   Test plain text conversion
-   Verify all dates and formatting

## Quick Checklist for Each Application

-   [ ] Job posting saved
-   [ ] Keywords extracted and mapped
-   [ ] Resume customized with relevant keywords
-   [ ] Achievements reordered by relevance
-   [ ] Technologies list matches job requirements
-   [ ] Cover letter addresses specific requirements
-   [ ] ATS scan shows 70%+ match
-   [ ] PDFs generated
-   [ ] Application tracked in notes
-   [ ] Calendar reminder set for follow-up
