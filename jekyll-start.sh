#!/bin/bash
# Start Jekyll development server for resume site
#
# Usage:
#   ./jekyll-start.sh          # Start with default flags (livereload, incremental)
#   ./jekyll-start.sh --clean  # Hard clean cache before starting (fixes macOS FSEvents staleness)
#
# Default flags: --trace --livereload --incremental
# Port: 4000 (configured in _config.yml)
# Preview: http://localhost:4000/resume/
# Print:   http://localhost:4000/resume/print/
#
# Prerequisites:
#   - Ruby 3.3+ via rbenv (see .ruby-version)
#   - bundle install completed
#   - On macOS: launch VS Code from terminal, not Dock/Spotlight
#
# See mcgarrah.github.io/.amazonq/rules/ruby-environment.md for full setup guide.
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

# Check if port is already in use
check_port() {
    local pid=""
    local process=""

    if command -v lsof &>/dev/null; then
        # macOS and most Linux
        pid=$(lsof -i :"$PORT" -sTCP:LISTEN -P -n -t 2>/dev/null | head -1)
        if [ -n "$pid" ]; then
            process=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
        fi
    elif command -v ss &>/dev/null; then
        # Linux without lsof (some minimal WSL2 installs)
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

# Optional hard clean before starting
if [ "$CLEAN" = true ]; then
    echo "Hard cleaning before start..."
    bundle exec jekyll clean
    [ -d ".jekyll-cache" ] && rm -rf .jekyll-cache && echo "Removed .jekyll-cache"
    [ -f ".jekyll-metadata" ] && rm -f .jekyll-metadata && echo "Removed .jekyll-metadata"
    [ -d "_site" ] && rm -rf _site && echo "Removed _site/"
    echo ""
fi

echo "Starting Jekyll on port $PORT..."
echo "  Preview: http://localhost:$PORT/resume/"
echo "  Print:   http://localhost:$PORT/resume/print/"
echo ""
bundle exec jekyll serve --trace --livereload --incremental
