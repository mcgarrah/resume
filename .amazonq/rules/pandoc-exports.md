# Pandoc Exports — PDF & DOCX Generation

## How It Works

The `jekyll-pandoc-exports` plugin (v0.1.14) runs as a `:site, :post_write` hook.
It reads the rendered HTML from `_site/print.html`, applies `title_cleanup` regex
patterns and `image_path_fixes` substitutions, then feeds the processed HTML to
Pandoc for conversion to PDF (via LaTeX) and DOCX.

### Pipeline

```
print.html (Jekyll) → rendered HTML in _site/
    → title_cleanup regexes strip unwanted elements
    → image_path_fixes rewrite asset paths
    → template CSS injected into <head>
    → PandocRuby converts HTML → DOCX (always works)
    → PandocRuby converts HTML → PDF (requires LaTeX)
```

Output lands in `_site/downloads/print.pdf` and `_site/downloads/print.docx`.

### What Pandoc Sees

Pandoc receives the **full rendered HTML** of the print layout, including:
- `<head>` with `<title>`, `<meta>`, and jekyll-seo-tag output
- `<div class="sidebar-wrapper">` (hidden via CSS but still in the DOM)
- `<div class="print-header">` (name, tagline, contact links)
- `<div class="main-wrapper">` with all resume sections
- `<section class="print-links-section">` at the bottom

The `<title>` tag becomes the **document title** in PDF/DOCX metadata. The
jekyll-seo-tag generates a compound title: `site.title | site.description`.
Keep `site.title` clean (currently "Michael McGarrah — Resume") and
`site.description` free of the author's name to avoid repetition.

### Three Rendering Targets

The print layout serves three distinct consumers:

| Consumer | What it sees | Notes |
|----------|-------------|-------|
| Browser (`/resume/print/`) | Full HTML with CSS | print-header visible, sidebar hidden via CSS |
| Pandoc → DOCX | HTML after title_cleanup | print-header stripped by regex, sidebar stripped by existing patterns |
| Pandoc → PDF | HTML after title_cleanup + LaTeX | Same as DOCX but also requires LaTeX for rendering |

Changes to `print.html`, `print-header.html`, or `print-links.html` affect all
three. Use `title_cleanup` patterns to strip elements from Pandoc output without
affecting the browser view.

## title_cleanup Regex Patterns

These are Ruby regexes applied with `Regexp::MULTILINE` (`.` matches newlines).
They run via `gsub!` against the full HTML string before Pandoc conversion.

### Current Patterns (in _config.yml)

| Pattern | Purpose |
|---------|---------|
| `<div class="print-header">[\s\S]*?</ul>\s*</div>\s*</div>` | Strips the name/tagline/contact header block |
| `<img class="avatar"[^>]*/?>` | Strips profile photo |
| `<li class="phone">...` through `<li class="print">...` | Strips sidebar contact items |
| `<div class="languages-container...` | Strips languages section |
| `<span class="fa-stack...` | Strips Font Awesome icon stacks from section headers |

### Regex Authoring Rules

1. **Ruby MULTILINE flag**: The plugin passes `Regexp::MULTILINE` which makes `.`
   match `\n`. Use `.*?` for non-greedy matching across lines.

2. **Nested div matching**: Ruby regexes can't count balanced tags. For nested
   `<div>` structures, anchor the end pattern on a unique child element:
   ```
   # BAD — stops at first </div>, misses nested content
   <div class="print-header">.*?</div>

   # BAD — counting </div> tags is fragile if nesting changes
   <div class="print-header">.*?</div>\s*</div>\s*</div>

   # GOOD — anchor on </ul> which uniquely ends the contact list
   <div class="print-header">[\s\S]*?</ul>\s*</div>\s*</div>
   ```

