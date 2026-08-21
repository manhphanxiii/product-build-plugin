# Agent instructions

## Scope and destinations

This is a self-contained skill chain for building a product from idea to code that has passed the ship gate.
Read `README.md` for the product overview before changing anything in this folder.
When the overview differs from executable code, manifests, tests, or the relevant `SKILL.md`, those implementation sources are authoritative and `README.md` must be corrected.
Use the canonical destinations defined by the skills: chain documents go into `prd/`, production code into `app/`, and prototypes into `demos/prototypes/`; only the explicit skill rules may additionally write promoted demos under `demos/<name>/`, routine definitions under `routines/`, or dated product reports under `report/product/`.
If a destination directory is missing, the agent must state its path, propose creating it, and wait for approval.
`<root>` is the product repository: a skill uses the path the user supplied, falls back to the Git root of the current working directory, requires `<root>/prd/roadmap.md` to exist, and never accepts this skill-set repository as `<root>`.
`start-repo` is the exception: it resolves `<root>` through its interview and does not require `prd/roadmap.md` to exist before initialization.
No skill writes chain artifacts into this repository, and every path in a skill without an explicit prefix is relative to `<root>`.
Never edit `client-note/` or runtime content in `app/knowledge-base/`.

## Portability and hosts

First-party skill instructions and bundled resources must not depend on files outside this repository.
Optional runtime tools must have declared fallbacks.
The skill set must work correctly when installed as a Claude Code plugin or a Codex universal plugin.
Standalone Codex installation through `scripts/install-codex.sh` is a fallback for development and pre-publication cloud testing, not the production distribution path.
Do not reference the name, brand, or path of any other skill set in this folder, except `skills/lavish/`, a third-party MIT skill by Kun Chen vendored from <https://github.com/kunchenguid/lavish-axi>. Keep its `license` and `metadata.author` frontmatter intact.
`SKILL.md`, `AGENTS.md`, and `CLAUDE.md` instruction files in this repository are written in English; `README.md` is written in Vietnamese; templates under `skills/*/assets/` and their generated output in product repositories use the product language, including Vietnamese when configured.
A skill calls another skill through the Skill tool by its namespaced name `build:<skill>` on Claude Code.
On Codex, a skill calls another by reading the complete sibling `SKILL.md` under `<skill_dir>/../<skill>/`, as the shared `## Host resolution` block defines.
A script bundled with a skill is addressed as `<skill_dir>/scripts/<file>`, never by a path relative to the current working directory or through a host-specific plugin root environment variable.
Keep Lavish as the default surface, use the Artifact tool only when it and `artifact-design` are available, and keep Markdown in the conversation as the universal fallback.
Write command mentions in first-party skill content in canonical Claude Code form `/build:<skill>` and let the shared Host resolution block map them for Codex.
Codex plugin selectors use `$build:<skill>`; standalone fallback selectors use `$<skill>`.

## Shared blocks

The shared `## Host resolution` preamble must remain byte-identical across the nine first-party skills, while skill-specific tails may differ.
The shared `## Review gate` preamble must remain byte-identical across the six document-generating skills, while skill-specific tails may differ to encode roadmap-row ownership.
The shared `## Root resolution` block must remain byte-identical except in `start-repo`, which uses `## Ground rules`, `update`, where Phase 0 already uses Q1 and interactive runs always ask for language, and `review-code`, which receives `<root>` from its caller and adds diff and sub-agent instructions.
`start-repo` must contain `## Plan gate`, and every write phase from phase 7 through phase 10 must appear after it.

## Skill metadata and manifests

For every skill, including Lavish, keep `interface.display_name` and `interface.short_description` in `skills/<name>/agents/openai.yaml` consistent with the frontmatter in its `SKILL.md`, and include `policy` when the skill is explicit-only.
A new first-party skill requires `skills/<name>/SKILL.md`, matching Codex interface metadata at `skills/<name>/agents/openai.yaml`, and the corresponding README chain and installation updates; neither plugin manifest lists skills individually.
When adding or renaming a skill, consider standalone Codex name collisions and keep `skills/<name>/agents/openai.yaml` aligned with the skill frontmatter.
Frontmatter in first-party `SKILL.md` files must stay within the fields accepted by the Codex plugin validator.
Skills that must remain explicit-only use `policy.allow_implicit_invocation: false` in their `skills/<name>/agents/openai.yaml` plus an instruction-level invocation guard that is also safe on Claude Code.
Keep shared metadata and the release version synchronized between `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.

## Release checks

`scripts/check.py` enforces shared-block, skill-metadata, and manifest-synchronization invariants, with negative fixtures in `tests/`.
The checker requires every first-party review-surface probe to use separate CLI and current-platform browser-opener checks and rejects chained forms that can hide a working setup behind the other platform's exit status.
Every `vX.Y.Z` release ref in `README.md` must equal the version in both plugin manifests.
When `scripts/check.py --release` runs, the matching `v<version>` tag must exist on `origin`.
Run `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v` before every release.
When adding an invariant to `AGENTS.md`, add the corresponding check.

## General Guidelines

- Never use the em dash or en dash. Use plain dash "-" instead.
- When writing commit messages, never auto-add your agent name as co-author.
- Never manually modify `CHANGELOG.md` files or any files that are marked as auto-generated.
- When writing or substantially editing long Markdown files, put each full sentence on its own line.
  Preserve normal Markdown structure, but avoid wrapping multiple sentences onto one physical line.
- When making technical decisions, do not give much weight to development cost.
  Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
- When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end user encounters it as possible.
  This makes sure you find the real problem so your fix will actually solve it.
- When end-to-end testing a product, be picky about the UI you see and be obsessed with pixel perfection.
  If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along.
- Apply that same high standard to engineering excellence: lint, test failures, and test flakiness.
  If you see one, even if it is not caused by what you are working on right now, still get it fixed.
