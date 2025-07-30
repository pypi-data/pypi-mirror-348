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

    # NOTE: I don't like this, ideally upstream application should handle searching by whatever case, but this is fine for now

    # Handle URLs without scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.strip("/")

    # Remove www. for consistency
    if netloc.startswith("www."):
        netloc = netloc[4:]

    names = []

    # Full path (netloc + path)
    if path:
        full_path = f"{netloc}/{path}"
        names.append(full_path)
        last_segment = path.split("/")[-1]
        names.append(last_segment)
        # Add lowercase version if original has uppercase
        if last_segment.lower() != last_segment:
            names.append(last_segment.lower())
    else:
        # Domain-only URLs
        names.append(netloc)
        # For domains like elfutils.org, extract the name part
        domain_parts = netloc.split(".")
        if len(domain_parts) > 1:
            if len(domain_parts) > 2:
                # For cases like poppler.freedesktop.org
                names.append(domain_parts[0])  # e.g., "poppler"
                names.append(domain_parts[1])  # e.g., "freedesktop"
            else:
                # For cases like elfutils.org
                names.append(domain_parts[0])  # e.g., "elfutils"

    return names
