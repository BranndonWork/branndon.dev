#!/usr/bin/env python3
"""
hiring_cafe.py - Fetch and filter jobs from hiring.cafe

Uses curl_cffi to impersonate Chrome TLS and call the hiring.cafe internal API
directly — no browser or Playwright required.

Usage:
    poetry run python scripts/hiring_cafe.py
    poetry run python scripts/hiring_cafe.py --output json
    poetry run python scripts/hiring_cafe.py --limit 30 --days 7
"""

import argparse
import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import diskcache
import yaml
from curl_cffi import requests

# ──────────────────────────────────────────────────────────────────────────────
# CACHE
# Responses are cached to disk for CACHE_TTL seconds so repeated invocations
# (e.g. multiple tool calls in one session) don't hammer the API.
# ──────────────────────────────────────────────────────────────────────────────
CACHE_DIR = Path.home() / ".cache" / "hiring_cafe"
CACHE_TTL = 3600  # 1 hour in seconds

# ──────────────────────────────────────────────────────────────────────────────
# FILTER REFERENCE
# Complete map of all known queryable attributes and their valid values.
# Use this as a reference when adjusting ACTIVE_FILTERS below.
# ──────────────────────────────────────────────────────────────────────────────
FILTER_OPTIONS = {
    # How results are ordered
    "sortBy": ["date", "default"],  # "default" = relevance

    # How far back to look (days)
    "dateFetchedPastNDays": [7, 14, 29, 60, 121],  # 121 = effectively all-time

    # Where the work is performed
    "workplaceTypes": ["Remote", "Hybrid", "On-Site"],

    # Broad job category buckets
    "departments": [
        "Engineering", "Software Development", "Information Technology",
        "Data and Analytics", "Product", "Design", "Marketing", "Sales",
        "Finance", "Operations", "Legal", "Human Resources", "Customer Success",
    ],

    # Career stage — can mix levels in a list
    "seniorityLevel": [
        "Entry Level", "Mid Level", "Senior Level",
        "Director", "VP Level", "C-Suite",
    ],

    # IC vs management
    "roleTypes": [
        "Individual Contributor", "People Manager", "Technical Lead",
    ],

    # Employment type — can mix in a list
    "commitmentTypes": ["Full Time", "Part Time", "Contract", "Temporary"],

    # Travel burden
    "airTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],
    "landTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],

    # On-call burden (exact API strings)
    "onCallRequirements": [
        "None",
        "Occasional (once a month or less)",
        "Regular (once a week or more)",
    ],

    # Physical environment
    "physicalPositions": ["Sitting", "Standing"],
    "physicalLaborIntensity": ["Low", "Medium", "High"],

    # Application complexity filter
    "applicationFormEase": ["Simple", "Moderate", "Complex"],

    # Security clearance required (exact API strings)
    "securityClearances": [
        "None", "Confidential", "Secret", "Top Secret",
        "Top Secret/SCI", "Public Trust", "Interim Clearances", "Other",
    ],

    # Compensation filters
    "restrictJobsToTransparentSalaries": [True, False],
    # maxCompensationLowEnd: integer USD (show jobs where low end <= this value)

    # Free-text keyword filters — use quoted phrases for exact match
    "jobTitleQuery":            'e.g. "software engineer" "backend developer"',
    "technologyKeywordsQuery":  'e.g. "python" "django" "fastapi"',
    "jobDescriptionQuery":      "keyword search within full description",
    "requirementsKeywordsQuery": "keyword search within requirements section",

    # Misc
    "defaultToUserLocation": [True, False],
}

