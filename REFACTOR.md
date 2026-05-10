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

### 6. Interactive Features (Search + AI Agent)

The site adds purposeful interactivity beyond the static resume presentation:

#### In-Browser Search

Client-side search over resume content, built at deploy time:

- **Pagefind** (recommended) — Rust-based static search indexer. Runs during GitHub Actions build, ships a ~100KB WASM bundle. Zero runtime dependencies, works offline, indexes all three views.
- Alternative: Build-time JSON index from `_data/data.yml` + vanilla JS fuzzy matcher (~50 lines).
- Search UI lives in the brief view header area — excluded from print and machine views.

#### AI Agent Integration

An external AI agent provides conversational interaction with the resume for recruiters and interested parties:

- **Chat widget** — Floating button → chat panel on the brief view. Small JS component that calls an external API. The resume site stays static; intelligence lives elsewhere.
- **Knowledge base** — The `/resume/machine/` JSON-LD view serves dual purpose: SEO structured data AND the agent's grounding context. Optionally extended with blog content from mcgarrah.org.
- **Hosting options** (to be decided):
  - AWS Lambda + API Gateway (leverages existing AWS accounts and EKS expertise)
  - Cloudflare Workers (edge-deployed, minimal cold start)
  - Third-party widget (Chatbase, CustomGPT, or similar — fastest to prototype)
- **Graceful degradation** — Chat widget is non-essential. Site is fully functional without it. Widget loads asynchronously and doesn't block page render.

#### JavaScript Principle (Revised)

> **No JavaScript for presentation.** Layout, styling, and content rendering are pure HTML/CSS. JavaScript is reserved for *interactive features* (search, AI chat) that provide genuine user value and degrade gracefully when disabled.

#### Open Questions

- Where should the AI agent be hosted? (AWS Lambda, third-party, edge worker)
- Should the agent know blog content from mcgarrah.org in addition to resume data?
- Privacy boundary — what level of detail should the agent discuss about current role?
- Interaction model — chat bubble on brief view, dedicated `/resume/ask/` page, or both?

### Future: Project Nexus (Strategic Fit Engine)

A more ambitious system — **Project Nexus** — is planned as a later evolution that builds on this refactor's foundation. Nexus transforms the resume + blog into a hybrid-cloud intelligence gateway for executive-level candidate evaluation. Key architectural elements:

- **Hybrid search**: MiniSearch (in-browser, fuzzy, custom tokenization for technical terms) + Mark.js for DOM-aware highlighting and expanding collapsed sections. This supersedes the simpler Pagefind approach in Phase 5.
- **Cross-site intelligence**: Jekyll generates `nexus-index.json` manifests for both the resume and blog. A TypeScript orchestrator merges them in-browser for unified search across both sites.
- **Edge layer**: Proxmox cluster with NVIDIA P620 GPUs for local embedding generation and semantic cross-linking via Tailscale Funnel.
- **Multi-cloud LLM orchestration**: AWS Bedrock (Claude) for strategic reasoning, Google Gemini for deep-context analysis. Governance proxy on DigitalOcean with hard budget caps.
- **Circuit breaker pattern**: Graceful degradation — if cloud/edge services fail, falls back to local keyword search. The static site always works.
- **Executive value layer**: Strategic fit analysis (T-shirt sizing across 5 pillars), 90-day onboarding plan generation from job descriptions.

**Impact on this refactor:** The current phases (1–6) build the foundation that Nexus requires:

| Refactor Output | Nexus Dependency |
|---|---|
| `/resume/machine/` JSON-LD | Becomes part of the `nexus-index.json` manifest |
| Single-column semantic HTML | Clean DOM for Mark.js highlighting and section expansion |
| `_data/data.yml` as single source | Jekyll generates both human views and machine manifests from same data |
| `assets/js/` directory structure | Houses the TypeScript orchestrator and MiniSearch client |
| Shared webroot with blog | Enables cross-site index merging under one domain |
| Chat widget architecture (Phase 6) | Evolves into the Nexus governance proxy + LLM orchestration layer |

**We are NOT implementing Nexus now.** But the refactor should avoid decisions that would conflict with it — specifically:
- Don't couple search to a tool (like Pagefind) that can't be replaced by MiniSearch later
- Keep the machine view's structured data format extensible for manifest generation
- Ensure the JS loading pattern supports a future TypeScript orchestrator
- Maintain the shared-domain architecture between resume and blog

