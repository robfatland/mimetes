"""
extract_figures.py — Extract specific pages/figures from the paper PDF as images.

Uses pymupdf to render PDF pages to PNG at high resolution.
Figures 4a (bed elevation map) and 4b (ice thickness map) need to be identified
by page number — adjust PAGE_NUMBERS after visual inspection.

Usage:
    python extract_figures.py

Output:
    images/fig4a_bed_elevation.png
    images/fig4b_ice_thickness.png
"""

import pymupdf
from pathlib import Path

PDF_PATH = Path(__file__).parent / "tober_2025_alaskan_glacier_depths.pdf"
OUTPUT_DIR = Path(__file__).parent / "images"

# Figure 4 is on page 12 (index 11). Left half = 4a, right half = 4b.
PREVIEW_MODE = False
FIG4_PAGE = 11  # 0-indexed: page 12
DPI = 300  # High resolution for cropping


def preview_all_pages(pdf_path: Path, output_dir: Path):
    """Render all pages at low res so you can identify which contain Fig 4."""
    preview_dir = output_dir / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    print(f"PDF has {len(doc)} pages. Rendering previews...")

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=72)
        out_path = preview_dir / f"page_{i+1:02d}.png"
        pix.save(str(out_path))

    doc.close()
    print(f"Previews saved to: {preview_dir}/")
    print("Inspect these to find which pages contain Figures 4a and 4b.")
    print("Then set PREVIEW_MODE = False and FIG4_PAGES = [page_a, page_b]")


def extract_figures(pdf_path: Path, page_num: int, output_dir: Path):
    """Extract page and crop to just the figure areas (no line numbers, captions)."""
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    page = doc[page_num]

    # Render full page at high DPI
    pix = page.get_pixmap(dpi=DPI)
    full_path = output_dir / "fig4_full.png"
    pix.save(str(full_path))

    from PIL import Image
    img = Image.open(full_path)
    w, h = img.size

    # Crop coordinates — adjust these by visual inspection.
    # These define the bounding box of JUST the figure content
    # (excluding line numbers on left, caption below, header above).
    # Format: (left, top, right, bottom) in pixels at DPI=300
    #
    # For a letter-size page at 300 DPI: ~2550 x 3300 px
    # Adjust these values after inspecting fig4_full.png:
    TOP = int(h * 0.16)      # skip header/title area
    BOTTOM = int(h * 0.426)   # stop above caption
    LEFT_MARGIN = int(w * 0.080)   # skip line numbers
    MID = w // 2
    RIGHT_MARGIN = int(w * 0.92)  # skip right edge

    # Additional trim: 4a needs more off its left side, 4b needs more off its right
    FIG_A_LEFT_EXTRA = int(w * 0.03)   # extra left trim for 4a only
    FIG_B_RIGHT_EXTRA = int(w * 0.03)  # extra right trim for 4b only

    img_a = img.crop((LEFT_MARGIN + FIG_A_LEFT_EXTRA, TOP, MID, BOTTOM))
    img_b = img.crop((MID, TOP, RIGHT_MARGIN - FIG_B_RIGHT_EXTRA, BOTTOM))

    path_a = output_dir / "fig4a_bed_elevation.png"
    path_b = output_dir / "fig4b_ice_thickness.png"

    img_a.save(path_a)
    img_b.save(path_b)

    print(f"Full page: {w}x{h} px @ {DPI} DPI")
    print(f"Crop box: top={TOP}, bottom={BOTTOM}, left_margin={LEFT_MARGIN}")
    print(f"  → {path_a} ({img_a.size[0]}x{img_a.size[1]})")
    print(f"  → {path_b} ({img_b.size[0]}x{img_b.size[1]})")
    print()
    print("If the crop isn't right, adjust TOP/BOTTOM/LEFT_MARGIN/RIGHT_MARGIN")
    print(f"in the script. Reference: fig4_full.png is in {output_dir}/")

    # Keep full page for reference this time
    doc.close()


if __name__ == "__main__":
    if PREVIEW_MODE:
        preview_all_pages(PDF_PATH, OUTPUT_DIR)
    else:
        extract_figures(PDF_PATH, FIG4_PAGE, OUTPUT_DIR)