# ──────────────────────────────────────────────────────────────────────────────
# ACTIVE FILTERS
# These are the filters actually sent to the API.
# Comment out any line to remove that filter from the query.
# Change values freely — refer to FILTER_OPTIONS above for valid choices.
# ──────────────────────────────────────────────────────────────────────────────
ACTIVE_FILTERS = {
    # Ordering & time window
    "sortBy":                           "date",
    "dateFetchedPastNDays":             7,

    # Location
    "workplaceTypes":                   ["Remote"],
    "defaultToUserLocation":            False,

    # Role targeting
    "departments":                      [
        "Engineering", "Software Development",
        "Information Technology", "Data and Analytics",
    ],
    "seniorityLevel":                   ["Mid Level", "Senior Level"],
    "roleTypes":                        ["Individual Contributor"],
    "commitmentTypes":                  ["Full Time", "Part Time", "Contract", "Temporary"],

    # Tech & title keywords
    "jobTitleQuery":                    (
        '"software engineer" "senior software engineer" "backend engineer" '
        '"backend developer" "api engineer" "api developer"'
    ),
    "technologyKeywordsQuery":          '"python"',

    # Compensation
    "restrictJobsToTransparentSalaries": True,
    "maxCompensationLowEnd":            150000,

    # Lifestyle filters — all hard requirements
    "airTravelRequirement":             ["None"],
    "landTravelRequirement":            ["None"],
    "onCallRequirements":               ["None"],  # exact API string
    "physicalPositions":                ["Sitting"],
    "physicalLaborIntensity":           ["Low"],
    "securityClearances":               ["None"],

    # Only simple-to-apply postings
    "applicationFormEase":              ["Simple"],
}


# ──────────────────────────────────────────────────────────────────────────────
# API
# ──────────────────────────────────────────────────────────────────────────────
API_URL = "https://hiring.cafe/api/search-jobs"
PROJECT_ROOT = Path(__file__).parent.parent

# Real Chrome UAs on macOS — rotated per request to avoid static fingerprint
_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]


def _encode_state(filters: dict) -> str:
    """
    Encode the search state the way the hiring.cafe frontend does:
        btoa(encodeURIComponent(JSON.stringify(state)))

    btoa() only handles ASCII, so encodeURIComponent converts unicode first.
    Python equivalent: base64(urllib.quote(json.dumps(state)))
    """
    import base64
    from urllib.parse import quote
    json_str = json.dumps(filters, separators=(",", ":"))
    pct_encoded = quote(json_str, safe="")
    return base64.b64encode(pct_encoded.encode()).decode()


def fetch_jobs(filters: dict, page: int = 0, size: int = 100, no_cache: bool = False) -> list[dict]:
    """
    Fetch a page of jobs from the hiring.cafe API.

    Results are cached to disk for CACHE_TTL seconds. Pass no_cache=True to
    force a fresh network request regardless of cached data.
    """
    s = _encode_state(filters)
    cache_key = f"{s}:{page}:{size}"

    with diskcache.Cache(CACHE_DIR) as cache:
        if not no_cache:
            cached = cache.get(cache_key)
            if cached is not None:
                print("Cache hit — using stored response (use --no-cache to refresh).", file=sys.stderr)
                return cached

        # curl_cffi impersonates Chrome TLS fingerprint to bypass Vercel bot protection
        params = {"s": s, "size": str(size), "page": str(page)}
        session = requests.Session()
        resp = session.get(
            API_URL,
            params=params,
            impersonate="chrome142",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://hiring.cafe/",
                "Origin": "https://hiring.cafe",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": random.choice(_USER_AGENTS),
            },
            timeout=20,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])

        cache.set(cache_key, results, expire=CACHE_TTL)
        print(f"Cached {len(results)} results for {CACHE_TTL // 60} minutes.", file=sys.stderr)
        return results


# ──────────────────────────────────────────────────────────────────────────────
# DEDUP / FILTERING
# ──────────────────────────────────────────────────────────────────────────────

def load_ignored_companies() -> set[str]:
    """Load company names from the ignore list (lowercased for comparison)."""
    ignore_path = PROJECT_ROOT / "data" / "company_ignore_list.json"
    if not ignore_path.exists():
        return set()
    data = json.loads(ignore_path.read_text())
    return {name.lower() for name in data.get("ignored_companies", {}).keys()}


