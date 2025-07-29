"""
permalint: Lint URLs

Exports:
    - normalize_url: Normalize URLs so it's easy to figure out canonical sources of truth
    for packages
"""

from urllib.parse import urlparse


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
