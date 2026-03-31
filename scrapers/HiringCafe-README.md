# HiringCafe Scraper — Reference

## How It Works

HiringCafe crawls company career pages directly (not user-submitted postings). Every job is run through GPT-4o-mini at temperature 0 to extract structured data. This means each job record contains AI-extracted fields for salary, seniority, role type, on-call requirements, etc — not just raw text.

## API

**Base URL**: `https://hiring.cafe`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/search-jobs` | GET | Paginated job results |
| `/api/search-jobs/get-total-count` | GET | Result count before fetching |

Both endpoints take a single `s` query parameter: the `searchState` JSON object, URL-encoded, then base64-encoded.

```python
import json, base64, urllib.parse

def encode_s(state: dict) -> str:
    return base64.b64encode(urllib.parse.quote(json.dumps(state)).encode()).decode()
```

**Pagination params** (on the jobs endpoint):
- `s` — encoded searchState
- `size` — results per page (max observed: 1000, actual pages return ~3800)
- `page` — 0-indexed page number

**Count response:**
```json
{ "total": 3726127, "collapsedTotal": 155402 }
```
`total` counts the same job across multiple source URLs. `collapsedTotal` is unique jobs — the number that matters.

**Jobs response:**
```json
{ "results": [ ...job objects... ] }
```
The server returns a 500 after roughly 10 pages on a broad query — this is a server-side limit, not a pagination error.

## searchState Fields

The full searchState object with all available filter fields:

```python
search_state = {
    # ── Search ────────────────────────────────────────────────
    "searchQuery": "",                    # Free text. Empty = all jobs
    "technologyKeywordsQuery": "",        # Tech stack search (separate from title/desc)
    "requirementsKeywordsQuery": "",      # Requirements text search
    "jobTitleQuery": "",                  # Title-only search
    "jobDescriptionQuery": "",            # Description-only search
    "dateFetchedPastNDays": -1,           # -1 = all time. 1/2/7/14/30 for recency

    # ── Workplace ─────────────────────────────────────────────
    "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
    "locations": [],                      # Location objects (empty = worldwide)
    "defaultToUserLocation": False,
    "userLocation": None,

    # ── Role ──────────────────────────────────────────────────
    "commitmentTypes": ["Full Time", "Part Time", "Contract", "Internship", "Temporary", "Seasonal", "Volunteer"],
    "seniorityLevel": ["No Prior Experience Required", "Entry Level", "Mid Level", "Senior Level"],
    "roleTypes": ["Individual Contributor", "People Manager"],
    "roleYoeRange": [0, 20],              # Years of experience range for IC role
    "managementYoeRange": [0, 20],        # Years of experience range for management
    "excludeIfRoleYoeIsNotSpecified": False,
    "excludeIfManagementYoeIsNotSpecified": False,

    # ── Compensation ──────────────────────────────────────────
    "currency": {"label": "Any", "value": None},
    "frequency": {"label": "Any", "value": None},
    "calcFrequency": "Yearly",
    "minCompensationLowEnd": None,        # Min salary low bound
    "minCompensationHighEnd": None,       # Min salary high bound
    "maxCompensationLowEnd": None,
    "maxCompensationHighEnd": None,
    "restrictJobsToTransparentSalaries": False,

    # ── Work Conditions ───────────────────────────────────────
    "onCallRequirements": ["None", "Occasional (once a month or less)", "Regular (once a week or more)"],
    "overtimeRequired": "Doesn't Matter",       # or "Yes" / "No"
    "weekendAvailabilityRequired": "Doesn't Matter",
    "holidayAvailabilityRequired": "Doesn't Matter",
    "airTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],
    "landTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],
    "morningShiftWork": [],
    "eveningShiftWork": [],
    "overnightShiftWork": [],

    # ── Physical ──────────────────────────────────────────────
    "physicalEnvironments": ["Office", "Outdoor", "Vehicle", "Industrial", "Customer-Facing"],
    "physicalLaborIntensity": ["Low", "Medium", "High"],
    "physicalPositions": ["Sitting", "Standing"],
    "oralCommunicationLevels": ["Low", "Medium", "High"],
    "computerUsageLevels": ["Low", "Medium", "High"],
    "cognitiveDemandLevels": ["Low", "Medium", "High"],

    # ── Education & Credentials ───────────────────────────────
    "associatesDegreeRequirements": [],
    "bachelorsDegreeRequirements": [],
    "mastersDegreeRequirements": [],
    "doctorateDegreeRequirements": [],
    "bachelorsDegreeFieldsOfStudy": [],
    "mastersDegreeFieldsOfStudy": [],
    "doctorateDegreeFieldsOfStudy": [],
    "excludedBachelorsDegreeFieldsOfStudy": [],
    "excludedMastersDegreeFieldsOfStudy": [],
    "excludedDoctorateDegreeFieldsOfStudy": [],
    "licensesAndCertifications": [],
    "excludedLicensesAndCertifications": [],
    "excludeAllLicensesAndCertifications": False,
    "securityClearances": ["None", "Confidential", "Secret", "Top Secret", "Top Secret/SCI", "Public Trust", "Interim Clearances", "Other"],

    # ── Company ───────────────────────────────────────────────
    "companyNames": [],                   # Whitelist specific companies
    "excludedCompanyNames": [],           # Blacklist companies
    "companyHqCountries": [],
    "excludedCompanyHqCountries": [],
    "companySizeRanges": [],
    "companyPublicOrPrivate": "all",      # "public" / "private" / "all"
    "isNonProfit": "all",                 # "yes" / "no" / "all"
    "organizationTypes": [],
    "excludedOrganizationTypes": [],
    "industries": [],
    "excludedIndustries": [],
    "companyKeywords": [],
    "excludedCompanyKeywords": [],
    "companyKeywordsBooleanOperator": "OR",
    "usaGovPref": None,

    # ── Funding / Investment ──────────────────────────────────
    "latestInvestmentSeries": [],         # e.g. ["Seed", "Series A", "Series B"]
    "excludedLatestInvestmentSeries": [],
    "latestInvestmentYearRange": [None, None],
    "latestInvestmentAmount": None,
    "latestInvestmentCurrency": [],
    "investors": [],
    "excludedInvestors": [],
    "minYearFounded": None,
    "maxYearFounded": None,

    # ── Benefits ──────────────────────────────────────────────
    "benefitsAndPerks": [],
    "encouragedToApply": [],
    "applicationFormEase": [],

    # ── Misc ──────────────────────────────────────────────────
    "languageRequirements": [],
    "excludedLanguageRequirements": [],
    "languageRequirementsOperator": "OR",
    "excludeJobsWithAdditionalLanguageRequirements": False,
    "sortBy": "default",
    "departments": [],
    "hiddenCompanies": [],
    "hideJobTypes": [],
    "restrictedSearchAttributes": [],
    "user": None,
    "searchModeSelectedCompany": None,
}
```

## Response Data Structure

Each job object returned has these top-level keys:

```
id                    — job identifier
objectID              — stable deduplication key across runs
board_token           — source ATS identifier
source                — ATS source name (workday, greenhouse, taleo, etc.)
apply_url             — direct application URL
source_and_board_token
job_information       — raw job data (title, description, company_info)
v5_processed_job_data — GPT-extracted structured fields (see below)
enriched_company_data — company profile data
_geoloc               — lat/lon for location-based filtering
original_source_id
requisition_id
collapse_key
is_expired
```

### v5_processed_job_data — Key Fields

These are AI-extracted and the most useful for filtering:

```
core_job_title                  — normalized title
requirements_summary            — ≤250 char summary of requirements
technical_tools                 — list of tech/tools mentioned
seniority_level                 — "Senior Level", "Mid Level", etc.
role_type                       — "Individual Contributor" or "People Manager"
commitment                      — "Full Time", "Contract", etc.
workplace_type                  — "Remote", "Hybrid", "Onsite"
on_call_requirement             — "None", "Occasional...", "Regular..."
overtime_required               — "Yes" / "No" / null
weekend_availability_required   — bool
four_day_work_week              — bool
yearly_min_compensation         — integer (USD)
yearly_max_compensation         — integer (USD)
monthly/weekly/hourly variants  — same for other frequencies
listed_compensation_currency    — ISO currency code
is_compensation_transparent     — bool
visa_sponsorship                — bool
relocation_assistance           — bool
401k_matching                   — bool
generous_paid_time_off          — bool
generous_parental_leave         — bool
tuition_reimbursement           — bool
fair_chance                     — bool
security_clearance              — clearance level string
position_employer_type          — "Direct" / "Staffing Agency" etc.
company_name                    — extracted company name
company_website
estimated_publish_date          — ISO date string
estimated_publish_date_millis   — unix ms timestamp
min_industry_and_role_yoe       — minimum YOE required
job_category                    — one of 16 categories (e.g. "Software Development")
role_activities                 — list of activity types
workplace_countries / states / cities — location arrays
```

### enriched_company_data — Key Fields

```
name
homepage_uri
hq_country
industries                — list
activities                — list
nb_employees              — headcount
year_founded
organization_type
latest_funding_type       — "Series A", "Series B", "IPO", "Bootstrapped", etc.
latest_funding_investors  — list
tagline
```

## Running the Scraper

```bash
# Full pull — all remote jobs, all time
poetry run python scrapers/HiringCafe-upstream/job_scraper.py

# Targeted query
poetry run python scrapers/HiringCafe-upstream/job_scraper.py --query "Python"

# Last N days
poetry run python scrapers/HiringCafe-upstream/job_scraper.py --days 2

# Custom output
poetry run python scrapers/HiringCafe-upstream/job_scraper.py --output /tmp/jobs.json
```

## Incremental Updates

`dateFetchedPastNDays` controls which jobs are returned — it filters by when HiringCafe's crawler fetched the job from the company site, not the original post date. Using `days=2` on daily runs gives a safe overlap window.

Deduplication key for merging runs: `objectID`.

```python
with open("remote_jobs_all.json") as f:
    existing = {j["objectID"]: j for j in json.load(f)}

new_jobs = scrape_hiring_cafe_jobs("", days=2)

for job in new_jobs:
    existing[job["objectID"]] = job  # insert or update

with open("remote_jobs_all.json", "w") as f:
    json.dump(list(existing.values()), f)
```
