# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-27

Initial release.

### Added
- `imagegen` skill — image generation via OpenAI's `gpt-image-1.5` model, with a stdlib-only `scripts/generate.py` (size/quality/format/count/background options, `.env` key resolution) and an `references/openai-images-api.md` API reference.
- `structure-plan`, `audit-plan`, `audit-implementation` commands — a general-purpose, stack-agnostic plan → verify → implement → verify workflow.
- `install.sh` — symlinks the skills and commands into `~/.claude`, skipping existing targets.
- README documentation covering each skill/command, the workflow rationale, installation, and versioning.
- MIT license.

[1.0.0]: https://github.com/sayedhfatimi/claude-skills/releases/tag/v1.0.0
