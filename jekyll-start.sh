#!/bin/bash
# Start Jekyll development server for resume site
#
# Usage:
#   ./jekyll-start.sh          # Build all exports, then start with livereload
#   ./jekyll-start.sh --clean  # Hard clean cache before building and starting
#
# What happens on start:
#   1. Prerequisite checks (ruby, bundle, python3, venv, pandoc, xelatex)
#   2. Full jekyll build (generates Pandoc PDF/DOCX)
#   3. XeLaTeX typeset PDFs (brief + full, if available)
#   4. Jekyll serve with --livereload --incremental
#
# Default flags: --trace --livereload --incremental
# Port: 4000 (configured in _config.yml)
# Preview: http://localhost:4000/resume/
# Print:   http://localhost:4000/resume/print/
#
# Prerequisites:
#   - Ruby 3.3+ via rbenv (see .ruby-version)
#   - bundle install completed
#   - Python 3.10+ with .venv (for PDF exports)
#   - pandoc (for Pandoc PDF/DOCX during Jekyll build)
#   - xelatex (for LaTeX PDF — MacTeX on macOS, texlive-xetex on Ubuntu)
#   - On macOS: launch VS Code from terminal, not Dock/Spotlight
#
# See README.md "Prerequisites" section for full install instructions.
#
# =============================================================================
# Jekyll serve flags:
#   --trace         Show full Ruby backtrace on errors
#   --livereload    Auto-refresh browser on file save
#   --incremental   Only rebuild changed pages (faster, but restart
#                   if edits to _includes/ or _layouts/ seem stale)
# =============================================================================

set -e

PORT=4000
CLEAN=false
WARNINGS=()

for arg in "$@"; do
    case "$arg" in
        --clean)
            CLEAN=true
            ;;
        --help)
            echo "Usage: $0 [--clean] [--help]"
            echo "  --clean  Hard clean (.jekyll-cache, _site/, .jekyll-metadata) before starting"
            echo "  --help   Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--clean] [--help]"
            exit 1
            ;;
    esac
done

# =============================================================================
# Prerequisite checks
# =============================================================================

echo "Checking prerequisites..."
echo ""

# --- Ruby / Jekyll ---
if ! command -v ruby &> /dev/null; then
    echo "ERROR: ruby not found. Install via rbenv:"
    echo "  brew install rbenv ruby-build   # macOS"
    echo "  # See README.md for WSL2/Ubuntu instructions"
    exit 1
fi

RUBY_VERSION=$(ruby -e "puts RUBY_VERSION")
RUBY_MAJOR=$(echo "$RUBY_VERSION" | cut -d. -f1)
RUBY_MINOR=$(echo "$RUBY_VERSION" | cut -d. -f2)
if [ "$RUBY_MAJOR" -lt 3 ] || { [ "$RUBY_MAJOR" -eq 3 ] && [ "$RUBY_MINOR" -lt 2 ]; }; then
    echo "ERROR: Ruby >= 3.2 required (found $RUBY_VERSION)"
    echo "  rbenv install 3.3.11 && rbenv local 3.3.11"
    exit 1
fi
echo "  ✓ ruby $RUBY_VERSION"

if ! command -v bundle &> /dev/null; then
    echo "ERROR: bundler not found. Run: gem install bundler"
    exit 1
fi
echo "  ✓ bundler $(bundle --version | awk '{print $NF}')"

if [ ! -f "Gemfile.lock" ]; then
    echo "ERROR: Gemfile.lock not found. Run: bundle install"
    exit 1
fi

# --- Pandoc (required for Jekyll build PDF/DOCX) ---
if ! command -v pandoc &> /dev/null; then
    echo "  ✗ pandoc not found — Jekyll build will skip PDF/DOCX exports"
    echo "    Install: brew install pandoc  (macOS)"
    echo "             sudo apt install pandoc  (Ubuntu)"
    WARNINGS+=("pandoc missing — no Pandoc PDF/DOCX")
else
    echo "  ✓ pandoc $(pandoc --version | head -1 | awk '{print $2}')"
fi

