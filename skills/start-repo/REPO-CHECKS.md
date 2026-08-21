# Repository Checks

Run every check read-only and report one table before proposing changes.
Checks are grouped by when they run: phase 2 runs before the mode and `<root>` are chosen, phase 4 runs after.

## Phase 2 checks

Run against the repository named in Q2, before the mode or `<root>` placement is decided.

1. Check which of `app`, `client-note`, `prd`, `demos`, `routines`, `report/product` already exist in the repository, and record their real paths, without changing anything.
2. Check whether `prd/roadmap.md` exists; if it does, classify the repository as already initialized and switch to report-only behavior for the roadmap.
3. Check whether `AGENTS.md`, `CLAUDE.md`, `prd/evals/checklist.md`, and `.claude/settings.json` exist, and identify agent configuration files that duplicate instructions instead of pointing to `AGENTS.md`. If a root-level `REVIEW.md` exists instead, that is the old layout; see [SKILL.md](SKILL.md) phase 4 for the migration proposal.
4. Discover install, development, test, typecheck, lint, and build commands from the existing app manifest, `Makefile`, or `pyproject.toml`. A command counts only when discovery verifies it; there is no interview fallback.
5. List the first-level directories in the repository and compare them with every canonical role in [REPO-LAYOUT.md](REPO-LAYOUT.md), without changing anything. Count how many roles already exist with real, matching content, and conclude how close the repository already is to the canonical layout. This conclusion drives the phase 3 placement proposal: a repository satisfying most roles is proposed to keep in place, not replaced or duplicated into a new folder.
6. Verify that the filesystem supports symlinks, as a general capability check; the actual proposed link names are checked for collisions again in phase 5 once a mapping is proposed.

## Phase 4 checks

Run against the `<root>` chosen in phase 3.

1. In `new` mode, verify that `<root>` does not exist or is empty. In `restructure` mode, verify that the existing application repository exists, is readable, and is a Git repository; for the separate-folder branch, also verify that `<root>` has no conflicting content.
2. Check whether the `gh` CLI is installed. When it is, run `gh auth status`; if authenticated, ask which remote repository belongs to the product and whether GitHub Issues is an enabled task source. When `gh` is absent, such as in a cloud session, fall back to the built-in GitHub tools for the same questions and state plainly that `gh` is not installed. If Q2 named a Git link not yet cloned, propose the clone destination and command here as one row.
3. Check whether a Notion connector is available; if unavailable, explain that the user must enable it in connector settings and this session cannot complete OAuth on its own.
4. If Notion is enabled, ask for the root product page or database.
5. For Claude Code, check whether `<root>/.claude/settings.json` declares `manhphanxiii` under `extraKnownMarketplaces` and enables `build@manhphanxiii`. This is what makes `/build:*` visible to a Claude Code cloud session, a second machine, or a teammate; a local Claude session with the plugin already enabled in user settings does not need it. Codex plugin installation is account or environment configuration and is not written into the product repository. If the Claude settings file is missing or lacks this declaration, the phase 4 table proposes seeding or patching it from [assets/settings.json.template](assets/settings.json.template).
6. Require Node 22 or newer and working `npx` for visual review.
   Also check whether `open` on macOS or `xdg-open` on Linux is available.
   Report whether the setup will use Lavish, the Artifact tool when that tool and `artifact-design` are available, or Markdown in the conversation.
   Treat a user-started asynchronous cloud run as interactive across turns and stop before writing until the user approves the Markdown draft.
7. Check whether `.gitignore` ignores `demos/prototypes/`; if it does, propose removing that line and tracking any prototype content already present but untracked, since prototypes are public evidence for their ADR and are the only artifact of a cloud-run spike that survives past the session. Check whether `.gitignore` ignores `.lavish/`, which should stay ignored; state that the scaffold does not edit `.gitignore`. In `restructure` mode, also propose ignoring the approved symlink names. Ask how `app/knowledge-base/` should be tracked only when `app/` is a real directory, with tracked README as the default until architecture defines runtime data behavior.
8. Count files in `<app-dir>/knowledge-base` and `client-note/` without changing either; explain that an empty evidence base means a longer concept interview. When `app/` is a symlink, report `app/knowledge-base/` as a TODO instead of creating it.

Record only verified project commands in the `Commands` section of `AGENTS.md`, and leave every other command as `TODO`.
Record enabled and disabled external sources plus GitHub and Notion roots under `Nguồn thông tin` in `prd/README.md`.
Do not invent missing commands or sources.