See `Project_Nexus_Summary.md` for the full architectural plan (also promoted to `mcgarrah.github.io/_drafts/PROJECT-NEXUS.md` as the canonical reference).

### 7. Preserve Assets

All files under `assets/` carry forward:

- `assets/images/` — Avatar, company logos (used in future experience section enhancement)
- `assets/pdf/` — Static PDF snapshots (historical)
- `assets/css/main.scss` — Rebuilt from scratch but same path
- `assets/icons.svg` — New SVG sprite (replaces CDN Font Awesome)

The `assets/plugins/` directory (Bootstrap, Font Awesome, jQuery) is removed — these are the legacy dependencies being eliminated.

## Constraints

1. **`baseurl: /resume`** — Blog nav links to `/resume/`, About page links to `/resume/print`. The resume deploys as a subpath of mcgarrah.github.io, not at the webroot.
2. **Shared webroot** — Both sites serve from the same GitHub Pages domain (mcgarrah.org). The blog owns the webroot (`/`) and provides shared resources like `favicon.ico`, `site.webmanifest`, `robots.txt`, and site-level indexes. The resume lives at `/resume/` and inherits those shared resources. They are nested and work together — not isolated deployments.
3. **Asset path separation** — Blog serves its own assets from `/assets/`; resume serves `/resume/assets/` from this repo. Resume asset references must use `{{ site.baseurl }}/assets/...`. Shared webroot resources (favicons, manifests) are referenced with absolute paths from the blog's root.
4. **`_data/data.yml`** — Single content source, unchanged.
5. **Pandoc PDF/DOCX** — `jekyll-pandoc-exports` continues to generate `/resume/downloads/print.pdf` and `.docx`.
6. **Local dev** — `bundle exec jekyll serve` at `http://localhost:4000/resume/`.
7. **GitHub Actions** — Existing deployment workflow (or simplified version).
8. **Ruby 3.3.11** via rbenv — `.ruby-version` stays.
9. **Ruby >= 3.2 requires Jekyll >= 4.3.2** — Ruby 3.2 removed `Object#tainted?` from the standard library. Liquid 4.x (used by Jekyll < 4.3.2) calls this method at runtime, causing `undefined method 'tainted?'` crashes. This means Jekyll 3.x, 4.0–4.2, and 4.3.0–4.3.1 are all incompatible with our Ruby floor. The `jekyll-pandoc-exports` gemspec enforces `jekyll >= 4.3.2` to prevent silent installation of broken combinations.

## Integration with mcgarrah.github.io

| Blog reference | Resume URL | Status |
|----------------|-----------|--------|
| Navigation sidebar icon | `/resume/` | Stable |
| About page "full print version" | `/resume/print` | Stable |
| PDF download link | `/resume/downloads/McGarrah-Resume.pdf` | Updated (Phase 2) |
| DOCX download link | `/resume/downloads/McGarrah-Resume.docx` | Updated (Phase 2) |
| New: machine-readable | `/resume/machine/` | Live |
| New: AI chat interface | `/resume/ask/` | New URL, optional dedicated page |

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
- Pagefind static search (build-time indexing, WASM client)
- AI chat widget (external agent, async-loaded JS)

### Modern UI Without Node.js

The goal is a clean, modern aesthetic without introducing a Node.js/PostCSS build pipeline. Options evaluated:

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Tailwind CSS (standalone CLI)** | Utility-first, modern look, no Node required (Rust binary) | Large class strings in HTML, fights Liquid templating, still an external binary | Consider |
| **Open Props** | CSS custom properties library, modern defaults, zero build step | Less opinionated than Tailwind, requires more manual composition | Strong candidate |
| **Modern CSS (hand-rolled)** | Full control, zero dependencies, smallest footprint | More upfront design work | Current plan |
| **Pico CSS** | Classless/minimal-class framework, semantic HTML styling | Opinionated defaults may conflict with resume layout needs | Evaluate |
| **MVP.css / Water.css** | Classless — just drop in and semantic HTML looks good | Too minimal for a polished resume, limited customization | Too simple |

