---
name: start-repo
description: Initialize a product repository once with canonical instructions, quality gates, workspace structure, and the first product-building roadmap.
disable-model-invocation: true
---

# Start Repo

This is the one-time initialization command for a product repository.
After initialization, use `/update` to refresh progress and choose the next command.

## Ground rules

Resolve `<root>` in phase 0 before using it in any later phase.
Write chain documents only under `<root>/prd/`, production code only under `<root>/app/`, and prototypes only under `<root>/demos/prototypes/`.
Root governance files `AGENTS.md` and `CLAUDE.md` may be written only by `/start-repo`, after approval. The ship checklist at `prd/evals/checklist.md` is also seeded only by `/start-repo`, after approval.
Treat `client-note/` as read-only.
Read `app/knowledge-base/` freely, but never write there because it is runtime data owned by the application.
In the separate-folder branch of `restructure`, never create, edit, or delete anything inside the existing application repository, including `knowledge-base`.
Do not write chain files outside these destinations and approved root governance files.

Keep one canonical source for each fact.
`AGENTS.md` is canonical for commands, conventions, constraints, and the definition of done.
Reduce other agent instruction files to thin pointers plus genuinely tool-specific instructions.
Link to facts owned by another file instead of copying them.

Do not interview about the product, buyer, promise, or scope.
Those decisions belong to `/idea-to-product-concept`.
Record unknown setup facts as explicit TODOs and never invent project commands.

## Phase 0: choose the initialization mode

Ask whether this product needs `new` or `restructure` mode.
Use `new` only when no product code exists yet.
Use `restructure` whenever an application or product code already exists.

For `new`, ask for the product repository path.
The approved scaffold will create the directory and initialize Git, so the user does not need to prepare it.

For `restructure`, ask these two paths in one batch:

1. The existing application repository.
2. The product repository, either in place at the application repository or in a separate folder beside it.

Resolve and print the resulting `<root>` before phase 1.
Do not create the directory or initialize Git until the phase 1 proposal is approved.

## Phase 1: inspect

Read [REPO-CHECKS.md](REPO-CHECKS.md) and [REPO-LAYOUT.md](REPO-LAYOUT.md), then perform every check read-only.
State the selected mode and whether an existing `<root>` is already initialized before any change.
Present exactly one table with `Item`, `Status`, and `Proposal` columns.
Do not create files, initialize Git, authenticate services, or create directories before approval.

If `prd/roadmap.md` already exists, report what exists and what is missing.
Propose only the missing files, never modify `prd/roadmap.md`, skip phases 2 and 4 except for questions required to fill a missing file, and finish by directing the user to `/update`.

If a root-level `REVIEW.md` exists, that is the old layout. Propose migrating its content to `prd/evals/checklist.md` and deleting the root file, as one row in the phase 1 table, and wait for approval. Never overwrite `prd/evals/checklist.md` if it already exists.

## Phase 1b: propose the role mapping

Run this phase only in `restructure` mode.
Scan the existing code read-only, compare real folders with the roles in [REPO-LAYOUT.md](REPO-LAYOUT.md), and print exactly one mapping table:

| Canonical role | Proposal | Existing source | Reason |
|---|---|---|---|
| `app/` | symlink | `../my-running-app/` | that repository is the production application |
| `prd/` | symlink | `docs/product/` | existing product documents live here |
| `client-note/` | create | - | no folder matching customer voice was found |

Propose a symlink only when an existing folder genuinely matches the role.
Otherwise propose creating the canonical folder.
Never propose symlinks for `routines/` or `report/`; those belong to the product repository.

For the in-place branch, do not symlink `app/`.
Detect the real production code path such as `src/` or `apps/web/`, record it as `app-dir` in the `AGENTS.md` mapping, and scaffold with `--retrofit --app-dir <detected-path>`.
For the separate-folder branch, propose `app/` as a symlink to the existing application repository.

Explain that writing through a symlink writes directly to its real target and that those changes belong to the Git history of the repository containing that target, not the product repository.
Wait for approval of every row before running the scaffold.
Do not reorganize or edit anything inside the existing application repository.

## Phase 2: interview setup

Ask exactly one question using `❓ **Q1** - **<title>**` followed by `➡️ <recommended answer>`.

Ask whether generated repository files should use Vietnamese or English.

## Phase 3: scaffold and fill canonical files

After approval, run the mode-appropriate scaffold command and relay its created, skipped, and symlink lists verbatim.
Use `python3 scripts/scaffold.py <root> --init-git` for `new`.
For the separate-folder branch of `restructure`, add `--init-git --no-knowledge-base` and every approved `--link ROLE=PATH` mapping.
For the in-place branch, use `--retrofit --app-dir <detected-path>` and every approved non-app `--link ROLE=PATH` mapping.

The scaffold never creates or edits `.gitignore`.
After symlinks are created, separately propose adding each symlink name to `.gitignore`, then apply only entries the user approves.
Fill `AGENTS.md` first, then `CLAUDE.md`, `prd/evals/checklist.md`, and `prd/README.md` from the templates in [assets](assets/).
In `AGENTS.md`, record the approved canonical-role mapping and whether each role is a symlink or a real directory.
In `new` mode, record that every role is a real directory in this repository.
Write a conservative permission posture into `AGENTS.md` and state how it may loosen after the review system proves reliable.
Populate commands only with values verified by check 10 in [REPO-CHECKS.md](REPO-CHECKS.md).
Leave every unverified command as `TODO`; do not ask and do not guess.
A missing command is safer than a plausible but incorrect command.
Leave product-specific quality criteria as the self-describing TODOs owned by `/to-prd` in the checklist template.
Always install both `weekly-ops-review.md` and `pr-auto-review.md` in `routines/`.
Do not fill or seed any file whose approved symlink resolves inside the existing application repository in the separate-folder branch.
If `.cursorrules`, `GEMINI.md`, or another agent configuration duplicates canonical instructions, propose reducing it to a thin pointer.
Translate the Vietnamese templates while filling them if the user selected English.

## Phase 4: initialize the chain and hand off

Explain steps 1 through 6 for someone seeing the workflow for the first time.
For every step, state the question it answers, the decision the user must make, its artifact and location, an honest time estimate, and evidence of completion.
Recommend one context window per step, `/clear` between steps, and `/clear` between implementation tickets.

Read [ROADMAP-FORMAT.md](ROADMAP-FORMAT.md) and create `prd/roadmap.md` for the first time.
Set all six product-building steps to not started.
Set the weekly goal to completing `prd/concept.md`.
Leave Out of scope empty with a note that `/idea-to-product-concept` will supply it.
Do not infer progress or add tasks.

Tell the user to use `/update`, not `/start-repo`, to refresh roadmap progress and choose future commands.
Finish with exactly `/idea-to-product-concept` as the next command and one sentence explaining why.
Do not start product code in the same turn.

## Repository operating rules to preserve

When roughly the same prompt is typed a third time, convert it into a skill.
Treat parallel sessions as separate people with shared context, separate tasks, separate output, and separate changes.
When the user challenges the workspace structure, read [PRINCIPLES.md](PRINCIPLES.md) and explain the relevant reason.
