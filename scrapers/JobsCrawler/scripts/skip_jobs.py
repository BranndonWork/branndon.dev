#!/usr/bin/env python3
"""
Skip multiple jobs by marking them as reviewed.

Usage:
    python scripts/skip_jobs.py --ids 348 349 350
    python scripts/skip_jobs.py --ids 348 349 --reason "Location restriction"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_job_status import update_status_by_id, DB_PATH


def skip_multiple_jobs(job_ids: list[int], reason: str = "Auto-skipped") -> dict:
    results = []
    success_count = 0
    error_count = 0

    for job_id in job_ids:
        result = update_status_by_id(DB_PATH, job_id, "reviewed", reason)
        results.append(result)

        if result["status"] == "success":
            success_count += 1
        else:
            error_count += 1

    return {
        "status": "success" if error_count == 0 else "partial",
        "total": len(job_ids),
        "success": success_count,
        "errors": error_count,
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(
        description="Skip multiple jobs by marking them as reviewed",
        epilog="""
Examples:
  python scripts/skip_jobs.py --ids 444 443 441 440
  python scripts/skip_jobs.py --ids 444 443 --reason "Non-engineering role"
        """
    )
    parser.add_argument("--ids", type=int, nargs="+", required=True, help="Job IDs to skip")
    parser.add_argument("--reason", type=str, default="Auto-skipped", help="Reason for skipping")

    args = parser.parse_args()

    if not DB_PATH.exists():
        result = {"status": "error", "message": f"Database not found at {DB_PATH}"}
        print(json.dumps(result, indent=2))
        sys.exit(1)

    result = skip_multiple_jobs(args.ids, args.reason)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
