# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-11-26

### Added
- This repo is now a Claude plugin marketplace (`.claude-plugin/marketplace.json`). Add it in Claude under Customize → Plugins, or with `/plugin marketplace add sayedhfatimi/claude-skills` in Claude Code, and install `imagegen` from it.

### Changed
- **Breaking:** `imagegen` moved from `skills/imagegen` to `plugins/imagegen/skills/imagegen` and ships as a plugin. `install.sh` no longer symlinks it; remove an existing `~/.claude/skills/imagegen` symlink and install the plugin from the marketplace instead.
- `imagegen` SKILL.md: run `generate.py` by its full path in the skill's own folder, so it works wherever the plugin is installed and images save in the working directory.
- `refactor-pass` now suggests turning the plan into an implementation plan with superpowers:writing-plans, instead of the removed `/structure-plan`.
- `imagegen` triggers only on explicit requests for an image file, not loose wording like "visualise" or "diagram". Every call is a paid API request, and in unattended cloud sessions the old casual triggers could spend credits unasked.
- `imagegen`: in a cloud session, save repo-bound images at their real path and commit them, since the user can't open files on the session's machine.

### Removed
- **Breaking:** `structure-plan` and `audit-implementation` commands, superseded by model and harness updates and the superpowers planning skills. `install.sh` no longer links them; delete any existing symlinks in `~/.claude/commands/`.

### Fixed
- `imagegen` SKILL.md: removed a non-working `import anthropic_imagegen_helper` example.

## [1.2.0] - 2026-11-22

### Changed
- `imagegen` now uses OpenAI's `gpt-image-2.6-sunburst`, the same model as Valeon's covers (`gpt-image-1.5` is removed from the API on 1 Dec 2026).

### Added
- `imagegen`: optional `--complexity` flag (`low` / `medium` / `high`) for how much the 2.6 models plan before rendering; omitted, the model default (`high`) applies.

### Fixed
- `imagegen` API reference: GPT image models don't return `revised_prompt`, and pricing is per token, not the old per-image table.
- `imagegen`: `generate.py` now reads a `.env` that's a named pipe (as 1Password mounts them) instead of skipping it, gives up on a silent pipe after 15s, and accepts `export KEY=value` lines.

## [1.1.0] - 2026-06-23

### Added
- `refactor-pass` command — read-only, stack-agnostic codebase analysis that writes a structured `REFACTOR_PLAN.md` (naming conventions, file/folder organisation, function/type consolidation, dead code, import boundaries, priority matrix). Complements the `structure-plan` → `audit-plan` → `audit-implementation` workflow as its structural-cleanup entry point.
- `install.sh` now symlinks `commands/refactor-pass.md`.

## [1.0.0] - 2026-05-27

Initial release.

### Added
- `imagegen` skill — image generation via OpenAI's `gpt-image-1.5` model, with a stdlib-only `scripts/generate.py` (size/quality/format/count/background options, `.env` key resolution) and an `references/openai-images-api.md` API reference.
- `structure-plan`, `audit-plan`, `audit-implementation` commands — a general-purpose, stack-agnostic plan → verify → implement → verify workflow.
- `install.sh` — symlinks the skills and commands into `~/.claude`, skipping existing targets.
- README documentation covering each skill/command, the workflow rationale, installation, and versioning.
- MIT license.

[2.0.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v2.0.0
[1.2.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.0.0
