#!/usr/bin/env python3
"""CLI entry point for fast resume customization pipeline.

All output goes to /tmp/resume-poc/ — never writes to the project tree.

Usage:
    poetry run python scripts/resume/generate.py job-search/Recharge-Platform-Software-Engineer/
    poetry run python scripts/resume/generate.py job-search/Recharge-Platform-Software-Engineer/ --pdf
    poetry run python scripts/resume/generate.py job-search/Recharge-Platform-Software-Engineer/ --dry-run
"""

import argparse
import asyncio
import json
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

# Project root is two levels up from this file
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MASTER_RESUME_PATH = PROJECT_ROOT / "webroot" / "branndon-coelho-resume.json"
WEBROOT = PROJECT_ROOT / "webroot"
OUTPUT_DIR = Path("/tmp/resume-poc")

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from resume.keyword_extractor import extract_keywords, get_company_name, get_job_title
from resume.resume_builder import build_ats_resume


def make_slug(company_name: str) -> str:
    """Create a filename-safe slug from a company name."""
    slug = company_name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def load_master_resume() -> dict:
    with open(MASTER_RESUME_PATH, encoding="utf-8") as f:
        return json.load(f)


def _find_free_port() -> int:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def generate_pdf(json_path: Path, pdf_path: Path) -> bool:
    """Generate PDF using a temporary isolated webroot and server.

    1. Copy real webroot to /tmp/resume-poc/webroot/
    2. Drop the custom JSON in as the resume data file
    3. Start a temp HTTP server on that copy
    4. Run Playwright to render PDF to /tmp/resume-poc/
    5. Kill the temp server
    """
    tmp_webroot = OUTPUT_DIR / "webroot"

    # Copy real webroot into temp (HTML, CSS, JS, images)
    if tmp_webroot.exists():
        shutil.rmtree(tmp_webroot)
    shutil.copytree(WEBROOT, tmp_webroot, ignore=shutil.ignore_patterns("*.pdf"))

    # Place the custom JSON as the ATS file the HTML expects in ATS mode
    shutil.copy2(json_path, tmp_webroot / "branndon-coelho-resume-ats.json")

    # Patch the temp HTML: fix SummarySection to be visible and render HTML
    index_html = tmp_webroot / "index.html"
    html_text = index_html.read_text(encoding="utf-8")
    html_text = html_text.replace(
        'style={{ display: "none" }} className="resume-section summary-section mb-5"',
        'className="resume-section summary-section mb-5"',
    )
    html_text = html_text.replace(
        '<p className="mb-0 highlight">{sectionData.summary}</p>',
        '<p className="mb-0 highlight" dangerouslySetInnerHTML={{ __html: sectionData.summary }} />',
    )
    index_html.write_text(html_text, encoding="utf-8")

    # Start isolated HTTP server
    port = _find_free_port()
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        cwd=str(tmp_webroot),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # Wait for server to be ready
        import urllib.request
        url = f"http://127.0.0.1:{port}?mode=ats"
        for _ in range(20):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.25)
        else:
            print("  Error: temp server never became ready")
            return False

        # Run Playwright inline (avoids shelling out to another script)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector(".resume-wrapper", timeout=10000)
            page.wait_for_selector(".resume-header", timeout=10000)
            page.wait_for_timeout(2000)

            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
                print_background=False,
                prefer_css_page_size=True,
            )
            browser.close()

        print(f"  PDF: {pdf_path}")
        return True

    except Exception as e:
        print(f"  PDF generation failed: {e}")
        return False

    finally:
        server_proc.terminate()
        server_proc.wait(timeout=5)
        # Clean up temp webroot
        if tmp_webroot.exists():
            shutil.rmtree(tmp_webroot)


def main():
    parser = argparse.ArgumentParser(
        description="Generate customized ATS resume JSON from a job directory"
    )
    parser.add_argument(
        "job_dir",
        type=str,
        help="Path to the job directory (e.g., job-search/Recharge-Platform-Software-Engineer/)",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also generate PDF using Playwright pipeline",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files",
    )

    args = parser.parse_args()

    start_time = time.time()

    # Resolve job directory (read-only source)
    job_dir = Path(args.job_dir)
    if not job_dir.is_absolute():
        job_dir = PROJECT_ROOT / job_dir
    job_dir = job_dir.resolve()

    if not job_dir.exists():
        print(f"Error: Job directory not found: {job_dir}")
        sys.exit(1)

    # Load master resume
    master_resume = load_master_resume()

    # Step 1: Extract keywords
    keywords = extract_keywords(job_dir, master_resume)
    if not keywords:
        print("Warning: No keywords extracted from JD. Check job directory contents.")
        print(f"  Looked for: job-posting.md, job-tracking.yaml, job-application.yaml")
        sys.exit(1)

    # Get job metadata
    job_title = get_job_title(job_dir)
    company_name = get_company_name(job_dir)
    company_slug = make_slug(company_name)

    print(f"Company:  {company_name}")
    print(f"Title:    {job_title}")
    print(f"Keywords: {len(keywords)} matched")
    print(f"  {', '.join(sorted(keywords))}")

    # Step 2: Build ATS resume
    ats_resume = build_ats_resume(master_resume, keywords, job_title, company_name)

    # Show experience selection
    print(f"\nExperiences selected:")
    for exp in ats_resume["experienceSection"]["experiences"]:
        print(f"  - {exp['companyName']} ({exp['position']})")

    if args.dry_run:
        print(f"\n[DRY RUN] Would write to: {OUTPUT_DIR}/")
        print(f"\nSummary preview:")
        print(f"  {ats_resume['summarySection']['summary'][:200]}...")
        elapsed = time.time() - start_time
        print(f"\nElapsed: {elapsed:.1f}s")
        return

    # All output goes to /tmp/resume-poc/
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 3: Write JSON
    json_filename = f"resume-branndon-coelho-{company_slug}-ats.json"
    json_path = OUTPUT_DIR / json_filename
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ats_resume, f, indent=4, ensure_ascii=False)
    print(f"\nJSON: {json_path}")

    # Step 4: Optional PDF generation
    if args.pdf:
        print("\nGenerating PDF...")
        pdf_filename = f"resume-branndon-coelho-{company_slug}-ats.pdf"
        pdf_path = OUTPUT_DIR / pdf_filename
        if generate_pdf(json_path, pdf_path):
            job_pdf_dest = job_dir / pdf_filename
            shutil.copy2(pdf_path, job_pdf_dest)
            print(f"  Copied: {job_pdf_dest.relative_to(PROJECT_ROOT)}")

    # Always copy JSON to job dir for reference
    shutil.copy2(json_path, job_dir / json_filename)
    print(f"Copied: {(job_dir / json_filename).relative_to(PROJECT_ROOT)}")

    elapsed = time.time() - start_time
    print(f"\nElapsed: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
