# Resume Project — TODO

Items organized by the REFACTOR.md phase they belong to, plus standalone improvements.

## Completed Phases

- [x] Phase 1 — Layout and Structure (single-column CSS Grid, light/dark mode, SVG sprite)
- [x] Phase 2 — Print View, Pandoc, and Plugin CLI Extension (jekyll-pandoc-exports 0.2.0)
- [x] Phase 3 — Machine View (JSON-LD + semantic HTML at /resume/machine/)
- [x] Phase 4 — Polish and Cleanup (live at mcgarrah.org/resume, html-proofer in CI)
- [x] Phase 4b — Experience Subsections Schema (structured `subsections` array in data.yml)
- [x] Phase 5a — Project Dates (added `time` field to project entries)
- [x] Jinja2/XeLaTeX Pipeline — Python-based PDF generation with full typographic control
  - Three templates: long (34 pages), brief (5 pages), ultra-brief (2 pages)
  - WeasyPrint evaluated and removed; XeLaTeX is primary
  - Company/university logo images in all PDF variants
  - Anchor links in brief PDF for internal navigation
  - Section-linked footers in ultra-brief PDF
- [x] Ultra-Brief View — Two-page HTML view + matching XeLaTeX PDF
- [x] Company Logos — SVGs for web, PNGs for LaTeX, consistent naming
- [x] SEO Validation — og:image, Rich Results Test fixes, Schema.org warnings resolved
- [x] CI Optimization — apt package caching (6+ min savings), ultra-brief in pipeline
- [x] Cleanup — removed obsolete template files, organized bin/ scripts, removed Gemfile.lock

## Phase 5 — In-Browser Search

- [ ] Add Pagefind indexing step to GitHub Actions build pipeline
- [ ] Add search UI component to brief view header (excluded from print/machine)
- [ ] Test search relevance across career profile, experiences, skills, certifications
- [ ] Ensure search widget respects light/dark mode CSS custom properties
- [ ] Design search container to be swappable for future MiniSearch (Project Nexus)

## Phase 5b — Per-Entry Skills Taxonomy

- [ ] Add optional `skills` array to experience, education, and project entries
- [ ] Start with 5 most recent experience entries as proof of concept
- [ ] Machine view: render as `schema.org/skills` or `knowsAbout`
- [ ] Brief/print views: compact tag list below each entry
- [ ] LaTeX template: italic comma-separated list after entry content

## Phase 6 — AI Agent Integration

- [ ] Select hosting platform (AWS Lambda, Cloudflare Workers, or third-party)
- [ ] Build agent knowledge base from `/resume/machine/` JSON-LD
- [ ] Evaluate including mcgarrah.org blog content as additional context
- [ ] Define privacy boundaries and response guardrails
- [ ] Implement chat widget (floating button → panel, async/lazy-loaded)
- [ ] Add `/resume/ask/` dedicated page (optional)

## Content

- [ ] Consolidate 1990–2005 early career into fewer entries (shorten resume length)
- [x] Add company/university logo images to experience and education sections
- [ ] Add ADP-AI Automated Document Processing project entry (when public)
- [ ] Create cover letter templates (ChatGPT-assisted, tailored per role)

## Export & PDF Quality

- [ ] Fix `\MakeTextUppercase` undefined control sequence warning in XeLaTeX
- [ ] Add `--verbose` flag to `jekyll export` CLI (plugin enhancement)
- [ ] Formalize `export_filename` as documented plugin feature
- [ ] Config-level filename mapping for jekyll-pandoc-exports

## CI & Automation

- [x] Cache apt packages in CI (6+ min savings per deploy)
- [x] Add ultra-brief PDF generation to GitHub Actions workflow
- [ ] Add Lighthouse CI to GitHub Actions (performance, accessibility, SEO scores)
- [ ] Add `html-proofer` external link checking (currently `--disable-external`)
- [ ] Consider adding LaTeX PDF to CI artifact upload for PR review
- [ ] Add `jekyll doctor` to CI pipeline (configuration smells)

## SEO & Discoverability

- [x] Site live at mcgarrah.org/resume (enables live validation)
- [x] Add og:image social preview card
- [x] Fix Schema.org validation warnings from Google Rich Results Test
- [x] Resolve ScholarlyArticle Rich Results Test warnings
- [ ] Test parsability with common ATS systems (Greenhouse, Lever, Workday)
- [ ] Review job board keyword optimization (LinkedIn, Indeed, Dice)
- [ ] Verify structured data indexing in Google Search Console

## Low Priority / Future

- [ ] Update Kaggle homepage with older ML coursework
- [ ] Create plain text resume version for Indeed paste fields
- [ ] Add performance monitoring for site build times
- [ ] Investigate GitHub fork detachment (contact GitHub Support)

---
*Last Updated: 2026-05-09*
