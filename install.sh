#!/usr/bin/env bash
# install.sh — bootstrap a freshly-cloned copy of this wiki template.
#
# Non-destructive: DRY-RUN by default (pass --apply to make changes), never
# overwrites existing files. Creates the optional directories the docs reference
# and prints the placeholder checklist so a new adopter knows what to edit.
#
# This is a fork-and-edit *scaffolder*, not a config installer — you use this repo
# AS your wiki, so there is nothing to copy into a system config dir. Pattern
# adapted from PropterMaltwo (https://github.com/PropterMalone/PropterMaltwo),
# MIT License (c) 2026 PropterMalone — reshaped from their config-merge installer.

set -euo pipefail

apply=0
[ "${1:-}" = "--apply" ] && apply=1
root="$(cd "$(dirname "$0")" && pwd)"

say() { printf '%s\n' "$*"; }

if [ "$apply" -eq 1 ]; then
  say "MODE: apply (creating directories below)"
else
  say "MODE: dry-run (no changes — pass --apply to act)"
fi
say ""

say "Optional directories referenced by CLAUDE.md / README:"
for d in projects ideas; do
  if [ -d "$root/$d" ]; then
    say "  ok:    $d/ already exists"
  elif [ "$apply" -eq 1 ]; then
    mkdir -p "$root/$d"
    : > "$root/$d/.gitkeep"
    say "  made:  $d/ (+ .gitkeep)"
  else
    say "  would: create $d/ (+ .gitkeep)"
  fi
done
say ""

say "Next steps — edit these by hand (the installer never touches your content):"
say "  1. CLAUDE.md  — fill the placeholders (see 'Placeholders to Fill' at the top)"
say "  2. home.md    — replace the example homepage with your own"
say "  3. Workflow   — uncomment the GitHub or Forgejo/Gitea PR block in CLAUDE.md"
say "  4. optional   — reset git history for a clean start:  rm -rf .git && git init"
say ""

if [ "$apply" -eq 0 ]; then
  say "Dry-run complete. Re-run with --apply to create the directories above."
fi
