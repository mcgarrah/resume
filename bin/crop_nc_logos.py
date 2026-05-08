#!/usr/bin/env python3
"""Crop NC DIT and NC DOR logos to the logo mark left of the vertical bar.

Layout of these logos:
  [NC state outline] [NCDIT or NCDOR text] | [Full department name]

The vertical bar '|' is a thin line separating the compact mark from
the full agency name. We want everything LEFT of that bar including
the state outline AND the acronym text.

The bar is located roughly 55-70% into the image width.
"""

from PIL import Image
from pathlib import Path

LOGOS_DIR = Path(__file__).parent.parent / "assets" / "images" / "company-logos"


def find_vertical_bar(img):
    """Find the vertical separator bar.
    
    Search between 40-75% of image width for a thin column of pixels
    that spans most of the image height, with empty space on both sides.
    """
    pixels = img.load()
    w, h = img.size
    
    # Search range: 40% to 75% of width
    search_start = int(w * 0.40)
    search_end = int(w * 0.75)
    
    # For each column, find the longest continuous vertical run of visible pixels
    best_x = None
    best_run = 0
    
    for x in range(search_start, search_end):
        max_run = 0
        current_run = 0
        for y in range(h):
            if pixels[x, y][3] > 30:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        # Bar should span >50% of height
        if max_run > h * 0.5:
            # Check that 10px to the left is mostly empty (gap before bar)
            left_check_x = x - 10
            if left_check_x > 0:
                left_content = sum(1 for y in range(h) if pixels[left_check_x, y][3] > 30)
                if left_content < h * 0.15:  # mostly empty to the left
                    if max_run > best_run:
                        best_x = x
                        best_run = max_run
    
    if best_x:
        print(f"  Found vertical bar at x={best_x} (run={best_run}/{h})")
        # Include a few pixels before the bar for padding
        return best_x - 5
    
    # Fallback
    print(f"  No bar found in range {search_start}-{search_end}, using 60%")
    return int(w * 0.60)


def crop_logo(input_name, output_name):
    """Crop a logo PNG to the mark portion (left of vertical bar)."""
    input_path = LOGOS_DIR / input_name
    output_path = LOGOS_DIR / output_name

    img = Image.open(input_path).convert("RGBA")
    print(f"\n{input_name}: {img.size[0]}x{img.size[1]}")

    crop_x = find_vertical_bar(img)
    print(f"  Cropping at x={crop_x}")

    cropped = img.crop((0, 0, crop_x, img.size[1]))

    # Trim transparent padding
    bbox = cropped.getbbox()
    if bbox:
        cropped = cropped.crop(bbox)

    cropped.save(output_path, "PNG", optimize=True)
    size_kb = output_path.stat().st_size / 1024
    print(f"  Saved: {output_name} ({cropped.size[0]}x{cropped.size[1]}, {size_kb:.1f} KB)")


if __name__ == "__main__":
    crop_logo("nc_dit_logo.png", "nc_dit_mark.png")
    crop_logo("nc_dor_logo.png", "nc_dor_mark.png")
    print("\nDone.")
