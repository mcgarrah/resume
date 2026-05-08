#!/bin/bash
# Generate brief LaTeX resume (summaries only, early career consolidated)
# Run from the resume project root after `bundle exec jekyll build`
#
# Usage: bin/generate-brief.sh

set -e

OUTPUT_DIR="_site/downloads"
TEX_FILE="$OUTPUT_DIR/McGarrah-Resume-brief.tex"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Error: $OUTPUT_DIR not found. Run 'bundle exec jekyll build' first."
  exit 1
fi

# Generate .tex from YAML data using brief template
python3 bin/generate-latex.py --template resume-brief.tex.j2 --output "$TEX_FILE"

# Compile to PDF if xelatex is available
if command -v xelatex &> /dev/null; then
  xelatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" > /dev/null 2>&1 || true
  # Run twice for cross-references
  xelatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" > /dev/null 2>&1 || true

  # Clean up LaTeX auxiliary files
  rm -f "$OUTPUT_DIR"/McGarrah-Resume-brief.aux "$OUTPUT_DIR"/McGarrah-Resume-brief.log \
        "$OUTPUT_DIR"/McGarrah-Resume-brief.out

  if [ -f "$OUTPUT_DIR/McGarrah-Resume-brief.pdf" ]; then
    echo "Generated: $OUTPUT_DIR/McGarrah-Resume-brief.pdf"
  else
    echo "Error: PDF compilation failed. Check the .tex file for errors."
    exit 1
  fi
else
  echo "Generated: $TEX_FILE (xelatex not available for PDF compilation)"
fi