# --- Python 3 ---
if ! command -v python3 &> /dev/null; then
    echo "  ✗ python3 not found — PDF export pipeline unavailable"
    echo "    Install: brew install python  (macOS)"
    echo "             sudo apt install python3 python3-venv  (Ubuntu)"
    WARNINGS+=("python3 missing — no LaTeX PDF")
else
    PY_VERSION=$(python3 --version | awk '{print $2}')
    echo "  ✓ python3 $PY_VERSION"

    # --- Python venv ---
    if [ ! -f ".venv/bin/activate" ]; then
        echo "  ✗ .venv not found — Python PDF exports unavailable"
        echo "    Create it:"
        echo "      python3 -m venv .venv"
        echo "      source .venv/bin/activate"
        echo "      pip install -r requirements.txt"
        WARNINGS+=(".venv missing — no LaTeX PDF")
    else
        # Activate and check packages
        source .venv/bin/activate

        if ! python3 -c "import jinja2" 2>/dev/null; then
            echo "  ✗ jinja2 not installed in .venv"
            echo "    Fix: source .venv/bin/activate && pip install -r requirements.txt"
            WARNINGS+=("jinja2 missing in .venv — no LaTeX PDF")
        else
            echo "  ✓ jinja2 $(python3 -c 'import jinja2; print(jinja2.__version__)')"
        fi
    fi
fi

# --- XeLaTeX ---
if ! command -v xelatex &> /dev/null; then
    echo "  ✗ xelatex not found — LaTeX PDF compilation unavailable"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "    Install: brew install --cask mactex"
        echo "         or: brew install --cask basictex && sudo tlmgr install collection-xetex"
    else
        echo "    Install: sudo apt install texlive-xetex texlive-fonts-recommended texlive-latex-extra"
    fi
    WARNINGS+=("xelatex missing — .tex will generate but no LaTeX PDF")
else
    echo "  ✓ xelatex $(xelatex --version | head -1 | sed 's/.*Version //' | awk '{print $1}')"
fi

# --- pdflatex (used by Pandoc) ---
if command -v pandoc &> /dev/null && ! command -v pdflatex &> /dev/null; then
    echo "  ✗ pdflatex not found — Pandoc PDF export will fail"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "    Install: brew install --cask basictex"
    else
        echo "    Install: sudo apt install texlive-latex-base texlive-fonts-recommended"
    fi
    WARNINGS+=("pdflatex missing — Pandoc PDF will fail")
elif command -v pdflatex &> /dev/null; then
    echo "  ✓ pdflatex $(pdflatex --version | head -1 | sed 's/.*Version //' | awk '{print $1}')"
fi

echo ""

