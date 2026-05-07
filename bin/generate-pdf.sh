#!/bin/bash
# Generate PDF from the built print.html using WeasyPrint
# Fixes baseurl paths so images resolve correctly from _site/
#
# Usage: bin/generate-pdf.sh [output-filename]
# Run from the resume project root after `bundle exec jekyll build`

set -e

SITE_DIR="_site"
PRINT_HTML="$SITE_DIR/print.html"
OUTPUT_DIR="$SITE_DIR/downloads"
OUTPUT_FILE="${1:-McGarrah-Resume-styled.pdf}"
TEMP_HTML=$(mktemp /tmp/resume-print-XXXXXX.html)

if [ ! -f "$PRINT_HTML" ]; then
  echo "Error: $PRINT_HTML not found. Run 'bundle exec jekyll build' first."
  exit 1
fi

# Copy print.html and fix baseurl paths to be relative to _site/
# /resume/assets/images/foo.png → assets/images/foo.png
sed 's|src="/resume/|src="|g; s|href="/resume/assets/|href="assets/|g' "$PRINT_HTML" > "$TEMP_HTML"

# Generate PDF with base-url pointing to _site/ so relative paths resolve
weasyprint "$TEMP_HTML" "$OUTPUT_DIR/$OUTPUT_FILE" --base-url "file://$PWD/$SITE_DIR/"

rm -f "$TEMP_HTML"

echo "Generated: $OUTPUT_DIR/$OUTPUT_FILE"
