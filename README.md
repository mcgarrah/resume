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

**macOS:**

```bash
# Ruby 3.3.11 via rbenv (see .ruby-version)
brew install rbenv ruby-build
rbenv install 3.3.11
rbenv local 3.3.11

# Bundler + gems
gem install bundler
bundle install

# Pandoc (for PDF/DOCX export during Jekyll build)
brew install pandoc

# BasicTeX or MacTeX (provides pdflatex for Pandoc)
brew install --cask basictex
```

> **macOS note:** Always launch VS Code from a terminal (`code .`), not from Dock/Spotlight.
> GUI-launched VS Code inherits `launchd` PATH which doesn't include rbenv shims.
> See `.amazonq/rules/ruby-environment.md` for the full rbenv troubleshooting guide.

**WSL2 / Ubuntu 24.04:**

```bash
# Build dependencies for rbenv/ruby-build
sudo apt update
sudo apt install -y build-essential libssl-dev libreadline-dev zlib1g-dev \
  libyaml-dev libffi-dev libgdbm-dev

# rbenv + ruby-build
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash
echo 'eval "$(~/.rbenv/bin/rbenv init - bash)"' >> ~/.bashrc
source ~/.bashrc

# Ruby 3.3.11
rbenv install 3.3.11
rbenv local 3.3.11

# Bundler + gems
gem install bundler
bundle install

# Pandoc + LaTeX (for PDF/DOCX export during Jekyll build)
sudo apt install -y pandoc texlive-latex-base texlive-fonts-recommended
```

### Python (PDF exports)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # weasyprint, jinja2, pyyaml
```

### XeLaTeX (typeset LaTeX PDF)

The LaTeX pipeline (`bin/generate-latex.sh`) requires XeLaTeX with Helvetica Neue:

**macOS:**

```bash
# Full MacTeX (includes XeLaTeX + all fonts) — ~4GB
brew install --cask mactex

# Or minimal: BasicTeX + XeLaTeX packages
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install collection-xetex collection-fontsrecommended \
  parskip needspace fancyhdr lastpage
```

Helvetica Neue is bundled with macOS.

**WSL2 / Ubuntu 24.04:**

```bash
sudo apt install -y texlive-xetex texlive-fonts-recommended texlive-latex-extra \
  texlive-fonts-extra fonts-texgyre
```

Helvetica Neue is not available on Linux. The template falls back to TeX Gyre Heros
(a metric-compatible Helvetica clone). To use the exact same font as macOS, install
Helvetica Neue manually in `~/.local/share/fonts/` and run `fc-cache -fv`.

## Build

```bash
# Full build: site + Pandoc exports (PDF/DOCX)
bundle exec jekyll build

# Generate additional PDF formats (requires jekyll build first)
source .venv/bin/activate
bin/generate-pdf.sh             # WeasyPrint → McGarrah-Resume-styled.pdf
bin/generate-latex.sh           # YAML → .tex → McGarrah-Resume-latex.pdf (via XeLaTeX)

# Development server (livereload + incremental)
./jekyll-start.sh               # http://localhost:4000/resume/
./jekyll-start.sh --clean       # Hard clean cache before starting

# Clean build artifacts
./jekyll-clean.sh               # Soft clean (_site/, .jekyll-metadata)
./jekyll-clean.sh --hard        # Also removes .jekyll-cache
```

### Export Scripts

| Script | Input | Output | Engine |
|--------|-------|--------|--------|
| `bundle exec jekyll build` | `_data/data.yml` | `McGarrah-Resume.pdf`, `.docx` | Pandoc → LaTeX |
| `bin/generate-pdf.sh` | `_site/print.html` | `McGarrah-Resume-styled.pdf` | WeasyPrint |
| `bin/generate-latex.sh` | `_data/data.yml` | `McGarrah-Resume-latex.pdf`, `.tex` | Jinja2 → XeLaTeX |

All outputs land in `_site/downloads/`.

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

## Acknowledgments

This project originally started as a fork of [online-cv](https://github.com/sharu725/online-cv)
by [Sharath Kumar](https://github.com/sharu725), a Jekyll theme based on the
[Orbit](http://themes.3rdwavemedia.com/) design by Xiaoying Riley at 3rd Wave Media.
The site has since been completely rewritten — new layouts, new build pipelines, new
export system, new data schema — and shares no code with the original template. The
acknowledgment here is for the starting point that got the project off the ground in 2017.
