#!/bin/bash
# Generate LaTeX resume and compile to PDF
# Run from the resume project root after `bundle exec jekyll build`
#
# Usage: bin/generate-latex.sh

set -e

OUTPUT_DIR="_site/downloads"
TEX_FILE="$OUTPUT_DIR/McGarrah-Resume-long.tex"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Error: $OUTPUT_DIR not found. Run 'bundle exec jekyll build' first."
  exit 1
fi

# Generate .tex from YAML data
python3 bin/generate-latex.py --output "$TEX_FILE"

# Compile to PDF if xelatex is available
if command -v xelatex &> /dev/null; then
  xelatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" > /dev/null 2>&1 || true
  # Run twice for cross-references
  xelatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" 2>&1 | tail -30
  
  if [ -f "$OUTPUT_DIR/McGarrah-Resume-long.pdf" ]; then
    echo "Generated: $OUTPUT_DIR/McGarrah-Resume-long.pdf"
    # Clean up LaTeX auxiliary files on success
    rm -f "$OUTPUT_DIR"/*.aux "$OUTPUT_DIR"/*.log "$OUTPUT_DIR"/*.out "$OUTPUT_DIR"/missfont.log
  else
    echo "Error: PDF compilation failed."
    if [ -f "$OUTPUT_DIR/McGarrah-Resume-long.log" ]; then
      echo "Last 40 lines of LaTeX log:"
      tail -40 "$OUTPUT_DIR/McGarrah-Resume-long.log"
    fi
    exit 1
  fi
else
  echo "Generated: $TEX_FILE (xelatex not available for PDF compilation)"
fi
