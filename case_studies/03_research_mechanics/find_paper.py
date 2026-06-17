"""
find_paper.py — Search for a paper using the Semantic Scholar API
and download it from its open-access source.

This is Step 1 of the presentation: demonstrating programmatic paper discovery.
No AWS services are used here — just the free Semantic Scholar REST API.

Usage:
    python find_paper.py

What it does:
    1. Searches Semantic Scholar for the paper by keywords + author
    2. Displays metadata (title, authors, year, DOI, venue)
    3. Checks for an open-access PDF URL
    4. Downloads the PDF if available

API docs: https://api.semanticscholar.org/api-docs/
"""

import requests
import json
import time
import os
from pathlib import Path

# --- Configuration ---
# Search parameters for our target paper
QUERY = "Alaskan glacier depths airborne radar sounding IceBridge"
AUTHOR_FILTER = "Tober"
FIELDS = "title,authors,year,abstract,externalIds,openAccessPdf,venue,url"

# Semantic Scholar API endpoint
SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

# Optional API key — set via environment variable or paste here.
# Request a free key at: https://www.semanticscholar.org/product/api
# Without a key you share the anonymous rate limit pool (often saturated).
S2_API_KEY = os.environ.get("S2_API_KEY", "")

OUTPUT_DIR = Path(__file__).parent

# Retry settings for rate limiting (HTTP 429)
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


def search_papers(query: str, fields: str, limit: int = 5) -> list:
    """Search Semantic Scholar for papers matching the query, with retry on 429."""
    params = {
        "query": query,
        "fields": fields,
        "limit": limit,
    }
    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
        print("(Using S2 API key)")

    print(f"Searching Semantic Scholar for: '{query}'")
    print(f"URL: {SEARCH_URL}?query={query}&fields={fields}&limit={limit}")
    print()

    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(SEARCH_URL, params=params, headers=headers)

        if response.status_code == 429:
            wait = RETRY_DELAY_SECONDS * attempt
            print(f"  Rate limited (429). Retry {attempt}/{MAX_RETRIES} "
                  f"in {wait}s...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    print("ERROR: Still rate-limited after retries. Try again in a minute,")
    print("       or set S2_API_KEY environment variable for dedicated limits.")
    print("       Request a free key: https://www.semanticscholar.org/product/api")
    return []


def filter_by_author(papers: list, author_name: str) -> list:
    """Filter results to papers with a matching author surname."""
    matches = []
    for paper in papers:
        authors = paper.get("authors", [])
        if any(author_name.lower() in a.get("name", "").lower() for a in authors):
            matches.append(paper)
    return matches


def display_paper(paper: dict) -> None:
    """Pretty-print paper metadata."""
    print("=" * 60)
    print(f"TITLE:   {paper.get('title', 'N/A')}")
    print(f"AUTHORS: {', '.join(a['name'] for a in paper.get('authors', []))}")
    print(f"YEAR:    {paper.get('year', 'N/A')}")
    print(f"VENUE:   {paper.get('venue', 'N/A')}")

    # External IDs (DOI, ArXiv, etc.)
    ext_ids = paper.get("externalIds", {})
    if ext_ids:
        print(f"DOI:     {ext_ids.get('DOI', 'N/A')}")
        if "ArXiv" in ext_ids:
            print(f"ArXiv:   {ext_ids['ArXiv']}")

    # Open access PDF
    oa = paper.get("openAccessPdf")
    if oa:
        print(f"PDF URL: {oa.get('url', 'N/A')}")
    else:
        print("PDF URL: No open-access PDF found via Semantic Scholar")

    print(f"S2 URL:  {paper.get('url', 'N/A')}")
    print("=" * 60)

    # Abstract preview
    abstract = paper.get("abstract", "")
    if abstract:
        preview = abstract[:500] + ("..." if len(abstract) > 500 else "")
        print(f"\nABSTRACT:\n{preview}")


def download_pdf(url: str, filename: str) -> Path:
    """Download a PDF from the given URL."""
    output_path = OUTPUT_DIR / filename
    print(f"\nDownloading PDF to: {output_path.name}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"Downloaded: {size_mb:.1f} MB")
    return output_path


if __name__ == "__main__":
    # Step 1: Search
    papers = search_papers(QUERY, FIELDS)

    if not papers:
        print("No papers found.")
        raise SystemExit(1)

    print(f"Found {len(papers)} result(s)")

    # Step 2: Filter by author
    matches = filter_by_author(papers, AUTHOR_FILTER)

    if matches:
        print(f"Filtered to {len(matches)} paper(s) by author '{AUTHOR_FILTER}'")
        target = matches[0]
    else:
        print(f"No exact author match for '{AUTHOR_FILTER}', showing top result")
        target = papers[0]

    # Step 3: Display metadata
    print()
    display_paper(target)

    # Step 4: Download PDF if available
    oa = target.get("openAccessPdf")
    if oa and oa.get("url"):
        download_pdf(oa["url"], "tober_2025_alaskan_glacier_depths.pdf")
    else:
        # Fallback: try EarthArXiv directly if we have the DOI
        ext_ids = target.get("externalIds", {})
        doi = ext_ids.get("DOI", "")
        if doi:
            print(f"\nNo S2 open-access link. Paper DOI: {doi}")
            print("You can download manually from EarthArXiv:")
            print(f"  https://doi.org/{doi}")
        else:
            print("\nNo open-access PDF or DOI found.")

    # Save metadata as JSON for downstream use
    meta_path = OUTPUT_DIR / "paper_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=2, ensure_ascii=False)
    print(f"\nMetadata saved to: {meta_path.name}")
