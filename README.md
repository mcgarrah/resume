# Resume — mcgarrah.org/resume

A Jekyll-based resume site with multiple export formats, deployed at [mcgarrah.org/resume](https://mcgarrah.org/resume).

## Architecture

The resume is a single-source system: all content lives in `_data/data.yml` and is rendered into multiple output formats through different pipelines.

```
_data/data.yml (single source of truth)
    │
    ├── Jekyll (Ruby) ──────────────────────────────────────────────
    │   ├── index.html        → Brief view (collapsible details)
    │   ├── print.html        → Print view (expanded, styled)
    │   ├── machine.html      → Machine view (Schema.org microdata)
    │   ├── Pandoc plugin     → McGarrah-Resume.pdf (compact LaTeX)
    │   │                     → McGarrah-Resume.docx (Word)
    │   └── WeasyPrint        → McGarrah-Resume-styled.pdf (CSS-faithful)
    │
    └── Python (Jinja2 + XeLaTeX) ──────────────────────────────────
        └── LaTeX template    → McGarrah-Resume-latex.pdf (typeset)
                              → McGarrah-Resume-latex.tex (source)
```

## Design Decisions

### Dual Language Stack (Ruby + Python)

The project deliberately uses both Ruby and Python:

- **Ruby/Jekyll** — Site generation, Liquid templates, Pandoc plugin integration. Jekyll is the established static site generator and handles HTML views, SEO, sitemaps, and the primary build pipeline.

- **Python/Jinja2** — LaTeX template rendering and WeasyPrint PDF generation. Python was chosen for the export pipeline because:
  - Jinja2 handles LaTeX templating cleanly with custom delimiters (`<< >>`) that don't conflict with LaTeX's `{ }` syntax
  - WeasyPrint (Python) renders CSS faithfully for the styled PDF — something Pandoc's LaTeX backend cannot do
  - PyYAML reads the same `_data/data.yml` that Jekyll uses
  - The Python tooling runs post-build as a separate pipeline, not entangled with Jekyll's internals

This separation means the Jekyll site works independently (Ruby only), and the enhanced PDF exports are an additive layer (Python). Either can be modified without affecting the other.

### Three PDF Strategies

Each PDF serves a different purpose:

| File | Engine | Strengths | Use Case |
|------|--------|-----------|----------|
| `McGarrah-Resume.pdf` | Pandoc → LaTeX | Compact, reliable, auto-generated during Jekyll build | Default download, ATS submission |
| `McGarrah-Resume-styled.pdf` | WeasyPrint | CSS-faithful (flex, columns, borders render correctly) | Visual review, matches browser print view |
| `McGarrah-Resume-latex.pdf` | Jinja2 → XeLaTeX | Full typographic control, two-column skills, professional typesetting | High-quality print, LaTeX source available |

The Pandoc PDF is a stop-gap that works within Jekyll's build lifecycle. WeasyPrint may be retired once the LaTeX template matures. The LaTeX pipeline is the long-term solution for publication-quality output.

### Structured Subsections

Experience entries use a `subsections` array (not flat markdown with bold headings) to give Pandoc and LaTeX distinct heading levels. See `.kiro/specs/experience-subsections/` for the full design rationale.

## Prerequisites

### Ruby (Jekyll site)

```bash
ruby >= 3.2
bundler
pandoc
texlive (pdflatex)
```

### Python (PDF exports)

```bash
python >= 3.10
pip install -r requirements.txt  # weasyprint, jinja2, pyyaml
xelatex  # for LaTeX PDF compilation (texlive-xetex)
```

## Build

```bash
# Full build: site + all exports
bundle exec jekyll build        # HTML views + Pandoc PDF/DOCX
bin/generate-pdf.sh             # WeasyPrint styled PDF
bin/generate-latex.sh           # LaTeX typeset PDF + .tex source

# Development server
bundle exec jekyll serve --livereload
```

## Project Structure

```
_data/data.yml              # All resume content (single source)
_includes/                  # Jekyll partials (brief + print views)
_layouts/                   # Page layouts (default, print, machine)
_sass/                      # Browser stylesheets (CSS variables)
templates/resume.tex.j2     # Jinja2 LaTeX template
bin/generate-pdf.sh         # WeasyPrint PDF script
bin/generate-latex.sh       # LaTeX generation + compilation script
bin/generate-latex.py       # Python script: YAML → .tex via Jinja2
_config.yml                 # Jekyll config + Pandoc export CSS
```

## Deployment

GitHub Actions (`.github/workflows/jekyll.yml`) builds and deploys to GitHub Pages on push to `main`. The workflow:
1. Builds Jekyll (generates HTML + Pandoc PDF/DOCX)
2. Runs WeasyPrint for the styled PDF
3. Deploys `_site/` to GitHub Pages

The LaTeX PDF is generated locally (requires XeLaTeX + fonts) and is not part of the CI pipeline currently.

## Views

- **Brief** (`/resume/`) — Collapsible details, interactive
- **Print** (`/resume/print`) — Expanded, optimized for browser print/PDF
- **Machine** (`/resume/machine/`) — Schema.org microdata for ATS/search engines
