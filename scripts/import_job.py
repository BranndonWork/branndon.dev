#!/usr/bin/env python3
"""
Job Import Script
Imports selected jobs from scraped data to local job-search directory.
"""

import os
import shutil
import argparse
import re
from pathlib import Path
from datetime import datetime
import json

from job_tracker_storage import JobStorage
from job_tracker_operations import JobOperations

class JobTracker:
    """Compatibility wrapper for the new job tracker architecture"""
    def __init__(self, tracking_file=None):
        self.storage = JobStorage(job_search_dir=None, central_tracking_file=tracking_file)
        self.operations = JobOperations(self.storage)
    
    def get_job_status(self, job_id: str) -> str:
        central_data = self.storage.load_central_tracking()
        job_data = central_data.get("jobs", {}).get(job_id, {})
        return job_data.get("status", "new")
    
    def update_job_status(self, job_id: str, status: str, notes: str = "", job_details: dict = None):
        title = job_details.get("title") if job_details else None
        company = job_details.get("company") if job_details else None
        location = job_details.get("location") if job_details else None
        self.operations.update_job_status(job_id, status, notes, title, company, location)


class JobImporter:
    def __init__(self, source_dir: str, target_dir: str = None, tracking_file: str = None):
        """Initialize job importer."""
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir) if target_dir else Path.cwd() / "job-search"
        self.tracker = JobTracker(tracking_file)
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    def extract_job_details(self, job_file: Path) -> dict:
        """Extract job details from markdown file."""
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key information
            job_id_match = re.search(r'\*\*Job ID\*\*:\s*`([^`]+)`', content)
            job_id = job_id_match.group(1) if job_id_match else job_file.stem
            
            title_match = re.search(r'---\n\n# (.+?)\n', content)
            title = title_match.group(1) if title_match else "Unknown Title"
            
            company_match = re.search(r'\*\*Company\*\*:\s*(.+)', content)
            company = company_match.group(1) if company_match else "Unknown"
            
            location_match = re.search(r'\*\*Location\*\*:\s*(.+)', content)
            location = location_match.group(1) if location_match else "Unknown"
            
            level_match = re.search(r'\*\*Level\*\*:\s*(.+)', content)
            level = level_match.group(1) if level_match else ""
            
            score_match = re.search(r'\*\*Resume Score\*\*:\s*(\d+)', content)
            score = int(score_match.group(1)) if score_match else 0
            
            return {
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "level": level,
                "score": score,
                "content": content
            }
        
        except Exception as e:
            print(f"Error extracting job details from {job_file}: {e}")
            return {}
    
    def create_directory_name(self, company: str, title: str) -> str:
        """Create standardized directory name for job."""
        # Clean company name
        company_clean = re.sub(r'[^a-zA-Z0-9\\s-]', '', company)
        company_clean = re.sub(r'\\s+', '-', company_clean.strip())
        
        # Clean title - extract key role info
        title_clean = re.sub(r'[^a-zA-Z0-9\\s-]', '', title)
        title_clean = re.sub(r'\\s+', '-', title_clean.strip())
        
        # Combine and limit length
        dir_name = f"{company_clean}-{title_clean}"
        if len(dir_name) > 80:  # Limit directory name length
            dir_name = dir_name[:80].rstrip('-')
        
        return dir_name
    
    def copy_template_files(self, job_dir: Path):
        """Copy template files to job directory."""
        templates_dir = Path(__file__).parent.parent / "docs" / "templates"
        
        template_files = {
            "resume-ats-template.json": "resume-branndon-coelho-{company}-ats.json",
            "customization-analysis-template.md": "customization-analysis.md",
            "application-tracking-template.md": "application-tracking.md",
            "interview-prep-template.md": "interview-prep.md",
            "cover-letter-template.txt": "cover-letter.txt"
        }
        
        company_slug = job_dir.name.split('-')[0].lower()
        
        for template_file, target_name in template_files.items():
            template_path = templates_dir / template_file
            if template_path.exists():
                target_file = target_name.format(company=company_slug)
                target_path = job_dir / target_file
                try:
                    shutil.copy2(template_path, target_path)
                    print(f"  ✓ Copied {template_file} → {target_file}")
                except Exception as e:
                    print(f"  ⚠️ Failed to copy {template_file}: {e}")
            else:
                print(f"  ⚠️ Template not found: {template_file}")
    
    def import_job(self, job_id: str, force: bool = False) -> str:
        """Import a specific job to local directory."""
        # Find the job file
        job_file = self.source_dir / f"{job_id}.md"
        if not job_file.exists():
            raise FileNotFoundError(f"Job file not found: {job_file}")
        
        # Extract job details
        job_details = self.extract_job_details(job_file)
        if not job_details:
            raise ValueError(f"Could not extract job details from {job_file}")
        
        # Check if already imported
        current_status = self.tracker.get_job_status(job_id)
        if current_status in ["imported", "applying", "applied"] and not force:
            existing_dir = self.find_existing_job_dir(job_id)
            if existing_dir:
                print(f"Job {job_id} already imported to: {existing_dir}")
                return str(existing_dir)
        
        # Create directory name
        dir_name = self.create_directory_name(job_details["company"], job_details["title"])
        job_dir = self.target_dir / dir_name
        
        # Handle existing directory
        if job_dir.exists():
            if not force:
                counter = 1
                while (self.target_dir / f"{dir_name}-{counter}").exists():
                    counter += 1
                job_dir = self.target_dir / f"{dir_name}-{counter}"
                print(f"Directory exists, using: {job_dir.name}")
            else:
                print(f"Overwriting existing directory: {job_dir.name}")
        
        # Create job directory
        job_dir.mkdir(parents=True, exist_ok=True)
        print(f"\\n📁 Creating job directory: {job_dir.name}")
        
        # Save job posting
        job_posting_file = job_dir / "job-posting.md"
        with open(job_posting_file, 'w', encoding='utf-8') as f:
            f.write(job_details["content"])
        print(f"  ✓ Saved job posting: job-posting.md")
        
        # Generate and save LinkedIn URL
        linkedin_url = f"https://www.linkedin.com/jobs/view/{job_id}"
        linkedin_url_file = job_dir / "linkedin-url.txt"
        with open(linkedin_url_file, 'w', encoding='utf-8') as f:
            f.write(linkedin_url)
        print(f"  ✓ Saved LinkedIn URL: linkedin-url.txt")
        
        # Copy template files
        print(f"  📋 Copying template files...")
        self.copy_template_files(job_dir)
        
        # Update tracking
        self.tracker.update_job_status(
            job_id, 
            "imported", 
            f"Imported to {job_dir.name}",
            job_details
        )
        
        print(f"\\n✅ Successfully imported job {job_id}")
        print(f"Directory: {job_dir}")
        print(f"LinkedIn URL: {linkedin_url}")
        
        return str(job_dir)
    
    def find_existing_job_dir(self, job_id: str) -> Path:
        """Find existing job directory for a job ID."""
        if not self.target_dir.exists():
            return None
        
        for dir_path in self.target_dir.iterdir():
            if dir_path.is_dir():
                job_posting = dir_path / "job-posting.md"
                if job_posting.exists():
                    try:
                        content = job_posting.read_text()
                        if f"**Job ID**: `{job_id}`" in content:
                            return dir_path
                    except Exception:
                        continue
        return None
    
    def list_importable_jobs(self, limit: int = 20) -> list:
        """List jobs that can be imported (high scores, not yet imported)."""
        from find_top_jobs import find_top_jobs
        
        # Get top unprocessed jobs
        jobs = find_top_jobs(
            str(self.source_dir),
            top_n=limit * 2,  # Get more to filter
            exclude_processed=False,  # We'll filter manually
            status_filter=None
        )
        
        importable = []
        for job_id, score, title in jobs:
            status = self.tracker.get_job_status(job_id)
            if status in ["new", "reviewed", "researching"]:
                importable.append((job_id, score, title, status))
        
        return importable[:limit]


