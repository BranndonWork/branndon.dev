"""Assemble customized ATS JSON from master resume + scores + keywords."""

import copy
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from .bold_injector import inject_bold, inject_bold_in_list
from .experience_scorer import rank_experiences
from .keyword_extractor import build_vocabulary

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Technology limits per experience position (1st, 2nd, 3rd)
TECH_LIMITS = [10, 8, 6]

# Max descriptions and achievements per experience
MAX_DESCRIPTIONS = 3
MAX_ACHIEVEMENTS = 3


def _load_summary_templates() -> dict:
    with open(TEMPLATES_DIR / "summaries.json", encoding="utf-8") as f:
        return json.load(f)


def _keyword_density(text: str, keywords: set[str]) -> int:
    """Count keyword occurrences in text for ranking."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def _select_summary_template(keywords: set[str], templates: dict) -> str:
    """Select the best matching summary template based on keyword categories."""
    category_keywords = templates.get("category_keywords", {})
    best_category = "backend-general"
    best_count = 0

    kw_lower = {kw.lower() for kw in keywords}

    for category, cat_keywords in category_keywords.items():
        if category == "backend-general":
            continue
        count = sum(1 for ck in cat_keywords if ck.lower() in kw_lower)
        if count > best_count:
            best_count = count
            best_category = category

    return templates.get(best_category, templates["backend-general"])


def _fill_summary_slots(template: str, keywords: set[str]) -> str:
    """Fill template slots with actual keywords from the JD match."""
    kw_list = list(keywords)
    kw_lower = {kw.lower(): kw for kw in keywords}

    # Define slot priorities — try to find the best match for each slot
    slot_candidates = {
        "primary_lang": ["Python", "JavaScript", "TypeScript", "Node.js", "Ruby", "Go", "Java"],
        "framework": ["Django", "Flask", "FastAPI", "Node.js", "React", "Next.js", "Express", "Hapi"],
        "architecture": [
            "distributed systems", "microservices", "event-driven architectures",
            "scalable systems", "cloud-native architecture", "serverless architecture",
            "platform engineering", "system architecture",
        ],
        "database": [
            "PostgreSQL", "MySQL", "Redis", "MongoDB", "DynamoDB",
            "Elasticsearch", "Amazon Redshift",
        ],
        "infra": [
            "AWS Lambda", "Kubernetes", "Docker", "AWS", "Google Cloud Platform",
            "Cloudflare", "CI/CD", "AWS S3", "Redis",
        ],
        "system_types": [
            "event-driven architectures", "real-time systems", "distributed systems",
            "scalable backend services", "production applications",
        ],
        "specialty": [
            "platform engineering", "backend development", "API design",
            "performance optimization", "system architecture",
        ],
    }

    # Collect values already hardcoded in the template (outside of slots)
    # to avoid duplicate terms in filled output
    template_lower = template.lower()
    used_values = set()
    # Pre-populate with terms already in the template text (not in slots)
    for candidates in slot_candidates.values():
        for candidate in candidates:
            if candidate.lower() in template_lower:
                used_values.add(candidate.lower())

    replacements = {}
    for slot, candidates in slot_candidates.items():
        matched = None
        for candidate in candidates:
            if candidate.lower() in kw_lower and candidate.lower() not in used_values:
                matched = kw_lower[candidate.lower()]
                break
        if not matched:
            defaults = {
                "primary_lang": "Python",
                "framework": "Django",
                "architecture": "scalable systems",
                "database": "PostgreSQL",
                "infra": "cloud infrastructure",
                "system_types": "production backend services",
                "specialty": "backend development",
            }
            matched = defaults.get(slot, "backend systems")
        replacements[slot] = matched
        used_values.add(matched.lower())

    result = template
    for slot, value in replacements.items():
        result = result.replace("{" + slot + "}", value)

    return result


def _reorder_positions(master_positions: list[str], job_title: str) -> list[str]:
    """Reorder positions list so the closest match to the job title is first."""
    if not job_title:
        return list(master_positions)

    scored = []
    for pos in master_positions:
        ratio = SequenceMatcher(None, pos.lower(), job_title.lower()).ratio()
        scored.append((pos, ratio))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [pos for pos, _ in scored]


def _reorder_technologies(
    technologies: list[str],
    keywords: set[str],
    limit: int,
    technology_levels: dict | None = None,
) -> list[str]:
    """Reorder tech list using usage levels and JD match. Apply limit.

    Priority order (lower bucket number = higher priority):
      0: core + JD match
      1: frequent + JD match
      2: core, no JD match
      3: frequent, no JD match
      4: minor (JD match or not — always last)
    """
    if not technology_levels:
        # Fallback: original behavior (JD match first, then remaining)
        kw_lower = {kw.lower() for kw in keywords}
        matching = [t for t in technologies if t.lower() in kw_lower]
        remaining = [t for t in technologies if t.lower() not in kw_lower]
        return (matching + remaining)[:limit]

    kw_lower = {kw.lower() for kw in keywords}
    core = {t.lower() for t in technology_levels.get("core", [])}
    frequent = {t.lower() for t in technology_levels.get("frequent", [])}
    # minor is implicitly everything not in core or frequent

    def _bucket(tech: str) -> int:
        t = tech.lower()
        is_jd = t in kw_lower
        if t in core:
            return 0 if is_jd else 2
        if t in frequent:
            return 1 if is_jd else 3
        return 4  # minor

    reordered = sorted(technologies, key=_bucket)
    return reordered[:limit]


def _select_by_keyword_density(
    items: list[str], keywords: set[str], limit: int
) -> list[str]:
    """Select top items by keyword density. Tiebreak by content length (prefer substantive text)."""
    scored = [(i, _keyword_density(i, keywords), len(i), idx) for idx, i in enumerate(items)]
    scored.sort(key=lambda x: (-x[1], -x[2]))
    selected_indices = sorted([idx for _, _, _, idx in scored[:limit]])
    return [items[i] for i in selected_indices]


def _reorder_about_paragraphs(
    descriptions: list[str], keywords: set[str]
) -> list[str]:
    """Reorder about paragraphs so the highest keyword density comes first."""
    scored = [(desc, _keyword_density(desc, keywords)) for desc in descriptions]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [desc for desc, _ in scored]


def build_ats_resume(
    master_resume: dict,
    keywords: set[str],
    job_title: str,
    company_name: str,
) -> dict:
    """Build a customized ATS resume JSON.

    Args:
        master_resume: The full master resume dict (read-only, will be deep-copied)
        keywords: Set of matched keywords from the JD
        job_title: The job title from the posting
        company_name: The company name
    """
    resume = copy.deepcopy(master_resume)

    # Build full vocabulary once — used for bolding summary and about sections
    all_vocab = build_vocabulary(master_resume)

    # 1. Positions: reorder by similarity to job title
    resume["overviewData"]["positions"] = _reorder_positions(
        master_resume["overviewData"]["positions"], job_title
    )

    # 2. Summary: use master resume text, bold with full vocabulary
    summary_text = master_resume["summarySection"]["summary"]
    summary_text = inject_bold(summary_text, all_vocab)
    resume["summarySection"] = {
        "title": "Professional Summary",
        "summary": summary_text,
    }

    # 3. About section: bold with full vocabulary
    about_descriptions = _reorder_about_paragraphs(
        master_resume["aboutSection"]["descriptions"], keywords
    )
    about_descriptions = inject_bold_in_list(about_descriptions, all_vocab)
    resume["aboutSection"]["descriptions"] = about_descriptions

    # 4. Experiences: score to select top 3, then display in chronological order (most recent first)
    all_experiences = master_resume["experienceSection"]["experiences"]
    ranked = rank_experiences(all_experiences, keywords, top_n=3)

    # Re-sort selected experiences: "Present" first, then by end year descending
    def _sort_key(item):
        exp, score = item
        time_str = exp.get("time", "")
        if "present" in time_str.lower():
            return -9999  # Current job always first
        years = re.findall(r"\d{4}", time_str)
        end_year = int(years[-1]) if len(years) >= 2 else 0
        return -end_year  # Negate so higher years sort first

    ranked.sort(key=_sort_key)

    customized_experiences = []
    for idx, (exp, score) in enumerate(ranked):
        tech_limit = TECH_LIMITS[idx] if idx < len(TECH_LIMITS) else 6
        custom_exp = copy.deepcopy(exp)

        # Bold injection on descriptions and achievements
        custom_exp["description"] = inject_bold_in_list(
            custom_exp.get("description", []), keywords
        )
        custom_exp["achievements"] = inject_bold_in_list(
            custom_exp.get("achievements", []), keywords
        )

        # Select top descriptions/achievements by keyword density
        if len(custom_exp["description"]) > MAX_DESCRIPTIONS:
            custom_exp["description"] = _select_by_keyword_density(
                custom_exp["description"], keywords, MAX_DESCRIPTIONS
            )
        if len(custom_exp["achievements"]) > MAX_ACHIEVEMENTS:
            custom_exp["achievements"] = _select_by_keyword_density(
                custom_exp["achievements"], keywords, MAX_ACHIEVEMENTS
            )

        # Reorder and limit technologies (use usage levels from master resume)
        custom_exp["technologies"] = _reorder_technologies(
            exp["technologies"],
            keywords,
            tech_limit,
            exp.get("technology_levels"),
        )

        # Strip pipeline metadata — not part of the rendered output
        custom_exp.pop("technology_levels", None)
        customized_experiences.append(custom_exp)

    resume["experienceSection"]["title"] = "Professional Experience"
    resume["experienceSection"]["experiences"] = customized_experiences

    # 5. Recommendations: copy as-is (already in the deep copy)

    # 6. Remove funFactsSection
    resume.pop("funFactsSection", None)

    return resume
