#!/usr/bin/env python3
"""Convert SVG logos to PDF for XeLaTeX inclusion.

XeLaTeX can include PDF and PNG/JPG images but not SVG directly.
This script converts all SVG logos to PDF in a latex-logos/ subdirectory,
and copies PNG/JPG logos there too for a single include path.

Output: assets/images/company-logos/latex-logos/
"""

import shutil
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("ERROR: cairosvg not installed. Run: pip install cairosvg")
    raise SystemExit(1)

LOGOS_DIR = Path("assets/images/company-logos")
OUTPUT_DIR = LOGOS_DIR / "latex-logos"
OUTPUT_DIR.mkdir(exist_ok=True)


def convert_svg_to_pdf(svg_path, pdf_path):
    """Convert SVG to PDF using cairosvg."""
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))


def main():
    print("Converting logos for XeLaTeX...")

    # Convert SVGs to PDF
    svg_files = sorted(LOGOS_DIR.glob("*.svg"))
    for svg in svg_files:
        pdf_name = svg.stem + ".pdf"
        pdf_path = OUTPUT_DIR / pdf_name
        try:
            convert_svg_to_pdf(svg, pdf_path)
            print(f"  SVG→PDF: {svg.name} → latex-logos/{pdf_name}")
        except Exception as e:
            print(f"  FAILED: {svg.name} — {e}")

    # Copy PNG/JPG files as-is (XeLaTeX handles these directly)
    for ext in ("*.png", "*.jpg"):
        for img in sorted(LOGOS_DIR.glob(ext)):
            dest = OUTPUT_DIR / img.name
            shutil.copy2(img, dest)
            print(f"  Copied: {img.name} → latex-logos/{img.name}")

    print(f"\nDone. Output: {OUTPUT_DIR}/")
    print(f"Total files: {len(list(OUTPUT_DIR.iterdir()))}")


if __name__ == "__main__":
    main()
