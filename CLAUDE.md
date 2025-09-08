# Claude Instructions for branndon.dev

## Critical Global Rules (Apply to ALL tasks)

1. **NEVER fabricate information** - Only use existing, verified content
2. **Use MultiEdit for efficiency** when making multiple changes to files
3. **Preserve exact language** - Don't paraphrase technical content unnecessarily

## Self-Contained Workflow Documents

**⚠️ IMPORTANT: Each workflow doc below is COMPLETE and SELF-CONTAINED. When doing a specific task, use ONLY the relevant workflow doc - do not reference multiple docs.**

### For Resume Generation

**USE THIS**: `./docs/RESUME_GENERATION_COMPLETE.md`

- Contains EVERYTHING: comprehensive workflow, rules, templates
- Do NOT reference other docs when using this

### For Other Documentation (Reference Only)

- `./docs/` - Contains various project documentation
- List directory first if unsure which doc to use

## Directory Structure

- `./job-search/[Company-JobTitle]/` - Individual job applications (private, gitignored)
  - Each contains `job-application.yaml` with complete job tracking data
- `./docs/` - Self-contained workflow documents
- `./webroot/` - Live resume files and assets
- `./scripts/` - PDF generation and utility scripts

## Job Tracking and Queries

**Primary job tracking is now YAML-based** - each job directory contains a `job-application.yaml` file with comprehensive tracking data.

### Using yq for Job Queries

Install yq: `brew install yq`

**Common queries:**

```bash
# Show all applied jobs
yq 'select(.status == "applied")' job-search/*/job-application.yaml

# Find jobs by company
yq 'select(.company == "Files.com")' job-search/*/job-application.yaml

# High-scoring unprocessed jobs
yq 'select(.resume_score > 90 and .status == "new")' job-search/*/job-application.yaml

# Show tech stacks for all jobs
yq '.company + ": " + (.job_details.tech_stack | join(", "))' job-search/*/job-application.yaml

# Jobs needing follow-up
yq 'select(.follow_up.check_date) | {company, check_date: .follow_up.check_date}' job-search/*/job-application.yaml

# Companies with red flags
yq 'select(.company_research.red_flags != "None identified")' job-search/*/job-application.yaml
```

### Using ripgrep for Simple Searches

```bash
# All Ruby jobs
rg "Ruby" job-search/*/job-application.yaml

# High-scoring jobs
rg "resume_score: 9[0-9]" job-search/*/job-application.yaml

# Jobs with specific benefits
rg -A3 "benefits:" job-search/*/job-application.yaml
```

### YAML Job Management Scripts

**Job Tracker** - Status updates and queries:

```bash
# Show statistics
poetry run python scripts/job_tracker_yaml.py status

# List all jobs
poetry run python scripts/job_tracker_yaml.py list

# Update job status
poetry run python scripts/job_tracker_yaml.py update 4288643008 applied --notes "Application submitted"

# Show query examples
poetry run python scripts/job_tracker_yaml.py query
```

**Migration Scripts** - Convert existing jobs to YAML:

```bash
# 1. Create YAML files from existing jobs (dry-run first)
poetry run python scripts/create_yaml_from_jobs.py --dry-run
poetry run python scripts/create_yaml_from_jobs.py

# 2. Verify existing YAML files
poetry run python scripts/create_yaml_from_jobs.py --verify-existing

# 3. Clean up legacy template files (after YAML creation)
poetry run python scripts/cleanup_legacy_files.py --dry-run
poetry run python scripts/cleanup_legacy_files.py
```
