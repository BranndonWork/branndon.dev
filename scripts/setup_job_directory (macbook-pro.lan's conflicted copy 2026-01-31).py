#!/usr/bin/env python3
"""
Job Directory Setup Script
Creates standardized job directory structure with all template files.
Works independently of job import - use for manual job setup or import workflow.
"""

import os
import shutil
import argparse
import re
from pathlib import Path
from datetime import datetime


class JobDirectorySetup:
    def __init__(self, target_dir: str = None):
        """Initialize job directory setup."""
        self.target_dir = Path(target_dir) if target_dir else Path.cwd() / "job-search"
        self.templates_dir = Path(__file__).parent.parent / "docs" / "templates"

        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

    def create_directory_name(self, company: str, title: str) -> str:
        """Create standardized directory name for job."""
        # Clean company name
        company_clean = re.sub(r'[^a-zA-Z0-9\s-]', '', company)
        company_clean = re.sub(r'\s+', '-', company_clean.strip())

        # Clean title - extract key role info
        title_clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        title_clean = re.sub(r'\s+', '-', title_clean.strip())

        # Combine and limit length
        dir_name = f"{company_clean}-{title_clean}"

        # Replace multiple consecutive hyphens with single hyphen
        dir_name = re.sub(r'-+', '-', dir_name)

        if len(dir_name) > 80:  # Limit directory name length
            dir_name = dir_name[:80].rstrip('-')

        return dir_name

    def create_directory_structure(self, job_dir: Path):
        """Create the standardized directory structure."""
        # Create main job directory
        job_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        interviews_dir = job_dir / "interviews"
        correspondence_dir = job_dir / "correspondence"

        interviews_dir.mkdir(exist_ok=True)
        correspondence_dir.mkdir(exist_ok=True)

        print(f"  ✓ Created directory structure:")
        print(f"    • {job_dir.name}/")
        print(f"    • {job_dir.name}/interviews/")
        print(f"    • {job_dir.name}/correspondence/")

    def copy_template_files(self, job_dir: Path, company_slug: str = None):
        """Copy all template files to job directory, skip existing files."""
        if not company_slug:
            company_slug = job_dir.name.split('-')[0].lower()

        # Template files mapping
        template_files = {
            "job-tracking-template.yaml": "job-tracking.yaml",
            "resume-ats-template.json": f"resume-branndon-coelho-{company_slug}-ats.json",
            "customization-analysis-template.md": "customization-analysis.md",
            "application-tracking-template.md": "application-tracking.md",
            "interview-prep-template.md": "interview-prep.md",
            "cover-letter-template.txt": "cover-letter.txt"
        }

        print(f"  📋 Copying template files:")

        for template_file, target_name in template_files.items():
            template_path = self.templates_dir / template_file
            target_path = job_dir / target_name

            if not template_path.exists():
                print(f"    ⚠️ Template not found: {template_file}")
                continue

            # Skip if file already exists
            if target_path.exists():
                print(f"    ↪ Skipped {target_name} (already exists)")
                continue

            try:
                shutil.copy2(template_path, target_path)
                print(f"    ✓ Copied {template_file} → {target_name}")
            except Exception as e:
                print(f"    ⚠️ Failed to copy {template_file}: {e}")

    def setup_job_directory(self, company: str, title: str, force: bool = False) -> str:
        """Set up complete job directory with all templates."""
        # Create directory name
        dir_name = self.create_directory_name(company, title)
        job_dir = self.target_dir / dir_name

        # Handle existing directory
        if job_dir.exists():
            # Check if directory has critical tracking files
            has_yaml = (job_dir / "job-tracking.yaml").exists() or (job_dir / "job-application.yaml").exists()
            has_progress = (job_dir / "application-tracking.md").exists() or (job_dir / "job-progress.md").exists()

            # If directory exists but has no critical files, reuse it
            if not has_yaml and not has_progress:
                print(f"Directory exists but is empty, reusing: {job_dir.name}")
            # If force flag is set, use existing directory regardless
            elif force:
                print(f"Using existing directory (--force): {job_dir.name}")
            # Otherwise, create numbered variant
            else:
                counter = 1
                while (self.target_dir / f"{dir_name}-{counter}").exists():
                    counter += 1
                job_dir = self.target_dir / f"{dir_name}-{counter}"
                print(f"Directory exists with files, using: {job_dir.name}")

        print(f"\n📁 Setting up job directory: {job_dir.name}")

        # Create directory structure
        self.create_directory_structure(job_dir)

        # Copy template files
        self.copy_template_files(job_dir)

        print(f"\n✅ Job directory setup complete!")
        print(f"Directory: {job_dir}")
        print(f"\n📋 Template files ready for customization:")
        print(f"  • job-tracking.yaml - Fill this out FIRST")
        print(f"  • customization-analysis.md - Job requirements analysis")
        print(f"  • interview-prep.md - Interview preparation")
        print(f"  • cover-letter.txt - Cover letter draft")

        return str(job_dir)

    def list_existing_jobs(self) -> list:
        """List existing job directories."""
        if not self.target_dir.exists():
            return []

        jobs = []
        for dir_path in self.target_dir.iterdir():
            if dir_path.is_dir() and not dir_path.name.startswith('.'):
                # Check if it has expected job files
                has_tracking = (dir_path / "job-tracking.yaml").exists()
                has_posting = (dir_path / "job-posting.md").exists()

                jobs.append({
                    "name": dir_path.name,
                    "path": str(dir_path),
                    "has_tracking": has_tracking,
                    "has_posting": has_posting,
                    "created": dir_path.stat().st_ctime
                })

        # Sort by creation time, newest first
        jobs.sort(key=lambda x: x["created"], reverse=True)
        return jobs


def main():
    parser = argparse.ArgumentParser(description="Set up standardized job directory structure with templates")
    parser.add_argument(
        "company",
        help="Company name"
    )
    parser.add_argument(
        "title",
        help="Job title"
    )
    parser.add_argument(
        "--target-dir",
        default="./job-search",
        help="Target directory for job folders (default: ./job-search)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Use existing directory if it exists (don't create numbered variant)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List existing job directories"
    )

    args = parser.parse_args()

    try:
        setup = JobDirectorySetup(args.target_dir)

        if args.list:
            print(f"\n📋 Existing job directories in {setup.target_dir}:")
            jobs = setup.list_existing_jobs()

            if not jobs:
                print("  No job directories found.")
                return

            print(f"{'Directory Name':<50} {'Tracking':<10} {'Posting':<10}")
            print("-" * 75)

            for job in jobs:
                tracking = "✓" if job["has_tracking"] else "✗"
                posting = "✓" if job["has_posting"] else "✗"
                print(f"{job['name']:<50} {tracking:<10} {posting:<10}")

            print(f"\n💡 Use 'python scripts/setup_job_directory.py \"<Company>\" \"<Job Title>\"' to create new directory")
            return

        if not args.company or not args.title:
            print("❌ Company and title are required unless using --list")
            return 1

        job_dir = setup.setup_job_directory(args.company, args.title, args.force)

        print(f"\n🎯 Next steps:")
        print(f"1. Fill out job-tracking.yaml with job details")
        print(f"2. Add job posting content to job-posting.md (if available)")
        print(f"3. Follow RESUME_GENERATION_COMPLETE.md workflow for resume generation")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())