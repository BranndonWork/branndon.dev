"""
Job filtering configuration for auto-skipping unwanted roles.

These keywords in job titles indicate roles that should be automatically marked as 'reviewed' (skipped).
"""

# Keywords that indicate jobs to skip (case-insensitive matching)
SKIP_TITLE_KEYWORDS = [
    # Management & Leadership
    "manager",
    "director",
    "head of",

    # Non-engineering roles
    "consultant",
    "trader",
    "auditor",
    "analyst",
    "psychometrician",

    # Wrong seniority
    "intern",
    "junior",
    "new graduate",

    # Non-backend focus
    "artist",
    "scientist",
    "quantitative",
    "r&d",

    # Non-target tech
    "c++",

    # System administration (not backend development)
    "administrator",

    # French roles (location mismatch)
    "concepteur",
]

# Reason for auto-skip
AUTO_SKIP_REASON = "Auto-skipped: title contains excluded keyword"
