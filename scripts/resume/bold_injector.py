"""Add <strong> tags around keyword matches in text strings."""

import re


def inject_bold(text: str, keywords: set[str]) -> str:
    """Wrap matching keywords with <strong> tags.

    - Matches longest keywords first to prevent partial matches
      (e.g., "AWS Lambda" before "AWS")
    - Case-insensitive matching, preserves original case
    - Skips text already inside <strong> tags
    """
    if not keywords:
        return text

    # Sort by length descending so longer terms match first
    sorted_keywords = sorted(keywords, key=len, reverse=True)

    for kw in sorted_keywords:
        # Build pattern that matches the keyword but NOT inside existing <strong> tags
        # Use negative lookbehind/lookahead for <strong> boundaries
        escaped = re.escape(kw)

        # For single-word keywords, use word boundaries
        if " " not in kw and "/" not in kw and "." not in kw:
            pattern = r"(?<!</strong>)(?<!<strong>)\b(" + escaped + r")\b(?!</strong>)"
        else:
            pattern = r"(?<!</strong>)(?<!<strong>)(" + escaped + r")(?!</strong>)"

        def _replacer(match: re.Match) -> str:
            # Check if already wrapped in <strong>
            start = match.start()
            prefix = text[:start] if start > 0 else ""
            if prefix.endswith("<strong>"):
                return match.group(0)
            return f"<strong>{match.group(0)}</strong>"

        text = re.sub(pattern, _replacer, text, flags=re.IGNORECASE)

    return text


def inject_bold_in_list(texts: list[str], keywords: set[str]) -> list[str]:
    """Apply bold injection to a list of strings."""
    return [inject_bold(t, keywords) for t in texts]
