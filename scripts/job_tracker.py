#!/usr/bin/env python3

import argparse
from pathlib import Path
from job_tracker_storage import JobStorage
from job_tracker_operations import JobOperations
from job_tracker_stats import JobStatistics


def query_jobs_yq_examples(job_search_dir: Path, central_file: Path):
    job_dir = str(job_search_dir)
    central_file_str = str(central_file)
    
    examples = f"""
📊 YAML Job Query Examples:

🗄️  CENTRAL TRACKING FILE QUERIES ({central_file_str}):

# Show all reviewed jobs
yq '.jobs | to_entries | map(select(.value.status == "reviewed")) | from_entries' {central_file_str}

# Show all processed jobs (not new)
yq '.jobs | to_entries | map(select(.value.status != "new")) | from_entries' {central_file_str}

# Count jobs by status
yq '.jobs | group_by(.status) | map({{status: .[0].status, count: length}})' {central_file_str}

# Jobs updated recently
yq '.jobs | to_entries | map(select(.value.last_updated | test("2025-09"))) | from_entries' {central_file_str}

📁 INDIVIDUAL JOB FILE QUERIES ({job_dir}/*/job-application.yaml):

# Show all applied jobs
yq 'select(.status == "applied")' {job_dir}/*/job-application.yaml

# Find jobs by company
yq 'select(.company == "Files.com")' {job_dir}/*/job-application.yaml  

# High-scoring unprocessed jobs
yq 'select(.resume_score > 90 and .status == "new")' {job_dir}/*/job-application.yaml

# Show tech stacks for all jobs
yq '.company + ": " + (.job_details.tech_stack | join(", "))' {job_dir}/*/job-application.yaml

🔍 Using ripgrep for simple queries:

# All Ruby jobs (central file)
rg "Ruby" {central_file_str}

# High-scoring jobs (individual files)
rg "resume_score: 9[0-9]" {job_dir}/*/job-application.yaml

# Jobs with specific benefits
rg -A3 "benefits:" {job_dir}/*/job-application.yaml
    """
    print(examples)


def main():
    parser = argparse.ArgumentParser(description="YAML-based job tracking")
    parser.add_argument("--job-search-dir", help="Path to job-search directory")
    parser.add_argument("--central-file", help="Path to central tracking file")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    status_parser = subparsers.add_parser("status", help="Show job statistics")
    
    list_parser = subparsers.add_parser("list", help="List jobs")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--limit", type=int, default=20, help="Limit results")
    list_parser.add_argument("--source", choices=["all", "central", "individual"], 
                           default="all", help="Data source to query")
    
    update_parser = subparsers.add_parser("update", help="Update job status")
    update_parser.add_argument("job_id", help="Job ID to update")
    update_parser.add_argument("status", help="New status")
    update_parser.add_argument("--notes", default="", help="Optional notes")
    update_parser.add_argument("--title", help="Job title (for new entries)")
    update_parser.add_argument("--company", help="Company name (for new entries)")
    update_parser.add_argument("--location", help="Location (for new entries)")
    
    query_parser = subparsers.add_parser("query", help="Show yq query examples")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    storage = JobStorage(args.job_search_dir, args.central_file)
    operations = JobOperations(storage)
    stats = JobStatistics(storage)
    
    try:
        if args.command == "status":
            statistics = stats.get_statistics()
            stats.print_statistics(statistics)
        
        elif args.command == "list":
            jobs = operations.list_jobs(args.status, args.limit, args.source)
            stats.print_job_list(jobs)
        
        elif args.command == "update":
            operations.update_job_status(args.job_id, args.status, args.notes,
                                       args.title, args.company, args.location)
        
        elif args.command == "query":
            query_jobs_yq_examples(storage.job_search_dir, storage.central_tracking_file)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()