def load_applied_companies() -> set[str]:
    """Scan job-search/ YAML files and return companies already in the pipeline."""
    applied = set()
    for yaml_file in (PROJECT_ROOT / "job-search").glob("*/job-application.yaml"):
        try:
            doc = yaml.safe_load(yaml_file.read_text())
            if doc and doc.get("company"):
                applied.add(doc["company"].lower())
        except Exception:
            pass
    return applied


def get_company_name(job: dict) -> str:
    """Extract company name from a job record, trying multiple fields."""
    v5 = job.get("v5_processed_job_data") or {}
    ec = job.get("enriched_company_data") or {}
    return (
        ec.get("name")
        or v5.get("company_name")
        or job.get("board_token", "")
    )


# ──────────────────────────────────────────────────────────────────────────────
# TITLE FILTER
# Reject leadership/coordination titles before scoring. These roles carry
# meeting load, planning overhead, and visibility that conflicts with OE goals.
# ──────────────────────────────────────────────────────────────────────────────
_REJECT_TITLE_WORDS = [
    "staff", "principal", "lead", "manager", "director", "architect",
    "vp ", "head of", "chief", "cto", "cio", "founding",
]


def title_is_eligible(title: str) -> bool:
    """Return False if the title contains a leadership/coordination keyword."""
    t = title.lower()
    return not any(r in t for r in _REJECT_TITLE_WORDS)


def location_is_eligible(v5: dict) -> bool:
    """
    Return False if the job is geo-locked to non-US countries.
    Jobs with no country data or worldwide=True are allowed through.
    """
    if v5.get("is_workplace_worldwide_ok"):
        return True
    countries = v5.get("workplace_countries") or []
    if not countries:
        return True  # no geo data — give benefit of the doubt
    return "US" in countries


# ──────────────────────────────────────────────────────────────────────────────
# SCORING
# ──────────────────────────────────────────────────────────────────────────────

def score_job(job: dict) -> int:
    """
    Score 0-100 based on salary floor, Python presence, and recency.

      Salary floor (0-40):  USD only. $200k+ = 40, $175k = 30, $150k = 20, $125k = 10, else 0
      Python in stack (20): exact match in technical_tools
      Recency (0-20):       <=3 days = 20, <=7 days = 15, <=14 days = 10, else 5
      YOE fit (0-20):       <=5 yrs required = 20, <=8 = 15, <=12 = 10, else 0

    Non-USD roles score 0 on salary — the raw numbers are not comparable.
    """
    v5 = job.get("v5_processed_job_data") or {}
    score = 0

    # Salary floor — only score if currency is USD (or not specified, assume USD)
    currency = (v5.get("listed_compensation_currency") or "USD").upper()
    min_comp = v5.get("yearly_min_compensation") or 0
    if currency == "USD" and min_comp:
        if min_comp >= 200_000:
            score += 40
        elif min_comp >= 175_000:
            score += 30
        elif min_comp >= 150_000:
            score += 20
        elif min_comp >= 125_000:
            score += 10

    # Python in tech stack
    tools = [t.lower() for t in (v5.get("technical_tools") or [])]
    if "python" in tools:
        score += 20

    # Recency
    pub_date_str = v5.get("estimated_publish_date")
    if pub_date_str:
        try:
            pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - pub_date).days
            if age_days <= 3:
                score += 20
            elif age_days <= 7:
                score += 15
            elif age_days <= 14:
                score += 10
            else:
                score += 5
        except ValueError:
            score += 5

    # Years of experience fit
    yoe = v5.get("min_industry_and_role_yoe") or 0
    if yoe <= 5:
        score += 20
    elif yoe <= 8:
        score += 15
    elif yoe <= 12:
        score += 10

    # Staffing agency penalty — direct employer is strongly preferred
    employer_type = (v5.get("position_employer_type") or "").lower()
    if "staffing" in employer_type or "agency" in employer_type or "recruiter" in employer_type:
        score -= 20

    return max(score, 0)


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

