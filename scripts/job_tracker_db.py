#!/usr/bin/env python3
"""
Database-based job tracker for import_job.py

This replaces the YAML-based job tracker functionality with direct database access.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add job-search-2025 path to import the database modules
job_search_path = Path("/Volumes/Storage/Dropbox/documents/job-search-2025")
sys.path.append(str(job_search_path))

from job_scraper.sqlite_wrapper import SQLiteProvider


class JobTrackerDB:
    """Database-based job tracker for job import functionality"""

    def __init__(self, tracking_file=None):
        """Initialize database connection (tracking_file ignored - for compatibility)"""
        self.db = SQLiteProvider()

    def get_job_status(self, job_id: str) -> str:
        """Get the current status of a job"""
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT status FROM job_tracking WHERE job_id = ?', (job_id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return result[0]
            else:
                return "new"  # Default status for jobs not yet tracked

        except Exception as e:
            print(f"Error getting job status for {job_id}: {e}")
            return "new"

    def update_job_status(self, job_id: str, status: str, notes: str = "", job_details: dict = None):
        """Update job status in the database"""
        try:
            # Extract details if provided
            title = job_details.get("title", "") if job_details else ""
            company = job_details.get("company", "") if job_details else ""
            location = job_details.get("location", "") if job_details else ""
            resume_score = job_details.get("score") if job_details else None

            # Prepare the record for bulk insert (which handles INSERT OR REPLACE)
            record = {
                'job_id': job_id,
                'status': status,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'notes': notes
            }

            # Add optional fields if they have values
            if title:
                record['title'] = title
            if company:
                record['company'] = company
            if location:
                record['location'] = location
            if resume_score:
                record['resume_score'] = resume_score

            # Use bulk_insert_job_tracking for consistency
            count = self.db.bulk_insert_job_tracking([record])

            if count > 0:
                print(f"Updated job {job_id} status to {status}")
                return True
            else:
                print(f"Failed to update job {job_id}")
                return False

        except Exception as e:
            print(f"Error updating job status for {job_id}: {e}")
            return False


class JobOperationsDB:
    """Database-based job operations for compatibility with import_job.py"""

    def __init__(self, storage):
        """Initialize with storage (unused but kept for compatibility)"""
        self.tracker = JobTrackerDB()

    def update_job_status(self, job_id: str, status: str, notes: str = "", title: str = None, company: str = None, location: str = None):
        """Update job status - compatibility method"""
        job_details = {}
        if title:
            job_details['title'] = title
        if company:
            job_details['company'] = company
        if location:
            job_details['location'] = location

        return self.tracker.update_job_status(job_id, status, notes, job_details)


class JobStorageDB:
    """Database-based job storage for compatibility with import_job.py"""

    def __init__(self, job_search_dir=None, central_tracking_file=None):
        """Initialize (parameters ignored but kept for compatibility)"""
        self.tracker = JobTrackerDB()

    def load_central_tracking(self) -> dict:
        """Load central tracking data - returns minimal structure for compatibility"""
        return {
            "schema_version": "2.0",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "description": "Database-based job tracking system",
            "jobs": {}  # Not needed since we query database directly
        }