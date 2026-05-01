# Resume Site — Project Context

## What This Is

A Jekyll-based online resume for Michael McGarrah, hosted on GitHub Pages at
https://mcgarrah.org/resume. The site renders two views from a single data source:

| URL | Layout | Behavior |
|-----|--------|----------|
| `/resume/` | `default` | Interactive — `<details>` elements collapse long sections |
| `/resume/print/` | `print` | Fully expanded — all content visible for PDF/print |

The resume is the canonical detailed record of career history. LinkedIn is the
networking-optimized version. The blog (mcgarrah.org) is the technical portfolio.
All three should tell a consistent story.

## Data Model

All resume content lives in `_data/data.yml`. The YAML file drives every section
of the site — there are no content markdown files.

### Key Sections in data.yml

| Section | Purpose |
|---------|---------|
| `sidebar` | Name, tagline, contact info, links (PDF, DOCX, print) |
| `career-profile` | Top-of-page summary paragraph |
| `education` | Degrees with `summary` (always visible) + `details` (collapsible/expandable) |
| `experiences` | Jobs with `summary` (always visible) + `details` (collapsible/expandable) |
| `certifications` | Professional certifications with credential links |
| `projects` | Selected projects with links and descriptions |
| `publications` | Academic publications |
| `skills` | Categorized skills organized by domain |

### The summary/details Pattern

Both `education` and `experiences` use a two-tier content model:

- **`summary`** — Always rendered. This is the one-paragraph highlight visible on both
  `/resume/` and `/resume/print/`. Should be concise enough for a two-page resume.
- **`details`** — Extended content. On `/resume/`, wrapped in `<details>` (collapsible).
  On `/resume/print/`, rendered fully expanded. Contains the deep narrative, bullet
  points, project descriptions, and links.

When editing entries:
- Put the "elevator pitch" in `summary` — what a recruiter scanning for 5 seconds needs
- Put the depth in `details` — what a hiring committee doing deep diligence reads
- An entry can have `summary` only (no collapsible section), `details` only (backward
  compat), or both

### Template Pairs

| Section | Interactive (`/resume/`) | Print (`/resume/print/`) |
|---------|------------------------|------------------------|
| Education | `education.html` — `<details>` wrapper | `education-print.html` — fully expanded |
| Experiences | `experiences.html` — `<details>` wrapper | `experiences-print.html` — fully expanded |

## Technology Stack

- **Jekyll** with GitHub Pages hosting
- **Ruby 3.3.11** via rbenv (see `ruby-environment.md` in the blog repo's rules)
- **`.ruby-version`** in repo root — ensures rbenv selects the correct Ruby
- **Gemfile**: jekyll, github-pages, jekyll-sitemap, jekyll-seo-tag, jekyll-pandoc-exports
- **Pandoc exports**: Automatic PDF and DOCX generation from the print layout
- **SASS/SCSS** for styling with theme skins (`_sass/skins/`)
- **GitHub Actions** CI/CD deploys on push to `main`

## File Structure

```
resume/
├── _data/data.yml              # ALL resume content lives here
├── _includes/
│   ├── education.html          # Interactive (collapsible details)
│   ├── education-print.html    # Print (fully expanded)
│   ├── experiences.html        # Interactive (collapsible details)
│   ├── experiences-print.html  # Print (fully expanded)
│   ├── career-profile.html     # Career summary section
│   ├── sidebar.html            # Name, tagline, contact, links
│   ├── certifications.html     # Certification list
│   ├── projects.html           # Selected projects
│   ├── publications.html       # Academic publications
│   └── skills.html             # Categorized skills
├── _layouts/
│   ├── default.html            # Interactive resume layout
│   └── print.html              # Print/PDF resume layout
├── _sass/                      # SCSS stylesheets and theme skins
├── index.html                  # /resume/ entry point (uses default layout)
├── print.html                  # /resume/print/ entry point (uses print layout)
├── _config.yml                 # Jekyll config (baseurl: /resume)
├── .ruby-version               # rbenv Ruby version (3.3.11)
└── .github/workflows/jekyll.yml # CI/CD deployment
```

## Development

```bash
cd resume
bundle install
bundle exec jekyll serve        # Preview at http://localhost:4000/resume/
```

The print version is at http://localhost:4000/resume/print/

### YAML Validation

The data.yml file contains Date objects (certification dates). Use rbenv Ruby for validation:

```bash
$HOME/.rbenv/versions/3.3.11/bin/ruby -e "
  require 'yaml'; require 'date'
  YAML.load_file('_data/data.yml', permitted_classes: [Date])
  puts 'YAML is valid'
"
```

System Ruby 2.6 will fail on `permitted_classes` — always use rbenv Ruby 3.3.

## Relationship to Other Repos

| Repo | Relationship |
|------|-------------|
| `mcgarrah.github.io` | Parent site — resume is deployed as a subpath (`/resume/`) |
| `mcgarrah.github.io/_drafts/PERSONA-RESUME.md` | Cross-reference between resume and LinkedIn, proposed rewrites |
| `mcgarrah.github.io/_drafts/PERSONA-SVP.md` | SVP positioning strategy that drives resume content |
| `mcgarrah.github.io/_drafts/ENVESTNET-RESUME.md` | Consolidated Envestnet work history sourced from Jira reviews |

## When Editing data.yml

- Always validate YAML after edits (see above)
- Preview both `/resume/` and `/resume/print/` — they render differently
- Keep `summary` fields concise — they determine the "short resume" length
- Use `details` for depth that supports the summary claims
- Maintain consistency with LinkedIn profile descriptions (see `PERSONA-LINKEDIN.md`)
- Use leadership language in summaries — "Led", "Architected", "Designed" not "Built", "Worked on"
