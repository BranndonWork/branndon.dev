# Job Directory YAML Migration Process

## Overview

Convert job directories from multiple files to a single `job-tracking.yaml` for AI/system use, while keeping human-readable files separate.

## Step-by-Step Process

### 1. Read Source Files

For each job directory, read these files to extract data:

- `customization-analysis.md` → Extract tech stack, requirements, strengths, learning gaps
- `application-tracking.md` → Extract status, timeline info
- `job-posting.md` → Extract basic job info (title, company, salary, location)

### 2. Create job-tracking.yaml

Using template: `docs/templates/job-tracking-template.yaml`

- Copy template to `job-search/[Company-JobTitle]/job-tracking.yaml`
- Fill in all extracted data from source files
- Update file references to point to remaining external files

### 3. Verify Data Migration

Check that all important data from source files is captured in YAML:

- ✅ Tech stack from job posting
- ✅ Key requirements from job posting
- ✅ Your matching strengths from customization analysis
- ✅ Learning opportunities/gaps from customization analysis
- ✅ Decision factors (pros/cons/verdict) from customization analysis
- ✅ Application status from tracking file

### 4. Delete Migrated Files

Once verified, remove these files:

- ❌ `customization-analysis.md` (data migrated to YAML)
- ❌ `application-tracking.md` (data migrated to YAML)

## Files That Remain

### ✅ Keep These Files (Human Use)

- `job-tracking.yaml` - Complete tracking data for AI/system use
- `interview-prep.md` - For reading before interviews
- `job-posting.md` - Original posting for reference
- `cover-letter.txt` - For use when applying
- `company-research-report.md` - Detailed research for reading
- `*.pdf` files - Resume and cover letter PDFs
- `*.json` files - ATS resume files

### ❌ Delete These Files (After Migration)

- `customization-analysis.md` - Technical data → YAML
- `application-tracking.md` - Status/timeline → YAML

## Final Directory Structure

```
job-search/Company-JobTitle/
├── job-tracking.yaml          # AI/system tracking data
├── interview-prep.md          # Human-readable interview prep
├── job-posting.md            # Original job posting reference
├── cover-letter.txt          # Cover letter for applying
├── company-research-report.md # Human-readable company research
├── Company-JobTitle-Resume.pdf
├── Company-JobTitle-CoverLetter.pdf
└── resume-branndon-coelho-company-ats.json
```

## Key Principles

1. **YAML = Database** - Structured data for AI/system queries and tracking
2. **MD Files = Human Reading** - Content you need to read and reference
3. **Separate Concerns** - Tracking data vs human-readable content
4. **File References** - YAML points to external files, doesn't duplicate content

## Example YAML Structure

```yaml
company_research:
  file: "./company-research-report.md"
  summary: "Brief summary for AI context"

interview_prep:
  file: "./interview-prep.md"
  summary: "Brief summary for AI context"

cover_letter_file: "./cover-letter.txt"
```

## Migration Command Pattern

For each job directory:

1. `Read` all source files
2. Extract data using `MultiEdit` to populate YAML template
3. Verify data completeness
4. `rm customization-analysis.md application-tracking.md`
