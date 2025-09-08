#!/usr/bin/env python3

"""
Update YAML from Files - Smart Job Import Tool

Reads all relevant files in a job directory and creates/updates a comprehensive 
job-application.yaml file with proper structure.

Usage:
    python -m scripts.update_yaml_from_files job-search/Company-JobTitle
    python -m scripts.update_yaml_from_files --all  # Update all jobs
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class JobFileProcessor:
    def __init__(self, job_dir: Path):
        self.job_dir = Path(job_dir)
        self.data = {}
        
    def process_all_files(self) -> Dict[str, Any]:
        """Process all relevant files and create structured YAML data."""
        print(f"Processing job directory: {self.job_dir}")
        
        # Start with basic structure
        self.data = self._create_base_structure()
        
        # Process each file type
        self._process_job_posting()
        self._process_customization_analysis()
        self._process_cover_letter()
        self._process_application_tracking()
        self._process_linkedin_url()
        
        # Add file references for human-readable content
        self._add_file_references()
        
        return self.data
    
    def _create_base_structure(self) -> Dict[str, Any]:
        """Create the basic YAML structure."""
        return {
            'job_id': '',
            'status': 'imported',
            'company': '',
            'title': '',
            'location': 'TBD',
            'level': '',
            'resume_score': 0,
            'linkedin_url': '',
            'application_timeline': {
                'scraped': 'TBD',
                'imported': datetime.now().strftime('%Y-%m-%d'),
                'applied': 'TBD',
                'response_deadline': 'TBD'
            },
            'job_details': {
                'tech_stack': [],
                'key_requirements': '',
                'compensation': {
                    'salary_range': 'Not specified',
                    'benefits': ''
                }
            },
            'my_match': {
                'strengths': [],
                'learning_opportunities': []
            },
            'company_research': {
                'file': './company-research-report.md',
                'summary': 'Research data in external file'
            },
            'application_materials': {
                'resume_pdf': '',
                'cover_letter_pdf': '',
                'ats_resume_json': ''
            },
            'cover_letter_approach': '',
            'notes': '',
            'follow_up': {
                'next_action': '',
                'check_date': 'TBD',
                'backup_plan': ''
            },
            'interview_prep': {
                'file': './interview-prep.md',
                'summary': 'Interview preparation in external file'
            },
            'decision_factors': {
                'pros': [],
                'cons': [],
                'verdict': ''
            }
        }
    
    def _process_job_posting(self):
        """Extract data from job-posting.md."""
        posting_file = self.job_dir / 'job-posting.md'
        if not posting_file.exists():
            return
            
        content = posting_file.read_text()
        
        # Extract job metadata
        if match := re.search(r'\*\*Job ID\*\*: `([^`]+)`', content):
            self.data['job_id'] = match.group(1)
            
        if match := re.search(r'\*\*Resume Score\*\*: (\d+)', content):
            self.data['resume_score'] = int(match.group(1))
            
        # Extract basic job info  
        if match := re.search(r'^# (.+)$', content, re.MULTILINE):
            self.data['title'] = match.group(1).strip()
            
        if match := re.search(r'\*\*Company\*\*: (.+)', content):
            self.data['company'] = match.group(1).strip()
            
        if match := re.search(r'\*\*Location\*\*: (.+)', content):
            self.data['location'] = match.group(1).strip()
            
        if match := re.search(r'\*\*Level\*\*: (.+)', content):
            self.data['level'] = match.group(1).strip()
            
        # Extract scraped date
        if match := re.search(r'\*\*Scraped At\*\*: (.+)', content):
            self.data['application_timeline']['scraped'] = match.group(1).strip()
            
        # Extract tech stack and requirements from job description
        self._extract_tech_requirements(content)
    
    def _extract_tech_requirements(self, content: str):
        """Extract technology stack and requirements from job posting."""
        # Common technology patterns
        tech_patterns = [
            r'Python', r'Django', r'Flask', r'JavaScript', r'React', r'Node\.js',
            r'AWS', r'Azure', r'GCP', r'Docker', r'Kubernetes', r'MongoDB',
            r'PostgreSQL', r'Redis', r'GraphQL', r'REST', r'API',
            r'Machine Learning', r'AI', r'TensorFlow', r'PyTorch'
        ]
        
        found_tech = []
        for pattern in tech_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                # Clean up the match
                clean_tech = re.sub(r'\.js', '.js', pattern)
                clean_tech = re.sub(r'\\\.', '.', clean_tech)
                if clean_tech not in found_tech:
                    found_tech.append(clean_tech)
        
        self.data['job_details']['tech_stack'] = found_tech
        
        # Extract key requirements section
        if match := re.search(r'## Job Description\s*\n---\s*\n(.+?)(?=\n##|\n---|\Z)', content, re.DOTALL):
            requirements = match.group(1).strip()
            # Clean up the requirements text
            requirements = re.sub(r'\n\s*\n', '\n', requirements)
            self.data['job_details']['key_requirements'] = requirements
    
    def _process_customization_analysis(self):
        """Extract matching strengths from customization analysis."""
        analysis_file = self.job_dir / 'customization-analysis.md'
        if not analysis_file.exists():
            return
            
        content = analysis_file.read_text()
        
        # Extract strengths and gaps
        strengths = []
        learning_opps = []
        
        # Look for gap analysis section
        if gap_match := re.search(r'### Gap Analysis\s*\n\*\*Requirements I DON\'T have.*?\n(.+?)(?=\n##|\Z)', content, re.DOTALL):
            gap_text = gap_match.group(1)
            # Convert gaps to learning opportunities
            for line in gap_text.split('\n'):
                if line.strip().startswith('- '):
                    gap = line.strip()[2:].split(':')[0]
                    learning_opps.append(f"Learning {gap}")
        
        # Extract matching experience section
        if match_match := re.search(r'### My Matching Experience.*?\n(.+?)(?=\n###|\Z)', content, re.DOTALL):
            match_text = match_match.group(1)
            for line in match_text.split('\n'):
                if line.strip().startswith('- '):
                    strength = line.strip()[2:]
                    strengths.append(strength)
        
        if strengths:
            self.data['my_match']['strengths'] = strengths
        if learning_opps:
            self.data['my_match']['learning_opportunities'] = learning_opps
    
    def _process_cover_letter(self):
        """Extract cover letter approach."""
        cover_file = self.job_dir / 'cover-letter.txt'
        if not cover_file.exists():
            return
            
        content = cover_file.read_text().strip()
        if content:
            # Create approach summary from cover letter
            approach = f"Emphasize relevant experience based on cover letter content"
            self.data['cover_letter_approach'] = approach
    
    def _process_application_tracking(self):
        """Extract application status from tracking file."""
        tracking_file = self.job_dir / 'application-tracking.md'
        if not tracking_file.exists():
            return
            
        content = tracking_file.read_text()
        
        # Look for status updates
        if 'applied' in content.lower():
            self.data['status'] = 'applied'
        elif 'interview' in content.lower():
            self.data['status'] = 'interview'
    
    def _process_linkedin_url(self):
        """Extract LinkedIn URL."""
        url_file = self.job_dir / 'linkedin-url.txt'
        if url_file.exists():
            url = url_file.read_text().strip()
            if url:
                self.data['linkedin_url'] = url
    
    def _add_file_references(self):
        """Add references to external files."""
        # Update application materials paths
        job_name = self.job_dir.name
        self.data['application_materials'] = {
            'resume_pdf': f'./{job_name}-Resume.pdf',
            'cover_letter_pdf': f'./{job_name}-CoverLetter.pdf',
            'ats_resume_json': f'./resume-branndon-coelho-{job_name.lower().replace("-", "-")}-ats.json'
        }
        
        # Add notes about migration
        self.data['notes'] = f'Migrated from existing job directory on {datetime.now().strftime("%Y-%m-%d")}. External files contain detailed research and prep materials.'
        
        # Set follow-up actions
        self.data['follow_up']['next_action'] = 'Review external files and complete any remaining research'
        self.data['follow_up']['check_date'] = (datetime.now().strftime('%Y-%m-') + str(int(datetime.now().strftime('%d')) + 7).zfill(2))

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.update_yaml_from_files <job_directory>")
        print("       python -m scripts.update_yaml_from_files --all")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        # Process all job directories
        job_search_dir = Path('job-search')
        for job_dir in job_search_dir.iterdir():
            if job_dir.is_dir() and not job_dir.name.startswith('.'):
                try:
                    processor = JobFileProcessor(job_dir)
                    data = processor.process_all_files()
                    
                    # Write YAML file
                    yaml_file = job_dir / 'job-application.yaml'
                    with open(yaml_file, 'w') as f:
                        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                    
                    print(f"✅ Updated {job_dir.name}")
                    
                except Exception as e:
                    print(f"❌ Failed to process {job_dir.name}: {e}")
    else:
        # Process single directory
        job_dir = Path(sys.argv[1])
        if not job_dir.exists():
            print(f"Directory not found: {job_dir}")
            sys.exit(1)
        
        processor = JobFileProcessor(job_dir)
        data = processor.process_all_files()
        
        # Write YAML file
        yaml_file = job_dir / 'job-application.yaml'
        with open(yaml_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✅ Updated {yaml_file}")

if __name__ == '__main__':
    main()