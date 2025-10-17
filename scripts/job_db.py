#!/usr/bin/env python3
"""
Job Database Wrapper

A clean interface to the job tracking database that eliminates the need for
directory changes and inline Python code in command files.

Usage:
    poetry run python scripts/job_db.py next-job                           # Find next unprocessed job
    poetry run python scripts/job_db.py check-status [job_id]              # Check if job is processed
    poetry run python scripts/job_db.py update-status [job_id] [status] [notes]  # Update job status
    poetry run python scripts/job_db.py query [sql]                        # Run custom SQL query
    poetry run python scripts/job_db.py stats                              # Show job statistics
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add job-search-2025 path
job_search_path = Path("/Volumes/Storage/Dropbox/documents/job-search-2025")
sys.path.append(str(job_search_path))

from job_scraper.sqlite_wrapper import SQLiteProvider


class JobDB:
    def __init__(self):
        # Set the correct database path to match the original script
        import os

        os.environ["SQLITE_DB_PATH"] = str(job_search_path / "jobs_database.db")
        self.db = SQLiteProvider()

    def next_job(self):
        """Find the next highest-scoring unprocessed job, excluding ignored companies"""
        conn = self.db._get_connection()
        cursor = conn.cursor()

        query = """
        SELECT jobs.job_id, jobs.company, jobs.job_title, jobs.resume_score,
               jobs.created_at, jobs.description
        FROM jobs
        LEFT JOIN job_tracking ON jobs.job_id = job_tracking.job_id
        LEFT JOIN company_ignore ON jobs.company = company_ignore.company
        WHERE jobs.created_at > date('now', '-7 days')
          AND jobs.resume_score IS NOT NULL
          AND (job_tracking.job_id IS NULL OR job_tracking.status = 'new')
          AND company_ignore.company IS NULL
        ORDER BY jobs.resume_score DESC, jobs.created_at DESC
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            job_id, company, title, score, created_at, description = result
            print(f"job_id\tcompany\tjob_title\tresume_score\tcreated_at\tdescription")
            print(f"------------------------------------------------------------")
            print(f"{job_id}\t{company}\t{title}\t{score}\t{created_at}\t{description}")
            return True
        else:
            print("No unprocessed jobs found in the last 7 days (excluding ignored companies)")
            return False

    def check_status(self, job_id):
        """Check if a job is already processed"""
        conn = self.db._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT job_id, status FROM job_tracking WHERE job_id = ?", (job_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            print(f"job_id\tstatus")
            print(f"-----------")
            print(f"{result[0]}\t{result[1]}")
            return True
        else:
            print("No results found.")
            return False

    def update_status(self, job_id, status, notes=""):
        """Update job status in tracking database"""
        try:
            record = {
                "job_id": job_id,
                "status": status,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "notes": notes,
            }

            count = self.db.bulk_insert_job_tracking([record])

            if count > 0:
                print(f"Updated job {job_id} status to {status}")
                return True
            else:
                print(f"Failed to update job {job_id}")
                return False

        except Exception as e:
            print(f"Error updating job {job_id}: {e}")
            return False

    def query(self, sql):
        """Execute a custom SQL query"""
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)

            # Check if this is a modification query (INSERT, UPDATE, DELETE)
            is_modification = sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE"))

            if is_modification:
                conn.commit()
                affected_rows = cursor.rowcount
                print(f"Query executed successfully. {affected_rows} rows affected.")
            else:
                # Get column names for SELECT queries
                if cursor.description:
                    columns = [description[0] for description in cursor.description]
                    print("\t".join(columns))
                    print("-" * (len("\t".join(columns)) + 10))

                    # Print results
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            print("\t".join(str(cell) if cell is not None else "NULL" for cell in row))
                    else:
                        print("No results found.")
                else:
                    print("Query executed successfully.")

            conn.close()
            return True

        except Exception as e:
            print(f"Error executing query: {e}")
            return False

    def stats(self):
        """Show job tracking statistics"""
        conn = self.db._get_connection()
        cursor = conn.cursor()

        # Total jobs in tracking
        cursor.execute("SELECT COUNT(*) FROM job_tracking")
        total_tracked = cursor.fetchone()[0]

        # Jobs by status
        cursor.execute("SELECT status, COUNT(*) FROM job_tracking GROUP BY status ORDER BY COUNT(*) DESC")
        status_counts = cursor.fetchall()

        # Recent activity (last 7 days)
        cursor.execute(
            """
        SELECT COUNT(*) FROM job_tracking
        WHERE last_updated > date('now', '-7 days')
        """
        )
        recent_activity = cursor.fetchone()[0]

        # Ignored companies count
        cursor.execute("SELECT COUNT(*) FROM company_ignore")
        ignored_companies = cursor.fetchone()[0]

        conn.close()

        print("=== Job Tracking Statistics ===")
        print(f"Total tracked jobs: {total_tracked}")
        print(f"Recent activity (7 days): {recent_activity}")
        print(f"Ignored companies: {ignored_companies}")
        print("\nJobs by status:")
        for status, count in status_counts:
            print(f"  {status}: {count}")

    def add_ignored_company(self, company, reasons, research_source="Manual", job_id=None):
        """Add a company to the ignore list"""
        import json
        from datetime import date

        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            # Convert reasons list to JSON if it's a list
            if isinstance(reasons, list):
                reasons_json = json.dumps(reasons)
            else:
                reasons_json = json.dumps([reasons])

            # Handle job_ids_rejected
            job_ids_rejected = json.dumps([job_id] if job_id else [])

            cursor.execute("""
                INSERT OR REPLACE INTO company_ignore
                (company, date_added, reasons, research_source, job_ids_rejected)
                VALUES (?, ?, ?, ?, ?)
            """, (
                company,
                date.today().isoformat(),
                reasons_json,
                research_source,
                job_ids_rejected
            ))

            conn.commit()
            conn.close()

            print(f"Added {company} to ignore list")
            return True

        except Exception as e:
            print(f"Error adding {company} to ignore list: {e}")
            return False

    def list_ignored_companies(self):
        """List all ignored companies"""
        import json

        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT company, date_added, reasons, research_source
                FROM company_ignore
                ORDER BY date_added DESC
            """)

            results = cursor.fetchall()
            conn.close()

            if results:
                print("=== Ignored Companies ===")
                for company, date_added, reasons_json, research_source in results:
                    reasons = json.loads(reasons_json)
                    print(f"\n{company} (added: {date_added})")
                    print(f"Source: {research_source}")
                    print("Reasons:")
                    for reason in reasons:
                        print(f"  - {reason}")
            else:
                print("No companies in ignore list")

            return True

        except Exception as e:
            print(f"Error listing ignored companies: {e}")
            return False

    def check_company_ignored(self, company):
        """Check if a company is on the ignore list"""
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT company FROM company_ignore WHERE company = ?", (company,))
            result = cursor.fetchone()
            conn.close()

            return result is not None

        except Exception as e:
            print(f"Error checking company ignore status: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Job Database Wrapper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Next job command
    subparsers.add_parser("next-job", help="Find next unprocessed job")

    # Check status command
    check_parser = subparsers.add_parser("check-status", help="Check if job is processed")
    check_parser.add_argument("job_id", help="Job ID to check")

    # Update status command
    update_parser = subparsers.add_parser("update-status", help="Update job status")
    update_parser.add_argument("job_id", help="Job ID to update")
    update_parser.add_argument("status", help="New status (reviewed, applied, rejected, etc.)")
    update_parser.add_argument("notes", nargs="?", default="", help="Optional notes")

    # Custom query command
    query_parser = subparsers.add_parser("query", help="Run custom SQL query")
    query_parser.add_argument("sql", help="SQL query to execute")

    # Stats command
    subparsers.add_parser("stats", help="Show job statistics")

    # Ignore company commands
    ignore_parser = subparsers.add_parser("add-ignored-company", help="Add company to ignore list")
    ignore_parser.add_argument("company", help="Company name to ignore")
    ignore_parser.add_argument("reasons", nargs="+", help="Reasons to ignore this company")
    ignore_parser.add_argument("--source", default="Manual", help="Research source")
    ignore_parser.add_argument("--job-id", help="Job ID being rejected")

    subparsers.add_parser("list-ignored-companies", help="List all ignored companies")

    check_ignored_parser = subparsers.add_parser("check-company-ignored", help="Check if company is ignored")
    check_ignored_parser.add_argument("company", help="Company name to check")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    job_db = JobDB()

    try:
        if args.command == "next-job":
            job_db.next_job()
        elif args.command == "check-status":
            job_db.check_status(args.job_id)
        elif args.command == "update-status":
            job_db.update_status(args.job_id, args.status, args.notes)
        elif args.command == "query":
            job_db.query(args.sql)
        elif args.command == "stats":
            job_db.stats()
        elif args.command == "add-ignored-company":
            job_db.add_ignored_company(args.company, args.reasons, args.source, args.job_id)
        elif args.command == "list-ignored-companies":
            job_db.list_ignored_companies()
        elif args.command == "check-company-ignored":
            result = job_db.check_company_ignored(args.company)
            print(f"{args.company} is {'IGNORED' if result else 'NOT IGNORED'}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
