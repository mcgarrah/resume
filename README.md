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
    │   └── Pandoc plugin     → McGarrah-Resume.pdf (compact LaTeX)
    │                         → McGarrah-Resume.docx (Word)
    │
    └── Python (Jinja2 + XeLaTeX) ──────────────────────────────────
        └── Brief template    → McGarrah-Resume-brief.pdf (5 pages)
        └── Full template     → McGarrah-Resume-long.pdf (typeset)
                              → McGarrah-Resume-long.tex (source)
```

## Design Decisions

### Dual Language Stack (Ruby + Python)

The project deliberately uses both Ruby and Python:

- **Ruby/Jekyll** — Site generation, Liquid templates, Pandoc plugin integration. Jekyll is the established static site generator and handles HTML views, SEO, sitemaps, and the primary build pipeline.

- **Python/Jinja2** — LaTeX template rendering for PDF generation. Python was chosen for the export pipeline because:
  - Jinja2 handles LaTeX templating cleanly with custom delimiters (`<< >>`) that don't conflict with LaTeX's `{ }` syntax
  - PyYAML reads the same `_data/data.yml` that Jekyll uses
  - The Python tooling runs post-build as a separate pipeline, not entangled with Jekyll's internals

This separation means the Jekyll site works independently (Ruby only), and the enhanced PDF exports are an additive layer (Python). Either can be modified without affecting the other.

### PDF Strategies

Each PDF serves a different purpose:

| File | Engine | Strengths | Use Case |
|------|--------|-----------|----------|
| `McGarrah-Resume-brief.pdf` | Jinja2 → XeLaTeX | 5 pages, summaries only, early career consolidated | Primary download, recruiter-friendly |
| `McGarrah-Resume-long.pdf` | Jinja2 → XeLaTeX | Full typographic control, all subsections, 30+ pages | Deep-dive readers, complete history |
| `McGarrah-Resume.pdf` | Pandoc → LaTeX | Auto-generated during Jekyll build, compact | ATS submission, DOCX companion |

The Pandoc PDF is auto-generated as part of the Jekyll build lifecycle. The XeLaTeX PDFs (brief and full) are the primary outputs with professional typesetting.

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
pip install -r requirements.txt  # jinja2, pyyaml
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

# Generate LaTeX PDFs (requires jekyll build first)
source .venv/bin/activate
bin/generate-brief.sh           # XeLaTeX → McGarrah-Resume-brief.pdf (5 pages)
bin/generate-latex.sh           # XeLaTeX → McGarrah-Resume-long.pdf (full)

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
| `bin/generate-brief.sh` | `_data/data.yml` | `McGarrah-Resume-brief.pdf` | Jinja2 → XeLaTeX |
| `bin/generate-latex.sh` | `_data/data.yml` | `McGarrah-Resume-long.pdf`, `.tex` | Jinja2 → XeLaTeX |

All outputs land in `_site/downloads/`.

## Project Structure

```
_data/data.yml              # All resume content (single source)
_includes/                  # Jekyll partials (brief + print views)
_layouts/                   # Page layouts (default, print, machine)
_sass/                      # Browser stylesheets (CSS variables)
templates/resume.tex.j2     # Jinja2 LaTeX template (full)
templates/resume-brief.tex.j2  # Jinja2 LaTeX template (brief, 5 pages)
bin/generate-brief.sh       # Brief LaTeX PDF script
bin/generate-latex.sh       # Full LaTeX generation + compilation script
bin/generate-latex.py       # Python script: YAML → .tex via Jinja2
_config.yml                 # Jekyll config + Pandoc export CSS
```

## Deployment

GitHub Actions (`.github/workflows/jekyll.yml`) builds and deploys to GitHub Pages on push to `main`. The workflow:
1. Builds Jekyll (generates HTML + Pandoc PDF/DOCX)
2. Generates brief and full LaTeX PDFs via XeLaTeX
3. Deploys `_site/` to GitHub Pages

### Build Optimization: Cached APT Packages

The `Install Pandoc and LaTeX` step uses [`awalsh128/cache-apt-pkgs-action`](https://github.com/awalsh128/cache-apt-pkgs-action) to cache the TeX Live and Pandoc apt packages between runs. Without caching, this step takes 6+ minutes (downloading ~500MB of packages every build). With caching, subsequent runs restore from cache in seconds.

**If you change the LaTeX/Pandoc package list**, you must bump the `version` field in the workflow step to invalidate the cache:

```yaml
- name: Install Pandoc and LaTeX
  uses: awalsh128/cache-apt-pkgs-action@latest
  with:
    packages: pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra texlive-xetex fonts-texgyre
    version: 1.0  # ← bump this (e.g., 1.1) when changing packages
```

The `version` key is the cache key — same version means "use the cached result." Changing it forces a fresh `apt-get install` on the next run, which will then be cached under the new key.

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
