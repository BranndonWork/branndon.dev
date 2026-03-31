"""Extract technology keywords from job descriptions.

Two input paths:
- Path A: job-posting.md (markdown text) — match against vocabulary from master resume
- Path B: job-tracking.yaml / job-application.yaml — read tech_stack array directly
"""

import json
import re
from pathlib import Path

import yaml


def build_vocabulary(master_resume: dict) -> set[str]:
    """Build keyword vocabulary from all technology arrays in the master resume."""
    vocab = set()
    for exp in master_resume.get("experienceSection", {}).get("experiences", []):
        for tech in exp.get("technologies", []):
            vocab.add(tech)
    return vocab


def _normalize(text: str) -> str:
    return text.lower().strip()


def extract_from_markdown(md_text: str, vocabulary: set[str]) -> set[str]:
    """Match vocabulary terms against markdown job description text.

    Matches case-insensitively. For multi-word terms, checks for their presence
    as substrings. For single-word terms, uses word boundary matching to avoid
    false positives (e.g., "Go" matching "going").
    """
    md_lower = md_text.lower()
    matched = set()

    for term in vocabulary:
        term_lower = _normalize(term)
        if " " in term_lower or "/" in term_lower or "." in term_lower:
            # Multi-word or special char terms: substring match
            if term_lower in md_lower:
                matched.add(term)
        else:
            # Single-word terms: word boundary match to avoid false positives
            pattern = r"\b" + re.escape(term_lower) + r"\b"
            if re.search(pattern, md_lower):
                matched.add(term)

    return matched


def extract_from_yaml(yaml_data: dict) -> set[str]:
    """Extract tech_stack from structured YAML data."""
    tech_stack = (
        yaml_data.get("job_details", {}).get("tech_stack", [])
    )
    return set(tech_stack) if tech_stack else set()


def extract_from_yaml_text(yaml_data: dict, vocabulary: set[str]) -> set[str]:
    """Extract keywords by matching vocabulary against key_requirements and notes text."""
    text_parts = []
    key_reqs = yaml_data.get("job_details", {}).get("key_requirements", "")
    if key_reqs:
        text_parts.append(key_reqs)
    notes = yaml_data.get("notes", "")
    if notes:
        text_parts.append(notes)
    strengths = yaml_data.get("my_match", {}).get("strengths", [])
    if strengths:
        text_parts.extend(strengths)

    if not text_parts:
        return set()

    combined = "\n".join(text_parts)
    return extract_from_markdown(combined, vocabulary)


def extract_keywords(job_dir: Path, master_resume: dict) -> set[str]:
    """Extract keywords from all available JD sources in a job directory.

    Combines signals from all available sources:
    - job-posting.md: vocabulary matching against full markdown text
    - job-tracking.yaml: tech_stack array + vocabulary matching against key_requirements
    - job-application.yaml: tech_stack array (fallback)
    """
    vocabulary = build_vocabulary(master_resume)
    keywords = set()

    job_posting = job_dir / "job-posting.md"
    job_tracking = job_dir / "job-tracking.yaml"
    job_application = job_dir / "job-application.yaml"

    # Always try markdown first — it has the most signal
    if job_posting.exists():
        md_text = job_posting.read_text(encoding="utf-8")
        keywords.update(extract_from_markdown(md_text, vocabulary))

    # Also pull structured tech_stack + key_requirements from YAML
    for yaml_path in [job_tracking, job_application]:
        if yaml_path.exists():
            with open(yaml_path, encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
            yaml_keywords = extract_from_yaml(yaml_data)
            if yaml_keywords:
                keywords.update(yaml_keywords)
            # Also match vocabulary against text fields in YAML
            text_keywords = extract_from_yaml_text(yaml_data, vocabulary)
            keywords.update(text_keywords)

    return keywords


def get_job_title(job_dir: Path) -> str:
    """Extract job title from available YAML files."""
    for yaml_name in ["job-tracking.yaml", "job-application.yaml"]:
        yaml_path = job_dir / yaml_name
        if yaml_path.exists():
            with open(yaml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            title = data.get("title", "")
            if title:
                return title

    # Fallback: parse from job-posting.md header
    job_posting = job_dir / "job-posting.md"
    if job_posting.exists():
        first_line = job_posting.read_text(encoding="utf-8").split("\n")[0]
        return first_line.lstrip("# ").strip()

    # Last resort: parse from directory name
    return job_dir.name.replace("-", " ")


def get_company_name(job_dir: Path) -> str:
    """Extract company name from available YAML files."""
    for yaml_name in ["job-tracking.yaml", "job-application.yaml"]:
        yaml_path = job_dir / yaml_name
        if yaml_path.exists():
            with open(yaml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            company = data.get("company", "")
            if company:
                return company

    # Fallback: parse from job-posting.md
    job_posting = job_dir / "job-posting.md"
    if job_posting.exists():
        text = job_posting.read_text(encoding="utf-8")
        match = re.search(r"\*\*Company\*\*:\s*(.+)", text)
        if match:
            return match.group(1).strip()

    return job_dir.name.split("-")[0]
