#!/usr/bin/env python3
"""
Clean up legacy template files after YAML migration.
Focused on removing old files only - requires YAML files to exist first.
"""

import argparse
from pathlib import Path


def get_legacy_files_to_remove() -> list:
    """Return list of legacy template files that can be safely removed."""
    return [
        "customization-analysis.md",
        "application-tracking.md", 
        "interview-prep.md"
    ]


def analyze_job_directory(job_dir: Path) -> dict:
    """Analyze job directory to determine what can be cleaned up."""
    yaml_file = job_dir / "job-application.yaml"
    legacy_files = get_legacy_files_to_remove()
    
    analysis = {
        "has_yaml": yaml_file.exists(),
        "legacy_files_present": [],
        "keep_files": [],
        "can_cleanup": False
    }
    
    # Check which legacy files exist
    for filename in legacy_files:
        file_path = job_dir / filename
        if file_path.exists():
            analysis["legacy_files_present"].append(filename)
    
    # Always keep these critical files
    keep_files = ["job-posting.md", "cover-letter.txt", "linkedin-url.txt"]
    for filename in keep_files:
        file_path = job_dir / filename
        if file_path.exists():
            analysis["keep_files"].append(filename)
    
    # Can cleanup if YAML exists and has legacy files
    analysis["can_cleanup"] = analysis["has_yaml"] and len(analysis["legacy_files_present"]) > 0
    
    return analysis


def cleanup_job_directory(job_dir: Path, dry_run: bool = False) -> dict:
    """Clean up legacy files in a single job directory."""
    analysis = analyze_job_directory(job_dir)
    
    result = {
        "success": False,
        "files_removed": [],
        "files_kept": analysis["keep_files"],
        "error": None
    }
    
    if not analysis["has_yaml"]:
        result["error"] = "No YAML file found - run create_yaml_from_jobs.py first"
        return result
    
    if not analysis["can_cleanup"]:
        result["error"] = "No legacy files to remove"
        return result
    
    # Remove legacy files
    for filename in analysis["legacy_files_present"]:
        file_path = job_dir / filename
        
        if dry_run:
            result["files_removed"].append(filename)
        else:
            try:
                file_path.unlink()
                result["files_removed"].append(filename)
                print(f"    🗑️  Removed: {filename}")
            except Exception as e:
                result["error"] = f"Failed to remove {filename}: {e}"
                return result
    
    result["success"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description="Clean up legacy template files after YAML migration")
    parser.add_argument(
        "--job-search-dir",
        default="./job-search",
        help="Path to job-search directory (default: ./job-search)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what files would be removed without making changes"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Remove files even without confirmation"
    )
    
    args = parser.parse_args()
    job_search_dir = Path(args.job_search_dir)
    
    if not job_search_dir.exists():
        print(f"Job search directory not found: {job_search_dir}")
        return 1
    
    job_dirs = [d for d in job_search_dir.iterdir() if d.is_dir()]
    if not job_dirs:
        print("No job directories found")
        return 1
    
    print(f"🧹 Legacy File Cleanup")
    print(f"Directory: {job_search_dir.absolute()}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be removed")
    
    # Analyze all directories first
    cleanup_candidates = []
    already_clean = []
    missing_yaml = []
    
    for job_dir in sorted(job_dirs):
        analysis = analyze_job_directory(job_dir)
        
        if not analysis["has_yaml"]:
            missing_yaml.append(job_dir.name)
        elif analysis["can_cleanup"]:
            cleanup_candidates.append((job_dir, analysis))
        else:
            already_clean.append(job_dir.name)
    
    # Report analysis
    print(f"\\n📊 Analysis:")
    print(f"   Cleanup candidates: {len(cleanup_candidates)}")
    print(f"   Already clean: {len(already_clean)}")
    print(f"   Missing YAML: {len(missing_yaml)}")
    
    if missing_yaml:
        print(f"\\n⚠️  Directories missing YAML files:")
        for name in missing_yaml[:5]:  # Show first 5
            print(f"     {name}")
        if len(missing_yaml) > 5:
            print(f"     ... and {len(missing_yaml) - 5} more")
        print("   Run: poetry run python scripts/create_yaml_from_jobs.py")
    
    if not cleanup_candidates:
        print("\\n✅ Nothing to clean up!")
        return 0
    
    # Show what will be cleaned
    print(f"\\n🗑️  Files to remove from {len(cleanup_candidates)} directories:")
    total_files = 0
    for job_dir, analysis in cleanup_candidates[:3]:  # Show first 3 examples
        print(f"   {job_dir.name}: {', '.join(analysis['legacy_files_present'])}")
        total_files += len(analysis['legacy_files_present'])
    
    if len(cleanup_candidates) > 3:
        for job_dir, analysis in cleanup_candidates[3:]:
            total_files += len(analysis['legacy_files_present'])
        print(f"   ... and {len(cleanup_candidates) - 3} more directories")
    
    print(f"\\n📈 Total files to remove: {total_files}")
    
    # Confirmation (unless dry-run or force)
    if not args.dry_run and not args.force:
        response = input("\\n❓ Proceed with cleanup? (y/N): ").lower().strip()
        if response != 'y':
            print("❌ Cleanup cancelled")
            return 0
    
    # Perform cleanup
    print("\\n🧹 Cleaning up...")
    success_count = 0
    error_count = 0
    
    for job_dir, analysis in cleanup_candidates:
        print(f"Processing: {job_dir.name}")
        result = cleanup_job_directory(job_dir, args.dry_run)
        
        if result["success"]:
            if args.dry_run:
                print(f"  📝 Would remove: {', '.join(result['files_removed'])}")
            else:
                print(f"  ✅ Removed {len(result['files_removed'])} files")
            success_count += 1
        else:
            print(f"  ❌ {result['error']}")
            error_count += 1
    
    # Summary
    print(f"\\n🏁 Cleanup Summary:")
    print(f"   Successful: {success_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total: {len(cleanup_candidates)}")
    
    if not args.dry_run and success_count > 0:
        print(f"\\n✨ Cleanup complete! Job directories now use YAML-first workflow.")
        print(f"   Use: poetry run python scripts/job_tracker_yaml.py list")
    
    return 0


if __name__ == "__main__":
    exit(main())