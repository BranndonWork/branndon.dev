---
description: "Generate complete job application package with ATS resume and PDF"
argument-hint: "[Company-JobTitle]"
---

# Resume Generation Workflow

Generate a complete job application package for the specified job directory, following the documented workflow process.

## Instructions

1. **Validate Prerequisites**:
   - Confirm job directory exists: `./job-search/$ARGUMENTS/`
   - Verify `job-posting.md` exists in the directory

2. **Create Missing Files Only** (never overwrite existing):
   - Copy ATS template to `resume-branndon-coelho-[company]-ats.json` if missing
   - Copy example templates for missing tracking files:
     - `application-tracking.md` (from example directory)
     - `interview-prep.md` (from example directory)
     - `cover-letter.txt` (create new based on job requirements)
     - `customization-analysis.md` (create new)

3. **Analyze Job Requirements**:
   - Read `job-posting.md` to extract key requirements
   - Identify technologies, skills, and experience needed
   - Map to items in ENGINEER_PROFILE.md (never fabricate)

4. **Customize ATS Resume**:
   - Use MultiEdit to customize the ATS template
   - Follow LLM_RESUME_RULES.md strictly
   - Emphasize relevant experience from ENGINEER_PROFILE.md
   - Reorder technologies to match job requirements
   - Update position titles, summary, and descriptions

5. **Generate PDF**:
   - Follow the complete workflow in `docs/ATS_RESUME_LIMITS.md`
   - This includes server checks, port handling, and proper cleanup
   - Output PDF to `./job-search/$ARGUMENTS/resume.pdf`

6. **Verify Output**:
   - Confirm PDF was generated successfully
   - List final directory contents
   - Report what files were created vs preserved
   - **PROVIDE VERIFICATION LINKS**: Always provide clickable file:// links to generated resume.pdf and cover-letter.txt for user verification

## Safety Rules

- NEVER fabricate skills or experience
- ONLY use content from ENGINEER_PROFILE.md
- NEVER overwrite existing customized files
- Follow exact language from original resume
- Maintain truthful representation throughout

## Target Job Directory

$ARGUMENTS