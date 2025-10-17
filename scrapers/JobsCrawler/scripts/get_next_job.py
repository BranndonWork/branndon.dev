#!/usr/bin/env python3
"""
Script to filter and retrieve the next job to review from the jobs database.

Usage:
    python scripts/get_next_job.py [--limit N]
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_PATH = PROJECT_ROOT / "data" / "jobs.db"


def get_next_job(
    db_path: Path,
    source: str = "4dayweek.io",
    exclude_title_keywords: list[str] | None = None,
    include_title_keywords: list[str] | None = None,
    include_description_keywords: list[str] | None = None,
    limit: int = 1,
) -> list[dict]:
    exclude_title_keywords = exclude_title_keywords or []
    include_title_keywords = include_title_keywords or []
    include_description_keywords = include_description_keywords or []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT
            id,
            title,
            link,
            description,
            location,
            location_tags,
            pubdate,
            timestamp,
            status,
            notes
        FROM main_jobs
        WHERE link LIKE ?
          AND (status IS NULL OR status = 'new')
    """
    params = [f"%{source}%"]

    for keyword in exclude_title_keywords:
        query += " AND LOWER(title) NOT LIKE ?"
        params.append(f"%{keyword.lower()}%")

    if include_title_keywords:
        title_conditions = " OR ".join(["LOWER(title) LIKE ?" for _ in include_title_keywords])
        query += f" AND ({title_conditions})"
        for keyword in include_title_keywords:
            params.append(f"%{keyword.lower()}%")

    if include_description_keywords:
        desc_conditions = " OR ".join(["LOWER(description) LIKE ?" for _ in include_description_keywords])
        query += f" AND ({desc_conditions})"
        for keyword in include_description_keywords:
            params.append(f"%{keyword.lower()}%")

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Get the next job(s) to review from the database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/get_next_job.py --exclude-title manager
  python scripts/get_next_job.py --exclude-title manager --include-title senior --include-title engineer
  python scripts/get_next_job.py --include-title senior --include-desc python
  python scripts/get_next_job.py --exclude-title manager --limit 10
        """
    )
    parser.add_argument("--limit", type=int, default=1, help="Number of jobs to retrieve")
    parser.add_argument("--source", type=str, default="4dayweek.io", help="Filter by job source")
    parser.add_argument("--exclude-title", type=str, action="append", default=[], help="Keywords to exclude from titles")
    parser.add_argument("--include-title", type=str, action="append", default=[], help="Keywords in title (ANY match)")
    parser.add_argument("--include-desc", type=str, action="append", default=[], help="Keywords in description (ANY match)")
    parser.add_argument("--show-all", action="store_true", help="Show all matching jobs")
    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    if not DB_PATH.exists():
        result = {"status": "error", "message": f"Database not found at {DB_PATH}"}
        print(json.dumps(result, indent=2))
        sys.exit(1)

    limit = 999999 if args.show_all else args.limit
    jobs = get_next_job(
        db_path=DB_PATH,
        source=args.source,
        exclude_title_keywords=args.exclude_title,
        include_title_keywords=args.include_title,
        include_description_keywords=args.include_desc,
        limit=limit
    )

    result = {
        "status": "success" if jobs else "no_results",
        "count": len(jobs),
        "filters": {
            "source": args.source,
            "exclude_title": args.exclude_title,
            "include_title": args.include_title,
            "include_desc": args.include_desc
        },
        "jobs": jobs
    }

    print(json.dumps(result, indent=2))

    if jobs:
        print("\n📋 WORKFLOW NOTE: Once a job is selected, Claude Code must check location restrictions before researching", file=sys.stderr)
        print("   poetry run python scripts/check_job_location.py --job-id 123", file=sys.stderr)
        print("   poetry run python scripts/check_job_location.py --url https://4dayweek.io/remote-job/...", file=sys.stderr)


if __name__ == "__main__":
    main()
