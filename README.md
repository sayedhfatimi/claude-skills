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
    refactor-pass.md
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

These are general-purpose development commands — language- and stack-agnostic, usable on any codebase regardless of framework (unlike the stack-specific `imagegen` skill above).

These three form a single `/structure-plan` → `/audit-plan` → build → `/audit-implementation` workflow. They exist to solve a specific problem: a fresh Claude session has **no reliable knowledge of the repo** it's working in. Whatever lives in memory may be stale, and reading the whole codebase up front floods the context with detail that drowns out the task. The workflow is therefore a deliberate two-phase reading strategy — **broad-and-shallow first, narrow-and-deep second** — that builds just enough accurate context to write code that actually fits, without polluting the context window.

### `/structure-plan`

The broad, shallow pass. Claude reads the *shape* of the codebase — the types, interfaces, functions, and variables relevant to the work, noting where they live (files and line numbers) — but deliberately **does not** read exact implementation bodies or trace how each symbol ripples through the rest of the code. The output is one concrete plan: what to build, every file to create or modify, the types/interfaces/schemas involved, the dependency-ordered sequence, and the assumptions that `/audit-plan` will later verify. This establishes a cheap, approximate map of the territory without spending context on detail that may not matter.

### `/audit-plan`

The narrow, deep pass. Using the regions `/structure-plan` already identified, Claude now reads the **exact implementation details** of just those areas — verifying the assumptions the plan made, confirming real type and interface shapes, signatures, exports, and dependencies. Because it's scoped to the regions that matter, it gets precision without pulling unnecessary code into context. The goal is to ensure the planned code will genuinely fit the codebase's architecture and contracts — not merely match the surface "vibe" of the surrounding code — and to revise the plan wherever an assumption turns out to be wrong, before a single line is written.

### `/audit-implementation`

The closing check. After the code is written, Claude audits what was actually built against what the final plan/spec required — checking signatures, logic, exports, and edge cases against the spec, listing any divergences or missing pieces with their impact, and producing a verdict (fully / partially / incorrectly implemented) before any remediation. This confirms the implementation meets the standard and functionality the plan set out, rather than something that merely looks plausible.

### `/refactor-pass`

The structural-cleanup entry point — the counterpart to the plan/audit trio, run *before* `/structure-plan` when kicking off a refactor or cleanup sprint rather than building a feature. It is a read-only, stack-agnostic pass that surveys the whole project, then works through each concern category in depth — file and folder organisation, variable/function/type naming conventions, function consolidation and decomposition, type organisation, import boundaries, and dead code — and emits a single categorised `REFACTOR_PLAN.md` at the project root, complete with a priority matrix ranking each change by effort and impact. It modifies nothing but that one plan file; you review it, prune anything out of scope, and then drive the changes (optionally through `/structure-plan`). Trigger it with `/refactor-pass` or by asking Claude to "audit the codebase" or "review naming conventions".

## Installation

Clone the repo, then run the installer to symlink everything into `~/.claude`:

```bash
git clone https://github.com/sayedhfatimi/claude-skills.git
cd claude-skills
./install.sh
```

To pin to a specific release instead of tracking `main`, clone a tag: `git clone --branch v1.0.0 --depth 1 https://github.com/sayedhfatimi/claude-skills.git` (see [Versioning](#versioning)).

`install.sh` skips any target that already exists, so it won't clobber existing skills/commands. The manual equivalent:

```bash
REPO="$(pwd)"
ln -s "$REPO/skills/imagegen"                   ~/.claude/skills/imagegen
ln -s "$REPO/commands/audit-plan.md"            ~/.claude/commands/audit-plan.md
ln -s "$REPO/commands/audit-implementation.md"  ~/.claude/commands/audit-implementation.md
ln -s "$REPO/commands/structure-plan.md"        ~/.claude/commands/structure-plan.md
ln -s "$REPO/commands/refactor-pass.md"         ~/.claude/commands/refactor-pass.md
```

Restart Claude Code (or start a new session) so it picks up the newly symlinked skills and commands.

## Versioning

Releases are semver git tags (`vMAJOR.MINOR.PATCH`). `main` is the rolling latest; tags mark stable points, and [`CHANGELOG.md`](CHANGELOG.md) records what changed in each one.

**Pin to a version.** Clone the tag you want, then install:

```bash
git clone --branch v1.0.0 --depth 1 https://github.com/sayedhfatimi/claude-skills.git
cd claude-skills
./install.sh
```

**Switching versions is just a checkout.** `install.sh` symlinks the entries in `~/.claude` to files in your clone's working tree, so the *contents* the symlinks resolve to always reflect whatever you have checked out — there's nothing to re-link when you move between versions:

```bash
git -C <clone> fetch --tags && git -C <clone> checkout vX.Y.Z   # pin to a release
git -C <clone> checkout main && git -C <clone> pull             # back to latest
```

Re-run `install.sh` only when a new version *adds* a skill or command (a brand-new file needs a new symlink); content changes to existing ones are picked up automatically.

### Releasing

For maintainers, to keep history clean and reproducible:

- The `CHANGELOG.md` entry and the tag go in their own release commit, separate from the feature/doc commits they describe.
- Tag from `main` (`git tag -a vX.Y.Z`), push the tag, and publish a GitHub release with notes mirroring the changelog entry.
- Never delete, rewrite, or force-push a tag — published releases are a historical record.

## Notes

No secrets are committed to this repo. The `imagegen` skill needs your own `OPENAI_API_KEY`, supplied via one of the resolution paths listed above.

## License

[MIT](LICENSE)
