#!/usr/bin/env python3
"""
Job Import Script
Imports selected jobs from scraped data to local job-search directory.
"""

import os
import shutil
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
import json

job_search_path = Path("/Volumes/Storage/Dropbox/documents/job-search-2025")
sys.path.append(str(job_search_path))

from job_scraper.sqlite_wrapper import SQLiteProvider
from job_tracker_db import JobTrackerDB, JobOperationsDB, JobStorageDB
from setup_job_directory import JobDirectorySetup

class JobTracker:
    """Compatibility wrapper for the new job tracker architecture"""
    def __init__(self, tracking_file=None):
        self.storage = JobStorageDB(job_search_dir=None, central_tracking_file=tracking_file)
        self.operations = JobOperationsDB(self.storage)
    
    def get_job_status(self, job_id: str) -> str:
        return self.storage.tracker.get_job_status(job_id)
    
    def update_job_status(self, job_id: str, status: str, notes: str = "", job_details: dict = None):
        title = job_details.get("title") if job_details else None
        company = job_details.get("company") if job_details else None
        location = job_details.get("location") if job_details else None
        self.operations.update_job_status(job_id, status, notes, title, company, location)


class JobImporter:
    def __init__(self, source_dir: str = None, target_dir: str = None, tracking_file: str = None):
        """Initialize job importer."""
        self.target_dir = Path(target_dir) if target_dir else Path.cwd() / "job-search"
        self.tracker = JobTracker(tracking_file)
        self.setup = JobDirectorySetup(str(self.target_dir))

        os.environ["SQLITE_DB_PATH"] = str(job_search_path / "jobs_database.db")
        self.db = SQLiteProvider()
    
    def get_job_from_db(self, job_id: str) -> dict:
        """Get job details from database."""
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT job_id, company, job_title, resume_score,
                       description, location, level
                FROM jobs
                WHERE job_id = ?
            """, (job_id,))

            result = cursor.fetchone()
            conn.close()

            if not result:
                return {}

            job_id, company, title, score, description, location, level = result

            return {
                "job_id": str(job_id),
                "title": title or "Unknown Title",
                "company": company or "Unknown",
                "location": location or "Unknown",
                "level": level or "",
                "score": score or 0,
                "content": description or ""
            }

        except Exception as e:
            print(f"Error getting job {job_id} from database: {e}")
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
    
    def import_job(self, job_id: str, force: bool = False) -> str:
        """Import a specific job to local directory."""
        job_details = self.get_job_from_db(job_id)
        if not job_details:
            raise ValueError(f"Could not find job {job_id} in database")
        
        # Check if already imported
        current_status = self.tracker.get_job_status(job_id)
        if current_status in ["imported", "applying", "applied"] and not force:
            existing_dir = self.find_existing_job_dir(job_id)
            if existing_dir:
                print(f"Job {job_id} already imported to: {existing_dir}")
                return str(existing_dir)
        
        # Set up job directory using standardized setup
        job_dir_str = self.setup.setup_job_directory(
            job_details["company"],
            job_details["title"],
            force
        )
        job_dir = Path(job_dir_str)

        # (Directory already created by setup_job_directory)
        
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
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT jobs.job_id, jobs.resume_score, jobs.job_title,
                       COALESCE(job_tracking.status, 'new') as status
                FROM jobs
                LEFT JOIN job_tracking ON jobs.job_id = job_tracking.job_id
                LEFT JOIN company_ignore ON jobs.company = company_ignore.company
                WHERE jobs.created_at > date('now', '-7 days')
                  AND jobs.resume_score IS NOT NULL
                  AND (job_tracking.status IS NULL OR job_tracking.status IN ('new', 'reviewed', 'researching'))
                  AND company_ignore.company IS NULL
                ORDER BY jobs.resume_score DESC, jobs.created_at DESC
                LIMIT ?
            """, (limit,))

            results = cursor.fetchall()
            conn.close()

            return [(str(job_id), score, title, status) for job_id, score, title, status in results]

        except Exception as e:
            print(f"Error listing importable jobs: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Import jobs from database to local directory")
    parser.add_argument(
        "job_id",
        nargs="?",
        help="Job ID to import (or use --list to see available jobs)"
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
        importer = JobImporter(target_dir=args.target_dir, tracking_file=args.tracking_file)
        
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