def main():
    parser = argparse.ArgumentParser(description="Import jobs from scraped data to local directory")
    parser.add_argument(
        "job_id", 
        nargs="?",
        help="Job ID to import (or use --list to see available jobs)"
    )
    parser.add_argument(
        "--source-dir", 
        default="/Volumes/Home/Documents/job-search-2025/data/jobs",
        help="Source directory with scraped jobs"
    )
    parser.add_argument(
        "--target-dir", 
        default="./job-search",
        help="Target directory for imported jobs"
    )
    parser.add_argument(
        "--tracking-file", 
        help="Path to job tracking file"
    )
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List importable jobs"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=20,
        help="Limit number of jobs to show when listing"
    )
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force import even if already imported"
    )
    
    args = parser.parse_args()
    
    try:
        importer = JobImporter(args.source_dir, args.target_dir, args.tracking_file)
        
        if args.list or not args.job_id:
            print(f"\\n📋 Top importable jobs:")
            print(f"{'ID':<12} {'Score':<6} {'Status':<12} {'Title':<50}")
            print("-" * 85)
            
            jobs = importer.list_importable_jobs(args.limit)
            for job_id, score, title, status in jobs:
                title_display = title[:47] + "..." if len(title) > 50 else title
                print(f"{job_id:<12} {score:<6} {status:<12} {title_display:<50}")
            
            if not args.job_id:
                print(f"\\n💡 Use 'python scripts/import_job.py <job_id>' to import a specific job")
                return
        
        if args.job_id:
            job_dir = importer.import_job(args.job_id, args.force)
            
            # Read LinkedIn URL for final output
            linkedin_url_file = Path(job_dir) / 'linkedin-url.txt'
            linkedin_url = ""
            if linkedin_url_file.exists():
                with open(linkedin_url_file, 'r') as f:
                    linkedin_url = f.read().strip()
            
            print(f"\\n🎯 Next steps:")
            print(f"1. Review job posting: {Path(job_dir) / 'job-posting.md'}")
            print(f"2. Research company (if not done): python scripts/research_company.py '<company>'")
            print(f"3. Customize resume: edit {Path(job_dir) / 'customization-analysis.md'}")
            print(f"4. Generate resume: Follow RESUME_GENERATION_COMPLETE.md workflow")
            if linkedin_url:
                print(f"\\n🔗 LinkedIn Job URL: {linkedin_url}")
                print(f"   (Click to apply after resume generation is complete)")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())