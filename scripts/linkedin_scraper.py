#!/usr/bin/env python3
"""
LinkedIn Job Scraper
Fetches and parses LinkedIn job postings
"""

import argparse
import requests
import re
import html
from pathlib import Path
from fake_useragent import UserAgent


def clean_html(text):
    """Remove HTML tags and decode entities"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text


def extract_job_details(html_content: str, job_id: str):
    """Extract structured job details from HTML"""
    # Extract title
    title_match = re.search(r'<h2 class="top-card-layout__title[^"]*">([^<]+)</h2>', html_content)
    title = title_match.group(1).strip() if title_match else "Unknown Title"

    # Extract company
    company_match = re.search(r'<a class="topcard__org-name-link[^>]*>\s*([^<]+)\s*</a>', html_content)
    company = company_match.group(1).strip() if company_match else "Unknown Company"

    # Extract location
    location_match = re.search(r'<span class="topcard__flavor topcard__flavor--bullet">\s*([^<]+)\s*</span>', html_content)
    location = location_match.group(1).strip() if location_match else "Unknown Location"

    # Extract job description
    jd_match = re.search(r'<div class="show-more-less-html__markup[^"]*">(.*?)</div>', html_content, re.DOTALL)
    job_description = ""
    if jd_match:
        job_description = clean_html(jd_match.group(1))

    # Extract seniority level
    seniority_match = re.search(r'<h3 class="description__job-criteria-subheader">\s*Seniority level\s*</h3>\s*<span[^>]*>\s*([^<]+)\s*</span>', html_content, re.DOTALL)
    seniority = seniority_match.group(1).strip() if seniority_match else "Not specified"

    # Format job posting
    job_posting = f"""# {title}

**Company**: {company}
**Location**: {location}
**Seniority Level**: {seniority}
**Job ID**: `{job_id}`
**LinkedIn URL**: https://www.linkedin.com/jobs/view/{job_id}

---

## Job Description

{job_description}
"""

    return {
        'title': title,
        'company': company,
        'location': location,
        'seniority': seniority,
        'job_posting': job_posting
    }


def create_directory_name(company: str, title: str) -> str:
    """Create standardized directory name from company and title"""
    # Clean company name
    company_clean = re.sub(r'[^a-zA-Z0-9\s-]', '', company)
    company_clean = re.sub(r'\s+', '-', company_clean.strip())

    # Clean title - extract key role info
    title_clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    title_clean = re.sub(r'\s+', '-', title_clean.strip())

    # Combine and limit length
    dir_name = f"{company_clean}-{title_clean}"

    # Replace multiple consecutive hyphens with single hyphen
    dir_name = re.sub(r'-+', '-', dir_name)

    if len(dir_name) > 80:
        dir_name = dir_name[:80].rstrip('-')

    return dir_name


def scrape_linkedin_job(job_id: str, raw: bool = False, save: bool = True):
    """Fetch job posting from LinkedIn"""
    job_detail_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    resp = requests.get(job_detail_url, headers=headers, timeout=30)
    resp.raise_for_status()

    if raw:
        # Output raw HTML
        print(resp.text)
    else:
        # Parse and output structured data
        details = extract_job_details(resp.text, job_id)

        if save:
            # Create directory name from company and title
            dir_name = create_directory_name(details['company'], details['title'])
            base_dir = Path(__file__).parent.parent / "job-search"
            job_dir = base_dir / dir_name

            # Check if directory already exists
            original_name = dir_name
            if job_dir.exists():
                # Auto-increment with suffix starting at 1
                counter = 1
                while (base_dir / f"{dir_name}-{counter}").exists():
                    counter += 1
                job_dir = base_dir / f"{dir_name}-{counter}"
                print(f"⚠️  Directory already exists: {original_name}")
                print(f"   New directory: {job_dir.name}")

            # Create directory
            job_dir.mkdir(parents=True, exist_ok=True)

            # Save job posting
            (job_dir / "job-posting.md").write_text(details['job_posting'], encoding='utf-8')

            # Save LinkedIn URL
            linkedin_url = f"https://www.linkedin.com/jobs/view/{job_id}"
            (job_dir / "linkedin-url.txt").write_text(linkedin_url, encoding='utf-8')

            print(f"\n✅ Job scraped and saved to: {job_dir.name}")
            print(f"   • job-posting.md")
            print(f"   • linkedin-url.txt")
            print(f"\n📋 Company: {details['company']}")
            print(f"📋 Title: {details['title']}")
        else:
            # Just print to stdout
            print(details['job_posting'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape LinkedIn job postings")
    parser.add_argument("--job-id", required=True, help="LinkedIn job ID")
    parser.add_argument("--raw", action="store_true", help="Output raw HTML instead of parsed content")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file, just print to stdout")
    args = parser.parse_args()

    scrape_linkedin_job(args.job_id, args.raw, save=not args.no_save)
