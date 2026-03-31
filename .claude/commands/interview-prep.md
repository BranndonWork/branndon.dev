---
description: "Generate interview fact sheet for job/company"
allowed-tools: ["read", "grep", "glob", "write", "bash"]
---

# Interview Prep Fact Sheet Generator

## Instructions

Generate a concise, scannable interview fact sheet (under 500 words) for a job/company that includes:

- Company name and brief summary
- Top required languages and skills
- Top "nice to have" languages and skills
- Salary range
- Benefits
- Key points to mention during phone screens
- Company recognition/awards

## Workflow

1. **Extract job information** from the provided context (job description text, job-application.yaml file, or other sources mentioned in user instructions)

2. **Determine company and job title** to create the job directory name in format: `Company-JobTitle` (e.g., `SentinelOne-StaffAIAPIEngineer`)

3. **Check if job directory exists** at `job-search/[Company-JobTitle]/`
   - If not, create the directory structure

4. **Save job description** as `job-search/[Company-JobTitle]/job-description.md` with the raw job posting text

5. **Read the HTML template** from `.claude/commands/templates/interview-fact-sheet-template.html`

6. **Generate the fact sheet content** by:
   - Extracting and organizing required vs nice-to-have skills
   - Identifying key languages and technologies
   - **CRITICAL: Bold skills/languages that match user's resume** by reading `/Volumes/Storage/Dropbox/workspace/projects/branndon.dev/webroot/branndon-coelho-resume.json` and comparing against job requirements
   - Use `<strong>` tags for matching skills in both Required and Nice to Have sections
   - Pulling salary range if available
   - Summarizing benefits
   - Highlighting company recognition/awards
   - Noting key talking points for interviews (CRITICAL: Do NOT duplicate information already listed in Required or Nice to Have sections. Focus on unique aspects like company culture, role context, work environment, strategic importance, or interview emphasis points)

7. **Create the HTML file** at `job-search/[Company-JobTitle]/interview-fact-sheet.html` using the template with Tailwind CSS via CDN

8. **Format for print-friendliness**:
   - Use clean columns and containers
   - High-contrast, readable fonts
   - Organized sections for easy scanning
   - Page-break considerations

9. **Confirm completion** and provide the file path

## Notes

- Keep total content under 500 words
- Use Tailwind CSS via CDN for styling
- Organize with columns/containers for easy scanning during phone calls
- Make it print-friendly with clean formatting
- The template HTML file must exist at `.claude/commands/templates/interview-fact-sheet-template.html`

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
