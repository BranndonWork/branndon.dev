#!/usr/bin/env python3
"""
Interactive Job Processing Workflow
Main script for processing jobs from scraped data through to application.
"""

import os
import sys
import subprocess
from pathlib import Path
import json
import re

from job_tracker import JobTracker
from find_top_jobs import find_top_jobs, extract_job_score
from import_job import JobImporter
from research_company import CompanyResearcher


class JobProcessor:
    def __init__(self, source_dir: str, target_dir: str = None, tracking_file: str = None):
        """Initialize job processor."""
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir) if target_dir else Path.cwd() / "job-search"
        self.tracker = JobTracker(tracking_file)
        self.importer = JobImporter(str(source_dir), str(self.target_dir), tracking_file)
        self.researcher = CompanyResearcher()
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    def display_job_details(self, job_id: str) -> dict:
        """Display detailed job information."""
        job_file = self.source_dir / f"{job_id}.md"
        if not job_file.exists():
            print(f"❌ Job file not found: {job_file}")
            return {}
        
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key information
            title_match = re.search(r'---\\n\\n# (.+?)\\n', content)
            title = title_match.group(1) if title_match else "Unknown Title"
            
            company_match = re.search(r'\\*\\*Company\\*\\*:\\s*(.+)', content)
            company = company_match.group(1) if company_match else "Unknown"
            
            location_match = re.search(r'\\*\\*Location\\*\\*:\\s*(.+)', content)
            location = location_match.group(1) if location_match else "Unknown"
            
            level_match = re.search(r'\\*\\*Level\\*\\*:\\s*(.+)', content)
            level = level_match.group(1) if level_match else ""
            
            score_match = re.search(r'\\*\\*Resume Score\\*\\*:\\s*(\\d+)', content)
            score = int(score_match.group(1)) if score_match else 0
            
            # Extract job description (everything after "## Job Description")
            desc_match = re.search(r'## Job Description\\n\\n(.*?)(?=\\n##|$)', content, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else ""
            
            job_info = {
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "level": level,
                "score": score,
                "description": description,
                "full_content": content
            }
            
            # Display formatted job details
            print(f"\\n{'='*80}")
            print(f"🏢 {company}")
            print(f"📋 {title}")
            print(f"📍 {location}")
            if level:
                print(f"📊 Level: {level}")
            print(f"⭐ Score: {score}/100")
            print(f"🆔 Job ID: {job_id}")
            print(f"{'='*80}")
            
            # Show description preview
            if description:
                preview = description[:500]
                if len(description) > 500:
                    preview += "..."
                print(f"\\n📝 Job Description Preview:\\n{preview}")
            
            return job_info
            
        except Exception as e:
            print(f"❌ Error reading job file: {e}")
            return {}
    
    def get_user_decision(self, job_info: dict) -> str:
        """Get user decision on how to process the job."""
        print(f"\\n🤔 What would you like to do with this job?")
        print(f"  [s] Skip - not interested")
        print(f"  [r] Research company first")
        print(f"  [i] Import and proceed with application")
        print(f"  [d] Show full description")
        print(f"  [n] Next job (mark as reviewed)")
        print(f"  [q] Quit")
        
        while True:
            choice = input(f"\\n👉 Your choice [s/r/i/d/n/q]: ").lower().strip()
            
            if choice in ['s', 'skip']:
                return 'skip'
            elif choice in ['r', 'research']:
                return 'research'
            elif choice in ['i', 'import']:
                return 'import'
            elif choice in ['d', 'description', 'desc']:
                return 'description'
            elif choice in ['n', 'next']:
                return 'next'
            elif choice in ['q', 'quit']:
                return 'quit'
            else:
                print(f"❌ Invalid choice. Please enter s, r, i, d, n, or q")
    
    def show_full_description(self, job_info: dict):
        """Show the full job description."""
        print(f"\\n{'='*80}")
        print(f"FULL JOB DESCRIPTION: {job_info['title']} at {job_info['company']}")
        print(f"{'='*80}")
        print(job_info['description'])
        print(f"{'='*80}")
    
    def research_company_interactive(self, company_name: str) -> bool:
        """Interactive company research workflow."""
        print(f"\\n🔍 Starting company research for: {company_name}")
        
        # Ask for specific URLs to research
        print(f"\\n📋 Do you have specific URLs to research? (Glassdoor, Indeed, etc.)")
        print(f"Enter URLs one per line, or press Enter to skip:")
        
        urls = []
        while True:
            url = input(f"URL (or Enter to finish): ").strip()
            if not url:
                break
            if url.startswith('http'):
                urls.append(url)
            else:
                print(f"⚠️ Invalid URL: {url}")
        
        try:
            # Run company research
            report_file = self.researcher.research_company_full(company_name, urls)
            
            print(f"\\n📄 Research report generated: {report_file}")
            
            # Ask if user wants to view the report
            view = input(f"\\n👁️ View research report now? [y/N]: ").lower().strip()
            if view in ['y', 'yes']:
                if Path(report_file).exists():
                    with open(report_file, 'r') as f:
                        content = f.read()
                    print(f"\\n{'='*80}")
                    print(content)
                    print(f"{'='*80}")
            
            # Ask if research looks good
            proceed = input(f"\\n✅ Based on research, proceed with this company? [y/N]: ").lower().strip()
            return proceed in ['y', 'yes']
            
        except Exception as e:
            print(f"❌ Error during company research: {e}")
            proceed = input(f"\\n❓ Continue without research? [y/N]: ").lower().strip()
            return proceed in ['y', 'yes']
    
    def get_next_unprocessed_job(self) -> str:
        """Get the next highest-scoring unprocessed job."""
        try:
            # Get top unprocessed jobs
            jobs = find_top_jobs(
                str(self.source_dir),
                top_n=1,
                exclude_processed=True,
                tracking_file=str(self.tracker.tracking_file)
            )
            
            if jobs:
                return jobs[0][0]  # Return job_id
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error finding next job: {e}")
            return None
    
    def process_next_job(self) -> bool:
        """Process the next unprocessed job interactively."""
        # Get next job
        job_id = self.get_next_unprocessed_job()
        if not job_id:
            print(f"\\n🎉 No more unprocessed jobs found!")
            return False
        
        # Display job details
        job_info = self.display_job_details(job_id)
        if not job_info:
            return True  # Continue with next job
        
        # Get user decision
        while True:
            decision = self.get_user_decision(job_info)
            
            if decision == 'quit':
                return False
            
            elif decision == 'skip':
                self.tracker.update_job_status(job_id, "reviewed", "User skipped - not interested")
                print(f"✅ Marked job {job_id} as reviewed (skipped)")
                break
            
            elif decision == 'next':
                self.tracker.update_job_status(job_id, "reviewed", "User reviewed - moving to next")
                print(f"✅ Marked job {job_id} as reviewed")
                break
            
            elif decision == 'description':
                self.show_full_description(job_info)
                continue  # Show menu again
            
            elif decision == 'research':
                # Research company
                self.tracker.update_job_status(job_id, "researching", "Company research in progress")
                
                should_proceed = self.research_company_interactive(job_info['company'])
                
                if should_proceed:
                    print(f"\\n✅ Research completed - proceeding with import")
                    # Continue to import
                    decision = 'import'
                else:
                    print(f"\\n❌ Research indicated skip - marking as reviewed")
                    self.tracker.update_job_status(job_id, "reviewed", "Skipped after company research")
                    break
            
            if decision == 'import':
                try:
                    # Import the job
                    job_dir = self.importer.import_job(job_id)
                    
                    print(f"\\n🎯 Job successfully imported!")
                    print(f"Directory: {job_dir}")
                    print(f"\\n📋 Next steps:")
                    print(f"1. Review: {Path(job_dir) / 'job-posting.md'}")
                    print(f"2. Customize: {Path(job_dir) / 'customization-analysis.md'}")  
                    print(f"3. Generate resume using RESUME_GENERATION_COMPLETE.md workflow")
                    
                    # Ask if user wants to continue with more jobs
                    continue_processing = input(f"\\n▶️ Process another job? [Y/n]: ").lower().strip()
                    if continue_processing in ['n', 'no']:
                        return False
                    break
                    
                except Exception as e:
                    print(f"❌ Error importing job: {e}")
                    self.tracker.update_job_status(job_id, "reviewed", f"Import failed: {e}")
                    break
        
        return True  # Continue processing
    
    def run_interactive_session(self):
        """Run the main interactive job processing session."""
        print(f"\\n🚀 Interactive Job Processing Session")
        print(f"Source: {self.source_dir}")
        print(f"Target: {self.target_dir}")
        
        # Show statistics
        stats = self.tracker.get_statistics()
        print(f"\\n📊 Current Status:")
        print(f"  Total jobs: {stats['total_jobs']}")
        print(f"  New/unprocessed: {stats.get('new', 0)}")
        print(f"  Already reviewed: {stats.get('reviewed', 0)}")
        print(f"  Imported: {stats.get('imported', 0)}")
        
        # Process jobs one by one
        while True:
            if not self.process_next_job():
                break
        
        print(f"\\n👋 Session ended. Thanks for using the job processor!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive job processing workflow")
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
        "--job-id", 
        help="Process specific job ID instead of interactive mode"
    )
    
    args = parser.parse_args()
    
    try:
        processor = JobProcessor(args.source_dir, args.target_dir, args.tracking_file)
        
        if args.job_id:
            # Process specific job
            job_info = processor.display_job_details(args.job_id)
            if job_info:
                while True:
                    decision = processor.get_user_decision(job_info)
                    if decision == 'quit':
                        break
                    # Handle decision similar to interactive session
                    # (simplified for single job processing)
                    print(f"Decision: {decision}")
                    break
        else:
            # Run full interactive session
            processor.run_interactive_session()
    
    except KeyboardInterrupt:
        print(f"\\n\\n👋 Session interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())