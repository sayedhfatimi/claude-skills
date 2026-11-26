#!/usr/bin/env bash
# Symlink this repo's commands into ~/.claude so Claude Code can discover them.
# Skips any target that already exists (won't clobber).
# imagegen is not linked: it ships as a plugin from this repo's marketplace (see README),
# and account plugins sync to Claude Code, so a symlink would load it twice.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

link() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    echo "skip (exists): $dst"
  else
    ln -s "$src" "$dst"
    echo "linked: $dst -> $src"
  fi
}

link "$REPO/commands/audit-plan.md"            "$CLAUDE_DIR/commands/audit-plan.md"
link "$REPO/commands/refactor-pass.md"         "$CLAUDE_DIR/commands/refactor-pass.md"

echo "Done. Restart Claude Code to pick up newly linked commands."