# Print summary of warnings
if [ ${#WARNINGS[@]} -gt 0 ]; then
    echo "⚠ Setup warnings (non-fatal — Jekyll site will still build):"
    for w in "${WARNINGS[@]}"; do
        echo "  • $w"
    done
    echo ""
    echo "  See README.md 'Prerequisites' for install instructions."
    echo ""
fi

# =============================================================================
# Port check
# =============================================================================

check_port() {
    local pid=""
    local process=""

    if command -v lsof &>/dev/null; then
        pid=$(lsof -i :"$PORT" -sTCP:LISTEN -P -n -t 2>/dev/null | head -1)
        if [ -n "$pid" ]; then
            process=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
        fi
    elif command -v ss &>/dev/null; then
        pid=$(ss -tlnp "sport = :$PORT" 2>/dev/null | grep -oP 'pid=\K[0-9]+' | head -1)
        if [ -n "$pid" ]; then
            process=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
        fi
    fi

    if [ -n "$pid" ]; then
        echo "ERROR: Port $PORT is already in use by $process (PID $pid)"
        echo ""
        echo "Options:"
        echo "  kill $pid              # Stop the existing process"
        echo "  kill -9 $pid           # Force stop if it won't die"
        echo "  ./jekyll-clean.sh      # If it's a stale Jekyll, clean and retry"
        exit 1
    fi
}

check_port

# =============================================================================
# Clean (optional)
# =============================================================================

if [ "$CLEAN" = true ]; then
    echo "Hard cleaning before start..."
    bundle exec jekyll clean
    [ -d ".jekyll-cache" ] && rm -rf .jekyll-cache && echo "Removed .jekyll-cache"
    [ -f ".jekyll-metadata" ] && rm -f .jekyll-metadata && echo "Removed .jekyll-metadata"
    [ -d "_site" ] && rm -rf _site && echo "Removed _site/"
    echo ""
fi

# =============================================================================
# Build
# =============================================================================

echo "Running initial build..."
bundle exec jekyll build --quiet
echo "  ✓ Jekyll build complete (HTML + Pandoc PDF/DOCX)"

# --- LaTeX PDFs ---
if [ -f ".venv/bin/activate" ]; then
    # Ensure venv is active (may already be from prereq checks)
    source .venv/bin/activate 2>/dev/null || true

    # --- LaTeX PDF (Full) ---
    if [ -f "bin/generate-latex.py" ] && python3 -c "import jinja2, yaml" 2>/dev/null; then
        echo "Generating LaTeX PDFs..."

        # Full version
        if python3 bin/generate-latex.py --output "_site/downloads/McGarrah-Resume-latex.tex" 2>&1 | grep -q "Generated:"; then
            echo "  ✓ McGarrah-Resume-latex.tex"

            if command -v xelatex &> /dev/null; then
                xelatex -interaction=nonstopmode -output-directory="_site/downloads" \
                    "_site/downloads/McGarrah-Resume-latex.tex" > /dev/null 2>&1 || true
                xelatex -interaction=nonstopmode -output-directory="_site/downloads" \
                    "_site/downloads/McGarrah-Resume-latex.tex" > /dev/null 2>&1 || true
                rm -f _site/downloads/McGarrah-Resume-latex.aux _site/downloads/McGarrah-Resume-latex.log _site/downloads/McGarrah-Resume-latex.out

                if [ -f "_site/downloads/McGarrah-Resume-latex.pdf" ]; then
                    echo "  ✓ McGarrah-Resume-latex.pdf (full)"
                else
                    echo "  ✗ XeLaTeX compilation failed (full)"
                    echo "    Debug: xelatex -interaction=nonstopmode _site/downloads/McGarrah-Resume-latex.tex"
                fi
            else
                echo "  ⚠ .tex generated but xelatex not available for PDF compilation"
            fi
        else
            echo "  ✗ LaTeX template rendering failed (full)"
            echo "    Debug: python3 bin/generate-latex.py --output /tmp/test.tex"
        fi

        # Brief version
        if python3 bin/generate-latex.py --template resume-brief.tex.j2 --output "_site/downloads/McGarrah-Resume-brief.tex" 2>&1 | grep -q "Generated:"; then
            echo "  ✓ McGarrah-Resume-brief.tex"

            if command -v xelatex &> /dev/null; then
                xelatex -interaction=nonstopmode -output-directory="_site/downloads" \
                    "_site/downloads/McGarrah-Resume-brief.tex" > /dev/null 2>&1 || true
                xelatex -interaction=nonstopmode -output-directory="_site/downloads" \
                    "_site/downloads/McGarrah-Resume-brief.tex" > /dev/null 2>&1 || true
                rm -f _site/downloads/McGarrah-Resume-brief.aux _site/downloads/McGarrah-Resume-brief.log _site/downloads/McGarrah-Resume-brief.out

                if [ -f "_site/downloads/McGarrah-Resume-brief.pdf" ]; then
                    echo "  ✓ McGarrah-Resume-brief.pdf (brief)"
                else
                    echo "  ✗ XeLaTeX compilation failed (brief)"
                    echo "    Debug: xelatex -interaction=nonstopmode _site/downloads/McGarrah-Resume-brief.tex"
                fi
            else
                echo "  ⚠ .tex generated but xelatex not available for PDF compilation"
            fi
        else
            echo "  ✗ LaTeX template rendering failed (brief)"
            echo "    Debug: python3 bin/generate-latex.py --template resume-brief.tex.j2 --output /tmp/test.tex"
        fi
    fi
fi

echo ""

# =============================================================================
# Serve
# =============================================================================

echo "Starting Jekyll on port $PORT..."
echo "  Preview: http://localhost:$PORT/resume/"
echo "  Print:   http://localhost:$PORT/resume/print/"
echo "  Machine: http://localhost:$PORT/resume/machine/"
echo ""
bundle exec jekyll serve --trace --livereload --incremental
