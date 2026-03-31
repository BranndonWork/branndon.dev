---
description: "Fetch today's hiring.cafe jobs, filter against your pipeline, and get ranked recommendations"
argument-hint: "[optional context or flags]"
allowed-tools: ["bash", "read", "glob"]
---

# Hiring Cafe Jobs

Read `prompts/hiring-cafe-jobs.md` and follow it completely. That file is the single source of truth for workflow, scoring, file locations, and current preference overrides.

## Fetch Strategy

### Step 1 — Try the standard API route first

```bash
poetry run python scripts/hiring_cafe.py --output json 2>/dev/null > /tmp/hiring_cafe_jobs.json
```

Then read `/tmp/hiring_cafe_jobs.json`. If the result is valid JSON with at least one job, proceed normally.

**Blocked / empty = anything that is:**
- Not valid JSON
- An empty array `[]`
- An error message or HTML (Cloudflare block page)

### Step 2 — Fallback: manual browser fetch

If Step 1 is blocked or returns no results, immediately run:

```bash
poetry run python scripts/hiring_cafe.py --manual
```

This opens the API URL in the browser and a VS Code file waiting for input. Tell the user:

> "The API is blocked. I've opened the URL in your browser and a VS Code file. Copy the full JSON from the browser (Cmd+A, Cmd+C), paste it into VS Code, then close the tab (Cmd+W)."

Wait for the user to confirm they've closed the tab, then verify the data with:

```bash
python3 -c "import json; d=json.load(open('/tmp/hiring_cafe_jobs.json')); jobs=d.get('results', d) if isinstance(d, dict) else d; print(f'{len(jobs)} jobs')"
```

The JSON is a dict with a `results` key — `len(data)` returns 1 (key count), not job count. Use the above to confirm you have real data before proceeding.

---

## Other CLI Flags (use only on explicit request)

```bash
# Wider time window
poetry run python scripts/hiring_cafe.py --output json --days 14

# Force fresh (bypass 1hr cache)
poetry run python scripts/hiring_cafe.py --output json --no-cache

# Include non-USD
poetry run python scripts/hiring_cafe.py --output json --currencies USD,CAD

# Audit filtered results
poetry run python scripts/hiring_cafe.py --currencies all --no-filter
```

Note: never use `2>&1` — it corrupts the JSON output by merging stderr into stdout.

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
