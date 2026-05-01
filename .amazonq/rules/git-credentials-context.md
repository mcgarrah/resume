# Git Credential & Operations Context

## Git Authentication

GitHub authentication uses the `gh` CLI credential helper scoped to `github.com`.
See `mcgarrah.github.io/.amazonq/rules/git-credentials-context.md` for the full
credential helper configuration, VPN diagnostics, and troubleshooting.

**Quick reference:**
- GitHub push/pull uses `gh auth git-credential` (personal `mcgarrah` account)
- If HTTP 403 on push: run `vpn` alias first to check VPN status before debugging credentials
- The 403 from VPN/proxy issues looks identical to credential misconfiguration

## File Operations

Always use `git mv` instead of `mv` when renaming or moving tracked files. This preserves
Git history (rename detection) so `git log --follow` traces the file back to its original
commits. A plain `mv` + `git add` can work, but it relies on Git's similarity heuristic
and may lose history if the file content also changes significantly in the same commit.

```bash
# Correct — preserves history
git mv old-path/file.md new-path/file.md

# Avoid — history may not follow
mv old-path/file.md new-path/file.md
```

The only exception is for untracked files that have never been committed.
