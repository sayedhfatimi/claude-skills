# claude-skills

Personal [Claude](https://claude.com) plugins and [Claude Code](https://claude.com/claude-code) slash commands, kept under version control here.

The repo holds two kinds of artifact:

- **Plugins** live in `plugins/<name>/` and are served from this repo's plugin marketplace (`.claude-plugin/marketplace.json`). Add the marketplace once in Claude and its plugins work in chat, Cowork and Claude Code, and pick up changes from this repo when it syncs.
- **Commands** live in `commands/<name>.md` as a single Markdown file and run when you type `/<name>`. `install.sh` symlinks them into `~/.claude/commands/` so Claude Code can discover them.

## Layout

```
claude-skills/
  README.md
  install.sh
  .gitignore
  .claude-plugin/
    marketplace.json
  plugins/
    imagegen/
      .claude-plugin/plugin.json
      skills/
        imagegen/
          SKILL.md
          scripts/generate.py
          references/openai-images-api.md
  commands/
    audit-plan.md
    refactor-pass.md
```

## Plugins

### `imagegen`

Generates images with OpenAI's `gpt-image-2.6-sunburst` model via the [Images API](https://platform.openai.com/docs/api-reference/images). Triggers only when you explicitly ask Claude to generate or refine an image. It deliberately ignores loose wording like "visualise", because every call is a paid API request.

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
| Complexity        | `--complexity` | model default (`high`) | `low`, `medium`, `high` — planning before rendering |
| Format            | `--format`   | `png`       | `png`, `jpeg`, `webp`                                |
| Count             | `--n`        | `1`         | `1`–`10`                                             |
| Background        | `--background` | `auto`    | `auto`, `transparent` (png/webp only), `opaque`     |
| Output directory  | `--output-dir` | `.`       | any path                                            |

**Direct usage** (the skill normally runs this for you):

```bash
python plugins/imagegen/skills/imagegen/scripts/generate.py \
  --prompt "A serene Japanese garden at dawn, soft mist, photorealistic" \
  --size 1024x1024 --quality medium --output-dir .
```

It prints the saved paths as JSON, e.g. `{"saved": ["./image-20260527-150000.png"]}`. The script is pure Python 3 standard library — no `pip install` needed. See `plugins/imagegen/skills/imagegen/references/openai-images-api.md` for advanced parameters.

## Commands

These are general-purpose development commands — language- and stack-agnostic, usable on any codebase regardless of framework (unlike the stack-specific `imagegen` plugin above).

### `/audit-plan`

Run once a plan has been drafted and before any code is written. Claude reads the **exact implementation details** of every file, function and module the plan references — verifying the assumptions the plan made, confirming real type and interface shapes, signatures, exports, and dependencies. Because it's scoped to the regions that matter, it gets precision without pulling unnecessary code into context. The goal is to ensure the planned code will genuinely fit the codebase's architecture and contracts — not merely match the surface "vibe" of the surrounding code — and to revise the plan wherever an assumption turns out to be wrong, before a single line is written.

### `/refactor-pass`

The structural-cleanup entry point, for kicking off a refactor or cleanup sprint rather than building a feature. It is a read-only, stack-agnostic pass that surveys the whole project, then works through each concern category in depth — file and folder organisation, variable/function/type naming conventions, function consolidation and decomposition, type organisation, import boundaries, and dead code — and emits a single categorised `REFACTOR_PLAN.md` at the project root, complete with a priority matrix ranking each change by effort and impact. It modifies nothing but that one plan file; you review it, prune anything out of scope, and then drive the changes. Trigger it with `/refactor-pass` or by asking Claude to "audit the codebase" or "review naming conventions".

## Installation

### Plugins (marketplace)

Add this repo as a plugin marketplace, then install its plugins:

- **Claude (web, desktop, Cowork):** Customize → Plugins → Add → Add marketplace → Add from a repository, and enter `sayedhfatimi/claude-skills`. Turn on **Sync automatically** so pushes to `main` update the installed plugins, or use **Check for updates** to pull them by hand. Plugins added here are saved to your account and sync to Claude Code when you sign in with the same account.
- **Claude Code only:**

  ```bash
  /plugin marketplace add sayedhfatimi/claude-skills
  /plugin install imagegen@claude-skills
  ```

Bump a plugin's `version` in its `plugin.json` whenever you change it, so every client sees it as an update.

### Commands

Clone the repo, then run the installer to symlink the commands into `~/.claude`:

```bash
git clone https://github.com/sayedhfatimi/claude-skills.git
cd claude-skills
./install.sh
```

To pin to a specific release instead of tracking `main`, clone a tag: `git clone --branch v1.0.0 --depth 1 https://github.com/sayedhfatimi/claude-skills.git` (see [Versioning](#versioning)).

`install.sh` skips any target that already exists, so it won't clobber existing commands. It doesn't link `imagegen`: that comes from the marketplace, and a symlink as well would load it twice. The manual equivalent:

```bash
REPO="$(pwd)"
ln -s "$REPO/commands/audit-plan.md"            ~/.claude/commands/audit-plan.md
ln -s "$REPO/commands/refactor-pass.md"         ~/.claude/commands/refactor-pass.md
```

Restart Claude Code (or start a new session) so it picks up the newly symlinked commands.

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

Re-run `install.sh` only when a new version *adds* a command (a brand-new file needs a new symlink); content changes to existing ones are picked up automatically. Marketplace plugins always track `main`, not a tag.

### Releasing

For maintainers, to keep history clean and reproducible:

- The `CHANGELOG.md` entry and the tag go in their own release commit, separate from the feature/doc commits they describe.
- Make sure each changed plugin's `version` in its `plugin.json` matches the release.
- Tag from `main` (`git tag -a vX.Y.Z`), push the tag, and publish a GitHub release with notes mirroring the changelog entry.
- Never delete, rewrite, or force-push a tag — published releases are a historical record.

## Notes

No secrets are committed to this repo. The `imagegen` plugin needs your own `OPENAI_API_KEY`, supplied via one of the resolution paths listed above.

## License

[MIT](LICENSE)
