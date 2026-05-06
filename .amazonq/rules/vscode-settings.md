# .vscode/settings.json — Intentionally Tracked

## Why This File Is Committed

The `.vscode/settings.json` file is intentionally tracked in this repository. It contains
the Jekyll Run plugin configuration needed to serve the resume site locally:

- `--livereload --incremental` — enables live reload and incremental builds
- `--trace` — verbose error output for debugging
- `stopServerOnExit: true` — cleanly stops the Jekyll server when VS Code closes

These settings are project-specific (not personal preference) and ensure anyone cloning
the repo can use the Jekyll Run VS Code extension with the correct arguments immediately.

## Do Not Remove From Git

This file should remain tracked. It is part of the local development workflow for
previewing the resume at `http://localhost:4000/resume/` using the Jekyll Run extension.
