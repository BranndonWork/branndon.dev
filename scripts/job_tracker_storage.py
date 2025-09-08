#!/usr/bin/env python3

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


class JobStorage:
    def __init__(self, job_search_dir: str = None, central_tracking_file: str = None):
        if not job_search_dir:
            self.job_search_dir = Path(__file__).parent.parent / "job-search"
        else:
            self.job_search_dir = Path(job_search_dir)
        
        if not central_tracking_file:
            self.central_tracking_file = Path(__file__).parent.parent / "data" / "job_tracking.yaml"
        else:
            self.central_tracking_file = Path(central_tracking_file)

    def load_central_tracking(self) -> Dict:
        if not self.central_tracking_file.exists():
            return {
                "schema_version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "description": "YAML-based job tracking system",
                "jobs": {}
            }
        
        try:
            with open(self.central_tracking_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading central tracking file: {e}")
            return {"jobs": {}}

    def save_central_tracking(self, data: Dict):
        try:
            self.central_tracking_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.central_tracking_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, 
                         allow_unicode=True, width=80)
        except Exception as e:
            print(f"Error saving central tracking file: {e}")

    def find_job_yaml_files(self) -> List[Path]:
        if not self.job_search_dir.exists():
            return []
        
        yaml_files = []
        for job_dir in self.job_search_dir.iterdir():
            if job_dir.is_dir():
                yaml_file = job_dir / "job-application.yaml"
                if yaml_file.exists():
                    yaml_files.append(yaml_file)
        
        return yaml_files

    def find_job_by_id(self, job_id: str) -> Optional[Path]:
        yaml_files = self.find_job_yaml_files()
        
        for yaml_file in yaml_files:
            try:
                data = self.load_yaml_file(yaml_file)
                if str(data.get('job_id', '')).strip() == str(job_id).strip():
                    return yaml_file
            except Exception as e:
                print(f"Error reading {yaml_file}: {e}")
                continue
        
        return None

    def load_yaml_file(self, file_path: Path) -> Dict:
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    def save_yaml_file(self, file_path: Path, data: Dict):
        try:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, 
                         allow_unicode=True, width=80)
        except Exception as e:
            print(f"Error saving {file_path}: {e}")

    def load_all_individual_jobs(self) -> List[Dict]:
        jobs = []
        yaml_files = self.find_job_yaml_files()
        
        for yaml_file in yaml_files:
            data = self.load_yaml_file(yaml_file)
            if data:
                data['_file_path'] = str(yaml_file)
                jobs.append(data)
        
        return jobs