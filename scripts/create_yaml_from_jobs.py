#!/usr/bin/env python3
"""
Create job-application.yaml files from existing job directories.
Focused on YAML creation and verification only.
"""

import yaml
import argparse
from pathlib import Path
from datetime import datetime
import re


def extract_job_info_from_posting(job_posting_file: Path) -> dict:
    """Extract job information from job-posting.md file."""
    if not job_posting_file.exists():
        return {}

    try:
        with open(job_posting_file, "r") as f:
            content = f.read()

        # Extract metadata
        job_id_match = re.search(r"\*\*Job ID\*\*:\s*`([^`]+)`", content)
        job_id = job_id_match.group(1) if job_id_match else ""

        # Extract basic company/title info
        title_match = re.search(r"---\n\n# (.+?)\n", content)
        title = title_match.group(1) if title_match else ""

        company_match = re.search(r"\*\*Company\*\*:\s*(.+)", content)
        company = company_match.group(1) if company_match else ""

        location_match = re.search(r"\*\*Location\*\*:\s*(.+)", content)
        location = location_match.group(1) if location_match else ""

        level_match = re.search(r"\*\*Level\*\*:\s*(.+)", content)
        level = level_match.group(1) if level_match else ""

        score_match = re.search(r"\*\*Resume Score\*\*:\s*(\d+)", content)
        score = int(score_match.group(1)) if score_match else 0

        # Try to extract LinkedIn URL
        linkedin_url = ""
        if job_id:
            linkedin_url = f"https://www.linkedin.com/jobs/view/{job_id}"

        return {
            "job_id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "level": level,
            "resume_score": score,
            "linkedin_url": linkedin_url,
        }

    except Exception as e:
        print(f"Error reading {job_posting_file}: {e}")
        return {}


def create_yaml_from_job_directory(job_dir: Path, dry_run: bool = False) -> bool:
    """Create job-application.yaml from existing job directory files."""

    # Check if YAML already exists
    yaml_file = job_dir / "job-application.yaml"
    if yaml_file.exists():
        print(f"  ⏭️  YAML already exists: {job_dir.name}")
        return True

    # Extract info from existing files
    job_posting = job_dir / "job-posting.md"
    job_info = extract_job_info_from_posting(job_posting)

    if not job_info.get("company"):
        print(f"  ⚠️  Skipping {job_dir.name} - no company info found")
        return False

    # Create YAML structure
    yaml_data = {
        "job_id": job_info.get("job_id", ""),
        "status": "imported",
        "company": job_info.get("company", ""),
        "title": job_info.get("title", ""),
        "location": job_info.get("location", ""),
        "level": job_info.get("level", ""),
        "resume_score": job_info.get("resume_score", 0),
        "linkedin_url": job_info.get("linkedin_url", ""),
        "application_timeline": {
            "scraped": "TBD",
            "imported": datetime.now().strftime("%Y-%m-%d"),
            "applied": "TBD",
            "response_deadline": "TBD",
        },
        "job_details": {
            "tech_stack": [],
            "key_requirements": "TBD - migrate from job-posting.md",
            "compensation": {"salary_range": "Not specified", "benefits": "TBD - extract from job posting"},
        },
        "my_match": {"strengths": [], "learning_opportunities": []},
        "company_research": {
            "financial_health": "TBD - needs research",
            "funding": "TBD",
            "employee_feedback": "TBD",
            "culture": "TBD - needs research",
            "red_flags": "TBD",
        },
        "application_materials": {
            "resume_pdf": f"./{job_dir.name}-Resume.pdf",
            "cover_letter_pdf": f"./{job_dir.name}-CoverLetter.pdf",
            "ats_resume_json": f"./resume-branndon-coelho-{job_info.get('company', '').lower()}-ats.json",
        },
        "cover_letter_approach": "TBD - migrate from cover-letter.txt",
        "notes": f"Migrated from existing job directory on {datetime.now().strftime('%Y-%m-%d')}. Manual review recommended to fill TBD fields.",
        "follow_up": {"next_action": "Review and complete TBD fields in this YAML", "check_date": "TBD", "backup_plan": "TBD"},
        "interview_prep": {"technical_topics": [], "behavioral_topics": []},
        "decision_factors": {"pros": [], "cons": [], "verdict": "TBD - needs evaluation"},
    }

    if dry_run:
        print(
            f"  📝 Would create YAML for {job_info.get('company')} - {job_info.get('title')} (Score: {job_info.get('resume_score', 0)})"
        )
        return True

    # Save YAML file
    try:
        with open(yaml_file, "w") as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=80)

        print(
            f"  ✅ Created YAML: {job_info.get('company')} - {job_info.get('title')} (Score: {job_info.get('resume_score', 0)})"
        )
        return True

    except Exception as e:
        print(f"  ❌ Error creating YAML for {job_dir.name}: {e}")
        return False


