# bin/ — Build & Utility Scripts

Scripts for generating PDFs, converting assets, and validating the resume site.

## Active Scripts

These are part of the ongoing build pipeline or useful for repeated tasks.

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `generate-latex.py` | Renders Jinja2 LaTeX templates from `_data/data.yml` and optionally compiles to PDF with XeLaTeX. Core of the PDF pipeline. | Every build (called by `jekyll-start.sh`) |
| `generate-latex.sh` | Shell convenience wrapper for `generate-latex.py` — generates the full (long) PDF. | Manual PDF regeneration |
| `generate-brief.sh` | Shell convenience wrapper — generates the brief PDF. | Manual PDF regeneration |
| `generate_og_image.py` | Generates the 1200×630 Open Graph social preview image (`assets/images/og-resume.png`) from the profile photo. Uses Pillow. | When profile photo or design changes |
| `validate_seo.py` | Validates SEO tags (title, canonical, og:image, JSON-LD) across all three views against the built `_site/`. | After builds, before deploy |
| `convert_logos_to_png.py` | Converts all SVG logos to 400px PNG with transparent backgrounds for XeLaTeX inclusion. Outputs to `assets/images/company-logos/latex-logos/`. | When logos are added or modified |
| `crop_nc_logos.py` | Crops NC DIT and NC DOR full-width logos to just the mark (left of vertical bar). Uses Pillow pixel scanning to find the separator. | If NC agency logos need re-cropping |

## Usage

All scripts should be run from the resume project root with the `.venv` activated:

```bash
cd ~/github/resume
source .venv/bin/activate

# Generate all PDFs
python3 bin/generate-latex.py --template resume-ultra-brief.tex.j2 \
  --output _site/downloads/McGarrah-Resume-ultra-brief.tex --compile

python3 bin/generate-latex.py --template resume-brief.tex.j2 \
  --output _site/downloads/McGarrah-Resume-brief.tex --compile

python3 bin/generate-latex.py \
  --output _site/downloads/McGarrah-Resume-long.tex --compile

# Convert logos for LaTeX
python3 bin/convert_logos_to_png.py

# Validate SEO
python3 bin/validate_seo.py

# Regenerate OG image
python3 bin/generate_og_image.py
```

## Dependencies

- **Python 3.10+** with `.venv` (see `requirements.txt`)
- **Pillow** — image generation and manipulation
- **cairosvg** — SVG to PNG conversion
- **Jinja2** — LaTeX template rendering
- **PyYAML** — reading `_data/data.yml`
- **XeLaTeX** — PDF compilation (MacTeX on macOS, texlive-xetex on Ubuntu)

## archive/ — One-Time Scripts

Scripts that were run once to perform a specific migration or transformation.
Kept for reference in case the operation needs to be repeated or understood.

| Script | What It Did | Date |
|--------|-------------|------|
| `reorganize_logos.py` | Renamed all logos to consistent `{company}-{variant}.{ext}` scheme, moved originals to `original/`, old JPGs to `archive/` | May 2026 |
| `update_preview_refs.py` | Updated `preview.html` image references after the logo rename | May 2026 |
| `add_anchors.py` | Added stable `anchor` fields to all 27 experience + 3 education entries in `_data/data.yml` | May 2026 |
| `add_links_to_ultra_brief.py` | Wrapped job titles in `ultra-brief.html` with hyperlinks to full resume anchors | May 2026 |
| `add_section_anchors.py` | Added `id` attributes to section `<h2>` elements in all view templates | May 2026 |
| `fix_ziff_davis_svg.py` | Converted Ziff-Davis SVG (with XML entities) to PDF using `unsafe=True`. Logic now handled by `convert_logos_to_png.py`. | May 2026 |

## Deleted Scripts

| Script | Reason |
|--------|--------|
| `convert_logos_for_latex.py` | Deprecated — converted SVGs to PDF. Replaced by `convert_logos_to_png.py` which produces PNGs with transparent backgrounds instead. |
