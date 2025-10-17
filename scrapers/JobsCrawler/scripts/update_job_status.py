#!/usr/bin/env python3
"""
Update job status in the JobsCrawler database.

Usage:
    python scripts/update_job_status.py [job_id] [status] [notes]
    python scripts/update_job_status.py --link [job_link] [status] [notes]
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_PATH = PROJECT_ROOT / "data" / "jobs.db"


def update_status_by_id(db_path: Path, job_id: int, status: str, notes: str = "") -> dict:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_notes = f"[{timestamp}] {notes}" if notes else f"[{timestamp}] Status updated"

        cursor.execute("""
            UPDATE main_jobs
            SET status = ?, notes = ?
            WHERE id = ?
        """, (status, full_notes, job_id))

        if cursor.rowcount == 0:
            conn.close()
            return {"status": "error", "message": f"No job found with ID: {job_id}"}

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "job_id": job_id,
            "new_status": status,
            "notes": notes
        }

    except Exception as e:
        return {"status": "error", "message": f"Error updating job {job_id}: {str(e)}"}


def update_status_by_link(db_path: Path, job_link: str, status: str, notes: str = "") -> dict:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_notes = f"[{timestamp}] {notes}" if notes else f"[{timestamp}] Status updated"

        cursor.execute("""
            UPDATE main_jobs
            SET status = ?, notes = ?
            WHERE link = ?
        """, (status, full_notes, job_link))

        if cursor.rowcount == 0:
            conn.close()
            return {"status": "error", "message": f"No job found with link: {job_link}"}

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "job_link": job_link,
            "new_status": status,
            "notes": notes
        }

    except Exception as e:
        return {"status": "error", "message": f"Error updating job: {str(e)}"}


def get_job_status(db_path: Path, job_id: int | None = None, job_link: str | None = None) -> dict:
    if not job_id and not job_link:
        return {"status": "error", "message": "Must provide either job_id or job_link"}

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if job_id:
            cursor.execute("""
                SELECT id, title, status, notes
                FROM main_jobs
                WHERE id = ?
            """, (job_id,))
        else:
            cursor.execute("""
                SELECT id, title, status, notes
                FROM main_jobs
                WHERE link = ?
            """, (job_link,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "status": "success",
                "job_id": result['id'],
                "title": result['title'],
                "job_status": result['status'] or 'new',
                "notes": result['notes']
            }
        else:
            return {"status": "error", "message": "No job found"}

    except Exception as e:
        return {"status": "error", "message": f"Error getting job status: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(
        description="Update job status in the JobsCrawler database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/update_job_status.py 42 reviewed "Not a good fit"
  python scripts/update_job_status.py --link "https://4dayweek.io/..." applied
  python scripts/update_job_status.py --check 42
        """
    )
    parser.add_argument("job_id", nargs="?", type=int, help="Job ID to update")
    parser.add_argument("status", nargs="?", help="New status (new, reviewed, applied, rejected)")
    parser.add_argument("notes", nargs="?", default="", help="Optional notes")
    parser.add_argument("--link", help="Update by job link instead of ID")
    parser.add_argument("--check", type=int, help="Check current status of job ID")
    parser.add_argument("--check-link", help="Check current status of job by link")

    args = parser.parse_args()

    if not DB_PATH.exists():
        result = {"status": "error", "message": f"Database not found at {DB_PATH}"}
        print(json.dumps(result, indent=2))
        sys.exit(1)

    if args.check:
        result = get_job_status(DB_PATH, job_id=args.check)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "success" else 1)

    if args.check_link:
        result = get_job_status(DB_PATH, job_link=args.check_link)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "success" else 1)

    if not args.status:
        result = {"status": "error", "message": "status is required"}
        print(json.dumps(result, indent=2))
        sys.exit(1)

    valid_statuses = ["new", "reviewed", "applied", "rejected"]
    if args.status not in valid_statuses:
        result = {
            "status": "error",
            "message": f"Invalid status '{args.status}'",
            "valid_statuses": valid_statuses
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    if args.link:
        result = update_status_by_link(DB_PATH, args.link, args.status, args.notes)
    elif args.job_id:
        result = update_status_by_id(DB_PATH, args.job_id, args.status, args.notes)
    else:
        result = {"status": "error", "message": "Must provide either job_id or --link"}

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