**Current direction:** Hand-rolled modern CSS with CSS custom properties, CSS Grid, `clamp()` for fluid typography, and modern selectors (`:has()`, `:is()`). The ~200 line target is achievable for a single-purpose resume site and avoids any external tooling. If the design work proves too time-consuming, **Open Props** is the fallback — it's a pure CSS import with no build step that provides well-designed spacing, typography, and color scales as custom properties.

**Tailwind standalone CLI** remains an option if the hand-rolled approach feels too spartan. The [Tailwind standalone binary](https://tailwindcss.com/blog/standalone-cli) is a single Rust executable — no Node.js, no npm. It could be added to the GitHub Actions build without changing the Ruby toolchain. But it adds a binary dependency and the utility-class approach clutters Liquid templates.

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
├── assets/                     # Repo-relative: /assets → serves at /resume/assets/
│   ├── css/main.scss           # SCSS entry point
│   ├── images/                 # Avatar, company logos (preserved)
│   ├── js/
│   │   ├── search.js           # Pagefind initialization (async)
│   │   └── chat-widget.js      # AI agent chat widget (async, lazy-loaded)
│   ├── pdf/                    # Historical PDF snapshots (preserved)
│   └── icons.svg               # SVG sprite file
├── _config.yml                 # Simplified config
├── index.html                  # /resume/ (brief view)
├── print.html                  # /resume/print/ (print view)
├── machine.html                # /resume/machine/ (AI/robot view)
├── ask.html                    # /resume/ask/ (AI chat page, Phase 6)
├── Gemfile                     # Minimal deps (no github-pages)
├── .ruby-version               # 3.3.11
└── .github/workflows/jekyll.yml
```

**Note on asset paths:** The blog (mcgarrah.github.io) owns the webroot and provides shared resources (favicon, site.webmanifest, robots.txt, sitemap index). The resume site is nested at `/resume/` within the same domain and inherits those shared webroot resources. The resume's `assets/` directory serves at `/resume/assets/` — separate from the blog's `/assets/` but coexisting on the same domain. Resume-specific asset references use `{{ site.baseurl }}/assets/...`; shared resources use absolute paths from root.

## Refactoring Phases

### Phase 1 — Layout and Structure
- New `_layouts/default.html` — single-column, CSS Grid header block
- New `_sass/` — variables with light/dark custom properties, single layout file
- New `_includes/header.html` — replaces sidebar with compact contact header
- SVG sprite with ~12 icons
- Verify renders at `localhost:4000/resume/`

### Phase 2 — Print View, Pandoc, and Plugin CLI Extension
- New `_layouts/print.html` — linear HTML, no sidebar, no icon decorations
- Restructure so Pandoc needs zero (or minimal) `title_cleanup` patterns
- Simplify `_config.yml` pandoc_exports section
- Test PDF and DOCX output

#### Export File Naming (Complete — plugin 0.2.0)

The generated exports use a professional filename via `export_filename` front matter:

- **Result**: `McGarrah-Resume.pdf` and `McGarrah-Resume.docx`
- **Mechanism**: `export_filename: McGarrah-Resume` in `print.html` front matter
- **Plugin support**: `jekyll-pandoc-exports` 0.2.0 reads `export_filename` from front matter in both generator and CLI modes
- **Status**: ✅ Complete — both `jekyll build` and `jekyll export` produce correctly named files

#### Plugin CLI Extension (jekyll-pandoc-exports 0.2.0)

The plugin now includes a `Jekyll::Command` for standalone export:

- `bundle exec jekyll export` — generate PDF/DOCX from pre-built HTML (requires `jekyll build` first)
- `--format pdf|docx|both` — selective output format
- `--target=print` — export a specific page by filename
- `--dry-run` — print the exact pandoc shell command without executing
- `--validate` — check `_data/data.yml` schema before export (required sections, fields, structure)
- `--output DIR` — override the output directory
- **Status**: ✅ Complete — all flags tested and working

#### Plugin Future Enhancements (tracked for jekyll-pandoc-exports)

These items should be addressed in a future plugin release:

1. **Formalize `export_filename` as a documented feature** — Currently works via front matter (`export_filename: McGarrah-Resume`) in both the inline generator and CLI paths, but needs proper documentation, tests, and inclusion in the plugin's README/configuration reference. Should be promoted from "happens to work" to "first-class supported feature" with examples.

2. **`--verbose` / logging level for `jekyll export` CLI** — The export command currently requires `quiet: false` in the Jekyll configuration load to produce any output. Jekyll's global logger level conflicts with command-level verbosity settings (known Jekyll issue — commands inherit the site config's logging level). The fix should:
   - Add a `--verbose` flag specific to the export command
   - Set logger level independently of `Jekyll.configuration()` quiet setting
   - Avoid conflicting with Jekyll's own `--trace` flag (which handles exceptions, not verbosity)
   - Consider using `$stdout.puts` for critical CLI feedback instead of relying solely on `Jekyll.logger`

3. **Config-level filename mapping** — Support a `pandoc_exports.filename_map` config option as an alternative to per-page front matter, e.g.:
   ```yaml
   pandoc_exports:
     filename_map:
       print: McGarrah-Resume
       cv: McGarrah-CV
   ```

### Phase 3 — Machine View
- New `_layouts/machine.html` — semantic HTML + JSON-LD
- Schema.org Person/Organization/EducationalOrganization markup
- Validate with Google's Rich Results Test
- Validate parseable by common ATS systems
- **Status**: ✅ Implementation complete and locally validated
  - Layout, JSON-LD, and semantic HTML all rendering correctly
  - 7 sections, 66 articles, 110 itemscope attributes, 278 itemprop attributes
  - 2 valid JSON-LD blocks (WebPage + Person with 17 credentials, 27 occupations)
  - Heading hierarchy clean, no accessibility issues
  - Live at mcgarrah.org/resume/machine/ — ready for Google Rich Results Test and ATS validation

#### Machine View Validation Steps

**1. Google Rich Results Test** (structured data for SEO)
- URL: https://search.google.com/test/rich-results
- Test: `https://mcgarrah.org/resume/machine/`
- Validates: JSON-LD syntax, Schema.org type correctness, required properties
- Status: ⚠️ Needs re-validation — machine view updated 2026-05-09 (added education details, removed summary truncation, added social profiles). Previous validation passed 2026-05-09 but content has changed since.

**2. Schema Markup Validator** (general Schema.org validation)
- URL: https://validator.schema.org/
- Test: paste URL or HTML source
- Validates: Schema.org vocabulary correctness, nesting, property types
- More permissive than Google (validates all Schema.org, not just Google-supported types)

**3. ATS Parse Testing** (resume-specific)

ATS systems parse resumes through a 5-stage pipeline: text extraction → tokenization → sectioning → named entity recognition → structured output. Each major ATS implements this differently.

| Tool | What It Tests | Free Tier | URL |
|------|---------------|-----------|-----|
| **Jobscan** | Keyword match + parse fidelity against a job description | 5 scans/month | https://www.jobscan.co/ |
| **Resume Worded** | ATS score + section detection + keyword gaps | Limited free | https://resumeworded.com/ |
| **SkillSyncer** | Keyword matching + formatting issues | Free basic | https://skillsyncer.com/ |
| **Teal** | ATS score + keyword tracking across applications | Free tier | https://www.tealhq.com/ |

**Testing methodology:**
1. Export `/resume/print/` as PDF via browser print (or use the XeLaTeX brief PDF)
2. Upload to each ATS checker with a target job description
3. Record: parse success rate, section detection accuracy, keyword match score
4. Compare results across tools to identify consistent failures

**4. Direct ATS Upload Testing** (gold standard)

The most reliable test is submitting through actual ATS portals:
- **Greenhouse**: Apply to any Greenhouse-powered job posting (look for "Powered by Greenhouse" in footer)
- **Lever**: Apply to any Lever-powered posting (URL contains `jobs.lever.co`)
- **Workday**: Apply to any large enterprise posting (most Fortune 500)
- **iCIMS**: Common in healthcare, finance, government

After submitting, check if the parsed profile matches your resume content. Some ATS systems show you the parsed result during the application flow.

**5. AI Agent Parsing Test** (future-focused)

Test whether AI systems can extract structured information from the machine view:
- Feed `https://mcgarrah.org/resume/machine/` to Claude, ChatGPT, or Gemini
- Ask: "Extract all jobs, dates, companies, and skills from this page"
- Verify: completeness, accuracy of dates, correct company-role associations
- This validates the JSON-LD + semantic HTML serves its dual purpose (SEO + AI grounding)

**Key insight:** ATS systems primarily parse PDF/DOCX uploads, not web pages. The machine view serves a different audience — AI agents, recruiters browsing the URL, and Google's structured data indexer. The PDF exports are what ATS systems actually consume. Both need to be tested independently.

### Phase 4 — Polish and Cleanup
- Light/dark mode testing across browsers
- `@media print` stylesheet for browser print
- Mobile responsive (single breakpoint at ~768px)
- Accessibility audit (headings, ARIA, contrast ratios in both modes)
- Lighthouse scores (Performance, Accessibility, SEO)
- Remove `assets/plugins/` directory
- Remove legacy files (`compress.html`, `_sass/skins/`, etc.)
- CI quality gates: `jekyll doctor` (configuration smells) + `html-proofer` (link integrity)

### Phase 4b — Experience Subsections Schema (data model change)
- Restructure `_data/data.yml` to replace flat `details` markdown blobs with structured `subsections` array
- Each subsection has explicit `title` and `text` fields instead of relying on `**bold**` markdown
- Templates render subsection titles as `<h4>` — Pandoc converts to `\paragraph{}` (visually distinct from `<h3>` → `\subsubsection{}`)
- Machine view wraps subsections as `schema.org/CreativeWork` nested within `OrganizationRole` for ATS compatibility
- Backward compatible: entries without subsections continue using `summary`/`details` fields
- Migration scope: 19 jobs, 135 subsections, preserving all 51 markdown links and rich content
- **Motivation**: Pandoc renders `<h3>` job titles and `<strong>` subsection headings at identical visual weight in PDF — CSS class-based styling is ignored during LaTeX conversion
- **Spec**: `.kiro/specs/experience-subsections/requirements.md` (in mcgarrah.github.io workspace)

### Phase 5 — In-Browser Search
- Add Pagefind indexing step to GitHub Actions build pipeline (interim solution)
- Add search UI component to brief view header (excluded from print/machine views)
- Build-time index covers all three views for comprehensive results
- Test search relevance across career profile, experiences, skills, certifications
- Ensure search widget respects light/dark mode CSS custom properties
- **Note:** Pagefind is a pragmatic first step. Project Nexus will later replace it with MiniSearch + Mark.js for custom tokenization (technical terms like "K8s"/"Kubernetes"), fuzzy matching, and DOM-aware highlighting that expands collapsed `<details>` sections. Design the search UI container and JS loading pattern to be swappable.

### Phase 5a — Project Dates
- Add `time` field to project entries in `_data/data.yml` where dates are discoverable
- Sources: GitHub repository creation dates, article publication dates, conference years
- Format: match existing convention (e.g., "2024", "Jun 2024", "2022 - 2024")
- Update all three views + LaTeX template to render project dates (right-aligned, matching experience pattern)
- Projects without discoverable dates remain undated (field is optional)
- **Scope**: 13 projects, most have dates in their titles or linked articles already

### Phase 5b — Per-Entry Skills Taxonomy
- Add optional `skills` array to each experience, education, and project entry in `_data/data.yml`
- Skills values should match entries in the Skills section for cross-referencing
- Schema: `skills: ["Python", "AWS EKS", "Terraform", "New Relic"]` — flat list of strings
- Machine view: render as `schema.org/skills` or `schema.org/knowsAbout` properties
- Brief/print views: optionally render as a compact tag list below each entry
- LaTeX template: render as italic comma-separated list after the entry content
- **Goal**: Enable future semantic mapping — which skills were used at which jobs, for how long
- **Cross-reference**: Skills in per-entry lists should be a subset of the master Skills section categories
- **ATS value**: Explicit skill-to-experience mapping improves keyword matching for applicant tracking systems
- **Scope**: Start with the 5 most recent experience entries as proof of concept, then expand

### Phase 6 — AI Agent Integration
- Select hosting platform (AWS Lambda + API Gateway, Cloudflare Workers, or third-party)
- Build agent knowledge base from `/resume/machine/` JSON-LD output
- Evaluate whether to include mcgarrah.org blog content as additional context
- Define privacy boundaries and response guardrails
- Implement chat widget component (floating button → panel)
- Async/lazy-load the widget JS — must not impact page load performance
- Add `/resume/ask/` dedicated page as alternative interaction surface (optional)
- Test conversational quality: recruiter questions, role inquiries, skill deep-dives
- Monitor usage and iterate on agent prompt engineering

## Local Development

```bash
cd ~/github/resume
bundle install
bundle exec jekyll serve
# Brief: http://localhost:4000/resume/
# Print: http://localhost:4000/resume/print/
# Machine: http://localhost:4000/resume/machine/
# Ask (Phase 6): http://localhost:4000/resume/ask/
```

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-05 | Started refactor on `main` | Work committed directly to main; no separate branch needed |
| 2026-05-05 | Create PROJECT-NEXUS.md | Promote to _drafts convenience file for reference |
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
| | Add in-browser search (Pagefind) | Static-site best practice, build-time index, ~100KB WASM client |
| | Add AI agent chat widget | Conversational resume interaction for recruiters, external service |
| | JS principle: no JS for presentation | Layout/styling pure CSS; JS reserved for interactive features that degrade gracefully |
| | `/resume/machine/` serves dual purpose | SEO structured data AND AI agent knowledge base |
| | Acknowledge Project Nexus as future state | Refactor builds the foundation; avoid decisions that conflict with Nexus architecture |
| | Pagefind as interim search (swappable) | Pragmatic first step; Nexus replaces with MiniSearch + Mark.js for custom tokenization |
| | Keep search/chat JS loading pattern generic | Future TypeScript orchestrator needs the same entry points |
| 2026-05-06 | Add `jekyll export` CLI command to plugin | Decouple PDF/DOCX generation from full site build for faster iteration |
| 2026-05-06 | Add `--dry-run` flag to export command | Debug LaTeX/Pandoc issues without executing; print exact shell command |
| 2026-05-06 | Add pre-export YAML schema validation | Catch structural errors in data.yml before Pandoc fails cryptically |
| 2026-05-06 | Add `jekyll doctor` + `html-proofer` to CI | Quality gates: config smells and link integrity checks |
| 2026-05-06 | Modern UI: hand-rolled CSS first, Open Props fallback | Avoid Node.js dependency; Tailwind standalone CLI as last resort |
| 2026-05-06 | Export filenames: `McGarrah-Resume.pdf/.docx` | Professional naming; blocked on plugin support for custom output filenames |
| 2026-05-06 | Phase 3 machine view implemented | Semantic HTML5 + JSON-LD at `/resume/machine/`; 7 sections, 66 articles, 110 itemscope attributes |
| 2026-05-06 | Phase 2 complete with plugin 0.2.0 | Custom filenames via `export_filename` front matter; CLI export command with --dry-run, --validate, --format |
| 2026-05-06 | Drop `github-pages` gem | Conflicts with Jekyll 4.x; replaced with explicit `jekyll ~> 4.4` dependency |
| 2026-05-06 | Add `html-proofer` to CI | Link integrity checking in GitHub Actions workflow |
| 2026-05-06 | Phase 3 locally validated | JSON-LD valid, heading hierarchy clean, microdata complete; pending Google Rich Results Test on live URL |
| 2026-05-06 | Experience subsections schema change | Pandoc can't distinguish `<h3>` job titles from `<strong>` subsection headings in PDF; restructure data.yml with explicit `subsections` array |
| 2026-05-06 | Schema.org `CreativeWork` for subsections | Subsections in machine view wrapped as nested `CreativeWork` within `OrganizationRole` for ATS keyword indexing and semantic structure |
| 2026-05-07 | Add Jinja2/XeLaTeX resume pipeline | Full typographic control independent of HTML; Python reads same YAML |
| 2026-05-07 | Dual language stack (Ruby + Python) | Jekyll for web views, Python for export pipeline; deliberate architecture decision |
| 2026-05-07 | Plan: Project dates from GitHub/articles | Add `time` field to projects where dates are discoverable |
| 2026-05-07 | Plan: Per-entry skills taxonomy | Add `skills` array to each experience/education/project for semantic cross-referencing |
| 2026-05-09 | Remove WeasyPrint, XeLaTeX is primary | WeasyPrint dropped; Jinja2/XeLaTeX pipeline handles all PDF generation with full typographic control |
| 2026-05-09 | Site live at mcgarrah.org/resume | Published via GitHub Pages; enables Google Rich Results Test and live validation |
