# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- `imagegen` triggers only on explicit requests for an image file, not loose wording like "visualise" or "diagram". Every call is a paid API request, and in unattended cloud sessions the old casual triggers could spend credits unasked.
- `imagegen`: in a cloud session, save repo-bound images at their real path and commit them, since the user can't open files on the session's machine.

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

[1.2.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.0.0
