# Jekyll Pandoc Exports Plugin

A Jekyll plugin that automatically generates DOCX and PDF exports of your pages using Pandoc.

## Features

- Generate Word documents (.docx) and PDFs from Jekyll pages
- Configurable PDF options (margins, paper size, etc.)
- Automatic Unicode cleanup for LaTeX compatibility
- Configurable HTML cleanup patterns
- Auto-injection of download links
- Flexible image path fixing
- Print-friendly CSS class support

## Installation

1. Add `pandoc-ruby` to your Gemfile:
```ruby
gem "pandoc-ruby"
```

2. Install Pandoc and LaTeX (for PDF generation):
```bash
# Ubuntu/Debian
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# macOS
brew install pandoc
brew install --cask mactex
```

3. Copy `_plugins/jekyll-pandoc-exports.rb` to your Jekyll site's `_plugins` directory.

## Usage

### Basic Usage

Add front matter to any page you want to export:

```yaml
---
title: My Document
docx: true    # Generate Word document
pdf: true     # Generate PDF
---
```

### Configuration

Add configuration to your `_config.yml`:

```yaml
pandoc_exports:
  enabled: true
  pdf_options:
    variable: 'geometry:margin=0.75in'
  unicode_cleanup: true
  inject_downloads: true
  download_class: 'pandoc-downloads no-print'
  title_cleanup:
    - '<title>.*?</title>'
    - '<h1[^>]*>.*?Site Title.*?</h1>'
  image_path_fixes:
    - pattern: 'src="/assets/images/'
      replacement: 'src="{{site.dest}}/assets/images/'
```

### Configuration Options

- `enabled`: Enable/disable the plugin (default: true)
- `pdf_options`: Pandoc options for PDF generation (default: 1in margins)
- `unicode_cleanup`: Remove problematic Unicode characters for LaTeX (default: true)
- `inject_downloads`: Auto-inject download links into pages (default: true)
- `download_class`: CSS class for download links (default: 'pandoc-downloads no-print')
- `title_cleanup`: Array of regex patterns to remove from PDF HTML
- `image_path_fixes`: Array of path replacements for images

### Per-Page PDF Options

Override PDF options for specific pages:

```yaml
---
title: My Document
pdf: true
pdf_options:
  variable: 'geometry:margin=0.5in'
---
```

### CSS for Print Hiding

Include the CSS to hide download links when printing:

```html
{% include pandoc-exports-css.html %}
```

Or add to your main CSS:

```css
@media print {
  .no-print {
    display: none !important;
  }
}
```

## Generated Files

The plugin generates files with the same name as your markdown file:

- `my-page.md` → `my-page.docx` and `my-page.pdf`
- Accessible at `/my-page.docx` and `/my-page.pdf`

## Download Links

When `inject_downloads` is enabled, the plugin automatically adds download links to pages that generate exports. Links are inserted after the first heading or at the beginning of the body.

## Troubleshooting

### LaTeX Errors
- Ensure LaTeX packages are installed
- Enable `unicode_cleanup` to remove problematic characters
- Add custom cleanup patterns to `title_cleanup`

### Image Issues
- Configure `image_path_fixes` for your site's image paths
- Use absolute paths in the replacement patterns

### Missing Files
- Check that Pandoc is installed and accessible
- Verify file permissions in the `_site` directory