def format_salary(v5: dict) -> str:
    low = v5.get("yearly_min_compensation")
    high = v5.get("yearly_max_compensation")
    currency = v5.get("listed_compensation_currency") or "USD"
    if low and high:
        return f"{currency} ${low:,.0f} – ${high:,.0f}/yr"
    if low:
        return f"{currency} ${low:,.0f}+/yr"
    return "Not disclosed"


def build_summary(job: dict, score: int) -> dict:
    v5 = job.get("v5_processed_job_data") or {}
    ec = job.get("enriched_company_data") or {}
    return {
        "score": score,
        "title": v5.get("core_job_title") or job.get("job_information", {}).get("title"),
        "company": get_company_name(job),
        "seniority": v5.get("seniority_level"),
        "salary": format_salary(v5),
        "tech_stack": (v5.get("technical_tools") or [])[:8],
        "yoe_required": v5.get("min_industry_and_role_yoe"),
        "posted": v5.get("estimated_publish_date", "")[:10],
        "requirements_summary": v5.get("requirements_summary"),
        "apply_url": job.get("apply_url"),
        "company_size": ec.get("nb_employees"),
        "company_funding": ec.get("latest_funding_type"),
        "company_founded": ec.get("year_founded"),
        "visa_sponsorship": v5.get("visa_sponsorship"),
        "employer_type": v5.get("position_employer_type"),
        "source": job.get("source"),
    }