3. **Testing patterns**: Verify against the actual rendered HTML, not the template:
   ```bash
   $HOME/.rbenv/versions/3.3.11/bin/ruby -e '
     html = File.read("_site/print.html")
     pattern = Regexp.new(%q{YOUR_PATTERN_HERE}, Regexp::MULTILINE)
     matches = html.scan(pattern)
     puts "Matches: #{matches.length}"
     matches.each { |m| puts m[0..200] + "..." }
   '
   ```

4. **Single match rule**: Every pattern should match exactly once. Multiple matches
   means the pattern is too broad and may strip content from other sections.

5. **YAML escaping**: Patterns in `_config.yml` are YAML strings. Backslashes need
   escaping (`\\s` not `\s`). Use single-quoted YAML strings when possible to
   reduce escaping confusion.

### The print-header Structure

```html
<div class="print-header">           ← outer div
  <div class="print-header-main">    ← inner div 1
    <h1 class="print-name">...</h1>
    <h3 class="print-tagline">...</h3>
  </div>                              ← closes inner div 1
  <div class="print-contact">        ← inner div 2
    <ul class="print-contact-list">
      <li>...</li>
      ...
    </ul>
  </div>                              ← closes inner div 2
</div>                                ← closes outer div
```

The regex `<div class="print-header">[\s\S]*?</ul>\s*</div>\s*</div>` works
because `</ul>` is the unique anchor — it only appears once inside print-header,
and the two `</div>` tags after it close `print-contact` and `print-header`.

## Template CSS

The `template.css` config injects CSS into `<head>` before Pandoc conversion.
This controls how Pandoc interprets the HTML layout:

```yaml
template:
  css: >
    .wrapper { display: block; padding: 0; margin: 0; }
    .sidebar-wrapper { display: block; padding: 0; }
    .main-wrapper { display: block; padding: 0; }
    .section { margin-bottom: 10px; }
    .section-title { font-size: 24px; font-weight: bold; text-transform: uppercase;
      border-bottom: 2px solid #333; padding-bottom: 4px; margin-bottom: 10px; }
```

Pandoc respects some CSS properties when converting to DOCX/PDF. Block layout
and font sizing work; complex grid/flexbox does not.

## Dependencies

### macOS

Both Pandoc and a full LaTeX distribution are required for PDF generation:

```bash
brew install pandoc
brew install --cask mactex
```

| Tool | Install | Provides |
|------|---------|----------|
| Pandoc | `brew install pandoc` | HTML → DOCX conversion, HTML → PDF (via LaTeX) |
| MacTeX | `brew install --cask mactex` | `pdflatex` and full TeX Live (~6.9GB) |

Without LaTeX, DOCX generates but PDF fails with `pdflatex: createProcess:
find_executable: failed`.

**MacTeX post-install PATH issue**: MacTeX is a `.pkg` cask — Homebrew downloads
the installer package but macOS must run it to install binaries to
`/Library/TeX/texbin/` and create `/etc/paths.d/TeX`. If `which pdflatex` returns
nothing after `brew install --cask mactex`:

```bash
# Check if the pkg was downloaded but not installed
ls /opt/homebrew/Caskroom/mactex/*/mactex-*.pkg

# If the pkg exists, run the installer manually
sudo installer -pkg /opt/homebrew/Caskroom/mactex/2026.0324/mactex-20260324.pkg -target /

# Or reinstall the cask (triggers the installer)
brew reinstall --cask mactex
```

After installation, `/etc/paths.d/TeX` should contain `/Library/TeX/texbin`.
New terminal sessions pick this up automatically. For the current session:
```bash
eval "$(/usr/libexec/path_helper)"
which pdflatex  # should show /Library/TeX/texbin/pdflatex
```

**Non-interactive shells** (Amazon Q `executeBash`, VS Code tasks) may not have
`/Library/TeX/texbin` on PATH even after installation. The `path_helper` utility
reads `/etc/paths.d/TeX` but only runs in login shells. If `bundle exec jekyll
build` can't find `pdflatex`, add it to PATH explicitly:
```bash
export PATH="/Library/TeX/texbin:$PATH" && bundle exec jekyll build
```

