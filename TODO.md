# Resume Project — TODO

Items organized by the REFACTOR.md phase they belong to, plus standalone improvements.

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
- [ ] Add company/university logo images to experience and education sections
- [ ] Add ADP-AI Automated Document Processing project entry (when public)
- [ ] Create cover letter templates (ChatGPT-assisted, tailored per role)

## Export & PDF Quality

- [ ] Evaluate retiring WeasyPrint PDF once LaTeX template matures
- [ ] Fix `\MakeTextUppercase` undefined control sequence warning in XeLaTeX
- [ ] Add `--verbose` flag to `jekyll export` CLI (plugin enhancement)
- [ ] Formalize `export_filename` as documented plugin feature

## CI & Automation

- [ ] Add Lighthouse CI to GitHub Actions (performance, accessibility, SEO scores)
- [ ] Add `html-proofer` external link checking (currently `--disable-external`)
- [ ] Consider adding LaTeX PDF to CI artifact upload for PR review

## SEO & Discoverability

- [ ] Validate machine view with Google Rich Results Test (requires live URL)
- [ ] Test parsability with common ATS systems (Greenhouse, Lever, Workday)
- [ ] Review job board keyword optimization (LinkedIn, Indeed, Dice)
- [ ] Verify structured data indexing in Google Search Console

## Low Priority / Future

- [ ] Update Kaggle homepage with older ML coursework
- [ ] Create plain text resume version for Indeed paste fields
- [ ] Add performance monitoring for site build times
- [ ] Investigate GitHub fork detachment (contact GitHub Support)

---
*Last Updated: 2026-05-07*
