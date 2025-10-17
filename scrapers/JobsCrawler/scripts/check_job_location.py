#!/usr/bin/env python3
"""
Check location restrictions for a job posting.

Usage:
    python scripts/check_job_location.py --url https://4dayweek.io/remote-job/...
    python scripts/check_job_location.py --job-id 431
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils.scrape_job_page import scrape_job_metadata


async def check_location(job_url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        metadata = await scrape_job_metadata(session, job_url)
        return {
            "status": "success",
            "url": job_url,
            "location_restriction": metadata["location_restriction"],
            "posted_date": metadata["posted_date"],
            "pto_days": metadata["pto_days"]
        }


def main():
    parser = argparse.ArgumentParser(
        description="Check location restrictions and metadata for a job posting",
        epilog="""
Examples:
  python scripts/check_job_location.py --url https://4dayweek.io/remote-job/backend-engineer-abc123
  python scripts/check_job_location.py --job-id 431
        """
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", type=str, help="Full URL to the job posting")
    group.add_argument("--job-id", type=int, help="Job ID from database")

    args = parser.parse_args()

    if args.job_id:
        import sqlite3
        db_path = Path(__file__).resolve().parent.parent / "data" / "jobs.db"
        if not db_path.exists():
            result = {"status": "error", "message": f"Database not found at {db_path}"}
            print(json.dumps(result, indent=2))
            sys.exit(1)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT link FROM main_jobs WHERE id = ?", (args.job_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            result = {"status": "error", "message": f"Job ID {args.job_id} not found"}
            print(json.dumps(result, indent=2))
            sys.exit(1)

        job_url = row[0]
    else:
        job_url = args.url

    result = asyncio.run(check_location(job_url))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
