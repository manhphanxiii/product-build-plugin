# Agent instructions

This is a self-contained skill chain for building a product from idea to code that has passed the ship gate.
Read `README.md` before changing anything in this folder.
Follow the three-destination rule: documents go into `prd/`, production code into `app/`, prototypes into `demos/prototypes/`.
If a destination directory is missing, the agent must state its path, propose creating it, and wait for approval.
`<root>` is the product repository and is never automatically the Git root of the current working directory: a skill uses the path the user supplied, requires `<root>/prd/roadmap.md` to exist, and never accepts this skill-set repository as `<root>`.
No skill writes chain artifacts into this repository, and every path in a skill without an explicit prefix is relative to `<root>`.
Never edit `client-note/` or runtime content in `app/knowledge-base/`.
This skill must not depend on anything outside its own folder, and must work correctly when installed as a plugin, which is the only supported installation path.
Do not reference the name, brand, or path of any other skill set in this folder, except `skills/lavish/`, a third-party MIT skill by Kun Chen vendored from <https://github.com/kunchenguid/lavish-axi>. Keep its `license` and `metadata.author` frontmatter intact.
`SKILL.md`, `AGENTS.md`, and `CLAUDE.md` are written in English; `README.md` is written in Vietnamese.
A skill calls another skill through the Skill tool by its namespaced name `build:<skill>`, not by file path, because every skill here ships inside the `build` plugin.
A script bundled with a skill is addressed as `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/scripts/<file>`, never by a path relative to the current working directory.
Keep the frontmatter and invocation policy in `agents/openai.yaml` always in sync.
This repo is installed only as a plugin, so a new skill is added by creating `skills/<name>/SKILL.md` and nothing else; `.claude-plugin/plugin.json` must not list skills individually.
When adding or renaming a skill, update the chain table and the install section in `README.md`.

## General Guidelines

- Never use the em dash "–". Use plain dash "-" instead.
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
