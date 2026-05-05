# Resume Site Refactor — Ground-Up Jekyll Rebuild

## Motivation

The current resume site carries significant legacy from the original [orbit-theme](https://github.com/sharu725/developer-theme) template (circa 2017):

- **Bootstrap 3.4.1 + jQuery** — Loaded via CDN and local plugins for a site that uses CSS Grid. The only jQuery usage is animating skill bars (which we're removing).
- **Font Awesome 6.x via CDN** — Full icon library for ~15 icons.
- **IE8/IE9 conditional comments and shims** — Dead code.
- **compress.html layout** — Liquid-based HTML minifier adding complexity for negligible benefit.
- **Multi-skin SCSS** — 9 color themes when we use exactly one (ceramic).
- **`github-pages` gem** — 80+ transitive dependencies for a site deployed via GitHub Actions.
- **Pandoc `title_cleanup` regex gymnastics** — 16 patterns to strip HTML that shouldn't be in the export path in the first place.
- **Sidebar layout** — Worked in 2017, but wastes horizontal space on a content-dense resume.

## Design Goals

### 1. Three Views, One Data Source

All views render from `_data/data.yml`. No content duplication.

| View | URL | Purpose | Audience |
|------|-----|---------|----------|
| **Brief** | `/resume/` | Concise, scannable — summaries only, collapsible details | Recruiters, hiring managers |
| **Print** | `/resume/print/` | Fully expanded, optimized for PDF/DOCX export | ATS systems, deep-dive readers |
| **Machine** | `/resume/machine/` | Structured JSON-LD + semantic HTML, no visual chrome | AI agents, HR system ingestion |

### 2. Light/Dark Mode (OS-Aware)

Use `prefers-color-scheme` media query with CSS custom properties. No JavaScript toggle needed — the site respects the user's OS setting automatically.

```css
:root {
  --bg: #ffffff;
  --text: #3F4650;
  --accent: #4B6A78;
  --muted: #97AAC3;
  --surface: #f5f5f5;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a2e;
    --text: #e0e0e0;
    --accent: #7fb3c8;
    --muted: #8899aa;
    --surface: #16213e;
  }
}
```

### 3. Modern Single-Column Layout (No Sidebar)

Replace the sidebar with a compact header block:

```text
┌─────────────────────────────────────────────────┐
│  [Avatar]  Michael McGarrah                     │
│            Engineering Leader | Architect | PE  │
│            📧 email  🔗 linkedin  🐙 github    │
│            📄 PDF    📝 DOCX     🖨️ Print      │
└─────────────────────────────────────────────────┘
│                                                 │
│  Career Profile                                 │
│  ─────────────────────────────────────────────  │
│  Education                                      │
│  ─────────────────────────────────────────────  │
│  Experience                                     │
│  ...                                            │
└─────────────────────────────────────────────────┘
```

Benefits:

- Full width for content (resume text is dense — it needs the space)
- Contact info is above the fold, not buried in a narrow column
- Mobile-friendly without a breakpoint that collapses the sidebar
- Pandoc export is trivial — linear HTML maps directly to linear PDF

### 4. AI/Machine-Friendly View

The `/resume/machine/` view provides:

- **JSON-LD structured data** using [Schema.org Resume](https://schema.org/Person) vocabulary
- **Semantic HTML5** — `<article>`, `<section>`, `<header>`, `<time datetime="...">`, `<address>`
- **Microdata attributes** on all content elements
- **No visual styling** — raw semantic markup that AI agents and HR systems can parse
- **`<meta name="robots" content="index, follow">` with structured data hints**

This makes the resume trivially parseable by:

- LinkedIn profile importers
- ATS systems (Greenhouse, Lever, Workday)
- AI recruiting agents (Claude, GPT-based HR tools)
- Google's structured data rich results

### 5. Pandoc Export Without Regex Hacks

The current `title_cleanup` has 16 regex patterns because the HTML mixes presentation (sidebar, icons, CDN links) with content. The refactored structure eliminates this:

**Current problem:** Pandoc sees the sidebar, Font Awesome icon stacks, contact list items, and language sections — all of which must be stripped via regex.

**Solution:** The print layout (`/resume/print/`) renders *only* content-bearing HTML. No sidebar, no icon decorations, no elements that need stripping. The `print-header.html` include provides name/contact in a structure Pandoc handles natively.

Target: **zero `title_cleanup` patterns** (or at most 1-2 for edge cases).

### 6. Preserve Assets

All files under `assets/` carry forward:

- `assets/images/` — Avatar, company logos (used in future experience section enhancement)
- `assets/pdf/` — Static PDF snapshots (historical)
- `assets/css/main.scss` — Rebuilt from scratch but same path
- `assets/icons.svg` — New SVG sprite (replaces CDN Font Awesome)

The `assets/plugins/` directory (Bootstrap, Font Awesome, jQuery) is removed — these are the legacy dependencies being eliminated.

## Constraints

1. **`baseurl: /resume`** — Blog nav links to `/resume/`, About page links to `/resume/print`.
2. **`_data/data.yml`** — Single content source, unchanged.
3. **Pandoc PDF/DOCX** — `jekyll-pandoc-exports` continues to generate `/resume/downloads/print.pdf` and `.docx`.
4. **Local dev** — `bundle exec jekyll serve` at `http://localhost:4000/resume/`.
5. **GitHub Actions** — Existing deployment workflow (or simplified version).
6. **Ruby 3.3.11** via rbenv — `.ruby-version` stays.

## Integration with mcgarrah.github.io

| Blog reference | Resume URL | Status |
|----------------|-----------|--------|
| Navigation sidebar icon | `/resume/` | Stable |
| About page "full print version" | `/resume/print` | Stable |
| PDF download link | `/resume/downloads/print.pdf` | Stable |
| DOCX download link | `/resume/downloads/print.docx` | Stable |
| New: machine-readable | `/resume/machine/` | New URL, no existing links |

## Technology Choices

### Keep
- Jekyll 4.4.x
- `jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-pandoc-exports`
- SCSS (but minimal — one variables file, one layout file)
- `webrick` for local dev

### Drop
- Bootstrap (any version)
- jQuery
- Font Awesome CDN
- `github-pages` gem
- `compress.html` Liquid minifier
- IE conditional comments
- Multi-skin SCSS system
- Skill bar animations

### Add
- CSS custom properties for light/dark mode
- `prefers-color-scheme` media query
- SVG sprite for icons (inline, no external request)
- JSON-LD structured data (machine view)
- `<details>`/`<summary>` for brief view (native HTML, no JS)
- `@media print` stylesheet (browser print = clean output)

## Proposed File Structure

```
resume/
├── _data/data.yml              # Content (unchanged)
├── _includes/
│   ├── head.html               # Minimal <head> — no CDNs, no shims
│   ├── header.html             # Name, tagline, contact links (replaces sidebar)
│   ├── career-profile.html     # Summary section
│   ├── education.html          # Brief view (details/summary)
│   ├── education-print.html    # Print view (expanded)
│   ├── experiences.html        # Brief view
│   ├── experiences-print.html  # Print view
│   ├── certifications.html     # Cert list
│   ├── projects.html           # Selected projects
│   ├── publications.html       # Academic pubs
│   ├── skills.html             # Categorized skills (text list, no bars)
│   ├── icons.svg               # Inline SVG sprite
│   ├── print-header.html       # Compact header for Pandoc-friendly print
│   ├── print-links.html        # Footer URLs for PDF readers
│   └── structured-data.html    # JSON-LD for machine view
├── _layouts/
│   ├── default.html            # Brief view layout
│   ├── print.html              # Print/export layout (linear, no chrome)
│   └── machine.html            # Machine-readable layout (semantic only)
├── _sass/
│   ├── _variables.scss         # Colors (light + dark), fonts, spacing
│   └── _layout.scss            # All styles (~200 lines target)
├── assets/
│   ├── css/main.scss           # SCSS entry point
│   ├── images/                 # Avatar, company logos (preserved)
│   ├── pdf/                    # Historical PDF snapshots (preserved)
│   └── icons.svg               # SVG sprite file
├── _config.yml                 # Simplified config
├── index.html                  # /resume/ (brief view)
├── print.html                  # /resume/print/ (print view)
├── machine.html                # /resume/machine/ (AI/robot view)
├── Gemfile                     # Minimal deps (no github-pages)
├── .ruby-version               # 3.3.11
└── .github/workflows/jekyll.yml
```

## Refactoring Phases

### Phase 1 — Layout and Structure
- New `_layouts/default.html` — single-column, CSS Grid header block
- New `_sass/` — variables with light/dark custom properties, single layout file
- New `_includes/header.html` — replaces sidebar with compact contact header
- SVG sprite with ~12 icons
- Verify renders at `localhost:4000/resume/`

### Phase 2 — Print View and Pandoc
- New `_layouts/print.html` — linear HTML, no sidebar, no icon decorations
- Restructure so Pandoc needs zero (or minimal) `title_cleanup` patterns
- Simplify `_config.yml` pandoc_exports section
- Test PDF and DOCX output

### Phase 3 — Machine View
- New `_layouts/machine.html` — semantic HTML + JSON-LD
- Schema.org Person/Organization/EducationalOrganization markup
- Validate with Google's Rich Results Test
- Validate parseable by common ATS systems

### Phase 4 — Polish and Cleanup
- Light/dark mode testing across browsers
- `@media print` stylesheet for browser print
- Mobile responsive (single breakpoint at ~768px)
- Accessibility audit (headings, ARIA, contrast ratios in both modes)
- Lighthouse scores (Performance, Accessibility, SEO)
- Remove `assets/plugins/` directory
- Remove legacy files (`compress.html`, `_sass/skins/`, etc.)

## Local Development

```bash
cd ~/github/resume
git checkout refactor
bundle install
bundle exec jekyll serve
# Brief: http://localhost:4000/resume/
# Print: http://localhost:4000/resume/print/
# Machine: http://localhost:4000/resume/machine/
```

Side-by-side comparison with current site:
```bash
# Terminal 1 — current
git checkout main && bundle exec jekyll serve --port 4001

# Terminal 2 — refactor
git checkout refactor && bundle exec jekyll serve --port 4000
```

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-07-XX | Created `refactor` branch | Explore ground-up rebuild without risking main |
| | Drop sidebar → compact header | Full-width content, better mobile, simpler Pandoc |
| | Light/dark via `prefers-color-scheme` | OS-aware, zero JS, CSS custom properties |
| | Add `/resume/machine/` view | AI agents and ATS systems need structured data |
| | Target zero `title_cleanup` regexes | Print layout renders only exportable content |
| | Drop Bootstrap, jQuery, CDN FA | Dead weight — CSS Grid + SVG sprite replaces all |
| | Keep `_data/data.yml` unchanged | Content is correct; only presentation rebuilds |
| | Keep `baseurl: /resume` | Blog integration depends on stable URL paths |
| | Preserve `assets/images/` and `assets/pdf/` | Company logos and historical PDFs stay |
| | Drop `assets/plugins/` | Bootstrap/jQuery/FA local copies no longer needed |
| | Three views from one data source | Brief (recruiters), Print (ATS/PDF), Machine (AI) |
