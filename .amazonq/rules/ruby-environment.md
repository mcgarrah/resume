# Ruby Environment — macOS rbenv Configuration

## The Problem

macOS ships system Ruby 2.6 which is too old for Jekyll and modern YAML APIs.
Homebrew Ruby 4.0 breaks Jekyll `--livereload`. Use rbenv with Ruby 3.3.11.

## Current Setup

| Component | Path | Version |
|-----------|------|---------|
| System Ruby | `/System/Library/Frameworks/Ruby.framework/` | 2.6.10 (do not use) |
| rbenv Ruby | `~/.rbenv/versions/3.3.11/bin/ruby` | 3.3.11 ✅ (use this) |

This repo has `.ruby-version` set to `3.3.11` in the repo root.

## Platform Differences

### macOS

The hardest environment. Three compounding issues:

1. **System Ruby 2.6** is SIP-protected and too old for Jekyll 4.4.1
2. **Homebrew Ruby 4.0** works for builds but breaks `--livereload` (EventMachine)
3. **Non-interactive shells** (Amazon Q `executeBash`, VS Code tasks, cron) don't source
   `~/.zshrc`, so `eval "$(rbenv init - zsh)"` never runs and the rbenv shim resolves
   to system Ruby 2.6 even when `.ruby-version` is present
4. **GUI-launched VS Code** (Dock, Spotlight) inherits `launchd` environment, not shell
   PATH — always launch VS Code from a terminal on macOS

### WSL2 / Linux

Mostly "just works." Key differences from macOS:

- **No system Ruby conflict** — WSL2 Debian/Ubuntu don't ship a system Ruby that
  interferes. Install rbenv normally and it's the only Ruby on PATH.
- **VS Code Remote Server** runs inside a login shell that sources `~/.bashrc` or
  `~/.zshrc` — rbenv init runs automatically. The GUI app PATH problem doesn't exist.
- **Amazon Q `executeBash`** in VS Code Remote (WSL2) runs through the Remote Server's
  shell, which typically has rbenv initialized. Less likely to hit the shim resolution
  bug than macOS, but `.ruby-version` in the repo root is still the safest guarantee.
- **`--livereload` works** with Homebrew or rbenv Ruby — the EventMachine compatibility
  issue is macOS-specific.
- **File watching** for `--incremental` is more reliable on Linux (inotify) than macOS
  (FSEvents). Fewer stale cache issues.

### Windows (native, not WSL2)

Not a supported development environment for this project. All Windows work goes through
WSL2. If Ruby commands are needed on native Windows, use the WSL2 terminal.

## Amazon Q / Non-Interactive Shell Workaround

**Always use the rbenv Ruby binary directly for validation:**

```bash
$HOME/.rbenv/versions/3.3.11/bin/ruby -e "
  require 'yaml'; require 'date'
  YAML.load_file('_data/data.yml', permitted_classes: [Date])
  puts 'YAML is valid'
"
```

This works on both macOS and WSL2 regardless of shell initialization state.

**Do NOT use:**
- `ruby -e "..."` — may resolve to system Ruby 2.6 on macOS
- `eval "$(rbenv init - zsh)" && ruby ...` — unreliable in non-interactive shells on macOS

## When Running Ruby Commands

- Use `$HOME/.rbenv/versions/3.3.11/bin/ruby` for one-off validation
- Use `bundle exec` for all Jekyll commands
- Run `ruby --version` first to verify you're on 3.3.x before proceeding

See `mcgarrah.github.io/.amazonq/rules/ruby-environment.md` for the full reference.
