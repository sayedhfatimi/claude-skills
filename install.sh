#!/usr/bin/env bash
# Symlink this repo's skills and commands into ~/.claude so Claude Code can discover them.
# Skips any target that already exists (won't clobber).
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

link "$REPO/skills/imagegen"                   "$CLAUDE_DIR/skills/imagegen"
link "$REPO/commands/audit-plan.md"            "$CLAUDE_DIR/commands/audit-plan.md"
link "$REPO/commands/audit-implementation.md"  "$CLAUDE_DIR/commands/audit-implementation.md"
link "$REPO/commands/structure-plan.md"        "$CLAUDE_DIR/commands/structure-plan.md"
link "$REPO/commands/refactor-pass.md"         "$CLAUDE_DIR/commands/refactor-pass.md"

echo "Done. Restart Claude Code to pick up newly linked skills and commands."