### WSL2 / Linux

```bash
sudo apt-get update
sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

No PATH issues on Linux — packages install to `/usr/bin/` which is always on PATH.

### GitHub Actions CI/CD

The `jekyll.yml` workflow installs both on Ubuntu:
```yaml
- name: Install Pandoc and LaTeX
  run: |
    sudo apt-get update
    sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

Both PDF and DOCX generate successfully in CI. The PDF uses the `geometry:margin=0.75in`
option for tighter margins than the default 1-inch.

### Plugin Dependencies

- `jekyll-pandoc-exports` (0.1.14) — Jekyll plugin, installed via Gemfile
- `pandoc-ruby` — Ruby wrapper for Pandoc CLI, transitive dependency
- Pandoc CLI — system binary, must be on PATH
- pdflatex — system binary, required only for PDF output

## Common Issues

### Name Repetition in PDF/DOCX

The document title comes from `<title>` which jekyll-seo-tag builds as
`site.title | site.description`. If both contain the author's name, it appears
multiple times in the first half-page. Keep the name in `site.title` only.

Current config:
- `title`: "Michael McGarrah — Resume" (has the name once)
- `description`: "Engineering Leader bridging..." (no name — intentional)

### Elements Appearing in PDF That Shouldn't

If an HTML element appears in the PDF/DOCX but should be stripped:
1. Build the site: `bundle exec jekyll build`
2. Open `_site/print.html` and find the element
3. Write a regex that matches it exactly once (test with Ruby snippet above)
4. Add to `title_cleanup` array in `_config.yml`
5. Rebuild and verify the DOCX output

### Font Awesome Icons in PDF

Font Awesome `<i>` tags render as empty boxes or missing characters in PDF/LaTeX.
The `<span class="fa-stack...">` pattern strips the icon stacks from section
headers. Individual `<i class="fas ...">` or `<i class="fab ...">` tags in
contact lists are stripped by the `<li class="...">` patterns.

If new icon elements appear in PDF output, add a `title_cleanup` pattern for them.

### Unicode Characters Breaking LaTeX

The `unicode_cleanup: true` config strips emoji and symbol ranges
(`\u{1F000}-\u{1F9FF}`, `\u{2600}-\u{26FF}`, `\u{2700}-\u{27BF}`) that cause
LaTeX compilation failures. If a new Unicode character breaks PDF generation,
check the Pandoc error output for the specific character and add it to the
cleanup range in the plugin source or work around it in the content.

The em dash (—) in the site title works fine — it's in the Latin Extended range
that LaTeX handles natively.

### Incremental Build Skipping Exports

The `incremental: true` config skips regeneration if the output files are newer
than the source. If you change `_config.yml` (title_cleanup patterns, template
CSS) but not `print.html`, the plugin may skip regeneration. Force a rebuild:

```bash
rm -rf _site/downloads/
bundle exec jekyll build
```

## print-links.html — Footer Section

The `print-links.html` include renders at the bottom of the print layout. It
contains profile URLs (website, LinkedIn, GitHub, etc.) and a canonical URL
reference: "Full interactive resume with all links: https://mcgarrah.org/resume/"

This footer appears in both the browser view and the Pandoc output. It exists
because URLs in the body of the resume are not printed as text in PDF/DOCX —
Pandoc converts `<a href="...">text</a>` to just "text" without the URL. The
footer gives readers a single URL to access the full interactive version.

## When Modifying PDF/DOCX Formatting

1. Make changes to templates/includes/config
2. Build: `bundle exec jekyll build`
3. Check `_site/print.html` in a browser — verify the web print view is correct
4. Check `_site/downloads/print.docx` — open in Word/LibreOffice to verify
5. If LaTeX is installed locally, check `_site/downloads/print.pdf`
6. If LaTeX is not installed, push to GitHub and check the CI-generated PDF
7. Test any new `title_cleanup` regex against `_site/print.html` using the Ruby
   snippet before committing