def verify_yaml_content(yaml_file: Path) -> dict:
    """Verify YAML content and return analysis."""
    try:
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        analysis = {
            "valid_yaml": True,
            "company": data.get("company", ""),
            "title": data.get("title", ""),
            "resume_score": data.get("resume_score", 0),
            "tbd_count": str(data).count("TBD"),
            "has_job_id": bool(data.get("job_id")),
        }

        return analysis

    except Exception as e:
        return {"valid_yaml": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Create job-application.yaml files from existing jobs")
    parser.add_argument("--job-search-dir", default="./job-search", help="Path to job-search directory (default: ./job-search)")
    parser.add_argument("--dry-run", action="store_true", help="Show what YAMLs would be created without making changes")
    parser.add_argument("--verify-existing", action="store_true", help="Verify existing YAML files instead of creating new ones")

    args = parser.parse_args()
    job_search_dir = Path(args.job_search_dir)

    if not job_search_dir.exists():
        print(f"Job search directory not found: {job_search_dir}")
        return 1

    job_dirs = [d for d in job_search_dir.iterdir() if d.is_dir()]
    if not job_dirs:
        print("No job directories found")
        return 1

    print(f"📁 Found {len(job_dirs)} job directories")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be created")
    elif args.verify_existing:
        print("✅ VERIFY MODE - Checking existing YAML files")

    created_count = 0
    verified_count = 0
    skipped_count = 0

    for job_dir in sorted(job_dirs):
        print(f"Processing: {job_dir.name}")

        yaml_file = job_dir / "job-application.yaml"

        if args.verify_existing:
            if yaml_file.exists():
                analysis = verify_yaml_content(yaml_file)
                if analysis["valid_yaml"]:
                    print(
                        f"  ✅ Valid: {analysis['company']} - {analysis['title']} (Score: {analysis['resume_score']}, TBD: {analysis['tbd_count']})"
                    )
                    verified_count += 1
                else:
                    print(f"  ❌ Invalid YAML: {analysis.get('error', 'Unknown error')}")
            else:
                print(f"  ⚠️  No YAML file found")
                skipped_count += 1
        else:
            if create_yaml_from_job_directory(job_dir, args.dry_run):
                if not args.dry_run and yaml_file.exists():
                    # Verify created YAML
                    analysis = verify_yaml_content(yaml_file)
                    if not analysis["valid_yaml"]:
                        print(f"    ⚠️  Created YAML has issues: {analysis.get('error', 'Unknown')}")
                created_count += 1
            else:
                skipped_count += 1

    print(f"\\n📊 Summary:")
    if args.verify_existing:
        print(f"   Verified: {verified_count}")
    else:
        print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total: {len(job_dirs)}")

    if not args.dry_run and created_count > 0:
        print(f"\\n💡 Next steps:")
        print(f"   1. Review created YAML files and fill in TBD fields")
        print(f"   2. Use: poetry run python scripts/cleanup_legacy_files.py")
        print(f"   3. Query with: yq '.company' job-search/*/job-application.yaml")

    return 0


if __name__ == "__main__":
    exit(main())
