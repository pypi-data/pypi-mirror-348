"""
permalint: Lint URLs

Exports:
    - normalize_url: Normalize URLs so it's easy to figure out canonical sources of truth
    for packages
"""

from typing import List, Optional, Set
from urllib.parse import ParseResult, urlparse


def normalize_url(url: str) -> str:
    """
    Normalize a URL according to CHAI database rules:
    - Ignore protocol (http, https, etc.)
    - For GitHub URLs, keep only owner/repo
    - Remove query strings and fragments
    - Remove trailing slashes
    - Lowercase the domain
    """
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    # Remove www. for consistency
    if netloc.startswith("www."):
        netloc = netloc[4:]

    # GitHub special handling
    if netloc == "github.com":
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2:
            return f"github.com/{parts[0]}/{parts[1]}"
        elif parts:
            return f"github.com/{parts[0]}"
        else:
            return "github.com"

    # Remove query and fragment, ignore protocol
    return f"{netloc}{path}" if netloc else path


def guess_url(urls: List[str]) -> Optional[str]:
    """
    Given a list of URLs, return the most likely canonical URL.
    """
    results: Set[ParseResult] = set()
    for url in urls:
        normalized = normalize_url(url)
        if normalized in urls:
            results.add(normalized)

    if len(results) == 1:
        return results.pop()
    else:
        return None


def possible_names(url: str) -> List[str]:
    """
    Given a URL, return a list of possible names for the package.
    The list is ordered by relevance to the input.
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.strip("/")

    # Remove www. for consistency
    if netloc.startswith("www."):
        netloc = netloc[4:]

    names = []
    # Full path (netloc + path)
    if path:
        names.append(f"{netloc}/{path}")
    else:
        names.append(netloc)

    # Path segments
    if path:
        segments = path.split("/")
        # Add last segment (most specific)
        if segments:
            names.append(segments[-1])
        # Add all individual segments (if not already present)
        for seg in segments:
            if seg not in names:
                names.append(seg)

    # Add just the domain
    if netloc not in names:
        names.append(netloc)

    return names
