# Claude Instructions for branndon.dev

## Project Documentation Reference

When working on resume customization or job search tasks, reference these project-specific docs:

- **RESUME_CUSTOMIZATION_WORKFLOW.md** - Step-by-step process for customizing resumes using human+LLM workflow, emphasizes never fabricating skills
- **JOB_APPLICATION_CUSTOMIZATION.md** - Framework for organizing job applications with examples  
- **ATS_BEST_PRACTICES.md** - Guidelines for ATS-friendly formatting and keyword optimization
- **RESUME_WRITING_STYLE.md** - Writing guidelines and tone for resume content
- **WORK_HISTORY_DETAILED.md** - Complete work history details for accurate resume updates
- **RECOMMENDATIONS.md** - Available recommendations and when to include them
- **FUN_FACTS_ACHIEVEMENTS.md** - Personal achievements and interesting facts for resume customization
- **RESUME_PROJECT.md** - Overall project overview and goals
- **LOCAL_SETUP.md** - Instructions for running the resume site locally

**When in doubt about which doc to use, always list the ./docs/ directory first to see available documentation.**

## Resume Customization Rules

1. **NEVER fabricate skills, experience, or achievements** - Only reorganize and emphasize existing content
2. **Always read original resume first** for full context before making changes
3. **Use MultiEdit for efficiency** when making multiple changes to resume files
4. **Copy original resume** to new location to preserve structure and save tokens
5. **Job applications should look completely real** - no "this is an example" disclaimers in application files

## Directory Structure

- `./job-search/[Company-JobTitle]/` - Individual job applications (private, gitignored except example)
- `./docs/` - Project documentation and guidelines
- `./webroot/` - Live resume files and assets
- `./scripts/` - PDF generation and utility scripts

## Template Example

The `job-search/example-ACME-Corp-Senior-Django-Developer/` directory serves as a template but should be treated as a real application with no disclaimers in the application files themselves. The "example" nature is documented only in the workflow docs.