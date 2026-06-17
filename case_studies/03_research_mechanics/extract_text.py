"""
extract_text.py — Extract text from the Tober et al. PDF using pymupdf.

Usage:
    python extract_text.py

Output:
    - Prints page count, character count, and a preview
    - Writes full extracted text to tober_2025_extracted.txt
"""

import pymupdf
from pathlib import Path

PDF_PATH = Path(__file__).parent / "tober_2025_alaskan_glacier_depths.pdf"
OUTPUT_PATH = Path(__file__).parent / "tober_2025_extracted.txt"


def extract(pdf_path: Path) -> str:
    """Extract all text from a PDF, page by page."""
    doc = pymupdf.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append(f"--- PAGE {i + 1} ---\n{text}")
    doc.close()
    return "\n".join(pages)


if __name__ == "__main__":
    print(f"Reading: {PDF_PATH.name}")
    text = extract(PDF_PATH)

    # Summary stats
    page_count = text.count("--- PAGE ")
    char_count = len(text)
    word_count = len(text.split())

    print(f"Pages:      {page_count}")
    print(f"Characters: {char_count:,}")
    print(f"Words:      {word_count:,}")
    print(f"\n{'='*60}")
    print("PREVIEW (first 2000 characters):")
    print("="*60)
    print(text[:2000])

    # Write full text to file
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"Full text written to: {OUTPUT_PATH.name}")
