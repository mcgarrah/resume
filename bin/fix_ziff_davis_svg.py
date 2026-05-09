#!/usr/bin/env python3
"""Convert the Ziff-Davis SVG (which has XML entities) to PDF."""
from pathlib import Path
import cairosvg

# Use unsafe=True to allow entity resolution
cairosvg.svg2pdf(
    url="assets/images/company-logos/ziff-davis-1990.svg",
    write_to="assets/images/company-logos/latex-logos/ziff-davis-1990.pdf",
    unsafe=True
)
print("Converted ziff-davis-1990.svg -> latex-logos/ziff-davis-1990.pdf")
