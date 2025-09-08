#!/usr/bin/env python3

from datetime import datetime
from typing import Dict, Optional, List, Set
from job_tracker_storage import JobStorage


class JobOperations:
    def __init__(self, storage: JobStorage):
        self.storage = storage
        self.valid_statuses = [
            "new", "reviewed", "researching", "imported", 
            "applying", "applied", "rejected", "interview"
        ]

    def _format_note(self, existing_notes: str, new_note: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        formatted_note = f"[{timestamp}] {new_note}"
        
        if existing_notes:
            return f"{existing_notes}\\n\\n{formatted_note}"
        return formatted_note

    def get_processed_jobs(self, exclude_status: List[str] = None) -> Set[str]:
        if exclude_status is None:
            exclude_status = ["new"]
        
        central_data = self.storage.load_central_tracking()
        processed = set()
        
        for job_id, job_data in central_data.get("jobs", {}).items():
            status = job_data.get("status", "new")
            if status not in exclude_status:
                processed.add(job_id)
        
        return processed

    def update_job_status(self, job_id: str, status: str, notes: str = "", 
                         job_title: str = None, company: str = None, location: str = None):
        if status not in self.valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid: {self.valid_statuses}")
        
        central_data = self.storage.load_central_tracking()
        
        if job_id not in central_data.get("jobs", {}):
            central_data.setdefault("jobs", {})[job_id] = {}
        
        job_entry = central_data["jobs"][job_id]
        job_entry["status"] = status
        job_entry["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_entry["job_id"] = job_id
        
        if job_title:
            job_entry["title"] = job_title
        if company:
            job_entry["company"] = company
        if location:
            job_entry["location"] = location
        
        if notes:
            current_notes = job_entry.get('notes', '')
            job_entry['notes'] = self._format_note(current_notes, notes)
        
        self.storage.save_central_tracking(central_data)
        print(f"Updated job {job_id} to status: {status}")
        
        self._sync_individual_file(job_id, status, notes)
        return True

    def _sync_individual_file(self, job_id: str, status: str, notes: str):
        if status == "imported" or self.storage.find_job_by_id(job_id):
            individual_file = self.storage.find_job_by_id(job_id)
            if individual_file:
                try:
                    individual_data = self.storage.load_yaml_file(individual_file)
                    
                    individual_data['status'] = status
                    individual_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if notes:
                        current_notes = individual_data.get('notes', '')
                        individual_data['notes'] = self._format_note(current_notes, notes)
                    
                    self.storage.save_yaml_file(individual_file, individual_data)
                    print(f"Also updated individual YAML: {individual_file}")
                except Exception as e:
                    print(f"Error updating individual YAML file: {e}")

    def list_jobs(self, status: str = None, limit: int = 20, source: str = "all") -> List[Dict]:
        all_jobs = []
        
        if source in ["all", "central"]:
            all_jobs.extend(self._get_jobs_from_central(status))
        
        if source in ["all", "individual"]:
            all_jobs.extend(self._get_jobs_from_individual(status))
        
        unique_jobs = self._deduplicate_jobs(all_jobs)
        jobs_list = list(unique_jobs.values())
        jobs_list.sort(key=lambda x: x['resume_score'], reverse=True)
        return jobs_list[:limit]

    def _get_jobs_from_central(self, status: str = None) -> List[Dict]:
        jobs = []
        central_data = self.storage.load_central_tracking()
        
        for job_id, job_data in central_data.get("jobs", {}).items():
            if status and job_data.get('status', 'new') != status:
                continue
            
            job_info = {
                'job_id': job_id,
                'status': job_data.get('status', 'new'),
                'company': job_data.get('company', 'Unknown'),
                'title': job_data.get('title', 'Unknown'),
                'resume_score': job_data.get('resume_score', 0),
                'location': job_data.get('location', 'Unknown'),
                'source': 'central',
                'last_updated': job_data.get('last_updated', 'Unknown')
            }
            jobs.append(job_info)
        
        return jobs

    def _get_jobs_from_individual(self, status: str = None) -> List[Dict]:
        jobs = []
        individual_jobs = self.storage.load_all_individual_jobs()
        
        for data in individual_jobs:
            job_status = data.get('status', 'new')
            if status and job_status != status:
                continue
            
            job_info = {
                'job_id': data.get('job_id', 'Unknown'),
                'status': job_status,
                'company': data.get('company', 'Unknown'),
                'title': data.get('title', 'Unknown'),
                'resume_score': data.get('resume_score', 0),
                'location': data.get('location', 'Unknown'),
                'source': 'individual',
                'file_path': data.get('_file_path', ''),
                'last_updated': data.get('last_updated', 'Unknown')
            }
            jobs.append(job_info)
        
        return jobs

    def _deduplicate_jobs(self, all_jobs: List[Dict]) -> Dict[str, Dict]:
        unique_jobs = {}
        for job in all_jobs:
            job_id = job['job_id']
            if job_id not in unique_jobs or job['source'] == 'individual':
                unique_jobs[job_id] = job
        return unique_jobs