def print_human(jobs: list[dict]) -> None:
    print(f"\n{'='*70}")
    print(f"  hiring.cafe results — {len(jobs)} jobs after filtering")
    print(f"{'='*70}\n")

    for i, job in enumerate(jobs, 1):
        score = job["score"]
        tech = ", ".join(job["tech_stack"]) or "N/A"
        funding = job["company_funding"] or "unknown"
        size = f"{job['company_size']:,} employees" if job["company_size"] else "size unknown"
        yoe = f"{job['yoe_required']}+ yrs" if job["yoe_required"] else "not specified"

        et = (job.get("employer_type") or "").lower()
        employer_flag = f"  ⚠ {job['employer_type']}" if any(w in et for w in ("staffing", "agency", "recruiter")) else ""
        print(f"#{i:02d}  [{score:3d}/100]  {job['title']}{employer_flag}")
        print(f"       Company:  {job['company']}  ({size}, {funding}, founded {job['company_founded'] or '?'})")
        print(f"       Salary:   {job['salary']}")
        print(f"       Stack:    {tech}")
        print(f"       YOE:      {yoe}  |  Posted: {job['posted']}")
        if job["requirements_summary"]:
            print(f"       Summary:  {job['requirements_summary'][:120]}...")
        print(f"       Apply:    {job['apply_url']}")
        print()


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def manual_fetch() -> None:
    """
    Open the search URL in the browser, then wait for you to paste the JSON response
    into a VS Code file and close the tab.

    Workflow:
      1. Copy the full JSON response from the browser tab that opens (Cmd+A, Cmd+C).
      2. Paste into the VS Code file that opens, then close the tab (Cmd+W).
      3. The script exits and Claude can read the file automatically.
    """
    import subprocess
    import webbrowser

    s = _encode_state(ACTIVE_FILTERS)
    url = f"{API_URL}?s={s}&size=100&page=0"
    output = Path("/tmp/hiring_cafe_jobs.json")
    output.write_text("")

    print(f"\nOpening browser URL:\n  {url}\n", file=sys.stderr)
    webbrowser.open(url)

    print(f"Paste the JSON response into VS Code, then close the tab (Cmd+W)...\n", file=sys.stderr)
    subprocess.run(["code", "--wait", str(output)])

    print(f"Done. File saved at {output}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Fetch and rank hiring.cafe jobs")
    parser.add_argument("--manual", action="store_true", help="Open browser + temp file for manual CF bypass")
    parser.add_argument("--from-file", metavar="PATH", help="Load raw API JSON from file instead of hitting the API")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--limit", type=int, default=25, help="Max results to show")
    parser.add_argument("--days", type=int, help="Override dateFetchedPastNDays")
    parser.add_argument("--no-filter", action="store_true", help="Skip ignore/applied filtering")
    parser.add_argument("--no-cache", action="store_true", help="Bypass disk cache and force a fresh API request")
    parser.add_argument(
        "--currencies",
        default="USD",
        help=(
            "Comma-separated list of salary currencies to include (default: USD). "
            "Options seen in data: USD, CAD, EUR, GBP, PLN, INR. "
            "Use 'all' to skip currency filtering."
        ),
    )
    args = parser.parse_args()

    if args.manual:
        manual_fetch()
        args.from_file = "/tmp/hiring_cafe_jobs.json"
        print(f"\nProcessing {args.from_file} through filters...\n", file=sys.stderr)

    if args.from_file:
        src = Path(args.from_file)
        raw = json.loads(src.read_text())
        jobs = raw.get("results", raw) if isinstance(raw, dict) else raw
        print(f"Loaded {len(jobs)} jobs from {src}.", file=sys.stderr)
    else:
        filters = dict(ACTIVE_FILTERS)
        if args.days:
            filters["dateFetchedPastNDays"] = args.days
        print("Fetching jobs from hiring.cafe...", file=sys.stderr)
        jobs = fetch_jobs(filters, no_cache=args.no_cache)
        print(f"Fetched {len(jobs)} raw results.", file=sys.stderr)

    # Local date filter — API does not enforce dateFetchedPastNDays server-side
    max_age_days = args.days or ACTIVE_FILTERS.get("dateFetchedPastNDays", 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    before = len(jobs)
    jobs = [
        j for j in jobs
        if (pub := (j.get("v5_processed_job_data") or {}).get("estimated_publish_date"))
        and datetime.fromisoformat(pub.replace("Z", "+00:00")) >= cutoff
    ]
    print(f"Date filter (last {max_age_days}d): {len(jobs)} remain (removed {before - len(jobs)}).", file=sys.stderr)

    if not args.no_filter:
        ignored = load_ignored_companies()
        applied = load_applied_companies()
        skip = ignored | applied

        before = len(jobs)
        jobs = [
            j for j in jobs
            if get_company_name(j).lower() not in skip
        ]
        print(f"Filtered to {len(jobs)} (removed {before - len(jobs)} ignored/applied).", file=sys.stderr)

    if args.currencies.lower() != "all":
        allowed_currencies = {c.strip().upper() for c in args.currencies.split(",")}
        before = len(jobs)
        jobs = [
            j for j in jobs
            if ((j.get("v5_processed_job_data") or {}).get("listed_compensation_currency") or "USD").upper()
            in allowed_currencies
        ]
        print(
            f"Currency filter ({', '.join(sorted(allowed_currencies))}): "
            f"{len(jobs)} remain (removed {before - len(jobs)}).",
            file=sys.stderr,
        )

    # Title filter — reject leadership/coordination titles
    before = len(jobs)
    jobs = [
        j for j in jobs
        if title_is_eligible(
            (j.get("v5_processed_job_data") or {}).get("core_job_title")
            or j.get("job_information", {}).get("title", "")
        )
    ]
    print(f"Title filter: {len(jobs)} remain (removed {before - len(jobs)}).", file=sys.stderr)

    # Location filter — reject jobs geo-locked to non-US countries
    before = len(jobs)
    jobs = [
        j for j in jobs
        if location_is_eligible(j.get("v5_processed_job_data") or {})
    ]
    print(f"Location filter: {len(jobs)} remain (removed {before - len(jobs)}).", file=sys.stderr)

    # Score and sort
    scored = sorted(
        [build_summary(j, score_job(j)) for j in jobs],
        key=lambda x: x["score"],
        reverse=True,
    )
    results = scored[: args.limit]

    if args.output == "json":
        print(json.dumps(results, indent=2, default=str))
    else:
        print_human(results)


if __name__ == "__main__":
    main()
