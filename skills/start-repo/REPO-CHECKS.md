# Repository Checks

Run every check read-only and report one table before proposing changes.

1. Use `<root>` resolved in phase 0. In `new` mode, verify that its path does not exist or is empty. In `restructure` mode, verify that the existing application repository exists, is readable, and is a Git repository; for the separate-folder branch, also verify that `<root>` has no conflicting content.
2. Check `app`, `client-note`, `prd`, `demos`, `routines`, `report/product`, and `<app-dir>/knowledge-base` against the selected mode without changing them.
3. Check whether `prd/roadmap.md` exists; if it does, classify the repository as already initialized and switch to report-only behavior for the roadmap.
4. Check whether `AGENTS.md`, `CLAUDE.md`, and `prd/evals/checklist.md` exist, and identify agent configuration files that duplicate instructions instead of pointing to `AGENTS.md`. If a root-level `REVIEW.md` exists instead, that is the old layout; see [SKILL.md](SKILL.md) phase 1 for the migration proposal.
5. Run `gh auth status`; if authenticated, ask which remote repository belongs to the product and whether GitHub Issues is an enabled task source.
6. Check whether a Notion connector is available; if unavailable, explain that the user must enable it in connector settings and this session cannot complete OAuth on its own.
7. If Notion is enabled, ask for the root product page or database.
8. Check whether `start-repo` and the remaining chain skills are available under the project `.claude/skills/` or `~/.claude/skills/`; if absent, point to `product-building-agents/link.sh` but do not run it.
9. Require Node 22 or newer and working `npx` for visual review.
10. Discover install, development, test, typecheck, lint, and build commands from the existing app manifest, `Makefile`, or `pyproject.toml`. A command counts only when discovery verifies it; there is no interview fallback.
11. In `restructure` mode, list the first-level directories in the existing application repository and compare them with every canonical role in [REPO-LAYOUT.md](REPO-LAYOUT.md), without changing anything.
12. In `restructure` mode, verify that the filesystem supports symlinks and that every proposed canonical link name has no collision at `<root>`.
13. Check whether `.gitignore` ignores `demos/prototypes/` and `.lavish/`; state that the scaffold does not edit `.gitignore`. In `restructure` mode, also propose ignoring the approved symlink names. Ask how `app/knowledge-base/` should be tracked only when `app/` is a real directory, with tracked README as the default until architecture defines runtime data behavior.
14. Count files in `<app-dir>/knowledge-base` and `client-note/` without changing either; explain that an empty evidence base means a longer concept interview. When `app/` is a symlink, report `app/knowledge-base/` as a TODO instead of creating it.

Record only verified project commands in the `Commands` section of `AGENTS.md`, and leave every other command as `TODO`.
Record enabled and disabled external sources plus GitHub and Notion roots under `Nguồn thông tin` in `prd/README.md`.
Do not invent missing commands or sources.
