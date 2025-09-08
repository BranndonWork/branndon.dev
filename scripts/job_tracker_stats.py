#!/usr/bin/env python3

from typing import Dict
from job_tracker_storage import JobStorage


class JobStatistics:
    def __init__(self, storage: JobStorage):
        self.storage = storage
        self.valid_statuses = [
            "new", "reviewed", "researching", "imported", 
            "applying", "applied", "rejected", "interview"
        ]

    def get_statistics(self) -> Dict:
        central_data = self.storage.load_central_tracking()
        individual_files = self.storage.find_job_yaml_files()
        
        central_stats = self._count_central_jobs(central_data)
        individual_stats = self._count_individual_jobs(individual_files)
        
        return {
            'central_tracking': {
                'total_jobs': len(central_data.get("jobs", {})),
                'by_status': central_stats
            },
            'individual_files': {
                'total_jobs': len(individual_files),
                'by_status': individual_stats
            }
        }

    def _count_central_jobs(self, central_data: Dict) -> Dict[str, int]:
        stats = {status: 0 for status in self.valid_statuses}
        
        for job_data in central_data.get("jobs", {}).values():
            status = job_data.get('status', 'new')
            if status in stats:
                stats[status] += 1
        
        return stats

    def _count_individual_jobs(self, yaml_files: list) -> Dict[str, int]:
        stats = {status: 0 for status in self.valid_statuses}
        
        for yaml_file in yaml_files:
            try:
                data = self.storage.load_yaml_file(yaml_file)
                if data:
                    status = data.get('status', 'new')
                    if status in stats:
                        stats[status] += 1
            except:
                continue
        
        return stats

    def print_statistics(self, stats: Dict):
        print("\n📊 Job Tracking Statistics:")
        print("-" * 50)
        
        print("\n🗄️  Central Tracking:")
        print(f"   Total jobs: {stats['central_tracking']['total_jobs']}")
        for status, count in stats['central_tracking']['by_status'].items():
            if count > 0:
                print(f"   {status.capitalize()}: {count}")
        
        print("\n📁 Individual Files:")
        print(f"   Total jobs: {stats['individual_files']['total_jobs']}")
        for status, count in stats['individual_files']['by_status'].items():
            if count > 0:
                print(f"   {status.capitalize()}: {count}")

    def print_job_list(self, jobs: list):
        if not jobs:
            print("No jobs found")
            return
            
        print(f"\n{'Score':<6} {'Status':<12} {'Company':<25} {'Title':<40} {'Source':<10}")
        print("-" * 100)
        
        for job in jobs:
            print(f"{job['resume_score']:<6} {job['status']:<12} "
                  f"{job['company'][:24]:<25} {job['title'][:39]:<40} "
                  f"{job['source']:<10}")