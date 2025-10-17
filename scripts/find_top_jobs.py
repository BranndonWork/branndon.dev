#!/usr/bin/env python3
"""
Script to find the highest scoring jobs from scraped job data.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Set
import argparse

# Add job-search-2025 path to import the database modules
job_search_path = Path("/Volumes/Storage/Dropbox/documents/job-search-2025")
sys.path.append(str(job_search_path))

from job_scraper.sqlite_wrapper import SQLiteProvider


def extract_job_score(file_path: Path) -> Optional[Tuple[str, int, str]]:
    """Extract job ID, resume score, and job title from a job markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Job ID
        job_id_match = re.search(r'\*\*Job ID\*\*:\s*`([^`]+)`', content)
        job_id = job_id_match.group(1) if job_id_match else file_path.stem
        
        # Extract Resume Score
        score_match = re.search(r'\*\*Resume Score\*\*:\s*(\d+)', content)
        if not score_match:
            return None
        score = int(score_match.group(1))
        
        # Extract Job Title (first heading after the metadata section)
        title_match = re.search(r'---\n\n# (.+?)\n', content)
        title = title_match.group(1) if title_match else "Unknown Title"
        
        return (job_id, score, title)
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def load_tracking_data_from_db() -> dict:
    """Load job tracking data from database."""
    try:
        # Set the correct database path
        os.environ['SQLITE_DB_PATH'] = str(job_search_path / "jobs_database.db")
        db = SQLiteProvider()

        conn = db._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT job_id, status FROM job_tracking')
        results = cursor.fetchall()
        conn.close()

        # Convert to the expected format
        jobs = {}
        for job_id, status in results:
            jobs[job_id] = {"status": status}

        return {"jobs": jobs}
    except Exception as e:
        print(f"Error loading tracking data from database: {e}")
        return {"jobs": {}}


def get_processed_jobs(tracking_data: dict, exclude_status: List[str] = None) -> Set[str]:
    """Get set of job IDs that have been processed."""
    if exclude_status is None:
        exclude_status = ["new"]
    
    processed = set()
    for job_id, job_data in tracking_data.get("jobs", {}).items():
        status = job_data.get("status", "new")
        if status not in exclude_status:
            processed.add(job_id)
    return processed


def find_top_jobs(jobs_dir: str, top_n: int = 10, exclude_processed: bool = True,
                  tracking_file: str = None, status_filter: str = None) -> List[Tuple[str, int, str]]:
    """Find the top N jobs by resume score.

    Args:
        jobs_dir: Directory containing job markdown files
        top_n: Number of top jobs to return
        exclude_processed: Whether to exclude already processed jobs
        tracking_file: Ignored - kept for compatibility, uses database
        status_filter: Only include jobs with this status
    """
    jobs_path = Path(jobs_dir)
    if not jobs_path.exists():
        raise FileNotFoundError(f"Jobs directory not found: {jobs_dir}")

    # Load tracking data from database if filtering is requested
    processed_jobs = set()
    tracking_data = {}
    if exclude_processed or status_filter:
        tracking_data = load_tracking_data_from_db()
        if exclude_processed:
            processed_jobs = get_processed_jobs(tracking_data)
    
    job_scores = []
    
    for file_path in jobs_path.glob("*.md"):
        result = extract_job_score(file_path)
        if result:
            job_id, score, title = result
            
            # Skip processed jobs if requested
            if exclude_processed and job_id in processed_jobs:
                continue
            
            # Filter by status if requested
            if status_filter:
                job_status = tracking_data.get("jobs", {}).get(job_id, {}).get("status", "new")
                if job_status != status_filter:
                    continue
            
            job_scores.append(result)
    
    # Sort by score (highest first)
    job_scores.sort(key=lambda x: x[1], reverse=True)
    
    return job_scores[:top_n]


def display_jobs(jobs: List[Tuple[str, int, str]], show_details: bool = False, jobs_dir: str = None):
    """Display jobs in a formatted table.
    
    Args:
        jobs: List of (job_id, score, title) tuples
        show_details: Whether to show full job descriptions
        jobs_dir: Directory containing job files (needed for show_details)
    """
    print(f"{'Rank':<5} {'Score':<6} {'Job ID':<12} {'Title':<50}")
    print("-" * 80)
    
    for i, (job_id, score, title) in enumerate(jobs, 1):
        # Truncate title if too long
        display_title = title[:47] + "..." if len(title) > 50 else title
        print(f"{i:<5} {score:<6} {job_id:<12} {display_title:<50}")
        
        # Show job details if requested
        if show_details and jobs_dir:
            job_file = Path(jobs_dir) / f"{job_id}.md"
            if job_file.exists():
                try:
                    with open(job_file, 'r') as f:
                        content = f.read()
                    # Extract company and location
                    company_match = re.search(r'\*\*Company\*\*:\s*(.+)', content)
                    location_match = re.search(r'\*\*Location\*\*:\s*(.+)', content)
                    company = company_match.group(1) if company_match else "Unknown"
                    location = location_match.group(1) if location_match else "Unknown"
                    print(f"      Company: {company}")
                    print(f"      Location: {location}")
                    print("      ---")
                except Exception:
                    pass


def main():
    parser = argparse.ArgumentParser(description="Find top jobs by resume score")
    parser.add_argument(
        "--jobs-dir", 
        default="/Volumes/Storage/Dropbox/documents/job-search-2025/data/jobs",
        help="Directory containing job markdown files"
    )
    parser.add_argument(
        "--top", 
        type=int, 
        default=10,
        help="Number of top jobs to display (default: 10)"
    )
    parser.add_argument(
        "--include-processed",
        action="store_true",
        help="Include jobs that have already been processed (default: exclude processed)"
    )
    parser.add_argument(
        "--tracking-file",
        help="Ignored - kept for compatibility (now uses database)"
    )
    parser.add_argument(
        "--status", 
        help="Only show jobs with this status (new, reviewed, imported, etc.)"
    )
    parser.add_argument(
        "--show-details", 
        action="store_true",
        help="Show additional job details (company, location)"
    )
    
    args = parser.parse_args()
    
    try:
        top_jobs = find_top_jobs(
            args.jobs_dir,
            args.top,
            exclude_processed=not args.include_processed,  # Flip the logic
            tracking_file=args.tracking_file,
            status_filter=args.status
        )
        
        if not top_jobs:
            print("No jobs with scores found.")
            return
        
        print(f"\nTop {len(top_jobs)} Jobs by Resume Score:\n")
        display_jobs(top_jobs, show_details=args.show_details, jobs_dir=args.jobs_dir)
        
        all_jobs = list(Path(args.jobs_dir).glob('*.md'))
        jobs_with_scores = [f for f in all_jobs if extract_job_score(f)]
        
        print(f"\nTotal jobs analyzed: {len(all_jobs)}")
        print(f"Jobs with scores: {len(jobs_with_scores)}")
        
        # Show filtering stats if applicable
        if not args.include_processed or args.status:
            try:
                tracking_data = load_tracking_data_from_db()
                processed_count = len(get_processed_jobs(tracking_data))
                print(f"Processed jobs: {processed_count}")
                if not args.include_processed:
                    print(f"Unprocessed jobs: {len(jobs_with_scores) - processed_count}")
            except Exception as e:
                print(f"Warning: Could not load tracking data: {e}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()