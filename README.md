# claude-skills

Personal [Claude Code](https://claude.com/claude-code) skills and slash commands, kept under version control here and symlinked into `~/.claude` so Claude Code can discover them.

Claude Code distinguishes two kinds of artifact:

- **Skills** live in `~/.claude/skills/<name>/` as a directory with a `SKILL.md` (plus any scripts/references). They load on demand based on their `description`.
- **Commands** live in `~/.claude/commands/<name>.md` as a single Markdown file and run when you type `/<name>`.

This repo keeps each kind in its own top-level folder and symlinks them back into place.

## Layout

```
claude-skills/
  README.md
  install.sh
  .gitignore
  skills/
    imagegen/
      SKILL.md
      scripts/generate.py
      references/openai-images-api.md
  commands/
    audit-plan.md
    audit-implementation.md
    structure-plan.md
```

## Skills

### `imagegen`

Generates images with OpenAI's `gpt-image-1.5` model via the [Images API](https://platform.openai.com/docs/api-reference/images). Triggers whenever you ask Claude to generate, draw, render, or refine an image.

**Prerequisite:** an `OPENAI_API_KEY`. You don't need to export it manually — `scripts/generate.py` resolves it in this order and stops at the first hit:

1. `IMAGEGEN_ENV_FILE` env var (explicit path to a `.env` file)
2. `.env` in the current working directory
3. `.env` found by walking up the directory tree to the project root
4. `~/.env` in your home directory
5. `OPENAI_API_KEY` already set in the environment

**Parameters** (CLI flags on `generate.py`, also chosen automatically by the skill):

| Parameter         | Flag         | Default     | Options                                              |
|-------------------|--------------|-------------|------------------------------------------------------|
| Size              | `--size`     | `1024x1024` | `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait) |
| Quality           | `--quality`  | `medium`    | `low`, `medium`, `high`                              |
| Format            | `--format`   | `png`       | `png`, `jpeg`, `webp`                                |
| Count             | `--n`        | `1`         | `1`–`10`                                             |
| Background        | `--background` | `auto`    | `auto`, `transparent` (png/webp only), `opaque`     |
| Output directory  | `--output-dir` | `.`       | any path                                            |

**Direct usage** (the skill normally runs this for you):

```bash
python skills/imagegen/scripts/generate.py \
  --prompt "A serene Japanese garden at dawn, soft mist, photorealistic" \
  --size 1024x1024 --quality medium --output-dir .
```

It prints the saved paths as JSON, e.g. `{"saved": ["./image-20260527-150000.png"]}`. The script is pure Python 3 standard library — no `pip install` needed. See `skills/imagegen/references/openai-images-api.md` for advanced parameters.

## Commands

These three form a single plan → verify → implement → verify workflow. Use them in sequence: `/structure-plan` to draft, `/audit-plan` to validate the draft against real code, build, then `/audit-implementation` to confirm the build matches the plan.

### `/structure-plan`

Turns a feature name (or a hyphenated list of features) into one concrete implementation plan: what to build, every file to create or modify, the types/interfaces/schemas involved, the dependency-ordered sequence, and the assumptions `/audit-plan` should later verify.

### `/audit-plan`

Audits the plan above against the actual code surface before any implementation begins — reads the real files/functions/modules the plan references, verifies signatures, types, exports, and dependencies, flags gaps between the plan's assumptions and reality, and revises the plan where it was wrong.

### `/audit-implementation`

Audits a finished implementation against the plan that produced it — checks signatures, logic, exports, and edge cases against the spec, lists any divergences or missing pieces with their impact, and produces a verdict (fully / partially / incorrectly implemented) before any remediation.

## Installation

Clone the repo, then run the installer to symlink everything into `~/.claude`:

```bash
git clone https://github.com/sayedhfatimi/claude-skills.git
cd claude-skills
./install.sh
```

`install.sh` skips any target that already exists, so it won't clobber existing skills/commands. The manual equivalent:

```bash
REPO="$(pwd)"
ln -s "$REPO/skills/imagegen"                   ~/.claude/skills/imagegen
ln -s "$REPO/commands/audit-plan.md"            ~/.claude/commands/audit-plan.md
ln -s "$REPO/commands/audit-implementation.md"  ~/.claude/commands/audit-implementation.md
ln -s "$REPO/commands/structure-plan.md"        ~/.claude/commands/structure-plan.md
```

Restart Claude Code (or start a new session) so it picks up the newly symlinked skills and commands.

## Notes

No secrets are committed to this repo. The `imagegen` skill needs your own `OPENAI_API_KEY`, supplied via one of the resolution paths listed above.
