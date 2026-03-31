"""Score and rank master resume experiences by keyword overlap with a JD."""

import re


def _normalize(text: str) -> str:
    return text.lower()


def _count_keyword_hits(text: str, keywords: set[str]) -> int:
    """Count how many keywords appear as substrings in text (case-insensitive)."""
    text_lower = _normalize(text)
    count = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            count += 1
    return count


def _recency_bonus(time_str: str) -> int:
    """Give a bonus for recent/current roles so they don't get buried.

    "Present" = 5 bonus points, otherwise extract end year and scale.
    """
    if not time_str:
        return 0
    if "present" in time_str.lower():
        return 5
    # Extract the end year (second year in "2014 - 2020")
    years = re.findall(r"\d{4}", time_str)
    if len(years) >= 2:
        end_year = int(years[-1])
        if end_year >= 2022:
            return 3
        if end_year >= 2020:
            return 1
    return 0


def score_experience(experience: dict, keywords: set[str]) -> int:
    """Score a single experience against a keyword set.

    Weights:
    - technologies array: exact match = 2 points each
    - description text: substring match = 1 point each
    - achievements text: substring match = 1 point each
    - recency bonus: current role = 5, recent = 3/1
    """
    score = 0
    kw_lower = {kw.lower() for kw in keywords}

    # Technologies: exact match (weight 2)
    for tech in experience.get("technologies", []):
        if tech.lower() in kw_lower:
            score += 2

    # Description: substring match (weight 1)
    descriptions = " ".join(experience.get("description", []))
    score += _count_keyword_hits(descriptions, keywords)

    # Achievements: substring match (weight 1)
    achievements = " ".join(experience.get("achievements", []))
    score += _count_keyword_hits(achievements, keywords)

    # Recency bonus
    score += _recency_bonus(experience.get("time", ""))

    return score


def rank_experiences(
    experiences: list[dict], keywords: set[str], top_n: int = 3
) -> list[tuple[dict, int]]:
    """Score all experiences and return top N sorted by score descending.

    Returns list of (experience, score) tuples.
    """
    scored = [(exp, score_experience(exp, keywords)) for exp in experiences]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
