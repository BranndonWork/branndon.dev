---
description: "Generate complete job application package with ATS resume and PDF"
argument-hint: "[Company-JobTitle]"
---

# Resume Generation Command

## Instructions

**Read and follow `docs/RESUME_GENERATION_COMPLETE.md` carefully.**

**Always Read RESUME_GENERATION_COMPLETE.md First**: This document is a summary. The full, detailed workflow is in `docs/RESUME_GENERATION_COMPLETE.md`. Always refer to that for complete instructions. eg: Read(docs/RESUME_GENERATION_COMPLETE.md)

## Key Reminder: MANDATORY VERIFICATION

**🚨 CRITICAL**: Before PDF generation, MUST use the resume-audit-validator agent to verify all claims are truthful:

```bash
Task(subagent_type="resume-audit-validator", description="Verify resume claims",
     prompt="Please audit and validate the [Company] resume generation...")
```

This step is non-negotiable and blocks PDF generation until passed.

## Target Job Directory

$ARGUMENTS
